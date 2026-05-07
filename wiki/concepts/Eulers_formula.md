# Euler's Formula

## Definition

**Euler's formula** is a fundamental relationship in graph theory and topology that relates the number of vertices, edges, and faces of a planar graph. For a connected planar graph $G$:

$$V - E + F = 2$$

where:
- $V$ = number of vertices
- $E$ = number of edges  
- $F$ = number of faces (including the outer unbounded face)

For **triangulated planar graphs** (where every face is a triangle), Euler's formula yields a specialized form. If $G$ is a triangulation with $n$ vertices and all faces are triangles:

$$E = 3n - 6$$

This is derived by counting face-edge incidences: if every face is a triangle, then $2E = 3F$ (each edge borders exactly 2 faces). Substituting into Euler's formula gives this result directly.

## Key Equations

**Standard Form:**
$$V - E + F = 2$$

**For Triangulations:**
$$E = 3n - 6$$
$$F = 2n - 4$$

**Handshaking Lemma (degree sum):**
$$\sum_{u \in V(G)} d(u) = 2E$$

For triangulations, this yields:
$$\sum_{u \in V(G)} d(u) = 2(3n - 6) = 6n - 12$$

**Charge/Discharging Analysis:**
The average degree of a vertex in a triangulation:
$$\text{avg degree} = \frac{6n - 12}{n} = 6 - \frac{12}{n} \to 6 \text{ as } n \to \infty$$

A vertex with degree $d(u)$ can be assigned an initial charge $\sigma(u) = 6 - d(u)$. Summing over all vertices:
$$\sum_{u \in V(G)} \sigma(u) = 6n - (6n - 12) = 12$$

This invariant sum of 12 is crucial for discharging arguments in Four Color Theorem proofs.

## Physical Intuition / Derivation

### Topological Origin

Euler's formula is a topological invariant—it depends only on the connectivity structure, not the geometric embedding. The formula reflects a deep constraint: as you add vertices and edges to a planar graph, their contributions to the left side $V - E + F$ must always balance to 2.

**Intuitive Derivation:**

1. Start with a single vertex: $V=1, E=0, F=1$ → $1-0+1=2$ ✓
2. Add edges and vertices carefully to maintain planarity
3. Each new vertex-edge pair added while keeping planarity preserves the invariant
4. The constant 2 reflects that we're on a **simply-connected** surface (the plane)

### Why Triangulations Have Fewer Edges

In a triangulation, the constraint that every bounded face is a triangle is very restrictive:
- If all faces have exactly 3 edges, then $\sum_{\text{faces}} (\text{edges per face}) = 3F$
- But each edge borders exactly 2 faces, so $\sum_{\text{edges}} 2 = 3F$
- Thus $E = \frac{3F}{2}$

Combined with $V - E + F = 2$, this immediately gives $E = 3n - 6$.

### Degree Constraints

Since $\sum d(u) = 6n - 12$ and we have $n$ vertices, the average degree is $6 - \frac{12}{n}$. This approaches 6 from below as $n$ grows. **Crucially**: not all vertices can have degree ≥ 7, and not all can have degree ≤ 5. This pigeonhole-like consequence is the foundation of discharging arguments in the Four Color Theorem.

## Applications in Engineering

### 1. **Circuit Design & Network Analysis**
- **Planarity testing**: Determine if a circuit layout can be routed on a 2D plane without crossing wires
- **PCB design**: Validates whether multi-layer board layouts are topologically feasible
- Euler's formula provides necessary conditions: a planar graph with $V$ vertices can have at most $3V - 6$ edges

### 2. **Graph Coloring & Resource Allocation**
- **Four Color Theorem**: Proves any planar graph is 4-colorable (e.g., map coloring, frequency assignment)
- **Mesh generation**: Validates simplicial meshes for FEM (Finite Element Method) analysis
- Discharging arguments using Euler's formula constraints guarantee existence of low-degree vertices that can be colored

### 3. **Structural Topology**
- **Finite Element Analysis**: Tetrahedral/triangular meshes must satisfy Euler characteristic relationships
- **Polyhedron analysis**: In molecular modeling and crystallography, vertex-face-edge relationships constrain possible structures (e.g., fullerenes with 12 pentagonal faces and rest hexagonal)

### 4. **Planar Subdivision & Computational Geometry**
- **Map overlay algorithms**: Computing intersections of planar subdivisions respects Euler formula invariants
- **Voronoi diagrams**: Dual graph (Delaunay triangulation) satisfies triangulation constraints

### 5. **Network Reliability**
- **Connectivity analysis**: Establishes bounds on minimum vertex/edge cuts needed to disconnect planar networks
- **Wireless sensor networks**: Constraints on deployment density for planar network topologies

## Common Mistakes / Pitfalls

### 1. **Forgetting the Outer Face**
❌ **Wrong:** Counting only interior triangles as faces in Euler's formula  
✓ **Correct:** The unbounded exterior region is also a face; include it in $F$

### 2. **Applying to Non-Planar Graphs**
❌ **Wrong:** Using $V - E + F = 2$ for $K_5$ or $K_{3,3}$  
✓ **Correct:** $V - E + F = 2$ only for **connected planar graphs**; non-planar graphs have $V - E + F = 1 - g$ where $g$ is