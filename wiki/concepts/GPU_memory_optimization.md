# GPU Memory Optimization

## Definition

GPU memory optimization is the systematic design and implementation of data structures and algorithms that maximize the efficient use of GPU memory hierarchy while maintaining high computational throughput. It encompasses techniques for:

1. **Reducing memory footprint** — minimizing the amount of GPU global/local memory required to store data structures
2. **Improving cache utilization** — structuring data access patterns to maximize cache hits across GPU cache levels
3. **Balancing memory-compute tradeoffs** — choosing between precomputation/storage overhead versus runtime computation costs
4. **Exploiting memory hierarchy** — strategically placing data across registers, shared memory, L1/L2 caches, and global memory

Unlike CPU memory optimization, GPU optimization must account for massive parallelism, limited per-thread memory access patterns, and fundamentally different cache coherency models.

## Key Equations

### Memory Access Cost Model

The effective memory access time on a GPU can be approximated as:

$$T_{\text{access}} = P_{\text{hit}} \cdot T_{\text{cache}} + (1 - P_{\text{hit}}) \cdot T_{\text{global}}$$

where:
- $P_{\text{hit}}$ = probability of cache hit
- $T_{\text{cache}}$ = latency for cached access (typically 10-100 cycles)
- $T_{\text{global}}$ = latency for global memory access (typically 200-400+ cycles)

### Memory Efficiency Ratio

$$\eta_{\text{mem}} = \frac{\text{Useful Data Bytes Transferred}}{\text{Total Bytes Transferred}} \times 100\%$$

Higher ratios indicate better memory coalescing and reduced wasted bandwidth.

### Footprint Scaling Factor

For hierarchical data structures, the memory overhead factor is:

$$S_{\text{footprint}} = \frac{M_{\text{structure}}}{M_{\text{raw data}}} = \frac{\text{Total memory used}}{\text{Input size}}$$

Optimization targets $S_{\text{footprint}} \ll 1$ to handle larger datasets within GPU constraints.

## Physical Intuition / Derivation

### GPU Memory Hierarchy and Constraints

Modern GPUs (e.g., NVIDIA RTX 3090, RTX 6000 Pro) have:
- **Registers**: ~256 KB per thread block, extremely fast but limited
- **Shared Memory (L1)**: ~96 KB per thread block, low latency (~30 cycles)
- **L2 Cache**: Shared across all thread blocks (~5-6 MB)
- **Global Memory**: 24GB–96GB, high latency (~200+ cycles)

The **memory wall** problem is acute on GPUs: a single thread can issue memory requests much faster than they can be serviced. With thousands of threads, unoptimized access patterns cause:
- Bank conflicts in shared memory
- Cache misses in L1/L2
- Low global memory bandwidth utilization (~10-20% of peak if uncoalesced)

### Why Hierarchical Structures Help

The source material demonstrates this via **GPU-RMQ** (Range Minimum Query acceleration):

- **Naive approach**: Store all data in global memory, compute queries from scratch → high memory bandwidth, long latency
- **Hierarchical approach**: Precompute a multi-level summary structure (similar to a segment tree or sparse table)
  - Level 0: Original array (size $N$)
  - Level 1: Summaries of ranges of size $2^1$ (size $\approx N/2$)
  - Level 2: Summaries of ranges of size $2^2$ (size $\approx N/4$)
  - Total overhead: $N(1 + 1/2 + 1/4 + ...) \approx 2N$ bits

**Key insight**: Trading $2N$ total storage for $O(\log N)$ query time and better cache locality is often favorable when $N$ is large enough that the hierarchy fits in cache for common working sets.

### Example: Cache-Fit Threshold

From the source data:
- RTX 3090 (24GB): GPU-RMQ handles $2^{22}$ elements (16 MB), then performance drops
- RTX 6000 Pro (96GB): GPU-RMQ handles $2^{33}$ elements (64 GB), scaling **4× with memory**, not just 4× in raw storage

This super-linear scaling occurs because:
1. Larger hierarchies allow more of the access tree to remain in cache
2. Reduced memory stalls enable better thread occupancy and ILP
3. Fewer cache misses per query → higher sustained throughput

## Applications in Engineering

### 1. Bioinformatics & Sequence Analysis
- **Range minimum queries** on sequence alignment scores, phylogenetic distances
- **Lowest common ancestor (LCA) queries** for tree-based taxonomic classification
- Example: GPU-RMQ enables processing datasets 4× larger than prior methods, critical for metagenomics pipelines

### 2. Pattern Matching & Text Search
- Indexing large genomic/text databases where naive brute-force search is prohibitive
- Suffix arrays and suffix trees with optimized memory layouts
- Document retrieval systems operating on 100 GB+ datasets

### 3. Computer Graphics & Spatial Indexing
- **BVH (Bounding Volume Hierarchy)** acceleration structures for ray tracing
- Spatial queries (nearest neighbor, range search) on point clouds
- GPU-optimized tree traversal reducing cache misses and memory divergence

### 4. Machine Learning
- Graph neural network inference on large static graphs (minimize memory shuffling)
- Fast approximate nearest-neighbor search using hierarchical structures
- Sparse matrix operations where structure exploits locality

### 5. Database Systems
- GPU-accelerated database indexes (B-trees, hash tables adapted for GPU)
- Join operations and aggregations on large datasets
- The referenced GPU LSM and dynamic hash table structures

## Common Mistakes / Pitfalls

### 1. **Ignoring Memory Coalescing**
Threads in a warp reading non-contiguous memory locations cause serialized global memory stalls. 

**Mistake**: Designing access patterns without considering 32-thread warp coalescing requirements.

**Correction**: Ensure consecutive threads access consecutive (or predictable strided) memory locations.