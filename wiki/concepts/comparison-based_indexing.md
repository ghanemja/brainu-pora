# Comparison-Based Indexing

## Definition

**Comparison-based indexing** is a data structure strategy that uses comparative operations (e.g., binary search, key comparisons) to locate data elements within a dataset, rather than direct computation of element locations. In the context of GPU-accelerated concurrent data structures, comparison-based indexing refers to techniques that maintain sorted order and enable efficient lookups through comparison operations while minimizing index layer traversals.

Formally, a comparison-based index $I$ maps a query key $k$ to a data location through a sequence of comparison operations:
$$\text{locate}(k) = \begin{cases}
\text{left subtree} & \text{if } k < \text{pivot} \\
\text{right subtree} & \text{if } k > \text{pivot} \\
\text{current location} & \text{if } k = \text{pivot}
\end{cases}$$

This contrasts with **hash-based indexing**, which computes locations directly via $\text{locate}(k) = h(k) \mod m$, sacrificing ordering guarantees for $O(1)$ average-case access.

## Key Equations

### Traditional Index Traversal Cost
In conventional indexed structures (B-trees, LSM-trees), the cost of a single operation is:
$$C_{\text{trad}} = C_{\text{index traverse}} + C_{\text{data access}}$$

where index traversal dominates for deep trees: $C_{\text{index traverse}} = O(\log N)$ comparisons.

### FliX Flipped-Indexing Cost
By inverting the compute-to-data mapping:
$$C_{\text{FliX}} = C_{\text{batch binary search}} + C_{\text{data access}}$$

where batch binary search is performed once per bucket:
$$C_{\text{batch search}} = O(\log B) \text{ comparisons per bucket}$$

with $B$ = batch size (typically much smaller than dataset size $N$).

### Warp Divergence Reduction
Traditional approach creates divergence across threads $T$:
$$\text{Divergence}_{\text{trad}} \propto \text{tree depth} \times \text{branching variance}$$

FliX eliminates per-operation index traversal, reducing:
$$\text{Divergence}_{\text{FliX}} \propto O(1) \text{ per bucket}$$

## Physical Intuition / Derivation

### Traditional GPU Indexing Problem

In conventional GPU B-trees or LSM-trees:
1. Each thread/warp is assigned **one operation** (query, insert, delete)
2. Thread must **traverse the index layer** to find its target bucket
3. During traversal, different threads take different paths → **warp divergence**
4. Many threads wait while others continue → thread underutilization
5. Index maintenance under concurrent updates introduces contention

```
Traditional (operation → index → data):
Thread 1: Operation 1 → traverse tree → leaf 4
Thread 2: Operation 2 → traverse tree → leaf 7  [different path → divergence]
Thread 3: Operation 3 → traverse tree → leaf 4  [same leaf, redundant work]
```

### FliX Inversion Strategy

FliX **reverses the assignment**:
1. Each **bucket** (not operation) is assigned compute resources (warp)
2. Bucket performs **one binary search** on the entire batch to locate its operations
3. All threads in a warp follow the **same code path** → no divergence
4. Operations are naturally grouped by destination bucket

```
FliX (bucket → batch binary search → operations):
Bucket 4: binary search batch → find [Op1, Op3] → process together
Bucket 7: binary search batch → find [Op2]      → process together
[All threads in warp execute same instructions]
```

### Why This Works

**Key insight**: Index layer traversal is redundant when multiple operations target the same bucket.

- **Traditional**: $N$ operations × $\log D$ comparisons = $N \log D$ total comparisons
- **FliX**: $B$ buckets × $\log N_{\text{ops}}$ comparisons = $B \log N$ comparisons (where $B \ll N$)
- **Batch size effect**: If batch size $B \approx 1000$, savings are immediate for $N > 1000$

## Applications in Engineering

### 1. **GPU Database Systems**
- **Range queries**: Maintain sort order while enabling efficient $\text{range}(k_{\min}, k_{\max})$ lookups
- **Ordered aggregations**: GROUP BY, ORDER BY operations benefit from ordered index
- **Interactive analytics**: 6.5× query latency reduction directly improves dashboard responsiveness

### 2. **Real-Time Data Warehouses**
- **Write-heavy workloads**: 8× insertion throughput improvement enables streaming ingest
- **Dynamic memory reclamation**: Eliminates index layer overhead, simplifying garbage collection
- **LSM alternative**: Outperforms LSM-trees while maintaining ordered access

### 3. **Graph Processing on GPUs**
- **Adjacency index**: Comparison-based ordering enables efficient edge list traversal
- **Degree-ordered access**: Comparison predicates optimize for power-law graph properties

### 4. **Scientific Computing**
- **Particle simulations**: Spatial indexing via comparison-based sorting
- **Sparse matrix operations**: Maintaining COO (coordinate) format ordering

### 5. **Key-Value Stores**
- **Hybrid workloads**: Competes with hash tables on insertion, exceeds on range queries
- **Memory efficiency**: 4× better throughput-per-byte than ordered competitors

## Common Mistakes / Pitfalls

### 1. **Assuming Hash Tables Are Always Faster**
- **Error**: "Hash indexing is $O(1)$, so comparison-based is worse"
- **Reality**: On GPUs, hash collisions cause thread divergence; comparison-based binary search on batches has better warp efficiency
- **Lesson**: Asymptotic analysis ignores GPU architectural constraints (warp execution, memory coalescing)

### 2. **Neglecting Warp Divergence Costs**
- **Error**: Counting only "comparisons" without considering divergence