# Pathwidth

## Definition

**Pathwidth** is a graph parameter measuring how "path-like" a graph is. Formally, the pathwidth of a graph $G$ is the minimum width of a *path decomposition* of $G$.

A **path decomposition** of a graph $G = (V, E)$ is a sequence of sets $X_1, X_2, \ldots, X_r$ (called *bags*) such that:

1. **Vertex coverage**: $\bigcup_{i=1}^{r} X_i = V$
2. **Edge coverage**: For every edge $(u,v) \in E$, there exists a bag $X_i$ containing both $u$ and $v$
3. **Consecutive property**: For each vertex $v \in V$, the set of indices $\{i : v \in X_i\}$ forms a consecutive interval

The **width** of a path decomposition is $\max_{i=1}^{r} |X_i| - 1$ (the width is the maximum bag size minus one).

The **pathwidth** $\text{pw}(G)$ is the minimum width over all possible path decompositions.

### Special Cases
- A graph has pathwidth 0 if and only if it is edgeless
- A graph has pathwidth 1 if and only if it is a forest (acyclic)
- A graph has pathwidth 1 if and only if it is a collection of disjoint paths

## Key Equations

The relationship between pathwidth and other structural parameters:

$$\text{pathwidth}(G) \leq \text{treewidth}(G) \leq \text{pathwidth}(G) \cdot \lceil \log_2 n \rceil$$

where $n = |V(G)|$.

More directly:
$$\text{pathwidth}(G) \leq \text{treewidth}(G)$$

since every path decomposition is a tree decomposition (with the tree being a path).

For parameterized complexity, the relationship to elimination distance:
$$\text{A graph has bounded pathwidth} \not\Rightarrow \text{bounded elimination distance to forests}$$

## Physical Intuition / Derivation

### Understanding Path Decomposition

Think of a path decomposition as an ordered "scanning process" moving left to right through a graph:

1. **Bags as snapshots**: Each bag $X_i$ represents the set of vertices "visible" or "active" at step $i$ of a path-like process
2. **Consecutive property as locality**: The requirement that each vertex appears in consecutive bags ensures that we process vertices in a contiguous manner—once we're "done" with a vertex, we don't need to return to it
3. **Width as resource bound**: The width limits how many vertices we must manage simultaneously at any step

### Why "Path" not "Tree"?

- A **tree decomposition** allows bags arranged in a tree structure, giving maximum flexibility
- A **path decomposition** restricts to a linear arrangement, which is more constrained but still captures important graph structure
- This middle ground makes pathwidth valuable for algorithms: more restrictive than treewidth (easier to exploit), more general than tree-depth

### Building Intuition with Examples

**Example 1**: A cycle $C_n$ has $\text{pw}(C_n) = 2$
- Decomposition: $X_1 = \{v_1, v_2\}, X_2 = \{v_2, v_3\}, \ldots, X_n = \{v_n, v_1\}$
- Each bag has size 2 (width 1)

**Example 2**: A clique $K_n$ has $\text{pw}(K_n) = n-1$
- Any decomposition must have all vertices in every bag (all edges must be covered)
- Thus width is $n - 1$

**Example 3**: A path $P_n$ has $\text{pw}(P_n) = 1$
- Decomposition: $X_i = \{v_i, v_{i+1}\}$ for consecutive vertices
- Each bag has width 1

## Applications in Engineering

### 1. **Parameterized Complexity & Kernelization**
Pathwidth serves as a structural parameter for fixed-parameter tractable (FPT) algorithms:
- Problems that are NP-hard in general become FPT when parameterized by pathwidth
- **Example**: The $d$-COC (Conflict-free Coloring) problem admits polynomial kernels on graphs of bounded pathwidth
- **Use case**: Network design and scheduling where bounded pathwidth structure emerges from spatial/temporal constraints

### 2. **VLSI Design & Circuit Layout**
- Graph layouts with bounded pathwidth correspond to efficient physical circuit implementations
- Pathwidth bounds the number of "crossing wires" in one-dimensional layouts
- **Application**: Designing PCB routing and minimizing layer complexity

### 3. **Compiler Optimization & Program Analysis**
- Control flow graphs in programs with bounded pathwidth permit efficient data-flow analysis
- Enables polynomial-time computation of reachability and dependency information
- **Use case**: Static analysis tools for real-time systems verification

### 4. **Network Packet Routing**
- Networks with bounded pathwidth structure allow efficient routing algorithms
- Related to bandwidth minimization in network design
- **Application**: Minimizing buffer requirements in network switches

### 5. **Sparse Graph Algorithms**
- Many sparse graph families have bounded pathwidth
- Enables efficient dynamic programming on path decompositions
- **Application**: Large-scale network analysis where pathwidth structures emerge naturally

## Common Mistakes / Pitfalls

### 1. **Confusing Pathwidth with Treewidth**
**Mistake**: Treating them as equivalent parameters
- **Reality**: Pathwidth ≤ treewidth, but can be exponentially smaller for some graphs
- **Impact**: A polynomial algorithm in treewidth may not be polynomial in pathwidth; verify the dependence carefully

### 2. **Assuming Bounded Pathwidth Implies Bounded Elimination Distance**
**Mistake**: Thinking pathwidth is "just another structural parameter" with similar dichotomy properties
- **Reality** (from source): Graphs with bounded pathwidth do NOT necessarily have bounded elimination distance to forests
- **Impact**: Kernelization results for path