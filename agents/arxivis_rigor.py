"""
arXivis research-rigor scorer — automate the 10-criteria check a careful
research-assistant would do before quoting a paper:

  1. Hierarchy of evidence       (proof / empirical / theoretical / preliminary)
  2. Preliminary findings        (flag if "preliminary", "pilot", "initial")
  3. Correlation vs. causation   (flag if causal claim without controlled exp)
  4. Confounding variables       (credit ablation / controls / baselines)
  5. Conflicts of interest       (industry affiliation, funding declared)
  6. Publication bias            (preprint vs peer-reviewed venue)
  7. Replication                 (code / data link present?)
  8. Sample size                 (extract N / dataset count from abstract)
  9. Relative vs. absolute risk  (flag % improvement claims w/o absolute base)
 10. P-value                     (statistical significance explicitly reported)

Output per paper:
  rigor: {
    scores: {evidence: 0-3, preliminary: bool, causation_ok: bool, ...},
    flags:  {green: [labels], red: [labels]},
    total:  float (composite weight)
    summary: str (one-paragraph research-assistant note)
  }

Heuristic-only — no LLM. Fast, deterministic, runs in build pipeline.
"""

from __future__ import annotations

import re

# ── Patterns ─────────────────────────────────────────────────────────────

RE_PRELIMINARY = re.compile(r"\b(?:preliminary|pilot study|initial findings?|early[- ]stage|in progress|future work|work in progress|not yet (?:complete|reviewed))\b", re.I)
RE_CAUSAL_CLAIM = re.compile(r"\b(?:causes?|caused by|causal(?:ly)? (?:link|effect|relationship|mechanism)|leads to|results in)\b", re.I)
RE_CORRELATIONAL = re.compile(r"\b(?:correlat(?:ed|ion)|associated with|associat(?:ion|ed)|observed|observational|cross[- ]sectional|retrospective)\b", re.I)
RE_RANDOMIZED   = re.compile(r"\b(?:randomi[sz]ed|RCT|controlled trial|controlled experiment|A/B test)\b", re.I)
RE_PROOF        = re.compile(r"\b(?:we prove|theorem|lemma|proposition|corollary|proof of|formally prove)\b", re.I)
RE_META         = re.compile(r"\bmeta[- ]analysis\b", re.I)
RE_ABLATION     = re.compile(r"\b(?:ablat(?:ion|e[ds]?)|controlled for|control variable|baseline (?:comparison|experiment)|sanity check)\b", re.I)
RE_CODE         = re.compile(r"(?:github\.com|gitlab\.com|huggingface\.co|zenodo|open[- ]source|code (?:is )?(?:available|released|public)|we release|reproduce(?:d|s|ibility)|replicat(?:ed?|ion))", re.I)
RE_DATA_RELEASE = re.compile(r"\b(?:dataset (?:is )?(?:available|released|public)|we release the data|benchmark released)\b", re.I)
RE_SAMPLE_N     = re.compile(r"\b[Nn]\s*=\s*([\d,]+)\b")
RE_SUBJECTS     = re.compile(r"\b(\d{2,}[\d,]*)\s+(?:subjects?|participants?|patients?|users?|samples?|instances?|examples?|graphs?|datasets?)\b", re.I)
RE_BIG_DATASET  = re.compile(r"\b(?:million|billion|10\^?\d+)\b", re.I)
RE_PVAL         = re.compile(r"\bp\s*[<≤]\s*0?\.\d+|\bp[- ]value", re.I)
RE_SIGNIF       = re.compile(r"\b(?:statistically (?:significant|sig)|significant at)\b", re.I)
RE_PCT_IMPROVE  = re.compile(r"(?:improv(?:e[sd]?|ement)|increas(?:e[sd]?)|reduc(?:e[sd]?|tion))\s+(?:by|of)\s*(\d+(?:\.\d+)?)\s*%", re.I)
RE_ABS_NUMBERS  = re.compile(r"\b\d+(?:\.\d+)?\s*(?:absolute|points?|pp|percentage points?)\b", re.I)
RE_FUNDING      = re.compile(r"\b(?:funded by|funding from|grant (?:from )?|sponsored by)\b", re.I)
RE_INDUSTRY     = re.compile(r"\b(?:google|deepmind|microsoft|meta|facebook|amazon|nvidia|apple|openai|anthropic|ibm|baidu|alibaba|tencent|huawei|salesforce|netflix)\b", re.I)
RE_ARXIV_ONLY   = re.compile(r"\barxiv preprint\b", re.I)

# Venues that imply peer review — must be acronyms or unambiguous journal
# names to avoid common-word false positives (e.g. "science", "chi", "www").
PEER_VENUES = (
    "neurips", "icml", "iclr", "cvpr", "iccv", "eccv", "siggraph",
    "stoc", "focs", "soda", "podc", "spaa", "ijcai", "aaai",
    "jama", "lancet", "pnas", "kdd", "sigir", "vldb", "sigmod",
)
# Tighter pattern: "appeared in <venue>" / "published in <venue>" / "to appear in <venue>"
RE_VENUE_PHRASE = re.compile(
    r"\b(?:appeared|published|accepted|to appear)\s+(?:in|at)\s+([A-Z][A-Za-z0-9' /-]{3,40})", re.I
)


