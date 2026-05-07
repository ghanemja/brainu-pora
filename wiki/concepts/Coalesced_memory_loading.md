# Coalesced Memory Loading

## Definition

**Coalesced memory loading** is a GPU optimization technique that arranges memory access patterns so that multiple threads in a warp or thread block retrieve consecutive data elements from global memory in a single, efficient transaction. Rather than allowing each thread to independently fetch arbitrary memory locations, coalesced loading ensures that threads access memory in sequential, aligned patterns that map directly to the GPU's memory bus width, minimizing the number of memory transactions required.

In the context of GPU-RMQ (Range Minimum Query acceleration), coalesced loading is applied during the scanning phase of the hierarchy to fetch range minimum summaries and intermediate query results with maximal memory bandwidth utilization.

## Key Equations

The **memory transaction efficiency** can be characterized as:

$$\text{Efficiency} = \frac{\text{Useful bytes transferred}}{\text{Total bytes transferred in all transactions}}$$

For perfectly coalesced access by a warp of $w$ threads accessing $b$-byte elements from consecutive addresses:

$$\text{Transactions}_{\text{coalesced}} = \frac{w \cdot b}{B_{\text{bus}}}$$

where $B_{\text{bus}}$ is the memory bus width (typically 128 bytes for modern GPUs).

By contrast, uncoalesced random access requiring one transaction per thread yields:

$$\text{Transactions}_{\text{uncoalesced}} = w$$

The **speedup factor** from coalescing is thus bounded by:

$$\text{Speedup} \leq \frac{B_{\text{bus}}}{b}$$

## Physical Intuition / Derivation

### Memory Hierarchy and Bandwidth Constraints

Modern GPUs transfer data from global memory in fixed-size transactions (cache lines). A typical transaction retrieves 128 bytes regardless of whether only 4 bytes are actually needed. This design reflects the principle that **data locality matters**—nearby memory locations are cheaply fetched together.

### Warp-Level Execution Model

GPU threads are organized into **warps** (groups of 32 threads on NVIDIA hardware) that execute in lockstep. When a warp issues a load instruction:

1. **If coalesced**: All 32 threads request consecutive 4-byte values (128 bytes total = one transaction)
2. **If scattered**: Threads request random locations, each potentially requiring a separate transaction

The GPU hardware detects coalesced patterns and consolidates them; scattered patterns cannot be consolidated, wasting bandwidth.

### Application to RMQ Hierarchy Scanning

In GPU-RMQ, the hierarchy levels contain range minimum summaries stored as arrays. When multiple query threads scan the same hierarchy level:

- **Coalesced pattern**: Thread $i$ reads element $i$ from the level
- **Uncoalesced pattern**: Threads read query-specific offsets with no spatial locality

GPU-RMQ achieves coalescing by organizing computation so threads naturally map to sequential array indices, avoiding bank conflicts and memory divergence.

## Applications in Engineering

### 1. **GPU-Accelerated Database Queries**
In GPU-RMQ systems, coalesced loading enables efficient scanning of precomputed range summary hierarchies during RMQ answering, achieving up to **8–17× speedup** over CPU baselines by fully saturating memory bandwidth.

### 2. **Parallel Scan and Reduction Operations**
Work-efficient parallel scan algorithms (Blelloch-style) explicitly structure computation to respect memory coalescence, improving throughput for prefix sums, cumulative operations, and histogram computations.

### 3. **Scientific Computing and Stencil Kernels**
Finite difference and stencil-based solvers (e.g., PDEs on grids) arrange thread blocks to access neighboring grid cells in coalesced patterns, maximizing cache utilization and bandwidth.

### 4. **Image and Signal Processing**
Convolution and filtering kernels on GPUs organize thread assignments so adjacent threads process spatially adjacent pixels/samples, naturally achieving coalesced memory access.

### 5. **Machine Learning Inference**
Batched matrix operations and tensor contractions on GPUs use coalesced memory patterns to efficiently load weight matrices and activation tensors, critical for real-time inference.

## Common Mistakes / Pitfalls

### 1. **Assuming Row-Major vs. Column-Major Automatically Coalesces**
Students often think data layout alone ensures coalescence. **Reality**: Thread assignment to data elements also matters. A row-major matrix accessed column-wise by consecutive threads is *uncoalesced* despite "good" layout.

**Fix**: Transpose data or reorder thread indices to match memory layout.

### 2. **Ignoring Bank Conflicts Alongside Coalescence**
Coalesced *global* memory access can still suffer from *shared memory bank conflicts*, a separate issue. Checking only one level of the hierarchy is insufficient.

**Fix**: Analyze both global and shared memory access patterns independently.

### 3. **Over-Optimizing for One Architecture**
Coalescence patterns optimal for compute capability 7.0 (Volta, 128-byte transactions) may differ for capability 8.0 (Ampere). Hard-coding assumptions breaks portability.

**Fix**: Use GPU abstraction layers or query device properties at runtime (e.g., `cudaDeviceGetAttribute`).

### 4. **Misunderstanding Vectorized Loads**
GPU-RMQ mentions **vector loading** (e.g., `float4`) alongside coalescence. Students conflate these: vector loads help the compiler, but don't *guarantee* coalescence if the base address isn't aligned or threads access non-consecutive elements.

**Fix**: Vector loads only optimize when underlying memory access is already coalesced.

### 5. **Neglecting Warp Divergence with Coalesced Access**
Control flow divergence can break coalescence indirectly: if some threads take different code paths, they may skip load instructions, causing warp-level serialization and partial transaction utilization.

**Fix**: Keep control flow uniform within warps during memory-intensive phases.

## See Also

- [[Warp-Level Parallelism]] – Foundation for understanding thread grouping and coalesced access
- [[GPU Memory Hierarchy]] – Detailed structure of global, shared, and cache memory enabling coalescence optimization
- [[Range Minimum Query (RMQ)]] – Application domain motivating these optimizations
- [[Memory Bank Conflicts]] – Related shared memory optimization orthogonal to global coalescence
- [[Occupancy and Throughput]] – Higher-level