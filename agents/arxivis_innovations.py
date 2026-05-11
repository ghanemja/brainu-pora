"""
Innovation extractor for arXivis — replace raw token-tfidf with real
named-innovation candidates pulled from a paper's text.

Goal: every paper that contributes something new produces a list of
"innovation candidates" — short noun-phrases that name what the paper
proposes / introduces / defines / improves. These are the things that
either (a) connect to existing concept manifold nodes or (b) are
genuinely new and worth proposing as new nodes.

Strategy (no external NLP deps — just regex):
  1. Authorial-claim patterns ("we propose X", "we introduce X",
     "this paper presents X", "novel X", "new X", …) → high-priority.
  2. Title-of-thing patterns (Capitalized phrase + algorithm / theorem
     / framework / method / model / protocol / technique / lemma /
     bound / approximation / decomposition / oracle).
  3. Hyphenated-quantifier patterns (k-center, log-space, near-linear,
     constant-time, sublinear, polynomial-time).
  4. Greek + capital combos (α-tree, β-norm, k-NN, etc.).
  5. Dedupe / merge near-duplicates.
  6. Filter against the existing concept vocabulary — anything that
     overlaps an existing concept name gets tagged kind="connects",
     everything else is kind="proposes" (i.e. candidate-new-node).

Output per paper:
  innovations: [{ phrase, kind: "proposes"|"connects",
                  connects_to: [wiki_id, ...], pattern: "we-propose"|… }]
"""

from __future__ import annotations

import re

# ── Patterns ─────────────────────────────────────────────────────────────

# Authorial claim phrasings (case-insensitive)
CLAIM_PATTERNS = [
    re.compile(r"\bwe (?:propose|introduce|present|develop|design|construct|define|prove|study|investigate)\s+(?:a |an |the |our |new |novel )?([^.,;:()]{6,80})", re.I),
    re.compile(r"\bthis (?:paper|work|study|note) (?:proposes?|introduces?|presents?|establishes?|gives?|develops?|describes?|studies)\s+(?:a |an |the |new |novel )?([^.,;:()]{6,80})", re.I),
    re.compile(r"\b(?:our|the) (?:main|primary|key|central) (?:contribution|result|theorem|finding|claim)\s+(?:is|are|states)\s+(?:that\s+)?([^.,;:()]{6,80})", re.I),
    re.compile(r"\b(?:propose|introduce|present)\s+(?:a |an |the )?(novel|new|first|fastest|optimal|near-optimal|sublinear|near-linear|polynomial-time|constant-time)\s+([^.,;:()]{6,80})", re.I),
]

# Named-thing pattern: capitalized phrase followed by canonical noun
THING_NOUN = r"(?:algorithm|theorem|framework|method|methodology|technique|protocol|architecture|model|bound|inequality|decomposition|approximation|oracle|lemma|estimator|sketch|filter|reduction|encoding|construction|formulation)"
NAMED_THING = re.compile(
    r"\b((?:[A-Z][a-zA-Z0-9-]+(?:'s)?\s+){1,4})(" + THING_NOUN + r")\b"
)

# Hyphenated technical phrases ("near-linear time", "constant-time", "log-space")
HYPHEN_PHRASE = re.compile(
    r"\b((?:near-|sub-|poly-|quasi-|almost-|fully-)?(?:linear|polynomial|logarithmic|sublinear|exponential|constant|optimal|adaptive|approximate|deterministic|randomized)-(?:time|space|round|round-complexity|query|optimal|approximation))\b",
    re.I,
)

# Greek/k-prefixed terms ("k-center", "α-tree", "ε-net")
KGREEK = re.compile(r"\b([kkmnε𝛼𝛽𝜀αβε])-([a-z]{3,16})\b")

# Filter junk
JUNK_PREFIX = re.compile(r"^(?:the |a |an |this |our |their |such |these |those |many |most |some )", re.I)
WHITESPACE  = re.compile(r"\s+")


def _clean(s: str) -> str:
    s = WHITESPACE.sub(" ", s).strip(" ,.;:()[]")
    s = JUNK_PREFIX.sub("", s)
    return s.strip()


def extract_innovations(text: str, max_n: int = 8) -> list[dict]:
    """Return ranked innovation candidates with the pattern that matched."""
    out: list[dict] = []
    seen: set[str] = set()

    def add(phrase: str, pattern: str, priority: int):
        phrase = _clean(phrase)
        if not phrase or len(phrase) < 5 or len(phrase) > 80:
            return
        key = phrase.lower()
        if key in seen:
            return
        # reject single common words
        if len(phrase.split()) == 1 and len(phrase) < 7:
            return
        seen.add(key)
        out.append({"phrase": phrase, "pattern": pattern, "priority": priority})

    # 1. Authorial-claim patterns
    for pat in CLAIM_PATTERNS:
        for m in pat.finditer(text):
            # Last group is the captured innovation phrase
            phrase = m.group(m.lastindex)
            add(phrase, "claim", priority=3)

    # 2. Named-thing patterns ("Welzl orders algorithm")
    for m in NAMED_THING.finditer(text):
        add(m.group(0), "named", priority=2)

    # 3. Hyphenated technical phrases
    for m in HYPHEN_PHRASE.finditer(text):
        add(m.group(1), "hyphen", priority=1)

    # 4. k-/Greek-prefixed
    for m in KGREEK.finditer(text):
        add(f"{m.group(1)}-{m.group(2)}", "kgreek", priority=1)

    # Rank: priority desc, then earlier position wins ties
    out.sort(key=lambda x: -x["priority"])
    return out[:max_n]


def classify_against_vocab(
    innovations: list[dict],
    concept_name_index: dict[str, str],
) -> list[dict]:
    """
    For each candidate, mark kind="connects" if the phrase substring-matches
    an existing concept name; otherwise kind="proposes".
    """
    enriched = []
    for innov in innovations:
        phrase_lc = innov["phrase"].lower()
        connects = []
        for name_lc, wid in concept_name_index.items():
            if len(name_lc) < 5:
                continue
            if name_lc in phrase_lc or phrase_lc in name_lc:
                connects.append(wid)
        enriched.append({
            **innov,
            "kind":         "connects" if connects else "proposes",
            "connects_to":  connects[:3],
        })
    return enriched


if __name__ == "__main__":
    sample = """
    We propose a near-linear time algorithm for computing Welzl orders on
    graphs with linear neighborhood complexity. This paper presents a novel
    randomized k-center approximation that improves on Chazelle's bound.
    The main contribution is that our framework runs in polynomial-time
    and yields constant-time queries via an ε-net data structure.
    """
    for i in extract_innovations(sample):
        print(i)
