"""
Billing + marketplace licensing API — docs/HARDENING.md Phase 4.

Two routers, both mounted by api/server.py:

    router          — /billing/*  license admin (org-scoped, T1 per
                      docs/TENANCY.md) + optional Stripe self-serve checkout
    experts_router  — /experts/{agent_id}/chat  license-key-gated delivery
                      proxy (metered per call)

Stripe is OPTIONAL by design. Without STRIPE_API_KEY the platform still
issues 'manual' licenses via POST /billing/licenses (design partners pay by
invoice) and all gating / metering / revocation behaves identically; the
Stripe endpoints (/billing/checkout, /billing/webhook) then 404 cleanly.
With STRIPE_API_KEY (+ STRIPE_WEBHOOK_SECRET for the webhook) Stripe adds
self-serve subscription checkout on top: checkout.session.completed issues
the license, customer.subscription.deleted revokes it.

Key handling (atp/licensing.py stores only the key_id half — never the
secret):
  * The plaintext licenseKey is returned exactly ONCE — in the POST
    /billing/licenses response. Save it then or re-issue.
  * Webhook-issued keys are DISCARDED here after issuance (the webhook
    response goes to Stripe, not the customer) — delivery happens
    out-of-band via the billing portal / support until a customer portal
    ships.
  * GET /billing/licenses never returns key material (keyId, the public
    identifier half, is not key material).

Enforcement model for /experts/{agent_id}/chat: the route is on the
auth-middleware allowlist (bearer optional) but the handler calls
atp.licensing.check_license on EVERY request — a DB status read per call is
the enforcement, there is deliberately NO cache of check results, so
revoking a license cuts this path off on the very next call.

Org scoping: /billing/* admin routes take the org ONLY from verified
request.state (set by the auth middleware from the JWT — TENANCY.md layer 1).
The expert gate authenticates by license key instead; the license ROW
carries the org its usage is metered under.
"""

from __future__ import annotations

import os
import re
import sys

from fastapi import APIRouter, Depends, Header, HTTPException, Request
from pydantic import BaseModel

from api.auth import require_role
from atp import licensing, store

router = APIRouter(prefix="/billing")
experts_router = APIRouter(prefix="/experts")

#: Backend spec for the expert delivery proxy (agents/backend.get_backend).
#: The dry-run default keeps the delivery path CI-exercisable with no keys.
EXPERT_SPEC_ENV = "ATP_EXPERT_SPEC"
EXPERT_SPEC_DEFAULT = "dryrun:candidate"


# ── Tenancy helper (same idiom as api/atp.py) ───────────────────────────────

def _org(request: Request) -> str:
    """Org for this request — ONLY from verified auth state (TENANCY.md §4
    layer 1). 'org-demo' when auth is disabled / legacy single-admin token."""
    return getattr(request.state, "org_id", None) or "org-demo"


# ── Seed catalog helpers (T0 — atp/store.get_data) ─────────────────────────

def _agent(agent_id: str) -> dict | None:
    for a in store.get_data().get("AGENTS", []):
        if a.get("id") == agent_id:
            return a
    return None


def _top_cert_label(agent: dict) -> str:
    """Label of the agent's highest-layer cert (Stripe product naming)."""
    certs = {c.get("id"): c for c in store.get_data().get("CERTS", [])}
    held = [certs[cid] for cid in (agent.get("certIds") or []) if cid in certs]
    if not held:
        return ""
    top = max(held, key=lambda c: c.get("layer") or 0)
    return str(top.get("label") or "")


def _unit_amount_usd(price: str | None) -> int | None:
    """Seed licensing.price ('$4,800/mo') → Stripe unit_amount cents."""
    m = re.search(r"\$?\s*([0-9][0-9,]*(?:\.[0-9]+)?)", price or "")
    if not m:
        return None
    return int(round(float(m.group(1).replace(",", "")) * 100))


def _license_for_subscription(org_id: str,
                              subscription_id: str | None) -> dict | None:
    """The org's license bound to a Stripe subscription id, if any."""
    if not subscription_id:
        return None
    for row in licensing.list_licenses(org_id):
        if row.get("stripeSubscription") == subscription_id:
            return row
    return None


