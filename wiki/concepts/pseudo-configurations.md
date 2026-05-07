# pseudo-configurations

## Definition

A **pseudo-configuration** is an intermediate combinatorial structure used in computational geometry and mesh processing that represents a partially constructed or simplified configuration of darts and vertices without requiring the full closure properties of a complete configuration.

Formally, given:
- A dart graph $Z$ with vertices and directed edges (darts)
- A degree function $\delta: V \to \mathbb{Z}_{\geq 0}$ assigning target degrees to vertices
- A homomorphism $\varphi: Z \to \tilde{Z}$ mapping the original structure into a quotient pseudo-configuration $\tilde{Z}$

A pseudo-configuration $\tilde{Z}$ is characterized by:

1. **No-loop property**: For all darts $e$, we have $\text{head}(e) \neq \text{head}(\text{reverse}(e))$
2. **Degree respecting**: For inner vertices $v$: $d_{\tilde{Z}}(v) = \delta(v)$; for boundary vertices: $d_{\tilde{Z}}(v) < \delta(v)$

where $d_{\tilde{Z}}(v)$ denotes the actual degree of vertex $v$ in the pseudo-configuration.

## Key Equations

**Degree constraint for inner vertices:**
$$d_{\tilde{Z}}(v) = \delta(v) \quad \forall v \in V_{\text{inner}}$$

**Degree constraint for boundary vertices:**
$$d_{\tilde{Z}}(v) < \delta(v) \quad \forall v \in V_{\text{boundary}}$$

**Successor distance property**: For vertices with excess degree, distinct incident darts $e$ and $f$ must exist with successor distance:
$$\text{dist}_{\text{succ}}(e, f) = \delta(v)$$

## Physical Intuition / Derivation

Pseudo-configurations serve as **working snapshots** in an iterative refinement algorithm for constructing valid combinatorial structures (such as pseudo-triangulations or other configurations).

### Why They Exist

Direct construction of valid configurations is often computationally intractable. Instead:

1. **Start with a rough approximation** via Lemma 9.7, producing an initial pseudo-configuration $\tilde{Z}$
2. **Iteratively refine** the structure by identifying problematic vertices and edges
3. **Validate in stages**: check for loops, degree mismatches, and boundary violations after each refinement

### The Refinement Loop

The algorithm repeatedly:
- **Identifies violations** of degree constraints or topological properties
- **Issues identification requests** that trigger homomorphic quotient operations
- **Re-validates** the resulting pseudo-configuration

This staged approach is essential because:
- Loop detection requires complete reverse pointers (unavailable until $\tilde{Z}$ is fully constructed)
- Degree matching checks must precede loop detection to avoid spurious failures

## Applications in Engineering

### Computational Geometry
- **Pseudo-triangulation construction**: Computing visibility graphs and collision detection where exact triangulations are expensive
- **Mesh generation**: Progressive refinement of unstructured meshes toward valid configurations

### Robotics & Motion Planning
- **Configuration space approximation**: Building simplified representations of high-dimensional configuration spaces before full verification
- **Roadmap construction**: Staging vertex and edge validation in probabilistic roadmaps

### Topology & CAD Systems
- **Boundary representation**: Handling incomplete or partially-validated surface meshes during interactive design
- **Iterative validation**: Processing user edits to geometric models with deferred consistency checks

### Constraint Solving
- **Degree-constrained subgraph problems**: Building spanning subgraphs where degree constraints must be satisfied iteratively
- **Homomorphic quotient approximation**: Using pseudo-configurations as intermediate steps in graph compression

## Common Mistakes / Pitfalls

### 1. **Checking Loops Before Reverse Pointers are Final**
❌ **Wrong**: Testing for loops immediately after dart identification
✓ **Right**: Defer loop detection until the entire pseudo-configuration is constructed; reverse pointers must reach their final state

### 2. **Failing to Validate Degree Matching Before Identification**
❌ **Wrong**: Allowing identification of vertices with different target degrees $\delta(u) \neq \delta(v)$
✓ **Right**: Report a *degree mismatch error* and halt if $\varphi(u) = \varphi(v)$ but $\delta(u) \neq \delta(v)$

### 3. **Confusing Inner and Boundary Degree Constraints**
❌ **Wrong**: Requiring inner vertices to have $d < \delta$ (boundary condition)
✓ **Right**: Inner vertices must satisfy $d = \delta$ exactly; only boundary vertices allow $d < \delta$

### 4. **Boundary Triangle Construction Without Validation**
❌ **Wrong**: Adding the closing triangle $uvw$ without verifying $u$, $v$, $w$ are distinct
✓ **Right**: Check distinctness explicitly; report a *boundary error* if any pair coincides

### 5. **Insufficient Pointer Updates During Boundary Closure**
❌ **Wrong**: Adding darts $uw$ and $wu$ without updating successor/predecessor chains around all three vertices
✓ **Right**: Update pointers around $u$, $v$, and $w$ symmetrically; ensure $nil$ predecessors/successors are correctly placed

## See Also

- [[Pseudo-triangulations]] — Primary application domain; structures guaranteed by pseudo-configurations
- [[Dart graphs]] — Underlying combinatorial representation using directed edges
- [[Homomorphic identification]] — Quotient construction mechanism triggering refinement
- [[Degree-constrained graphs]] — The constraint satisfaction problem solved via iterative refinement
- [[Configuration spaces]] — Broader context in robotics and computational geometry

## Sources

- Lecture excerpt on pseudo-triangulation construction (Lemma 9.7 and iterative validation)
- Notes on dart-based combinatorial structures and pointer-based incidence lists
- Algorithm description for boundary vertex closure and degree identification requests