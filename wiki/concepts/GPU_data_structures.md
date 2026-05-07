# GPU Data Structures

## Definition

GPU data structures are specialized data organization schemes designed to exploit the massively parallel architecture of graphics processing units (GPUs) for efficient querying and computation. Unlike CPU data structures that optimize for sequential access and cache locality, GPU data structures prioritize:

- **Massive parallelism**: Leveraging thousands of concurrent threads
- **Memory bandwidth utilization**: Balancing global memory, shared memory, and register access
- **Computational density**: Maximizing operations per memory transaction
- **Hardware acceleration**: Exploiting specialized cores (CUDA cores, tensor cores, ray tracing cores)

A canonical example is the **hierarchical range minimum query (RMQ) structure**, which organizes data into levels of progressively coarser summaries, enabling both sequential and parallel query processing.

## Key Equations

For a hierarchical RMQ structure over array $X$ of size $n$:

**Level construction:**
$$L_i[j] = \min(L_{i-1}[k \cdot j], L_{i-1}[k \cdot j + 1], \ldots, L_{i-1}[k \cdot j + k - 1])$$

where $L_0 = X$ (original array), $k$ is the fanout, and $L_i$ represents the $i$-th level of the hierarchy.

**Memory complexity:**
$$M = n \left(1 + \frac{1}{k} + \frac{1}{k^2} + \cdots \right) = \frac{nk}{k-1}$$

**Query time (parallel scan):**
$$T_{\text{query}} = O\left(\log_k n\right) \text{ sequential levels, processed with } O\left(\frac{\text{range width}}{p}\right) \text{ parallel work}$$

where $p$ is the number of parallel threads available.

## Physical Intuition / Derivation

### Why GPU Data Structures Differ from CPU Structures

CPUs excel at irregular access patterns and complex branching. A balanced binary search tree fits this model—it has $O(\log n)$ depth, minimal extra space, and works well with caching.

GPUs, conversely, suffer when:
- Threads diverge (some follow different code paths)
- Memory access is irregular (cache misses are expensive without prefetching)
- Synchronization is required (stalls all threads in a warp)

GPUs thrive when:
- All threads do the same operation on different data (**SIMD paradigm**)
- Memory access is coalesced (consecutive threads access consecutive memory)
- Computation is regular and predictable

### Hierarchical RMQ Construction

The key insight is to replace binary trees with **wide, shallow hierarchies**:

1. **Level 0**: Original array $X$ of size $n$
2. **Level 1**: Array of minima over contiguous blocks of size $k$ → size $n/k$
3. **Level 2**: Minima of blocks at Level 1 → size $n/k^2$
4. **...Level $h$**: Single element (global minimum)

**Parallel construction:** Each GPU thread independently computes one summary value:
$$L_i[\text{thread\_id}] = \min_{j=0}^{k-1} L_{i-1}[\text{thread\_id} \cdot k + j]$$

This is perfectly parallel with no data dependencies within a level.

### Query Processing

For a range query $\text{RMQ}(X, \ell, r)$ (find minimum in $X[\ell \ldots r]$):

1. Start at the coarsest level $h$ containing the range
2. Scan relevant summaries in that level
3. Descend to finer levels as needed, using lazy evaluation

**Example with $k=4$:**
- Query range $[5, 23]$ spans multiple blocks at Level 1
- Level 1 computes: $\min(L_0[4..7], L_0[8..11], \ldots, L_0[20..23])$
- Process boundaries at Level 0 if they don't align with block boundaries

## Applications in Engineering

### 1. Biological Sequence Analysis
Range minimum queries answer **lowest common ancestor (LCA)** queries on suffix trees and phylogenetic trees. GPU acceleration enables real-time analysis of gigabase-scale genomic datasets.

**Use case:** Finding shared ancestry between sequences in massive DNA databases.

### 2. String Processing & Document Retrieval
RMQs compute **longest common extensions (LCE)** between arbitrary suffixes without full suffix array traversal. Essential for:
- Full-text search in terabyte-scale corpora
- Duplicate detection and compression
- DNA read alignment

### 3. Web Search & Information Retrieval
Range queries on ranked lists enable:
- Distance calculations between query results
- Relevance ranking over ranges of documents
- Real-time aggregation statistics

### 4. Database Query Optimization
Hierarchical structures support:
- **Window aggregate queries**: SUM, MIN, MAX over ranges
- **Range cardinality estimation**: Approximate query planning
- **Bitmap index operations**: Fast range filtering

### 5. Graphics & Ray Tracing
Modern approach: Express RMQ as ray-triangle intersection problem:
- Organize minima at different granularities as hierarchical triangles in 3D space
- Fire rays (queries) into the scene
- Hardware-accelerated ray tracing cores solve RMQ instantly

## Common Mistakes / Pitfalls

### 1. Ignoring Memory Coalescing
**Mistake:** Accessing global memory in a strided pattern (thread $i$ reads from position $i \cdot d$).

**Impact:** Memory bandwidth drops by 10–100×. Global memory accesses are **only fast if consecutive threads access consecutive addresses**.

**Fix:** Restructure data layout and access patterns to ensure coalesced reads.

### 2. Choosing Wrong Fanout $k$
**Mistake:** Using $k=2$ (binary hierarchy) because it's familiar from CPUs.

**Impact:** Creates $O(\log_2 n)$ levels; each level requires level-to-level synchronization, killing throughput.

**Solution:** Use $k = 16$ to $k = 256$ (matching warp size or thread block size). Trade space overhead for shallower hierarchies