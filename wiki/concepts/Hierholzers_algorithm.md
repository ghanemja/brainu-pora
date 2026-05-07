# Hierholzer's Algorithm

## Definition

**Hierholzer's algorithm** is a greedy, linear-time procedure for constructing an **Eulerian trail** or **Eulerian circuit** in a graph. An Eulerian trail is a walk that traverses every edge of a graph exactly once; an Eulerian circuit is an Eulerian trail that begins and ends at the same vertex.

The algorithm operates on a directed graph $G = (V, E)$ where an Eulerian circuit exists if and only if:
- Every vertex has equal in-degree and out-degree, and
- All vertices with nonzero degree belong to a single strongly connected component.

An Eulerian trail exists when exactly zero or two vertices have unequal in/out degrees.

## Key Equations

**Time Complexity:**
$$T_{\text{Hierholzer}} = O(|E|) = O(m)$$

where $m$ is the number of edges.

**Space Complexity:**
$$S = O(|V| + |E|) = O(n + m)$$

**For enumeration of all Eulerian trails** in a graph:
$$T_{\text{enum}} = O(m \cdot z_T)$$

where $z_T$ is the total number of distinct Eulerian trails.

**Compressed state tree size** (with compression rules):
$$|\text{State Tree}_{\text{compressed}}| = O(m + z_T)$$

## Physical Intuition / Derivation

### Core Mechanism

Hierholzer's algorithm builds an Eulerian trail by following edges greedily, maintaining a stack of vertices:

1. **Start** at an arbitrary vertex (or a specified starting vertex)
2. **Follow edges** arbitrarily from the current vertex, removing each edge as it is traversed
3. **When stuck** (no outgoing edges remain), backtrack and record the current vertex
4. **Continue** with unexplored edges from the backtracked vertex
5. **Reverse** the recorded sequence to obtain the Eulerian trail

### Why It Works

The algorithm exploits a fundamental property: once a vertex has no outgoing edges remaining, it cannot be visited again (in a connected graph satisfying Eulerian conditions). Thus, vertices can be finalized in a **postorder traversal** of the implicit DFS tree, and reversing this order yields a valid Eulerian trail.

### Intuitive Picture

Imagine a network of one-way streets. Hierholzer's algorithm is like an explorer who:
- Drives along streets arbitrarily, marking them as "driven"
- When reaching a dead end, backs up to the last intersection with unexplored streets
- Records the order of final departures from each intersection
- The reversed record forms a valid tour traversing all streets exactly once

### Extension to Trail Enumeration

The source material describes a **state tree** representation where:
- Each **node** represents a partial Eulerian trail (prefix)
- Each **edge** represents extending the trail by one edge
- **Leaf nodes** represent complete Eulerian trails
- **Branching states** are prefixes with multiple valid extensions

The key insight is that Hierholzer's algorithm can **complete any prefix** to a full trail in $O(m)$ time, enabling recursive enumeration of all trails through the state tree.

## Applications in Engineering

### 1. **Network Routing & Postman Problems**
- **Chinese Postman Problem**: Finding the shortest closed walk traversing all edges (requires minimum edge duplication to create an Eulerian circuit)
- **Vehicle routing**: Planning inspection routes that cover all roads/pipes exactly once

### 2. **Bioinformatics & Sequence Assembly**
- **DNA sequence assembly**: Constructing genomes from overlapping fragments by finding Eulerian paths in de Bruijn graphs
- **Protein sequencing**: Reconstructing protein sequences from mass spectrometry data

### 3. **Circuit Design & PCB Manufacturing**
- **Printed circuit board routing**: Optimal traces connecting components
- **Logic circuit minimization**: Analyzing state transition diagrams

### 4. **Social Network Analysis**
- Detecting cyclic structures and feedback loops in directed social graphs
- Analyzing information propagation patterns

### 5. **Robotic Path Planning**
- Coverage path planning for autonomous systems (cleaning robots, surveillance drones)
- Ensuring systematic exploration of environments

### 6. **VLSI & Chip Design**
- Optimizing scan-chain configurations in circuit testing
- Routing wires in multi-layer interconnects

## Common Mistakes / Pitfalls

### 1. **Assuming Undirected ≠ Directed**
- Students often apply undirected Eulerian conditions to directed graphs
- **Pitfall**: In directed graphs, in-degree must equal out-degree *per vertex*, not just overall balance

### 2. **Forgetting the Graph Must Be Connected**
- An Eulerian trail requires that all edges belong to a single strongly connected component (directed case)
- **Pitfall**: Applying the algorithm to disconnected graphs yields trails of only one component

### 3. **Incorrect Starting Vertex for Trails**
- For an Eulerian trail (not circuit), you must start from a vertex with out-degree exceeding in-degree
- **Pitfall**: Starting from an arbitrary vertex when such vertices exist

### 4. **Not Removing Edges Properly**
- Many implementations fail to explicitly remove traversed edges
- **Pitfall**: Re-traversing edges or getting trapped in infinite loops

### 5. **Confusing Trail ≠ Path**
- An Eulerian **trail** may visit vertices multiple times; it only constrains edges to appear exactly once
- **Pitfall**: Assuming vertices cannot repeat, leading to incorrect invalidation of solutions

### 6. **Inefficient Enumeration**
- Naive state enumeration without compression explores redundant branches
- **Pitfall**: Achieving $O(m \cdot z_T)$ instead of optimal $O(m + z_T)$ by not compressing non-branching prefixes

## See Also

- [[Eulerian Path and Circuit]] — Foundational graph theory concept
- [[De Bruijn Graph]] — Application to sequence assembly
- [[Chinese Postman Problem]] — Optimization variant
- [[Strongly Connected Components]] — Prerequisite for directed graph analysis
- [[Depth-First Search (DFS)]] — Underlying traversal mechanism

## Sources

- Source material: Lecture/paper excerpt on Eul