# ── Stripe (optional — endpoints 404 when unconfigured) ────────────────────

def _stripe_key() -> str | None:
    return os.environ.get("STRIPE_API_KEY") or None


def _stripe_configured_or_404():
    """Stripe endpoints don't exist without config — plain 404, no oracle."""
    if not _stripe_key():
        raise HTTPException(404, "Not Found")
    try:
        import stripe
    except ImportError as e:  # pragma: no cover — requirements.txt has it
        raise HTTPException(
            503, "stripe library not installed (pip install stripe)") from e
    stripe.api_key = _stripe_key()
    return stripe


def _cancel_subscription_best_effort(subscription_id: str | None) -> bool:
    """Cancel the Stripe subscription behind a revoked license. Best-effort
    by contract: the license is already revoked in OUR ledger (the expert
    gate is cut off regardless); a Stripe hiccup must not un-revoke it."""
    if not subscription_id or not _stripe_key():
        return False
    try:
        import stripe
        stripe.api_key = _stripe_key()
        stripe.Subscription.cancel(subscription_id)
        return True
    except Exception as e:  # noqa: BLE001 — best-effort by contract
        print(f"WARNING: stripe cancel of {subscription_id} failed: {e}",
              file=sys.stderr)
        return False


# ── License admin routes ────────────────────────────────────────────────────

class IssueBody(BaseModel):
    agentId: str
    kind: str = "production"   # licensing.VALID_KINDS
    expiresAt: str | None = None   # ISO-8601 UTC; None = perpetual


@router.post("/licenses", dependencies=[Depends(require_role("admin"))])
def billing_issue(body: IssueBody, request: Request):
    """Issue a 'manual' license for a marketplace agent (role admin).

    The Stripe-less path (design partners pay by invoice). Returns
    {license, licenseKey}; the plaintext licenseKey appears ONLY here —
    the engine stores just its key_id half.
    """
    try:
        return licensing.issue_license(_org(request), body.agentId, body.kind,
                                       expires_at=body.expiresAt)
    except licensing.UnknownAgentError as e:
        raise HTTPException(404, str(e)) from e
    except licensing.AgentNotLicensableError as e:
        raise HTTPException(400, str(e)) from e
    except ValueError as e:  # bad kind / expires_at
        raise HTTPException(400, str(e)) from e
    except licensing.LicenseSigningKeyError as e:
        raise HTTPException(503, str(e)) from e


@router.post("/licenses/{license_id}/reissue",
             dependencies=[Depends(require_role("admin"))])
def billing_reissue(license_id: str, request: Request):
    """Mint a fresh key for an active license (role admin). The previous key
    stops working immediately. This is how Stripe self-serve customers get
    their key: the webhook stores no plaintext, an org admin re-issues here
    and delivers it. Key shown ONCE."""
    try:
        return licensing.reissue_key(_org(request), license_id)
    except licensing.LicenseNotFoundError as e:
        raise HTTPException(404, str(e)) from e
    except ValueError as e:
        raise HTTPException(400, str(e)) from e
    except licensing.LicenseSigningKeyError as e:
        raise HTTPException(503, str(e)) from e


@router.get("/licenses",
            dependencies=[Depends(require_role("admin", "viewer"))])
def billing_licenses(request: Request):
    """Org's licenses, latest-first. Never contains key material — keys are
    shown once, at issue time (keyId is the public identifier half only)."""
    return {"licenses": licensing.list_licenses(_org(request))}


class RevokeBody(BaseModel):
    reason: str = ""


@router.post("/licenses/{license_id}/revoke",
             dependencies=[Depends(require_role("admin"))])
