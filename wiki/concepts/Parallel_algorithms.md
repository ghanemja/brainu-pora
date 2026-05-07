# Parallel Algorithms

## Definition

Parallel algorithms are computational procedures designed to execute multiple operations simultaneously across multiple processors, cores, or computing devices to solve a problem faster than sequential execution. Unlike traditional sequential algorithms that perform one operation at a time, parallel algorithms decompose a problem into independent or loosely-dependent subproblems that can be solved concurrently.

**Key distinction**: A parallel algorithm's efficiency is measured not just by correctness and time complexity, but by:
- **Speedup**: $S_p = \frac{T_1}{T_p}$ where $T_1$ is sequential execution time and $T_p$ is parallel execution time on $p$ processors
- **Efficiency**: $E_p = \frac{S_p}{p}$ (ideally close to 1, indicating near-linear scaling)
- **Scalability**: ability to maintain efficiency as problem size or processor count increases

## Key Equations

### Amdahl's Law
The theoretical maximum speedup of a parallel algorithm is limited by its sequential portion:

$$S_p = \frac{1}{f + \frac{1-f}{p}}$$

where $f$ is the fraction of the algorithm that must execute sequentially, and $p$ is the number of processors.

**Implication**: As $p \to \infty$, $S_p \to \frac{1}{f}$, meaning the speedup is bounded by the inverse of the sequential fraction.

### Strong Scaling Efficiency
For a fixed problem size:

$$E_p = \frac{T_{\text{optimal}}}{p \cdot T_p}$$

where $T_{\text{optimal}}$ is the theoretical minimum time.

### Weak Scaling
Measuring efficiency as problem size grows proportionally with processor count:

$$W(p) = \frac{T_1(n)}{T_p(p \cdot n)}$$

where problem size scales with $p$.

## Physical Intuition / Derivation

### Why Parallelism Matters

Consider a sequential algorithm processing $N$ elements with work complexity $O(N)$. On a single processor, this takes $T_1 = c \cdot N$ time (where $c$ is a constant factor). With $p$ processors working simultaneously:

- **Ideal case** (perfect load balancing, no communication): $T_p = c \cdot N / p$, giving linear speedup
- **Reality**: Communication overhead, synchronization costs, and load imbalance reduce efficiency

### Hierarchical Acceleration (Illustrated by GPU-RMQ Example)

The GPU-RMQ case study demonstrates a fundamental pattern in modern parallel computing:

1. **Problem decomposition**: Range Maximum Query (RMQ) problems are decomposed into hierarchical subproblems amenable to massive parallelism
2. **Data structure optimization**: The algorithm uses a hierarchical acceleration structure that minimizes memory footprint ($4\times$ smaller than alternatives) while enabling **throughput improvement of $8\text{-}17\times$**
3. **Hardware exploitation**: GPU architecture features (CUDA cores for data-parallel operations, RT cores for specialized computation) are leveraged, though heterogeneous resource utilization introduces overhead

**Key insight**: Memory efficiency ($\propto$ cache utilization and bandwidth) often dominates performance in data-parallel problems more than raw computational power.

### Scalability Characteristics

The GPU-RMQ results show **weak scaling** properties:
- RTX 3090 (24GB): handles $2^{22}$ elements
- RTX 6000 Pro (96GB): handles $2^{33}$ elements ($4\times$ larger)

This $4\times$ increase in problem size capacity with $4\times$ memory increase suggests near-constant efficiency scaling with available memory.

## Applications in Engineering

### 1. **Bioinformatics & Sequence Analysis**
- Parallel algorithms for sequence alignment (Smith-Waterman, BLAST variants)
- Range query problems on genomic data require RMQ-style solutions
- Massive parallelism via GPUs enables analysis of gigabase-scale genomes

### 2. **Pattern Matching & Text Processing**
- String matching on large text corpora (web search, document analysis)
- Suffix array construction parallelized across multiple processors
- Dynamic programming on sequence data benefits from GPU acceleration

### 3. **Data Structure Operations**
- **Hash tables on GPUs**: collision resolution and dynamic resizing across many threads
- **Search trees**: parallel tree traversal and rebalancing
- **Graph algorithms**: breadth-first search, shortest paths (Dijkstra, Bellman-Ford)

### 4. **Scientific Computing**
- Stencil computations (finite difference methods, image processing)
- Matrix operations (linear algebra libraries like cuBLAS)
- N-body simulations in computational physics

### 5. **Machine Learning**
- Gradient computation in deep learning (data-parallel across batches)
- Convolution operations in CNNs (highly parallelizable)
- Distributed training across GPUs/TPUs

### 6. **Image & Signal Processing**
- Parallel convolution and filtering
- FFT computation using fast Fourier algorithms
- Morphological operations (dilation, erosion) across pixel data

## Common Mistakes / Pitfalls

### 1. **Ignoring Amdahl's Law**
**Mistake**: Assuming parallel hardware automatically gives proportional speedups.
**Reality**: If $10\%$ of code is sequential, maximum speedup is $10\times$ regardless of processor count. Identify and optimize the critical sequential section.

### 2. **Memory Bandwidth Underestimation**
**Mistake**: Focusing only on computation time, ignoring memory access patterns.
**Reality**: Most parallel algorithms on modern hardware are **memory-bound**, not compute-bound. The GPU-RMQ result ($8\text{-}17\times$ faster) comes from cache-aware design, not just parallelism.

**Diagnostic**: Compute arithmetic intensity $I = \frac{\text{operations}}{\text{bytes transferred}}$. If $I < 10$ for GPUs, memory bandwidth is the bottleneck.

### 3. **Load Imbalance**
**Mistake**: Assuming uniform problem decomposition equals uniform execution time.
**Reality**: Irregular algorithms (sparse graphs, adaptive mesh refinement) suffer from load imbalance. Idle processors waste resources.

**Solution**: Use dynamic scheduling, work-stealing queues,