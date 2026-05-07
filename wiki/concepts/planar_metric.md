# planar metric

## Definition

A **planar metric** is a metric space $(V, \text{dist})$ where the underlying point set $V$ can be embedded in the Euclidean plane (or equivalently, admits a planar graph representation), and the distance function $\text{dist}$ respects the geometric constraints of this planar embedding.

More formally: A metric $(V, \text{dist})$ is planar if there exists a planar graph $G = (V, E)$ such that for any two vertices $u, v \in V$, the metric distance $\text{dist}(u,v)$ corresponds to the shortest-path distance in $G$, denoted $\text{dist}_G(u,v)$.

### Key Property: ε-Comatching Index

For a planar metric and a real parameter $\varepsilon \in (0,1)$, the **ε-comatching index** quantifies the maximum number of point pairs that can be "separated" (rendered uncrossable by disjoint paths) while maintaining metric distance constraints. 

**Theorem 1.5 (Comatching in Planar Metrics):** There exists a polynomial $L_{\text{planar}}$ such that for every $\varepsilon \in (0,1)$ and every planar metric $(V, \text{dist})$, the ε-comatching index is bounded by:

$$L_{\text{planar}}(1/\varepsilon) = O(\varepsilon^{-332} \log^{72}(\varepsilon^{-1}))$$

This is a **polynomial-in-$\varepsilon^{-1}$ bound**, not exponential.

## Key Equations

### Distance Scaling and Normalization

Given a clean ε-comatching instance $I = (G, M)$ with terminal pairs $M = \{(p_1, q_1), \ldots, (p_L, q_L)\}$, define the reference scale:

$$R := \min_{(p,q) \in M} \text{dist}(p,q)$$

The canonical distance unit is:
$$\delta := \frac{\varepsilon}{100R}$$

### Rounded Distance Profile

For vertices $u, v \in V(G)$, the **rounded distance profile** is the unique integer $i$ satisfying:
$$i \cdot \delta \leq \text{dist}_G(u,v) < (i+1) \cdot \delta$$

This discretization allows for combinatorial analysis while absorbing small metric perturbations.

### Separation Bound

For a set $X$ contained in the union of $\alpha$ paths each of length at most $\beta R$, the number of pairs of $M$ separated by $X$ is bounded by:

$$O\left(\alpha^4 \varepsilon^{-4}(1 + \beta\varepsilon^{-1})^4\right)$$

## Physical Intuition / Derivation

### Why Study Planar Metrics?

Planar metrics arise naturally in:
- **Road networks**: Cities and transportation systems embedded in 2D space
- **VLSI design**: Circuit routing on planar layers
- **Computational geometry**: Point sets in the plane under graph-based distances

The planar constraint fundamentally restricts how paths can interact—they cannot cross arbitrarily, creating topological constraints absent in general metric spaces.

### The Comatching Problem

A **comatching** (complementary matching) captures pairs of terminals that are "incompatible" in some sense—typically, pairs that cannot be simultaneously routed without overlap or conflict. The index measures the worst-case density of such conflicts.

**Intuition for the bound:**

1. **Local structure dominance** (Lemma 5.1): Global comatching is dominated by local configurations within small neighborhoods. The factor $O(L_{\text{local}}(\varepsilon)^9 \varepsilon^{-8})$ reflects that we must analyze 9 layers of local interactions, each incurring an $\varepsilon^{-8}$ cost.

2. **Non-crossing decomposition** (Lemma 5.2): Linked non-crossing instances (where terminal paths don't intersect) can be analyzed separately. The $\log^{72}$ term emerges from recursive depth analysis of nested path systems; the $(\varepsilon^{-1})^4$ term accounts for distance-profile differentiation.

3. **Topological constraint** (Lemma 5.3): The hardest bound, $\varepsilon^{-14}$, comes from analyzing the maximum number of distinct "separated configurations" possible in a planar graph. The planarity prevents exponential proliferation.

### Why Polynomial, Not Exponential?

In general (non-planar) metrics, the ε-comatching index can be **exponential** in $\varepsilon^{-1}$. Planarity's topological constraint—the Jordan curve theorem—limits path interactions, reducing the polynomial degree. This is a deep result: **planarity fundamentally simplifies metric complexity**.

## Applications in Engineering

### 1. **Transportation and Logistics**
- **Road network design**: Planar metrics model urban street networks. The comatching bound provides worst-case guarantees on demand-routing conflicts, informing infrastructure capacity planning.
- **Congestion analysis**: Predicts maximum simultaneous incompatible routing requests before gridlock.

### 2. **Semiconductor Design & VLSI**
- **Multi-layer routing**: Circuit traces on planar PCB layers must avoid crossing. The comatching index bounds the number of simultaneous routing conflicts at finer granularities.
- **Clock tree synthesis**: Ensures minimal skew by respecting planar distance metrics on silicon.

### 3. **Network Design & Telecommunications**
- **Backbone topology optimization**: Planar (or near-planar) network topologies minimize crosstalk and simplify routing protocols.
- **Fault tolerance**: The polynomial bound ensures graceful degradation; at most polynomial (not exponential) request pairs can be simultaneously disrupted.

### 4. **Computational Geometry & GIS**
- **Facility location**: Placing services (hospitals, fire stations) in planar environments, accounting for worst-case incompatible demand pairs.
- **Geometric approximation algorithms**: Planar metric structure enables PTAS (