def billing_revoke(license_id: str, body: RevokeBody, request: Request):
    """Revoke a license (role admin, idempotent). Takes effect on the very
    next /experts call — the gate re-reads DB state every time. Cross-tenant
    ids 404 identically to unknown ids (TENANCY.md #6). When the license was
    Stripe-issued AND Stripe is configured, the subscription is cancelled
    too, best-effort."""
    try:
        revoked = licensing.revoke_license(
            _org(request), license_id, body.reason.strip() or "revoked by admin")
    except licensing.LicenseNotFoundError as e:
        raise HTTPException(404, f"license {license_id} not found") from e
    revoked["stripeCancelled"] = _cancel_subscription_best_effort(
        revoked.get("stripeSubscription"))
    return revoked


@router.get("/usage", dependencies=[Depends(require_role("admin", "viewer"))])
def billing_usage(request: Request, licenseId: str | None = None):
    """Metered usage for the org (optionally one license):
    {calls, tokensIn, tokensOut, byAgent}."""
    return licensing.usage_summary(_org(request), license_id=licenseId)


# ── Stripe self-serve checkout ──────────────────────────────────────────────

class CheckoutBody(BaseModel):
    agentId: str
    kind: str = "production"


@router.post("/checkout", dependencies=[Depends(require_role("admin"))])
def billing_checkout(body: CheckoutBody, request: Request):
    """Create a Stripe subscription Checkout Session for a seed listing.

    404 when STRIPE_API_KEY is unset (manual licensing still fully works).
    Price comes from the seed agent's licensing.price; the license itself is
    issued by the checkout.session.completed webhook, keyed by the metadata
    written here ({org_id, agent_id, kind} — org from verified state ONLY,
    so a tampered client cannot buy a license into another org).
    """
    stripe = _stripe_configured_or_404()
    org = _org(request)
    agent = _agent(body.agentId)
    if agent is None:
        raise HTTPException(404, f"agent {body.agentId} not found")
    if body.kind not in licensing.VALID_KINDS:
        raise HTTPException(
            400, f"kind must be one of {sorted(licensing.VALID_KINDS)}")
    seed_licensing = agent.get("licensing") or {}
    if not seed_licensing.get("available"):
        raise HTTPException(400, f"agent {body.agentId} is not licensable")
    unit_amount = _unit_amount_usd(seed_licensing.get("price"))
    if not unit_amount:
        raise HTTPException(
            400, f"agent {body.agentId} has no parseable price")

    label = _top_cert_label(agent)
    product_name = agent.get("name") or body.agentId
    if label:
        product_name = f"{product_name} — {label}"
    metadata = {"org_id": org, "agent_id": body.agentId, "kind": body.kind}
    base = (os.environ.get("BU_PUBLIC_URL")
            or request.headers.get("origin")
            or str(request.base_url)).rstrip("/")
    try:
        session = stripe.checkout.Session.create(
            mode="subscription",
            line_items=[{
                "quantity": 1,
                "price_data": {
                    "currency": "usd",
                    "unit_amount": unit_amount,
                    "recurring": {"interval": "month"},
                    "product_data": {"name": product_name},
                },
            }],
            # Session metadata drives checkout.session.completed issuance;
            # subscription_data.metadata puts the SAME keys on the
            # subscription object so customer.subscription.deleted can
            # resolve the org + license to revoke.
            metadata=metadata,
            subscription_data={"metadata": metadata},
            success_url=(base +
                         "/#/billing/success?session_id={CHECKOUT_SESSION_ID}"),
            cancel_url=base + "/#/billing/cancelled",
        )
    except Exception as e:  # noqa: BLE001 — stripe SDK error zoo
        raise HTTPException(502, f"stripe checkout failed: {e}") from e
    return {"url": session.url, "sessionId": session.id}


# ── Stripe webhook (public path — the signature IS the authentication) ─────

