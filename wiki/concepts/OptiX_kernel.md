# OptiX kernel

## Definition

An **OptiX kernel** is a GPU compute shader executed within NVIDIA's OptiX ray tracing framework. OptiX kernels enable hardware-accelerated ray tracing on NVIDIA GPUs by allowing programmers to define custom ray generation, intersection, and shading programs that run on specialized ray tracing hardware (e.g., RT cores on RTX GPUs).

However, OptiX kernels impose important constraints: they do **not guarantee warp locality**. The OptiX programming model may dynamically move threads to different processing cores during execution, breaking the standard CUDA warp execution model. Consequently, **warp-level intrinsics and warp synchronization primitives are prohibited** in OptiX kernels.

## Key Equations

No formal equations apply directly to OptiX kernel definition, but the performance trade-off can be characterized:

$$\text{Total Time}_{\text{OptiX}} = \text{Overhead}_{\text{OptiX}} + \text{Time}_{\text{algorithm}}$$

where $\text{Overhead}_{\text{OptiX}}$ represents the fixed cost of executing within the OptiX framework (context switching, thread scheduling, warp breakdown).

## Physical Intuition / Derivation

### Why OptiX Breaks Warp Locality

CUDA's standard execution model guarantees that threads in a warp (32 threads on modern NVIDIA GPUs) execute in **lock-step synchrony** on the same physical processing cores. This enables:

- **Warp-level reductions**: Fast prefix scans and aggregations using `__shfl_down()`, `__shfl_xor()`, etc.
- **Efficient memory access patterns**: Coalesced reads/writes when threads access contiguous memory
- **Implicit synchronization**: No explicit barriers needed within a warp

OptiX's ray tracing model, by contrast, requires **dynamic thread scheduling** because rays diverge chaotically through space. When a ray hits an object or misses, the OptiX runtime may reassign the thread to a different physical core to balance load across the ray tracing hardware (BVH traversal, intersection testing, etc.). This breaks the warp-lockstep guarantee.

### The Rewriting Requirement

When OptiX kernels cannot use warp intrinsics, algorithms must be rewritten to use:
- **Atomic operations** instead of warp reductions (slower, requires global memory synchronization)
- **Global synchronization barriers** instead of warp-level implicit sync
- **Global memory aggregation** instead of shared memory within warps

This typically causes **10–20% performance degradation** or more, depending on algorithm structure.

## Applications in Engineering

### GPU-Accelerated Range Minimum Queries (RMQ)

The source material discusses GPU-RMQ, a data structure for efficient range queries on arrays:

- **Standard GPU-RMQ**: Uses WLQ (warp-level queuing) with warp reductions → fast
- **OptiX variant (GPU-RMQ w/o warp intrinsics in OptiX)**: Must rewrite to atomic aggregation → slower
- **Ray-tracing hybrid**: Attempts to accelerate the topmost layer of the RMQ tree using hardware ray tracing, but the OptiX overhead outweighs the ray-tracing speedup

**Key finding**: For array sizes $\geq 2^{30}$, the OptiX framework overhead alone is substantial. When ray tracing is added (GPU-RMQ w/o warp intrinsics in OptiX w/ RT), no net speedup is achieved compared to standard GPU-RMQ.

### Broader Use Cases

OptiX kernels are effective for:
- **Rendering and visibility**: Monte Carlo path tracing, shadow rays, ambient occlusion
- **Geometric search**: Spatial acceleration structures (BVH, kd-trees) where ray-triangle or ray-primitive queries dominate
- **Physics simulation**: Ray-casting for collision detection where the cost of ray traversal amortizes the OptiX overhead

However, OptiX kernels are **inefficient for fine-grained data-parallel tasks** (e.g., array scans, sorting, small reductions) where warp-level operations are critical.

## Common Mistakes / Pitfalls

1. **Assuming OptiX adds no overhead**: OptiX kernels incur measurable context-switching and scheduling overhead even before using ray tracing. For small problems or cache-friendly algorithms, this overhead is not recovered.

2. **Porting warp-optimized code to OptiX without rewriting**: Simply removing warp intrinsics and hoping atomic operations "just work" often results in $2\times$ or worse slowdowns. Algorithms must be redesigned for global aggregation.

3. **Underestimating memory footprint of BVH structures**: In RTXRMQ (ray-tracing RMQ), the Bounding Volume Hierarchy (BVH) grows rapidly with input size. For $n = 2^{28}$ elements, memory usage can exceed 24 GB GPU memory, making the approach impractical.

4. **Conflating ray tracing speedup with OptiX kernel speedup**: Hardware ray tracing is fast *relative to software traversal*, but if the core algorithm doesn't benefit from rays (e.g., a linear scan is already optimal), OptiX overhead dominates.

5. **Ignoring warp-vs-global memory latency trade-offs**: Warp reductions use shared memory ($O(1)$ latency, no atomics). Atomic aggregation uses global memory ($O(100+)$ cycle latency, serialized). The cost multiplies for algorithms with many aggregations.

## See Also

- [[Warp-level primitives and intrinsics]]: CUDA's `__shfl_*`, `__ballot_sync()`, and reduction functions prohibited in OptiX
- [[GPU ray tracing and BVH traversal]]: Hardware acceleration for which OptiX kernels are designed
- [[Atomic operations and memory synchronization]]: Required alternative when warp intrinsics unavailable
- [[GPU memory hierarchy and coalescing]]: Context for understanding why OptiX thread migration hurts performance
- [[Work-stealing and dynamic load balancing]]: The underlying reason OptiX moves threads between cores

## Sources

- Kreis, Lara; Henneberg, Justus; Henkys, Valentin; Schuhknecht, Felix; Schmidt, Bert