#!/usr/bin/env python3
"""
Seed referential-integrity gate — docs/HARDENING.md Phase 5 CI check.

Exit-code wrapper around the internal-consistency invariants the ATP seed
promises (atp/seed.py docstring + docs/ATP.md §3):

  * every certId / evidenceId / agentId / policyId / packId cross-reference
    anywhere in the seed resolves to a defined record
  * LAYERS.agentIds ⊆ AGENTS, bidirectional with AGENTS.level
  * MARKETPLACE lists only licensable agents (and every licensable agent
    is listed — ATP.md §3 seed content requirement)
  * COMPOSE (majors / badges / packs) certIds + policyIds resolve
  * EXPERT_REQUESTS statuses are valid + their cross-ids resolve
  * blueprint section weights sum ≈ 1 per cert
  * item banks (atp/items/<certId>.json) cover every blueprint section of
    their cert, and never name a section the blueprint doesn't have
  * skillEdges reference skill ids defined on the same agent

Usage:  python3 scripts/check_integrity.py
Exit 0 = all invariants hold; exit 1 = violations (each printed on stderr).
Stdlib-only on purpose (atp/seed.py is pure data) so CI needs no pip step.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from atp.seed import build_seed  # noqa: E402

ITEMS_DIR = ROOT / "atp" / "items"

#: EXPERT_REQUESTS lifecycle states the UI knows how to render
#: (design/screens/atp-marketplace.jsx STATUS map).
VALID_REQUEST_STATUSES = {"matched", "gap", "training", "certifying", "listed"}

#: seed key name → registry it must resolve in (generic reference sweep)
REF_KEYS = {
    "agentId": "agents",
    "agentIds": "agents",
    "matchedAgentId": "agents",
    "resultAgentId": "agents",
    "coveringAgentIds": "agents",
    "boundAgentIds": "agents",
    "bindsAgentIds": "agents",
    "certId": "certs",
    "certIds": "certs",
    "badgeIds": "certs",
    "evidenceIds": "evidence",
    "policyIds": "policies",
    "packId": "packs",
}

ERRORS: list[str] = []


def fail(msg: str) -> None:
    ERRORS.append(msg)


def sweep(node, registries: dict[str, set], path: str = "$") -> None:
    """Recursively resolve every REF_KEYS reference in the seed.

    Scalar reference keys may be None (e.g. EVIDENCE.certId for
    training-interaction rows, EXPERT_REQUESTS.matchedAgentId while a
    request is unfilled) — None means 'no reference', not a dangling one.
    """
    if isinstance(node, dict):
        for key, val in node.items():
            here = f"{path}.{key}"
            registry = REF_KEYS.get(key)
            if registry is not None:
                ids = registries[registry]
                refs = val if isinstance(val, list) else [val]
                for ref in refs:
                    if ref is None:
                        continue
                    if not isinstance(ref, str) or ref not in ids:
                        fail(f"{here}: dangling {registry} reference {ref!r}")
            sweep(val, registries, here)
    elif isinstance(node, list):
        for i, item in enumerate(node):
            sweep(item, registries, f"{path}[{i}]")


def check_layers(data: dict, agent_ids: set) -> None:
    """LAYERS.agentIds ⊆ AGENTS + level ↔ layer membership is bidirectional."""
    placed: dict[str, int] = {}
    for layer in data["LAYERS"]:
        for aid in layer["agentIds"]:
            if aid not in agent_ids:
                fail(f"LAYERS[{layer['id']}].agentIds: unknown agent {aid!r}")
            elif aid in placed:
                fail(f"agent {aid!r} appears in two layers "
                     f"(L{placed[aid]} and {layer['id']})")
            else:
                placed[aid] = layer["n"]
    for agent in data["AGENTS"]:
        if placed.get(agent["id"]) != agent["level"]:
            fail(f"agent {agent['id']!r} has level {agent['level']} but sits "
                 f"in layer {placed.get(agent['id'])} (LAYERS.agentIds)")


def check_marketplace(data: dict) -> None:
    """Marketplace ↔ licensable agents, both directions (ATP.md §3)."""
    licensable = {a["id"] for a in data["AGENTS"]
                  if (a.get("licensing") or {}).get("available")}
    listed = [entry["agentId"] for entry in data["MARKETPLACE"]["listings"]]
    for aid in listed:
        if aid not in licensable:
            fail(f"MARKETPLACE lists {aid!r}, which is not licensable "
                 f"(licensing.available != true)")
    if len(set(listed)) != len(listed):
        fail("MARKETPLACE has duplicate listings for one agent")
    for aid in sorted(licensable - set(listed)):
        fail(f"agent {aid!r} is licensable but has no MARKETPLACE listing")


def check_expert_requests(data: dict) -> None:
    pack_ids = {p["id"] for p in data["COMPOSE"]["packs"]}
    for req in data["EXPERT_REQUESTS"]:
        rid = req.get("id", "?")
        if req.get("status") not in VALID_REQUEST_STATUSES:
            fail(f"EXPERT_REQUESTS[{rid}]: invalid status {req.get('status')!r} "
                 f"(valid: {sorted(VALID_REQUEST_STATUSES)})")
        pack = req.get("packId")
        if pack is not None and pack not in pack_ids:
            fail(f"EXPERT_REQUESTS[{rid}]: unknown packId {pack!r}")


def check_blueprint_weights(data: dict, tolerance: float = 1e-3) -> None:
    for cert in data["CERTS"]:
        sections = (cert.get("blueprint") or {}).get("sections") or []
        if not sections:
            fail(f"cert {cert['id']!r}: blueprint has no sections")
            continue
        total = sum(s.get("weight", 0) for s in sections)
        if abs(total - 1.0) > tolerance:
            fail(f"cert {cert['id']!r}: blueprint weights sum to {total:.4f}, "
                 f"expected ≈ 1.0")


def check_item_banks(data: dict) -> None:
    """Every atp/items/<certId>.json bank must belong to a seed cert and
    cover its blueprint sections exactly (atp/exams.py load contract:
    blueprints-before-commissioning)."""
    certs = {c["id"]: c for c in data["CERTS"]}
    for path in sorted(ITEMS_DIR.glob("*.json")):
        cert_id = path.stem
        cert = certs.get(cert_id)
        if cert is None:
            fail(f"item bank {path.name}: no seed cert {cert_id!r}")
            continue
        try:
            bank = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            fail(f"item bank {path.name}: unreadable ({exc})")
            continue
        items = bank.get("items") or []
        if not items:
            fail(f"item bank {path.name}: empty 'items' list")
            continue
        blueprint = {s["name"] for s in cert["blueprint"]["sections"]}
        banked = {item.get("section") for item in items}
        for section in sorted(banked - blueprint, key=str):
            fail(f"item bank {path.name}: section {section!r} is not in "
                 f"cert {cert_id!r}'s blueprint")
        for section in sorted(blueprint - banked):
            fail(f"item bank {path.name}: blueprint section {section!r} "
                 f"has no items")


def check_skill_edges(data: dict) -> None:
    for agent in data["AGENTS"]:
        skill_ids = {s["id"] for s in agent.get("skills") or []}
        for edge in agent.get("skillEdges") or []:
            for end in edge:
                if end not in skill_ids:
                    fail(f"agent {agent['id']!r}: skillEdge endpoint {end!r} "
                         f"is not one of its skills")


def main() -> int:
    data = build_seed()

    registries = {
        "agents": {a["id"] for a in data["AGENTS"]},
        "certs": {c["id"] for c in data["CERTS"]},
        "evidence": {e["id"] for e in data["EVIDENCE"]},
        "policies": {p["id"] for p in data["POLICIES"]},
        "packs": {p["id"] for p in data["COMPOSE"]["packs"]},
    }

    sweep(data, registries)
    check_layers(data, registries["agents"])
    check_marketplace(data)
    check_expert_requests(data)
    check_blueprint_weights(data)
    check_item_banks(data)
    check_skill_edges(data)

    counts = ", ".join(
        f"{len(registries[k])} {k}" for k in ("agents", "certs", "evidence", "policies"))
    if ERRORS:
        print(f"check_integrity: {len(ERRORS)} violation(s) across seed "
              f"({counts}):", file=sys.stderr)
        for err in ERRORS:
            print(f"  ✗ {err}", file=sys.stderr)
        return 1
    print(f"check_integrity: OK — {counts}, "
          f"{len(data['MARKETPLACE']['listings'])} listings, "
          f"{len(list(ITEMS_DIR.glob('*.json')))} item banks; "
          f"all cross-references resolve.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
