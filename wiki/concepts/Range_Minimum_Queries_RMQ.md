# Range Minimum Queries (RMQ)

## Definition

A **Range Minimum Query (RMQ)** is a fundamental algorithmic problem: given an array $A$ of $n$ elements and a query range $[l, r]$ where $0 \le l \le r < n$, efficiently compute:

$$\text{RMQ}(l, r) = \min\{A[i] : l \le i \le r\}$$

The goal is to preprocess the array into a data structure that answers arbitrary queries as quickly as possible, balancing preprocessing time against query latency and memory overhead.

**Problem variants:**
- **Static RMQ:** Array is fixed after preprocessing
- **Dynamic RMQ:** Array supports updates between queries
- **Batched RMQ:** Process multiple queries simultaneously (relevant for GPU acceleration)

## Key Equations

### Query Complexity Trade-off

For a static array with preprocessing time $T_{\text{prep}}$ and query time $T_q$:

$$\text{Total Cost} = T_{\text{prep}} + Q \cdot T_q$$

where $Q$ is the number of queries.

### Sparse Table (Classical Solution)

Build a table $M[i][j]$ where $M[i][j] = \min(A[i], A[i+1], \ldots, A[i+2^j-1])$:

$$M[i][j] = \begin{cases} A[i] & \text{if } j = 0 \\ \min(M[i][j-1], M[i+2^{j-1}][j-1]) & \text{if } j > 0 \end{cases}$$

Then answer queries in $O(1)$ time via:

$$\text{RMQ}(l, r) = \min(M[l][k], M[r-2^k+1][k]) \quad \text{where } k = \lfloor \log_2(r - l + 1) \rfloor$$

- **Space:** $O(n \log n)$
- **Preprocessing:** $O(n \log n)$
- **Query:** $O(1)$

### Segment Tree (Dynamic Solution)

Build a binary tree with leaves as array elements; internal nodes store minimum of children:

$$\text{node}[i] = \min(\text{node}[2i], \text{node}[2i+1])$$

- **Space:** $O(n)$
- **Preprocessing:** $O(n)$
- **Query/Update:** $O(\log n)$

## Physical Intuition / Derivation

### Why RMQ Matters

Many problems reduce to RMQ: lowest common ancestor queries, string matching, geometric problems. Efficient RMQ solvers form critical building blocks in algorithm pipelines.

### The Sparse Table Insight

The Sparse Table works because **range-minimum queries possess optimal substructure:**

1. Any range $[l, r]$ can be covered by overlapping powers-of-two intervals
2. Since $\min$ is **idempotent** ($\min(x, x) = x$), overlapping intervals are safe:
   $$\min(M[l][k], M[r-2^k+1][k]) = \min(\text{left power-of-2}, \text{right power-of-2})$$
3. This avoids the $O(n^2)$ space of naive DP

### GPU Acceleration Trade-offs

The source material reveals a critical insight: **GPU performance depends on memory access patterns, not computational complexity.**

- **LCA-based methods:** Better cache locality for small arrays ($n < 2^{24}$), but uncoalesced random memory accesses cause L2 cache misses at scale
- **GPU-RMQ:** Coalesced memory access patterns enable graceful scaling to larger arrays; relatively **invariant to query range size** due to hierarchical traversal (queries traverse 3–6 layers uniformly)
- **Full GPU Scan:** Naïve per-query scan degrades catastrophically ($\sim 10$ms for large ranges), orders of magnitude slower

**Key observation:** On GPUs, *where you access memory matters more than how much computation you do.*

## Applications in Engineering

### 1. **Bioinformatics: Sequence Analysis**
- Identify conserved regions in DNA sequences (minimum alignment scores)
- Protein structure comparison via similarity windows

### 2. **Financial Engineering**
- Calculate minimum closing price over trading windows
- Efficient portfolio risk metrics (minimum loss scenarios)

### 3. **Database Systems**
- Query optimization over sorted indices
- Aggregate queries on time-series data

### 4. **Graphics & Geometry**
- Find nearest features in space-partitioning hierarchies
- Lowest common ancestor in spatial decomposition trees

### 5. **Real-time Signal Processing**
- GPU-accelerated minimum detection in streaming sensor data
- Batch processing of radar/seismic signals (as tested in the source material with $2^{26}$ queries)

### 6. **Network Routing**
- Bottleneck path queries (minimum bandwidth along routes)
- Encodes as RMQ on edge weights along tree paths

## Common Mistakes / Pitfalls

### 1. **Confusing Theoretical and Practical Complexity**
**Mistake:** Assuming $O(1)$ query time (Sparse Table) is always best.

**Reality:** Sparse Table's $O(n \log n)$ memory overhead and cache misses can underperform $O(\log n)$ Segment Trees on modern hardware. The profiling data shows LCA's theoretical elegance collapses at $n = 2^{24}$ due to uncoalesced L2 cache misses.

### 2. **Ignoring Access Patterns on Accelerators**
**Mistake:** Porting CPU-optimized algorithms directly to GPU without considering coalesced memory access.

**Reality:** GPU-RMQ's superiority (8–17× faster than alternatives on large arrays) stems entirely from **coalesced global-memory-to-L2 access**, not algorithmic cleverness.

### 3. **Overestimating Scan-Based Approaches**
**Mistake:** Implementing full range scans for large ranges on GPU, expecting parallelism to compensate.

**