@router.post("/webhook")
async def billing_webhook(request: Request):
    """Stripe event sink. api/server.py adds this exact path to the auth
    allowlist: Stripe cannot send a bearer — every delivery is authenticated
    by its Stripe-Signature header, verified against STRIPE_WEBHOOK_SECRET
    (invalid/missing signature → 400; Stripe unconfigured → 404).

    Handled events (anything else is acknowledged and ignored):
      checkout.session.completed    → issue the license from the session
        metadata ({org_id, agent_id, kind} written by /billing/checkout),
        storing the Stripe customer/subscription ids. Idempotent across
        Stripe's retries (one license per subscription). The plaintext key
        is DISCARDED here — only its key_id persists, so it is not
        retrievable later (out-of-band delivery via the billing portal).
      customer.subscription.deleted → revoke the matching license
        (reason 'subscription cancelled').

    Responds 200 fast — handling is local DB writes only, no network calls.
    """
    if not _stripe_key() or not os.environ.get("STRIPE_WEBHOOK_SECRET"):
        raise HTTPException(404, "Not Found")
    import stripe

    payload = await request.body()
    sig_header = request.headers.get("stripe-signature", "")
    try:
        stripe.Webhook.construct_event(
            payload, sig_header, os.environ["STRIPE_WEBHOOK_SECRET"])
    except Exception as e:  # noqa: BLE001 — bad payload OR bad signature
        raise HTTPException(400, "invalid webhook signature") from e

    # construct_event verified signature + JSON; work on the verified bytes
    # as plain dicts (StripeObject's dict-likeness varies across versions).
    import json
    event = json.loads(payload)
    etype = event.get("type", "")
    obj = (event.get("data") or {}).get("object") or {}

    if etype == "checkout.session.completed":
        md = obj.get("metadata") or {}
        org, agent_id = md.get("org_id"), md.get("agent_id")
        kind = md.get("kind") or "production"
        if not (org and agent_id):
            return {"received": True, "handled": etype,
                    "skipped": "missing metadata"}
        subscription = obj.get("subscription")
        # Stripe retries deliveries — never double-issue for one sub.
        if subscription and _license_for_subscription(org, subscription):
            return {"received": True, "handled": etype,
                    "skipped": "already issued"}
        try:
            issued = licensing.issue_license(
                org, agent_id, kind,
                stripe_customer=obj.get("customer"),
                stripe_subscription=subscription)
        except (licensing.LicensingError, ValueError) as e:
            # Ack (200) so Stripe stops retrying a permanently-bad event,
            # but say what was wrong for the webhook log.
            print(f"WARNING: webhook license issue failed: {e}",
                  file=sys.stderr)
            return {"received": True, "handled": etype, "skipped": str(e)}
        # Hash-only persistence: the plaintext key never leaves this scope.
        return {"received": True, "handled": etype,
                "licenseId": issued["license"]["id"]}

    if etype == "customer.subscription.deleted":
        md = obj.get("metadata") or {}
        org, sub_id = md.get("org_id"), obj.get("id")
        if not (org and sub_id):
            return {"received": True, "handled": etype,
                    "skipped": "missing metadata"}
        row = _license_for_subscription(org, sub_id)
        if row is None:
            return {"received": True, "handled": etype,
                    "skipped": "no matching license"}
        licensing.revoke_license(org, row["id"], "subscription cancelled")
        return {"received": True, "handled": etype, "licenseId": row["id"]}

    return {"received": True, "ignored": etype}


# ── Expert delivery gate — /experts/{agent_id}/chat ─────────────────────────

class ChatBody(BaseModel):
    messages: list[dict]


def _persona(agent: dict) -> str:
    """Agent persona system prompt from T0 seed fields only (no tenant
    data — TENANCY.md leak surface #5)."""
    name = agent.get("name") or agent.get("id")
    level = agent.get("level")
    domains = ", ".join(agent.get("domains") or []) or "general"
    skills = ", ".join(
        s.get("name", "") for s in (agent.get("skills") or [])[:8])
    summary = (agent.get("reportCard") or {}).get("summary", "")
    boundaries = " ".join(
        f.get("boundary", "") for f in (agent.get("failures") or [])[:2])
    parts = [
        f"You are {name}, an ATP Level {level} certified expert agent "
        f"(domains: {domains}).",
        f"Certified skills: {skills}." if skills else "",
        summary,
        f"Known boundaries: {boundaries}" if boundaries else "",
        "Answer within your certified scope; when a request falls outside "
        "it, say so plainly and recommend human review.",
    ]
    return " ".join(p for p in parts if p)


