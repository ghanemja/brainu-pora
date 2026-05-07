# Warp Locality

## Definition

**Warp locality** is a GPU execution property that guarantees threads within a warp (a group of threads executed in lockstep on modern GPUs) remain assigned to the same processing core throughout their execution. This property enables the safe use of **warp intrinsics**—low-level synchronization and communication primitives that assume threads in a warp can directly access each other's data and state without global synchronization.

In NVIDIA's terminology:
- A **warp** typically consists of 32 threads
- **Warp intrinsics** include operations like `__shfl_down()`, `__ballot()`, and warp-level reductions
- **Warp locality guarantee**: the programming model ensures no thread migration between cores during warp execution

When warp locality is *not* guaranteed (e.g., in OptiX ray tracing kernels), warp intrinsics are forbidden and must be replaced with less efficient alternatives like atomic operations.

## Key Equations

Warp intrinsic speedup factor (illustrative):

$$S_{\text{warp}} = \frac{T_{\text{atomic}}}{T_{\text{warp intrinsic}}} \approx 10\text{–}100\times$$

where $T_{\text{warp intrinsic}}$ represents latency of direct warp communication and $T_{\text{atomic}}$ represents atomic global memory aggregation.

**Memory access pattern with warp locality:**
$$\text{Access cost} = O(1) \text{ per thread (warp-local)} \quad \text{vs} \quad O(\log W) \text{ per thread (atomic)}$$

where $W$ is the warp width (typically 32).

## Physical Intuition / Derivation

### Why Warp Locality Matters

GPUs execute threads in **lockstep synchronization** within a warp—all threads in a warp must proceed through the same instruction stream. If the hardware guarantees that these threads remain on the same physical core, several optimizations become safe:

1. **Direct register communication**: Thread $i$ can use `__shfl_down(value, offset)` to read a register value from thread $i + \text{offset}$ without memory access
2. **Implicit synchronization**: No explicit barrier needed; all threads in a warp are naturally synchronized at each instruction
3. **Reduction patterns**: Sum, max, or other aggregations across a warp use $\log_2(W)$ shuffle operations instead of global atomics

### Why OptiX Breaks Warp Locality

OptiX (NVIDIA's ray tracing framework) uses a **divergent execution model**:
- Rays (threads) may follow different code paths based on scene geometry
- The scheduler may pause rays and resume them on different cores
- This breaks the assumption that a warp remains cohesive on one core
- Therefore, OptiX forbids warp intrinsics entirely

### Trade-off Example

**With warp locality (WLQ = Warp-Level Queries):**
$$T_{\text{reduction}} = \lceil \log_2(W) \rceil \approx 5 \text{ cycles (32-thread warp)}$$

**Without warp locality (atomic aggregation):**
$$T_{\text{aggregation}} = T_{\text{atomic}} + T_{\text{contention}} \approx 100\text{–}1000 \text{ cycles}$$

The performance penalty motivates keeping computations on traditional GPU kernels rather than OptiX.

## Applications in Engineering

### 1. **GPU-Accelerated Range Minimum Query (RMQ)**
In the source material, GPU-RMQ uses warp-level reductions to efficiently aggregate results from multiple threads. When the same algorithm is ported to OptiX for ray tracing integration, switching from warp intrinsics to atomic operations causes **significant overhead** (visible at $2^{30}$ array elements and beyond).

### 2. **Parallel Prefix Scans**
Scan algorithms (parallel cumulative sum) heavily rely on warp-level shuffle operations:
$$\text{Parallel Scan} = O(\log N) \text{ warp steps} + O(\log B) \text{ block steps}$$
where $B$ is block size. OptiX versions require thread-block level atomics instead.

### 3. **Histogram/Sorting on GPUs**
Warp-level reductions allow local histogram binning before atomic updates to global bins, reducing contention by a factor of (threads per warp).

### 4. **Ray Tracing vs. Non-Ray-Tracing Trade-offs**
Engineers must decide: *Is the benefit of ray tracing hardware worth losing warp locality performance?* 
The source material shows that for RMQ, the answer is **no**—the overhead of OptiX negates speedup from ray tracing for typical workloads.

## Common Mistakes / Pitfalls

### 1. **Assuming Warp Locality in All GPU Kernels**
❌ **Mistake**: Using `__shfl_down()` inside dynamic parallelism or OptiX kernels  
✓ **Correct**: Check execution model documentation; restrict warp intrinsics to standard CUDA kernels

### 2. **Not Measuring the Atomic Overhead**
❌ **Mistake**: Assuming atomic fallbacks are "just a bit slower"  
✓ **Correct**: Atomic operations have 10–100× worse latency; always benchmark before porting to OptiX

### 3. **Ignoring Register Pressure**
Warp intrinsics appear "free" but heavy use of shuffle operations increases register pressure. Swapping to atomics may actually reduce register usage but increase memory traffic—the net effect depends on problem structure.

### 4. **Conflating Warp Locality with Thread Divergence**
❌ **Mistake**: Thinking thread divergence breaks warp locality  
✓ **Correct**: Threads can diverge (take different branches) and still maintain warp locality; OptiX's *scheduler-based* rescheduling breaks locality, not divergence itself

## See Also

- [[Warp synchronization]] — explicit synchronization within warps
- [[GPU atomic operations]] — memory-based synchronization alternative when warp intrinsics unavailable
- [[CUDA warp-level primitives]] — shuffle, ballot, matching operations
- [[Op