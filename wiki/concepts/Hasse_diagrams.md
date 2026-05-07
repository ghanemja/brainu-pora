# Hasse Diagrams

## Definition

A **Hasse diagram** is a directed acyclic graph (DAG) that visualizes the partial ordering relation (face poset) of a finite topological complex. For a finite regular CW complex $X$:

- **Vertices**: one vertex per cell (simplex, edge, face, etc.)
- **Directed edges**: an arc $\sigma \to \tau$ exists if $\sigma$ is an *immediate face* (cover relation) of $\tau$, meaning:
  - $\sigma$ is contained in $\tau$ 
  - $\dim(\tau) = \dim(\sigma) + 1$
  - no cell lies strictly between them in dimension

The **directed Hasse diagram** $\vec{H}(X)$ encodes the complete incidence structure of the complex. The **underlying undirected graph** $H(X)$ is obtained by ignoring edge directions and is the natural object for measuring graph properties like treewidth.

## Key Equations

### Cover relation and dimension constraint

$$\sigma \to \tau \text{ in } \vec{H}(X) \iff \sigma \subset \tau \text{ and } \dim(\tau) = \dim(\sigma) + 1$$

### Discrete Morse function correspondence

A discrete gradient vector field $W$ (matching on $\vec{H}(X)$) is valid if:
- $W = \{(\sigma_i, \tau_i) : \sigma_i \to \tau_i \in \vec{H}(X)\}$ 
- Each cell appears in **at most one pair**
- Reversing matched arcs yields an acyclic digraph $\vec{H}(X)_W$

The **unmatched cells** in $W$ are the critical cells of the induced discrete Morse function.

## Physical Intuition / Derivation

### Building the Hasse diagram

Consider a triangulated 2D surface:
- Vertices (0-cells), edges (1-cells), and triangles (2-cells)
- A triangle $\tau$ contains three edges, each of which is an immediate face: $e \to \tau$
- Each edge contains two vertices: $v \to e$
- The Hasse diagram stacks these relationships vertically by dimension

The direction of arcs is **upward in dimension**: lower-dimensional cells point to higher-dimensional cells that strictly contain them.

### Why this representation matters

The Hasse diagram compresses the combinatorial topology of $X$ into a graph that:
1. **Eliminates redundancy**: only cover relations are shown (no transitive arcs)
2. **Makes algorithms efficient**: incidence information is directly readable as adjacencies
3. **Enables discrete calculus**: matchings on this graph correspond to discrete vector fields and Morse theory

### Discrete Morse theory connection

A **discrete Morse function** $f: X \to \mathbb{R}$ assigns values to cells such that along any path in $\vec{H}(X)$, values generally increase. Rather than compute $f$ directly, **Forman's correspondence** lets us work with matchings:
- A matching pairs cells $(σ, τ)$ with $\sigma \to \tau$ 
- Reversing the matched arcs creates a gradient flow $\vec{H}(X)_W$
- Critical cells (unmatched) trap flow and determine topology
- The complex collapses to a smaller homotopy-equivalent Morse complex

This is powerful: minimizing unmatched cells = reducing critical points = simplifying the topology for downstream computation.

## Applications in Engineering

### Topological data analysis and simplification
- **Persistent homology**: Hasse diagrams provide the filtration structure needed to track birth/death of topological features
- **Mesh simplification**: discrete Morse matching reduces complex geometries while preserving homotopy type
- Applied in medical imaging (segmentation), material science (pore networks)

### Computational topology
- **Optimal Morse matching**: minimize unmatched cells in $\vec{H}(X)_W$ to reduce homology computation cost
- **Treewidth-bounded complexes**: restrict to complexes where $H(X)$ has bounded treewidth, enabling polynomial-time algorithms
- Used in finite element analysis for efficient computation of cohomology and persistent features

### Combinatorial algorithms
- **Graph coloring and reductions**: Hasse diagrams of simplicial complexes reduce to graph coloring problems
- **Erasibility testing**: determine if 2D complexes can be collapsed to lower dimensions (structural simplification)
- Applications in compiler optimization, circuit design where hierarchical structures are common

### Computational geometry
- **CW complex representation**: compact encoding of subdivisions (e.g., cell decompositions of manifolds)
- **Incremental complex construction**: Hasse diagrams naturally support adding cells while maintaining incidence relations
- Used in computational crystallography, where crystal structures are CW complexes

## Common Mistakes / Pitfalls

### 1. Confusing direction of arcs
**Mistake**: Drawing arcs downward from higher to lower dimension.  
**Correction**: Arcs point *upward* in dimension: $\sigma \to \tau$ means $\dim(\sigma) < \dim(\tau)$.

### 2. Including transitive arcs
**Mistake**: Adding arcs between all faces contained in a cell (e.g., $v \to \tau$ for a vertex-to-triangle in 2D).  
**Correction**: Hasse diagrams show *only* cover relations (immediate faces). If $\sigma \subset \rho \subset \tau$ with all dimensions distinct, draw $\sigma \to \rho$ and $\rho \to \tau$, not $\sigma \to \tau$.

### 3. Misapplying discrete Morse matching
**Mistake**: Assuming any matching on $\vec{H}(X)$ defines a valid gradient field.  
**Correction**: The matching must induce an acyclic digraph $\vec{H}(X)_W$ after reversing matched arcs. Not all matchings satisfy this; careful verification is required.

### 4. Ignoring treewidth constraints
**Mistake**: Assuming algorithms for optimal Morse matching scale to arbitrary complexes.  
**Correction**: Optimal matching is NP-hard in general; tractability is restricted to bounded-treewidth complexes. Check the underlying