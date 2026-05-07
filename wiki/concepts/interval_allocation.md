# interval allocation

## Definition

**Interval allocation** is a distributed algorithm technique for assigning contiguous ranges (intervals) of resources—typically communication slots or time slots—to network vertices in a hierarchical, tree-structured network. The process operates in phases where:

1. **Demand aggregation**: Child nodes request intervals based on their subtree requirements
2. **Interval request propagation**: Aggregated demands flow upward through the hierarchy
3. **Top-level allocation**: Root nodes obtain intervals matching total subtree demand
4. **Interval distribution**: Allocated intervals are recursively subdivided and distributed downward to requesting vertices
5. **Direct delivery**: Intervals reach originating requesters through reversal of the aggregation path

The key insight is that interval allocation **traces resource requests through a virtual tree structure**, ensuring that:
- Requests are aggregated efficiently (avoiding redundant messaging)
- Allocated resources are distributed deterministically along the reverse path
- All requesters receive contiguous sub-intervals without conflicts

## Key Equations

Let $F$ denote a fragment (a set of related vertices), and $r_F$ its leader vertex.

**Demand aggregation:**
$$\text{size\_request}(F) = \text{size}(F) + \sum_{C \in \text{children}(F)} \text{size\_request}(C)$$

where $\text{size}(F)$ is the number of base fragments or subsets contained in $F$, and the sum ranges over all child fragments of $F$ in the virtual subtree.

**Interval distribution (reservation):**
$$\text{reserved}(F) = \text{interval\_received}(F)[0:\text{size}(F))$$

where $[0:\text{size}(F))$ denotes the sub-interval from position 0 to position $\text{size}(F)-1$ of the interval received by $r_F$.

**MWOE-based request propagation:**
$$\text{incoming\_request}(B) = \sum_{\text{adjacent } v \text{ via MWOE edges}} \text{request}(v)$$

where $B$ is a base fragment and the sum aggregates interval requests from all vertices in parent fragments adjacent to $B$ via Minimum-Weight Outgoing Edge (MWOE) connections.

## Physical Intuition / Derivation

### Why Interval Allocation?

In distributed networks, many problems require assigning unique, contiguous identifiers (slots, time windows, channel IDs) to vertices without central coordination. Naive approaches—where each vertex requests directly from a global allocator—create bottlenecks and require $O(n)$ messages. Interval allocation achieves $O(\log n)$ or $O(n \log n)$ message complexity by:

**Aggregating demand hierarchically:**
- A subtree of 1000 vertices doesn't generate 1000 separate requests
- Instead, a single "fragment leader" aggregates and requests one large interval
- The root of the tree obtains one interval covering all descendants

**Distributing recursively:**
- The root breaks its interval into pieces for each child subtree
- Each child leader does the same, recursing until individual vertices are reached
- This mirrors the **aggregation path in reverse**, guaranteeing:
  - Correctness: each requester receives exactly what was requested
  - Efficiency: $O(d)$ rounds where $d$ is tree depth, not $O(n)$ rounds

### The Four-Step Process

**Step 1—Aggregation (Ready broadcasts):**
Each fragment $F$ announces readiness and publishes its total demand size. This is cached locally; no intervals are allocated yet.

**Step 2—Upward propagation:**
Designated leaders (roots of virtual subtrees) initiate allocation cycles:
- They request intervals matching $\text{size\_request}(\text{subtree})$
- The first slot of each received interval becomes the leader's **p-slot** (personal slot)
- Remaining slots are reserved for distribution to descendants

**Step 3—Downward distribution (mirroring):**
Each fragment root distributes its interval among descendants in **three iterations** (matching the depth-3 bound of virtual subtrees). At each level:
- **Reservation**: Leader reserves $\text{size}(F)$ slots for fragment $F$ itself
- **Interval allocation**: Allocation cycles assign intervals to sub-fragments based on cached demand sizes
- **Broadcast & convergcast**: Intervals propagate down; confirmations flow up

**Step 4—Final delivery via MWOE edges:**
MWOE-adjacent vertices in child fragments receive their allocated intervals via direct edge exchanges with parent fragments, ensuring low latency.

## Applications in Engineering

### 1. **Distributed Scheduling & Resource Allocation**
- **Problem**: Allocate time slots to transmitters in ad-hoc wireless networks without global clock
- **Solution**: Interval allocation provides each vertex a unique, contiguous set of slots via the network hierarchy
- **Benefit**: Avoids collisions and coordination overhead

### 2. **Channel Assignment in Cognitive Radio Networks**
- **Problem**: Assign frequency channels to secondary users without interfering with primary spectrum users
- **Solution**: Use interval allocation to partition channel ranges (intervals) hierarchically
- **Benefit**: Scales to thousands of nodes; adapts as network topology changes

### 3. **Parallel Algorithm Execution on Cluster Networks**
- **Problem**: Assign process IDs or memory addresses to parallel tasks on a tree-structured cluster
- **Solution**: Interval allocation ensures contiguous ID ranges for tasks in each subclusters
- **Benefit**: Simplifies inter-process communication patterns; enables efficient broadcasting

### 4. **Distributed Data Structure Labeling**
- **Problem**: Assign unique labels to tree vertices for distance queries, lowest-common-ancestor (LCA) queries
- **Solution**: Interval allocation assigns Euler tour positions or preorder/postorder labels
- **Benefit**: Enables $O(1)$ LCA and distance queries after $O(\log n)$ setup rounds

### 5. **Fair Bandwidth Allocation in Multi-hop Networks**
- **Problem**: Allocate transmission opportunities fairly across multi-hop paths
- **Solution**: Interval allocation ensures each link or path gets proportional bandwidth slots
- **Benefit**: Prevents starvation; distributes resources based on demand

## Common Mistakes / Pitfalls

### 1. **Conflating aggregation with allocation**
**Error**: Assuming that publishing