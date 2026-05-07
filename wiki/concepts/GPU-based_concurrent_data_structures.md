# GPU-based Concurrent Data Structures

## Definition

GPU-based concurrent data structures (CDSs) are indexing and storage systems designed to operate on fully GPU-resident data, supporting both high-throughput read-only queries and dynamic updates (insertions, deletions, modifications) with minimal synchronization overhead. These structures exploit GPU parallelism (thousands of threads organized in warps and blocks) while managing the unique computational constraints of GPU architectures: limited global synchronization, warp divergence penalties, and memory hierarchy differences from CPUs.

**Key distinguishing features:**
- **Ordered vs. Unordered**: Ordered CDSs (B-trees, LSM-trees) maintain index layers for range/successor queries; unordered structures (hash tables) sacrifice order for update efficiency
- **Fully GPU-resident**: Data never transfers to/from host; all operations execute on-device
- **Dynamic**: Support insertions, deletions, and updates, not just read-only workloads

## Key Equations

### Performance Metrics

**Query latency** (end-to-end):
$$L_q = L_{\text{index}} + L_{\text{data}} + L_{\text{sync}}$$

where $L_{\text{index}}$ is index traversal latency, $L_{\text{data}}$ is bucket/leaf access latency, and $L_{\text{sync}}$ is synchronization overhead.

**Throughput per memory footprint**:
$$\tau = \frac{\text{Operations per second}}{\text{Memory used (bytes)}}$$

### Warp Efficiency

When assigning operations to threads, warp divergence cost is:
$$\Delta L = \sum_{i=1}^{n_{\text{branches}}} \frac{\text{threads taking branch } i}{32} \cdot \text{branch latency}_i$$

High divergence occurs when threads in the same warp (32 threads on NVIDIA) follow different code paths, serializing execution.

### FliX Indexing Paradigm

**Traditional (operation-centric)**: Assign operation $op_i$ to thread $t_i$
$$t_i \gets \text{traverse}(\text{index}, \text{key}_i) \rightarrow \text{bucket}_j$$

**FliX (bucket-centric)**: Assign bucket $b_j$ to warp $w_j$
$$w_j \gets \text{binsearch}(\text{batch}, \text{range}_j) \rightarrow \{op_1, \ldots, op_m\}$$

## Physical Intuition / Derivation

### Why Traditional GPU CDSs Struggle with Updates

1. **Index Traversal Bottleneck**: In a B-tree or LSM-tree, each operation independently traverses an index layer (root → internal nodes → leaf). On a GPU, different threads may traverse different paths due to different keys, causing **warp divergence**—some threads stall while others execute, wasting compute.

2. **Contention at Popular Nodes**: Multiple threads accessing the same index node (especially the root) create lock contention and serialization in the memory system.

3. **Redundant Work**: Many operations traverse identical or overlapping index paths, but each thread independently repeats this work.

### The Flipped Indexing Insight (FliX)

Instead of threads chasing keys through an index, **flip the responsibility**: 
- Each **bucket** (data container) independently determines which **operations in the batch** belong to it.
- Replace hundreds of redundant index traversals with a **single binary search per bucket** on a sorted batch.

**Why this works:**
- **Reduced warp divergence**: All threads in a bucket's warp follow the same control flow (binary search logic), minimizing divergence.
- **Eliminated index maintenance**: No need to update B-tree nodes or LSM levels during insertions—data is simply reorganized in buckets.
- **Better memory locality**: Threads working on the same bucket access nearby data, improving cache hit rates.
- **Scalability**: As batch size grows, the amortized cost per operation drops.

### Mathematical Perspective

Consider a batch of $n$ operations and $m$ buckets:

**Traditional approach**: $O(m \cdot n \cdot h)$ thread-steps, where $h$ is index height and many operations traverse overlapping paths.

**FliX approach**: $O(m \cdot \log n)$ for binary searches + $O(n)$ for bucket processing = $O(n + m \log n)$ net work, with **zero warp divergence** if all threads execute identical binary search logic.

## Applications in Engineering

### 1. **Real-time Database Queries on Edge GPUs**
Mobile and edge devices with GPUs (NVIDIA Jetson, mobile SoCs) can answer sorted range queries on locally cached data without CPU involvement. Example: time-series data from IoT sensors.

### 2. **High-frequency Trading Systems**
Maintain order books on GPU. FliX's low latency and update throughput make it suitable for microsecond-scale trade matching with dynamic price levels.

### 3. **Genomic Data Analysis**
Index and query millions of genomic sequences. Range queries on genome coordinates are common; FliX's ordered nature + speed enables fast variant filtering.

### 4. **Graphics & Game Engines**
Spatial indexing of game objects (BSP trees, acceleration structures) must support rapid insertions (new objects) and deletions (destroyed objects) while handling ray-casting queries. FliX's dynamic updates and order-preservation suit spatial partitioning.

### 5. **Numerical Simulations (N-body, CFD)**
Particle or grid-based simulations on GPU require frequent neighbor lookups and data reorganization. FliX enables low-overhead dynamic spatial indexing.

### 6. **Machine Learning Feature Stores**
GPUs serving ML models need to rapidly fetch sorted feature vectors. Batch processing (natural in ML) aligns with FliX's batch-centric design.

## Common Mistakes / Pitfalls

### 1. **Assuming GPU CDSs match CPU B-tree performance**
GPUs excel at **bulk parallelism**, not single-threaded sequential access. A GPU B-tree may underperform a CPU B-tree for single-operation queries due to kernel launch overhead. FliX is designed for **batch workloads**.

### 2. **Ignoring warp