# Breadth-First Search (BFS)

## Definition

**Breadth-first search (BFS)** is a fundamental graph traversal algorithm that explores vertices in a graph by visiting all neighbors of the current vertex before moving to the next level of vertices. Starting from a designated source vertex, BFS systematically explores the graph level by level, maintaining an ordering where vertices closer to the source (in terms of edge count) are visited before more distant vertices.

Formally, BFS constructs a **breadth-first tree** rooted at the source vertex, where each vertex is visited exactly once and stored in a queue data structure for ordered processing.

## Key Equations

**Distance from source:**
$$d(s, v) = \text{number of edges on shortest path from } s \text{ to } v$$

**Time Complexity:**
$$O(V + E)$$
where $V$ is the number of vertices and $E$ is the number of edges.

**Space Complexity:**
$$O(V)$$
for the queue and visited marker storage.

**Frontier expansion:**
$$\text{Frontier}_{t+1} = \{v : v \in \text{Adj}(u), u \in \text{Frontier}_t, v \text{ unvisited}\}$$

## Physical Intuition / Derivation

BFS operates like a wave propagating outward from a source point:

1. **Initialization:** Place the source vertex in a queue and mark it as visited
2. **Wave propagation:** Repeatedly dequeue a vertex, examine all its unvisited neighbors, mark them visited, and enqueue them
3. **Systematic exploration:** The queue enforces FIFO (first-in-first-out) ordering, ensuring vertices are processed in distance order from the source

This level-by-level exploration guarantees that **the first time any vertex is encountered, it has been reached via a shortest path** (in unweighted graphs). This property makes BFS fundamentally different from depth-first search (DFS), which explores as deeply as possible before backtracking.

**Why the queue matters:** The queue acts as a "waiting line" that preserves the order of discovery. Only when all vertices at distance $d$ have been processed are vertices at distance $d+1$ dequeued and processed.

## Applications in Engineering

### Graph Analysis & Network Problems
- **Shortest path in unweighted graphs:** Finding the minimum number of hops between two nodes in computer networks, social networks, or road networks
- **Connected component detection:** Identifying all vertices reachable from a given vertex
- **Bipartiteness checking:** Determining if a graph can be 2-colored (useful in circuit design and task scheduling)

### Biological & Structural Analysis
- **Ultrabubble detection:** As cited in the source material, BFS is used to detect minimal snarls and ultrabubbles in biedged graphs (common in genomic sequence analysis). By running BFS on subgraphs defined by frontier nodes, algorithms can identify cycles and tips without expensive recursive stack operations
- **Protein interaction networks:** Finding groups of interacting proteins and measuring distances between functional groups

### Robotics & AI
- **Motion planning:** Exploring configuration space to find collision-free paths
- **Puzzle solving:** Finding shortest sequences of moves (e.g., solving Rubik's cubes, 8-puzzle)
- **Game AI:** Building game trees with uniform branching where all moves at the same depth are equally valuable

### Circuit & Logic Design
- **Level synchronization:** Organizing circuits by depth/delay levels
- **Timing analysis:** Computing critical path distances in digital circuits

### Source Code Analysis
- **Type inference & data flow:** Forward propagation of type information through call graphs
- **Reachability analysis:** Determining which functions can be called from a given entry point

## Common Mistakes / Pitfalls

### 1. **Forgetting to Mark Vertices as Visited**
```
❌ WRONG: Forgetting visited[] causes infinite loops on cycles
✓ CORRECT: Mark vertex as visited immediately upon enqueueing
```
This is critical—if you mark a vertex visited only when dequeuing, it may be enqueued multiple times.

### 2. **Using BFS for Weighted Shortest Paths**
BFS finds shortest paths only in unweighted graphs (where each edge has weight 1). For weighted graphs, use **Dijkstra's algorithm** or **Bellman-Ford**.

### 3. **Confusing BFS with DFS**
- BFS uses a **queue** → finds shortest paths in unweighted graphs
- DFS uses a **stack** (or recursion) → useful for detecting cycles, topological ordering, and strongly connected components

### 4. **Not Initializing the Queue**
Forgetting to enqueue the source vertex before starting the main loop leaves nothing to process.

### 5. **Graph Representation Inefficiency**
Using adjacency matrix instead of adjacency list for sparse graphs inflates time complexity from $O(V+E)$ to $O(V^2)$.

### 6. **Misunderstanding "Shortest Path" Context**
In the source material, BFS is mentioned for checking subgraphs for cycles and tips. This is not about finding paths but about **exhaustively exploring connectivity**—ensure you're using the right algorithm for your actual problem.

## See Also

- [[Depth-First Search (DFS)]] — Alternative graph traversal with different properties (stack-based, explores deeply)
- [[Dijkstra's Algorithm]] — Shortest path for weighted graphs (extends BFS with priority queue)
- [[Graph Connectivity]] — Problems solved by traversal algorithms
- [[Bipartite Graphs]] — Application area where BFS determines 2-colorability
- [[Ultrabubbles and Snarls]] — Genomic graph structures detected using BFS in biedged graphs

## Sources

- Lecture/paper excerpt on ultrabubbles and snarls in biedged graphs (Section 3.1: "Ultrabubbles and snarls by the naive approach")
- Standard references: *Introduction to Algorithms* (Cormen et al.), graph theory fundamentals