def _detect_evidence_tier(text: str) -> tuple[int, str]:
    """0=opinion/none, 1=theoretical/preliminary, 2=empirical observational,
    3=controlled experiment / proof / meta-analysis."""
    if RE_META.search(text):
        return 3, "meta-analysis"
    if RE_RANDOMIZED.search(text):
        return 3, "randomized / controlled trial"
    if RE_PROOF.search(text):
        return 3, "formal proof"
    if RE_PRELIMINARY.search(text):
        return 1, "preliminary"
    if RE_CORRELATIONAL.search(text):
        return 2, "observational / correlational"
    # Default to empirical if discussion of experiments
    if re.search(r"\b(?:experiment|evaluation|benchmark|empirical)\b", text, re.I):
        return 2, "empirical eval"
    return 1, "descriptive"


def _detect_sample_size(text: str) -> tuple[int | None, str]:
    """Return (N, description) or (None, '')."""
    m = RE_SAMPLE_N.search(text)
    if m:
        try:
            n = int(m.group(1).replace(",", ""))
            return n, f"N={n}"
        except ValueError:
            pass
    m = RE_SUBJECTS.search(text)
    if m:
        try:
            n = int(m.group(1).replace(",", ""))
            return n, f"{n} units"
        except ValueError:
            pass
    if RE_BIG_DATASET.search(text):
        return None, "large-scale (millions/billions)"
    return None, ""


def _detect_replication(text: str) -> dict:
    out = {"code": False, "data": False, "url": None}
    if RE_CODE.search(text):
        out["code"] = True
        # Try to pull URL
        url_match = re.search(r"https?://(?:github\.com|gitlab\.com|huggingface\.co|zenodo\.org)/[^\s\),\]]+", text)
        if url_match:
            out["url"] = url_match.group(0).rstrip(".,;")
    if RE_DATA_RELEASE.search(text):
        out["data"] = True
    return out


def _detect_venue(paper: dict, text: str) -> tuple[str, bool]:
    src = (paper.get("source") or "").lower()
    text_lc = text.lower()
    # Word-boundary match for venue acronyms (avoid "CHI" matching "machine")
    matched_venue = None
    for v in PEER_VENUES:
        if re.search(r"\b" + re.escape(v) + r"\b", text_lc):
            matched_venue = v
            break
    if matched_venue:
        return f"peer-reviewed ({matched_venue.upper()})", True
    venue_phrase = RE_VENUE_PHRASE.search(text)
    if venue_phrase:
        return f"published ({venue_phrase.group(1).strip()})", True
    if "arxiv" in src:
        return "preprint (unrefereed)", False
    if src in {"ntrs", "dtic"}:
        return f"government tech report ({src.upper()})", True
    if "openalex" in src:
        return "published (OpenAlex)", True
    return f"unknown venue ({src})", False


def _detect_conflict(text: str) -> tuple[bool, list[str]]:
    inds = sorted(set(m.group(0).lower() for m in RE_INDUSTRY.finditer(text)))
    has_funding_decl = bool(RE_FUNDING.search(text))
    return (len(inds) > 0 or has_funding_decl), inds


def _detect_causal_ok(text: str) -> tuple[bool, str]:
    has_causal_claim = bool(RE_CAUSAL_CLAIM.search(text))
    has_rct = bool(RE_RANDOMIZED.search(text))
    has_corr = bool(RE_CORRELATIONAL.search(text))
    if has_causal_claim and not has_rct and has_corr:
        return False, "causal claim from correlational data"
    if has_causal_claim and has_rct:
        return True, "causal claim backed by RCT"
    if has_causal_claim:
        return True, "causal claim (review for support)"
    return True, "no causal claim"


def _detect_risk_framing(text: str) -> tuple[bool, str]:
    """% improvement claims w/o absolute base = potential relative-only framing."""
    pct = RE_PCT_IMPROVE.search(text)
    if not pct:
        return True, "no % improvement claim"
    if RE_ABS_NUMBERS.search(text):
        return True, f"% improvement w/ absolute reference"
    return False, f"{pct.group(0)} — no absolute baseline shown"


