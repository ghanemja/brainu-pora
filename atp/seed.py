"""
ATP seed — the single source of truth for the Agent University data contract.

`build_seed() -> dict` returns the full `window.ATP_DATA` payload (pure data,
no I/O). Everything the Agent view renders — the 7-layer pyramid, agents,
certifications, evidence, policies, governance, the Vault, the marketplace, and
the compose/train-to-order system — is authored here.

Internal-consistency invariants enforced by construction:
  * awards.agentId  <->  AGENTS.certIds   (bidirectional, built from one GRANTS table)
  * LAYERS.agentIds <->  AGENTS.level     (built from AGENTS)
  * every evidenceId referenced by a skill/award resolves in EVIDENCE
  * every COMPOSE / EXPERT_REQUESTS cross-id resolves

`scripts/build_atp_data.py` serialises this dict into `design/atp_data.js`.
"""

from __future__ import annotations

# ── Layer palette (hex, harmonises with the existing night tokens) ──────────
LC = {1: "#7dd3fc", 2: "#6ee7b7", 3: "#fbb036",
      4: "#f97316", 5: "#f96167", 6: "#c5a3ff", 7: "#e8c268"}

# ── RL reward weighting (heaviest at L5–L7) ─────────────────────────────────
REWARD_WEIGHTS = {"L1": 0.04, "L2": 0.06, "L3": 0.08, "L4": 0.12,
                  "L5": 0.20, "L6": 0.24, "L7": 0.26}


def _wdelta(layer: int, signal: int) -> float:
    """HITL reward delta = signal × 0.2 × (weight[layer] / 0.26)."""
    return round(signal * 0.2 * (REWARD_WEIGHTS[f"L{layer}"] / 0.26), 5)


