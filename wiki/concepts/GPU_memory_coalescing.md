# GPU Memory Coalescing

## Definition

**GPU memory coalescing** is an optimization technique where multiple threads in a GPU warp access consecutive memory locations in a single memory transaction, rather than issuing separate transactions for each thread. When threads within a warp (typically 32 threads on NVIDIA GPUs) access memory addresses that fall within the same cache line (typically 128 bytes), the GPU hardware combines these requests into one or a few coalesced transactions, dramatically improving memory bandwidth utilization and reducing latency.

A **coalesced access pattern** occurs when:
- Thread $i$ in a warp accesses memory address $\text{base} + i \cdot \text{stride}$ (unit stride)
- All accessed addresses fit within one or more consecutive cache lines
- Threads participate in a contiguous pattern without gaps or irregular jumps

Conversely, **uncoalesced accesses** (scattered or random memory patterns) force the GPU to issue one memory transaction per thread or per small group of threads, wasting bandwidth and increasing memory latency penalties.

## Key Equations

**Memory bandwidth utilization:**
$$\text{Efficiency} = \frac{\text{Useful bytes transferred}}{\text{Total bytes transferred}} = \frac{\text{Active threads} \times \text{bytes per access}}{\text{Cache line size} \times \text{Transactions issued}}$$

For optimal coalescing (unit stride, all threads active):
$$\text{Efficiency}_{\text{max}} \approx 1.0 \quad \text{(100\%)}$$

For random/uncoalesced access:
$$\text{Efficiency}_{\text{random}} \approx \frac{1}{32} \quad \text{(3.1\% on 32-thread warp)}$$

**Stall cycles due to memory latency:**
$$\text{Stall cycles} = \text{Memory latency} \times \text{(1 - Cache hit rate)} \times \text{(1 - Instruction-level parallelism coverage)}$$

## Physical Intuition / Derivation

### Why Coalescing Matters

Modern GPUs are designed with a memory hierarchy optimized for **bandwidth**, not latency. A single memory request to global memory incurs ~200-400 cycles of latency. The GPU hides this latency by:

1. **Executing other warps** while one warp waits for memory
2. **Batching memory requests** into larger transactions that amortize the latency cost

When 32 threads each make independent (uncoalesced) requests to scattered addresses:
- The memory controller must issue 32 separate transactions (or at least many more than necessary)
- Each transaction traverses the memory bus independently
- The total time is proportional to the number of transactions, not the amount of data
- Bandwidth is severely underutilized

When those same 32 threads access consecutive addresses (coalesced):
- All 32 addresses fit within 1–4 cache lines (128 bytes each on modern GPUs)
- A single or few transactions fetch all needed data
- All threads obtain their values in parallel
- Bandwidth utilization approaches 100%

### Example: Impact on Performance

From the source material on Range Minimum Query (RMQ) algorithms:

> "LCA performs a small number of random, uncoalesced accesses for processing each query, which results in a **memory bottleneck** as soon as the working set no longer fits into the GPU's L2 cache."

When $n = 2^{24}$, the LCA algorithm's working set exceeds the L2 cache (typically ~12–48 MB), forcing all accesses to global memory. Without coalescing:
- Each query triggers multiple cache misses
- Each miss requires a separate, uncoalesced global memory transaction
- Performance drops **~8×** compared to GPU-RMQ, which maintains coalesced accesses
- The GPU cannot hide latency effectively; execution stalls waiting for data

In contrast, GPU-RMQ maintains coalesced access patterns:
> "The performance of GPU-RMQ decreases gracefully with an increase in array size, showing the best query performance for larger array sizes."

This is because GPU-RMQ's hierarchical structure ensures that queries access memory in localized, coalesced patterns regardless of array size.

## Applications in Engineering

### 1. **High-Performance Computing (HPC)**
   - Dense linear algebra (matrix multiplication, factorization)
   - Ensure memory-heavy kernels use coalesced patterns for matrix row/column access
   - Achieves 10–100× speedups over naive implementations

### 2. **Graphics Rendering**
   - Texture fetches, depth buffer reads, and framebuffer writes
   - GPU rasterizers are designed to exploit coalescing in 2D tile-based access patterns

### 3. **Numerical Simulation**
   - Stencil computations (finite difference, finite element)
   - Structure loops to access grid points in coalesced order (row-major vs. column-major layout decisions)

### 4. **Data Structure Design**
   - Query algorithms (RMQ, segment trees, range queries)
   - Choose data layouts and traversal orders that maintain spatial locality
   - Trade preprocessing complexity for coalesced query performance (as GPU-RMQ does)

### 5. **Machine Learning Inference**
   - Batched operations on neural network layers
   - Arrange weight matrices and activations in memory to enable coalesced tensor operations
   - Critical for achieving stated throughput on data-parallel GPUs

### 6. **Database Queries & Analytics**
   - Columnar storage formats naturally coalesce reads when multiple threads process consecutive column entries
   - Leads to superior performance vs. row-oriented storage on GPUs

## Common Mistakes / Pitfalls

### 1. **Assuming Cache Size is Sufficient**
   **Mistake:** "My algorithm fits in L2 cache, so coalescing doesn't matter."
   
   **Reality:** Once the working set exceeds cache, every miss becomes an expensive global memory round-trip. Without coalescing, each thread's miss becomes a separate transaction. Even small cache sizes mask uncoalesced access until data volume grows. The RMQ study shows this clearly: LCA's performance collapses at $n = 2^{24}$ despite working perfectly at smaller sizes.

### 2. **Forgetting Thread Index Mapping**
   **Mistake:** Assigning thread $i$