# Noncrossing Instance

## Definition

A **noncrossing instance** is a combinatorial-geometric structure consisting of a set of vertex pairs $\{(p_i, q_i)\}$ in a metric space (typically embedded in the plane or on a graph) such that the shortest paths connecting them satisfy strict disjointness constraints. Formally, for a linked noncrossing instance with pairs $(p_1, q_1), (p_2, q_2), \ldots, (p_\ell, q_\ell)$:

1. All shortest paths $\lfloor p_i q_i \rfloor$ are pairwise internally disjoint
2. The paths satisfy a **separation property**: for any $i \neq j$, the paths $\lfloor p_i q_j \rfloor$ and $\lfloor p_j q_i \rfloor$ are disjoint
3. Each path has bounded length: $\text{dist}(p_i, q_i) \leq (1-\varepsilon)R$ for some constraint radius $R$ and error margin $\varepsilon > 0$

The structure arises in graph theory when studying **comatching** problems—finding the maximum number of disjoint path pairs under geometric constraints.

## Key Equations

### Separation Lemma (Lemma 2.1)

For any two distinct pair indices $i \neq j$, if paths $\lfloor p_i q_j \rfloor$ and $\lfloor p_j q_i \rfloor$ share a common vertex $u$, we obtain a contradiction:

$$2(1-\varepsilon)R \geq \text{dist}(p_i, q_j) + \text{dist}(p_j, q_i)$$

$$= \underbrace{\left[\text{dist}(p_i, u) + \text{dist}(u, q_j)\right]}_{\geq \text{dist}(p_i, q_j)} + \underbrace{\left[\text{dist}(p_j, u) + \text{dist}(u, q_i)\right]}_{\geq \text{dist}(p_j, q_i)}$$

$$\geq \text{dist}(p_i, q_i) + \text{dist}(p_j, q_j) > 2R$$

This violates the upper bound constraint, establishing disjointness.

### Cardinality Bound

The maximum number of pairs in a linked noncrossing instance is:

$$\ell = O(1/\varepsilon)$$

This bound is tight and represents a fundamental trade-off: larger error margins $\varepsilon$ permit more pairs, but only logarithmically.

## Physical Intuition / Derivation

### Why Noncrossing Instances Matter

Imagine attempting to route $\ell$ telephone cables through a region where each cable connects endpoint pairs $(p_i, q_i)$. If cables must follow shortest paths and remain physically disjoint (non-intersecting), how many cables can you accommodate?

This is the **noncrossing instance problem**.

### The Separation Lemma Intuition

The key insight is that **mixed crossings are forbidden**. If paths from pair $i$ and pair $j$ were allowed to intersect, we could create "shortcuts"—rerouting through the intersection point would violate the shortest-path assumption. 

The contradiction arises from the triangle inequality: if $u$ lies on both $\lfloor p_i q_j \rfloor$ and $\lfloor p_j q_i \rfloor$, then:
- The detour from $p_i$ to $q_j$ via $u$ must cost the same as the direct path (by optimality)
- But then the combined cost of both detours would exceed our global budget $2(1-\varepsilon)R$

### Topological Case Analysis

Through exhaustive case-by-case analysis of how pairs can be arranged topologically in the plane (see Figure 6 in the source), one shows that pairs must be arranged in a **double-ladder structure**: alternating $p_1, p_2, \ldots, p_\ell$ along one "rail" and $q_1, q_2, \ldots, q_\ell$ along another, with paths connecting them monotonically. This highly constrained geometry limits $\ell$ to $O(1/\varepsilon)$.

## Applications in Engineering

### 1. **Network Routing & Telecommunication**
Noncrossing instances model disjoint path routing problems where cables or fiber optics must avoid physical intersections. Applications include:
- **VLSI design**: routing multiple signal traces on circuit boards without crossings
- **Optical network design**: managing fiber bundle layouts in data centers

### 2. **Computational Geometry & Graph Theory**
- **Planar graph algorithms**: separation lemmas establish bounds on matching sizes in planar and bounded-genus graphs
- **Graph minor theory**: understanding structural properties of graphs through forbidden topological patterns

### 3. **Metric Space Approximation**
The VC-dimension framework (referenced in preliminaries) applies noncrossing analysis to:
- **Machine learning**: bounding VC dimension of geometric classifiers
- **Data structure design**: efficient nearest-neighbor query structures in metric spaces

### 4. **Approximation Algorithms**
Theorem 1.5 (cited as Theorem 1.7 in sources) provides approximation guarantees for:
- Maximum flow problems on planar graphs
- Disjoint path packing with length constraints

### 5. **Bounded-Genus Surfaces**
Extension to surfaces of Euler genus $g$ (Theorems 1.6, 1.18) enables:
- **Topological network optimization**: routing on biological membranes or manifold-based systems
- **Robotic path planning**: motion planning on curved constraint surfaces

## Common Mistakes / Pitfalls

### 1. **Confusing "Disjoint Paths" with "Noncrossing Pairs"**
- **Error**: Thinking any collection of internally-disjoint paths forms a noncrossing instance
- **Correction**: The separation property (Lemma 2.1) is *additional*; it forbids