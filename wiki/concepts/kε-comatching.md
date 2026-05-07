# (k,ε)-comatching

## Definition

A **(k,ε)-comatching** is a variant of ε-comatching introduced to analyze coreset bounds for geometric optimization problems (particularly k-center) on graphs with restricted topology. It represents a collection of pairs of vertices that satisfy distance constraints with respect to a parameter $k$ and approximation tolerance $\varepsilon$.

For an unweighted graph $G = (V, E)$ and integer $d \geq 1$, a **d-comatching** is a family $\mathcal{M}$ of pairs of vertices $(p, q) \in V \times V$ such that:

1. **Separation condition**: For every $(p, q) \in \mathcal{M}$, we have $\text{dist}(p, q) > d$
2. **Proximity condition**: For every distinct pairs $(p, q), (p', q') \in \mathcal{M}$, we have $\text{dist}(p, q') \leq d$

A **d-comatching** is equivalently an $\varepsilon$-comatching for any $\varepsilon > 0$ such that $d = \lfloor 1/\varepsilon \rfloor$.

The **(k,ε)-comatching** extends this concept to the setting of k-center problems, where the structure must encode information about multiple facility locations and their interactions under ε-approximation constraints.

## Key Equations

**ε-comatching size bounds** by graph class:

$$\begin{aligned}
\text{Simple polygons:} \quad &O(1/\varepsilon^2) \\
\text{Planar graphs:} \quad &\text{poly}(1/\varepsilon) \\
\text{Bounded genus } g:\ \quad &O(g^4 \varepsilon^{-8}) \cdot L_{\text{planar}}(1/\varepsilon) \\
\text{H-minor-free:} \quad &2^{\text{poly}_H(1/\varepsilon)}
\end{aligned}$$

**k-center coreset size bounds** (Table 1):

| Graph Class | k-Center Coreset Bound |
|---|---|
| Trees | $\Omega(2^{1/\varepsilon})$ when $k \sim 1/\varepsilon$ |
| Planar | $(1/\varepsilon)^{2^{O(k)}}$ |
| Bounded genus $g$ | $\text{poly}(g) \cdot (1/\varepsilon)^{2^{O(k)}}$ |
| H-minor-free | $k^{\text{poly}_H(1/\varepsilon)}$ |

## Physical Intuition / Derivation

### Why (k,ε)-comatching?

Standard **ε-comatching** exhibits *symmetry* between source points (p-points) and query points (q-points). Both roles are interchangeable in distance constraints. This symmetry simplifies analysis.

**k-center coreset** problems break this symmetry: we need to simultaneously handle:
- $k$ facility locations (asymmetric role)
- Distance approximations to each facility
- Cross-facility distance constraints

The (k,ε)-comatching variant encodes this asymmetry explicitly.

### Building Intuition

Consider a metric space on a graph:

1. A **d-comatching pair** $(p, q)$ is "far" internally (distance $> d$) but "close" externally—any other pair in the matching is at distance $\leq d$ from $q$ (or $p$).

2. This represents a *witness pair* that proves a coreset cannot be too small. If you remove $(p, q)$ from consideration, nearby pairs become indistinguishable under ε-approximation.

3. For **k-center**, (k,ε)-comatching encodes multiple such witness structures that must be simultaneously preserved.

### Why Bounded Genus Matters

The bound for bounded genus graphs,
$$O(g^4 \varepsilon^{-8}) \cdot L_{\text{planar}}(1/\varepsilon),$$
arises from **cutting the surface** along $O(g)$ shortest paths. Each cut reduces the problem to planar case analysis, with the polynomial dependence on $g$ accounting for interaction between cuts.

## Applications in Engineering

### 1. **Facility Location & Network Design**
- k-center problems optimize placement of service facilities (hospitals, fire stations, data centers)
- (k,ε)-comatching provides certified coreset sizes for approximation algorithms
- Enables efficient computation on large geographic/network graphs

### 2. **Geographic Information Systems (GIS)**
- Computing spatial coverage with approximate distance guarantees
- Planar/bounded-genus assumption matches real terrain embedding constraints
- Coreset bounds inform data structure memory requirements

### 3. **Mobile & Wireless Network Planning**
- k-center models optimal transmitter placement for coverage
- Coreset algorithms reduce problem instance size while maintaining ε-approximation
- Critical for network optimization in large service regions

### 4. **Graph Algorithm Certification**
- (k,ε)-comatching lower bounds prove hardness of coreset compression
- Separates tractable graph classes (planar, bounded genus) from intractable ones (K₅-minor-free)
- Guides algorithm selection and complexity analysis

### 5. **Computational Geometry**
- Simplicial complex preservation under metric simplification
- Essential for mesh refinement and geometric data structures with accuracy guarantees

## Common Mistakes / Pitfalls

### 1. **Confusing d-comatching with ε-comatching**
- A d-comatching is **not** an ε-comatching; rather, it is an ε-comatching for $\varepsilon \approx 1/d$
- The discrete parameter $d$ converts to continuous $\varepsilon$ via quantization

### 2. **Ignoring the asymmetry**
- (k,ε)-comatching breaks the p/q symmetry of standard ε-comatching
- Analysis cannot simply reuse planar ε-comatching bounds;