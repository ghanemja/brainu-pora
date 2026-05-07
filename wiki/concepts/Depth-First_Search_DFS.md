# Depth-First Search (DFS)

## Definition

**Depth-First Search (DFS)** is a fundamental graph traversal algorithm that explores a graph by advancing as far as possible along each branch before backtracking. Starting from a source node, DFS systematically visits nodes by recursively exploring unvisited neighbors until reaching a dead-end, then backtracks to explore alternative paths.

More formally, DFS maintains a **stack** (either explicitly or via recursion) of nodes to visit. At each step, it:
1. Pops a node from the stack
2. Marks it as visited
3. Pushes all unvisited neighbors onto the stack

The algorithm naturally produces a **DFS tree** (or forest for disconnected graphs) where edges are classified as:
- **Tree edges**: edges used to discover new nodes
- **Back edges**: edges pointing to ancestors in the DFS tree
- **Forward edges**: edges to descendants (in directed graphs)
- **Cross edges**: all other edges

## Key Equations

**Time Complexity:**
$$T(n, m) = O(n + m)$$

where $n$ is the number of vertices and $m$ is the number of edges. Each vertex and edge is examined at most once.

**Space Complexity:**
$$S(n) = O(n)$$

for the recursion stack in the worst case (for a linear chain graph), or $O(h)$ where $h$ is the maximum depth of recursion.

**Recursive Formulation:**
```
DFS(v):
  mark v as visited
  for each unvisited neighbor u of v:
    DFS(u)
```

The **delay** for finding the next solution in DFS-based enumeration (from source context) is:
$$\text{Delay} = O((m+1) \cdot n \cdot l)$$

where $m$ is the number of solutions already found, $n$ is problem size, and $l$ is path length.

## Physical Intuition / Derivation

Imagine exploring a maze without memory. DFS models **exhaustive exploration with backtracking**:

- You enter a corridor and follow it completely, even when it becomes a dead-end
- When stuck, you backtrack to the last junction and try the next path
- You never enter a corridor twice
- You leave a "mark" (visited flag) to avoid cycles

This is why DFS works on **any graph structure** without prior knowledge of layout: the algorithm is *adaptive*—it discovers structure incrementally.

**Why is it called "depth-first"?** Because the traversal prioritizes *depth* (distance from start) over *breadth*. The stack nature means: "go as deep as you can before going wide."

**Connection to backtracking:** DFS is the foundation of backtracking algorithms. When exploring a solution space, DFS naturally builds a tree of possibilities and prunes branches when constraints are violated.

From the source material context (MUS enumeration in 2-CNF), DFS is used to enumerate paths in dependency graphs. The algorithm's key property is that each recursive call produces at least one path, making it suitable for structured enumeration with polynomial delay bounds.

## Applications in Engineering

### 1. **Graph Analysis & Connectivity**
- Computing connected components
- Detecting cycles in graphs
- Topological sorting (Kahn's algorithm variant)
- Finding strongly connected components (Tarjan's algorithm)

### 2. **Compiler Design**
- Control flow graph analysis
- Dead code elimination
- Register allocation via graph coloring

### 3. **Robotics & Path Planning**
- Maze solving and robot navigation
- Obstacle avoidance in discrete environments
- State space exploration

### 4. **Constraint Satisfaction & Optimization**
- Backtracking search in CSP solvers
- MUS (Minimal Unsatisfiable Subset) enumeration (as in source material)
- SAT solver branching strategies
- Solution enumeration in logical systems

### 5. **Network Analysis**
- Spanning tree computation
- Bridge and articulation point detection
- Network reachability analysis

### 6. **Bioinformatics**
- Protein folding simulations via conformational space search
- Phylogenetic tree construction

## Common Mistakes / Pitfalls

### 1. **Forgetting to Mark Visited Nodes**
**Error:** Not tracking visited nodes leads to infinite loops in cyclic graphs.
```python
# WRONG - infinite loop possible
def dfs_bad(v, graph):
    for neighbor in graph[v]:
        dfs_bad(neighbor, graph)

# CORRECT
def dfs_good(v, graph, visited):
    visited.add(v)
    for neighbor in graph[v]:
        if neighbor not in visited:
            dfs_good(neighbor, graph, visited)
```

### 2. **Confusing DFS with BFS**
Students often mix these up:
- **DFS**: Stack-based → explores deep first → backtracking natural
- **BFS**: Queue-based → explores level-by-level → shortest paths

### 3. **Incorrect Space Complexity Claims**
**Mistake:** "DFS uses $O(1)$ space"
- **Reality:** Recursive DFS uses $O(h)$ stack space where $h$ is tree height
- For deep or pathological graphs ($h = n$), this is $O(n)$
- Explicit-stack DFS still requires $O(n)$ space in worst case

### 4. **Misunderstanding Delay/Time in Enumeration**
From source material: The delay of $O((m+1) \cdot n \cdot l)$ occurs because finding the *next* solution may require exploring $m+1$ branches (including $m$ "silent" sibling paths already found). This is **not** per-solution time, but **amortized delay** to next output.

### 5. **Not Handling Disconnected Components**
```python
# WRONG - only finds one component
def dfs_incomplete(graph):
    visited = set()
    dfs_good(list(graph.keys())[0], graph, visited)

# CORRECT - finds all components
def dfs_all_components(graph):
    visited = set()
    for node in graph:
        if node not in visited:
            dfs_good(node, graph, visited)
```

### 6. **Misapplying DFS to