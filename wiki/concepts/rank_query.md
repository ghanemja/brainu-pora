# rank query

## Definition

A **rank query** is a fundamental operation on a structured array or sequence that returns the number of elements with a specific property up to a given position. In the context of permutation-based data structures (particularly those used in compressed text indexing), a rank query on a set $P$ determines which **input interval** contains a given element.

Formally, for a set of input intervals $P = \{[P[j], P[j+1]) \mid j \in [0, r)\}$ partitioning the range $[0, n)$, the rank query $P.\text{rank}(i)$ returns the interval index $j$ such that $i \in [P[j], P[j+1])$.

In the context of move structures with permutations $\pi$, a rank query identifies which input interval contains the image $\pi(i)$ of a position $i$, enabling efficient traversal of permutation-based representations.

## Key Equations

For a position $i \in [0, n)$ and input intervals $P[0..r]$:

$$j = P.\text{rank}(i) \iff P[j] \leq i < P[j+1]$$

Given a permutation $\pi$ and its output intervals $Q = \text{sort}(P_\pi) \cup \{n\}$, the interval mapping permutation $\tau$ relates input and output intervals:

$$\tau(j) = k \iff P_\pi[j] = Q[k]$$

The cost of determining which output interval contains $\pi(i)$ without a dedicated rank query structure is:

$$T_{\text{move}}(i) = O\left(\left|\left(Q[k], Q[k] + (i - P[j] + 1)\right) \cap P\right|\right)$$

where $k = \tau(j)$ and $j = P.\text{rank}(i)$.

## Physical Intuition / Derivation

### The Problem Context

Consider a permutation $\pi$ represented implicitly through runs of identical values in a compressed structure (like RLBWT). To apply $\pi$ to a position $i$:

1. **Find the input interval**: Determine which partition $j$ contains $i$ — this is what a rank query does
2. **Compute the output**: Use the permutation's structure to find $\pi(i)$
3. **Find the output interval**: Determine which partition contains $\pi(i)$ — requiring another rank query

### Why Rank Queries Matter

Without efficient rank queries, finding which interval contains an element requires **linear scanning** through all $r$ intervals. This degrades performance from $O(1)$ to $O(r)$ per operation.

The balanced move structure stores precomputed rank information:
- **$P_\text{rank}(\pi)$**: For each input interval $j$, store $P.\text{rank}(\pi(i))$ for representative elements
- **$\tau$**: Permutation mapping between interval orderings

This allows the move query to start the linear scan from a relevant position rather than from $P[0]$, reducing average case complexity and enabling balancing techniques.

### Interval Intersection Model

The key insight is that the cost of a move query depends on how many input intervals overlap with the output range $[Q[k], Q[k] + \delta)$ where $\delta = i - P[j] + 1$ is the offset within the interval. If intervals are **balanced** (intersections are bounded), rank queries become implicit, enabling $O(1)$ time.

## Applications in Engineering

### 1. **Compressed Text Indexing (BWT & RLBWT)**
Rank queries enable efficient computation of the **LF mapping** (Last-First) in Burrows-Wheeler Transform, fundamental to:
- Full-text search indices with linear space
- Pattern matching in milliseconds on gigabyte-scale texts

### 2. **Suffix Array Construction**
Fast rank queries on permutations accelerate suffix array and suffix tree construction algorithms, reducing time complexity in genome sequencing and string processing.

### 3. **Compressed Suffix Arrays (CSA)**
CSA data structures use rank/select operations to navigate compressed representations of suffix arrays without materializing them fully.

### 4. **Bioinformatics Sequence Analysis**
DNA/protein sequence alignment and pattern discovery rely on efficient rank queries to handle permutation-based indices over compressed genomic data.

### 5. **Data Compression & Entropy Encoding**
Rank queries enable navigation through context models and hierarchical interval structures in arithmetic and range coders.

### 6. **Wavelet Trees & Succinct Data Structures**
Rank/select operations form the primitive building blocks for constructing space-efficient rank/select structures that query and navigate tree-like hierarchies.

## Common Mistakes / Pitfalls

### 1. **Confusing Rank with Selection**
- **Rank query** $P.\text{rank}(i)$: "Which interval contains position $i$?" → returns interval index
- **Select query** $P.\text{select}(j, k)$: "What is the $k$-th occurrence of interval $j$?" → returns position
- These are inverse operations; using one when the other is needed breaks algorithms

### 2. **Ignoring Interval Structure**
Students often treat rank queries as simple binary search on a flat sorted array. The **interval-based abstraction** is crucial:
- Intervals are $P[0..r]$ partitions, not individual elements
- Rank returns an interval index, not an element index

### 3. **Underestimating Space Costs**
Pre-storing $P_\text{rank}(\pi)$ tables appears to be $O(r)$ space and seems negligible, but:
- On highly repetitive texts, $r \ll n$, so this is actually cheap
- On random texts, $r \approx n$, making the structure less effective
- The precomputation cost (Lemma 7-8) must be factored in

### 4. **Assuming O(1) Without Balancing**
The unbalanced move structure has worst-case $O(r)$ query time despite rank information, because linear scanning through intervals can visit many entries. The balancing technique (Definition 10, interval remapping) is **essential** for achieving true $O(1)$