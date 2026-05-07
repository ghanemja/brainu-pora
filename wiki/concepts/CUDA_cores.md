# CUDA cores

## Definition

**CUDA cores** are the fundamental parallel processing units in NVIDIA GPUs that execute general-purpose compute kernels. They are scalar processors capable of performing floating-point and integer operations independently, forming the primary compute backbone of CUDA-enabled GPUs.

Unlike specialized hardware units (such as tensor cores for matrix operations or RT cores for ray-tracing), CUDA cores handle arbitrary computational tasks through SIMD (Single Instruction Multiple Data) execution within warp groups of 32 threads. Each core can execute one instruction per clock cycle on its assigned thread.

## Key Equations

While CUDA cores do not have specific mathematical equations defining their operation, the following relationships characterize their performance:

**Peak Throughput (FP32 operations per second):**
$$T_{\text{peak}} = N_{\text{cores}} \times f_{\text{clock}} \times \text{ops/cycle}$$

where $N_{\text{cores}}$ is the number of CUDA cores, $f_{\text{clock}}$ is clock frequency (GHz), and ops/cycle depends on instruction pipelining.

**Effective Bandwidth Utilization:**
$$B_{\text{eff}} = \frac{\text{Data transferred}}{\text{Total execution time}} \leq B_{\text{peak}}$$

**Occupancy (thread utilization factor):**
$$\text{Occupancy} = \frac{\text{Active warps per multiprocessor}}{\text{Maximum possible warps}} \in [0, 1]$$

## Physical Intuition / Derivation

### Warp Execution Model

CUDA cores operate in **warps**—groups of 32 threads that execute the same instruction on different data. A single multiprocessor (SM) contains multiple CUDA cores and can manage hundreds of warps in flight simultaneously through hardware-level scheduling. This massive multi-threading compensates for individual thread latencies.

### Hybrid Compute Strategy

The source material demonstrates that modern GPU acceleration structures (like GPU-RMQ) benefit from **hierarchical specialization**:

- **Lower hierarchy levels** → CUDA cores (general-purpose scanning, flexible control flow)
- **Upper hierarchy levels** → RT cores (fixed, highly-optimized ray-triangle intersections)

This hybrid approach exploits each unit's strengths:
- CUDA cores: flexible, adaptive, configurable for variable workload patterns
- RT cores: fixed-function, extremely fast for single-purpose operations

### Memory Hierarchy Interaction

CUDA core performance depends critically on memory access patterns:
- **Coalesced loads**: Multiple threads access consecutive memory addresses → single memory transaction
- **Vector loading**: Batch-fetching to reduce bandwidth overhead
- **Warp-local queuing**: Organizing work per-warp to maximize cache locality

The GPU-RMQ paper emphasizes "hardware-conscious scan operations" that align CUDA core execution with memory subsystem capabilities.

## Applications in Engineering

### 1. **Data Processing & Analytics**
- Massive parallel scans, filters, and reductions on arrays (as in GPU-RMQ range minimum queries)
- Database query acceleration
- Scientific computing (CFD, molecular dynamics simulations)

### 2. **Machine Learning (non-matrix)**
- Custom kernel implementations for specialized layers
- Data preprocessing and augmentation pipelines
- Graph neural network traversals requiring flexible control flow

### 3. **Image & Signal Processing**
- Convolutions, morphological operations (when not optimized via tensor cores)
- Stencil computations
- Real-time video processing with adaptive algorithms

### 4. **Ray Tracing & Graphics**
- Fallback compute for non-geometric operations
- Hybrid workloads combining ray tracing (RT cores) with custom shading kernels (CUDA cores)
- Demonstrated in GPU-RMQ's hierarchical acceleration structure

### 5. **Numerical Methods**
- Iterative solvers requiring arbitrary control logic
- Stochastic simulations with data-dependent branching
- Adaptive mesh refinement algorithms

## Common Mistakes / Pitfalls

### 1. **Ignoring Memory Coalescing**
❌ **Mistake**: Assuming all CUDA core operations are equally fast  
✓ **Correct**: Uncoalesced memory access causes serialization; strided or random access decimates throughput despite high core count

### 2. **Treating CUDA Cores as Interchangeable with Specialized Units**
❌ **Mistake**: Using CUDA cores for matrix multiplication when tensor cores exist  
✓ **Correct**: Specialized cores often provide 10-100× higher throughput for their domain; reserve CUDA cores for flexible, non-standard operations

### 3. **Poor Occupancy Management**
❌ **Mistake**: Writing kernels that use excessive registers, limiting active warps per SM  
✓ **Correct**: Balance register usage, shared memory, and thread block size to maintain >50% occupancy

### 4. **Underutilizing Parallelism in Hierarchical Algorithms**
❌ **Mistake**: Processing hierarchy levels sequentially  
✓ **Correct**: As GPU-RMQ demonstrates, batch queries and use cooperative thread groups for parallel hierarchy traversal

### 5. **Ignoring Hybrid Hardware Opportunities**
❌ **Mistake**: Only using CUDA cores when specialized hardware (RT cores, tensor cores) could accelerate specific subtasks  
✓ **Correct**: Design algorithms to exploit multiple hardware units (hybrid approach in GPU-RMQ improved both construction time and throughput)

## See Also

- [[GPU Memory Hierarchy]]: Understanding cache behavior is essential for CUDA core optimization
- [[Warp Scheduling & Occupancy]]: Critical for predicting CUDA core utilization
- [[RT Cores]]: Specialized alternative for ray-tracing; contrasts with general-purpose CUDA cores
- [[Tensor Cores]]: Matrix-optimized compute units; why CUDA cores suit irregular workloads
- [[Cooperative Thread Groups]]: Synchronization primitive for coordinating CUDA core operations across warps

## Sources

- GPU-RMQ paper: "Highly efficient GPU-based acceleration structure for answering Range Minimum Queries" — hybrid CUDA/RT core design, section 1.1 and optimization discussions
- Context: Comparison with LCA, RTXRMQ, HRMQ baseline methods demonstrating CUDA core utility in hierarchical data structures