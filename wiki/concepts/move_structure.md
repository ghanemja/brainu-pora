# move structure

## Definition

A **move structure** is a compressed data structure representation for a permutation $\pi$ of the integer range $[0, n)$. It encodes the permutation as a covering set of **disjoint intervals** (contiguous subsets of the domain), requiring only $O(r)$ words of storage, where $r$ is a problem-dependent parameter measuring the "run-length" of the permutation.

Formally, for a permutation $\pi: [0, n) \to [0, n)$, the run-length parameter $r$ is defined as:

$$r = 1 + \left|\{i \in [1, n) : \pi(i) - 1 \neq \pi(i-1)\}  \right|$$

This counts the number of "breakpoints" where consecutive elements in the permutation are not consecutive in value, plus one for the initial interval.

### Key Property

Given:
- The interval index containing position $i$
- The move structure data

One can compute:
- $\pi(i)$ (the permutation value at $i$)
- The interval index containing $\pi(i)$

All in **$O(1)$ constant time**.

## Key Equations

**Run-length parameter:**
$$r = 1 + \left|\{i \in [1, n) : \pi(i) - 1 \neq \pi(i-1)\}  \right|$$

**Space complexity:**
$$\text{Space} = O(r) \text{ words}$$

**Query time:**
$$\text{Query}(\pi(i)) = O(1)$$

**Optimal construction time (Brown et al., 2026):**
$$\text{Construction Time} = O(r)$$

**Previous best construction time (Bertram et al.):**
$$\text{Construction Time} = O(r \log r)$$

## Physical Intuition / Derivation

### Why This Structure Works

Consider a permutation where consecutive positions map to consecutive (or nearly consecutive) output values. For instance:
- Positions $[0, 5)$ map to $[10, 15)$
- Positions $[5, 10)$ map to $[0, 5)$  
- Positions $[10, 15)$ map to $[15, 20)$

Traditional permutation storage requires $O(n)$ space to store all mappings. However, **if we can partition the domain into few intervals where values within each interval permute to a contiguous block of outputs**, we can represent the permutation implicitly with far fewer stored values.

### The Interval Decomposition

The move structure partitions $[0, n)$ into intervals $I_1, I_2, \ldots, I_m$ such that:
1. Each interval is **contiguous** in the domain
2. For each interval $I_j$, the set $\pi(I_j)$ forms a **contiguous block** in the codomain (modulo wrapping)
3. The number of intervals $m$ is bounded by the run-length $r$

**Why minimal intervals equal run-length:** A new interval must start whenever the output values "break" (become non-consecutive). The run-length parameter counts exactly these breakpoints.

### Navigation Efficiency

Once intervals are identified, the structure stores:
- The boundary positions of each interval
- The offset mapping each interval to its output range

This enables constant-time navigation: given position $i$ in interval $I_j$ mapping to output offset $\delta_j$, we compute $\pi(i) = I_j[\text{start}] + (i - I_j[\text{start}]) + \delta_j$ in $O(1)$ time.

## Applications in Engineering

### 1. **Genomic Sequence Alignment**

The most cited application is computing the **longest common prefix (LCP) array** from a run-length-encoded Burrows-Wheeler Transform (BWT):
- The BWT transform produces "runs" of repeated characters, naturally yielding small $r$
- Move structures allow LCP computation in $O(r)$ working space and $O(n)$ total time
- Essential for memory-efficient DNA sequence assembly and alignment

### 2. **Suffix Array Construction**

In text indexing and pattern matching:
- Permutations arising from suffix arrays often have small run-length
- Move structures reduce space overhead in suffix array construction algorithms
- Enables processing of large genomes on memory-constrained systems

### 3. **Data Compression**

For permutation-based compression schemes:
- Represents sparse or structured permutations without storing all $n$ mappings
- Applicable to run-length-encoded data common in log files, sensor streams, and bioinformatic data

### 4. **Graph Algorithms**

For permutations arising from graph reordering and renumbering:
- Useful when vertices are relabeled according to specific traversal patterns
- Supports efficient memory-constrained computation on large graphs

## Common Mistakes / Pitfalls

### 1. **Confusing Interval Boundaries with Output Values**

**Mistake:** Assuming intervals partition the output (codomain) rather than the input (domain).

**Clarification:** Intervals partition the domain $[0, n)$. Each interval maps to a contiguous output block, but the construction focuses on counting input-side breakpoints.

### 2. **Thinking $r = n$ Always**

**Mistake:** Assuming every permutation requires $r = n$ intervals.

**Reality:** Only the identity permutation achieves $r = 1$. Random permutations have $r \approx n$, but **structured** permutations (common in bioinformatics, compression, and reordering applications) have $r \ll n$.

### 3. **Overlooking the Asymptotic Improvement**

**Mistake:** Dismissing the $O(r)$ vs. $O(r \log r)$ improvement as negligible.

**Impact:** For practical cases where $r$ is moderate (e.g., $r \sim 10^4$), the factor of $\log r \sim 14$ means 10–100× speedup in construction. The $O(r)$ construction is **optimal** in theory and substantially faster in practice.

### 4. **Misapplying Without Profiling $r$**

**Mistake