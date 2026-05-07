# Euler's theorem

## Definition

**Euler's theorem** is a foundational result in graph theory that characterizes when a graph contains an **Eulerian trail** (a path traversing every edge exactly once) or an **Eulerian cycle** (a closed trail traversing every edge exactly once).

### Formal Statement

For a connected directed graph $G = (V, E)$:

- An **Eulerian cycle** exists if and only if every vertex $v$ satisfies $\delta^+(v) = \delta^-(v)$ (in-degree equals out-degree)
- An **Eulerian trail** exists if and only if:
  - Either an Eulerian cycle exists, OR
  - There exists exactly one vertex $s$ (the source) with $\delta^+(s) = \delta^-(s) + 1$ and exactly one vertex $t$ (the sink) with $\delta^-(t) = \delta^+(t) + 1$, with all other vertices satisfying $\delta^+(v) = \delta^-(v)$

For **undirected connected graphs**:
- An Eulerian cycle exists iff all vertices have even degree
- An Eulerian trail exists iff exactly zero or two vertices have odd degree

### Key Parameters

- $\delta^+(v)$ = out-degree of vertex $v$ (number of edges leaving $v$)
- $\delta^-(v)$ = in-degree of vertex $v$ (number of edges entering $v$)
- $m$ = number of edges
- $z_T$ = total number of distinct Eulerian trails

## Key Equations

The condition for an Eulerian cycle in a directed graph:
$$\forall v \in V: \quad \delta^+(v) = \delta^-(v)$$

The condition for an Eulerian trail in a directed graph with source $s$ and sink $t$:
$$\delta^+(s) = \delta^-(s) + 1, \quad \delta^-(t) = \delta^+(t) + 1, \quad \forall v \notin \{s,t\}: \delta^+(v) = \delta^-(v)$$

For undirected graphs, counting vertices with odd degree $\text{odd}(G)$:
- Eulerian cycle exists: $\text{odd}(G) = 0$
- Eulerian trail exists: $\text{odd}(G) \in \{0, 2\}$

## Physical Intuition / Derivation

### Why Degree Balance Matters

Think of vertices as intersections and edges as roads:
- **In-degree** = how many roads lead *into* the intersection
- **Out-degree** = how many roads lead *out of* the intersection

If you traverse every road exactly once:
- At each intermediate stop, every time you enter via a road, you must exit via a different road
- This forces in-degree = out-degree at all but (possibly) start and end vertices

**Traversal argument:** 
- Each time an edge is used to enter a vertex, we must eventually use a different edge to exit it
- At the start vertex $s$, we may have one "extra" outgoing edge (we start here without entering)
- At the end vertex $t$, we may have one "extra" incoming edge (we finish here without leaving)
- All other vertices must have perfect balance

### Verification Complexity

Checking Euler's conditions requires only examining degree sequences:
- Compute in- and out-degrees: $O(m)$ time
- Compare against conditions: $O(|V|)$ time
- **Total:** $O(m)$ time

This is vastly faster than explicitly searching for trails.

### Hierholzer's Algorithm Connection

Once Euler's conditions are verified, [[Hierholzer's algorithm]] constructs an actual Eulerian trail in $O(m)$ time by:
1. Starting at the designated source vertex
2. Greedily following available edges, backtracking when stuck
3. The degree-balance guarantee ensures completion without getting trapped

## Applications in Engineering

### Network Routing & Traversal

- **Street sweeping / garbage collection:** Find a route covering every street exactly once. Euler's theorem determines feasibility; the city's street graph must satisfy degree conditions.
- **Postal delivery:** Rural post carrier problem (Chinese postman variant) requires modifying graphs to satisfy Eulerian conditions when they don't naturally exist.
- **Utility inspection:** Gas line or water pipe networks need inspection routes visiting every segment once.

### Electrical Engineering

- **Circuit design validation:** Ensure test signals can traverse every wire in a circuit exactly once
- **PCB routing:** Determine if traces can be routed following Eulerian paths

### DNA Sequencing

- **Genome assembly:** Short DNA reads can be arranged in Eulerian trails through a de Bruijn graph (edges = k-mers)
- This approach revolutionized sequence assembly by reducing exponential to linear complexity

### Manufacturing & Robotics

- **Robot arm programming:** Minimize tool repositioning by finding paths that service all points/edges efficiently
- **Weld seam coverage:** Verify welding paths can traverse all seams without retracing

### Software Testing

- **Code coverage paths:** Identify if test cases can execute every edge (branch) in a control-flow graph exactly once

## Common Mistakes / Pitfalls

### 1. **Confusing Degree Conditions with Existence**
Students often think "the graph *looks* connected" implies an Eulerian trail exists. **Mistake:** You must verify the specific degree conditions, not just connectivity.

### 2. **Forgetting Connectivity Requirement**
Euler's conditions are *necessary* but *insufficient* without connectivity.
- **Correct statement:** A connected graph has an Eulerian cycle iff all vertices have even degree
- **Wrong:** "If all vertices have even degree, an Eulerian cycle exists" (fails on disconnected graphs)

### 3. **Mixing Directed & Undirected Conditions**
The degree conditions differ significantly:
- **Undirected:** Check total degree (in + out together)
- **Directed:** Check in-degree and out-degree separately
Applying undirected logic to directed graphs or vice versa gives incorrect results.

### 4. **Miscounting Odd-Degree Vertices**
In undirected graphs, the handshaking lemma guarantees an even number of odd-degree vertices. An