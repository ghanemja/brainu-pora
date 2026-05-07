# fragment leader upcasting

## Definition

**Fragment leader upcasting** is a distributed algorithm procedure in which designated leader vertices of fragments (subtrees in a hierarchical decomposition) collect aggregated slot or interval requests from their constituent components and transmit these requests upward through a tree hierarchy to a root authority. The leader then receives a globally unique interval allocation and distributes it back down to base fragments.

More formally: given a set of fragments $\{F_1, F_2, \ldots, F_k\}$ with designated leader vertices $\{\ell_1, \ell_2, \ldots, \ell_k\}$, fragment leader upcasting enables each leader $\ell_i$ to:
1. **Converge** slot requests from all subsets and base fragments in its subtree
2. **Upcast** an aggregated request of size $S_i$ to a root authority $r_T$
3. **Receive** a disjoint interval allocation $I_i$ from the global range $[1, \sum_{j=1}^{k} S_j)$
4. **Distribute** the interval back to constituent fragments

## Key Equations

**Disjoint interval property:** If fragments $F_1, F_2, \ldots, F_k$ have disjoint initial intervals and request sizes $S_1, S_2, \ldots, S_k$ matching their interval capacities, then allocated intervals remain disjoint:

$$I_i \cap I_j = \emptyset \quad \forall i \neq j$$

**Union coverage:** When a fragment leader upcasts with range bottom = 1, the union of all allocated intervals covers a contiguous range:

$$\bigcup_{i=1}^{k} I_i = \left[1, \sum_{i=1}^{k} S_i\right)$$

**Memory requirement:** Caching partial sums along upcasting paths requires:

$$O(\log n) \text{ bits per vertex}$$

where $n$ is the total number of vertices in the system.

## Physical Intuition / Derivation

### Hierarchical Slot Allocation Problem

In distributed systems (particularly BFS-tree-based algorithms), fragments need disjoint slots or intervals to perform subsequent computations. The challenge is to:
- Avoid duplication (two fragments receive overlapping slots)
- Minimize communication overhead
- Enable request tracing for correctness verification

### The Upcasting Approach

Rather than having each fragment independently request from a global authority (creating $O(k)$ messages), fragment leaders **aggregate** requests within their subtree and make a single request upward. This reduces message complexity while maintaining correctness.

**Key insight:** By eliminating fragment leader upcasting of a range bottom (setting range bottom = 1), the algorithm guarantees that disjoint input intervals remain disjoint after allocation. This invariant holds because:
- No overlap exists in the output range $[1, \sum S_i)$
- Each fragment receives exactly $S_i$ consecutive slots
- Allocation order preserves disjointness

### Request Tracing Mechanism

The algorithm must later retrace which requests contributed to which allocations. To enable this without excessive memory:
- **Convergecast steps** (direct child-to-parent communication on base fragments) and **extrinsic convergecast steps** (pipelined communication over BFS tree $T$) are intermixed
- Intermediate vertices cache partial sums along the path
- $O(\log n)$ bits per vertex is sufficient to store path information plus aggregated request sizes

## Applications in Engineering

### 1. **Distributed Memory Allocation**
In parallel computing systems, fragments (processor groups) use leader upcasting to request memory blocks. The root authority allocates disjoint memory regions, preventing cache conflicts and ensuring spatial locality.

### 2. **Network Time-Slot Allocation**
In wireless networks, fragments representing clusters request transmission time slots from a centralized scheduler. Upcasting prevents collisions while minimizing control message overhead.

### 3. **Graph Algorithm Acceleration**
In BFS-tree-based distributed graph algorithms (e.g., connected components, diameter approximation), fragments need disjoint work queues or buffer ranges. Fragment leader upcasting assigns them efficiently.

### 4. **Resource Scheduling in Cloud Computing**
Virtual machines organized hierarchically (by availability zone, rack, node) use fragment leader upcasting to request CPU cores, GPU slots, or I/O channels from a cluster controller.

### 5. **Data Structure Partitioning**
When building distributed hash tables or suffix trees, fragments request disjoint index ranges through leader upcasting to avoid secondary lookups.

## Common Mistakes / Pitfills

### 1. **Forgetting the Disjointness Invariant**
**Mistake:** Assuming disjoint intervals at the start remain disjoint without setting range bottom = 1.

**Pitfall:** If the range bottom is not fixed at 1, overlapping allocations can occur if some fragments are inactive or request fewer slots than expected.

**Correct approach:** Explicitly zero the range bottom before upcasting, or ensure all participating fragments have synchronized interval capacities.

### 2. **Ignoring Request Tracing Overhead**
**Mistake:** Not caching partial sums, then later attempting to reconstruct which requests contributed to each allocation.

**Pitfall:** This requires $O(k)$ additional memory per vertex or $O(n)$ global memory, violating efficiency goals.

**Correct approach:** Cache $O(\log n)$ bits per vertex representing cumulative request sizes up to that vertex.

### 3. **Mixing Intrinsic and Extrinsic Convergecast Incorrectly**
**Mistake:** Allowing intrinsic convergecast (on base fragments) and extrinsic convergecast (on BFS tree) to interleave without proper synchronization.

**Pitfall:** Requests may be duplicated, lost, or attributed to wrong fragments.

**Correct approach:** Follow Claim 5.3 rigorously; explicitly define which vertices perform which type of convergecast at each step (see Table 2 in source).

### 4. **Over-Aggregating Requests**
**Mistake:** Summing all requests at intermediate leaders without preserving request-origin information.

**Pitfall:** Cannot reconstruct which subset made which request; violates the requirement to "trace back requests to origin."

**Correct approach:**