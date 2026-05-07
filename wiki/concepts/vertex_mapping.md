# Vertex Mapping

## Definition

**Vertex mapping** is a function $\varphi: V(Z_1) \to V(Z^\circ)$ that associates vertices of a source graph or configuration $Z_1$ to vertices of a target graph or pseudo-configuration $Z^\circ$, subject to structural and degree constraints.

In the context of configuration containment checking, a vertex mapping must satisfy:

1. **Degree preservation**: vertices map to vertices with compatible degree constraints
2. **Structural preservation**: the mapping respects the graph topology (homomorphism property)
3. **Fixed-point constraints**: vertices $v \in V(Z_1)$ satisfying $\delta_1^-(v) = \delta_1^+(v) > 8$ must map to a designated center vertex $c^\circ$

Formally, for a configuration $(Z_1, \delta_1^-, \delta_1^+)$ with special dart $f = xy$:
$$\varphi: V(Z_1) \to V(Z^\circ) \text{ such that } \forall v \in V(Z_1), \delta_1^-(v) = \delta_1^+(v) > 8 \implies \varphi(v) = c^\circ$$

## Key Equations

### Degree Constraint Matching

For a dart $f = xy$ in $Z_1$ with endpoints having degrees $d_x = \delta_1^-(x)$ and $d_y = \delta_1^-(y)$, we seek a dart $f^\circ = x^\circ y^\circ$ in $Z^\circ$ such that:

$$\delta^\circ(x^\circ) = d_x \text{ and } \delta^\circ(y^\circ) = d_y$$

### Restricted Degree Range

For pseudo-configurations, vertices maintain degree ranges. For mapped vertices $v \in V(Z_1)$:

$$\delta_1^-(v) \leq \delta^\circ(\varphi(v)) \leq \delta_1^+(v)$$

This is particularly important for cut-vertices whose auxiliary neighbors have bounded degree ranges.

## Physical Intuition / Derivation

### Why Vertex Mapping Matters

In graph-based configuration analysis (e.g., planar graph verification, discharging arguments), determining whether one configuration "contains" another requires establishing a structural embedding. Vertex mapping formalizes this correspondence.

### The Dart-Centric Approach

Rather than mapping vertices directly, the algorithm **maps darts** (directed edges). This is more efficient because:

1. **Degree information is local**: a dart $f = xy$ immediately reveals the degrees of both endpoints
2. **Special vertex identification**: the special dart $f$ chosen by `maximumDartDegree` lexicographically maximizes endpoint degrees, providing a canonical anchor point
3. **Constraint propagation**: once the special dart maps to a candidate target dart $f^\circ$, the mapping of its endpoints is partially determined

### The Role of Cut-Vertices

Cut-vertices are special because they may have constrained degrees (where $\delta_1^-(v) = \delta_1^+(v)$). These must map to the **center vertex** $c^\circ$ in the target pseudo-configuration. This reflects a structural invariant: certain critical vertices cannot map elsewhere without violating the configuration's properties.

### Algorithm Flow

1. **Classify target darts** (`dartsByDegree`): organize darts in $Z^\circ$ by the degree pair $(d_y, d_x)$ of their head and tail
2. **Enumerate candidates** (`containConf`): for each configuration in $K$ with special dart $f = xy$, iterate over candidate target darts with matching endpoint degrees
3. **Verify homomorphism** (`rootedContainConf`): check if a full graph homomorphism exists with the dart mapping as root constraint

### Efficiency Optimization

The classification step is bounded: only darts with endpoint degrees $\leq \text{CONF\_DEG\_MAX} = 12$ need classification, since configurations have maximum $\delta = 12$. This keeps the complexity manageable.

## Applications in Engineering

### 1. Planar Graph Verification
Vertex mapping is essential in discharging method algorithms that verify the four-color theorem or planarity properties. Configuration containment relies on determining whether a subgraph locally matches a forbidden configuration.

### 2. Network Topology Analysis
In network design, vertex mapping identifies whether a network contains critical subgraph patterns (e.g., bottlenecks, dense clusters) by matching vertex degree profiles.

### 3. Computational Geometry & Mesh Generation
When validating triangulations or mesh quality, vertex mapping ensures that local vertex neighborhoods have expected degree constraints. This prevents degenerate elements.

### 4. Pattern Recognition in Graph Databases
Graph database systems use vertex mapping to search for query patterns within large graphs, with degree constraints serving as efficient filtering mechanisms.

### 5. Compiler Optimization & Data Flow Analysis
In compiler intermediate representations (IR), vertex mapping helps identify isomorphic subgraphs representing equivalent computational patterns, enabling code optimization and refactoring.

## Common Mistakes / Pitfalls

### 1. Confusing Vertex Mapping with Graph Isomorphism
**Mistake**: Assuming vertex mapping requires a bijection.  
**Reality**: A valid homomorphism is many-to-one; multiple source vertices may map to the same target vertex. Only special vertices (cut-vertices with $\delta^-(v) = \delta^+(v)$) have fixed mappings.

### 2. Ignoring Degree Constraints
**Mistake**: Mapping a vertex to a target vertex without verifying $\delta_1^-(v) \leq \delta^\circ(\varphi(v)) \leq \delta_1^+(v)$.  
**Reality**: This violates the configuration's structural constraints and will cause the containment check to fail.

### 3. Wrong Special Dart Selection
**Mistake**: Choosing the special dart arbitrarily.  
**Reality**: The special dart must be selected by `maximumDartDegree` (lexicographic maximum of endpoint degrees). This ensures a canonical choice needed for consistent containment testing.

### 4. Missing Center Vertex Constraint
**Mistake**: Forgetting to enforce that vertices $v$ with $\delta_1^-(v) = \delta