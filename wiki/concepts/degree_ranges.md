# degree ranges

## Definition

**Degree ranges** are intervals $[\delta^-_{\circ}(v), \delta^+_{\circ}(v)]$ assigned to vertices in a combinatorial structure that specify the permissible range of vertex degrees during iterative refinement or search procedures. For a vertex $v$, the range represents the minimum degree $\delta^-_{\circ}(v)$ and maximum degree $\delta^+_{\circ}(v)$ that $v$ is allowed to attain.

More formally, a configuration is a triple $(Z_{\circ}, \delta^-_{\circ}, \delta^+_{\circ})$ where:
- $Z_{\circ}$ is a combinatorial structure (such as a planar graph or dart system)
- $\delta^-_{\circ}, \delta^+_{\circ}: V(Z_{\circ}) \to \mathbb{N}$ assign lower and upper degree bounds
- For each vertex $v$: $\delta^-_{\circ}(v) \leq d_{Z_{\circ}}(v) \leq \delta^+_{\circ}(v)$

where $d_{Z_{\circ}}(v)$ denotes the actual degree of $v$ in $Z_{\circ}$.

## Key Equations

**Degree validity condition:**
$$d_{Z_{\circ}}(v) \geq \delta^-_{\circ}(v) \quad \text{for all inner vertices } v$$

**Intersection rule for identified vertices:**
When vertices $u$ and $v$ are identified, their resulting degree range is:
$$[\delta^-_{\circ}(u \equiv v), \delta^+_{\circ}(u \equiv v)] = [\delta^-_{\circ}(u), \delta^+_{\circ}(u)] \cap [\delta^-_{\circ}(v), \delta^+_{\circ}(v)]$$

**Termination condition:**
All vertices reach single-specified degrees:
$$\delta^-_{\circ}(v) = \delta^+_{\circ}(v) = d_{Z_{\circ}}(v) \quad \text{for all vertices } v$$

## Physical Intuition / Derivation

Degree ranges generalize fixed degree specifications to **flexible constraints**. Rather than requiring each vertex to have exactly one specified degree $\delta(v)$, ranges allow a vertex to achieve any degree within $[\delta^-_{\circ}(v), \delta^+_{\circ}(v)]$. This is essential for:

1. **Adaptive search**: Subdividing the space of valid configurations by progressively narrowing ranges
2. **Infeasibility detection**: If the intersection of ranges becomes empty after vertex identification, the configuration is abandoned as infeasible
3. **Minimizing branching**: Rather than splitting all degree ranges simultaneously, the algorithm prioritizes:
   - First, vertices with **single-specified degrees** (where $\delta^-_{\circ}(v) = \delta^+_{\circ}(v)$) that violate degree constraints
   - Then, vertices with proper ranges that satisfy $\delta^-_{\circ}(v) \leq d_{Z_{\circ}}(v)$

The algorithm iteratively refines configurations by:
- **Detecting errors**: $d_{Z_{\circ}}(v) < \delta^-_{\circ}(v)$ signals infeasibility (sub-degree error)
- **Splitting ranges**: When no error exists but a range remains unsplit, choose a vertex with $\delta^-_{\circ}(v) < \delta^+_{\circ}(v)$ and split into two branches:
  - One with $\delta^-_{\circ}(v) := \delta^+_{\circ}(v) := \delta^-_{\circ}(v)$ (single degree)
  - One with $\delta^-_{\circ}(v) := \delta^-_{\circ}(v) + 1$ (remaining range)

This strategy ensures exponential-time termination while exploring only feasible configurations.

## Applications in Engineering

**Combinatorial Optimization:**
- Mesh generation and refinement, where vertex degree constraints must be satisfied flexibly
- Graph drawing algorithms requiring degree-bounded realizations

**CAD/Computational Geometry:**
- Topological consistency checking in subdivision surfaces or polyhedral structures
- Validating that degree constraints remain satisfiable after local modifications

**Circuit Design:**
- Port/pin degree constraints in netlists with optional connections

**Constraint Satisfaction:**
- General CSP solvers that maintain interval domains; degree ranges are a specialized case

## Common Mistakes / Pitfalls

1. **Assuming ranges are independent**: When vertices are identified, ranges must be **intersected**, not unioned. An empty intersection signals infeasibility and requires backtracking.

2. **Checking the wrong error condition**: Use $d_{Z_{\circ}}(v) < \delta^-_{\circ}(v)$ (actual degree below minimum), not $d_{Z_{\circ}}(v) < \delta(v)$ for a single specified degree. The latter is only valid when $\delta^-_{\circ} = \delta^+_{\circ}$.

3. **Premature splitting**: Do not split all ranges uniformly. The algorithm prioritizes single-specified degrees first to trigger cascades of necessary identifications before expensive branching.

4. **Ignoring boundary conditions**: Boundary vertices (with incident boundary arcs) have different degree-issue conditions than inner vertices. A boundary vertex with $\delta(v) = d_{Z_{\circ}}(v)$ may require edge addition, converting it to an inner vertex.

5. **Loop formation**: After vertex identifications, always check for self-loops, which invalidate the configuration.

## See Also

- [[vertex identification]]
- [[combinatorial homomorphism]]
- [[constraint propagation]]
- [[planar graph refinement]]
- [[degree specification]]

## Sources

- Lecture/paper excerpt: Algorithm A.4.4, A.4.5, A.4.7, A.4.9 describing degree-range resolution procedures
- Context: Combinatorial geometry and topological constraint solving