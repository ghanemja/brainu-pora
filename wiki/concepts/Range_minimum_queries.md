# Range Minimum Queries

## Definition

A **range minimum query (RMQ)** on an array $X = [X[0], X[1], \ldots, X[n-1]]$ answers the following problem:

> Given indices $i$ and $j$ with $0 \leq i \leq j < n$, find $\min(X[i], X[i+1], \ldots, X[j])$.

In other words, RMQ returns the minimum value in any contiguous subarray of $X$. The query is characterized by a pair of indices $(i, j)$ representing the query range, and the output is both the minimum value and typically its position.

**Variants:**
- **Static RMQ**: Array $X$ is fixed; only queries are performed
- **Dynamic RMQ**: Array supports insertions, deletions, or updates between queries
- **Batched RMQ**: Multiple queries answered simultaneously

## Key Equations

For a query range $[i, j]$, the minimum value is defined as:

$$\text{RMQ}(i, j) = \min_{k=i}^{j} X[k]$$

**Sparse Table Approach** (classical preprocessing-based solution):
Precompute a table $M[i][k]$ where:

$$M[i][k] = \min(X[i], X[i+1], \ldots, X[i+2^k-1])$$

for all positions $i$ and all power-of-two lengths $k = 0, 1, \ldots, \log_2 n$.

Then any query can be answered by combining two overlapping ranges:

$$\text{RMQ}(i, j) = \min(M[i][k], M[j-2^k+1][k])$$

where $k = \lfloor \log_2(j - i + 1) \rfloor$.

**Preprocessing complexity**: $O(n \log n)$ time and space  
**Query complexity**: $O(1)$ time

## Physical Intuition / Derivation

### Why RMQs Matter

Consider a practical scenario: you have a time series of temperature measurements and want to quickly find the lowest temperature in any time window without scanning all values. Naive approach requires $O(j - i)$ time per query. For thousands of queries on large arrays, this becomes prohibitive.

The key insight is **precomputation through hierarchy**: instead of storing individual elements, we store aggregated minima at different granularities.

### Building the Sparse Table Intuitively

1. **Level 0** ($k=0$): Store minimum of each single element (identity)
2. **Level 1** ($k=1$): Store minimum of each pair of consecutive elements
3. **Level 2** ($k=2$): Store minimum of each group of 4 elements
4. Continue doubling the range size up to $\log_2 n$ levels

When querying range $[i, j]$:
- Find the largest power of 2 that fits in your range: $2^k = 2^{\lfloor \log_2(j-i+1) \rfloor}$
- The minimum is either in the first block starting at $i$ (covered by $M[i][k]$) or in the last block ending at $j$ (covered by $M[j-2^k+1][k]$)
- These blocks may overlap, but min operation is idempotent: $\min(a, a) = a$

### Modern GPU Acceleration

Recent approaches exploit GPU parallelism:

**Hierarchical Summarization** (GPU-RMQ):
- Organize array into blocks of size $b$ (e.g., $b = 1024$)
- Level 0: Original array
- Level 1: Minimum of each $b$-element block
- Level 2: Minimum of each $b$ blocks from Level 1
- Continue until single element at apex

For query $[i, j]$:
1. Find which blocks span the range
2. Process relevant hierarchy levels in parallel
3. Combine results via parallel reduction

**Complexity with hierarchy depth $d = \log_b n$**:
- Space: $O(n(1 + 1/b + 1/b^2 + \cdots)) = O(n \cdot \frac{b}{b-1})$ ≈ linear
- Query: $O(d)$ levels to traverse, each processed in $O(b/\text{parallelism})$ time

## Applications in Engineering

### 1. **Bioinformatics & String Processing**
- **Lowest Common Ancestor (LCA) queries**: In phylogenetic trees, finding the most recent common ancestor of two sequences requires RMQ on depth arrays
- **Longest Common Extension (LCE)**: Computing suffix array LCP ranges uses RMQ to find shared prefixes in linear time

### 2. **Database & Information Retrieval**
- **Document ranking**: Finding minimum relevance scores in candidate document ranges
- **Time-series databases**: Querying minimum values in temperature, stock price, or sensor data windows
- **Web search**: Aggregating statistics across index partitions

### 3. **Computational Geometry**
- **2D range searching**: Orthogonal range minimum queries on 2D grids
- **Visibility problems**: RMQ on height maps determines line-of-sight obstructions

### 4. **Network Algorithms**
- **Minimum bandwidth path queries**: Finding bottleneck edge weights in graph paths
- **Routing optimization**: Determining minimum latency segments in network paths

### 5. **Computer Vision & Ray Tracing**
- **Hierarchical acceleration structures**: Modern GPUs use ray tracing hardware (as in GPU-RMQ) to answer spatial queries by representing range minima as triangle geometry

## Common Mistakes / Pitfalls

### 1. **Confusing RMQ with Sorting**
RMQ does *not* sort the array—it respects positions. The minimum value in $[i, j]$ must come from that specific contiguous range, not from the globally sorted order.

### 2. **Ignoring Memory Overhead**
Naive implementations store entire sparse tables with $O(n \log n)$ entries. For $n = 2^{29}$ elements, this easily exceeds