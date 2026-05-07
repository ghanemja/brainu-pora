# Warp Divergence

## Definition

**Warp divergence** occurs on GPU processors when threads within a single warp (a group of threads executed in lock-step on modern GPUs, typically 32 threads for NVIDIA architectures) follow different execution paths in a conditional branch. Since a warp executes all threads synchronously on the same instruction, divergent branches force the GPU to serialize execution of different code paths, causing threads taking one branch to stall while threads on another branch execute, then vice versa.

In the context of data structure operations on GPUs, warp divergence represents a significant performance bottleneck: when multiple threads in a warp traverse different paths through an index structure (e.g., a B-tree) based on different keys, the warp cannot maintain full utilization, and overall throughput degrades substantially.

## Key Equations

The performance penalty of warp divergence can be approximated as:

$$T_{\text{divergent}} = \sum_{i=1}^{n_{\text{paths}}} T_i$$

where $T_i$ is the execution time of path $i$ and $n_{\text{paths}}$ is the number of distinct execution paths taken by threads in the warp. In contrast, the ideal time for a unified path is:

$$T_{\text{ideal}} = \max_i T_i$$

The **divergence overhead** is thus:

$$\text{Overhead} = \frac{T_{\text{divergent}} - T_{\text{ideal}}}{T_{\text{ideal}}} = \frac{\sum_i T_i - \max_i T_i}{\max_i T_i}$$

For $n$ threads in a warp with $k$ divergent branches of roughly equal work, the worst-case slowdown approaches $k \times$ (compared to the unified execution case).

## Physical Intuition / Derivation

### Hardware Reality

Modern GPUs (NVIDIA, AMD) employ **SIMT** (Single-Instruction Multiple-Thread) execution: a single instruction stream is broadcast to all threads in a warp. Each thread has its own program counter and register state, but when a conditional branch is encountered, threads with different conditions cannot execute independently.

### Why Divergence Hurts

Consider a warp of 32 threads executing a B-tree search:

1. **Unified execution path** (no divergence): All 32 threads traverse the same nodes. One instruction fetch, one memory access pattern → maximum efficiency.

2. **Divergent execution path**: Suppose 16 threads branch left (to node A) and 16 branch right (to node B).
   - The GPU executes the path for node A with 16 threads active (other 16 stalled).
   - Then it executes the path for node B with the other 16 threads active (first 16 now stalled).
   - Result: $2 \times$ the instruction count for the divergent region.

### Why Index Layers Exacerbate This

Traditional GPU-resident B-trees and LSM-trees assign **one operation (thread or warp) per query/update**. Different operations follow different index paths:
- Operation 1 may search for key=10, descending left at internal nodes.
- Operation 2 may search for key=90, descending right at internal nodes.

When both are in the same warp, their divergent index traversals serialize, eliminating parallelism gains.

### The FliX Solution: Flipped Perspective

FliX inverts the mapping:
- **Traditional**: operation → thread/warp; warp traverses index layer → high divergence.
- **FliX**: bucket → warp; warp performs binary search on batch of operations → reduced divergence.

By assigning a warp to a single bucket/leaf and having all threads in the warp search a sorted batch for operations belonging to that bucket, the entire warp follows the **same execution path** through the batch (the binary search tree). This reduces divergence to only differences in data processing width, not structural traversal differences.

## Applications in Engineering

### GPU-Resident Data Structures
- **B-trees and LSM-trees**: Designers must recognize divergence as a primary bottleneck in GPU implementations. Index layer redesign (e.g., via FliX) can yield 6–8× performance gains.
- **Hash tables**: GPU hash tables avoid index traversal but forfeit range query support; FliX offers an alternative with ordered queries.

### Concurrent Systems
- When designing lock-free or atomic operations on GPU, ensuring warp-level coherence in conditional logic reduces synchronization overhead.
- Batch processing and bulk operations inherently reduce divergence compared to fine-grained per-operation execution.

### Database Query Processing
- GPU-accelerated database systems benefit from flipped indexing to reduce query latency and increase throughput per memory footprint.
- Insertion/deletion-heavy workloads see dramatic improvements (8× insertion throughput in some cases) when divergence from index maintenance is eliminated.

### Stream Processing
- GPU kernels processing streams of data can minimize divergence by ensuring all threads in a warp process data cohesively (e.g., processing consecutive elements of a sorted batch together).

## Common Mistakes / Pitfalls

### 1. **Ignoring Divergence in Algorithm Design**
Students often focus on asymptotic algorithm complexity without considering GPU execution model. A theoretically optimal algorithm (e.g., traditional B-tree) can be slower on GPU than a suboptimal algorithm (e.g., batch binary search) due to divergence.

### 2. **Assuming Uniform Workload Distribution**
Believing that "random" key distributions avoid divergence. In reality, non-uniform distributions can make divergence *worse* if some warps serialize on heavily-accessed branches while others idle.

### 3. **Conflating Warp Divergence with Thread Divergence**
Not all divergence is catastrophic. Divergence within a thread block *outside* warp boundaries (different warps taking different paths) is generally fine, as different warps execute independently. Only *intra-warp* divergence is severely penalized.

### 4. **Overlooking Divergence in Batch Processing**
Believing batch processing automatically eliminates divergence. It helps, but if batches are unordered or heterogeneous, threads within a warp may still diverge during per-element processing. Sorting batches (as FliX does) is crucial.

### 5. **Premature Optimization**
Optimizing for