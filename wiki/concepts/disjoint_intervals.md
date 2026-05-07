# disjoint intervals

## Definition

**Disjoint intervals** are a collection of non-overlapping intervals on a linearly ordered domain such that no two intervals share a common point. Formally, intervals $I_1, I_2, \ldots, I_k$ are disjoint if:

$$I_i \cap I_j = \emptyset \quad \forall i \neq j$$

In the context of distributed resource allocation, disjoint intervals represent non-overlapping contiguous ranges of resources (slots, memory addresses, identifiers, etc.) that can be independently assigned to different entities without conflict.

## Key Equations

**Union of disjoint intervals:** If intervals $I_1, I_2, \ldots, I_k$ are pairwise disjoint with sizes $S_1, S_2, \ldots, S_k$, their union forms a single contiguous interval:

$$\bigcup_{i=1}^{k} I_i = \left[1, \sum_{i=1}^{k} S_i\right)$$

**Preservation property:** If fragments $F_1, F_2, \ldots, F_m$ initially hold disjoint intervals and each fragment's request size matches its interval size, then after allocation:

$$\text{disjoint}(I_1^{\text{initial}}, \ldots, I_m^{\text{initial}}) \implies \text{disjoint}(I_1^{\text{final}}, \ldots, I_m^{\text{final}})$$

## Physical Intuition / Derivation

### Why Disjoint Intervals Matter

Consider a distributed system where multiple fragments must each acquire resources (slots, memory blocks, or identifiers) from a global pool. If two fragments receive **overlapping** intervals, they could both access the same resource, causing conflicts, race conditions, or resource double-allocation.

By enforcing disjoint intervals, we guarantee:
- **No conflicts:** Each resource belongs to exactly one fragment
- **Fairness:** Resources are partitioned deterministically
- **Traceability:** Each fragment's resource allocation can be traced back to its origin

### Constructive Approach

The allocation procedure works hierarchically:

1. **Request phase:** Fragment leaders upcast slot requests of size $S_i$ toward the root
2. **Aggregation phase:** The root collects total demand $\sum S_i$ and allocates one master interval $[1, \sum S_i)$
3. **Distribution phase:** The master interval is subdivided and propagated back down the tree
4. **Result:** Each fragment $i$ receives a disjoint sub-interval of size exactly $S_i$

This structure ensures disjointness: since each fragment's request is satisfied sequentially in the aggregation phase, and sizes match exactly, no overlap can occur.

### Tracking Through the Tree

A subtle challenge arises when requests travel through a BFS tree with both:
- **Intrinsic convergecast steps** (aggregation over base fragments)
- **Extrinsic convergecast steps** (pipelined aggregation over the BFS tree)

To retrace which intervals correspond to which origin fragments, intermediate vertices must **cache partial sums** as requests propagate upward. This caching overhead is only $O(\log n)$ bits per vertex, making the scheme memory-efficient.

## Applications in Engineering

### 1. Distributed Memory Allocation
In parallel computing systems, disjoint intervals allocate virtual address spaces to different processes, ensuring no two processes write to the same memory location.

### 2. Slot Assignment in Networks
Network protocols use disjoint intervals to assign time slots, frequency bands, or node IDs to different subnetworks or devices, preventing collisions.

### 3. Database Partitioning
Range-based partitioning of database keys uses disjoint intervals to distribute rows across shards, ensuring each row is stored exactly once.

### 4. Resource Scheduling
In cloud computing, VM instances receive disjoint intervals of CPU cycles, disk I/O quotas, or network bandwidth, preventing resource contention.

### 5. Graph Algorithms on Distributed Architectures
When computing on fragments of a graph distributed across processors, disjoint vertex/edge ID ranges ensure consistent global numbering and prevent re-processing.

## Common Mistakes / Pitfalls

### 1. **Assuming Disjointness Without Proof**
Students often assume that if allocation procedures are designed to be fair, disjointness is automatic. However, it must be proven: the preservation property in the definition requires that request sizes match interval sizes exactly.

**Pitfall example:** If a fragment requests size $S_i$ but receives interval size $\geq S_i$, leftover space creates ambiguity about which fragment owns it, risking overlap.

### 2. **Off-by-One Errors in Union Representation**
When representing the union of $k$ disjoint intervals as $[1, \sum S_i)$, note that:
- The interval is **half-open** (left-inclusive, right-exclusive)
- The boundary between consecutive sub-intervals is exact, with no gaps

Common mistake: writing $[1, \sum S_i]$ (closed) and later allowing the $(i+1)$-th interval to start at $\sum_{j=1}^{i} S_j + 1$ instead of the correct $\sum_{j=1}^{i} S_j$.

### 3. **Ignoring the Root Variant**
The "variant with no fragment leader" (range bottom = 1) is distinct and used specifically for slot set generation. Confusing this with the general case can lead to incorrect interval mappings when a global offset is introduced.

### 4. **Forgetting the Caching Overhead**
While $O(\log n)$ overhead per vertex is theoretically small, in practice this must be explicitly allocated. Students sometimes claim the algorithm is in-place without accounting for this auxiliary memory.

### 5. **Conflating Interval Disjointness with Fragment Disjointness**
Two fragments may be disjoint in the graph structure but receive overlapping intervals if the allocation procedure is buggy. Conversely, fragments may be adjacent in the tree but still receive properly separated intervals. These are independent properties.

## See Also

- [[interval allocation procedure]] – the algorithmic mechanism for distributing disjoint intervals
- [[convergecast]] – the tree-based aggregation pattern used to collect and distribute interval requests
- [[