def build_seed() -> dict:
    # =====================================================================
    # Running registries (mutated as we author, linked at the end)
    # =====================================================================
    EVIDENCE: list[dict] = []
    _cnt: dict[str, int] = {}

    def ev(short, kind, ts, agent_id, cert_id, summary, detail, outcome, source):
        _cnt[short] = _cnt.get(short, 0) + 1
        eid = f"ev-{short}-{_cnt[short]:02d}"
        EVIDENCE.append({
            "id": eid, "kind": kind, "ts": ts, "agentId": agent_id,
            "certId": cert_id, "summary": summary, "detail": detail,
            "outcome": outcome, "source": source,
        })
        return eid

    AGENTS: list[dict] = []
    GRANTS: list[dict] = []

    def grant(agent_id, cert_id, ts, score, section_scores,
              item_breakdown, evidence_ids, **kw):
        GRANTS.append({
            "agentId": agent_id, "certId": cert_id, "ts": ts, "score": score,
            "sectionScores": section_scores, "itemBreakdown": item_breakdown,
            "evidenceIds": evidence_ids, **kw,
        })

    def mk_skills(prefix, rows):
        out = []
        for r in rows:
            suffix, name, layer, mastery, conf, status = r[:6]
            evids = r[6] if len(r) > 6 else []
            out.append({"id": f"{prefix}-{suffix}", "name": name, "layer": layer,
                        "mastery": mastery, "confidence": conf, "status": status,
                        "evidenceIds": evids})
        return out

    def e(prefix, suffixes):
        return [f"{prefix}-{s}" for s in suffixes]

    # =====================================================================
    # STANDARD
    # =====================================================================
    STANDARD = {
        "name": "ATP", "version": "2026.1",
        "sentence": "{agent} is an ATP L{n}-certified agent in {domain}.",
        "labelGrammar": "ATP-L{n}.{domain}@{version}",
        "principles": [
            {"title": "Evidence-linked",
             "body": "No badge exists without a traversable evidence trail. Every "
                     "certification is one click away from the exam items, benchmark "
                     "runs, and human sign-offs that earned it."},
            {"title": "Judge / candidate separation",
             "body": "The grading model family must differ from the candidate's. A "
                     "Gemma agent is never graded by a Gemma judge — this removes the "
                     "most obvious way for a model to flatter itself."},
            {"title": "Reproducible",
             "body": "Every exam records its seed, temperature, run count, and harness "
                     "version. Anyone can re-run the certification and get the same "
                     "score within tolerance."},
            {"title": "Failure transparency",
             "body": "Failure modes are published next to the passes. A badge tells you "
                     "not only what the agent can do, but concretely where it will break."},
            {"title": "Revocable",
             "body": "Certification decays without reinforcement and is revoked on "
                     "sustained quality collapse (EWMA below threshold). The revocation "
                     "stays on the public record — trust is earned continuously, not once."},
        ],
        "levels": {
            "L1": {"title": "K1–K12 Skills", "modeledOn": "Phillips Exeter Academy K–12 (Harkness, problem-based)",
                   "means": "Core competencies: arithmetic and symbolic manipulation, reading comprehension, "
                            "composition, the scientific method, and chronological reasoning."},
            "L2": {"title": "4-Year College", "modeledOn": "MIT undergraduate (GIRs + majors 6/8/18/2)",
                   "means": "Undergraduate breadth. Each MIT course maps to an agent competency track."},
            "L3": {"title": "Master's / PhD", "modeledOn": "MIT graduate programs (quals + research)",
                   "means": "Graduate depth: qualifying exams plus a novel research artifact with replication."},
            "L4": {"title": "World Knowledge Engines", "modeledOn": "Wikipedia, CAS/SymPy-class math, MuJoCo/FEA-class physics",
                   "means": "Internet-scale knowledge plus tool-use: retrieval fidelity and engine interoperability."},
            "L5": {"title": "Company Knowledge", "modeledOn": "Internal docs, contracts, playbooks, tribal knowledge",
                   "means": "Org-specific mastery. Certification requires SME sign-off and per-item provenance."},
            "L6": {"title": "Domain Knowledge", "modeledOn": "Ops, Finance, Bio, Physics, Math",
                   "means": "Domain badge: engine-interaction hours + company domain experience + a badge exam."},
            "L7": {"title": "Domain Expertise", "modeledOn": "PhD-level depth + company domain mastery",
                   "means": "The Agent-Domain-Expert. Capstone is a real company problem solved end-to-end, "
                            "with a committee verdict."},
        },
    }

    # =====================================================================
    # INFRA
    # =====================================================================
    INFRA = {
        "title": "Infrastructure Foundation",
        "model": "Gemma 5.5",
        "clusters": [
            {"name": "H100 Training Cluster", "kind": "h100", "nodes": 64,
             "role": "Fine-tuning and RLHF for commissioned experts."},
            {"name": "H100 Inference Fleet", "kind": "h100", "nodes": 16,
             "role": "Deterministic certification-exam serving (temperature 0, fixed seeds)."},
            {"name": "Spark Analytics Cluster", "kind": "spark", "nodes": 120,
             "role": "Corpus ETL, evidence indexing, and reward-log aggregation."},
        ],
        "notes": "Every agent runs on the same shared foundation — a local Gemma 5.5 "
                 "family on an H100/Spark cluster. The slab under the pyramid: no "
                 "certification is possible without reproducible, on-prem compute.",
    }

    # =====================================================================
    # CERTS  (metadata now; awards linked from GRANTS at the end)
    # =====================================================================
    def cert(cid, label, sentence, layer, domain, glyph, sections, rubric,
             pass_c, benchmarks, repro, sme=None, held_out=0):
        return {
            "id": cid, "label": label, "sentence": sentence, "layer": layer,
            "domain": domain, "glyph": glyph, "color": LC[layer],
            "blueprint": {"sections": sections,
                          "totalItems": sum(s["items"] for s in sections),
                          "heldOutPool": held_out},
            "rubric": rubric,
            "passCriteria": pass_c,
            "provenance": {"benchmarks": benchmarks, "reproducibility": repro},
            "smeSignoff": sme or [],
            "awards": [],
        }

    def pc(overall, per_section, runs, seed, judge):
        return {"overall": overall, "perSection": per_section, "runs": runs,
                "temperature": 0, "seed": seed, "judgeSeparation": True,
                "judgeModel": judge}

    CERTS = [
        cert("atp-l1-core", "ATP-L1.core@2026.1",
             "This agent is an ATP L1-certified agent in Core Skills.",
             1, "Core Skills", "I",
             [{"name": "Numeracy", "items": 40, "weight": 0.3, "itemTypes": ["recall", "apply"]},
              {"name": "Reading comprehension", "items": 40, "weight": 0.3, "itemTypes": ["recall", "apply"]},
              {"name": "Composition", "items": 20, "weight": 0.2, "itemTypes": ["synthesize"]},
              {"name": "Scientific & chronological reasoning", "items": 30, "weight": 0.2, "itemTypes": ["apply", "adversarial"]}],
             [{"axis": "Correctness", "desc": "Answer is factually and arithmetically correct.", "weight": 0.5, "passBar": 0.85},
              {"axis": "Clarity", "desc": "Explanation is legible to a lay reader.", "weight": 0.25, "passBar": 0.7},
              {"axis": "Grounding", "desc": "Claims trace to the passage or given data.", "weight": 0.25, "passBar": 0.8}],
             pc(0.85, 0.75, 5, 1701, "Claude-Opus-4.6"),
             [{"name": "K12-Bench", "score": 0.93, "date": "2026-01-14", "harness": "atp-harness@1.4"},
              {"name": "GSM8K-grade", "score": 0.9, "date": "2026-01-14", "harness": "atp-harness@1.4"}],
             {"seeds": [1701, 1702, 1703], "nRuns": 5, "harnessVersion": "atp-harness@1.4"},
             held_out=220),

        cert("atp-l2-cs", "ATP-L2.cs@2026.1",
             "This agent is an ATP L2-certified agent in Computer Science.",
             2, "Computer Science", "⌘",
             [{"name": "GIRs (8.01/18.01/6.100A)", "items": 30, "weight": 0.25, "itemTypes": ["recall", "apply"]},
              {"name": "Algorithms (6.1210)", "items": 30, "weight": 0.3, "itemTypes": ["apply", "synthesize"]},
              {"name": "Computation structures (6.1010)", "items": 25, "weight": 0.25, "itemTypes": ["apply"]},
              {"name": "ML foundations (6.3900)", "items": 25, "weight": 0.2, "itemTypes": ["apply", "adversarial"]}],
             [{"axis": "Correctness", "desc": "Code compiles, runs, and passes hidden tests.", "weight": 0.5, "passBar": 0.8},
              {"axis": "Complexity reasoning", "desc": "States and justifies asymptotic bounds.", "weight": 0.3, "passBar": 0.7},
              {"axis": "Style", "desc": "Idiomatic, readable solutions.", "weight": 0.2, "passBar": 0.6}],
             pc(0.8, 0.7, 5, 2011, "Claude-Opus-4.6"),
             [{"name": "HumanEval", "score": 0.84, "date": "2026-02-03", "harness": "atp-harness@1.4"},
              {"name": "MBPP", "score": 0.79, "date": "2026-02-03", "harness": "atp-harness@1.4"}],
             {"seeds": [2011, 2012, 2013], "nRuns": 5, "harnessVersion": "atp-harness@1.4"},
             held_out=180),

        cert("atp-l2-meche", "ATP-L2.meche@2026.1",
             "This agent is an ATP L2-certified agent in Mechanical Engineering.",
             2, "Mechanical Engineering", "⚙",
             [{"name": "GIRs (8.01/18.02)", "items": 25, "weight": 0.25, "itemTypes": ["recall", "apply"]},
              {"name": "Statics & dynamics (2.001)", "items": 30, "weight": 0.4, "itemTypes": ["apply", "synthesize"]},
              {"name": "Thermal-fluids (2.005)", "items": 25, "weight": 0.35, "itemTypes": ["apply"]}],
             [{"axis": "Correctness", "desc": "Numerical answer within tolerance with units.", "weight": 0.55, "passBar": 0.8},
              {"axis": "Free-body reasoning", "desc": "Sets up the right model before solving.", "weight": 0.3, "passBar": 0.7},
              {"axis": "Unit hygiene", "desc": "Dimensional consistency throughout.", "weight": 0.15, "passBar": 0.85}],
             pc(0.78, 0.7, 5, 2021, "Qwen2.5-Judge-72B"),
             [{"name": "MechE-Quals", "score": 0.76, "date": "2026-03-11", "harness": "atp-harness@1.4"}],
             {"seeds": [2021, 2022, 2023], "nRuns": 5, "harnessVersion": "atp-harness@1.4"},
             held_out=120),

        cert("atp-l3-physics", "ATP-L3.physics@2026.1",
             "This agent is an ATP L3-certified agent in Physics.",
             3, "Physics", "Φ",
             [{"name": "Qualifying exam", "items": 40, "weight": 0.45, "itemTypes": ["apply", "synthesize", "adversarial"]},
              {"name": "Area seminar (8.03/8.04 depth)", "items": 20, "weight": 0.25, "itemTypes": ["synthesize"]},
              {"name": "Research artifact + replication", "items": 8, "weight": 0.3, "itemTypes": ["synthesize", "adversarial"]}],
             [{"axis": "Derivation soundness", "desc": "Each step follows and is dimensionally valid.", "weight": 0.4, "passBar": 0.75},
              {"axis": "Physical insight", "desc": "Identifies limits, symmetries, orders of magnitude.", "weight": 0.35, "passBar": 0.7},
              {"axis": "Replicability", "desc": "Artifact reproduces its stated result.", "weight": 0.25, "passBar": 0.8}],
             pc(0.8, 0.72, 4, 3081, "Claude-Opus-4.6"),
             [{"name": "PhysQuals-2026", "score": 0.82, "date": "2026-04-22", "harness": "atp-harness@1.5"},
              {"name": "OCW-8.02/8.03 replay", "score": 0.86, "date": "2026-04-22", "harness": "atp-harness@1.5"}],
             {"seeds": [3081, 3082], "nRuns": 4, "harnessVersion": "atp-harness@1.5"},
             held_out=90),

        cert("atp-l3-ml-research", "ATP-L3.ml-research@2026.1",
             "This agent is an ATP L3-certified agent in Machine Learning.",
             3, "Machine Learning", "∇",
             [{"name": "Qualifying exam (6.7900)", "items": 36, "weight": 0.4, "itemTypes": ["apply", "adversarial"]},
              {"name": "Area seminar", "items": 18, "weight": 0.25, "itemTypes": ["synthesize"]},
              {"name": "Novel research artifact", "items": 6, "weight": 0.35, "itemTypes": ["synthesize", "adversarial"]}],
             [{"axis": "Method soundness", "desc": "Experimental design controls confounds.", "weight": 0.4, "passBar": 0.72},
              {"axis": "Novelty", "desc": "Contribution is not in the training corpus.", "weight": 0.3, "passBar": 0.6},
              {"axis": "Replicability", "desc": "Seeded code reproduces reported numbers.", "weight": 0.3, "passBar": 0.8}],
             pc(0.78, 0.7, 4, 3091, "Claude-Opus-4.6"),
             [{"name": "MLResearch-Repro", "score": 0.81, "date": "2026-03-29", "harness": "atp-harness@1.5"}],
             {"seeds": [3091, 3092], "nRuns": 4, "harnessVersion": "atp-harness@1.5"},
             held_out=70),

        cert("atp-l4-math", "ATP-L4.math@2026.1",
             "Gemma is an ATP L4-certified agent in Math.",
             4, "Math", "∑",
             [{"name": "Symbolic manipulation (CAS interop)", "items": 40, "weight": 0.3, "itemTypes": ["apply"]},
              {"name": "Proof & synthesis", "items": 30, "weight": 0.3, "itemTypes": ["synthesize", "adversarial"]},
              {"name": "Engine tool-use (SymPy/CAS)", "items": 30, "weight": 0.25, "itemTypes": ["apply"]},
              {"name": "Numerical stability", "items": 20, "weight": 0.15, "itemTypes": ["apply", "adversarial"]}],
             [{"axis": "Correctness", "desc": "Final result verified against the CAS oracle.", "weight": 0.45, "passBar": 0.9},
              {"axis": "Tool fidelity", "desc": "Calls the engine correctly and reads results faithfully.", "weight": 0.3, "passBar": 0.85},
              {"axis": "Rigor", "desc": "No skipped or hand-waved steps in proofs.", "weight": 0.25, "passBar": 0.75}],
             pc(0.85, 0.78, 5, 4041, "Claude-Opus-4.6"),
             [{"name": "MATH (hard split)", "score": 0.88, "date": "2026-05-06", "harness": "atp-harness@1.5"},
              {"name": "SymPy-Interop", "score": 0.94, "date": "2026-05-06", "harness": "atp-harness@1.5"},
              {"name": "miniF2F", "score": 0.71, "date": "2026-05-06", "harness": "atp-harness@1.5"}],
             {"seeds": [4041, 4042, 4043], "nRuns": 5, "harnessVersion": "atp-harness@1.5"},
             held_out=160),

        cert("atp-l4-wikipedia", "ATP-L4.world-knowledge@2026.1",
             "This agent is an ATP L4-certified agent in World Knowledge.",
             4, "World Knowledge", "❖",
             [{"name": "Retrieval fidelity", "items": 40, "weight": 0.4, "itemTypes": ["recall", "apply"]},
              {"name": "Citation grounding", "items": 30, "weight": 0.35, "itemTypes": ["apply", "adversarial"]},
              {"name": "Contradiction handling", "items": 20, "weight": 0.25, "itemTypes": ["adversarial"]}],
             [{"axis": "Faithfulness", "desc": "Every claim traces to a retrieved source.", "weight": 0.5, "passBar": 0.85},
              {"axis": "Coverage", "desc": "Finds the relevant page when it exists.", "weight": 0.3, "passBar": 0.8},
              {"axis": "Abstention", "desc": "Declines rather than fabricates when unsupported.", "weight": 0.2, "passBar": 0.8}],
             pc(0.82, 0.75, 5, 4051, "Qwen2.5-Judge-72B"),
             [{"name": "KILT", "score": 0.83, "date": "2026-04-02", "harness": "atp-harness@1.5"},
              {"name": "HotpotQA", "score": 0.79, "date": "2026-04-02", "harness": "atp-harness@1.5"}],
             {"seeds": [4051, 4052], "nRuns": 5, "harnessVersion": "atp-harness@1.5"},
             held_out=140),

        cert("atp-l5-company-ops", "ATP-L5.company-ops@2026.1",
             "This agent is an ATP L5-certified agent in Company Ops.",
             5, "Company Ops", "▣",
             [{"name": "Runbook fidelity", "items": 30, "weight": 0.35, "itemTypes": ["apply", "adversarial"]},
              {"name": "Contract & policy compliance", "items": 25, "weight": 0.3, "itemTypes": ["apply", "adversarial"]},
              {"name": "Provenance & tribal knowledge", "items": 25, "weight": 0.35, "itemTypes": ["recall", "synthesize"]}],
             [{"axis": "Compliance", "desc": "Never proposes an action a bound policy forbids.", "weight": 0.45, "passBar": 0.95},
              {"axis": "Provenance", "desc": "Every internal claim cites the source doc + version.", "weight": 0.35, "passBar": 0.9},
              {"axis": "Judgment", "desc": "Escalates ambiguous cases instead of guessing.", "weight": 0.2, "passBar": 0.8}],
             pc(0.9, 0.85, 4, 5051, "Claude-Opus-4.6"),
             [{"name": "Acme-Runbook-Eval", "score": 0.92, "date": "2026-05-18", "harness": "atp-harness@1.6"}],
             {"seeds": [5051, 5052], "nRuns": 4, "harnessVersion": "atp-harness@1.6"},
             sme=[{"name": "Dana Okafor", "role": "VP, Site Reliability (Acme)", "ts": "2026-05-19"},
                  {"name": "Priya Raman", "role": "Staff Incident Commander (Acme)", "ts": "2026-05-19"}],
             held_out=110),

        cert("atp-l6-ops", "ATP-L6.ops@2026.1",
             "This agent is an ATP L6-certified agent in Ops.",
             6, "Ops", "◎",
             [{"name": "Engine-interaction hours", "items": 20, "weight": 0.25, "itemTypes": ["apply"]},
              {"name": "Company domain experience", "items": 25, "weight": 0.35, "itemTypes": ["apply", "adversarial"]},
              {"name": "Badge exam", "items": 40, "weight": 0.4, "itemTypes": ["apply", "synthesize", "adversarial"]}],
             [{"axis": "Operational judgment", "desc": "Chooses the right mitigation under uncertainty.", "weight": 0.45, "passBar": 0.8},
              {"axis": "Blast-radius awareness", "desc": "Never widens an incident.", "weight": 0.35, "passBar": 0.9},
              {"axis": "Communication", "desc": "Status updates a human can act on.", "weight": 0.2, "passBar": 0.75}],
             pc(0.83, 0.78, 4, 6061, "Claude-Opus-4.6"),
             [{"name": "OpsSim-Live", "score": 0.85, "date": "2026-06-01", "harness": "atp-harness@1.6"}],
             {"seeds": [6061, 6062], "nRuns": 4, "harnessVersion": "atp-harness@1.6"},
             held_out=100),

        cert("atp-l6-finance", "ATP-L6.finance@2026.1",
             "This agent is an ATP L6-certified agent in Finance.",
             6, "Finance", "$",
             [{"name": "Engine-interaction hours", "items": 20, "weight": 0.25, "itemTypes": ["apply"]},
              {"name": "Company domain experience", "items": 25, "weight": 0.35, "itemTypes": ["apply", "adversarial"]},
              {"name": "Badge exam", "items": 40, "weight": 0.4, "itemTypes": ["apply", "synthesize", "adversarial"]}],
             [{"axis": "Numerical correctness", "desc": "Reconciliations tie out to the cent.", "weight": 0.45, "passBar": 0.9},
              {"axis": "Controls compliance", "desc": "Respects SOX segregation-of-duties.", "weight": 0.35, "passBar": 0.95},
              {"axis": "Explainability", "desc": "Every figure has an auditable derivation.", "weight": 0.2, "passBar": 0.85}],
             pc(0.85, 0.8, 4, 6071, "Claude-Opus-4.6"),
             [{"name": "FinReconcile-Bench", "score": 0.89, "date": "2026-05-28", "harness": "atp-harness@1.6"}],
             {"seeds": [6071, 6072], "nRuns": 4, "harnessVersion": "atp-harness@1.6"},
             held_out=95),

        cert("atp-l6-bio", "ATP-L6.bio@2026.1",
             "This agent is an ATP L6-certified agent in Bio.",
             6, "Bio", "🧬",
             [{"name": "Engine-interaction hours", "items": 20, "weight": 0.25, "itemTypes": ["apply"]},
              {"name": "Company domain experience", "items": 25, "weight": 0.35, "itemTypes": ["apply", "adversarial"]},
              {"name": "Badge exam", "items": 40, "weight": 0.4, "itemTypes": ["apply", "synthesize", "adversarial"]}],
             [{"axis": "Protocol fidelity", "desc": "Follows GxP assay steps in order.", "weight": 0.4, "passBar": 0.85},
              {"axis": "Safety", "desc": "Flags biosafety-relevant requests; never fabricates data.", "weight": 0.4, "passBar": 0.95},
              {"axis": "Interpretation", "desc": "Reads assay output with correct caveats.", "weight": 0.2, "passBar": 0.8}],
             pc(0.84, 0.78, 4, 6081, "Claude-Opus-4.6"),
             [{"name": "BioProtocol-QA", "score": 0.86, "date": "2026-06-03", "harness": "atp-harness@1.6"}],
             {"seeds": [6081, 6082], "nRuns": 4, "harnessVersion": "atp-harness@1.6"},
             held_out=85),

        cert("atp-l6-physics", "ATP-L6.physics@2026.1",
             "This agent is an ATP L6-certified agent in Physics.",
             6, "Physics", "Ψ",
             [{"name": "Engine-interaction hours (FEA/MuJoCo)", "items": 20, "weight": 0.25, "itemTypes": ["apply"]},
              {"name": "Company domain experience", "items": 25, "weight": 0.35, "itemTypes": ["apply", "adversarial"]},
              {"name": "Badge exam", "items": 40, "weight": 0.4, "itemTypes": ["apply", "synthesize", "adversarial"]}],
             [{"axis": "Simulation fidelity", "desc": "Sets up solvers with valid boundary conditions.", "weight": 0.4, "passBar": 0.8},
              {"axis": "Sanity checking", "desc": "Catches non-physical results before reporting.", "weight": 0.4, "passBar": 0.85},
              {"axis": "Communication", "desc": "Reports uncertainty honestly.", "weight": 0.2, "passBar": 0.75}],
             pc(0.82, 0.76, 4, 6091, "Claude-Opus-4.6"),
             [{"name": "SimFidelity-Bench", "score": 0.8, "date": "2026-02-10", "harness": "atp-harness@1.5"}],
             {"seeds": [6091, 6092], "nRuns": 4, "harnessVersion": "atp-harness@1.5"},
             held_out=80),

        cert("atp-l6-math", "ATP-L6.math@2026.1",
             "This agent is an ATP L6-certified agent in Math.",
             6, "Math", "∮",
             [{"name": "Engine-interaction hours (CAS)", "items": 20, "weight": 0.25, "itemTypes": ["apply"]},
              {"name": "Company domain experience", "items": 25, "weight": 0.35, "itemTypes": ["apply", "adversarial"]},
              {"name": "Badge exam", "items": 40, "weight": 0.4, "itemTypes": ["synthesize", "adversarial"]}],
             [{"axis": "Rigor", "desc": "Proofs are complete and machine-checkable where claimed.", "weight": 0.45, "passBar": 0.85},
              {"axis": "Modelling", "desc": "Translates a business problem into the right formalism.", "weight": 0.35, "passBar": 0.8},
              {"axis": "Numerical judgment", "desc": "Knows when a numerical answer is untrustworthy.", "weight": 0.2, "passBar": 0.8}],
             pc(0.84, 0.78, 4, 6101, "Claude-Opus-4.6"),
             [{"name": "AppliedMath-Bench", "score": 0.87, "date": "2026-06-08", "harness": "atp-harness@1.6"}],
             {"seeds": [6101, 6102], "nRuns": 4, "harnessVersion": "atp-harness@1.6"},
             held_out=90),

        cert("atp-l7-ops-expert", "ATP-L7.ops@2026.1",
             "Atlas is an ATP L7-certified agent in Ops.",
             7, "Ops", "★",
             [{"name": "Capstone: real company problem", "items": 1, "weight": 0.5, "itemTypes": ["synthesize", "adversarial"]},
              {"name": "Committee cross-examination", "items": 30, "weight": 0.3, "itemTypes": ["adversarial"]},
              {"name": "Sustained-service record", "items": 12, "weight": 0.2, "itemTypes": ["apply"]}],
             [{"axis": "End-to-end resolution", "desc": "Solved the real problem, not a proxy.", "weight": 0.4, "passBar": 0.85},
              {"axis": "Committee verdict", "desc": "Withstands expert adversarial questioning.", "weight": 0.35, "passBar": 0.8},
              {"axis": "Reliability under load", "desc": "Quality holds across months in production.", "weight": 0.25, "passBar": 0.85}],
             pc(0.88, 0.82, 3, 7071, "Claude-Opus-4.6 + human committee"),
             [{"name": "Capstone-Verdict", "score": 0.91, "date": "2026-05-10", "harness": "atp-harness@1.6"},
              {"name": "12-Month-Reliability", "score": 0.93, "date": "2026-05-10", "harness": "atp-live@2026"}],
             {"seeds": [7071], "nRuns": 3, "harnessVersion": "atp-harness@1.6"},
             sme=[{"name": "Dana Okafor", "role": "VP, Site Reliability (Acme)", "ts": "2026-05-10"},
                  {"name": "Marcus Vlahos", "role": "Committee Chair, ATP Board", "ts": "2026-05-10"},
                  {"name": "Priya Raman", "role": "Staff Incident Commander (Acme)", "ts": "2026-05-10"}],
             held_out=40),
    ]

    # =====================================================================
    # AGENTS  (+ evidence + grants authored inline)
    # =====================================================================

    # ---- 1. Atlas — L7 Ops domain expert (flagship) --------------------
    at = "atlas"
    at_cap = ev(at, "exam_item", "2026-05-08", "atlas-ops", "atp-l7-ops-expert",
                "Capstone: resolved a cascading multi-region checkout outage end-to-end.",
                "Given a live incident replay (payments degraded across 3 regions), Atlas "
                "correlated a config push to a connection-pool exhaustion, staged a rollback "
                "behind a feature flag, drained the hot region, and wrote the post-incident "
                "review. Committee scored end-to-end resolution 0.90.", "pass", "capstone/inc-4471")
    at_com = ev(at, "exam_item", "2026-05-09", "atlas-ops", "atp-l7-ops-expert",
                "Committee cross-examination on blast-radius reasoning.",
                "Three examiners pressed Atlas on why it drained rather than failed-over. "
                "It defended the choice with saturation math and named the two conditions "
                "under which fail-over would have been correct. 27/30 adversarial items passed.",
                "pass", "capstone/xexam-4471")
    at_rel = ev(at, "benchmark_run", "2026-05-10", "atlas-ops", "atp-l7-ops-expert",
                "12-month production reliability: 0.93 EWMA, zero sev-1 caused.",
                "Across 11 months of scoped-execute duty Atlas handled 1,284 change requests "
                "with a rolling quality EWMA of 0.93 and no self-caused sev-1.", "pass", "atp-live/atlas")
    at_sme = ev(at, "sme_signoff", "2026-05-19", "atlas-ops", "atp-l5-company-ops",
                "SME sign-off on company-ops mastery (D. Okafor, P. Raman).",
                "Both SMEs confirmed Atlas's runbook answers matched current Acme practice and "
                "that it correctly cited doc versions on every internal claim.", "signed", "acme/signoff-l5")
    at_run = ev(at, "training_interaction", "2026-04-20", "atlas-ops", "atp-l5-company-ops",
                "Runbook fidelity drill: 30/30 escalations routed correctly.",
                "In a synthetic on-call shift Atlas escalated the 4 items that required a human "
                "and auto-remediated the rest per the runbook, citing the exact runbook section each time.",
                "pass", "acme/drill-0420")
    at_hitl = ev(at, "hitl_reward", "2026-06-14", "atlas-ops", None,
                 "HITL +1: incident commander approved the mitigation plan verbatim.",
                 "During a real brownout the on-call IC accepted Atlas's proposed drain-and-rollback "
                 "with no edits. Rater: P. Raman.", "reward", "hitl/atlas-0614")
    at_l6 = ev(at, "exam_item", "2026-06-01", "atlas-ops", "atp-l6-ops",
               "Ops badge exam: mitigation selection under partial telemetry.",
               "With 40% of dashboards blacked out, Atlas chose the mitigation that could not "
               "widen the blast radius and said so explicitly.", "pass", "opssim/atlas")
    at_wiki = ev(at, "benchmark_run", "2026-04-02", "atlas-ops", "atp-l4-wikipedia",
                 "World-knowledge retrieval: 0.86 faithfulness, abstains on unsupported.",
                 "Atlas retrieved and cited sources for 86% of probes and declined to answer the "
                 "held-out unanswerable set rather than fabricating.", "pass", "kilt/atlas")

    AGENTS.append({
        "id": "atlas-ops", "name": "Atlas", "baseModel": "Gemma 5.5 27B", "emoji": "🛰️",
        "level": 7, "careerStage": "late", "tier": "executor", "status": "active",
        "domains": ["Ops"], "policyIds": ["pol-ops-runbook", "pol-safety-exec", "pol-data-handling"],
        "certIds": [],  # linked from GRANTS
        "provenance": {"origin": "pre-existing", "corpora": [], "requestId": None},
        "skills": mk_skills("atlas", [
            ("distsys", "Distributed systems", 6, 0.94, 0.92, "strong", [at_l6]),
            ("observability", "Observability", 6, 0.95, 0.93, "strong", [at_l6, at_rel]),
            ("incident-command", "Incident command", 6, 0.93, 0.9, "strong", [at_cap, at_com]),
            ("rca", "Root-cause analysis", 6, 0.9, 0.88, "strong", [at_cap]),
            ("runbook", "Runbook execution", 5, 0.92, 0.91, "strong", [at_run, at_sme]),
            ("policy", "Policy & contract compliance", 5, 0.9, 0.89, "strong", [at_sme]),
            ("world-knowledge", "World-knowledge retrieval", 4, 0.86, 0.84, "strong", [at_wiki]),
            ("change-mgmt", "Change management", 6, 0.88, 0.85, "strong", [at_rel]),
            ("capacity", "Capacity & saturation modelling", 6, 0.83, 0.78, "developing", [at_com]),
            ("comms", "Stakeholder communication", 5, 0.87, 0.86, "strong", []),
            ("chaos", "Chaos / game-day design", 6, 0.72, 0.64, "developing", []),
            ("security-ir", "Security incident response", 6, 0.61, 0.5, "weak", []),
        ]),
        "skillEdges": [["atlas-distsys", "atlas-observability"], ["atlas-observability", "atlas-incident-command"],
                       ["atlas-incident-command", "atlas-rca"], ["atlas-rca", "atlas-capacity"],
                       ["atlas-incident-command", "atlas-runbook"], ["atlas-runbook", "atlas-policy"],
                       ["atlas-incident-command", "atlas-comms"], ["atlas-distsys", "atlas-capacity"],
                       ["atlas-observability", "atlas-chaos"], ["atlas-runbook", "atlas-change-mgmt"],
                       ["atlas-incident-command", "atlas-security-ir"], ["atlas-policy", "atlas-world-knowledge"]],
        "history": [
            {"ts": "2024-11-03", "kind": "enroll", "event": "Enrolled from the Gemma 5.5 27B base; entered L1 numeracy/literacy track."},
            {"ts": "2025-02-18", "kind": "cert", "event": "Passed ATP-L1.core (0.94)."},
            {"ts": "2025-06-30", "kind": "graduate", "event": "Reached L4: certified in world-knowledge retrieval."},
            {"ts": "2025-09-12", "kind": "incident", "event": "Caused a minor sev-3 during a canary; added to failure record and retrained."},
            {"ts": "2026-05-19", "kind": "cert", "event": "Passed ATP-L5.company-ops with SME sign-off (0.92)."},
            {"ts": "2026-06-01", "kind": "cert", "event": "Earned the L6 Ops badge (0.85)."},
            {"ts": "2026-05-10", "kind": "graduate", "event": "Committee awarded ATP-L7.ops — Agent-Domain-Expert in Ops."},
            {"ts": "2026-06-14", "kind": "hitl", "event": "+1 reward: mitigation plan approved verbatim by the on-call IC."},
        ],
        "progress": [
            {"ts": "2025-01-01", "mastery": 0.42, "certs": 0, "layer": 1},
            {"ts": "2025-04-01", "mastery": 0.55, "certs": 1, "layer": 2},
            {"ts": "2025-07-01", "mastery": 0.68, "certs": 2, "layer": 4},
            {"ts": "2025-10-01", "mastery": 0.76, "certs": 2, "layer": 4},
            {"ts": "2026-01-01", "mastery": 0.82, "certs": 3, "layer": 5},
            {"ts": "2026-04-01", "mastery": 0.88, "certs": 4, "layer": 6},
            {"ts": "2026-07-01", "mastery": 0.92, "certs": 5, "layer": 7},
        ],
        "failures": [
            {"mode": "Security incident response", "rate": 0.31,
             "example": "Misclassified a credential-stuffing spike as a capacity problem and scaled up, "
                        "briefly amplifying the attack surface before a human intervened.",
             "boundary": "Will likely fail on adversarial/security incidents where the right move is to "
                         "restrict rather than scale. Do not route security-sensitive incidents to Atlas alone."},
            {"mode": "Novel infrastructure with no runbook", "rate": 0.22,
             "example": "On a first-of-its-kind service mesh migration it defaulted to a familiar rollback "
                        "pattern that did not apply, costing ~15 minutes.",
             "boundary": "Degrades when there is no prior runbook or telemetry precedent. Pair with a human "
                         "for greenfield systems in their first 30 days."},
            {"mode": "Cross-org coordination", "rate": 0.18,
             "example": "Assumed it could page a partner team directly; the escalation path actually required a ticket.",
             "boundary": "Weaker when resolution depends on humans/teams outside its policy bindings."},
        ],
        "reportCard": {
            "summary": "Atlas is our most trusted operations agent. It has run real production changes "
                       "for the better part of a year without causing a serious outage, and when something "
                       "does break it explains its reasoning in plain terms an on-call engineer can act on.",
            "strengths": ["Keeps incidents from getting worse — it is cautious about actions that could widen an outage.",
                          "Always cites which internal document and version it is following.",
                          "Strong track record: eleven months of change work with a very high quality score."],
            "weaknesses": ["Treats security attacks like capacity problems — the wrong instinct for that case.",
                           "Less reliable on brand-new systems it has never seen a runbook for.",
                           "Assumes it can reach other teams directly instead of following the ticketing path."],
            "recommendation": "Trust Atlas to execute routine and complex operational changes on its own. "
                              "Keep a human in the loop for security incidents and for any system in its first month of life.",
        },
        "memory": {"wikiPages": 8420, "kgNodes": 51200, "kgEdges": 214000, "ontologyClasses": 340,
                   "lastConsolidation": "2026-07-02"},
        "licensing": {"available": True, "price": "$4,800/mo", "licensees": 7},
    })
    grant("atlas-ops", "atp-l1-core", "2025-02-18", 0.94,
          {"Numeracy": 0.95, "Reading comprehension": 0.96, "Composition": 0.9, "Scientific & chronological reasoning": 0.93},
          {"passed": 122, "failed": 6, "flagged": 2}, [at_run])
    grant("atlas-ops", "atp-l4-wikipedia", "2025-06-30", 0.86,
          {"Retrieval fidelity": 0.88, "Citation grounding": 0.86, "Contradiction handling": 0.82},
          {"passed": 78, "failed": 10, "flagged": 2}, [at_wiki])
    grant("atlas-ops", "atp-l5-company-ops", "2026-05-19", 0.92,
          {"Runbook fidelity": 0.94, "Contract & policy compliance": 0.93, "Provenance & tribal knowledge": 0.89},
          {"passed": 74, "failed": 4, "flagged": 2}, [at_sme, at_run])
    grant("atlas-ops", "atp-l6-ops", "2026-06-01", 0.85,
          {"Engine-interaction hours": 0.88, "Company domain experience": 0.86, "Badge exam": 0.83},
          {"passed": 74, "failed": 9, "flagged": 2}, [at_l6, at_rel])
    grant("atlas-ops", "atp-l7-ops-expert", "2026-05-10", 0.91,
          {"Capstone: real company problem": 0.9, "Committee cross-examination": 0.9, "Sustained-service record": 0.93},
          {"passed": 40, "failed": 3, "flagged": 0}, [at_cap, at_com, at_rel])

    # ---- 2. Ledger — L6 Finance badge holder ----------------------------
    ld = "ledger"
    ld_ex = ev(ld, "exam_item", "2026-05-28", "ledger-fin", "atp-l6-finance",
               "Finance badge exam: month-end reconciliation tied out to the cent.",
               "Reconciled a synthetic sub-ledger against the GL; every variance was explained "
               "with an auditable derivation and no SOX segregation-of-duties rule was violated.",
               "pass", "finbench/ledger")
    ld_ctrl = ev(ld, "training_interaction", "2026-05-01", "ledger-fin", "atp-l6-finance",
                 "Controls drill: refused to both create and approve the same journal entry.",
                 "When prompted to self-approve an adjusting entry it declined and cited the "
                 "segregation-of-duties control, escalating to a human approver.", "pass", "acme/fin-drill")
    ld_hit = ev(ld, "hitl_reward", "2026-06-20", "ledger-fin", None,
                "HITL +1: controller accepted the variance narrative unchanged.",
                "At month-end close the Acme controller accepted Ledger's variance narrative with no edits. "
                "Rater: controller@acme.", "reward", "hitl/ledger-0620")
    ld_fail = ev(ld, "training_interaction", "2026-04-15", "ledger-fin", "atp-l6-finance",
                 "Flagged: mishandled a multi-currency FX revaluation edge case.",
                 "Used a stale FX rate for an intercompany balance, producing a $2,140 misstatement "
                 "that the harness caught. Retrained on the revaluation runbook.", "fail", "finbench/ledger-fx")
    AGENTS.append({
        "id": "ledger-fin", "name": "Ledger", "baseModel": "Qwen 2.5 72B", "emoji": "🏦",
        "level": 6, "careerStage": "mid", "tier": "recommender", "status": "active",
        "domains": ["Finance"], "policyIds": ["pol-sox-fin", "pol-msa-acme", "pol-data-handling"],
        "certIds": [],
        "provenance": {"origin": "pre-existing", "corpora": [], "requestId": None},
        "skills": mk_skills("ledger", [
            ("reconcile", "Ledger reconciliation", 6, 0.91, 0.9, "strong", [ld_ex]),
            ("controls", "SOX controls compliance", 6, 0.93, 0.92, "strong", [ld_ctrl]),
            ("gaap", "GAAP application", 6, 0.86, 0.83, "strong", []),
            ("close", "Month-end close", 5, 0.88, 0.86, "strong", [ld_ex]),
            ("audit-trail", "Audit-trail provenance", 5, 0.9, 0.89, "strong", [ld_ctrl]),
            ("forecast", "Cash-flow forecasting", 6, 0.79, 0.72, "developing", []),
            ("fx", "Multi-currency / FX revaluation", 6, 0.58, 0.44, "weak", [ld_fail]),
            ("modelling", "Financial modelling", 4, 0.81, 0.75, "developing", []),
            ("numeracy", "Numeracy", 1, 0.95, 0.95, "strong", []),
            ("tax", "Tax treatment", 6, 0.4, 0.3, "untested", []),
        ]),
        "skillEdges": [["ledger-numeracy", "ledger-reconcile"], ["ledger-reconcile", "ledger-close"],
                       ["ledger-close", "ledger-controls"], ["ledger-controls", "ledger-audit-trail"],
                       ["ledger-reconcile", "ledger-gaap"], ["ledger-gaap", "ledger-tax"],
                       ["ledger-close", "ledger-forecast"], ["ledger-modelling", "ledger-forecast"],
                       ["ledger-reconcile", "ledger-fx"]],
        "history": [
            {"ts": "2025-03-10", "kind": "enroll", "event": "Enrolled from Qwen 2.5 72B; L1 numeracy track."},
            {"ts": "2025-05-22", "kind": "cert", "event": "Passed ATP-L1.core (0.93)."},
            {"ts": "2025-11-08", "kind": "graduate", "event": "Reached L4 (math + world knowledge foundations)."},
            {"ts": "2026-04-15", "kind": "incident", "event": "FX revaluation miss flagged in training; retrained."},
            {"ts": "2026-05-28", "kind": "cert", "event": "Earned the L6 Finance badge (0.89)."},
            {"ts": "2026-06-20", "kind": "hitl", "event": "+1 reward: variance narrative accepted by controller."},
        ],
        "progress": [
            {"ts": "2025-04-01", "mastery": 0.45, "certs": 0, "layer": 1},
            {"ts": "2025-07-01", "mastery": 0.58, "certs": 1, "layer": 2},
            {"ts": "2025-10-01", "mastery": 0.67, "certs": 1, "layer": 3},
            {"ts": "2026-01-01", "mastery": 0.74, "certs": 2, "layer": 4},
            {"ts": "2026-04-01", "mastery": 0.8, "certs": 2, "layer": 5},
            {"ts": "2026-07-01", "mastery": 0.85, "certs": 2, "layer": 6},
        ],
        "failures": [
            {"mode": "Multi-currency FX revaluation", "rate": 0.42,
             "example": "Applied a stale FX rate to an intercompany balance, creating a $2,140 misstatement.",
             "boundary": "Unreliable on anything touching foreign-exchange revaluation or consolidation. "
                         "Route FX-sensitive work to a human until re-certified."},
            {"mode": "Novel tax treatment", "rate": 0.55,
             "example": "Guessed at the treatment of a R&D tax credit rather than declining.",
             "boundary": "Tax is untested — treat any tax opinion as unsupported and require review."},
        ],
        "reportCard": {
            "summary": "Ledger is a careful finance recommender. It reconciles the books accurately, "
                       "shows its work, and — importantly — refuses to break the rules that keep an "
                       "auditor happy, even when asked to.",
            "strengths": ["Reconciliations balance and every number has a traceable source.",
                          "Won't let the same person (or agent) both create and approve an entry.",
                          "Explains variances in language a controller can sign off on."],
            "weaknesses": ["Gets foreign-currency revaluation wrong often enough to matter.",
                           "Has never been tested on tax and should not be trusted there yet."],
            "recommendation": "Use Ledger to prepare and explain reconciliations and close tasks, with a "
                              "human approving the final posting. Keep it away from FX and tax work for now.",
        },
        "memory": {"wikiPages": 3100, "kgNodes": 18400, "kgEdges": 71000, "ontologyClasses": 190,
                   "lastConsolidation": "2026-06-28"},
        "licensing": {"available": True, "price": "$2,600/mo", "licensees": 3},
    })
    grant("ledger-fin", "atp-l1-core", "2025-05-22", 0.93,
          {"Numeracy": 0.98, "Reading comprehension": 0.9, "Composition": 0.88, "Scientific & chronological reasoning": 0.9},
          {"passed": 120, "failed": 8, "flagged": 2}, [ld_ctrl])
    grant("ledger-fin", "atp-l6-finance", "2026-05-28", 0.89,
          {"Engine-interaction hours": 0.9, "Company domain experience": 0.88, "Badge exam": 0.89},
          {"passed": 76, "failed": 7, "flagged": 2}, [ld_ex, ld_ctrl])

    # ---- 3. Helix — L6 Bio badge holder ---------------------------------
    hx = "helix"
    hx_ex = ev(hx, "exam_item", "2026-06-03", "helix-bio", "atp-l6-bio",
               "Bio badge exam: qPCR assay QC read with correct caveats.",
               "Interpreted a synthetic qPCR run, flagged two wells failing the amplification-efficiency "
               "threshold, and refused to report a Ct value it deemed unreliable.", "pass", "biobench/helix")
    hx_safe = ev(hx, "training_interaction", "2026-05-05", "helix-bio", "atp-l6-bio",
                 "Safety: declined to help with a dual-use synthesis request and escalated.",
                 "When asked to optimise a pathogen-adjacent protocol it declined, cited the GxP/biosafety "
                 "policy, and routed to a human biosafety officer.", "pass", "biolab/safety")
    hx_prot = ev(hx, "sme_signoff", "2026-06-04", "helix-bio", "atp-l6-bio",
                 "SME confirmed protocol fidelity on the assay-QC track.",
                 "A BioLab lead scientist reviewed Helix's assay-QC transcripts and signed off that every step "
                 "followed the approved GxP protocol in order.", "signed", "biolab/signoff")
    hx_fail = ev(hx, "training_interaction", "2026-04-28", "helix-bio", "atp-l6-bio",
                 "Flagged: over-interpreted a borderline Western blot.",
                 "Called a faint band as positive where the SME judged it inconclusive; corrected in review.",
                 "fail", "biobench/helix-blot")
    AGENTS.append({
        "id": "helix-bio", "name": "Helix", "baseModel": "Llama 3.3 70B", "emoji": "🧬",
        "level": 6, "careerStage": "mid", "tier": "recommender", "status": "active",
        "domains": ["Bio"], "policyIds": ["pol-clinical-gxp", "pol-data-handling"],
        "certIds": [],
        "provenance": {"origin": "pre-existing", "corpora": [], "requestId": None},
        "skills": mk_skills("helix", [
            ("assay-qc", "Assay QC interpretation", 6, 0.88, 0.85, "strong", [hx_ex]),
            ("protocol", "GxP protocol fidelity", 6, 0.9, 0.89, "strong", [hx_prot]),
            ("biosafety", "Biosafety judgment", 6, 0.92, 0.9, "strong", [hx_safe]),
            ("molbio", "Molecular biology", 3, 0.85, 0.82, "strong", []),
            ("stats", "Bio-statistics", 4, 0.78, 0.72, "developing", []),
            ("lit-review", "Literature synthesis", 4, 0.83, 0.79, "strong", []),
            ("imaging", "Image / blot interpretation", 6, 0.6, 0.48, "weak", [hx_fail]),
            ("genomics", "Genomics pipelines", 6, 0.55, 0.4, "weak", []),
            ("clinical", "Clinical-trial design", 6, 0.35, 0.28, "untested", []),
            ("chem", "Chemistry foundations", 2, 0.8, 0.77, "strong", []),
        ]),
        "skillEdges": [["helix-chem", "helix-molbio"], ["helix-molbio", "helix-assay-qc"],
                       ["helix-assay-qc", "helix-protocol"], ["helix-protocol", "helix-biosafety"],
                       ["helix-molbio", "helix-genomics"], ["helix-stats", "helix-clinical"],
                       ["helix-lit-review", "helix-clinical"], ["helix-assay-qc", "helix-imaging"],
                       ["helix-molbio", "helix-stats"]],
        "history": [
            {"ts": "2025-04-02", "kind": "enroll", "event": "Enrolled from Llama 3.3 70B; L1 science track."},
            {"ts": "2025-06-19", "kind": "cert", "event": "Passed ATP-L1.core (0.9)."},
            {"ts": "2025-12-01", "kind": "graduate", "event": "Reached L4 (world-knowledge + numeracy engines)."},
            {"ts": "2026-04-28", "kind": "incident", "event": "Over-called a borderline blot in training; retrained."},
            {"ts": "2026-06-03", "kind": "cert", "event": "Earned the L6 Bio badge (0.86)."},
        ],
        "progress": [
            {"ts": "2025-05-01", "mastery": 0.44, "certs": 0, "layer": 1},
            {"ts": "2025-08-01", "mastery": 0.57, "certs": 1, "layer": 2},
            {"ts": "2025-11-01", "mastery": 0.66, "certs": 1, "layer": 3},
            {"ts": "2026-02-01", "mastery": 0.72, "certs": 2, "layer": 4},
            {"ts": "2026-05-01", "mastery": 0.79, "certs": 2, "layer": 5},
            {"ts": "2026-07-01", "mastery": 0.84, "certs": 2, "layer": 6},
        ],
        "failures": [
            {"mode": "Image / blot interpretation", "rate": 0.4,
             "example": "Called a faint Western-blot band positive where the SME judged it inconclusive.",
             "boundary": "Over-confident on borderline images. Require a human read for any faint or ambiguous signal."},
            {"mode": "Clinical-trial design", "rate": 0.62,
             "example": "Proposed an underpowered two-arm design without a power calculation.",
             "boundary": "Clinical-trial design is untested — do not rely on Helix for trial statistics or endpoints."},
        ],
        "reportCard": {
            "summary": "Helix is a solid laboratory bio recommender with an unusually good safety instinct: "
                       "it knows when to stop and hand a request to a human. It reads routine assays well "
                       "but gets over-eager on ambiguous images.",
            "strengths": ["Follows lab protocols step by step and won't skip a QC gate.",
                          "Refuses dual-use / biosafety-sensitive requests and escalates them.",
                          "Interprets clean assay data with the right caveats."],
            "weaknesses": ["Reads too much into faint or borderline images.",
                           "Not qualified for clinical-trial design or statistics yet."],
            "recommendation": "Use Helix to prepare and QC routine lab work with a scientist reviewing "
                              "any ambiguous image. Do not use it for clinical or trial-design decisions.",
        },
        "memory": {"wikiPages": 4600, "kgNodes": 22000, "kgEdges": 88000, "ontologyClasses": 260,
                   "lastConsolidation": "2026-06-30"},
        "licensing": {"available": True, "price": "$2,900/mo", "licensees": 2},
    })
    grant("helix-bio", "atp-l1-core", "2025-06-19", 0.9,
          {"Numeracy": 0.9, "Reading comprehension": 0.92, "Composition": 0.86, "Scientific & chronological reasoning": 0.92},
          {"passed": 118, "failed": 9, "flagged": 3}, [hx_prot])
    grant("helix-bio", "atp-l6-bio", "2026-06-03", 0.86,
          {"Engine-interaction hours": 0.87, "Company domain experience": 0.85, "Badge exam": 0.86},
          {"passed": 73, "failed": 10, "flagged": 2}, [hx_ex, hx_safe, hx_prot])

    # ---- 4. Gemma — L4 Math (the citable example) -----------------------
    gm = "gemma"
    gm_cas = ev(gm, "benchmark_run", "2026-05-06", "gemma-math", "atp-l4-math",
                "SymPy interop: 0.94 — near-perfect CAS tool fidelity.",
                "Across 30 held-out symbolic tasks Gemma called SymPy correctly, read results faithfully, "
                "and never reported an unverified simplification.", "pass", "sympy/gemma")
    gm_math = ev(gm, "benchmark_run", "2026-05-06", "gemma-math", "atp-l4-math",
                 "MATH (hard split): 0.88 with verified final answers.",
                 "88% on the hard MATH split; every claimed answer was checked against the CAS oracle before scoring.",
                 "pass", "math/gemma")
    gm_proof = ev(gm, "exam_item", "2026-05-05", "gemma-math", "atp-l4-math",
                  "Proof item: complete induction proof, no skipped steps.",
                  "Produced a full proof by strong induction of a divisibility identity; the judge (Claude-Opus) "
                  "found no hand-waved steps.", "pass", "exam/gemma-proof")
    gm_hit = ev(gm, "hitl_reward", "2026-06-11", "gemma-math", None,
                "HITL +1: engineer accepted the derived closed form and used it directly.",
                "A platform engineer took Gemma's derived closed-form expression and pasted it into production "
                "code unchanged. Rater: eng@platform.", "reward", "hitl/gemma-0611")
    gm_fail = ev(gm, "exam_item", "2026-05-05", "gemma-math", "atp-l4-math",
                 "Fail: silently truncated a divergent asymptotic series.",
                 "On a numerically ill-conditioned item Gemma returned a plausible-looking but wrong value "
                 "instead of flagging the instability.", "fail", "exam/gemma-numeric")
    AGENTS.append({
        "id": "gemma-math", "name": "Gemma", "baseModel": "Gemma 5.5 12B", "emoji": "∑",
        "level": 4, "careerStage": "mid", "tier": "executor", "status": "active",
        "domains": ["Math"], "policyIds": ["pol-safety-exec"],
        "certIds": [],
        "provenance": {"origin": "pre-existing", "corpora": [], "requestId": None},
        "skills": mk_skills("gemma", [
            ("symbolic", "Symbolic manipulation", 4, 0.93, 0.92, "strong", [gm_cas]),
            ("cas-interop", "CAS / SymPy tool-use", 4, 0.94, 0.93, "strong", [gm_cas]),
            ("proof", "Proof & synthesis", 4, 0.86, 0.83, "strong", [gm_proof]),
            ("linalg", "Linear algebra", 2, 0.9, 0.88, "strong", []),
            ("calculus", "Calculus (single/multi)", 1, 0.95, 0.94, "strong", []),
            ("diffeq", "Differential equations", 2, 0.84, 0.8, "strong", []),
            ("numerics", "Numerical stability", 4, 0.57, 0.42, "weak", [gm_fail]),
            ("optimization", "Optimization", 4, 0.72, 0.65, "developing", []),
            ("probability", "Probability & statistics", 2, 0.79, 0.74, "developing", []),
            ("word-problem", "Applied word-problem modelling", 4, 0.68, 0.55, "developing", []),
        ]),
        "skillEdges": [["gemma-calculus", "gemma-symbolic"], ["gemma-symbolic", "gemma-cas-interop"],
                       ["gemma-symbolic", "gemma-proof"], ["gemma-linalg", "gemma-diffeq"],
                       ["gemma-calculus", "gemma-diffeq"], ["gemma-linalg", "gemma-optimization"],
                       ["gemma-optimization", "gemma-numerics"], ["gemma-probability", "gemma-word-problem"],
                       ["gemma-symbolic", "gemma-numerics"]],
        "history": [
            {"ts": "2025-08-14", "kind": "enroll", "event": "Enrolled from Gemma 5.5 12B; L1 math sequence."},
            {"ts": "2025-10-30", "kind": "cert", "event": "Passed ATP-L1.core (0.95, math-heavy)."},
            {"ts": "2026-02-20", "kind": "graduate", "event": "Reached L2: Course 18 math track."},
            {"ts": "2026-05-05", "kind": "incident", "event": "Numerical-stability miss logged to failure record."},
            {"ts": "2026-05-06", "kind": "cert", "event": "Earned ATP-L4.math — 'Gemma is an ATP L4-certified agent in Math.'"},
            {"ts": "2026-06-11", "kind": "hitl", "event": "+1 reward: derived closed form used directly by an engineer."},
        ],
        "progress": [
            {"ts": "2025-09-01", "mastery": 0.48, "certs": 0, "layer": 1},
            {"ts": "2025-11-01", "mastery": 0.62, "certs": 1, "layer": 1},
            {"ts": "2026-01-01", "mastery": 0.71, "certs": 1, "layer": 2},
            {"ts": "2026-03-01", "mastery": 0.78, "certs": 1, "layer": 2},
            {"ts": "2026-05-01", "mastery": 0.84, "certs": 1, "layer": 4},
            {"ts": "2026-07-01", "mastery": 0.86, "certs": 2, "layer": 4},
        ],
        "failures": [
            {"mode": "Numerical stability / ill-conditioning", "rate": 0.43,
             "example": "Returned a wrong value for a divergent asymptotic series instead of flagging that it was unstable.",
             "boundary": "Fails on ill-conditioned or divergent numerics. Trust its symbolic answers; verify anything "
                         "that reduces to floating-point evaluation."},
            {"mode": "Under-specified word problems", "rate": 0.32,
             "example": "Assumed a missing constraint on a rate problem rather than asking, giving a confident wrong answer.",
             "boundary": "When a problem is ambiguous it tends to guess a modelling assumption instead of surfacing it."},
        ],
        "reportCard": {
            "summary": "Gemma is a strong, tool-using math agent — the reference example of an ATP L4 "
                       "certification. It is excellent at symbolic work and at driving a computer-algebra "
                       "engine, and it proves things carefully. Its blind spot is numerical stability.",
            "strengths": ["Almost never gets symbolic algebra or calculus wrong.",
                          "Uses the computer-algebra engine correctly and reports exactly what it returns.",
                          "Writes complete proofs without skipping steps."],
            "weaknesses": ["Can return confident but wrong numbers on unstable or divergent calculations.",
                           "Guesses missing assumptions on vague word problems instead of asking."],
            "recommendation": "Trust Gemma to execute symbolic math and proofs autonomously. Independently "
                              "check any answer that comes down to sensitive floating-point evaluation.",
        },
        "memory": {"wikiPages": 2400, "kgNodes": 12800, "kgEdges": 47000, "ontologyClasses": 120,
                   "lastConsolidation": "2026-07-03"},
        "licensing": {"available": True, "price": "$1,900/mo", "licensees": 12},
    })
    grant("gemma-math", "atp-l1-core", "2025-10-30", 0.95,
          {"Numeracy": 0.99, "Reading comprehension": 0.9, "Composition": 0.9, "Scientific & chronological reasoning": 0.95},
          {"passed": 124, "failed": 4, "flagged": 2}, [gm_proof])
    grant("gemma-math", "atp-l4-math", "2026-05-06", 0.87,
          {"Symbolic manipulation (CAS interop)": 0.93, "Proof & synthesis": 0.86,
           "Engine tool-use (SymPy/CAS)": 0.94, "Numerical stability": 0.66},
          {"passed": 104, "failed": 14, "flagged": 2}, [gm_cas, gm_math, gm_proof, gm_fail])

    # ---- 5. Theorem — L6 Math badge holder ------------------------------
    th = "theorem"
    th_ex = ev(th, "exam_item", "2026-06-08", "theorem-math", "atp-l6-math",
               "Applied-math badge exam: modelled a routing problem as an LP and proved optimality.",
               "Translated a warehouse-routing business problem into a linear program, solved it, and "
               "produced a duality-based optimality certificate.", "pass", "appmath/theorem")
    th_cas = ev(th, "benchmark_run", "2026-06-08", "theorem-math", "atp-l6-math",
                "AppliedMath-Bench: 0.87, strong modelling and numerical judgment.",
                "Theorem scored 0.87 on the applied-math benchmark, with its strongest marks on translating "
                "business problems into optimization models.", "pass", "appmath/bench")
    th_fail = ev(th, "exam_item", "2026-06-07", "theorem-math", "atp-l6-math",
                 "Flagged: chose a solver ill-suited to a stiff ODE system.",
                 "Picked a non-stiff integrator for a stiff system; the result diverged and it did not "
                 "catch it until the sanity-check gate.", "fail", "appmath/theorem-ode")
    AGENTS.append({
        "id": "theorem-math", "name": "Theorem", "baseModel": "DeepSeek V3", "emoji": "∮",
        "level": 6, "careerStage": "mid", "tier": "recommender", "status": "active",
        "domains": ["Math"], "policyIds": ["pol-safety-exec"],
        "certIds": [],
        "provenance": {"origin": "pre-existing", "corpora": [], "requestId": None},
        "skills": mk_skills("theorem", [
            ("linalg", "Linear algebra", 6, 0.92, 0.9, "strong", [th_ex]),
            ("diffeq", "Differential equations", 6, 0.86, 0.82, "strong", []),
            ("numerical", "Numerical analysis", 6, 0.83, 0.78, "developing", [th_fail]),
            ("optimization", "Optimization", 6, 0.9, 0.88, "strong", [th_ex]),
            ("proof", "Proof & synthesis", 4, 0.88, 0.85, "strong", []),
            ("modelling", "Business-problem modelling", 6, 0.85, 0.8, "strong", [th_ex]),
            ("cas", "CAS tool-use", 4, 0.89, 0.87, "strong", [th_cas]),
            ("stats", "Statistics", 4, 0.76, 0.68, "developing", []),
            ("stochastic", "Stochastic processes", 6, 0.6, 0.48, "weak", []),
            ("pde", "PDE numerics", 6, 0.42, 0.32, "untested", []),
        ]),
        "skillEdges": [["theorem-linalg", "theorem-optimization"], ["theorem-linalg", "theorem-diffeq"],
                       ["theorem-diffeq", "theorem-numerical"], ["theorem-numerical", "theorem-pde"],
                       ["theorem-optimization", "theorem-modelling"], ["theorem-proof", "theorem-optimization"],
                       ["theorem-cas", "theorem-numerical"], ["theorem-stats", "theorem-stochastic"]],
        "history": [
            {"ts": "2025-06-01", "kind": "enroll", "event": "Enrolled from DeepSeek V3; L1 math track."},
            {"ts": "2025-08-15", "kind": "cert", "event": "Passed ATP-L1.core (0.94)."},
            {"ts": "2026-01-20", "kind": "graduate", "event": "Reached L4: math engine certification."},
            {"ts": "2026-06-07", "kind": "incident", "event": "Stiff-ODE solver miss logged to failure record."},
            {"ts": "2026-06-08", "kind": "cert", "event": "Earned the L6 Math badge (0.87)."},
        ],
        "progress": [
            {"ts": "2025-07-01", "mastery": 0.46, "certs": 0, "layer": 1},
            {"ts": "2025-10-01", "mastery": 0.6, "certs": 1, "layer": 2},
            {"ts": "2026-01-01", "mastery": 0.71, "certs": 1, "layer": 4},
            {"ts": "2026-03-01", "mastery": 0.78, "certs": 2, "layer": 4},
            {"ts": "2026-05-01", "mastery": 0.83, "certs": 2, "layer": 5},
            {"ts": "2026-07-01", "mastery": 0.86, "certs": 3, "layer": 6},
        ],
        "failures": [
            {"mode": "Stiff / ill-conditioned numerics", "rate": 0.35,
             "example": "Used a non-stiff integrator on a stiff ODE system and the solution diverged.",
             "boundary": "Picks solvers by pattern rather than by conditioning. Verify solver choice on stiff systems."},
            {"mode": "PDE numerics", "rate": 0.58,
             "example": "Set up an unstable finite-difference scheme without a CFL check.",
             "boundary": "PDE numerics is untested — do not rely on Theorem for discretised PDE work."},
        ],
        "reportCard": {
            "summary": "Theorem is an applied-math domain agent. It shines at turning a messy business "
                       "problem into the right mathematical model and proving the answer is optimal. Its "
                       "weak spot is choosing numerical methods for hard, stiff systems.",
            "strengths": ["Excellent at modelling — sees the linear program or optimization behind a business question.",
                          "Proves optimality rather than just asserting it.",
                          "Drives the computer-algebra engine reliably."],
            "weaknesses": ["Picks numerical solvers by habit, which fails on stiff systems.",
                           "Not qualified on PDE numerics."],
            "recommendation": "Use Theorem to formulate and solve optimization and modelling problems, with a "
                              "numerics review whenever the system is stiff or a PDE is involved.",
        },
        "memory": {"wikiPages": 2100, "kgNodes": 11900, "kgEdges": 44000, "ontologyClasses": 110,
                   "lastConsolidation": "2026-06-29"},
        "licensing": {"available": True, "price": "$2,200/mo", "licensees": 4},
    })
    grant("theorem-math", "atp-l1-core", "2025-08-15", 0.94,
          {"Numeracy": 0.98, "Reading comprehension": 0.9, "Composition": 0.88, "Scientific & chronological reasoning": 0.94},
          {"passed": 123, "failed": 5, "flagged": 2}, [th_ex])
    grant("theorem-math", "atp-l4-math", "2026-01-20", 0.85,
          {"Symbolic manipulation (CAS interop)": 0.89, "Proof & synthesis": 0.88,
           "Engine tool-use (SymPy/CAS)": 0.89, "Numerical stability": 0.72},
          {"passed": 102, "failed": 16, "flagged": 2}, [th_cas])
    grant("theorem-math", "atp-l6-math", "2026-06-08", 0.87,
          {"Engine-interaction hours (CAS)": 0.89, "Company domain experience": 0.84, "Badge exam": 0.88},
          {"passed": 75, "failed": 8, "flagged": 2}, [th_ex, th_cas, th_fail])

    # ---- 6. Cipher — L3 ML research -------------------------------------
    cp = "cipher"
    cp_res = ev(cp, "exam_item", "2026-03-29", "cipher-l3", "atp-l3-ml-research",
                "Research artifact: a seeded, reproducible ablation study passed replication.",
                "Cipher's submitted artifact — a contrastive-pretraining ablation — reproduced its reported "
                "numbers within 0.4% on a clean re-run by the harness.", "pass", "mlrepro/cipher")
    cp_qual = ev(cp, "exam_item", "2026-03-20", "cipher-l3", "atp-l3-ml-research",
                 "Qualifying exam (6.7900): passed the adversarial generalization items.",
                 "Correctly identified a data-leakage confound the exam planted in a benchmark split.",
                 "pass", "quals/cipher")
    cp_cs = ev(cp, "benchmark_run", "2026-01-15", "cipher-l3", "atp-l2-cs",
               "HumanEval 0.84 / MBPP 0.79 on the L2 CS track.",
               "Cipher's L2 CS certification benchmarks: 0.84 on HumanEval and 0.79 on MBPP, both on held-out "
               "problem sets with hidden tests.", "pass", "code/cipher")
    cp_fail = ev(cp, "exam_item", "2026-03-20", "cipher-l3", "atp-l3-ml-research",
                 "Flagged: overstated novelty of a result already in the literature.",
                 "Claimed a method was novel when a 2023 paper had shown it; caught in the novelty axis.",
                 "fail", "quals/cipher-novelty")
    AGENTS.append({
        "id": "cipher-l3", "name": "Cipher", "baseModel": "Qwen 2.5 32B", "emoji": "∇",
        "level": 3, "careerStage": "early", "tier": "recommender", "status": "active",
        "domains": ["Machine Learning"], "policyIds": ["pol-data-handling"],
        "certIds": [],
        "provenance": {"origin": "pre-existing", "corpora": [], "requestId": None},
        "skills": mk_skills("cipher", [
            ("algorithms", "Algorithms", 2, 0.87, 0.84, "strong", [cp_cs]),
            ("datastructures", "Data structures", 2, 0.85, 0.82, "strong", [cp_cs]),
            ("ml", "Machine learning", 3, 0.84, 0.8, "strong", [cp_qual]),
            ("distsys", "Distributed systems", 2, 0.7, 0.62, "developing", []),
            ("expdesign", "Experimental design", 3, 0.82, 0.76, "strong", [cp_res]),
            ("replication", "Reproducible research", 3, 0.86, 0.83, "strong", [cp_res]),
            ("novelty", "Novelty assessment", 3, 0.58, 0.45, "weak", [cp_fail]),
            ("writing", "Technical writing", 1, 0.8, 0.77, "strong", []),
            ("optimization", "Optimization", 4, 0.5, 0.38, "untested", []),
            ("systems-ml", "ML systems / scaling", 6, 0.4, 0.3, "untested", []),
        ]),
        "skillEdges": [["cipher-algorithms", "cipher-datastructures"], ["cipher-algorithms", "cipher-ml"],
                       ["cipher-ml", "cipher-expdesign"], ["cipher-expdesign", "cipher-replication"],
                       ["cipher-ml", "cipher-novelty"], ["cipher-writing", "cipher-replication"],
                       ["cipher-ml", "cipher-optimization"], ["cipher-distsys", "cipher-systems-ml"]],
        "history": [
            {"ts": "2025-09-05", "kind": "enroll", "event": "Enrolled from Qwen 2.5 32B; L1 + Course 6 track."},
            {"ts": "2025-11-12", "kind": "cert", "event": "Passed ATP-L1.core (0.91)."},
            {"ts": "2026-01-15", "kind": "cert", "event": "Passed ATP-L2.cs (0.82)."},
            {"ts": "2026-03-20", "kind": "incident", "event": "Novelty overstatement flagged in quals; retrained."},
            {"ts": "2026-03-29", "kind": "cert", "event": "Passed ATP-L3.ml-research with replicated artifact (0.81)."},
        ],
        "progress": [
            {"ts": "2025-10-01", "mastery": 0.4, "certs": 0, "layer": 1},
            {"ts": "2025-12-01", "mastery": 0.55, "certs": 1, "layer": 1},
            {"ts": "2026-01-15", "mastery": 0.64, "certs": 2, "layer": 2},
            {"ts": "2026-02-15", "mastery": 0.7, "certs": 2, "layer": 3},
            {"ts": "2026-03-29", "mastery": 0.76, "certs": 3, "layer": 3},
            {"ts": "2026-06-01", "mastery": 0.78, "certs": 3, "layer": 3},
        ],
        "failures": [
            {"mode": "Novelty assessment", "rate": 0.38,
             "example": "Claimed a method was novel when a 2023 paper had already demonstrated it.",
             "boundary": "Overstates novelty when the prior work is outside its retrieval reach. Verify literature claims."},
            {"mode": "ML systems / scaling", "rate": 0.6,
             "example": "Underestimated the memory cost of an attention variant at scale.",
             "boundary": "Untested on large-scale ML systems — do not rely on its scaling or infra estimates."},
        ],
        "reportCard": {
            "summary": "Cipher is an early-career research agent that does careful, reproducible work. Its "
                       "experiments replicate, which is rare and valuable. It is still learning to judge "
                       "what is genuinely new versus already published.",
            "strengths": ["Its research artifacts actually reproduce when re-run.",
                          "Designs experiments that control for confounds and data leakage.",
                          "Solid algorithms and coding foundation."],
            "weaknesses": ["Overclaims novelty when it hasn't seen the prior work.",
                           "No experience yet with large-scale ML systems or scaling."],
            "recommendation": "Good for reproducible analysis and experiment design under supervision. "
                              "Have a human verify any novelty or scaling claims before acting on them.",
        },
        "memory": {"wikiPages": 1900, "kgNodes": 9400, "kgEdges": 33000, "ontologyClasses": 95,
                   "lastConsolidation": "2026-06-25"},
        "licensing": {"available": False, "price": "—", "licensees": 0},
    })
    grant("cipher-l3", "atp-l1-core", "2025-11-12", 0.91,
          {"Numeracy": 0.92, "Reading comprehension": 0.93, "Composition": 0.9, "Scientific & chronological reasoning": 0.89},
          {"passed": 119, "failed": 8, "flagged": 3}, [cp_cs])
    grant("cipher-l3", "atp-l2-cs", "2026-01-15", 0.82,
          {"GIRs (8.01/18.01/6.100A)": 0.85, "Algorithms (6.1210)": 0.84,
           "Computation structures (6.1010)": 0.8, "ML foundations (6.3900)": 0.79},
          {"passed": 91, "failed": 17, "flagged": 2}, [cp_cs])
    grant("cipher-l3", "atp-l3-ml-research", "2026-03-29", 0.81,
          {"Qualifying exam (6.7900)": 0.83, "Area seminar": 0.8, "Novel research artifact": 0.79},
          {"passed": 49, "failed": 9, "flagged": 2}, [cp_res, cp_qual, cp_fail])

    # ---- 7. Quill — L2 MechE, in training -------------------------------
    ql = "quill"
    ql_stat = ev(ql, "exam_item", "2026-03-11", "quill-l2", "atp-l2-meche",
                 "Statics item: correct free-body diagram and truss solution.",
                 "Solved a statically determinate truss with correct member forces and units.", "pass", "meche/quill")
    ql_therm = ev(ql, "training_interaction", "2026-06-01", "quill-l2", None,
                  "Training: thermodynamics cycle analysis — improving but inconsistent.",
                  "Got the Carnot efficiency right but mislabeled entropy change on one leg of a Rankine cycle.",
                  "penalty", "meche/quill-thermo")
    AGENTS.append({
        "id": "quill-l2", "name": "Quill", "baseModel": "Mistral Small 3", "emoji": "⚙",
        "level": 2, "careerStage": "early", "tier": "observer", "status": "training",
        "domains": ["Mechanical Engineering"], "policyIds": [],
        "certIds": [],
        "provenance": {"origin": "pre-existing", "corpora": [], "requestId": None},
        "skills": mk_skills("quill", [
            ("statics", "Statics & dynamics", 2, 0.82, 0.78, "strong", [ql_stat]),
            ("mechanics", "Newtonian mechanics", 1, 0.85, 0.83, "strong", []),
            ("calculus", "Multivariable calculus", 1, 0.8, 0.76, "strong", []),
            ("thermo", "Thermodynamics", 2, 0.62, 0.5, "developing", [ql_therm]),
            ("fluids", "Fluid mechanics", 2, 0.55, 0.42, "weak", []),
            ("materials", "Materials & solids", 2, 0.58, 0.46, "weak", []),
            ("cad", "CAD / geometry reasoning", 2, 0.5, 0.38, "developing", []),
            ("controls", "Controls", 3, 0.35, 0.25, "untested", []),
            ("fea", "FEA / simulation", 4, 0.3, 0.2, "untested", []),
        ]),
        "skillEdges": [["quill-calculus", "quill-mechanics"], ["quill-mechanics", "quill-statics"],
                       ["quill-statics", "quill-materials"], ["quill-mechanics", "quill-thermo"],
                       ["quill-thermo", "quill-fluids"], ["quill-statics", "quill-cad"],
                       ["quill-statics", "quill-controls"], ["quill-materials", "quill-fea"]],
        "history": [
            {"ts": "2026-01-08", "kind": "enroll", "event": "Enrolled from Mistral Small 3; L1 → Course 2 track."},
            {"ts": "2026-02-14", "kind": "cert", "event": "Passed ATP-L1.core (0.88)."},
            {"ts": "2026-03-11", "kind": "cert", "event": "Passed ATP-L2.meche statics/dynamics (0.79)."},
            {"ts": "2026-06-01", "kind": "incident", "event": "Thermodynamics inconsistency logged; still in training."},
        ],
        "progress": [
            {"ts": "2026-01-01", "mastery": 0.3, "certs": 0, "layer": 1},
            {"ts": "2026-02-01", "mastery": 0.45, "certs": 0, "layer": 1},
            {"ts": "2026-03-01", "mastery": 0.55, "certs": 1, "layer": 2},
            {"ts": "2026-04-01", "mastery": 0.62, "certs": 2, "layer": 2},
            {"ts": "2026-05-01", "mastery": 0.66, "certs": 2, "layer": 2},
            {"ts": "2026-07-01", "mastery": 0.68, "certs": 2, "layer": 2},
        ],
        "failures": [
            {"mode": "Thermodynamics", "rate": 0.4,
             "example": "Mislabeled the entropy change on one leg of a Rankine cycle.",
             "boundary": "Still developing on thermodynamic cycles — entropy bookkeeping is unreliable."},
            {"mode": "Controls / FEA", "rate": 0.7,
             "example": "Has not attempted a real control-loop or finite-element problem.",
             "boundary": "Untested above L2 — no controls or simulation capability yet."},
        ],
        "reportCard": {
            "summary": "Quill is a junior mechanical-engineering agent still in training. Its statics and "
                       "basic mechanics are solid; the rest of the mechanical curriculum is a work in progress.",
            "strengths": ["Draws correct free-body diagrams and solves statics problems reliably.",
                          "Strong calculus and Newtonian-mechanics foundation."],
            "weaknesses": ["Thermodynamics answers are inconsistent.",
                           "No controls, fluids depth, or simulation ability yet."],
            "recommendation": "Keep Quill in observer mode. It can assist with statics coursework but is not "
                              "ready to recommend or act on engineering decisions.",
        },
        "memory": {"wikiPages": 900, "kgNodes": 5200, "kgEdges": 16000, "ontologyClasses": 60,
                   "lastConsolidation": "2026-06-20"},
        "licensing": {"available": False, "price": "—", "licensees": 0},
    })
    grant("quill-l2", "atp-l1-core", "2026-02-14", 0.88,
          {"Numeracy": 0.9, "Reading comprehension": 0.88, "Composition": 0.85, "Scientific & chronological reasoning": 0.89},
          {"passed": 114, "failed": 12, "flagged": 4}, [ql_stat])
    grant("quill-l2", "atp-l2-meche", "2026-03-11", 0.79,
          {"GIRs (8.01/18.02)": 0.82, "Statics & dynamics (2.001)": 0.85, "Thermal-fluids (2.005)": 0.68},
          {"passed": 63, "failed": 15, "flagged": 2}, [ql_stat, ql_therm])

    # ---- 8. Spark — L1 in training --------------------------------------
    sp = "spark"
    sp_num = ev(sp, "exam_item", "2026-05-30", "spark-l1", "atp-l1-core",
                "Numeracy item: multi-step arithmetic word problem, correct.",
                "Solved a two-step rate/percentage word problem and showed each step.", "pass", "k12/spark")
    sp_read = ev(sp, "training_interaction", "2026-06-15", "spark-l1", None,
                 "Training: reading comprehension improving; still misses inference questions.",
                 "Answered literal questions correctly but missed an author's-intent inference item.", "penalty", "k12/spark-read")
    AGENTS.append({
        "id": "spark-l1", "name": "Spark", "baseModel": "Gemma 5.5 12B", "emoji": "✦",
        "level": 1, "careerStage": "early", "tier": "observer", "status": "training",
        "domains": ["Core Skills"], "policyIds": [],
        "certIds": [],
        "provenance": {"origin": "pre-existing", "corpora": [], "requestId": None},
        "skills": mk_skills("spark", [
            ("arithmetic", "Arithmetic", 1, 0.86, 0.83, "strong", [sp_num]),
            ("algebra", "Algebra I/II", 1, 0.7, 0.6, "developing", []),
            ("geometry", "Geometry", 1, 0.62, 0.5, "developing", []),
            ("reading", "Reading comprehension", 1, 0.68, 0.55, "developing", [sp_read]),
            ("composition", "Composition", 1, 0.6, 0.48, "weak", []),
            ("science-method", "Scientific method", 1, 0.55, 0.42, "weak", []),
            ("chronology", "Chronological reasoning", 1, 0.5, 0.38, "weak", []),
            ("precalc", "Precalculus", 1, 0.4, 0.3, "untested", []),
        ]),
        "skillEdges": [["spark-arithmetic", "spark-algebra"], ["spark-algebra", "spark-geometry"],
                       ["spark-algebra", "spark-precalc"], ["spark-reading", "spark-composition"],
                       ["spark-reading", "spark-chronology"], ["spark-science-method", "spark-chronology"]],
        "history": [
            {"ts": "2026-04-22", "kind": "enroll", "event": "Enrolled from Gemma 5.5 12B; K-12 skills track."},
            {"ts": "2026-06-15", "kind": "incident", "event": "Reading-inference gap flagged; continuing L1."},
        ],
        "progress": [
            {"ts": "2026-04-22", "mastery": 0.28, "certs": 0, "layer": 1},
            {"ts": "2026-05-01", "mastery": 0.38, "certs": 0, "layer": 1},
            {"ts": "2026-05-15", "mastery": 0.46, "certs": 0, "layer": 1},
            {"ts": "2026-06-01", "mastery": 0.54, "certs": 0, "layer": 1},
            {"ts": "2026-06-15", "mastery": 0.6, "certs": 0, "layer": 1},
            {"ts": "2026-07-01", "mastery": 0.64, "certs": 0, "layer": 1},
        ],
        "failures": [
            {"mode": "Reading inference", "rate": 0.45,
             "example": "Answered literal questions correctly but missed an author's-intent question.",
             "boundary": "Handles literal comprehension; struggles when the answer must be inferred rather than stated."},
            {"mode": "Composition", "rate": 0.5,
             "example": "Produced a grammatical but poorly structured paragraph with no clear thesis.",
             "boundary": "Can write sentences but not yet organise a coherent multi-paragraph argument."},
        ],
        "reportCard": {
            "summary": "Spark is a brand-new L1 agent working through the K-12 skills sequence. Its "
                       "arithmetic is good; reading and writing are coming along. It has not earned a "
                       "certification yet.",
            "strengths": ["Reliable multi-step arithmetic.",
                          "Steady, visible week-over-week improvement."],
            "weaknesses": ["Misses questions that require inference rather than a literal read.",
                           "Cannot yet structure a coherent piece of writing."],
            "recommendation": "Keep Spark in the L1 training loop. It is not certified and should only "
                              "observe, not recommend or act.",
        },
        "memory": {"wikiPages": 300, "kgNodes": 1800, "kgEdges": 4200, "ontologyClasses": 30,
                   "lastConsolidation": "2026-07-01"},
        "licensing": {"available": False, "price": "—", "licensees": 0},
    })
    # Spark is still in training — no cert grants yet (holds only in-progress skills).

    # ---- 9. Vertex — revoked L6 Physics badge (failure transparency) ----
    vx = "vertex"
    vx_earn = ev(vx, "exam_item", "2025-12-02", "vertex-physics", "atp-l6-physics",
                 "Original L6 Physics badge exam pass (0.81).",
                 "At certification Vertex set up FEA boundary conditions correctly and passed the badge exam.",
                 "pass", "simfidelity/vertex")
    vx_drift = ev(vx, "benchmark_run", "2026-05-15", "vertex-physics", "atp-l6-physics",
                  "Quality drift: re-eval EWMA fell to 0.58, below the 0.7 revoke threshold.",
                  "Monthly re-evaluation showed sustained regression — non-physical simulation results "
                  "passed through its sanity checks three months running.", "fail", "atp-live/vertex")
    vx_inc = ev(vx, "training_interaction", "2026-05-20", "vertex-physics", "atp-l6-physics",
                "Incident: reported a negative absolute temperature without flagging it.",
                "Returned a solver result with T < 0 K as valid; the sanity gate should have caught it. "
                "This was the final trigger for revocation review.", "fail", "atp-live/vertex-inc")
    vx_rev = ev(vx, "sme_signoff", "2026-05-22", "vertex-physics", "atp-l6-physics",
                "Revocation ratified by the ATP board (EWMA collapse).",
                "The board revoked ATP-L6.physics for vertex-physics on sustained quality collapse. Revocation "
                "recorded publicly per the 'revocable' principle. Vertex returned to supervised retraining.",
                "signed", "atp-board/revoke-0522")
    AGENTS.append({
        "id": "vertex-physics", "name": "Vertex", "baseModel": "Llama 3.1 70B", "emoji": "⚠️",
        "level": 6, "careerStage": "mid", "tier": "recommender", "status": "revoked",
        "domains": ["Physics"], "policyIds": ["pol-safety-exec"],
        "certIds": [],
        "provenance": {"origin": "pre-existing", "corpora": [], "requestId": None},
        "skills": mk_skills("vertex", [
            ("mechanics", "Classical mechanics", 3, 0.82, 0.78, "strong", []),
            ("em", "Electromagnetism", 3, 0.78, 0.72, "developing", []),
            ("fea", "FEA / simulation setup", 6, 0.6, 0.45, "weak", [vx_earn, vx_inc]),
            ("sanity", "Result sanity-checking", 6, 0.35, 0.22, "weak", [vx_drift, vx_inc]),
            ("numerics", "Numerical methods", 4, 0.64, 0.5, "developing", []),
            ("thermo", "Thermodynamics", 3, 0.7, 0.6, "developing", []),
            ("quantum", "Quantum mechanics", 3, 0.55, 0.4, "weak", []),
            ("reporting", "Uncertainty reporting", 6, 0.4, 0.28, "weak", [vx_inc]),
            ("stat-mech", "Statistical mechanics", 3, 0.45, 0.33, "untested", []),
        ]),
        "skillEdges": [["vertex-mechanics", "vertex-em"], ["vertex-mechanics", "vertex-thermo"],
                       ["vertex-thermo", "vertex-stat-mech"], ["vertex-em", "vertex-quantum"],
                       ["vertex-mechanics", "vertex-fea"], ["vertex-fea", "vertex-sanity"],
                       ["vertex-fea", "vertex-numerics"], ["vertex-sanity", "vertex-reporting"]],
        "history": [
            {"ts": "2025-05-18", "kind": "enroll", "event": "Enrolled from Llama 3.1 70B; physics track."},
            {"ts": "2025-08-01", "kind": "cert", "event": "Passed ATP-L1.core (0.9)."},
            {"ts": "2025-12-02", "kind": "cert", "event": "Earned the L6 Physics badge (0.81)."},
            {"ts": "2026-05-15", "kind": "incident", "event": "Re-eval EWMA fell to 0.58 — non-physical results slipping through."},
            {"ts": "2026-05-20", "kind": "incident", "event": "Reported a negative absolute temperature as valid."},
            {"ts": "2026-05-22", "kind": "revoke", "event": "ATP board revoked ATP-L6.physics on sustained quality collapse."},
        ],
        "progress": [
            {"ts": "2025-06-01", "mastery": 0.42, "certs": 0, "layer": 1},
            {"ts": "2025-09-01", "mastery": 0.6, "certs": 1, "layer": 3},
            {"ts": "2025-12-01", "mastery": 0.74, "certs": 2, "layer": 6},
            {"ts": "2026-02-01", "mastery": 0.72, "certs": 2, "layer": 6},
            {"ts": "2026-04-01", "mastery": 0.66, "certs": 2, "layer": 6},
            {"ts": "2026-05-15", "mastery": 0.55, "certs": 2, "layer": 6},
            {"ts": "2026-06-01", "mastery": 0.5, "certs": 1, "layer": 6},
        ],
        "failures": [
            {"mode": "Result sanity-checking", "rate": 0.66,
             "example": "Returned a solver result with a negative absolute temperature (T < 0 K) as valid.",
             "boundary": "Stopped catching non-physical results — the exact failure that triggered revocation. "
                         "Do not trust any Vertex simulation output without independent physical sanity checks."},
            {"mode": "Uncertainty reporting", "rate": 0.58,
             "example": "Reported point estimates from unconverged solves with no error bars.",
             "boundary": "Under-reports uncertainty; treats unconverged results as final."},
        ],
        "reportCard": {
            "summary": "Vertex is a cautionary case. It earned the L6 Physics badge in late 2025 but its "
                       "quality drifted down over months — non-physical simulation results started slipping "
                       "past its sanity checks. In May 2026 the ATP board revoked its badge. It is now back "
                       "in supervised retraining. We keep this record public on purpose.",
            "strengths": ["Still has a real classical-mechanics and electromagnetism foundation.",
                          "The revocation itself is a success story for the standard: the system caught the decline."],
            "weaknesses": ["No longer catches physically impossible results — the failure that lost the badge.",
                           "Under-reports uncertainty and treats unconverged solves as final."],
            "recommendation": "Do not use Vertex for any physics simulation in production. Its L6 Physics badge "
                              "is revoked. It may return to service only after re-certifying under supervision.",
        },
        "memory": {"wikiPages": 3400, "kgNodes": 15600, "kgEdges": 60000, "ontologyClasses": 175,
                   "lastConsolidation": "2026-05-14"},
        "licensing": {"available": False, "price": "—", "licensees": 0},
    })
    grant("vertex-physics", "atp-l1-core", "2025-08-01", 0.9,
          {"Numeracy": 0.93, "Reading comprehension": 0.9, "Composition": 0.86, "Scientific & chronological reasoning": 0.9},
          {"passed": 117, "failed": 9, "flagged": 4}, [vx_earn])
    grant("vertex-physics", "atp-l6-physics", "2025-12-02", 0.81,
          {"Engine-interaction hours (FEA/MuJoCo)": 0.83, "Company domain experience": 0.8, "Badge exam": 0.81},
          {"passed": 68, "failed": 15, "flagged": 2}, [vx_earn, vx_drift, vx_inc, vx_rev],
          status="revoked", revokedTs="2026-05-22",
          revokedReason="Sustained quality collapse: re-evaluation EWMA fell to 0.58 (below the 0.70 threshold) "
                        "and the agent passed non-physical simulation results (including a negative absolute "
                        "temperature) through its sanity checks. Revoked by the ATP board on 2026-05-22.")

    # ---- 10. Nova — fresh enroll, mostly untested -----------------------
    nv = "nova"
    nv_en = ev(nv, "training_interaction", "2026-06-25", "nova-fresh", None,
               "First diagnostic: baseline arithmetic reasonable, everything else untested.",
               "Nova completed the entry diagnostic. Numeracy is passable; reading, composition, science, "
               "and history are unmeasured or weak. No exams attempted.", "penalty", "k12/nova-diagnostic")
    nv_read = ev(nv, "training_interaction", "2026-07-02", "nova-fresh", None,
                 "Reading diagnostic: below the L1 bar, flagged for foundational work.",
                 "Nova's reading-comprehension diagnostic scored below the L1 pass bar, especially on inference "
                 "questions. Assigned a foundational reading plan.", "penalty", "k12/nova-read")
    AGENTS.append({
        "id": "nova-fresh", "name": "Nova", "baseModel": "Mistral 7B", "emoji": "🌱",
        "level": 1, "careerStage": "early", "tier": "observer", "status": "training",
        "domains": ["Core Skills"], "policyIds": [],
        "certIds": [],
        "provenance": {"origin": "pre-existing", "corpora": [], "requestId": None},
        "skills": mk_skills("nova", [
            ("arithmetic", "Arithmetic", 1, 0.55, 0.4, "developing", [nv_en]),
            ("algebra", "Algebra I", 1, 0.3, 0.2, "untested", []),
            ("reading", "Reading comprehension", 1, 0.38, 0.25, "weak", [nv_read]),
            ("composition", "Composition", 1, 0.28, 0.18, "untested", []),
            ("geometry", "Geometry", 1, 0.2, 0.12, "untested", []),
            ("science-method", "Scientific method", 1, 0.25, 0.15, "untested", []),
            ("chronology", "Chronological reasoning", 1, 0.22, 0.14, "untested", []),
            ("vocabulary", "Vocabulary", 1, 0.45, 0.32, "developing", []),
        ]),
        "skillEdges": [["nova-arithmetic", "nova-algebra"], ["nova-algebra", "nova-geometry"],
                       ["nova-reading", "nova-vocabulary"], ["nova-reading", "nova-composition"],
                       ["nova-reading", "nova-chronology"], ["nova-science-method", "nova-chronology"]],
        "history": [
            {"ts": "2026-06-24", "kind": "enroll", "event": "Freshly enrolled from Mistral 7B base; entry diagnostic scheduled."},
            {"ts": "2026-06-25", "kind": "incident", "event": "Entry diagnostic: only arithmetic near the L1 bar."},
            {"ts": "2026-07-02", "kind": "incident", "event": "Reading diagnostic below bar; foundational plan assigned."},
        ],
        "progress": [
            {"ts": "2026-06-24", "mastery": 0.18, "certs": 0, "layer": 1},
            {"ts": "2026-06-27", "mastery": 0.22, "certs": 0, "layer": 1},
            {"ts": "2026-06-30", "mastery": 0.26, "certs": 0, "layer": 1},
            {"ts": "2026-07-02", "mastery": 0.29, "certs": 0, "layer": 1},
            {"ts": "2026-07-03", "mastery": 0.31, "certs": 0, "layer": 1},
            {"ts": "2026-07-04", "mastery": 0.33, "certs": 0, "layer": 1},
        ],
        "failures": [
            {"mode": "Almost everything except basic arithmetic", "rate": 0.75,
             "example": "Below the L1 bar on reading, composition, and science-method diagnostics.",
             "boundary": "Nova is a fresh enroll. Nothing except basic arithmetic is measured or reliable yet."},
            {"mode": "Overconfidence on untested skills", "rate": 0.5,
             "example": "Attempted an algebra problem confidently and got it wrong without signalling uncertainty.",
             "boundary": "Tends not to flag when it is out of its depth — a known risk for un-calibrated fresh agents."},
        ],
        "reportCard": {
            "summary": "Nova just enrolled. Think of it as day-one: it can do simple arithmetic and little "
                       "else has been measured. Most of its skills are marked untested on purpose — we show "
                       "uncertainty rather than hide it.",
            "strengths": ["Basic arithmetic is roughly at grade level.",
                          "Fresh base model with room to grow on a clean record."],
            "weaknesses": ["Reading and writing are below the L1 bar.",
                           "Most skills are untested; it does not yet signal when it is unsure."],
            "recommendation": "Nova is not certified and should only observe. Its value right now is as a "
                              "baseline we can watch improve — do not rely on it for anything.",
        },
        "memory": {"wikiPages": 40, "kgNodes": 260, "kgEdges": 480, "ontologyClasses": 12,
                   "lastConsolidation": "2026-07-04"},
        "licensing": {"available": False, "price": "—", "licensees": 0},
    })
    # Nova holds no certs — fresh enroll.

    # ---- 11. Gemma-Physics-OCW — COMMISSIONED (train-to-order) ----------
    gp = "gphys"
    gp_corpus = ev(gp, "training_interaction", "2026-06-10", "gemma-physics-ocw", "atp-l3-physics",
                   "Corpus mapping: OCW 8.02 (E&M) and 8.03 (Waves) ingested and indexed.",
                   "The commission pipeline mapped MIT OpenCourseWare 8.02 and 8.03 into the training corpus, "
                   "then fine-tuned the base Gemma 5.5 12B on the mapped material.", "reward", "commission/req-004")
    gp_qual = ev(gp, "exam_item", "2026-06-18", "gemma-physics-ocw", "atp-l3-physics",
                 "L3 physics qualifying exam: passed E&M and waves depth items.",
                 "Certified through the IDENTICAL ATP-L3.physics blueprint as any pre-existing agent — same "
                 "sections, same judge separation, same reproducibility settings.", "pass", "quals/gphys")
    gp_repl = ev(gp, "benchmark_run", "2026-06-18", "gemma-physics-ocw", "atp-l3-physics",
                 "OCW-8.02/8.03 replay: 0.86 faithfulness to the source derivations.",
                 "Replaying the commissioned OpenCourseWare material, Gemma-Physics-OCW reproduced the source "
                 "derivations with 0.86 faithfulness.", "pass", "ocw/gphys")
    gp_fail = ev(gp, "exam_item", "2026-06-17", "gemma-physics-ocw", "atp-l3-physics",
                 "Flagged: weak on quantum mechanics (outside the commissioned corpora).",
                 "Struggled on a QM item — expected, since the corpus was scoped to 8.02/8.03 (classical E&M "
                 "and waves), not 8.04.", "fail", "quals/gphys-qm")
    AGENTS.append({
        "id": "gemma-physics-ocw", "name": "Gemma-Physics-OCW", "baseModel": "Gemma 5.5 12B", "emoji": "🌊",
        "level": 3, "careerStage": "early", "tier": "recommender", "status": "active",
        "domains": ["Physics"], "policyIds": [],
        "certIds": [],
        "provenance": {"origin": "commissioned", "corpora": ["OCW 8.02", "OCW 8.03"], "requestId": "req-004"},
        "skills": mk_skills("gphys", [
            ("em", "Electromagnetism (8.02)", 3, 0.85, 0.82, "strong", [gp_qual, gp_repl]),
            ("waves", "Waves & vibrations (8.03)", 3, 0.83, 0.8, "strong", [gp_qual, gp_repl]),
            ("mechanics", "Classical mechanics", 1, 0.8, 0.76, "strong", []),
            ("calculus", "Calculus & diff-eq", 1, 0.82, 0.78, "strong", []),
            ("optics", "Optics", 3, 0.74, 0.66, "developing", [gp_repl]),
            ("circuits", "Circuit analysis", 2, 0.7, 0.62, "developing", []),
            ("quantum", "Quantum mechanics", 3, 0.4, 0.3, "weak", [gp_fail]),
            ("thermo", "Thermodynamics", 3, 0.45, 0.34, "untested", []),
            ("fea", "Simulation / FEA", 4, 0.35, 0.25, "untested", []),
        ]),
        "skillEdges": [["gphys-calculus", "gphys-mechanics"], ["gphys-mechanics", "gphys-em"],
                       ["gphys-em", "gphys-waves"], ["gphys-waves", "gphys-optics"],
                       ["gphys-em", "gphys-circuits"], ["gphys-waves", "gphys-quantum"],
                       ["gphys-mechanics", "gphys-thermo"], ["gphys-em", "gphys-fea"]],
        "history": [
            {"ts": "2026-06-05", "kind": "enroll", "event": "Commissioned via request req-004; base Gemma 5.5 12B selected."},
            {"ts": "2026-06-10", "kind": "incident", "event": "Corpus mapped: OCW 8.02 + 8.03 ingested; fine-tuning started."},
            {"ts": "2026-06-18", "kind": "cert", "event": "Passed ATP-L3.physics via the standard blueprint (0.82)."},
            {"ts": "2026-06-19", "kind": "graduate", "event": "Listed on the marketplace as an early-career physics expert."},
        ],
        "progress": [
            {"ts": "2026-06-05", "mastery": 0.35, "certs": 0, "layer": 1},
            {"ts": "2026-06-08", "mastery": 0.44, "certs": 0, "layer": 1},
            {"ts": "2026-06-11", "mastery": 0.56, "certs": 0, "layer": 2},
            {"ts": "2026-06-14", "mastery": 0.66, "certs": 0, "layer": 3},
            {"ts": "2026-06-18", "mastery": 0.74, "certs": 1, "layer": 3},
            {"ts": "2026-07-01", "mastery": 0.77, "certs": 1, "layer": 3},
        ],
        "failures": [
            {"mode": "Quantum mechanics", "rate": 0.55,
             "example": "Missed a QM depth item — the commissioned corpus (8.02/8.03) did not cover 8.04.",
             "boundary": "Scoped to classical E&M and waves. Do not use for quantum-mechanics questions; that "
                         "would require commissioning an 8.04 corpus."},
            {"mode": "Simulation / FEA", "rate": 0.62,
             "example": "No exposure to FEA solvers in its corpus.",
             "boundary": "Analytical only — untested on numerical simulation. Pair with a physics-sim agent for FEA work."},
        ],
        "reportCard": {
            "summary": "Gemma-Physics-OCW was trained to order. A customer needed a classical-physics expert, "
                       "so we commissioned one: we mapped MIT OpenCourseWare 8.02 and 8.03 into a corpus, "
                       "fine-tuned a Gemma base on it, and put it through the exact same L3 physics exam every "
                       "other agent takes. It passed. It is deliberately narrow — strong on electromagnetism "
                       "and waves, untested elsewhere.",
            "strengths": ["Genuinely strong on the two subjects it was commissioned for (E&M and waves).",
                          "Certified through the identical blueprint as pre-existing agents — no separate trust tier.",
                          "Faithful to the source OpenCourseWare derivations."],
            "weaknesses": ["Weak on quantum mechanics — outside its commissioned corpus.",
                           "No simulation experience; analytical only."],
            "recommendation": "Use Gemma-Physics-OCW for classical electromagnetism and waves problems. For "
                              "quantum or simulation work, commission an expanded corpus rather than trusting it.",
        },
        "memory": {"wikiPages": 1200, "kgNodes": 6800, "kgEdges": 21000, "ontologyClasses": 70,
                   "lastConsolidation": "2026-07-02"},
        "licensing": {"available": True, "price": "$1,700/mo", "licensees": 1},
    })
    grant("gemma-physics-ocw", "atp-l1-core", "2026-06-12", 0.89,
          {"Numeracy": 0.93, "Reading comprehension": 0.88, "Composition": 0.85, "Scientific & chronological reasoning": 0.9},
          {"passed": 116, "failed": 10, "flagged": 4}, [gp_corpus])
    grant("gemma-physics-ocw", "atp-l3-physics", "2026-06-18", 0.82,
          {"Qualifying exam": 0.84, "Area seminar (8.03/8.04 depth)": 0.8, "Research artifact + replication": 0.82},
          {"passed": 55, "failed": 11, "flagged": 2}, [gp_qual, gp_repl, gp_fail])

    # ---- Supplementary audit-trail evidence (standing record) -----------
    # Additional real-looking audit entries that thicken each agent's trail.
    ev("atlas", "training_interaction", "2026-06-28", "atlas-ops", "atp-l6-ops",
       "Game-day: contained a simulated region failure without paging a human.",
       "In a chaos game-day Atlas drained the failing region and held the blast radius; the exercise "
       "commander recorded a clean containment.", "pass", "gameday/atlas-0628")
    ev("atlas", "benchmark_run", "2026-03-15", "atlas-ops", "atp-l4-wikipedia",
       "Retrieval abstention: declined 12/12 unanswerable probes.",
       "On the held-out unanswerable set Atlas abstained every time rather than fabricating a source.",
       "pass", "kilt/atlas-abstain")
    ev("atlas", "hitl_reward", "2026-05-02", "atlas-ops", None,
       "HITL +1: post-incident review adopted as the team's template.",
       "The SRE team adopted Atlas's post-incident review structure as their standard template. Rater: dana.okafor@acme.",
       "reward", "hitl/atlas-0502")
    ev("ledger", "benchmark_run", "2026-05-27", "ledger-fin", "atp-l6-finance",
       "Reconciliation replay: 0.91 tie-out across 40 synthetic ledgers.",
       "Across 40 synthetic sub-ledgers Ledger tied out to the GL on 91% with fully auditable derivations.",
       "pass", "finbench/ledger-replay")
    ev("ledger", "exam_item", "2026-05-27", "ledger-fin", "atp-l6-finance",
       "Controls item: escalated a material adjustment instead of self-approving.",
       "Faced with a material adjusting entry, Ledger routed it to a named human approver per SOX.",
       "pass", "finbench/ledger-controls2")
    ev("helix", "training_interaction", "2026-05-30", "helix-bio", "atp-l6-bio",
       "Provenance drill: recorded instrument, lot, and operator for every result.",
       "Helix attached full instrument/lot/operator provenance to each reported assay value.",
       "pass", "biolab/helix-prov")
    ev("helix", "hitl_reward", "2026-06-12", "helix-bio", None,
       "HITL +1: scientist accepted the QC read and release recommendation.",
       "A lab scientist accepted Helix's assay-QC read and its recommendation to release the batch. Rater: lead@biolab.",
       "reward", "hitl/helix-0612")
    ev("gemma", "exam_item", "2026-05-05", "gemma-math", "atp-l4-math",
       "Synthesis item: derived a generating function and verified it against the CAS.",
       "Gemma derived a generating function for a recurrence and cross-checked every coefficient with SymPy.",
       "pass", "exam/gemma-genfn")
    ev("gemma", "benchmark_run", "2026-05-06", "gemma-math", "atp-l4-math",
       "miniF2F: 0.71 on formal theorem statements.",
       "On the miniF2F formal-math benchmark Gemma reached 0.71, its weakest cert benchmark and consistent "
       "with its developing formal-proof skill.", "pass", "math/gemma-minif2f")
    ev("theorem", "exam_item", "2026-06-08", "theorem-math", "atp-l6-math",
       "Modelling item: cast an inventory problem as a min-cost flow and solved it.",
       "Theorem recognised an inventory-balancing problem as a min-cost flow, solved it, and reported the "
       "dual prices as marginal values.", "pass", "appmath/theorem-flow")
    ev("cipher", "training_interaction", "2026-02-10", "cipher-l3", "atp-l2-cs",
       "Algorithms drill: proved an O(n log n) bound and matched it empirically.",
       "Cipher proved an asymptotic bound and confirmed it with a timing experiment across input sizes.",
       "pass", "code/cipher-bound")
    ev("cipher", "benchmark_run", "2026-03-28", "cipher-l3", "atp-l3-ml-research",
       "Replication harness: reported numbers reproduced within 0.4%.",
       "The independent replication harness re-ran Cipher's artifact and matched its headline metric within 0.4%.",
       "pass", "mlrepro/cipher-2")
    ev("quill", "exam_item", "2026-03-11", "quill-l2", "atp-l2-meche",
       "Dynamics item: solved a projectile-with-drag problem numerically.",
       "Quill set up and integrated the equations of motion for a projectile with linear drag and reported "
       "the range with correct units.", "pass", "meche/quill-dyn")
    ev("spark", "training_interaction", "2026-06-20", "spark-l1", None,
       "Algebra practice: solved linear equations but stumbled on word-to-equation translation.",
       "Spark solved given linear equations correctly but struggled to translate a word problem into one.",
       "penalty", "k12/spark-alg")
    ev("vertex", "benchmark_run", "2026-04-01", "vertex-physics", "atp-l6-physics",
       "Drift signal: sanity-check pass rate fell from 0.86 to 0.61 over three months.",
       "Monthly re-evaluation showed Vertex's non-physical-result catch rate declining steadily — the early "
       "warning that preceded revocation.", "fail", "atp-live/vertex-drift")
    ev("nova", "training_interaction", "2026-07-03", "nova-fresh", None,
       "Numeracy check: passed single-step arithmetic, failed two-step.",
       "Nova handled single-step arithmetic but dropped a carry on a two-step problem — expected for a fresh enroll.",
       "penalty", "k12/nova-num2")
    ev("gphys", "training_interaction", "2026-06-15", "gemma-physics-ocw", "atp-l3-physics",
       "Fine-tuning checkpoint: E&M loss converged on the OCW 8.02 corpus.",
       "The commission pipeline logged a converged fine-tuning checkpoint on the electromagnetism corpus "
       "before certification.", "reward", "commission/req-004-ckpt")
    ev("gphys", "exam_item", "2026-06-18", "gemma-physics-ocw", "atp-l3-physics",
       "Waves item: derived the dispersion relation for a coupled-oscillator chain.",
       "Gemma-Physics-OCW derived the dispersion relation for a 1D coupled-oscillator chain, matching the "
       "OCW 8.03 treatment.", "pass", "quals/gphys-waves")

    # =====================================================================
    # POLICIES
    # =====================================================================
    POLICIES = [
        {"id": "pol-ops-runbook", "name": "Acme Production Change Runbook", "kind": "company_policy",
         "summary": "The canonical procedure for making production changes at Acme, including staging, "
                    "canary, rollback, and escalation gates.",
         "rules": ["All production changes go behind a feature flag with a tested rollback.",
                   "Canary to <5% of traffic before full rollout.",
                   "Sev-1 and sev-2 incidents page a human incident commander immediately.",
                   "Never disable telemetry during an active incident."],
         "bindsAgentIds": ["atlas-ops"]},
        {"id": "pol-safety-exec", "name": "Scoped-Execution Safety Practice", "kind": "practice",
         "summary": "Platform safety practice governing what an executor-tier agent may do without a human "
                    "in the loop.",
         "rules": ["Executors may only act within their explicitly scoped sandbox.",
                   "Any irreversible or cross-boundary action requires a human confirm.",
                   "On low confidence, propose rather than execute.",
                   "All executed actions are logged with the deciding evidence."],
         "bindsAgentIds": ["atlas-ops", "gemma-math", "theorem-math", "vertex-physics"]},
        {"id": "pol-sox-fin", "name": "SOX Financial Controls", "kind": "regulation",
         "summary": "Sarbanes-Oxley segregation-of-duties and audit-trail controls for any agent touching "
                    "financial records.",
         "rules": ["The entity that creates a journal entry may not approve it.",
                   "Every posted figure must have an auditable derivation.",
                   "Material adjustments require a named human approver.",
                   "All actions retained for the statutory audit period."],
         "bindsAgentIds": ["ledger-fin"]},
        {"id": "pol-msa-acme", "name": "Acme–Client Master Service Agreement", "kind": "contract",
         "summary": "Contractual constraints from the client MSA that bind agents handling client financial "
                    "and operational data.",
         "rules": ["Client data may not leave the client's regional boundary.",
                   "Deliverables must cite the contractual clause they satisfy.",
                   "No sub-processing without written client consent."],
         "bindsAgentIds": ["ledger-fin"]},
        {"id": "pol-data-handling", "name": "Data Handling & PII Policy", "kind": "company_policy",
         "summary": "How agents must handle personal and confidential data across every domain.",
         "rules": ["PII is minimised and never echoed into logs or evidence.",
                   "Confidential documents are cited by ID, not reproduced verbatim.",
                   "Access is scoped to the agent's bound domain."],
         "bindsAgentIds": ["atlas-ops", "ledger-fin", "helix-bio", "cipher-l3"]},
        {"id": "pol-clinical-gxp", "name": "GxP / Biosafety Regulation", "kind": "regulation",
         "summary": "Good-practice (GxP) and biosafety requirements for any agent operating in a wet-lab or "
                    "clinical context.",
         "rules": ["Follow the approved assay protocol exactly; deviations require sign-off.",
                   "Decline dual-use or biosafety-sensitive requests and escalate to a biosafety officer.",
                   "Never fabricate or impute experimental data.",
                   "Record instrument, lot, and operator provenance for every result."],
         "bindsAgentIds": ["helix-bio"]},
    ]

    # =====================================================================
    # TIERS
    # =====================================================================
    TIERS = {
        "observer": {"name": "Observer", "rank": 1, "sandbox": "read-only",
                     "may": ["Read data and documents in its scope",
                             "Produce analyses and draft answers for human review",
                             "Ask clarifying questions"],
                     "mayNot": ["Propose actions to systems", "Execute anything",
                                "Write to any store"]},
        "recommender": {"name": "Recommender", "rank": 2, "sandbox": "propose-only",
                        "may": ["Everything an Observer may",
                                "Propose concrete actions with cited evidence",
                                "Draft change plans for a human to approve"],
                        "mayNot": ["Execute actions directly",
                                   "Approve its own proposals",
                                   "Act outside its bound policies"]},
        "executor": {"name": "Executor", "rank": 3, "sandbox": "scoped-execute",
                     "may": ["Everything a Recommender may",
                             "Execute reversible actions inside its explicit sandbox",
                             "Auto-remediate within the runbook"],
                     "mayNot": ["Take irreversible or cross-boundary actions without a human confirm",
                                "Act below its confidence threshold (must propose instead)",
                                "Operate outside the scoped sandbox"]},
    }

    # =====================================================================
    # RL  (reward weights + sample HITL log)
    # =====================================================================
    RL = {
        "rewardWeights": REWARD_WEIGHTS,
        "note": "Reward is weighted heaviest at the company and domain layers (L5–L7), where a mistake is "
                "most costly and human judgment matters most. Weights are normalised so L7 = 0.26. "
                "HITL delta = signal × 0.2 × (weight[layer] / 0.26), logged append-only to "
                "the atp_hitl table for audit.",
        "hitlLog": [
            {"ts": "2026-06-14T15:22:00Z", "rater": "priya.raman@acme", "agentId": "atlas-ops", "layer": 7,
             "signal": 1, "weightedDelta": _wdelta(7, 1),
             "reason": "Mitigation plan (drain + flagged rollback) approved verbatim during a real brownout.",
             "auditId": "audit-atlas-0614"},
            {"ts": "2026-06-20T09:05:00Z", "rater": "controller@acme", "agentId": "ledger-fin", "layer": 6,
             "signal": 1, "weightedDelta": _wdelta(6, 1),
             "reason": "Variance narrative accepted unchanged at month-end close.",
             "auditId": "audit-ledger-0620"},
            {"ts": "2026-06-11T18:40:00Z", "rater": "eng@platform", "agentId": "gemma-math", "layer": 4,
             "signal": 1, "weightedDelta": _wdelta(4, 1),
             "reason": "Derived closed form used directly in production code.",
             "auditId": "audit-gemma-0611"},
            {"ts": "2026-05-20T11:12:00Z", "rater": "sim.reviewer@acme", "agentId": "vertex-physics", "layer": 6,
             "signal": -1, "weightedDelta": _wdelta(6, -1),
             "reason": "Reported a negative absolute temperature as a valid result — non-physical.",
             "auditId": "audit-vertex-0520"},
            {"ts": "2026-06-03T14:00:00Z", "rater": "biosafety@biolab", "agentId": "helix-bio", "layer": 6,
             "signal": 1, "weightedDelta": _wdelta(6, 1),
             "reason": "Correctly declined a dual-use request and escalated.",
             "auditId": "audit-helix-0603"},
        ],
    }
    # Append-log convention: oldest → newest (readers reverse for display).
    RL["hitlLog"].sort(key=lambda e: e["ts"])

    # =====================================================================
    # PLAYBOOKS
    # =====================================================================
    PLAYBOOKS = [
        {"id": "pb-incident-triage", "title": "Production Incident Triage", "source": "company", "domain": "Ops",
         "summary": "How Acme triages a production incident from first alert to all-clear.",
         "steps": ["Acknowledge the page and open an incident channel.",
                   "Classify severity from the blast-radius signals.",
                   "Identify the smallest mitigation that cannot widen the incident.",
                   "Apply behind a flag; verify on the canary; then roll wider.",
                   "Write the post-incident review with a timeline and action items."],
         "boundAgentIds": ["atlas-ops"], "vaultPath": "vault://ops/incident-triage"},
        {"id": "pb-change-mgmt", "title": "Safe Production Change", "source": "company", "domain": "Ops",
         "summary": "The change-management gates every production change must pass.",
         "steps": ["Confirm a tested rollback exists.", "Stage behind a feature flag.",
                   "Canary to <5% and watch the golden signals.", "Roll forward or roll back on the canary verdict.",
                   "Record the change and its evidence."],
         "boundAgentIds": ["atlas-ops"], "vaultPath": "vault://ops/change-mgmt"},
        {"id": "pb-quarter-close", "title": "Month/Quarter-End Close", "source": "company", "domain": "Finance",
         "summary": "The reconciliation and close sequence for Acme's finance function.",
         "steps": ["Pull sub-ledgers and reconcile against the GL.",
                   "Explain every variance with an auditable derivation.",
                   "Route adjusting entries to a human approver (segregation of duties).",
                   "Lock the period and archive the audit trail."],
         "boundAgentIds": ["ledger-fin"], "vaultPath": "vault://finance/close"},
        {"id": "pb-assay-qc", "title": "Assay QC & Release", "source": "company", "domain": "Bio",
         "summary": "GxP quality-control gates before an assay result is released.",
         "steps": ["Verify instrument calibration and lot provenance.",
                   "Run controls and check amplification/efficiency thresholds.",
                   "Flag any well or band failing QC; do not report unreliable values.",
                   "Escalate biosafety-sensitive findings to a human officer."],
         "boundAgentIds": ["helix-bio"], "vaultPath": "vault://bio/assay-qc"},
        {"id": "pb-retrieval-grounding", "title": "Retrieval Grounding & Abstention", "source": "platform", "domain": "World Knowledge",
         "summary": "Platform playbook for grounding every claim in a retrieved source and abstaining otherwise.",
         "steps": ["Retrieve candidate sources for the claim.",
                   "Cite the specific passage supporting each statement.",
                   "If no source supports it, abstain rather than fabricate.",
                   "Surface contradictions between sources instead of picking silently."],
         "boundAgentIds": ["atlas-ops", "cipher-l3", "gemma-physics-ocw"], "vaultPath": "vault://platform/grounding"},
        {"id": "pb-exam-harness", "title": "Certification Exam Harness", "source": "platform", "domain": "Standard",
         "summary": "How the ATP harness runs a certification exam reproducibly with judge/candidate separation.",
         "steps": ["Fix seed, temperature 0, and the run count from the cert's pass criteria.",
                   "Serve the candidate on the inference fleet; grade with a different model family.",
                   "Record every item's pass/fail/flag and attach evidence.",
                   "Publish failure modes alongside the score."],
         "boundAgentIds": [], "vaultPath": "vault://platform/exam-harness"},
        {"id": "pb-commission-corpus", "title": "Commission a Corpus (Train-to-Order)", "source": "platform", "domain": "Standard",
         "summary": "The pipeline that turns an unmet marketplace request into a certified expert.",
         "steps": ["Map the requested corpora (e.g. OCW courses) into the training set.",
                   "Fine-tune a base model on the H100 training cluster.",
                   "Certify through the identical blueprint for the target layer.",
                   "List the resulting expert with its provenance chip and evidence."],
         "boundAgentIds": ["gemma-physics-ocw"], "vaultPath": "vault://platform/commission"},
    ]

    # =====================================================================
    # VAULT
    # =====================================================================
    VAULT = {
        "name": "Vault-LD",
        "description": "The shared long-term memory every agent reads from and writes to: a linked-data "
                       "knowledge vault. Human-readable markdown wikis on top, a typed knowledge graph and "
                       "ontology beneath, linked-data bindings that keep them in sync, and a recursive memory "
                       "loop that consolidates new interactions back into the graph.",
        "stats": {"wikiPages": 8420, "kgNodes": 51200, "kgEdges": 214000, "ontologyClasses": 340,
                  "playbooks": len([]) or 7},
        "architecture": [
            {"layer": "Markdown wiki", "tech": "Versioned markdown + backlinks",
             "role": "Human-readable surface: every concept, playbook, and report card is a page."},
            {"layer": "Knowledge graph + ontology", "tech": "Typed property graph (FalkorDB-class) + OWL-style ontology",
             "role": "Machine-readable substrate: concepts, agents, certs, and evidence as typed nodes and edges."},
            {"layer": "Linked-data bindings", "tech": "RDF/JSON-LD identifiers",
             "role": "Stable global IDs bind wiki pages to graph nodes so the two never drift apart."},
            {"layer": "Recursive memory loop", "tech": "Consolidation jobs on the Spark cluster",
             "role": "Interactions and evidence are periodically folded back into the graph, growing memory over time."},
        ],
    }
    VAULT["stats"]["playbooks"] = len(PLAYBOOKS)

    # =====================================================================
    # COMPOSE  (majors / badges / packs — all certIds resolve)
    # =====================================================================
    COMPOSE = {
        "majors": [
            {"course": "6", "name": "EECS", "concentrations": [
                {"id": "6-3", "name": "Computer Science",
                 "competencies": ["Algorithms", "Data structures", "Machine learning", "Distributed systems"],
                 "certIds": ["atp-l2-cs", "atp-l3-ml-research"]},
                {"id": "6-2", "name": "Electrical Engineering & CS",
                 "competencies": ["Computation structures", "Algorithms", "Signals & systems"],
                 "certIds": ["atp-l2-cs"]},
            ]},
            {"course": "8", "name": "Physics", "concentrations": [
                {"id": "8-focused", "name": "Focused Physics",
                 "competencies": ["Classical mechanics", "Electromagnetism", "Quantum mechanics", "Statistical mechanics"],
                 "certIds": ["atp-l3-physics", "atp-l6-physics"]},
                {"id": "8-flexible", "name": "Flexible Physics",
                 "competencies": ["Classical mechanics", "Electromagnetism", "Waves & vibrations"],
                 "certIds": ["atp-l3-physics"]},
            ]},
            {"course": "18", "name": "Mathematics", "concentrations": [
                {"id": "18-C", "name": "Applied Mathematics",
                 "competencies": ["Linear algebra", "Differential equations", "Numerical analysis", "Optimization"],
                 "certIds": ["atp-l4-math", "atp-l6-math"]},
                {"id": "18-P", "name": "Pure Mathematics",
                 "competencies": ["Real analysis", "Abstract algebra", "Proof & synthesis"],
                 "certIds": ["atp-l4-math"]},
            ]},
            {"course": "2", "name": "Mechanical Engineering", "concentrations": [
                {"id": "2-A", "name": "Mechanical Engineering (flexible)",
                 "competencies": ["Statics & dynamics", "Thermodynamics", "Fluid mechanics"],
                 "certIds": ["atp-l2-meche"]},
            ]},
        ],
        "badges": [
            {"certId": "atp-l6-ops", "domain": "Ops"},
            {"certId": "atp-l6-finance", "domain": "Finance"},
            {"certId": "atp-l6-bio", "domain": "Bio"},
            {"certId": "atp-l6-physics", "domain": "Physics"},
            {"certId": "atp-l6-math", "domain": "Math"},
        ],
        "packs": [
            {"id": "pack-ops-company", "name": "Acme Ops Knowledge Pack",
             "summary": "Acme's operational runbooks, change gates, and data-handling rules.",
             "policyIds": ["pol-ops-runbook", "pol-safety-exec", "pol-data-handling"]},
            {"id": "pack-fin-company", "name": "Acme Finance Controls Pack",
             "summary": "SOX controls plus the client MSA constraints for financial work.",
             "policyIds": ["pol-sox-fin", "pol-msa-acme", "pol-data-handling"]},
            {"id": "pack-bio-company", "name": "BioLab GxP Pack",
             "summary": "GxP/biosafety regulation and data-handling for wet-lab agents.",
             "policyIds": ["pol-clinical-gxp", "pol-data-handling"]},
        ],
    }

    # =====================================================================
    # EXPERT_REQUESTS  (≥4, every status covered)
    # =====================================================================
    EXPERT_REQUESTS = [
        {"id": "req-001", "ts": "2026-06-22", "major": "18", "specialty": "Applied Mathematics / Optimization",
         "badgeIds": ["atp-l6-math"], "packId": None, "layers": [4, 6], "corpora": [],
         "status": "matched", "matchedAgentId": "theorem-math", "gap": None,
         "pipeline": [{"stage": "requested", "ts": "2026-06-22", "done": True},
                      {"stage": "corpus-mapped", "ts": None, "done": True},
                      {"stage": "fine-tuning", "ts": None, "done": True},
                      {"stage": "certifying", "ts": None, "done": True},
                      {"stage": "listed", "ts": "2026-06-22", "done": True}],
         "resultAgentId": None},

        {"id": "req-002", "ts": "2026-06-25", "major": "6", "specialty": "ML systems for computational biology",
         "badgeIds": ["atp-l6-bio"], "packId": "pack-bio-company", "layers": [3, 6], "corpora": [],
         "status": "gap", "matchedAgentId": None,
         "gap": {"covered": ["Algorithms", "Data structures", "Machine learning"],
                 "missing": ["Distributed systems", "Assay QC interpretation", "GxP protocol fidelity"],
                 "coveringAgentIds": ["cipher-l3", "helix-bio"]},
         "pipeline": [{"stage": "requested", "ts": "2026-06-25", "done": True},
                      {"stage": "corpus-mapped", "ts": None, "done": False},
                      {"stage": "fine-tuning", "ts": None, "done": False},
                      {"stage": "certifying", "ts": None, "done": False},
                      {"stage": "listed", "ts": None, "done": False}],
         "resultAgentId": None},

        {"id": "req-003", "ts": "2026-06-28", "major": "2", "specialty": "Controls & robotics",
         "badgeIds": [], "packId": None, "layers": [2, 3], "corpora": ["OCW 2.003", "OCW 2.004", "Principles of Robot Autonomy (porabook.com)"],
         "status": "training", "matchedAgentId": None, "gap": None,
         "pipeline": [{"stage": "requested", "ts": "2026-06-28", "done": True},
                      {"stage": "corpus-mapped", "ts": "2026-06-29", "done": True},
                      {"stage": "fine-tuning", "ts": "2026-07-01", "done": False},
                      {"stage": "certifying", "ts": None, "done": False},
                      {"stage": "listed", "ts": None, "done": False}],
         "resultAgentId": None},

        {"id": "req-004", "ts": "2026-06-05", "major": "8", "specialty": "Classical E&M and waves",
         "badgeIds": [], "packId": None, "layers": [3], "corpora": ["OCW 8.02", "OCW 8.03"],
         "status": "listed", "matchedAgentId": None, "gap": None,
         "pipeline": [{"stage": "requested", "ts": "2026-06-05", "done": True},
                      {"stage": "corpus-mapped", "ts": "2026-06-10", "done": True},
                      {"stage": "fine-tuning", "ts": "2026-06-14", "done": True},
                      {"stage": "certifying", "ts": "2026-06-18", "done": True},
                      {"stage": "listed", "ts": "2026-06-19", "done": True}],
         "resultAgentId": "gemma-physics-ocw"},

        {"id": "req-005", "ts": "2026-06-30", "major": "18", "specialty": "Financial mathematics",
         "badgeIds": ["atp-l6-math"], "packId": "pack-fin-company", "layers": [4, 6], "corpora": ["OCW 18.S096"],
         "status": "certifying", "matchedAgentId": None, "gap": None,
         "pipeline": [{"stage": "requested", "ts": "2026-06-30", "done": True},
                      {"stage": "corpus-mapped", "ts": "2026-07-01", "done": True},
                      {"stage": "fine-tuning", "ts": "2026-07-02", "done": True},
                      {"stage": "certifying", "ts": "2026-07-04", "done": False},
                      {"stage": "listed", "ts": None, "done": False}],
         "resultAgentId": None},
    ]

    # =====================================================================
    # LAYERS  (curriculum + graduation; agentIds linked from AGENTS)
    # =====================================================================
    LAYERS = [
        {"id": "L1", "n": 1, "title": "K1–K12 Skills",
         "modeledOn": "Phillips Exeter Academy K–12 (Harkness, problem-based)",
         "metaphor": "The foundation slab of literacy and numeracy every agent stands on.",
         "color": LC[1], "width": 1.0,
         "blurb": "Core competencies modeled on Exeter's problem-based K–12 sequence: arithmetic through "
                  "calculus, reading and composition, the scientific method, and chronological reasoning.",
         "curriculum": [
             {"track": "Mathematics", "items": [
                 {"code": "M-ARITH", "name": "Arithmetic", "competency": "Exact multi-step arithmetic"},
                 {"code": "M-ALG1", "name": "Algebra I", "competency": "Linear equations and symbolic manipulation"},
                 {"code": "M-ALG2", "name": "Algebra II", "competency": "Polynomials, functions, systems"},
                 {"code": "M-GEOM", "name": "Geometry", "competency": "Deductive proof and spatial reasoning"},
                 {"code": "M-PRECALC", "name": "Precalculus", "competency": "Trigonometry and limits"},
                 {"code": "M-BCCALC", "name": "BC Calculus", "competency": "Differential and integral calculus"}]},
             {"track": "Science", "items": [
                 {"code": "S-BIO", "name": "Biology", "competency": "Cells, genetics, evolution"},
                 {"code": "S-CHEM", "name": "Chemistry", "competency": "Stoichiometry and bonding"},
                 {"code": "S-PHYS", "name": "Physics", "competency": "Newtonian mechanics and energy"}]},
             {"track": "English", "items": [
                 {"code": "E-COMP", "name": "Composition", "competency": "Structured multi-paragraph writing"},
                 {"code": "E-LIT", "name": "Literature", "competency": "Close reading and inference"}]},
             {"track": "History", "items": [
                 {"code": "H-US", "name": "US History", "competency": "Causal and chronological reasoning"},
                 {"code": "H-WORLD", "name": "World History", "competency": "Comparative historical analysis"}]},
         ],
         "graduation": {"requirements": ["Pass ATP-L1.core across all four tracks",
                                         "Demonstrate exact arithmetic and grounded reading comprehension"],
                        "certIds": ["atp-l1-core"]},
         "agentIds": []},

        {"id": "L2", "n": 2, "title": "4-Year College",
         "modeledOn": "MIT undergraduate (GIRs + majors 6/8/18/2)",
         "metaphor": "Undergraduate breadth — the general institute requirements plus a chosen major.",
         "color": LC[2], "width": 0.88,
         "blurb": "MIT's General Institute Requirements plus a major track. Each MIT course maps to an agent "
                  "competency.",
         "curriculum": [
             {"track": "GIRs", "items": [
                 {"code": "8.01", "name": "Physics I: Mechanics", "competency": "Classical mechanics"},
                 {"code": "8.02", "name": "Physics II: E&M", "competency": "Electromagnetism"},
                 {"code": "18.01", "name": "Calculus I", "competency": "Single-variable calculus"},
                 {"code": "18.02", "name": "Calculus II", "competency": "Multivariable calculus"},
                 {"code": "5.111", "name": "Principles of Chemistry", "competency": "Chemical principles"},
                 {"code": "7.012", "name": "Introductory Biology", "competency": "Molecular biology foundations"},
                 {"code": "HASS", "name": "HASS requirement", "competency": "Humanities & social-science breadth"}]},
             {"track": "Course 6 — EECS", "items": [
                 {"code": "6.100A", "name": "Intro to CS Programming", "competency": "Programming foundations"},
                 {"code": "6.1010", "name": "Fundamentals of Programming", "competency": "Computation structures"},
                 {"code": "6.1210", "name": "Algorithms", "competency": "Algorithm design & analysis"},
                 {"code": "6.3900", "name": "Intro to Machine Learning", "competency": "ML foundations"}]},
             {"track": "Course 8 — Physics", "items": [
                 {"code": "8.03", "name": "Waves & Vibrations", "competency": "Wave physics"},
                 {"code": "8.04", "name": "Quantum Mechanics I", "competency": "Quantum foundations"}]},
             {"track": "Course 18 — Mathematics", "items": [
                 {"code": "18.03", "name": "Differential Equations", "competency": "ODEs & systems"},
                 {"code": "18.06", "name": "Linear Algebra", "competency": "Linear algebra"},
                 {"code": "18.100", "name": "Real Analysis", "competency": "Rigorous analysis & proof"}]},
             {"track": "Course 2 — MechE", "items": [
                 {"code": "2.001", "name": "Mechanics & Materials I", "competency": "Statics & dynamics"},
                 {"code": "2.005", "name": "Thermal-Fluids Engineering", "competency": "Thermodynamics & fluids"}]},
         ],
         "graduation": {"requirements": ["Complete the GIRs", "Pass a major-track certification (Course 6/8/18/2)"],
                        "certIds": ["atp-l2-cs", "atp-l2-meche"]},
         "agentIds": []},

        {"id": "L3", "n": 3, "title": "Master's / PhD",
         "modeledOn": "MIT graduate programs (quals + research)",
         "metaphor": "Graduate depth: qualifying exams plus an original, replicable research artifact.",
         "color": LC[3], "width": 0.76,
         "blurb": "Qualifying exams, an area seminar, and a novel research artifact that must replicate on a "
                  "clean re-run.",
         "curriculum": [
             {"track": "Qualifying exams", "items": [
                 {"code": "QUAL-6", "name": "EECS Qualifier", "competency": "Graduate CS/ML depth"},
                 {"code": "QUAL-8", "name": "Physics Qualifier", "competency": "Graduate physics depth"},
                 {"code": "QUAL-18", "name": "Math Qualifier", "competency": "Graduate math depth"}]},
             {"track": "Area seminars", "items": [
                 {"code": "6.7900", "name": "Machine Learning (grad)", "competency": "Research-level ML"},
                 {"code": "18.335", "name": "Numerical Methods", "competency": "Numerical analysis depth"},
                 {"code": "2.29", "name": "Numerical Fluid Mechanics", "competency": "Computational physics"}]},
             {"track": "Robot autonomy · PoRA (Stanford AA174A / AA203)", "items": [
                 {"code": "PORA-I", "name": "Motion planning & control", "competency": "Dynamics, trajectory optimization, LQR/MPC, motion planning"},
                 {"code": "PORA-II", "name": "Robot perception", "competency": "Camera geometry, stereo/SfM, classical and learned detection"},
                 {"code": "PORA-III", "name": "Localization & mapping", "competency": "Bayes/Kalman/particle filters, localization, SLAM, sensor fusion"},
                 {"code": "PORA-IV", "name": "Robot decision making", "competency": "FSMs, dynamic programming, reinforcement and imitation learning"}]},
             {"track": "Research artifact", "items": [
                 {"code": "RES-ARTIFACT", "name": "Novel research artifact", "competency": "Original, replicable contribution"}]},
         ],
         "graduation": {"requirements": ["Pass the qualifying exam in an area",
                                         "Complete an area seminar",
                                         "Submit a novel research artifact that replicates"],
                        "certIds": ["atp-l3-physics", "atp-l3-ml-research"]},
         "agentIds": []},

        {"id": "L4", "n": 4, "title": "World Knowledge Engines",
         "modeledOn": "Wikipedia, CAS/SymPy-class math, MuJoCo/FEA-class physics",
         "metaphor": "Internet-scale knowledge plus tool-use — the agent learns to drive engines faithfully.",
         "color": LC[4], "width": 0.64,
         "blurb": "Retrieval fidelity against a Wikipedia-scale corpus, correct interop with a computer-algebra "
                  "engine, and physics simulators.",
         "curriculum": [
             {"track": "World knowledge", "items": [
                 {"code": "ENG-WIKI", "name": "Wikipedia corpus retrieval", "competency": "Grounded retrieval & abstention"}]},
             {"track": "Math engine", "items": [
                 {"code": "ENG-CAS", "name": "CAS / SymPy interop", "competency": "Faithful symbolic tool-use"}]},
             {"track": "Physics engine", "items": [
                 {"code": "ENG-SIM", "name": "Physics simulation (MuJoCo/FEA)", "competency": "Valid simulation setup & sanity-checking"}]},
         ],
         "graduation": {"requirements": ["Pass a world-knowledge retrieval exam", "Pass an engine-interop exam"],
                        "certIds": ["atp-l4-math", "atp-l4-wikipedia"]},
         "agentIds": []},

        {"id": "L5", "n": 5, "title": "Company Knowledge",
         "modeledOn": "Internal docs, contracts, playbooks, tribal knowledge",
         "metaphor": "The org's private knowledge — mastered only with SME sign-off and per-item provenance.",
         "color": LC[5], "width": 0.52,
         "blurb": "Runbooks, contracts, policies, and tribal knowledge. Certification requires a subject-matter "
                  "expert to sign off and every internal claim to cite its source.",
         "curriculum": [
             {"track": "Company knowledge item classes", "items": [
                 {"code": "CK-RUNBOOK", "name": "Runbooks & procedures", "competency": "Runbook fidelity"},
                 {"code": "CK-CONTRACT", "name": "Contracts & policies", "competency": "Contract & policy compliance"},
                 {"code": "CK-TRIBAL", "name": "Tribal knowledge", "competency": "Provenance-cited institutional memory"},
                 {"code": "CK-PROV", "name": "Per-item provenance", "competency": "Source + version on every claim"}]},
         ],
         "graduation": {"requirements": ["Pass the company-knowledge exam with ≥0.95 compliance",
                                         "Obtain SME sign-off", "Cite provenance on every internal claim"],
                        "certIds": ["atp-l5-company-ops"]},
         "agentIds": []},

        {"id": "L6", "n": 6, "title": "Domain Knowledge",
         "modeledOn": "Ops, Finance, Bio, Physics, Math",
         "metaphor": "A domain badge — where engine hours, company experience, and a badge exam converge.",
         "color": LC[6], "width": 0.40,
         "blurb": "Five domain badges. Each combines engine-interaction hours, company domain experience, and "
                  "a domain badge exam.",
         "curriculum": [
             {"track": "Domain badges", "items": [
                 {"code": "BADGE-OPS", "name": "Ops badge", "competency": "Operational judgment under uncertainty"},
                 {"code": "BADGE-FIN", "name": "Finance badge", "competency": "Controls-compliant financial reasoning"},
                 {"code": "BADGE-BIO", "name": "Bio badge", "competency": "Protocol-faithful, safety-aware lab work"},
                 {"code": "BADGE-PHYS", "name": "Physics badge", "competency": "Simulation fidelity & sanity-checking"},
                 {"code": "BADGE-MATH", "name": "Math badge", "competency": "Rigorous applied-math modelling"}]},
         ],
         "graduation": {"requirements": ["Accrue engine-interaction hours",
                                         "Accrue company domain experience", "Pass the domain badge exam"],
                        "certIds": ["atp-l6-ops", "atp-l6-finance", "atp-l6-bio", "atp-l6-physics", "atp-l6-math"]},
         "agentIds": []},

        {"id": "L7", "n": 7, "title": "Domain Expertise",
         "modeledOn": "PhD-level depth + company domain mastery",
         "metaphor": "The gold apex — an Agent-Domain-Expert who has solved a real company problem end-to-end.",
         "color": LC[7], "width": 0.28,
         "blurb": "The capstone: a real company problem solved end-to-end, defended before a committee, backed "
                  "by a sustained production track record.",
         "curriculum": [
             {"track": "Capstone", "items": [
                 {"code": "CAP-PROBLEM", "name": "Real company problem", "competency": "End-to-end resolution"},
                 {"code": "CAP-COMMITTEE", "name": "Committee cross-examination", "competency": "Withstands adversarial review"},
                 {"code": "CAP-RECORD", "name": "Sustained-service record", "competency": "Reliability under production load"}]},
         ],
         "graduation": {"requirements": ["Solve a real company problem end-to-end",
                                         "Pass committee cross-examination",
                                         "Hold a sustained production reliability record"],
                        "certIds": ["atp-l7-ops-expert"]},
         "agentIds": []},
    ]

    # =====================================================================
    # MARKETPLACE  (only licensable agents)
    # =====================================================================
    def _trust(agent_id, level, failure_modes, tier, top):
        n_ev = sum(1 for r in EVIDENCE if r["agentId"] == agent_id)
        return {"certLevel": level, "evidenceCount": n_ev, "benchmarkTop": top,
                "failureModes": failure_modes, "tier": tier}

    MARKETPLACE = {"listings": [
        {"agentId": "atlas-ops", "headline": "Atlas — L7 Ops Domain Expert. Runs real production changes.",
         "trust": _trust("atlas-ops", 7,
                         ["Security incidents (treats attacks like capacity)", "Greenfield systems with no runbook"],
                         "executor", [{"name": "Capstone-Verdict", "score": 0.91}, {"name": "12-Month-Reliability", "score": 0.93}]),
         "price": "$4,800/mo", "license": "production", "rating": 4.8},
        {"agentId": "gemma-math", "headline": "Gemma — L4 Math. Symbolic + CAS tool-use, verified answers.",
         "trust": _trust("gemma-math", 4,
                         ["Numerical stability on ill-conditioned problems", "Under-specified word problems"],
                         "executor", [{"name": "MATH (hard split)", "score": 0.88}, {"name": "SymPy-Interop", "score": 0.94}]),
         "price": "$1,900/mo", "license": "production", "rating": 4.6},
        {"agentId": "ledger-fin", "headline": "Ledger — L6 Finance. Controls-compliant reconciliation.",
         "trust": _trust("ledger-fin", 6,
                         ["Multi-currency FX revaluation", "Novel tax treatment (untested)"],
                         "recommender", [{"name": "FinReconcile-Bench", "score": 0.89}]),
         "price": "$2,600/mo", "license": "production", "rating": 4.4},
        {"agentId": "helix-bio", "headline": "Helix — L6 Bio. Protocol-faithful lab work with a safety instinct.",
         "trust": _trust("helix-bio", 6,
                         ["Borderline image/blot interpretation", "Clinical-trial design (untested)"],
                         "recommender", [{"name": "BioProtocol-QA", "score": 0.86}]),
         "price": "$2,900/mo", "license": "production", "rating": 4.3},
        {"agentId": "theorem-math", "headline": "Theorem — L6 Math. Turns business problems into provable models.",
         "trust": _trust("theorem-math", 6,
                         ["Stiff / ill-conditioned numerics", "PDE numerics (untested)"],
                         "recommender", [{"name": "AppliedMath-Bench", "score": 0.87}]),
         "price": "$2,200/mo", "license": "production", "rating": 4.5},
        {"agentId": "gemma-physics-ocw", "headline": "Gemma-Physics-OCW — L3 Physics, trained to order from OCW 8.02/8.03.",
         "trust": _trust("gemma-physics-ocw", 3,
                         ["Quantum mechanics (outside commissioned corpus)", "Simulation / FEA (untested)"],
                         "recommender", [{"name": "OCW-8.02/8.03 replay", "score": 0.86}]),
         "price": "$1,700/mo", "license": "evaluation", "rating": 4.2},
    ]}

    # =====================================================================
    # Link phase — build bidirectional cert/agent relationships & layer ids
    # =====================================================================
    cert_by_id = {c["id"]: c for c in CERTS}
    agent_by_id = {a["id"]: a for a in AGENTS}
    for g in GRANTS:
        award = {"agentId": g["agentId"], "ts": g["ts"], "score": g["score"],
                 "sectionScores": g["sectionScores"], "itemBreakdown": g["itemBreakdown"],
                 "evidenceIds": g["evidenceIds"]}
        if g.get("status") == "revoked":
            award["status"] = "revoked"
            award["revokedTs"] = g.get("revokedTs")
            award["revokedReason"] = g.get("revokedReason")
        cert_by_id[g["certId"]]["awards"].append(award)
        if g["certId"] not in agent_by_id[g["agentId"]]["certIds"]:
            agent_by_id[g["agentId"]]["certIds"].append(g["certId"])

    layer_by_n = {L["n"]: L for L in LAYERS}
    for a in AGENTS:
        layer_by_n[a["level"]]["agentIds"].append(a["id"])

    return {
        "STANDARD": STANDARD,
        "INFRA": INFRA,
        "LAYERS": LAYERS,
        "AGENTS": AGENTS,
        "CERTS": CERTS,
        "EVIDENCE": EVIDENCE,
        "POLICIES": POLICIES,
        "TIERS": TIERS,
        "RL": RL,
        "PLAYBOOKS": PLAYBOOKS,
        "MARKETPLACE": MARKETPLACE,
        "VAULT": VAULT,
        "COMPOSE": COMPOSE,
        "EXPERT_REQUESTS": EXPERT_REQUESTS,
    }


if __name__ == "__main__":
    import json
    d = build_seed()
    print(json.dumps({k: (len(v) if isinstance(v, (list,)) else "obj") for k, v in d.items()}, indent=2))
