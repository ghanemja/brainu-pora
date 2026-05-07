# Partition

## Definition

A **partition** is a parallel primitive that reorders an array $A$ such that all elements satisfying a given predicate $P$ appear before those that do not. More formally:

Given:
- An array $A$ of $n$ elements
- A boolean predicate $P: A \to \{\text{true}, \text{false}\}$

**Partition** produces a reordered permutation of $A$ where:
$$A' = [a_1, a_2, \ldots, a_k, a_{k+1}, \ldots, a_n]$$

such that $P(a_i) = \text{true}$ for all $i \in [1, k]$ and $P(a_i) = \text{false}$ for all $i \in (k, n]$. The relative order among elements within each group may be arbitrary (unlike [[Filter]], which preserves original order).

## Key Equations

**Work Complexity:**
$$W(\text{Partition}) = O(|A|)$$

**Depth (Parallel Complexity):**
$$D(\text{Partition}) = O(\log |A|)$$

These bounds assume:
- The predicate $P$ evaluates in $O(1)$ work and $O(1)$ depth
- The partition uses scan-based implementation (see [[Scan]]) as a subroutine

## Physical Intuition / Derivation

### How Partition Works

The key insight is to use two scans to compute destination addresses:

1. **Mark Phase**: Create a binary indicator array where $B[i] = 1$ if $P(A[i]) = \text{true}$, else $B[i] = 0$.

2. **Address Computation (Two Scans)**:
   - **Forward scan**: Compute $L[i] = \sum_{j=1}^{i-1} B[j]$ — the rank of element $i$ among elements satisfying $P$
   - **Backward scan**: Compute $R[i] = \sum_{j=i+1}^{n} (1 - B[j])$ — the rank among elements not satisfying $P$
   
   The destination index is:
   $$\text{dest}[i] = \begin{cases} L[i] & \text{if } P(A[i]) = \text{true} \\ k + R[i] & \text{if } P(A[i]) = \text{false} \end{cases}$$
   where $k = \sum_{j=1}^{n} B[j]$ is the total count of true elements.

3. **Parallel Write**: All elements write to their computed destinations in parallel.

### Why This Achieves Complexity Bounds

- **Work**: Each scan is $O(n)$; the predicate evaluations and parallel writes are $O(n)$ total → $O(n)$ work overall
- **Depth**: Each scan has $O(\log n)$ depth; all phases execute sequentially but independently → $O(\log n)$ depth total

This is fundamentally different from sequential partitioning (e.g., Hoare partition) which requires sequential pointer management.

## Applications in Engineering

### 1. Parallel Sorting
Partition is a core subroutine in parallel quicksort and other divide-and-conquer algorithms. It enables efficient load balancing by separating elements into independent subproblems.

### 2. Data Filtering and Preprocessing
In machine learning pipelines, partition efficiently removes outliers or separates classes:
$$\text{valid\_data} = \text{Partition}(D, \lambda x. |x| < \sigma)$$

### 3. Graph Processing
Partition vertices by properties (e.g., visited vs. unvisited in BFS) with logarithmic depth:
$$\text{frontier} = \text{Partition}(V, \lambda v. \text{discovered}[v] = \text{false})$$

### 4. Database Query Processing
SQL-like WHERE clauses benefit from parallel partitioning:
$$\text{SELECT} \, * \, \text{WHERE} \, A > 100$$
can be implemented as `Partition(A, λx. x > 100)`.

### 5. Quicksort Implementation
Classical divide-and-conquer sorting in parallel settings:
- Partition around pivot
- Recursively sort both sides in parallel
- Achieves better constants than [[Comparison sort|comparison sort]] when pivots are well-chosen

## Common Mistakes / Pitfalls

### 1. Confusing Partition with Filter
**Mistake**: Assuming partition preserves original order like filter does.

**Reality**: Partition may reorder elements within the true/false groups. Use [[Filter]] if order preservation is critical.

### 2. Ignoring Output Structure
**Mistake**: Writing code that assumes the "true" group occupies indices $[0, k)$ without computing $k$ first.

**Reality**: Always compute the split point $k$ via a final scan or reduce operation to get the count.

### 3. Non-Boolean Predicates
**Mistake**: Attempting to partition with multi-valued predicates (e.g., "red, blue, green").

**Reality**: Partition is binary. For $m$-way partitioning, apply partition recursively or use generalized radix sorting.

### 4. Predicate Side Effects
**Mistake**: Using predicates with I/O or state mutations in parallel evaluation.

**Reality**: Predicates must be pure functions evaluated independently across all elements simultaneously.

### 5. Overestimating Practical Speedup
**Mistake**: Expecting $O(\log n)$ depth to translate directly to wall-clock speedup with $n$ cores.

**Reality**: Communication costs, NUMA effects, and small constant factors dominate for practical array sizes. Actual speedup depends on cache locality and memory bandwidth.

## See Also

- [[Scan]] — Prefix sum primitive underlying partition's implementation
- [[Filter]] — Similar to partition but preserves order within groups
- [[Reduce]] — Aggregate operation often used with partition for statistics
- [[Comparison sort]] — Alternative sorting approach with $O(n \log n)$ work
- [[Hashing]] — Partitioning elements into hash buckets uses similar addressing principles

## Sources

- Lecture