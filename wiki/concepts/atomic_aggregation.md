# atomic aggregation

## Definition

**Atomic aggregation** is a GPU synchronization and data collection technique where multiple threads independently perform atomic operations (e.g., atomic add, atomic max) to combine their results into shared memory locations, rather than using hierarchical reduction or warp-level primitives.

In contrast to **warp aggregation** (which leverages warp-level intrinsics for fast intra-warp communication), atomic aggregation relies on hardware atomic instructions that guarantee read-modify-write atomicity across all threads in a thread block or grid. This approach trades efficiency for compatibility—it works in restricted execution environments (like NVIDIA OptiX kernels) where warp intrinsics are disabled, but incurs higher latency and memory contention overhead.

## Key Equations

For a reduction operation where $N$ threads each hold value $x_i$:

**Warp Aggregation (efficient, restricted availability):**
$$\text{result} = \sum_{i=0}^{N-1} x_i \quad \text{via warp shuffle/reduction ops}$$

**Atomic Aggregation (portable, higher overhead):**
$$\text{atomic\_add}(\text{output\_ptr}, x_i) \quad \text{for each thread } i$$

The **memory latency penalty** for atomic aggregation scales with contention:
$$T_{\text{atomic}} \approx T_{\text{base}} + C \cdot \rho$$

where $C$ is contention multiplier and $\rho$ is memory bus saturation ratio.

## Physical Intuition / Derivation

### Why Warp Intrinsics Are Unavailable

Modern GPU execution models (e.g., OptiX's work queuing) allow threads to migrate between processing cores during kernel execution. This breaks the **warp locality guarantee**—the assumption that 32 consecutive threads remain synchronized on the same core. Warp intrinsics (shuffles, reductions) depend critically on this locality. When the runtime cannot guarantee warp cohesion, warp intrinsics produce undefined behavior.

### Why Atomic Instructions Work Instead

Atomic operations are implemented at the **memory subsystem level** via hardware interlocks on cache lines or memory banks. They do not require threads to be physically co-located, only that they operate on the same memory location. Every atomic operation is guaranteed to:
- Read the current value
- Perform the operation
- Write the result back
- Appear indivisible to other threads

This comes at a cost: each atomic instruction stalls the requesting thread until the operation completes and the result returns—typically 200–800 GPU clock cycles vs. 1–2 cycles for warp shuffles.

### Performance Trade-off

Consider aggregating $N$ thread results:

| Method | Latency | Requirements | Portability |
|--------|---------|--------------|-------------|
| **Warp reduction** | $O(\log 32) \approx 5$ cycles | Warp locality | OptiX-incompatible |
| **Atomic aggregation** | $O(1)$ per op, but $\times$ latency + contention | None | OptiX-compatible |

When $N$ threads write atomically to a single address, serialization causes a "hot spot" that degrades throughput proportional to contention.

## Applications in Engineering

### 1. **Range Minimum Query (RMQ) Acceleration**
In the source material, GPU-RMQ must implement query result aggregation in OptiX kernels when using hardware ray tracing. Atomic aggregation replaces efficient warp reductions, causing **significant performance overhead** (visible in Figure 13 for array sizes $\geq 2^{30}$).

### 2. **Constrained GPU Execution Environments**
- **Ray tracing kernels** (OptiX, DXR) where thread scheduling is opaque
- **Dynamic parallelism** scenarios where child kernels have weak guarantees
- **Vendor runtime constraints** that restrict low-level synchronization primitives

### 3. **Histogram Computation**
Atomic increments to histogram bins when threads cannot be assumed to operate on disjoint bins:
```cuda
atomicAdd(&histogram[bin_id], 1);
```

### 4. **Global Reductions in Restricted Kernels**
Any pattern requiring all-threads-to-one aggregation when warp intrinsics are unavailable.

## Common Mistakes / Pitfalls

1. **Assuming atomic aggregation is "just a bit slower"**
   - The latency difference is not linear; contention causes superlinear degradation
   - For $\geq 2^{30}$ element arrays (Figure 13), overhead becomes 20–50%+ compared to warp-based approaches

2. **Ignoring the OptiX trade-off explicitly**
   - The source material shows that the overhead of switching to OptiX **is not compensated** by ray tracing speedups in this domain
   - Blindly using OptiX ray tracing for data structure queries is inefficient

3. **Hot-spotting a single aggregation address**
   - Writing all thread results to one atomic location serializes access
   - Consider local (block-level) aggregation followed by a single global atomic if possible

4. **Mixing atomic and non-atomic access patterns**
   - Race conditions if some threads use atomics and others use non-atomic reads/writes to the same location

5. **Forgetting memory footprint implications**
   - As noted for RTXRMQ (Figure 15), switching to alternate methods that require atomic aggregation may force different memory structures (e.g., BVH indices), increasing memory consumption and eventually exceeding GPU VRAM

## See Also

- [[warp aggregation]] – hierarchical reduction using warp shuffle and reduction intrinsics (efficient but locality-dependent)
- [[warp locality]] – the execution guarantee required for warp intrinsics
- [[atomic operations]] – hardware-level synchronization primitives
- [[range minimum query (RMQ)]] – the application domain in the source material
- [[OptiX]] – NVIDIA's ray tracing framework with restricted programming model

## Sources

- Kreis, L., Henneberg, J., Henkys, V., Schuhknecht, F., & Schmidt, B. "GPU-RMQ: Accelerated Range Minimum Queries." Section 4.3, Section 5.4 (OptiX integration and atomic aggregation), Section 5.5 (memory