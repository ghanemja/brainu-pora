# near-triangulation

## Definition

A **near-triangulation** is a plane graph obtained by removing the outer face from a triangulation. Formally, if $G$ is a triangulation of the plane, a near-triangulation $\tilde{Z}$ is constructed by taking a planar graph $Z$ (the interior) and adding a cycle $R$ (the outer facial cycle or "ring") such that all interior faces are triangles.

More precisely: A configuration $(Z, \delta)$ is a plane graph $Z$ with a **degree specification** $\delta : V(Z) \to \mathbb{Z}_{\geq 0}$ for each vertex. The **free completion** $\tilde{Z}$ of configuration $(Z, \delta)$ is a near-triangulation formed by:

1. Adding an outer cycle $R$ disjoint from $Z$
2. Connecting vertices on the boundary of $Z$ to vertices on $R$
3. Ensuring all interior faces are triangles
4. The ring $R$ becomes the unique non-triangular outer face

## Key Equations

### Ring Length Formula

The length of the ring $R = R(Z)$ in the free completion is:

$$|R| = \sum_{v \in V(Z)} (\delta(v) - d_Z(v)) - t$$

where:
- $\delta(v)$ = prescribed degree of vertex $v$
- $d_Z(v)$ = degree of $v$ in the graph $Z$
- $t$ = length of the outer facial walk of $Z$

**Alternative form:**

$$|R| = \sum_{v \in V(Z)} \delta(v) - 2|E(Z)| - t$$

### Extendibility Hierarchy

For a coloring $\varphi$ of ring $R$:
- **0-extendible**: $\varphi$ extends directly to a valid coloring of $\tilde{Z}$
- **$i$-extendible** (for $i > 0$): Either $(i-1)$-extendible, or extendible after applying Kempe changes in $G - V(Z)$

## Physical Intuition / Derivation

### Conceptual Foundation

Think of a near-triangulation as an "incomplete triangulation"—we have a planar graph whose interior is fully triangulated, but whose boundary is not yet closed. The ring $R$ represents the "deficit" vertices needed to complete the structure into a full triangulation.

### Why the Ring Length Formula Works

The ring must accommodate the total degree "slack" in the configuration:

1. Each vertex $v$ in $Z$ has a prescribed degree $\delta(v)$ in the complete triangulation
2. Currently $v$ has degree $d_Z(v)$ in the local graph
3. The difference $\delta(v) - d_Z(v)$ is the number of edges that must connect to the ring
4. Summing over all vertices gives the total edge count, but we must subtract $2|E(Z)|$ (each interior edge counted twice) and $t$ (the outer boundary)

### Role in 4-Color Theorem Proof

Near-triangulations are fundamental to Kempe's reducibility strategy:

- A configuration is **reducible** if any 4-coloring of $G - V(Z)$ can be modified (via Kempe chain swaps) so its restriction to $R$ extends to a valid 4-coloring of $\tilde{Z}$
- This reduces the global 4-coloring problem to local configurations
- Finite families of unavoidable configurations (all reducible) form the basis of computer-assisted proofs of 4CT

### Cut-Vertex Handling

The construction admits cut-vertices in $Z$ without ambiguity because the ring $R$ is determined purely by degree arithmetic, not topological connectivity.

## Applications in Engineering

### 1. Graph Planarization & Circuit Design
- Near-triangulations provide structured decompositions of planar graphs used in PCB layout and chip floorplanning
- Extracting near-triangulation configurations enables hierarchical routing algorithms

### 2. Mesh Generation & FEA Preprocessing
- Computational geometry uses near-triangulations as templates for adaptive mesh refinement
- Ring structure guides local vs. global refinement strategies in finite element analysis

### 3. Network Reliability Analysis
- Degree specifications $\delta(v)$ model redundancy requirements in planar communication networks
- Reducibility arguments parallel structural robustness verification

### 4. Combinatorial Optimization
- Configuration enumeration in near-triangulations bounds complexity of graph coloring problems
- Applied to register allocation in compiler design

### 5. Geometric Graph Drawing
- Hierarchical node placement respects near-triangulation boundaries to minimize edge crossings
- Ring structure constrains vertex positioning in force-directed layouts

## Common Mistakes / Pitfalls

### 1. Confusing Ring with Outer Face
**Error:** Treating the ring $R$ as identical to the outer facial walk of $Z$.

**Correction:** The ring $R$ is a *new* cycle added during free completion. The outer walk of $Z$ (length $t$) is absorbed into the degree deficit formula.

### 2. Incorrect Degree Counting
**Error:** Setting $\delta(v) = d_Z(v)$ for interior vertices, expecting $|R| = 0$.

**Correction:** $\delta(v)$ is the degree in the *completed* near-triangulation. Interior vertices generally satisfy $\delta(v) \geq 6$ (for triangulations). Degree deficit is $\delta(v) - d_Z(v) > 0$.

### 3. Ignoring Cut-Vertices
**Error:** Assuming $Z$ must be 2-connected for the free completion to be well-defined.

**Correction:** Cut-vertices in $Z$ are handled correctly; the ring formula and extendibility depend only on degree data, not connectivity.

### 4. Extendibility as Boolean Property
**Error:** Treating "$i$-extendible" as a discrete yes/no property independent of external graph structure.

**Correction:** $i$-extendibility is relative to the larger graph $G$ in which $(Z, \delta)$ is embedded. The same configuration may be extendible in one host graph but not another.

### 5. Underestimating Ring Complexity
**