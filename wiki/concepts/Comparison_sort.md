# Comparison sort

## Definition

A **comparison sort** is an algorithm that sorts an array of comparable elements by determining their relative order through pairwise comparisons. The algorithm reads the input array, performs comparisons between elements using a total ordering relation (typically $\leq$ or $<$), and produces a sorted permutation of the input.

In the context of parallel computing, a comparison sort refers specifically to algorithms designed to exploit parallelism—most notably **parallel merge sort**—which decompose the sorting problem into independent subproblems that can be solved concurrently.

## Key Equations

For an array $A$ of $n$ elements sorted via parallel merge sort:

$$\text{Work} = O(n \log n)$$

$$\text{Depth (critical path length)} = O(\log^2 n)$$

More precisely, using efficient implementations with optimal reduction operators:

$$\text{Depth} = O(\log n)$$

where:
- **Work** = total number of instructions executed across all processors
- **Depth** = length of the longest chain of data-dependent instructions (determines minimum parallel time on unlimited processors)

## Physical Intuition / Derivation

### Sequential Baseline
Traditional comparison sorts (quicksort, heapsort, merge sort) require $O(n \log n)$ comparisons in the average or worst case. This is a fundamental lower bound: any comparison-based sort must perform at least $\Omega(n \log n)$ comparisons.

### Parallel Decomposition
Parallel merge sort achieves the same $O(n \log n)$ work by recursively:

1. **Dividing** the array into two halves (constant-depth operation via indexing)
2. **Conquering** by recursively sorting both halves in parallel (depth recurrence: $T(n) = T(n/2) + O(\log n)$ for merging)
3. **Merging** two sorted arrays in parallel using a bitonic merge network or comparison tree (achievable in $O(\log n)$ depth with $O(n \log n)$ work)

The recurrence $T(n) = T(n/2) + O(\log n)$ solves to $T(n) = O(\log^2 n)$, but practical implementations achieve $O(\log n)$ depth through careful parallelization of the merge step.

### Why Work Remains $O(n \log n)$
Parallelism does not reduce the fundamental work required—it only redistributes comparisons across processors. Each element must ultimately "learn" its position relative to all others, necessitating $\Omega(n \log n)$ total comparisons.

## Applications in Engineering

### 1. **Database Query Processing**
- Sorting result sets for GROUP BY, ORDER BY, and JOIN operations
- Parallel sorts across distributed nodes in data warehouses
- Indexing and materialized view maintenance

### 2. **Graphics & Computational Geometry**
- Sorting vertices by spatial coordinates (z-buffer, ray tracing)
- Sweep-line algorithms for polygon clipping and intersection detection
- Parallel sorting of primitives for rendering pipelines

### 3. **Machine Learning & Data Science**
- Sorting feature values for decision tree splits (information gain computation)
- Ranking search results by relevance scores
- Clustering algorithms requiring sorted distances

### 4. **Network & Signal Processing**
- Sorting packet headers by priority (QoS scheduling)
- Finding order statistics (median, percentiles) in signal samples
- Parallel sorting of time-series data for anomaly detection

### 5. **GPU Computing**
- Highly parallel sort algorithms (bitonic sort, odd-even sort) for CUDA/OpenCL
- Efficient memory access patterns on streaming architectures
- Sorting keys for scatter-gather operations in sparse computations

### 6. **Operating Systems**
- Process scheduling (sorting by priority)
- Virtual memory page replacement (sorting page access times)
- Cache coherency protocols

## Common Mistakes / Pitfalls

### 1. **Confusing Work and Depth**
Students often assume parallel sorting is "faster" because depth is $O(\log n)$. In reality:
- Work is still $O(n \log n)$—you need that many comparisons total
- Depth is the parallelizable portion; wall-clock time on $p$ processors is $\Theta(n \log n / p + \log n)$

### 2. **Assuming Sorting is Comparison-Free**
Comparison sorts cannot do better than $\Omega(n \log n)$ work on arbitrary data. Non-comparison sorts (radix sort, counting sort) are $O(n + k)$ but require domain-specific structure (key range, digits).

### 3. **Ignoring Merge Cost**
The recursive structure means merging is as expensive as sorting. A poorly implemented merge can make the full algorithm $\Omega(n^2)$ work despite $O(\log n)$ depth.

### 4. **Overestimating Practical Parallelism**
On real systems with $p$ processors:
- Communication overhead often dominates for small $n$
- Caches favor sequential access; parallel sorts may cache-thrash
- Break-even point depends heavily on architecture (GPUs vs. multi-core CPUs)

### 5. **Forgetting Stability**
Comparison sorts like merge sort are stable (preserve relative order of equal elements); quicksort is not. Application requirements may mandate stability for reproducibility or correctness.

## See Also

- [[Merge sort]] — The canonical divide-and-conquer comparison sort
- [[Scan]] — Parallel prefix operation with $O(\log n)$ depth, used in parallel sort implementation
- [[Quicksort]] — In-place comparison sort with $O(n \log n)$ average work but $\Omega(n)$ depth (sequential critical path)
- [[Radix sort]] — Non-comparison sort achieving $O(n + k)$ work on integer keys
- [[Bitonic sort]] — Specialized parallel comparison sort network with $O(\log^2 n)$ depth

## Sources

- Lecture excerpt on parallel primitives (scan, reduce, partition, filter, comparison sort)
- Section 2.2 & 2.3 context on concentration bounds and hashing (supporting analysis for randomized parallel algorithms)