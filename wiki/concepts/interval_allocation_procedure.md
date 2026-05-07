# interval allocation procedure

## Definition

The **interval allocation procedure** is a distributed algorithm mechanism for assigning disjoint contiguous intervals of resources (slots, identifiers, memory ranges) to multiple fragments or components in a hierarchical tree-structured system. It operates in a coordinated, conflict-free manner where:

- Multiple fragments simultaneously request intervals of specified sizes
- Requests are aggregated through a tree hierarchy (typically a BFS tree)
- A root authority allocates non-overlapping intervals from a global range
- Allocated intervals are propagated back down the tree to requesting fragments
- Each fragment receives an interval whose size matches its request, with no overlap between fragments

The procedure guarantees that if input intervals held by fragments are disjoint and request sizes match available interval sizes, then output intervals at the end of the allocation cycle remain disjoint.

## Key Equations

Let $V = \{v_1, v_2, \ldots, v_k\}$ be vertices (fragments) requesting intervals with sizes $S_1, S_2, \ldots, S_k$.

**Allocation invariant:**
$$\bigcap_{i \neq j} I_i = \emptyset \quad \text{(disjointness)}$$

**Union coverage (simplified variant with base range 1):**
$$\bigcup_{i=1}^{k} I_i = \left[1, \sum_{i=1}^{k} S_i\right)$$

where $I_i$ is the interval allocated to fragment $v_i$.

**Range bound:**
For global range $[1, 2^{K_b}]$ where $K_b$ is a capacity parameter, each leader receives a distinct sub-interval such that total allocated size $\leq 2^{K_b}$.

## Physical Intuition / Derivation

### Why This Procedure Matters

Imagine distributing a contiguous resource (like memory addresses, time slots, or identifier ranges) among multiple independent components that don't have global knowledge. A naive approach—allowing each component to self-assign—leads to collisions. The interval allocation procedure solves this through **hierarchical negotiation**:

1. **Bottom-up aggregation (convergecast):** Requests bubble upward through fragment leaders, collecting counts of how many slots each subtree needs
2. **Top-down distribution:** The root allocates disjoint intervals to each subtree leader
3. **Recursive subdivision:** Each leader subdivides its interval among child fragments, ensuring no overlaps

### The Two-Phase Process

**Intrinsic convergecast (local):**
Direct communication within base fragments—child fragments ping parents to report their slot needs.

**Extrinsic convergecast (global):**
Pipelined aggregation through the BFS tree $T_a$, where partially aggregated requests travel upward with **caching at intermediate vertices** to enable later path reconstruction.

### Tracing and Reconstruction

A critical engineering challenge: how do we trace a request back to its origin after multi-hop aggregation?

**Solution:** Intermediate vertices along the request path cache:
- The aggregated request they received from children
- The aggregated request they sent upward

This forms a "breadcrumb trail" requiring only $O(\log n)$ bits per vertex in additional memory, enabling downstream systems to determine which base fragments should receive which portion of an allocated interval.

## Applications in Engineering

### 1. **Distributed Memory Allocation**
In cluster computing and shared-memory systems, the interval allocation procedure assigns contiguous address ranges to compute nodes without global synchronization, enabling each node to manage local memory independently.

### 2. **Slot Scheduling in Wireless Networks**
Base stations (fragments) collectively request transmission time slots from a network coordinator. The procedure ensures each station receives a conflict-free, contiguous temporal interval.

### 3. **ID/Token Generation in Distributed Systems**
Assigning unique identifier ranges to different processes or microservices in a large-scale system (e.g., Zookeeper-style ID generation, distributed sequence generation).

### 4. **Resource Partitioning in Multi-tenant Systems**
Cloud platforms partitioning CPU quota, storage capacity, or network bandwidth among tenant groups in a hierarchical organizational structure.

### 5. **BFS Tree-Based Distributed Computing**
Used as a subroutine in locality-aware algorithms on tree topologies, where each subtree must independently coordinate resource needs without global overhead.

## Common Mistakes / Pitfalls

### 1. **Assuming Intervals Can Overlap If Requests Are Ordered**
❌ **Wrong:** "If we process requests sequentially, overlaps will be prevented."
✓ **Correct:** The power of this procedure is **concurrent, non-blocking allocation**—multiple fragments request simultaneously without waiting, yet disjointness is guaranteed by the hierarchical structure itself.

### 2. **Conflating Request Size with Allocated Size**
❌ **Wrong:** Assuming a fragment requesting size $S_i$ might receive an interval of different size.
✓ **Correct:** The procedure enforces the invariant that allocated interval size = requested size exactly.

### 3. **Losing Track of the BFS Tree Topology**
❌ **Wrong:** Treating the procedure as "just a sorting algorithm" for size-ordered allocation.
✓ **Correct:** The tree structure is **essential**—it determines communication paths, convergecast hierarchies, and parent-child aggregation layers. Different tree structures yield different caching and communication costs.

### 4. **Ignoring Caching Overhead**
❌ **Wrong:** Dismissing caching as negligible.
✓ **Correct:** While per-vertex overhead is $O(\log n)$ bits, the tracing capability is a complex system property. Improper caching placement breaks request retraceability.

### 5. **Assuming Global Synchronization Is Needed**
❌ **Wrong:** "To guarantee disjointness, all fragments must synchronize at a barrier."
✓ **Correct:** The procedure works **asynchronously within each cycle**—synchronization is implicit in the tree topology and convergecast scheduling, not a global barrier.

## See Also

- [[Convergecast]] — the upward aggregation phase underlying request collection
- [[BFS tree]] — the hierarchical topology enabling distributed coordination
- [[Distributed resource allocation]] — broader class of algorithms for conflict-free resource sharing
- [[Fragment and subset hierarchies]] — the logical decomposition enabled by interval allocation
- [[Path retracing in distributed systems]] —