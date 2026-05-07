# Dart Representation

## Definition

A **dart representation** is a data structure for efficiently representing and navigating planar graphs and their embeddings, particularly triangulations. A dart (also called a *half-edge* or *directed edge*) is a directed version of an edge in a graph that maintains local topological information, enabling constant-time neighbor queries and face traversals in planar structures.

Formally, for each undirected edge $e = \{u, v\}$ in a planar graph, the dart representation creates two directed darts:
- One dart from $u$ to $v$ (denoted $d_{u \to v}$)
- One dart from $v$ to $u$ (denoted $d_{v \to u}$)

These darts are linked via three primary operations:

$$\text{next}(d) : \text{the next dart in counterclockwise order around a face}$$
$$\text{prev}(d) : \text{the previous dart in counterclockwise order around a face}$$
$$\text{flip}(d) : \text{the opposite dart (the dual direction on the same edge)}$$

Such that $\text{flip}(\text{flip}(d)) = d$ and $\text{flip}(d_{u \to v}) = d_{v \to u}$.

## Key Equations

The fundamental cyclic property around a vertex $v$:

$$\text{next}^{n}(d) = d \quad \text{for some finite } n \text{ (the vertex degree)}$$

Traversing an entire face requires following `next` pointers:

$$F = \{d, \text{next}(d), \text{next}^2(d), \ldots, \text{next}^{k-1}(d)\} \quad \text{where } k = |F|$$

The Euler characteristic for a connected planar graph embedded as a triangulation:

$$V - E + F = 2$$

where darts provide efficient access to compute these quantities.

## Physical Intuition / Derivation

### Why Darts Exist

When working with planar triangulations (the standard form for graph coloring proofs), you need to:
1. **Traverse face boundaries** quickly (essential for coloring algorithms)
2. **Query neighbors** of a vertex or face in constant time
3. **Navigate the embedding** in both directions around a face

Naive adjacency lists make face traversal expensive: you'd need to search through lists multiple times.

### How Darts Work

Imagine standing on a directed edge (dart) pointing from vertex $u$ to $v$. The `next` pointer tells you which dart you encounter next if you continue walking counterclockwise around the face. This creates a circular linked list structure for each face.

**Example**: In a triangulated region, if you have a dart from $A$ to $B$:
- `next(d_{A→B})` points you to the dart completing the triangle, say $d_{B→C}$
- `next(d_{B→C})` points to $d_{C→A}$
- `next(d_{C→A})` points back to $d_{A→B}$

This creates $O(1)$ time traversal of all three edges of a triangle.

### Constant-Time Neighbor Queries

To find all vertices adjacent to $v$:
1. Pick any dart $d$ with source $v$
2. Repeatedly apply: $d \leftarrow \text{flip}(\text{next}(d))$
3. This cycles through all neighbors of $v$

Since each step is $O(1)$ and there are $\deg(v)$ neighbors, the total time is $O(\deg(v))$—linear in the neighborhood size.

## Applications in Engineering

### 1. **Graph Coloring Proofs (Computational Mathematics)**
The dart representation is critical in modern proofs of the Four Color Theorem. The authors of near-linear 4CT proofs use dart representations to:
- Navigate triangulations efficiently during reducibility checking
- Track face and vertex constraints during the coloring algorithm
- Maintain pointer safety in formal verification (as noted in AI-assisted verification of pseudocode)

### 2. **Computational Geometry & Mesh Processing**
- **Planar subdivision management**: Darts represent topological information for embedded graphs in GIS and CAD systems
- **Mesh navigation**: In finite element analysis (FEA) or computer graphics, darts enable fast traversal of triangular or polygonal meshes
- **Half-edge structures**: Modern graphics APIs use half-edge data structures (a variant of darts) for manifold mesh operations

### 3. **VLSI & Circuit Layout**
- Planar graph embeddings for floorplanning and routing
- Dart structures optimize queries like "what circuits surround this region?"

### 4. **Formal Verification**
The dart representation's pointer-based structure with invariants (e.g., $\text{flip}(\text{flip}(d)) = d$) makes it amenable to static analysis and formal verification, as demonstrated in AI-assisted auditing of loop invariants and pointer safety.

## Common Mistakes / Pitfalls

### 1. **Confusing Darts with Edges**
A dart is *directional*; an edge is undirected. Always maintain that each undirected edge corresponds to exactly two darts (one in each direction). Forgetting this leads to missing half the graph.

### 2. **Incorrect `next` Pointer Semantics**
Students often confuse:
- `next(d)`: the dart encountered next when walking around a *face* in one direction
- `next_neighbor(d)`: not a standard operation; neighbors are found via `flip(next(d))`

### 3. **Face Orientation Inconsistency**
If you define `next` as counterclockwise on the sphere/plane, ensure *all* faces follow this consistently. Mixing clockwise and counterclockwise creates cycles that never terminate or traverse incorrectly.

### 4. **Ignoring the Outer Face**
In planar graphs embedded in the plane, the unbounded outer face must be treated like any other face in the dart structure. Overlooking this causes boundary condition bugs.

### 5. **Pointer Safety in Modifications**
When adding/removing edges from a triangulation, updating dart pointers is error-prone:
- Deleting an edge