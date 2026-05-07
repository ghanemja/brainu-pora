# SIMD Instructions

## Definition

**SIMD** (Single Instruction, Multiple Data) is a parallel computing architecture that executes a single machine instruction on multiple independent data elements simultaneously. It enables one CPU instruction to operate on a vector of data values in lockstep, rather than one scalar value per instruction.

In formal terms, a SIMD operation maps:
$$\text{instruction}(a_1, a_2, \ldots, a_n) \rightarrow (r_1, r_2, \ldots, r_n)$$

where a single operation is broadcast across $n$ independent data elements, with results computed in parallel within a single clock cycle or pipeline stage.

## Key Equations

For a data-parallel operation on vector registers, the speedup factor is theoretically:
$$S_{\text{SIMD}} = \min(n, \text{ILP}_{\text{available}})$$

where $n$ is the **vector width** (number of data elements per SIMD register) and $\text{ILP}_{\text{available}}$ is the instruction-level parallelism available in the hardware.

The throughput improvement for embarrassingly parallel operations is bounded by:
$$T_{\text{improved}} = \frac{T_{\text{scalar}}}{n} \times \text{overhead}_{\text{vectorization}}$$

where overhead includes register pressure, memory bandwidth constraints, and data alignment costs.

## Physical Intuition / Derivation

### Motivation
Modern CPUs execute one instruction per cycle (ideally). However, many workloads process multiple independent data elements—**bit-masking operations, conditional moves in sorting, or parallel comparisons**. Rather than issuing $n$ separate scalar instructions, SIMD allows one instruction to process all $n$ elements at once, amortizing the instruction dispatch cost.

### Hardware Implementation
SIMD execution leverages:

1. **Wide datapaths**: CPUs contain specialized registers (e.g., 128-bit XMM, 256-bit AVX, 512-bit AVX-512) that hold multiple operands
2. **Parallel ALUs**: Multiple functional units operate on sub-word elements independently
3. **Synchronized execution**: All sub-operations complete in the same cycle (or pipeline stage)

### Why It Matters for Sorting
In the context provided, **bit-masking operations and branchless partitioning** are ideal SIMD candidates because:
- They apply the same operation to many data elements
- They avoid branch mispredictions (critical for CPU pipeline efficiency)
- Conditional move instructions (e.g., `CMOV`) execute without branching, improving instruction cache locality

## Applications in Engineering

### 1. Sorting Algorithms
- **Radix sort optimization**: Vectorize counting histograms or bit-extraction across multiple keys
- **Partition operations**: Use SIMD conditional moves to avoid expensive branch mispredictions during quicksort/bitwise sort partitioning
- **Bit-masking**: Process $n$ bits per element simultaneously across $n$ keys

### 2. Scientific Computing
- Matrix operations: SSE/AVX acceleration of element-wise operations
- Convolution and filtering: Process multiple pixels/samples in parallel
- FFT preprocessing: Parallel bit-reversal or twiddle factor computations

### 3. Database Systems
- Vectorized comparisons for filtering and aggregation
- Parallel bit-vector scans for predicate evaluation
- Columnar storage alignment with SIMD-friendly memory layouts

### 4. Graphics & Game Engines
- Vector arithmetic (dot products, normalizations) on positions/colors
- Particle physics: Parallel force/velocity updates
- Collision detection: Batch distance computations

### 5. Cryptography
- Parallel AES block encryption
- Hash function acceleration (e.g., SHA-256 state updates)
- Constant-time operations to prevent timing attacks

## Common Mistakes / Pitfalls

### 1. **Ignoring Memory Bandwidth**
SIMD gains evaporate if data cannot be delivered to the CPU fast enough. Unaligned memory access or poor cache locality defeats vectorization benefits.

**Fix**: Ensure data alignment (typically 16, 32, or 64 bytes) and use cache-oblivious or cache-friendly data layouts.

### 2. **Vectorizing Branches**
Attempting to vectorize code with conditional control flow (if-else) across the vector often requires predication or blending, which is more expensive than scalar branching.

**Fix**: Use **branchless algorithms** with conditional moves or bit manipulation instead of conditional jumps.

### 3. **Register Pressure**
Using many SIMD registers simultaneously spills to memory, negating performance gains. Each vector element occupies register space.

**Fix**: Profile register allocation; consider hybrid approaches with scalar fallback paths.

### 4. **Hardware Portability Assumptions**
Not all CPUs support the same SIMD extensions (AVX-512 is rare; AVX is mainstream; SSE is older). Code compiled for AVX-512 crashes on older CPUs.

**Fix**: Use runtime CPU feature detection or ship multiple binaries; consider portable libraries (e.g., `std::simd` in C++17, or SIMD wrappers).

### 5. **Disregarding Data Type Width Mismatch**
Vectorizing across heterogeneous word sizes (mixing 8-bit and 32-bit operations) is inefficient; the vector width must align with the data width.

**Fix**: Keep homogeneous data types within SIMD loops; use SIMD instructions designed for your data width.

## Detailed Context: SIMD in Sorting

The source material highlights SIMD as a performance enhancement for **bit-sorting algorithms** in larger word-size regimes. Specifically:

- **Bit-masking parallelization**: Extract multiple bits from multiple keys in parallel
- **Branchless partitioning**: Use SIMD conditional moves to partition data without branch mispredictions, avoiding pipeline flushes
- **Instruction-Level Parallelism (ILP) overlap**: Issue multiple SIMD operations per cycle, overlapping memory latency with computation

The authors note that their experimental platform lacked modern SIMD support, making evaluation impossible. However, for practical high-performance sorting (especially radix and bitwise sorts), SIMD integration is **critical** for scaling beyond small word sizes (8-bit).

## See Also

- [[Instruction-Level Parallelism (ILP)]] — overlapping independent