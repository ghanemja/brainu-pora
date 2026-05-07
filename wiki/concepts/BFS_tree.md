# BFS Tree

## Definition

A **BFS tree** (Breadth-First Search tree) is a spanning tree of an undirected graph $G = (V, E)$ constructed by exploring vertices in order of their distance from a designated root vertex. For a graph $G$ and root $r$, the BFS tree $T$ is a subgraph where:

- $T$ is a tree spanning all vertices reachable from $r$
- Each vertex $v \in V$ has a well-defined **depth** $d(v)$ equal to the shortest path distance from $r$ to $v$
- Each non-root vertex $v$ has exactly one **parent** in $T$, which is a neighbor at depth $d(v) - 1$

In distributed computing contexts, the **BFS tree depth** $d(T) = \max_{v \in V} d(v)$ represents the height of the tree, which directly bounds the number of synchronous rounds required for tree-based communication algorithms.

## Key Equations

**Depth relationship:**
$$d(v) = \min_{u \in V} \{\text{shortest path distance from root } r \text{ to } v\}$$

**Tree depth:**
$$d(T) = \max_{v \in V} d(v)$$

**Construction complexity (synchronous distributed model):**
$$\text{Time complexity} = O(d(T)) \text{ rounds}$$
$$\text{Message complexity} = O(|E|) \text{ messages}$$

**Pipelined convergecast execution (from source material):**
$$\text{Extrinsic step time} = 2 \cdot d(T) + K$$
where $K$ is the number of fragments processed in a pipelined manner.

## Physical Intuition / Derivation

### Why BFS Trees Matter

A BFS tree imposes a **layered structure** on the graph. Think of concentric shells around the root:
- **Layer 0:** the root vertex
- **Layer $i$:** all vertices at shortest-path distance $i$ from the root
- The tree edges connect consecutive layers

This structure is valuable in distributed systems because:

1. **Predictable depth:** The depth of a BFS tree is always the diameter of the connected component in terms of shortest paths. This provides a **guaranteed bound** on communication latency.

2. **Collision avoidance in pipelined systems:** In the convergecast application described in the source material, multiple fragments perform calculations simultaneously over the same tree. By assigning each fragment a "time slot" and using the BFS tree's layered structure, information flowing up the tree from different fragments arrives at different tree levels at different times, avoiding congestion and memory conflicts.

3. **Optimal routing:** Once a BFS tree is established, routing from any vertex to the root requires at most $d(v)$ hops—provably optimal for undirected graphs.

### Construction Intuition

Standard BFS construction (in parallel/distributed settings):
- **Round 0:** Root initiates exploration
- **Round $i$:** Vertices at depth $i-1$ send discovery messages to unvisited neighbors, creating tree edges to depth-$i$ vertices
- **Termination:** After $d(T)$ rounds, all reachable vertices are incorporated

The **CONGEST model** complexity (relevant to the source material) uses $O(|E|)$ total messages because each edge is examined once, and each vertex communicates to at most $\deg(v)$ neighbors.

## Applications in Engineering

### 1. Distributed Computing & Sensor Networks
- **Data aggregation (convergecast):** BFS trees enable efficient collection of sensor readings from a distributed network to a central sink. The layered structure ensures data flows up predictably.
- **Example:** The source material applies BFS trees to pipelined convergecast calculations across multiple graph fragments.

### 2. Network Routing
- **Spanning tree protocols (e.g., RSTP - Rapid Spanning Tree Protocol):** Uses BFS-like exploration to build loop-free topologies and compute optimal paths from switch to root bridge.

### 3. Distributed Consensus & Synchronization
- **Synchronizer algorithms:** BFS trees provide known bounds on synchronization delays in asynchronous networks.

### 4. Graph Decomposition
- **Fragment coordination:** BFS trees establish a hierarchy for combining results from subgraph computations (as in the source material's multi-fragment convergecast).

### 5. Mobile & Ad-Hoc Networks
- **Neighborhood discovery:** BFS tree construction determines which nodes are reachable within $k$ hops, enabling localized algorithm design.

## Common Mistakes / Pitfalls

1. **Confusing BFS tree with shortest-path DAG:** A BFS tree is a *specific* tree; there may be multiple BFS trees for the same root (when multiple shortest paths exist). A shortest-path DAG includes all shortest-path edges. The difference matters in deterministic algorithms where tree structure must be unique.

2. **Assuming BFS tree depth equals graph diameter:** The BFS tree depth from *one* root is the eccentricity of that root, not the graph diameter. Different roots yield different depths.

3. **Ignoring weighted edges:** BFS finds shortest paths only in unweighted graphs (or graphs with unit weights). For weighted graphs, use Dijkstra-based approaches instead.

4. **Message complexity confusion in CONGEST:** A naive BFS can send $O(n)$ messages per round, giving $O(n \cdot d(T))$ total messages. However, careful implementation achieves $O(|E|)$ messages total. The source material's $O(\log n)$ message cost comes from routing label transmission, not BFS construction itself.

5. **Time-slot assignment error:** In the source material's pipelined convergecast, fragments must have *distinct* time slots to avoid collisions at tree vertices. Simply numbering fragments is necessary but not sufficient—the pipelining mechanism must respect time offsets.

## See Also

- [[Convergecast]] — aggregation of distributed data via tree structures
- [[Spanning Tree]] — tree connecting all graph vertices
- [[Distributed Graph Algorithms]] — algorithms executed on distributed network processors
- [[Tree Routing]] — routing schemes (e.g., Thorup-Zwick labels) for efficient tree-based communication
- [[CONGEST Model]] — distributed computing model with bandwidth constraints

## Sources

- **Source material:** Section 3