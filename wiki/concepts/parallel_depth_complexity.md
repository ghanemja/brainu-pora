# Parallel Depth Complexity

## Definition

**Parallel depth complexity** (or **parallel depth**) is a measure of the longest chain of sequential dependencies in a parallel algorithm when executed on an ideal parallel computer. It represents the minimum number of rounds needed to complete the computation, assuming unlimited processors and unit-time operations.

Formally, for an algorithm $\mathcal{A}$:
- **Depth** $D(\mathcal{A})$ = the length of the longest dependency chain from input to output
- **Work** $W(\mathcal{A})$ = total number of primitive operations across all processors
- **Span** is synonymous with depth in some contexts

The depth captures the *inherent parallelism limitation* of an algorithm independent of processor count.

## Key Equations

**Work-Depth Model:**
$$T_p = \frac{W}{p} + D$$

where:
- $T_p$ = execution time on $p$ processors
- $W$ = total work
- $D$ = depth (lower bound on parallel time)

**Optimal speedup bound:**
$$\text{Speedup} \leq \min\left(p, \frac{W}{D}\right)$$

**Scalability threshold:**
When $p \leq W/D$, we achieve linear speedup; beyond this point, speedup is bounded by $W/D$.

**Common depth bounds in practice:**
- $O(\log n)$ depth — polylogarithmic; highly parallelizable
- $O(\log^2 n)$ depth — moderately parallelizable with logarithmic overhead
- $O(n^\alpha)$ depth where $\alpha > 0$ — increasingly sequential bottleneck

## Physical Intuition / Derivation

### Why Depth Matters

Consider a pipeline filling with water:
- **Work** = total volume of water (sum of all tasks)
- **Depth** = the longest path from source to sink (bottleneck for filling time)

No matter how many workers you hire (processors), the longest sequential chain cannot be shortened below depth. If depth is $D$, you need *at least* $D$ time steps.

### Analyzing the Semisort Example

From the source material, the GSSB semisort algorithm achieves:
- **Work:** $O(n)$ with high probability (whp)
- **Depth:** $O(\log n)$ whp

**Why this depth?** The algorithm consists of three phases:

1. **Sampling & Bucketing** ($O(\log n)$ depth): 
   - Sorting the sample requires $O(\log n)$ depth (using parallel comparison sort)
   - Counting multiplicities by key is parallelizable

2. **Placement** ($O(\log n)$ depth):
   - Randomized distribution can be done in $O(\log n)$ rounds using parallel hash tables

3. **Local Semisorting** ($O(\log n)$ depth per bucket):
   - Each bucket has size $m_b = O(n/\log^2 n)$ whp
   - Radix sort on bucket $b$ takes $O(\log m_b) = O(\log n)$ depth
   - All buckets process in parallel → total depth $O(\log n)$

The total depth remains $O(\log n)$ because the maximum across all phases is dominated by logarithmic sorting operations.

### Why Upgrade from Expectation to High Probability?

The source material emphasizes upgrading from $O(\log n)$ **expected** depth to $O(\log n)$ **high probability** depth. This is crucial because:
- Tail events (rare bad cases) can derail execution time guarantees
- With $n$ items and many independent random choices, expectation alone is insufficient
- High probability: event occurs with probability $\geq 1 - n^{-c}$ for constant $c \geq 1$

## Applications in Engineering

### 1. **GPU Computing**
- GPUs are massively parallel but have limited parallelism depth (thousands of threads)
- Algorithms with $O(\log n)$ depth map well to GPU execution models
- Depth dictates synchronization barriers; minimize for GPU efficiency

### 2. **VLSI Circuit Design**
- Depth = circuit latency (clock cycles from input to output)
- Critical path sets maximum frequency
- Work = total transistor count / power consumption
- Trade-off: deep circuits (high frequency) vs. shallow circuits (low power, parallelism)

### 3. **Distributed Computing**
- Depth = number of communication rounds (network diameter constraints)
- MapReduce-style jobs: each round is a map-reduce phase
- Algorithms with logarithmic depth enable fast convergence in distributed optimization

### 4. **Reconfigurable Hardware (FPGAs)**
- Depth determines pipeline stages for optimal throughput
- Shallow depths allow higher clock frequencies
- Work determines resource utilization (LUTs, memory)

### 5. **Real-Time Systems**
- Hard real-time guarantees require worst-case depth bounds (high probability strengthens this)
- Autonomous vehicles, robotics: depth = maximum latency permitted

### 6. **Machine Learning**
- Training neural networks in parallel: batch size relates to work; training steps relate to depth
- Gradient descent iterations form a dependency chain (sequential depth)
- Synchronization depth in distributed SGD

## Common Mistakes / Pitfalls

### 1. **Confusing Depth with Execution Time**
❌ **Wrong:** "My algorithm has depth $O(\log n)$, so it runs in $O(\log n)$ time."  
✓ **Right:** Execution time is $T_p = W/p + D$. Depth is a lower bound, not the actual time.

### 2. **Ignoring Constants in Polylogarithmic Depth**
- $O(\log^2 n)$ depth might require $(\log n)^2 = 100$ rounds for $n = 2^{10}$
- Hidden constants and practical overhead can dominate
- Cache locality, synchronization cost, and communication latency matter in practice

### 3. **Assuming Unlimited Parallelism**
- The work-depth model assumes ideal parallelism; real systems have:
  - Memory bandwidth limits
  - Cache coherency overhead
  - Synchronization costs (not unit-time)
- A