def score_paper(paper: dict) -> dict:
    """Return rigor record for one paper."""
    text = (paper.get("title", "") + "\n" + (paper.get("text") or paper.get("pitch") or "")).strip()
    if not text:
        return {"total": 0, "summary": "no text to score", "scores": {}, "flags": {"green": [], "red": []}}

    green: list[str] = []
    red:   list[str] = []
    scores: dict = {}

    # 1. evidence
    ev_tier, ev_label = _detect_evidence_tier(text)
    scores["evidence_tier"] = ev_tier
    scores["evidence_label"] = ev_label
    if ev_tier >= 3:
        green.append(f"strong evidence: {ev_label}")
    elif ev_tier <= 1:
        red.append(f"weak evidence: {ev_label}")

    # 2. preliminary
    is_prelim = bool(RE_PRELIMINARY.search(text))
    scores["preliminary"] = is_prelim
    if is_prelim:
        red.append("self-described preliminary / pilot")

    # 3. causation
    caus_ok, caus_note = _detect_causal_ok(text)
    scores["causation_ok"] = caus_ok
    scores["causation_note"] = caus_note
    if not caus_ok:
        red.append("correlation/causation issue: " + caus_note)

    # 4. confounding / ablation
    has_ablation = bool(RE_ABLATION.search(text))
    scores["ablation"] = has_ablation
    if has_ablation:
        green.append("ablations / controlled comparisons")

    # 5. conflicts
    has_conflict, inds = _detect_conflict(text)
    scores["industry_affiliations"] = inds
    if inds:
        red.append("industry affiliations: " + ", ".join(inds[:3]))

    # 6. publication bias / venue
    venue_label, peer_reviewed = _detect_venue(paper, text)
    scores["venue"] = venue_label
    scores["peer_reviewed"] = peer_reviewed
    if peer_reviewed:
        green.append(f"venue: {venue_label}")
    else:
        red.append("not peer-reviewed: " + venue_label)

    # 7. replication
    repl = _detect_replication(text)
    scores["replication"] = repl
    if repl["code"]:
        green.append("code release detected" + (f" → {repl['url']}" if repl["url"] else ""))
    if repl["data"]:
        green.append("data release detected")
    if not (repl["code"] or repl["data"]):
        red.append("no code/data release found")

    # 8. sample size
    n, n_label = _detect_sample_size(text)
    scores["sample_n"]     = n
    scores["sample_label"] = n_label
    if n and n >= 1000:
        green.append(f"large sample: {n_label}")
    elif n and n < 30:
        red.append(f"small sample: {n_label}")
    elif not n and not n_label:
        # CS/theory papers often don't report N — neutral
        pass

    # 9. relative vs absolute risk
    risk_ok, risk_note = _detect_risk_framing(text)
    scores["risk_framing_ok"] = risk_ok
    if not risk_ok:
        red.append("relative-only metric: " + risk_note)

    # 10. p-value / significance
    has_pval = bool(RE_PVAL.search(text))
    has_signif = bool(RE_SIGNIF.search(text))
    scores["pvalue_reported"] = has_pval
    scores["significance_claimed"] = has_signif
    if has_pval:
        green.append("p-value reported")
    elif has_signif:
        red.append("'statistically significant' without explicit p-value")

    # Composite total: green +2 each, red -1 each, evidence tier *1.5, peer *3
    total = (
        2 * len(green)
        - 1 * len(red)
        + 1.5 * ev_tier
        + (3 if peer_reviewed else 0)
        + (2 if repl["code"] else 0)
        + (2 if not is_prelim else -2)
    )

    summary = _make_summary(paper, ev_label, peer_reviewed, repl, n_label,
                            is_prelim, caus_ok, has_ablation, has_conflict, inds,
                            risk_ok, has_pval)

    return {
        "total":   round(total, 1),
        "summary": summary,
        "scores":  scores,
        "flags":   {"green": green, "red": red},
    }


def _make_summary(paper, ev_label, peer_reviewed, repl, n_label, is_prelim,
                  caus_ok, has_ablation, has_conflict, inds,
                  risk_ok, has_pval) -> str:
    parts = []
    # Evidence
    parts.append(f"Evidence: {ev_label}.")
    # Venue
    parts.append("Peer-reviewed venue." if peer_reviewed else "Preprint / unrefereed.")
    # Replication
    if repl["code"]:
        parts.append("Code released.")
    elif repl["data"]:
        parts.append("Data released.")
    else:
        parts.append("No code/data link found.")
    # Sample
    if n_label:
        parts.append(f"Sample: {n_label}.")
    # Caveats
    if is_prelim:
        parts.append("⚠ self-described preliminary.")
    if not caus_ok:
        parts.append("⚠ causation claim under-supported.")
    if not risk_ok:
        parts.append("⚠ relative-only metric.")
    if has_conflict and inds:
        parts.append(f"⚠ industry affiliations: {', '.join(inds[:2])}.")
    if has_ablation:
        parts.append("Ablations present.")
    if has_pval:
        parts.append("p-value reported.")
    return " ".join(parts)


if __name__ == "__main__":
    sample = {
        "source": "arXiv",
        "title":  "Robust Mean Estimation",
        "text": ("We propose a near-linear time algorithm. We prove a tight bound."
                 "Code at https://github.com/example/x. We evaluate on N=10000 datasets."
                 "We improve by 35% over baseline; p < 0.01. Ablation studies confirm."),
    }
    import json
    print(json.dumps(score_paper(sample), indent=2))