def _flatten_messages(messages: list[dict]) -> str:
    """[{role, content}, ...] → one transcript string (backends take a
    single system + user pair, agents/backend.Backend.complete)."""
    parts = []
    for m in messages:
        if not isinstance(m, dict):
            continue
        role = str(m.get("role", "user")).strip().lower() or "user"
        content = str(m.get("content", "")).strip()
        if content:
            parts.append(f"{role.capitalize()}: {content}")
    return "\n\n".join(parts)


def _license_org(license_key: str) -> str | None:
    """Org the checked license row belongs to.

    check_license()'s public license dict intentionally carries no org key
    (atp/store.py convention), but metering must land under the license
    ROW's org (T1) — never under a caller-supplied value, and the keyed
    machine caller has no bearer/org at all. Resolve it through the same
    key-id lookup check_license used; the in-package coupling to
    licensing's _parse_key/_load_by_key_id is deliberate — the alternative
    (raw licenses SQL here) would break the DAL-only convention
    (TENANCY.md layer 2).
    """
    parsed = licensing._parse_key(license_key)
    if not parsed:
        return None
    row = licensing._load_by_key_id(parsed[0])
    return (row or {}).get("org_id")


_DENIED_403 = ("revoked", "expired")


@experts_router.post("/{agent_id}/chat")
def expert_chat(
    agent_id: str,
    body: ChatBody,
    request: Request,
    license_key: str | None = Header(default=None, alias="X-ATP-License-Key"),
):
    """Licensed expert delivery (HARDENING.md Phase 4).

    Authentication is the LICENSE KEY (X-ATP-License-Key header), not a
    bearer — api/server.py puts '/experts/' on the middleware allowlist and
    THIS handler enforces instead: atp.licensing.check_license runs on EVERY
    request (a DB status read — deliberately uncached, so revocation cuts
    the path off on the very next call). 401 invalid key / 403 revoked or
    expired (with the reason). Every successful call appends a usage_events
    row (metering).
    """
    if not license_key or not license_key.strip():
        raise HTTPException(
            401, "missing license key (X-ATP-License-Key header)")
    license_key = license_key.strip()

    try:
        check = licensing.check_license(license_key)
    except licensing.LicenseSigningKeyError as e:
        raise HTTPException(503, str(e)) from e
    if not check.get("ok"):
        reason = str(check.get("reason") or "invalid")
        if reason in _DENIED_403:
            raise HTTPException(403, f"license {reason}")
        raise HTTPException(401, f"invalid license key ({reason})")
    lic = check.get("license") or {}

    if lic.get("agentId") != agent_id:
        raise HTTPException(
            403, f"license is for agent {lic.get('agentId')}, not {agent_id}")

    agent = _agent(agent_id)
    if agent is None:  # licensed against a since-removed seed agent
        raise HTTPException(404, f"agent {agent_id} not found")

    transcript = _flatten_messages(body.messages or [])
    if not transcript:
        raise HTTPException(400, "messages must contain at least one "
                                 "non-empty {role, content} entry")

    from agents.backend import get_backend
    spec = os.environ.get(EXPERT_SPEC_ENV, EXPERT_SPEC_DEFAULT)
    system = _persona(agent)
    try:
        reply = get_backend(spec).complete(system, transcript)
    except Exception as e:  # noqa: BLE001 — backend/network failures
        raise HTTPException(503, f"expert backend unavailable: {e}") from e

    # Metering — approx token counts (chars/4). No usage row, no reply:
    # usage_events is the append-only billing record (HARDENING.md Phase 4).
    org = _license_org(license_key) or "org-demo"
    try:
        usage = licensing.record_usage(
            org, lic.get("id"), agent_id,
            endpoint=f"/experts/{agent_id}/chat",
            tokens_in=max(1, (len(system) + len(transcript)) // 4),
            tokens_out=max(1, len(reply or "") // 4),
            status="ok",
        )
    except Exception as e:  # noqa: BLE001
        raise HTTPException(503, f"usage metering failed: {e}") from e

    return {"reply": reply, "usage": usage}
