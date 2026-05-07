# Occurrence Lists

## Definition

An **occurrence list** $\Lambda_a$ for a letter $a \in \Sigma$ is a data structure that maintains a complete record of all positions where the letter $a$ appears in a word $w \in \Sigma^*$.

Formally, for a word $w = w_1 w_2 \cdots w_n$:

$$\Lambda_a = \{i \in \mathbb{N} \mid 1 \leq i \leq |w|, w_i = a\}$$

The **count of occurrences** of letter $a$ in word $w$ is:
$$\text{nocc}[a] = |\Lambda_a|$$

In the context of semi-extensible zero-growth (ZG) languages, occurrence lists track which letters are **rare** (occur fewer than $p$ times) versus **frequent** (occur $\geq p$ times), where $p \in \mathbb{N}$ is a fixed threshold parameter.

A letter $a$ is classified as:
- **Neutral**: contributes nothing to language membership
- **Rare**: $|\Lambda_a| < p$ (fewer than $p$ occurrences)  
- **Non-neutral and frequent**: $|\Lambda_a| \geq p$ (at least $p$ occurrences)

## Key Equations

**Membership condition** (from Definition 5.2):

A word $w$ belongs to semi-extensible ZG language $L$ if and only if:
$$w \in L \iff w[l,r] \in \text{Cond}(T)$$

where $T = \{a \in \Sigma \mid a \text{ is non-neutral and } \text{nocc}[a] \geq p\}$ for all valid infixes $w[l,r]$.

**Occurrence count update** (Algorithm 1, line 15):

When moving the right endpoint $r \rightarrow r-1$, if the exiting letter is $a = w[r]$:
$$\text{nocc}'[a] \gets \text{nocc}'[a] - 1$$

**Rarity threshold transition**:

Letter $a$ transitions from frequent to rare when:
$$\text{nocc}'[a] = p - 1 \quad \text{(just became rare)}$$

## Physical Intuition / Derivation

### Why Occurrence Lists Matter

In the context of **enumeration algorithms** for word infixes in regular languages, directly checking each potential infix against a language definition is prohibitively expensive. Occurrence lists provide an **incremental view** of letter frequencies that enables constant-time membership decisions (Lemma 5.6).

### Three-Phase Categorization Strategy

The algorithm partitions the alphabet $\Sigma$ into three disjoint sets:

1. **Neutral letters** ($N$): letters whose count never affects membership
2. **Rare letters** ($R(l,r)$): letters with count $< p$ in infix $w[l,r]$
3. **Frequent letters** ($F(l,r)$): letters with count $\geq p$ in infix $w[l,r]$

The power of this approach:
- Store only *rare* letter positions explicitly (sparse!)
- Frequent letters are tracked by count alone
- When transitioning $l \to l+1$ or $r \to r-1$, update counts incrementally
- Only when a letter crosses the $p$ threshold do we need to update the rare list

### Background Traversal Pattern

The algorithm maintains **parallel background traversals** of each $\Lambda_a$:

- **StartMinBackgroundTraversal** (line 4): Initial forward pass to establish baseline counts
- **MaxLeftBackgroundTraversal** (line 39): Backward pass used when iterating $l > 1$

These background processes run in parallel (not sequentially), enabling amortized $O(1)$ updates.

## Applications in Engineering

### 1. **Text Search and Pattern Matching**

Occurrence lists accelerate substring matching in DNA sequencing and full-text search engines by avoiding redundant alphabet scans.

### 2. **Finite Automata Enumeration**

In compiler construction and regex engines, occurrence lists enable **fast infix enumeration** of regular languages—critical for lexical analysis without scanning every position repeatedly.

### 3. **Symbolic Dynamics and Complexity Theory**

In formal language theory, occurrence lists quantify **letter frequency constraints**, essential for defining languages with growth restrictions (zero-growth languages) used in symbolic computation.

### 4. **Data Compression**

Adaptive compression algorithms (e.g., context modeling) rely on precise occurrence statistics. Maintaining occurrence lists allows real-time frequency updates without full re-scanning.

### 5. **Bioinformatics: k-mer Analysis**

In genomics, occurrence lists track the frequency of DNA k-mers (short substrings) across a sequence, enabling detection of genomic features and conservation patterns.

## Common Mistakes / Pitfalls

### 1. **Confusing Occurrence Count with Position**

**Mistake**: Assuming $\text{nocc}[a]$ directly gives a position in $w$.

**Correct understanding**: $\text{nocc}[a]$ is merely a scalar count; the actual positions are stored in $\Lambda_a$ itself.

### 2. **Off-by-One Errors in Rare/Frequent Transitions**

**Mistake**: Treating the threshold as $\text{nocc}[a] > p$ instead of $\text{nocc}[a] \geq p$.

**Correct understanding**: A letter becomes frequent at exactly $p$ occurrences; it becomes rare when it drops to $p-1$ (line 17).

### 3. **Forgetting Neutral Letter Handling**

**Mistake**: Allocating occurrence lists for all letters indiscriminately.

**Correct understanding**: Neutral letters must be excluded from the set $T$ (line 11) and never trigger rare-occurrence updates.

### 4. **Naive Re-computation on Every Iteration**

**Mistake**: Rebuilding $\Lambda_a$ or $T$ from scratch for each $(l,r)$ pair.

**Correct understanding**: Use incremental updates (Algorithm 1 employs background traversals) to amortize cost