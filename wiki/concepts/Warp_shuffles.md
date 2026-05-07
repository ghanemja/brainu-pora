# Warp Shuffles

## Definition

A **warp shuffle** is a low-latency inter-thread communication primitive in GPU programming (particularly NVIDIA CUDA) that allows threads within a warp to exchange data directly through their registers without accessing main memory or shared memory. A warp is the smallest scheduling unit on a GPU, typically consisting of 32 threads that execute in lockstep.

Warp shuffles enable **intra-warp data redistribution**: a thread can broadcast its register values to other threads in the same warp, scatter values across threads, gather values from other threads, or perform butterfly permutations—all within 1-2 clock cycles.

## Key Equations

### Memory Access Efficiency

Consider a batch of $m$ queries processed by $g$ threads per query:

**Multi-load strategy:**
$$\text{Memory transfers} = \frac{g \cdot m}{g} = m$$

**Warp-local queuing (WLQ) with shuffles:**
$$\text{Memory transfers} = \frac{m}{g}$$

**Improvement factor:** $g \times$ reduction in coalesced memory accesses when $g \leq 16$.

Register overhead for WLQ:
$$\text{Additional registers per thread} = 2g \text{ (for scattered RMQ bounds)}$$

## Physical Intuition / Derivation

### Why Shuffles Matter

On modern GPUs, the memory hierarchy has extreme latency differences:
- **Register access:** ~1 cycle (local to each thread)
- **Warp shuffle:** ~2 cycles (dedicated hardware bus within warp)
- **Shared memory:** ~20 cycles
- **Global memory:** ~200-400 cycles

Traditional inter-thread communication requires writing to shared memory (a bottleneck for many threads) or main memory (expensive). Warp shuffles bypass this by leveraging **dedicated wiring** between threads in a warp.

### How WLQ Repurposes Registers as a Queue

In the warp-local queuing strategy applied to Range Minimum Queries (RMQ):

1. **Thread spawning:** Only $m$ threads launched (vs. $g \cdot m$ in multi-load)
   - Saves thread management overhead
   - Reduces occupancy pressure

2. **Query distribution:** Thread $i$ initially owns query $i$, holding bounds $l_i$ and $r_i$

3. **Group processing loop:** For $g$ rounds:
   - Thread at rank $k$ in group broadcasts its $(l_k, r_k)$ via shuffle to all group members
   - All threads cooperatively scan the range together
   - Result is shuffled back to thread $k$ (only thread $k$ needs the answer initially)
   - Move to next thread's query

4. **Register reuse:** At each round, registers holding $(l, r)$ are overwritten with the next query's bounds—the registers form a virtual queue with no separate data structure overhead.

**Bandwidth comparison** (for Figure 10 example with $g=4$):
- Multi-load: $4 \times 8 = 32$ queries → 8 coalesced transfers (4 queries per transfer)
- WLQ: $8$ queries → 2 coalesced transfers (4 queries per transfer)

## Applications in Engineering

### 1. GPU-Accelerated Range Queries
**Context:** Processing batch workloads of Range Minimum Queries (RMQ) on modern GPUs.
- Use case: Competitive range queries, sparse table lookups, distance computations
- Benefit: Warp shuffles reduce memory pressure by $g \times$ for $g$-thread cooperative algorithms
- Trade-off: Increased register pressure (critical resource on older GPU generations)

### 2. Parallel Reductions
Warp shuffles enable tree-based reductions (sum, max, min) across warp without shared memory:
```
result = value;
for (int offset = 16; offset > 0; offset /= 2)
    result = min(result, __shfl_down_sync(0xFFFFFFFF, result, offset));
```
Applications: histogram computation, statistics aggregation, sorting networks.

### 3. Collective Communication in Multi-GPU Systems
- Distribute batched requests across warp before global synchronization
- Reduce redundant global memory reads when multiple threads need the same data
- Minimize synchronization barriers by processing multiple independent queries per warp

### 4. Spatial Data Structures
- K-d tree traversal where a warp processes multiple queries cooperatively
- Bounding volume hierarchy (BVH) queries in ray tracing
- Machine learning inference with batched feature lookups

## Common Mistakes / Pitfalls

### 1. **Exceeding Shuffle Width**
Shuffles only work within a warp (typically 32 threads). Attempting to shuffle between threads across warp boundaries silently produces undefined results or zeros. Always check `__shfl_sync()` calls are within warp bounds.

### 2. **Register Pressure Not Accounted For**
WLQ trades memory bandwidth for registers. On architectures with limited registers per thread (e.g., older compute capability), register spilling to local memory can **negate all WLQ benefits**. Profile with `nvprof --metrics gst_efficiency` and `--metrics global_hit_rate`.

### 3. **Ignoring Warp Divergence in Shuffle Operations**
If the condition determining which threads execute a shuffle differs across threads, results are undefined. All participating threads must execute the shuffle instruction (though not all need to use the result):
```cuda
__shfl_sync(FULL_MASK, value, sourceThread); // OK: all threads execute
if (condition)
    __shfl_sync(FULL_MASK, value, sourceThread); // WRONG: divergent execution
```

### 4. **Assuming Deterministic Scheduling Across Thread Groups**
Different thread groups in the same kernel may start and finish at different times. Warp-local queuing introduces implicit **intra-warp synchronization** but not inter-warp synchronization. Cross-group coordination requires explicit barriers.

### 5. **Missing Synchronization Masks in Modern CUDA**
Deprecated `__shfl()` (implicit synchronization) should be replaced with `__shfl_sync(mask, ...)`. Failure to update can cause deadlocks on compute capability ≥7.0.