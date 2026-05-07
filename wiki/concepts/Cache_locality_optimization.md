# Cache Locality Optimization

## Definition

**Cache locality optimization** is the practice of structuring algorithms and data access patterns to maximize cache hit rates and minimize cache misses by exploiting the hierarchical memory structure of modern processors. It involves organizing computation and memory references so that data accessed in close temporal and spatial proximity is kept together in fast cache levels.

Cache locality encompasses two primary dimensions:

- **Temporal locality**: Recently accessed data is likely to be accessed again soon
- **Spatial locality**: If data at address $x$ is accessed, data near address $x$ is likely to be accessed soon

In the context of sorting algorithms, poor cache locality manifests as frequent cache misses during recursive partitioning operations, causing significant performance degradation despite favorable asymptotic complexity.

## Key Equations

### Cache Miss Cost Model

The effective memory access time can be modeled as:

$$T_{\text{eff}} = T_{\text{hit}} \cdot P_{\text{hit}} + T_{\text{miss}} \cdot P_{\text{miss}} \cdot T_{\text{miss\_penalty}}$$

where:
- $T_{\text{hit}}$ = cache hit latency (typically 1-4 cycles for L1)
- $P_{\text{hit}}$ = probability of cache hit
- $T_{\text{miss}}$ = memory access latency (typically 200-400 cycles for main memory)
- $P_{\text{miss}} = 1 - P_{\text{hit}}$ = probability of cache miss

### Working Set Threshold

Optimal cache-friendly recursion depth occurs when the partition size $n$ satisfies:

$$n_{\text{optimal}} \approx \frac{L}{s \cdot \tau}$$

where:
- $L$ = cache line size (typically 64 bytes)
- $s$ = element size in bytes
- $\tau$ = elements per cache line

For 64-byte cache lines and 8-byte elements: $n_{\text{optimal}} \approx 8$ elements per partition.

## Physical Intuition / Derivation

### Why Cache Locality Matters

Modern CPU memory hierarchies are fundamentally **asymmetric**:

```
L1 Cache (32 KB):     ~4 cycles
L2 Cache (256 KB):    ~10 cycles
L3 Cache (8 MB):      ~40 cycles
Main Memory (GB+):    ~200-300 cycles
```

A single cache miss can erase the benefit of hundreds of fast operations. Consider sorting 1 million integers:

- **With good locality**: Most accesses hit L1/L2 (4-10 cycles), few memory accesses
- **With poor locality**: Random access patterns force main memory hits (300 cycles), causing 30-75× slowdown per miss

### Hybrid Algorithm Design

The source material identifies a critical performance gap in the `bsort` algorithm for larger word sizes. The solution involves **adaptive recursion depth control**:

**Phase 1 (Recursive)**: Use cache-optimal algorithm while partitions remain small (e.g., $> n_{\text{optimal}}$)

**Phase 2 (Base case)**: Switch to non-recursive, cache-friendly implementation when:

$$\text{partition\_size} \leq \alpha \cdot n_{\text{optimal}}$$

where $\alpha$ is an empirically-tuned constant (typically 2-4).

This hybrid approach ensures:
1. Recursive overhead is eliminated for small subproblems
2. Working set remains within cache boundaries
3. Linear scan operations (sequential access) dominate final phase, guaranteeing spatial locality

### Instruction-Level Optimization

Beyond data locality, the source identifies three complementary optimizations:

| Technique | Benefit | Mechanism |
|-----------|---------|-----------|
| **Branchless partitioning** | Eliminate branch misprediction penalties | Use conditional move (`cmov`) instead of conditional jumps |
| **SIMD parallelization** | Exploit 4-8 way data parallelism | Apply bit-masking to 256-bit or 512-bit registers simultaneously |
| **Instruction-level parallelism (ILP)** | Hide memory latency | Overlap multiple independent operations to fill CPU pipeline |

## Applications in Engineering

### 1. High-Performance Sorting Systems
- **Integer sorting** for databases and in-memory analytics (particularly effective for fixed-width data)
- **Radix sort variants** that partition data in-place while maintaining cache efficiency
- **Adaptive quicksort** implementations that detect small-partition thresholds

### 2. Embedded and Real-Time Systems
- **8-bit/16-bit microcontroller sorting**: Source notes `bsort` is "particularly effective for small word-size regimes"
- **Predictable latency**: Cache-friendly algorithms reduce variance in response times
- **Energy efficiency**: Fewer main memory accesses reduce power consumption

### 3. SIMD-Accelerated Algorithms
- **Vectorized partitioning**: Process 8-16 elements per cycle using SIMD instructions
- **Bit-parallel operations**: Conditional moves (`cmov`, `blend`) avoid branch mispredictions
- **Streaming algorithms**: Exploit wide loads/stores of modern GPUs and CPUs

### 4. Database Query Engines
- **Sort-based joins and aggregations**: Cache locality directly impacts query latency
- **Column-store layouts**: Optimize spatial locality by grouping related data elements

### 5. Graphics and Game Engines
- **Particle sorting**: Spatial coherence in cache directly affects frame rate
- **Z-buffer algorithms**: Cache-friendly memory access patterns are critical for real-time performance

## Common Mistakes / Pitfalls

### 1. **Ignoring the Recursion Overhead**
❌ **Wrong**: Implementing recursive partition even for tiny subarrays (size 1-2)
✓ **Right**: Use hybrid approach with empirically-determined threshold (typically 32-64 elements)

**Why this matters**: Recursive function calls pollute instruction cache and add stack overhead. The source explicitly identifies this as hindering performance: "the Opwq recursion depth penalty could be significantly mitigated" through base-case switching.

### 2. **Over-Optimizing Before Profiling**
❌ **Wrong**: Implementing SIMD without measuring cache miss rate first
✓ **Right**: Profile memory access patterns; SI