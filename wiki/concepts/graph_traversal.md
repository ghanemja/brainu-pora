# Graph Traversal

## Definition

**Graph traversal** is a systematic process of visiting all vertices (nodes) and edges in a graph, following a well-defined strategy to explore the graph structure. The process visits each node at most once and determines the order and manner in which edges are explored.

In the context of **Eulerian trails**, graph traversal becomes more specialized: an Eulerian trail is a path that traverses every edge in a graph exactly once. A graph admits an Eulerian trail if and only if:
- It is connected (or weakly connected for directed graphs), AND
- It has exactly 0 or 2 vertices of odd degree (for undirected graphs), OR
- It has at most one vertex with in-degree ≠ out-degree and at most one with out-degree ≠ in-degree (for directed graphs)

## Key Equations

**Euler's Degree Criterion** (for directed graphs):
$$\text{in-degree}(v) = \text{out-degree}(v) \quad \forall v \in V \quad \Rightarrow \quad \text{Eulerian cycle exists}$$

**State Tree Construction Time Complexity** (Theorem 4.3):
$$T(G, z) = O(m \cdot \min(z, z_T))$$

where:
- $m$ = number of edges
- $z$ = number of requested Eulerian trails
- $z_T$ = total number of Eulerian trails in graph $G$

**Detection of Crossing Edges** (Lemma 4.2):
For a trail $R = e_1, e_2, \ldots, e_k$ in graph $H$, an edge $e_i$ is a **crossing edge** (bridges between strongly connected components) if and only if it is the last out-edge at its source vertex with respect to the trail ordering.

## Physical Intuition / Derivation

### Historical Context: Hierholzer's Algorithm

Graph traversal for Eulerian trails builds on **Hierholzer's algorithm**, which efficiently constructs Eulerian paths by:

1. **Starting from any vertex** and following edges arbitrarily until returning to the starting point (forming a cycle)
2. **Finding unvisited edges** at any vertex on the partial trail
3. **Recursively constructing sub-trails** from those vertices
4. **Splicing together** the sub-trails into the main trail

### Why Crossing Edge Detection Matters

The key insight from the source material is that we can efficiently enumerate *multiple* Eulerian trails by:

1. **Identifying branching points**: states where the traversal has multiple valid continuations
2. **Computing crossings on-the-fly**: Rather than storing all crossing edges globally, we identify them locally as "last out-edges" in the current trail order
3. **Reusing computation**: The state tree structure allows sharing of common trail prefixes between different Eulerian trails

**Why last out-edges are crossings:**
- When we reach the *last* out-edge from vertex $v$ in our current trail, all other outgoing edges from $v$ have already been used
- To complete the Eulerian trail, we must eventually leave the current strongly connected component (SCC) containing $v$
- Therefore, the last out-edge necessarily crosses SCC boundaries
- Conversely, non-last out-edges cannot be crossings, because the algorithm must eventually return to $v$ to use its remaining edges

### Time Complexity Intuition

The $O(m \cdot \min(z, z_T))$ complexity arises because:
- Constructing the entire state tree requires traversing edges across all possible Eulerian trails: $O(m \cdot z_T)$
- When $z < z_T$, DFS can terminate early after finding $z$ trails: $O(m \cdot z)$
- Compression (Section 5) eliminates redundant subtrees by sharing common prefixes, improving constants

## Applications in Engineering

### 1. **Network Routing & Postman Problems**
- **Chinese Postman Problem**: Finding the shortest closed walk that traverses every edge at least once
- **Application**: Garbage collection routes, street sweeping, utility line inspection
- **Use case**: Minimizing vehicle travel distance when all edges must be serviced

### 2. **Bioinformatics: DNA Sequencing**
- **De Bruijn graphs**: Nodes represent short DNA sequences (k-mers), edges represent overlaps
- **Eulerian paths enumerate valid genomic sequences** consistent with observed fragments
- **Efficiency**: Multiple Eulerian trails correspond to different possible genome reconstructions

### 3. **Power Grid Analysis**
- **Connectivity verification**: Ensure all components remain weakly connected after failures
- **Traversal-based diagnostics**: Detect disconnected subsections in electrical networks
- **Application**: Critical infrastructure resilience testing

### 4. **Compiler Design & Program Verification**
- **Control flow graphs**: Vertices = basic blocks, edges = control transfers
- **Path enumeration**: Finding all execution paths for test coverage analysis
- **Eulerian techniques**: Detect unreachable code or unused branches

### 5. **Logistics & Optimization**
- **Vehicle routing with mandatory segments**: When all roads in a service area must be traversed
- **State-space exploration**: Enumerating feasible delivery sequences
- **Application**: Last-mile delivery optimization

## Common Mistakes / Pitfalls

### 1. **Confusing Necessary and Sufficient Conditions**
- **Error**: Assuming a connected graph always has an Eulerian trail
- **Correction**: Connectivity is *necessary* but not *sufficient*; degree constraints must also hold
- A connected graph with all vertices of even degree has an Eulerian *cycle*, but a trail through all edges may not exist

### 2. **Overlooking Weak vs. Strong Connectivity**
- **Error**: In directed graphs, treating strong connectivity as equivalent to weak connectivity
- **Correction**: Eulerian trails require only *weak* connectivity (ignoring edge direction), not strong connectivity
- A directed graph can have an Eulerian trail while remaining strongly disconnected

### 3. **Miscounting Crossings**
- **Error**: Assuming all edges leaving an SCC are crossings
- **Correction**: Only the *last* out-edge (in trail order) at each vertex is a crossing
- Non-final out-edges must eventually return to the same vertex, staying within local structure

### 