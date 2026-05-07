# degree range

## Definition

A **degree range** is a pair of constraints $(\delta^-, \delta^+)$ that specifies the permissible degrees for a vertex in a graph or pseudo-configuration. For a vertex $v$ in a pseudo-configuration $(Z^\circ, \delta^-, \delta^+)$, the degree range constrains the degree $d_G(v)$ of the corresponding vertex in an embedded graph $G$ such that:

$$\delta^-(v) \leq d_G(v) \leq \delta^+(v)$$

In the discrete mathematical context of planar graph analysis and discharging arguments, degree ranges allow flexible specification of vertex degree requirements by defining both a **lower bound** $\delta^-(v)$ and an **upper bound** $\delta^+(v)$ for each vertex $v$.

## Key Equations

For a vertex $v$ in a pseudo-configuration, the degree constraint is:

$$\delta^-(v) \leq d_G(v) \leq \delta^+(v)$$

where:
- $\delta^-(v)$ is the minimum allowable degree
- $\delta^+(v)$ is the maximum allowable degree (possibly $\infty$)
- $d_G(v)$ is the actual degree in the embedding

**Canonical degree range types** (from Lemma 9.12):
1. **Single degree**: $\delta^-(v) = \delta^+(v) = k$ (exact degree requirement)
2. **Bounded interval**: $\delta^-(v) < \delta^+(v) < \infty$ (e.g., the range $[5,6]$)
3. **Infinite range**: $\delta^-(v) < \delta^+(v) = \infty$ (degree at least $\delta^-(v)$)

## Physical Intuition / Derivation

### Motivation from Graph Embeddings

Degree ranges emerge naturally when embedding reducible configurations into pseudo-configurations. Rather than rigidly specifying exact degrees for every vertex, degree ranges provide flexibility:

- **Exact constraints** ($\delta^- = \delta^+$) are used when the embedding depends critically on a specific vertex degree
- **Range constraints** accommodate multiple valid embeddings without exhaustively listing each case
- **Infinite ranges** permit local variations when global structure is what matters

### Closure Under Operations

Degree ranges are **closed under interval intersection**: if two configurations have degree ranges for the same vertex, their intersection remains one of the canonical types above. This stability under set operations makes degree ranges tractable for computational verification (as in Algorithm A.8.2).

### Cut-Vertex Extension

When extending a configuration with a cut-vertex to remove the cut-vertex, we adjust degree ranges for the new vertices:

$$\delta^-_u(u) = d_{Z^u}(u) + 1, \quad \delta^+_u(u) = \infty$$

This indicates that the introduced vertex $u$ must have at least one additional neighbor (beyond the inherited structure) but can absorb any number of further edges.

## Applications in Engineering

### Graph Theory & Combinatorics
- **Planar graph algorithms**: Discharging rules use degree ranges to prove planarity properties and chromatic number bounds
- **Reducible configuration detection**: Degree ranges efficiently specify when a configuration can be embedded in a target graph
- **Computational verification**: Algorithms (e.g., A.8.2) systematically check all degree range combinations to prove structural properties

### Network Design
- **Constraint specification**: Degree ranges allow specification of node connectivity requirements without over-constraining designs
- **Flexibility in topology**: Networks can satisfy structural properties while maintaining variable node degrees within acceptable bounds
- **Load balancing**: Permits nodes to operate within degree ranges (e.g., communication hubs with $d \in [50, 200]$ connections)

### Configuration Testing & Validation
- **Automated verification**: C++ implementations can enumerate all pseudo-configurations satisfying given degree range constraints
- **Proof assistance**: Systematic exploration of degree range combinations (as in Lemma A.1) supports formal verification of mathematical theorems
- **Search space reduction**: Canonical forms (single degree, bounded interval, infinite) prune the space of configurations to check

## Common Mistakes / Pitfalls

1. **Confusing degree range with degree sequence**: A degree range applies to *individual vertices*, not the sequence of all vertex degrees. Different vertices may have different ranges.

2. **Assuming ranges are always bounded**: Degree ranges may be infinite ($\delta^+ = \infty$). Algorithms must handle unbounded upper bounds carefully; they are not simply enumerable.

3. **Neglecting closure under intersection**: When combining constraints from multiple sources, intersection of ranges must respect the canonical three types. Arbitrary interval intersections may not remain valid degree ranges.

4. **Over-constraining with single degrees**: Using $\delta^- = \delta^+$ everywhere may eliminate valid embeddings. Ranges should be as loose as the problem allows.

5. **Ignoring cut-vertex semantics**: When extending configurations with cut-vertices, the degree range for new vertices must account for the forced extra neighbor; setting $\delta^+_u(u) = \infty$ is not arbitrary but necessary for correctness.

6. **Misinterpreting embedding conditions**: A homomorphism $\varphi$ from a configuration to a pseudo-configuration exists only if actual degrees satisfy the ranges; failing to check this condition leads to incorrect reducibility claims.

## See Also

- [[pseudo-configuration]] — graph structure with degree range constraints
- [[discharging rules]] — rules for charge redistribution in planar graph proofs
- [[reducible configuration]] — configuration that can be embedded in any graph satisfying structural properties
- [[homomorphism (graphs)]] — structure-preserving map between configurations
- [[planar graph coloring]] — application domain for degree-range-based discharging arguments

## Sources

- Graph coloring and discharging rule verification (Lemma 9.12, Lemma A.1)
- Algorithm A.8.2: pseudo-code for degree range enumeration and configuration embedding
- Figure 6: discharging rules for planar graph analysis
- Cut-vertex handling in configuration embeddings (conditions Z3, Z5)