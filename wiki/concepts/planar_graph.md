# Planar Graph

## Definition

A **planar graph** is a graph $G = (V, E)$ that can be drawn on a plane (or equivalently, on a sphere) such that its edges intersect only at their endpoints (vertices). More formally, $G$ is planar if and only if it admits a **planar embedding**—a geometric realization where vertices are distinct points in $\mathbb{R}^2$ and edges are continuous curves connecting their endpoints with no edge crossings except at vertices.

A planar graph together with a fixed embedding in the plane is called a **plane graph**.

## Key Equations

**Euler's Formula** (fundamental property of connected plane graphs):
$$|V| - |E| + |F| = 2$$

where $|V|$ is the number of vertices, $|E|$ is the number of edges, and $|F|$ is the number of faces (regions created by the embedding, including the unbounded outer face).

**Edge bound for planar graphs** (consequence of Euler's formula):
$$|E| \leq 3|V| - 6$$

for simple planar graphs with $|V| \geq 3$. For planar graphs with no triangles:
$$|E| \leq 2|V| - 4$$

**Face-edge incidence:**
$$\sum_{f \in F} \deg(f) = 2|E|$$

where $\deg(f)$ is the number of edges bounding face $f$.

## Physical Intuition / Derivation

### Why Euler's Formula Holds

Consider building a plane graph incrementally. Start with a single vertex: $|V| = 1, |E| = 0, |F| = 1$ (only the outer face), so $1 - 0 + 1 = 2$ ✓

When you add a vertex not connected to the existing graph, you increase $|V|$ by 1 and $|F|$ stays the same, maintaining the invariant.

When you add an edge:
- **Connecting two existing vertices within the same face:** The edge splits that face into two, increasing $|F|$ by 1. Thus $|V|$ unchanged, $|E|$ increases by 1, $|F|$ increases by 1: the invariant is preserved.
- **Connecting a new vertex to the graph:** Creates one new vertex and one edge, but doesn't create new faces. Again the invariant holds.

This recursive construction proves Euler's formula for all connected plane graphs.

### Why the Edge Bound Follows

From Euler's formula: $|F| = 2 - |V| + |E|$

Each face in a simple graph is bounded by at least 3 edges (triangles are minimal). Counting face-edge incidences:
$$\sum_{f \in F} \deg(f) = 2|E|$$

If every face has degree $\geq 3$:
$$3|F| \leq 2|E|$$

Substituting $|F| = 2 - |V| + |E|$:
$$3(2 - |V| + |E|) \leq 2|E|$$
$$6 - 3|V| + 3|E| \leq 2|E|$$
$$|E| \leq 3|V| - 6$$

This sparse bound is fundamental: **planar graphs have linear rather than quadratic edge density**, making them structurally simpler than general graphs.

## Applications in Engineering

### 1. **Circuit Design & VLSI**
- **Integrated circuit layouts** are essentially planar graphs where vertices are logic gates and edges are wires. The planarity constraint reflects physical layer separation in multi-layer PCBs.
- Planar embedding algorithms minimize wire crossings, reducing fabrication cost and electromagnetic interference.

### 2. **Network Design**
- **Utility networks** (water pipes, electrical grids, roads) in geographic regions form planar graphs because infrastructure typically cannot cross except at designated junctions.
- Planar graph algorithms enable efficient network partitioning and reliability analysis.

### 3. **Computational Geometry & Spatial Data Structures**
- **Triangulated meshes** in finite element analysis are planar graphs (when projected), enabling specialized solvers for structural mechanics simulations.
- [[Tree decomposition|Tree decompositions]] of planar graphs (as referenced in Lemma 3.6) enable dynamic programming on spatially organized data with improved complexity.

### 4. **Graph Drawing & Visualization**
- **Automatic layout algorithms** exploit planarity to produce readable diagrams with minimal visual clutter.
- Applications in software engineering, biology (protein interaction networks), and knowledge representation.

### 5. **Robotics & Motion Planning**
- **Planar robot workspaces** and obstacle configurations often form planar subdivision graphs, enabling efficient path planning via planar duality and dual graphs.

## Common Mistakes / Pitfalls

1. **Confusing planarity with "looks planar"**: A graph drawn with crossings might still be planar—drawing quality doesn't determine planarity. Use **Kuratowski's theorem** (a graph is planar iff it contains no subdivision of $K_5$ or $K_{3,3}$) or algorithms like Hopcroft-Tarjan for verification.

2. **Forgetting the $|V| \geq 3$ condition**: The bound $|E| \leq 3|V| - 6$ is false for $|V| < 3$. For $|V| = 1, 2$, you can have arbitrary many edges if multigraphs are allowed.

3. **Applying dense-graph algorithms to planar graphs**: Using algorithms designed for general graphs ignores the sparsity structure. Specialized $O(n)$ or $O(n \log n)$ planar algorithms often exist (e.g., planar separator theorem).

4. **Misinterpreting Euler's formula for disconnected graphs**: For $c$ connected components: $|V| - |E| + |F| = 1 + c$. Always check connectivity first.

5. **Underestimating tree decomposition utility**: Lemma 3.6 shows that planar graphs admit tree decompositions with bounded width (treewidth $O(1)$ for planar graphs with good separators). This enables **parameterized algorithms**, but requires careful algorith