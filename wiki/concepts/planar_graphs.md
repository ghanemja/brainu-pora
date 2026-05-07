# Planar Graphs

## Definition

A **planar graph** is a graph that can be drawn in the plane such that no two edges cross each other (except at their endpoints/vertices). Equivalently, a planar graph can be embedded in the plane without edge intersections.

More formally, a graph $G = (V, E)$ is planar if there exists an injective mapping of vertices to points in $\mathbb{R}^2$ and a mapping of edges to curves in $\mathbb{R}^2$ connecting their endpoints such that curves intersect only at endpoints.

A planar embedding is a specific realization of a planar graph drawn in the plane. The embedding divides the plane into connected regions called **faces**, including one unbounded outer face.

### Characterization Theorems

**Kuratowski's Theorem:** A graph is planar if and only if it contains no subdivision of $K_5$ (complete graph on 5 vertices) or $K_{3,3}$ (complete bipartite graph with 3+3 vertices).

**Wagner's Theorem:** A graph is planar if and only if it does not contain $K_5$ or $K_{3,3}$ as a minor.

## Key Equations

### Euler's Formula
For a connected planar graph:
$$|V| - |E| + |F| = 2$$

where:
- $|V|$ = number of vertices
- $|E|$ = number of edges  
- $|F|$ = number of faces (including the outer face)

### Edge Bounds
For a planar graph with $|V| \geq 3$:
$$|E| \leq 3|V| - 6$$

For a planar graph without triangles (girth $\geq 4$):
$$|E| \leq 2|V| - 4$$

### Face-Edge Incidence
If each face is bounded by at least $k$ edges:
$$|E| \geq \frac{k|F|}{2}$$

## Physical Intuition / Derivation

### Why Planar Graphs Matter

Consider drawing a circuit on a single layer of material, a road network on a map, or a structural frame in 2D space. If you must avoid crossings (to prevent unwanted interference, contact, or signal degradation), you're constrained to planar configurations.

**Euler's Formula Intuition:** 
- Start with a single vertex ($V=1, E=0, F=1$): formula gives $1 - 0 + 1 = 2$ ✓
- Add an edge creating a loop ($V=2, E=1, F=1$): now $2 - 1 + 1 = 2$ ✓  
- Each time you add an edge inside a face without adding vertices, it splits that face (increases $|F|$ by 1) while $|E|$ increases by 1, preserving the invariant.

**Why $|E| \leq 3|V| - 6$:**
From Euler's formula and the handshaking lemma: each face has at least 3 boundary edges, and each edge borders at most 2 faces, so $3|F| \leq 2|E|$. Substituting into $|V| - |E| + |F| = 2$ yields the bound.

### The Planarization Problem

The source material illustrates a key challenge: an **intersection graph** of geometric objects (polygons, rectangles, etc.) may form a tree or forest topologically, but the physical realization may be **nonplanar** due to object crossings (see Figure 5(i) in source).

The **object frame** construction resolves this: decompose each object into smaller sub-objects that remain internally disjoint, creating an equivalent connectivity structure that *is* planar. This allows algorithmic results from planar graph theory to apply to more general intersection graphs.

## Applications in Engineering

### 1. **Circuit Design & VLSI**
- Single-layer PCB routing: minimizing layer count requires keeping connections planar
- Graph planarity testing determines feasibility before physical layout
- Planar subdivisions guide layer assignments in multi-layer designs

### 2. **Transportation & Logistics**
- Road/railway networks are approximately planar (respecting terrain and geography)
- Planar graph algorithms optimize routing and congestion analysis
- Bridge/overpass structures exploit planarity to minimize crossings

### 3. **Mechanical Linkages & Structures**
- Planar mechanisms (robotic arms, crank-slider assemblies) operate in 2D
- Stress analysis exploits planar graph topology for frame analysis
- Finite element mesh generation relies on planar triangulations

### 4. **Geographic Information Systems (GIS)**
- Road networks, parcel maps, and political boundaries form planar subdivisions
- Planarity ensures efficient spatial indexing and query algorithms
- Dual-graph relationships (faces ↔ regions) organize map data

### 5. **Network Topology**
- Planar graphs model networks where physical crossing is expensive (satellites, submarine cables)
- Planarization algorithms approximate non-planar networks with minimal "layer expansion"
- Crossing minimization is NP-hard but critical for visualization and fabrication cost

### 6. **Distributed Algorithms**
- Planar graphs have local separators, enabling divide-and-conquer parallelization
- Face-based decomposition supports hierarchical graph algorithms
- Low treewidth of planar graphs enables dynamic programming solutions

## Common Mistakes / Pitfalls

### 1. **Confusing "Planar" with "Drawn Planarly"**
A planar graph *can* be drawn without crossings, but a specific drawing might have crossings. Always ask: "does an *alternative* embedding exist without crossings?"

**Example:** $K_4$ (4-cycle with complete internal connections) looks nonplanar in one drawing but is actually planar.

### 2. **Forgetting the Outer Face**
Euler's formula counts $|F|$ including the unbounded outer face. Many students incorrectly count only bounded faces, violating the formula.

### 3. **Assuming Sparse ⟹ Planar**
Having $|E| \leq 3|V| - 6$ is *necessary* but **not sufficient** for planarity. Counter-example: $K_{3,3}$ has