# Breadth-First Search (BFS) tree

## Definition

A **Breadth-First Search (BFS) tree** is a spanning tree of a graph constructed by exploring vertices in order of their distance from a designated root vertex. Specifically:

- Start from a root vertex $r$
- Visit all vertices at distance 1 from $r$, then all at distance 2, and so on
- Edges connecting each vertex to the vertex that discovered it form the tree edges
- The tree has depth equal to the diameter of the component being explored

In the context of distributed minimum spanning tree (MST) algorithms, the BFS tree serves as an **auxiliary communication structure** that enables efficient hierarchical information aggregation and cycle detection without explicit global coordination.

## Key Equations

**Depth of BFS tree:**
$$\text{depth}(T) = \text{diam}(G)$$

where $\text{diam}(G)$ is the graph diameter.

**Memory per vertex for subtree representation:**
$$\text{Memory}_v = O\left(\sqrt{n}\right)$$
for storing virtual fragments and edges in pipelined MST algorithms.

**Time complexity for phase-based aggregation:**
$$\text{Time per round} = O(\text{depth}(T)) = O(\text{diam}(G))$$

## Physical Intuition / Derivation

### Why BFS Trees in Distributed MST?

In centralized MST algorithms (e.g., Kruskal's), we maintain global state. In distributed settings, we need a **hierarchy** to:

1. **Reduce message complexity**: Rather than broadcast to all $n$ vertices, aggregate information bottom-up
2. **Enable pipelining**: Vertices at different depths can work simultaneously without conflicts
3. **Facilitate cycle detection**: The tree structure lets each vertex maintain local subtree state to filter edges that would create cycles

### Construction and Role in GKP Pipeline

The BFS tree $T$ is constructed from an arbitrary root. Each vertex $v$ then:

- Maintains a representation of the subtree it has already processed (O($\sqrt{n}$) memory in practice)
- **Upcasts** candidate edges from children, ordered by weight
- Filters edges that would create cycles with previously-upcast edges in its subtree
- MST edges naturally reach the root first because:
  - Edges are sent in increasing weight order
  - Non-MST edges create cycles and are filtered locally

This leverages the **key insight**: once an MST edge is identified, it will be in any minimum spanning tree; non-MST edges will always create cycles with existing tree edges and can be safely discarded without reaching the root.

## Applications in Engineering

### 1. **Distributed Network Algorithms**
- Constructing MSTs in distributed systems where no central coordinator exists
- Used in spanning tree protocols (IEEE 802.1D) for network loop prevention
- Enabling efficient multi-source aggregation queries

### 2. **Parallel MST Computation (GKP Algorithm)**
- The **Gallager-Humblet-Spira (GKP) pipeline procedure** uses BFS trees as scaffolding
- Fragments (connected components) upcast MWOE (Minimum Weight Outgoing Edge) candidates
- Root makes global decisions with reduced message overhead

### 3. **Telecommunication Networks**
- Coordinating network reconfiguration without service disruption
- Broadcast and multicast tree construction

### 4. **Wireless Sensor Networks**
- Efficient data collection from distributed sensors
- Reducing energy consumption through hierarchical communication

### 5. **Distributed Cycle Detection**
- Each vertex stores only its local upcast subtree history
- Non-MST edges detected locally without global state

## Common Mistakes / Pitfalls

### 1. **Confusing BFS tree with the final MST**
The BFS tree $T$ is a **communication scaffold**, not the output. The final MST is constructed by filtering edges upcast through $T$ based on weight and cycle properties.

### 2. **Assuming arbitrary spanning tree equivalence**
Not all spanning trees are equally efficient for message-passing. BFS trees minimize depth ($O(\log n)$ in well-structured networks), reducing aggregation latency. Depth-first trees can have $O(n)$ depth.

### 3. **Underestimating memory for subtree representation**
- Naive approach: store all edges in subtree → $O(n)$ memory per vertex ❌
- Correct approach: store only the **virtual fragment structure** and edge weights → $O(\sqrt{n})$ with careful representation
- The "representation" is a compressed form showing connectivity of virtual fragments, not individual edges

### 4. **Ignoring root selection**
In practical systems, the root choice affects tree structure and algorithm performance. Poorly chosen roots can create unbalanced trees with large depth.

### 5. **Message ordering misconception**
Edges must be upcasted in **increasing weight order** for the pipelining property to work. Random ordering breaks the guarantee that MST edges reach the root first and defeats the cycle-filtering mechanism.

## See Also

- [[Minimum Spanning Tree (MST)]]
- [[Gallager-Humblet-Spira (GKP) Algorithm]]
- [[Minimum Weight Outgoing Edge (MWOE)]]
- [[Distributed Graph Algorithms]]
- [[Graph Coloring and Fragment Merging]]

## Sources

- Distributed MST Pipeline Procedure (Lenzen [41], sections referencing [24, 40])
- Time, Message and Memory-Optimal Distributed Minimum Spanning Tree algorithms (appendices A.2–A.4)
- GKP phase implementations with diameter-based fragment filtering
- Message-efficient MWOE candidate aggregation structures