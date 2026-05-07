# flipped indexing

## Definition

**Flipped indexing** is a GPU-optimized data structure design paradigm that inverts the traditional thread-to-operation mapping, instead assigning compute resources (warps/thread blocks) to data buckets, which then locate their responsible operations in a batch. Unlike conventional indexed structures (B-trees, LSM-trees) that assign each operation a thread and have it traverse an index layer, flipped indexing eliminates the index layer entirely and replaces multiple index traversals with a single binary search on the operation batch.

**Core principle**: Flip the mapping direction from `operation → thread → index traversal → bucket` to `bucket → thread(s) → batch binary search → operations`.

## Key Equations

For an ordered data structure with $n$ data elements partitioned into $b$ buckets:

**Traditional indexing work per operation:**
$$W_{\text{trad}} = O(\log_{\text{branching}} n) + O(\text{warp divergence})$$

**Flipped indexing work per operation:**
$$W_{\text{flip}} = O\left(\log_2 m + \frac{n}{b}\right)$$

where $m$ is the batch size. The reduction occurs because:
- Index traversal cost drops from logarithmic in data size to logarithmic in batch size
- Warp divergence is localized within buckets rather than spread across index levels
- Computation is reorganized as bucket-parallel rather than operation-parallel

**Throughput improvement metric:**
$$\text{Throughput per memory} = \frac{\text{ops/sec}}{\text{memory footprint (GB)}}$$

## Physical Intuition / Derivation

### Why Traditional GPU Indexing Struggles

Conventional GPU data structures (e.g., GPU B-trees) follow this pattern:
1. Assign each operation (query/insert/delete) to one GPU thread
2. Thread traverses index layer (multiple levels)
3. At each index level, different threads may take different branches → **warp divergence**
4. Threads eventually reach the appropriate bucket

**The problem on GPUs**: 
- Warp divergence causes idle cycles (32 threads execute in lockstep on typical architectures)
- Index layer traversals must be repeated for many operations accessing the same buckets
- Index maintenance during updates creates contention hotspots

### The Flipped Approach

FliX inverts this:
1. Assign each bucket (data partition) to a warp or thread block
2. Bucket's compute statically knows: "I own elements in range $[L, U)$"
3. Bucket uses **binary search on the operation batch** to find which operations target it
4. No index layer → no traversal, no divergence, no maintenance cost

**Why this works on GPUs**:
- **Locality**: A bucket processes all its operations in one kernel, maximizing data cache reuse
- **Divergence elimination**: Within a bucket, all threads follow the same binary search path
- **Simplicity**: Updates only modify the data layer; no index structure to maintain
- **Batch amortization**: The single binary search cost (log $m$) is amortized over all operations targeting that bucket

### Concrete Example

Consider 1000 elements in 10 buckets, batch of 100 operations:

| Approach | Index traversals | Cost per op |
|----------|------------------|------------|
| GPU B-tree (branching=8) | $\log_8(1000) \times 100$ ≈ 300 | ~3 |
| FliX | 1 per bucket (10 total) + local binary search | $\log_2(100)$ + scan ≈ 7–10 elements per bucket |

## Applications in Engineering

### 1. **Real-time Database Systems**
- GPU-accelerated in-memory databases (e.g., TPC-H analytical queries)
- Low-latency OLTP with dynamic inserts/updates
- Order preservation enables range queries on GPUs without hash table overhead

### 2. **High-Frequency Trading Platforms**
- Maintaining sorted order books with microsecond-level latency
- Updates and queries executed in batches to amortize compute
- Reduced memory footprint vs. ordered competitors improves cache efficiency

### 3. **Graph Processing & Machine Learning**
- Sorted adjacency lists for sparse matrix operations
- Graph neural network edge lookups with dynamic graph updates
- Beam search in sequence models (maintaining sorted hypotheses)

### 4. **Spatial Indexing (GPUs)**
- R-tree / quadtree-like structures for spatial queries
- Replacing multi-level tree traversals with batch-based bucket localization
- Applications: collision detection, geographic information systems

### 5. **Stream Processing**
- Window aggregations over sorted streams
- Windowed joins where both streams are dynamically updated
- Bucket structure naturally aligns with time windows or key ranges

## Common Mistakes / Pitfalls

### 1. **Assuming Flipped Indexing Solves All GPU Data Structure Problems**
- **Reality**: FliX is optimized for *batch-oriented* workloads. Single-operation latency may not match latency-optimized structures in low-concurrency scenarios.
- **Fix**: Profile your access pattern; if operations arrive sparsely, amortization benefits disappear.

### 2. **Overlooking Batch Size Dependency**
- **Reality**: The $O(\log_2 m)$ term depends critically on batch size. Small batches eliminate the advantage over indexed approaches.
- **Fix**: FliX shines with batch sizes $m \geq 32$–$128$. For single-query workloads, use traditional indexed structures.

### 3. **Misunderstanding Memory Layout**
- **Reality**: Flipped indexing still requires the data layer to support efficient random access. Poor bucket layout defeats the purpose.
- **Fix**: Ensure buckets are contiguous or well-localized in memory; use coalesced memory access patterns.

### 4. **Conflating Flipped Indexing with "No Structure"**
- **Reality**: FliX still imposes a logical bucket structure (range-based partitioning). This is *implicit indexing*, not unstructured storage.
- **Fix**: Understand that bucket boundaries are the "index" in FliX; they're just not traversed—they're searched around.

### 5. **