# merge condition

## Definition

In the context of adaptive sorting algorithms (particularly PowerSort), the **merge condition** is a decision criterion that determines whether two adjacent runs should be merged based on their relative sizes and power assignments.

Formally, given three consecutive runs $R_1$, $R_2$, and $R_3$ with respective sizes $r_1, r_2, r_3$ and powers $p_1, p_2, p_3$, a merge of $R_2$ and $R_3$ is **successful** (or "triggered") when certain invariants are satisfied. The primary merge condition requires:

$$p_3 > p_2$$

This condition ensures that merging $R_2$ and $R_3$ does not violate the power invariants maintained by the algorithm, specifically that the powers of adjacent runs in the final sequence are non-decreasing from left to right.

A merge is **failed** when the merge condition is not met—the algorithm checks whether a merge should occur but determines it should not proceed.

## Key Equations

**Power Definition:** Each run has an assigned power $p$ derived from its position in the input array:
$$p \leq \log_2 \frac{n}{r}$$

where $r$ is the run length and $n$ is the total input size.

**Observation 3 (Power Spacing):** The distance between any index with power $p$ and the closest index with power less than $p$ is:
$$d = \frac{n}{2^{p+1}}$$

Consequently, any contiguous range of $\frac{n}{2^p}$ indices contains either an index with power $p$ or power less than $p$.

**Lemma 3 (Size-Power Relationship):** If a run satisfies $r_3 \geq \frac{n}{2^{p_2}}$, then necessarily:
$$p_3 \leq p_2$$

**Observation 6 (Merge Spacing):** When a merge of $R_3$ and $R_2$ occurs (i.e., $p_3 > p_2$), the distance between the midpoints of $R_3$ and $R_1$ is at least:
$$d_{min} = \frac{n}{2^{p_3+1}}$$

## Physical Intuition / Derivation

### Why Check the Merge Condition?

In adaptive sorting, the goal is to efficiently sort arrays that may contain naturally sorted subsequences (runs). Rather than merging all adjacent runs immediately, PowerSort uses a **lazy merging strategy**: it decides when to merge based on the relative "importance" of runs, encoded by their powers.

The power of a run encodes its position in a hierarchical structure—runs with **higher power are more "recent"** or **higher priority** in the current merging phase. The merge condition $p_3 > p_2$ ensures that:

1. **Stability of power invariants:** If we merge two runs, the resulting run inherits a power that doesn't violate ordering constraints with neighboring runs.

2. **Amortized cost bounds:** By only merging when the condition is met, "successful merges" pay for their own computational cost (walk-back to determine run boundaries). The walk-back cost equals the merge cost when the condition succeeds, making the overall algorithm efficient.

3. **Avoiding redundant merges:** Failed merges (where the condition doesn't hold) represent comparisons that don't immediately trigger merging. The algorithm bounds the total "wasted" work on failed merges using Observation 2 and Observation 3, which guarantee that such failed comparisons can only happen sparsely across power intervals.

### Derivation via Power Intervals

Powers are implicitly maintained through **power intervals**—ranges of array indices assigned to each power level. From Observation 2: indices with the same power $p > 0$ are separated by at least $\frac{n}{2^p}$ elements. This exponential spacing ensures:

- Few indices have high power (dense near the beginning)
- Many indices have low power (sparse toward the end)
- Power levels are "evenly spaced"

When two runs $R_2$ and $R_3$ merge with $p_3 > p_2$, their power intervals $I_2$ and $I_3$ may shift, but the condition $p_3 > p_2$ guarantees the new run's power $p'$ satisfies $p' \leq p_3$, maintaining the non-decreasing power property.

## Applications in Engineering

### 1. **Adaptive Sorting Algorithms**
The merge condition is central to **PowerSort** and related entropy-sensitive sorting schemes. It enables algorithms that adapt automatically to input characteristics (e.g., partially sorted data, runs of equal elements) without explicit passes to detect runs or explicit tuning parameters.

### 2. **Database Query Optimization**
Sorting is a bottleneck in database operators (JOIN, GROUP BY, ORDER BY). Adaptive sort algorithms using merge conditions reduce cost in scenarios like:
- Multi-run external sorts (data doesn't fit in memory)
- Sorting partially-indexed tables
- Adaptive query planning based on observed run distributions

### 3. **Stream Processing and Online Algorithms**
When data arrives as a stream with natural structure (e.g., time-series with gaps), merge conditions allow the system to decide when to finalize and merge blocks of data without buffering excessively.

### 4. **In-Place Sorting with Strict Space Bounds**
PowerSort is strictly in-place: it uses $O(1)$ auxiliary space. The merge condition enables careful scheduling of merges so that temporary buffers are minimized and reclaimed efficiently—critical in embedded systems and memory-constrained environments.

## Common Mistakes / Pitfalls

### 1. **Confusing "Merge Condition" with "Merge Decision"**
The merge *condition* is a mathematical property ($p_3 > p_2$); the merge *decision* is the algorithm's choice. A failed merge (condition not met) doesn't mean the run is never merged—it may merge later when the condition becomes true.

### 2. **Misinterpreting Power as Run Rank**
Powers are **not** simply the ordinal rank of runs (1st, 2nd, 3rd, ...). A run's power depends on its **position in the array**, not its creation order. Two runs created at different times may have the same power if they occupy position ranges