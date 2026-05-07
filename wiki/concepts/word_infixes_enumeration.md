# Word Infixes Enumeration

## Definition

**Word infixes enumeration** is the algorithmic problem of efficiently identifying and listing all contiguous substrings (infixes) of a word $w \in \Sigma^*$ that belong to a regular language $L$. Formally:

Given a word $w = w_1 w_2 \cdots w_n$ over alphabet $\Sigma$ and a regular language $L \subseteq \Sigma^*$, enumerate all pairs $(l, r)$ with $1 \leq l \leq r \leq |w|$ such that $w[l,r] \in L$.

In the context presented here, the language $L$ is a **semi-extensible Zero-Gap (ZG) language**, defined operationally as:

$$L = \{w \in \Sigma^* \mid \text{for all non-neutral letters } a, \, |w|_a < p\}$$

where:
- $|w|_a$ denotes the number of occurrences of letter $a$ in $w$
- $p \in \mathbb{N}$ is a fixed threshold (typically $p \geq 2$)
- Letters are partitioned into **neutral** (unbounded occurrences allowed) and **non-neutral** (occurrence-bounded)

The key constraint distinguishing this from naive enumeration is that membership in $L$ depends only on the **occurrence counts** of non-neutral letters, not their positions.

## Key Equations

The fundamental characterization relies on **occurrence counts**:

$$\text{Condition for } w[l,r] \in L: \quad \forall a \in \Sigma_{\text{non-neutral}}, \quad |w[l,r]|_a < p$$

The three equivalent definitions (Proposition 5.5) state that a word belongs to $L$ iff:

1. **Threshold definition**: All non-neutral letters appear fewer than $p$ times
2. **Conditional definition**: The word matches the conditional language $\text{Cond}(T)$ where $T = \{a \mid |w|_a \geq p\}$
3. **Extensibility definition**: The word satisfies specified extensibility constraints

The letter classification for position $r$ in word $w$:

$$\text{nocc}'[a] = \left|\{i \in [l, r] : w_i = a\}\right|$$

$$\text{Rare}_a(l,r) = \begin{cases} 1 & \text{if } a \text{ non-neutral and } \text{nocc}'[a] < p \\ 0 & \text{otherwise} \end{cases}$$

## Physical Intuition / Derivation

### Why This Problem Matters

Classical enumeration of all $O(n^2)$ substrings is naive. For large texts, we need algorithms respecting the **structural constraint** that membership depends only on letter occurrence counts, not arrangements.

### Algorithmic Strategy: Constant-Time Enumeration per Infix

**Algorithm 1** achieves amortized constant-time per reported infix by:

1. **Outer loop over left endpoint** $l = 1$ to $|w|$:
   - For each $l$, shrink the right endpoint $r$ from $|w|$ downward
   
2. **Occurrence tracking** (lines 2–4):
   - Maintain `nocc[a]` = total occurrences of letter $a$ in the full word
   - Use **background traversals** of occurrence lists $\Lambda_a$ to efficiently track when occurrences enter/exit the window $[l,r]$

3. **Output condition** (lines 12–13):
   - Output $(l,r)$ when:
     - The word encoded in $\Delta$ (rare letter occurrences) belongs to $\text{Cond}(T)$, where $T$ is the set of "frequent" non-neutral letters
     - All non-neutral letters appear $< p$ times in $w[l,r]$

4. **Decrement and re-evaluate** (lines 14–19):
   - Move right endpoint leftward: $r \to r-1$
   - Update `nocc'[a]` for $a = w[r]$ (this letter exits the window)
   - When a letter transitions from frequent to rare ($\text{nocc}'[a] = p-1$), call `GetRareOccurrencesSingle` to locate its occurrences

### Why Background Traversals Work

Rather than scanning $\Lambda_a$ from scratch each iteration, **background traversals** maintain persistent pointers:

- **Min background traversal**: Identifies rare occurrences in the first iteration ($l=1$), moving forward through $\Lambda_a$ as $r$ decreases
- **Max-left background traversal**: For $l > 1$, tracks rare occurrences more efficiently by reusing prior traversal state, avoiding redundant scans

This amortization reduces per-infix cost from $O(n)$ to $O(1)$ amortized.

## Applications in Engineering

### 1. **Computational Biology**
- **DNA/Protein sequence analysis**: Finding all substrings with constrained nucleotide/amino acid composition (e.g., GC-content bounds, rare amino acids)
- **Motif discovery**: Locating regulatory regions with bounded occurrence of specific codons

### 2. **Text Processing & NLP**
- **Keyword filtering**: Identifying text segments with constrained vocabulary (bounded slang, repeated words, forbidden phrases)
- **Linguistic analysis**: Finding sentences with rare morphological patterns without enumerating all $O(n^2)$ substrings

### 3. **Network Security**
- **Malware detection**: Scanning packet streams for payload substrings matching anomaly signatures (e.g., bounded repeating byte patterns)
- **Intrusion detection**: Efficient pattern matching where threat indicators depend on frequency thresholds, not positions

### 4. **Data Stream Processing**
- **Sliding window statistics**: Computing properties of all contiguous segments of sensor/log data where membership is occurrence-based (not position-based)
- **Real-time quality metrics**: Flagging data windows violating frequency constraints

### 5. **Compiler Design**
- **