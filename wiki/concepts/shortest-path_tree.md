# shortest-path tree

## Definition

A **shortest-path tree (SPT)** rooted at a source vertex $p_0$ is a subgraph $T$ of a graph $G = (V, E)$ that:

1. Forms a tree (connected, acyclic subgraph)
2. Contains $p_0$ as its root
3. For every vertex $v \in V$, the unique path from $p_0$ to $v$ in $T$ is a shortest path in $G$

The tree connects the root to all other vertices (or at least all reachable vertices) while preserving shortest-path distances. Formally, for any vertex $v$:
$$d_T(p_0, v) = d_G(p_0, v)$$

where $d_T$ and $d_G$ denote distances in the tree and original graph, respectively.

## Key Equations

**Distance preservation property:**
$$\text{For all } v \in V: \quad d_T(p_0, v) = d_G(p_0, v)$$

**Tree property:**
$$|E(T)| = |V(T)| - 1$$

**Implicit edge direction:** Each edge $e \in T$ can be oriented according to the shortest path from $p_0$ through that edge to terminal $p_i$:
$$\text{edge } e \text{ lies on path } \pi: p_0 \to \cdots \to p_i$$

## Physical Intuition / Derivation

Think of a shortest-path tree as a **navigation blueprint** from a source location to all destinations. Rather than computing separate optimal routes to each destination independently, an SPT exploits the structure that optimal paths naturally share edges—particularly near the source.

### Why Trees?

The tree structure arises because:
- **No cycles are needed:** If a cycle existed in a shortest-path graph, you could remove the longest edge of that cycle without breaking distance guarantees (this is Claim 31 in the source material). This iterative elimination of cycles reduces any distance-preserving subgraph to a tree.
- **Uniqueness of parent:** For any vertex $v$ at distance $d$ from $p_0$, the immediate predecessor in a shortest path may not be unique, but selecting *any one* predecessor for the tree maintains optimality.

### Construction Intuition

When building an SPT (e.g., via Dijkstra's algorithm):
1. Start at $p_0$ with distance 0
2. Greedily add nearest unvisited vertices, recording the edge that reached them
3. Each added edge becomes part of the tree—it connects a newly discovered vertex to the already-explored portion
4. The result is automatically acyclic and distance-preserving

### Monotonicity and Directionality

In geometric settings (as in the source material), edges of an SPT can be **implicitly directed** from $p_0$ toward terminals. A key structural insight: if an edge is oriented *away* from $p_0$ along any shortest path, removing it disconnects the root from some terminal. Conversely, an edge oriented *toward* $p_0$ contradicts optimality and can be eliminated.

## Applications in Engineering

### 1. **Network Routing & Telecommunications**
   - **IP routing protocols** (OSPF, IS-IS) compute SPTs to minimize hop count or latency from a central router to all others
   - Reduces routing table size while maintaining optimal paths

### 2. **Robotics & Path Planning**
   - Constructing SPTs in configuration space enables a robot to reach all target poses optimally
   - Single computation replaces repeated point-to-point path searches

### 3. **Road Networks & Transportation**
   - GPS navigation systems compute SPTs from landmarks/hubs to enable efficient rerouting
   - Emergency response networks use SPTs to minimize response time from stations to all service areas

### 4. **Electrical Grid / Power Distribution**
   - Minimizing total wire length while ensuring all substations are reachable from a central source
   - SPTs reduce infrastructure cost while maintaining redundancy-free operation

### 5. **Facility Location & Supply Chain**
   - Optimal placement of distribution hubs with SPT connections to minimize total transportation distance
   - Reduces inventory handling and logistics cost

### 6. **Graph Compression & Distance Preservers**
   - As shown in the source material, SPTs are minimal subgraphs that preserve all distances from a root
   - Used in parameterized complexity studies (IRSA ↔ IPDP equivalence) to reduce problem size

## Common Mistakes / Pitfalls

### 1. **Confusing SPT with Minimum Spanning Tree (MST)**
   - **SPT:** Optimizes distances *from a root* to all other vertices
   - **MST:** Optimizes total edge weight over the entire graph with no designated root
   - An MST may violate distance guarantees from any single source

### 2. **Non-uniqueness Misunderstanding**
   - Multiple valid SPTs may exist (when there are ties in shortest-path distances)
   - Choosing different edges at tie-breakers creates different valid trees
   - Students mistakenly assume "the" SPT is unique

### 3. **Forgetting Connectivity Constraints**
   - An SPT only includes reachable vertices from $p_0$
   - In disconnected graphs, the SPT may not span all vertices
   - Must verify strong connectivity or specify reachability domain

### 4. **Confusing SPT with All-Pairs Shortest Paths**
   - An SPT only preserves distances from a *single root* $p_0$
   - Computing shortest paths for multiple sources requires separate SPTs or algorithms like Floyd-Warshall
   - The source material's equivalence (IRSA ↔ IPDP) exploits this: pairwise distances are checked via a rooted SPT

### 5. **Overhead of Recomputation**
   - Students sometimes assume an SPT can be reused unchanged when the graph changes
   - Edge weight modifications require recomputation; structural queries must be re-validated
   - Incremental SPT maintenance is a non-trivial problem

### 6. **Ignoring Geometric Constraints**
   - In planar/geometric settings (source material), SPTs have additional structure (monotonicity, acyclicity)
   - Assuming general graph properties may