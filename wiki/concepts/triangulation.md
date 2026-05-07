# Triangulation

## Definition

A **triangulation** is a planar graph decomposition where every bounded face is a triangle (3-sided polygon). More formally, a triangulation $G = (V, E, F)$ is a maximal planar graph where:

- Every face except the outer (unbounded) face is bounded by exactly 3 edges
- The outer face is bounded by a cycle (the outer facial walk)
- No edges can be added without destroying planarity or creating non-triangular faces

A **near-triangulation** is a relaxation where the outer face may have any length, but all interior faces are triangular.

A **configuration** $(Z, \delta)$ is a near-triangulation $Z$ paired with a function $\delta: V(Z) \to \mathbb{Z}^+$ assigning expected degrees to vertices. A configuration is **induced** in a larger graph $G$ if $Z$ appears as a subgraph of $G$ with the specified degree constraints locally satisfiable.

## Key Equations

### Ring Length Formula

For a configuration $(Z, \delta)$, the **free completion** $\widehat{Z}$ is formed by adding a cycle $R$ (the *ring*) to complete $Z$ to a full triangulation. The length of $R$ is:

$$|R| = \sum_{v \in V(Z)} \left(\delta(v) - d_Z(v)\right) - t$$

where:
- $\delta(v)$ = prescribed degree for vertex $v$
- $d_Z(v)$ = actual degree of $v$ in $Z$  
- $t$ = length of outer facial walk of $Z$

Equivalently:

$$|R| = \sum_{v \in V(Z)} \delta(v) - 2|E(Z)| - t$$

### Degree-Edge Relationship

For any triangulation with $n$ vertices, $e$ edges, and $f$ faces:

$$\sum_{v \in V} d(v) = 2e \quad \text{(handshaking lemma)}$$

For planar triangulations:
$$e = 3n - 6 \quad \text{(Euler relation with all faces triangular)}$$

## Physical Intuition / Derivation

### Why Triangulations Matter

Triangles are the minimal rigidity units in planar structures. A triangulation can be viewed as:

1. **Degree deficit model**: Each vertex has a "desired degree" $\delta(v)$. The difference $\delta(v) - d_Z(v)$ represents unsatisfied degree at that vertex. The ring $R$ must accommodate all these deficits.

2. **Inductive reduction**: Triangulations are used in **4-color theorem proofs** via:
   - Extract an induced configuration $(Z, \delta)$ from graph $G$
   - Prove the configuration is *reducible*: any 4-coloring of $G - V(Z)$ can be extended through $Z$
   - Use Kempe chains to recolor $G - V(Z)$ so that boundary colorings become extendible to $Z$

3. **Free completion logic**: The ring $R$ acts as a "closure" that converts a partial structure into a complete triangulation. Vertices on $R$ mediate between the internal configuration and external graph structure.

### Derivation of Ring Length

Starting from Euler's formula $V - E + F = 2$:
- The subgraph $Z$ has $|V(Z)|$ vertices, $|E(Z)|$ edges, interior faces + 1 outer face
- Total degree sum in $Z$: $\sum d_Z(v) = 2|E(Z)|$
- Prescribed total degree sum: $\sum \delta(v)$
- The ring $R$ with $|R|$ vertices must "close the gap":

$$2|R| + \sum d_Z(v) = \sum \delta(v) + \text{(edges between } Z \text{ and } R\text{)}$$

This yields the ring length formula.

## Applications in Engineering

### 1. Mesh Generation & Finite Element Analysis
- Automatic triangulation of irregular domains (Delaunay triangulation) for FEA
- Ensures mesh quality (avoiding obtuse triangles)
- Applications: structural analysis, fluid dynamics, electromagnetics

### 2. Graph Coloring & Optimization
- 4-color theorem proof (Appel-Haken-Koch): uses configuration reducibility
- Register allocation in compilers
- Frequency assignment in wireless networks

### 3. Planar Graph Algorithms
- Drawing planar graphs with minimal edge crossings
- Computing shortest paths in planar subdivision schemes (e.g., visibility graphs for robotics)

### 4. Computational Geometry
- Point location in triangulated polygons
- Surface reconstruction from point clouds
- Convex hull and Delaunay triangulation algorithms

### 5. Structural Mechanics
- Triangulated space frames and geodesic domes (inherent rigidity)
- Fault-tolerant network topology (triangulation ensures 3-connectivity)

## Common Mistakes / Pitfalls

### 1. Confusing Triangulation with Tessellation
**Mistake**: Assuming all plane decompositions into triangles are triangulations.  
**Reality**: A triangulation must be a maximal planar graph—no edges can be added without violating planarity or creating non-triangular faces.

### 2. Ignoring the Outer Face Constraint
**Mistake**: Treating the outer face as just another triangle.  
**Reality**: The outer face can have arbitrary length; only *interior* faces must be triangular. This distinction is crucial for inductive arguments.

### 3. Misinterpreting Degree Deficits
**Mistake**: Assuming $\delta(v) - d_Z(v) > 0$ always (vertices need more connections).  
**Reality**: Deficits can be negative (vertices already exceed prescribed degree), affecting ring closure and extendibility conditions.

### 4. Ring Non-Uniqueness
**Mistake**: Believing the ring $R$ is uniquely determined by $(Z, \delta)$.  
**Reality**: Multiple realizations exist (especially with cut-vertices in $G - V(Z)$). The formula gives length but not structure.

### 5. Extendibility vs.