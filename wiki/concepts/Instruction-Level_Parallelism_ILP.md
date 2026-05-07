# Instruction-Level Parallelism (ILP)

## Definition

**Instruction-Level Parallelism (ILP)** is a processor microarchitecture technique that executes multiple independent instructions from a single instruction stream concurrently, rather than strictly sequentially. ILP exploits the fact that consecutive instructions in a program often have no data or control dependencies, allowing a modern superscalar processor to issue and execute them in parallel across multiple execution units.

ILP differs from thread-level parallelism (TLP) in that it operates within a single logical thread of execution—the hardware automatically identifies parallelizable instructions without explicit programmer intervention or multiple threads.

## Key Concepts

### Instruction Dependencies

For instructions to execute in parallel, they must be **independent**—that is, free from:

- **Data dependencies**: An instruction reads a register or memory location written by a previous instruction
- **Control dependencies**: Branch instructions that affect which instructions execute next
- **Resource conflicts**: Two instructions competing for the same execution unit

### ILP Window

The **instruction window** (or reorder buffer depth) defines the maximum number of in-flight instructions the processor can track simultaneously. Larger windows expose more parallelism but increase complexity and power consumption.

$$\text{Maximum theoretical ILP} = \frac{\text{Number of independent instructions}}{\text{Critical dependency chain length}}$$

## Physical Intuition / Derivation

### Why ILP Matters

Consider a modern processor with multiple execution units (ALU, load/store unit, floating-point unit, branch unit). Without ILP, each unit sits idle while instructions execute sequentially—like having a multi-lane highway where only one lane is used.

A processor with **width** $w$ (ability to issue $w$ instructions per cycle) achieves speedup only if the instruction stream provides $w$ independent instructions. For example:

```
Sequential execution (width = 1):
1. A = B + C          [cycle 1: uses ALU]
2. D = A * 2          [cycle 2: uses ALU, depends on A]
3. E = F + G          [cycle 3: uses ALU, independent of A,D]
4. H = E + 10         [cycle 4: uses ALU, depends on E]
Total: 4 cycles

With ILP (width = 2):
1. A = B + C    |    E = F + G      [cycle 1: both ALUs active]
2. D = A * 2    |    H = E + 10     [cycle 2: both ALUs active]
Total: 2 cycles
```

### Hardware Mechanisms

Modern processors extract ILP through:

1. **Out-of-order execution**: Instructions execute when operands are ready, not in program order
2. **Register renaming**: Eliminates false (anti) dependencies by dynamically allocating new physical registers
3. **Speculative execution**: Predicts branch outcomes and executes speculatively, rolling back if wrong
4. **Dynamic scheduling**: Tracks dependencies at runtime via the reservation station/issue queue

### Limits to ILP

Two fundamental barriers limit ILP:

**1. True Dependency Chain:** Even with infinite hardware resources, Amdahl's law applies:

$$\text{Speedup}_{\text{ILP}} \leq w \quad \text{(width-limited)}$$

$$\text{Speedup}_{\text{ILP}} \leq \frac{\text{Average instructions per cycle}}{\text{Critical path length}} \quad \text{(dependency-limited)}$$

**2. Resource Constraints:** With $w$ execution units, the achievable ILP is bounded by instruction mix. If a workload requires 50% floating-point and 50% integer ops but has only one FP unit, max width is effectively $\leq 1.5$.

## Applications in Engineering

### 1. **Compiler Optimization**
Modern compilers (GCC, LLVM, ICC) perform instruction scheduling to maximize ILP:
- Instruction reordering respecting dependencies
- Loop unrolling to expose parallelism across iterations
- Predication to convert branches to conditional execution

### 2. **Sorting Algorithm Optimization**
As mentioned in the source material, sorting algorithms like **bsort** can be optimized by:
- Replacing branching comparisons with **branchless conditional moves** (e.g., `cmov` on x86), which avoid branch mispredictions that stall the pipeline
- Overlapping partitioning operations to hide memory latency
- Example: Instead of:
  ```c
  if (a > b) { temp = a; a = b; b = temp; }  // Branch prediction risk
  ```
  Use: `a = min(a,b); b = max(a,b);` (compiler may use cmov)

### 3. **Memory System Design**
Processors with higher ILP benefit from:
- Deeper pipelines (more in-flight instructions tolerate cache latency)
- Larger L1/L2 caches (reduce load-use stalls)
- Prefetching (hide main memory latency across parallel instructions)

### 4. **SIMD Integration**
ILP complements SIMD. While SIMD parallelizes within a single instruction (data-level parallelism), ILP parallelizes across independent instructions:
- SIMD `vpaddd` (vector add) on 4 integers + independent scalar operation = effective use of both instruction-level and data-level parallelism

### 5. **Real-Time Systems**
High-ILP designs are problematic for real-time systems because:
- Variable execution time due to dependency stalls and speculation
- Worst-case timing analysis becomes intractable
- In-order processors with predictable timing are preferred

## Common Mistakes / Pitfalls

### 1. **Assuming Compiler Does All the Work**
Compilers cannot overcome fundamental data dependencies. Code like:
```c
for (int i = 0; i < N; i++) {
    result = result + array[i];  // Reduction—each iteration depends on prior
}
```
Has inherent sequential dependency regardless of compiler. Rewrite with multiple accumulators:
```c
r1 = r2 = r3 = r4 = 0;
for (int i = 0; i < N; i += 4) {
    r1 += array[i];
    r2 += array[i+1];
    r3 += array[