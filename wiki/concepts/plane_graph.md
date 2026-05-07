# plane graph

## Definition

A **plane graph** is a graph that can be drawn on a two-dimensional plane such that:

1. **No edge crossings**: Edges are drawn as continuous curves (typically straight line segments or piecewise linear curves) that intersect only at their endpoints (vertices)
2. **Embedding property**: The graph admits a planar embedding—a specific geometric realization where the topological structure is preserved
3. **Faces**: The plane is partitioned into regions called *faces* by the edges and vertices, including one unbounded outer face

Formally, a plane graph $G = (V, E)$ is a planar graph together with a fixed embedding in $\mathbb{R}^2$. This differs from a *planar graph*, which merely admits the possibility of such an embedding without specifying which one.

### Representation and Constraints

In computational contexts (particularly geometric processing), a plane graph can be specified by:
- A set of vertices $V$ with geometric coordinates
- A set of edges $E$ with piecewise linear geometric realizations
- A cell partition $P$ derived from the geometric arrangement

Key geometric properties often enforced:
- **Geometric diameter**: Maximum Euclidean distance along any edge
- **Lipschitz continuity**: Distance-preserving properties under graph homomorphisms
- **Bounded degree**: Maximum vertex degree constraints

## Key Equations

**Euler's formula for connected plane graphs:**
$$V - E + F = 2$$

where $V$ is the number of vertices, $E$ is the number of edges, and $F$ is the number of faces (including the outer unbounded face).

**Lipschitz condition for map preservation:**
For a function $f: V(G) \to V(H)$ between graphs with geometric embeddings:
$$d_H(f(u), f(v)) \leq c \cdot d_G(u, v) \quad \forall u, v \in V(G)$$

where $c$ is the Lipschitz constant and $d_*$ denotes graph distance.

**Contracted graph mapping (Lemma 5.4):**
If $G$ admits a $c$-Lipschitz mapping to $H$, then the contracted graph $H/S$ admits a mapping to $G$ with Lipschitz constant bounded by:
$$c_{\text{contracted}} \leq c^2$$

**Degree and diameter bounds for constructed plane graphs:**
$$\Delta(H) = O(\alpha^{34}), \quad \text{diam}_{\text{geo}}(e) = O(\alpha^{17})$$

where $\alpha$ parameterizes the geometric complexity of the input.

## Physical Intuition / Derivation

### Why Plane Graphs Matter

Plane graphs capture the essential structure of 2D spatial arrangements without edge crossings. This property is fundamental because:

1. **Spatial localization**: In physical systems (networks, roads, circuit layouts), non-crossing embeddings reflect the actual spatial configuration
2. **Face structure**: The natural decomposition into faces corresponds to regions of space—rooms in a building, compartments in a network, or circuit regions

### Constructing Plane Graphs from Polygonal Arrangements

The source material addresses a deeper problem: given a complex intersection graph of polygons in the plane, how can we construct a simplified plane graph that preserves distance relationships?

**The construction process (Theorem 5.2):**

1. Start with a *fair intersection graph* $G$ where vertices represent polygons and edges represent intersections
2. Compute the cell partition $P$—the maximal set of connected regions formed by the geometric arrangement
3. Build a new plane graph $H = (\dot{P}, E')$ where:
   - Vertices $\dot{P}$ correspond to cells in the partition
   - Edges connect cells that share a boundary
4. Ensure the natural mapping from cells to original vertices is $c$-Lipschitz—distances are scaled by at most constant $c$

**Key insight:** This avoids the full complexity of the intersection graph while maintaining metric structure.

### Contraction while Preserving Planarity

Lemma 5.4 shows how to remove unnecessary vertices through edge contraction while:
- Maintaining distance bounds (Lipschitz constant squares: $c \to c^2$)
- Preserving the planar embedding
- Keeping edges as piecewise linear curves with bounded diameter

This is crucial for algorithms that need to simplify graphs incrementally while respecting geometric constraints.

## Applications in Engineering

### Circuit Design & Layout
- **Wire routing**: Plane graph embeddings ensure non-crossing wire layouts in PCB design
- **Floor planning**: Planar subdivisions represent rectangular floor layouts; planarity guarantees avoids crossing corridors

### Computational Geometry
- **Mesh generation**: Planar graphs form the basis for triangulation and quadrilateral meshes
- **Arrangement computation**: Constructing plane subdivisions from curves (lines, polygons) for collision detection and spatial queries

### Network Design
- **Road networks**: City street maps (naturally planar due to physical constraints) can be analyzed using plane graph algorithms
- **Infrastructure networks**: Utility networks (water, gas, electrical) often have planar or near-planar structure

### Computer Graphics & Visualization
- **Graph drawing**: Automatic layout algorithms exploit planarity for readable visualizations without edge crossings
- **Texture mapping**: Planar parameterization of 3D surfaces requires plane graph decomposition

### Geographic Information Systems (GIS)
- **Topological data structures**: Representing subdivisions of geographic space (regions, boundaries)
- **Spatial indexing**: Face-based queries exploit the planar structure for efficient search

## Common Mistakes / Pitfalls

1. **Confusing planar with plane**: A *planar graph* may admit multiple embeddings; a *plane graph* has one fixed embedding. The geometric realization matters!

2. **Ignoring geometric diameter**: In applications, Lipschitz constants and edge length bounds are not free—they directly affect algorithms' complexity. A "plane graph" with unbounded edge lengths defeats the purpose of geometric localization.

3. **Assuming Euler's formula applies blindly**: The formula $V - E + F = 2$ requires:
   - A *connected* graph (multiply by number of components otherwise)
   - Counting the outer unbounded face
   - Discrete vertices and edges (issues arise with curves and degeneracies)

4. **Missing the contraction subtlety**: When contracting