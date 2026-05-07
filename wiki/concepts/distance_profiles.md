# Distance Profiles

## Definition

A **distance profile** is a discrete representation of distances from a vertex to a reference set, used in metric graph analysis. Given a vertex $u \in V(G)$ and a reference set $Z \subseteq V(G)$, the **rounded distance profile** of $u$ to $Z$ is the vector of discretized distances:

$$\text{profile}_Z(u) = \left( \left\lfloor \frac{\text{dist}_G(u, z_1)}{\delta} \right\rfloor, \left\lfloor \frac{\text{dist}_G(u, z_2)}{\delta} \right\rfloor, \ldots, \left\lfloor \frac{\text{dist}_G(u, z_{|Z|})}{\delta} \right\rfloor \right)$$

where $\delta > 0$ is a discretization scale parameter, and $\text{dist}_G(u, v)$ denotes the graph distance between $u$ and $v$ in $G$.

The notation $d_{\text{dist}}(u, v)$ denotes the unique integer $i$ such that:
$$i \cdot \delta \leq \text{dist}_G(u, v) < (i+1) \cdot \delta$$

This is a **rounded distance** at granularity $\delta$.

## Key Equations

**Discretization scale relationship:**
$$\delta = \frac{\varepsilon}{100R}$$
where $R = \min_{(p,q) \in M} \text{dist}(p,q)$ is the minimum distance between terminal pairs and $\varepsilon$ is the precision parameter.

**Bounded distance constraint:**
For distinct terminal pairs $(p_i, q_i), (p_j, q_j) \in M$:
$$\text{dist}(p_i, q_j) \leq (1-\varepsilon)R = R - 100\delta$$

**Number of distinct profiles (Lemma 5.5):**
Given a set $Z$ of $m$ reference vertices, the number of distinct rounded distance profiles to $Z$ is bounded by:
$$\text{distinct profiles} = O(m^4 \varepsilon^{-4})$$

**Separation counting (Lemma 5.6):**
For a set $X$ contained in at most $\alpha$ paths of length at most $\beta R$:
$$\text{separated pairs} = O\left(\alpha^4 \varepsilon^{-4}(1+\beta\varepsilon^{-1})^4\right)$$

## Physical Intuition / Derivation

### Why Discretize?

In planar metric analysis, direct comparison of continuous distances becomes combinatorially complex. By rounding distances to integer multiples of $\delta$, we dramatically reduce the number of distinguishable configurations while maintaining sufficient resolution via the parameter choice $\delta = \varepsilon/(100R)$.

### Separation via Profiles

The key insight is that **pairs with identical distance profiles cannot be separated by a path set**. Consider a separating set $X$ (a bottleneck); if two terminal pairs $(p_i, q_i)$ and $(p_j, q_j)$ share the same rounded distance profile to vertices near $X$, then $X$ cannot distinguish them—they must have similar topological relationships to $X$.

### Scaling Argument

The scale $\delta$ is calibrated so that:
- Differences of order $\delta$ are "negligible" relative to the minimum terminal distance $R$
- This allows grouping pairs by their discretized profiles
- Groups with ≥3 pairs sharing identical profiles cannot all be separated simultaneously

### Stratification

By organizing terminal pairs into equivalence classes based on distance profiles:
$$\text{Pairs}(M) = \bigcup_{p \in \text{Profiles}(Z)} \text{Group}_p$$

A separating set can only break apart the class structure where groups have size ≤2, bounding total separated pairs.

## Applications in Engineering

### Network Design & Routing
- **Capacity planning:** Distance profiles enable clustering of network nodes with similar topological properties, reducing optimization complexity
- **QoS guarantees:** By identifying nodes with identical routing profiles, engineers can apply uniform service policies without individual analysis

### VLSI & Circuit Layout
- **Critical path analysis:** Discretized distance profiles help identify which net pairs have equivalent timing characteristics
- **Congestion modeling:** Profile-based clustering predicts bottleneck locations in chip designs

### Transportation Networks
- **Facility location:** Distance profiles group demand nodes, enabling efficient placement of distribution hubs
- **Load balancing:** Profiles identify equivalent routing options for traffic distribution

### Wireless Sensor Networks
- **Topology control:** Nodes with similar distance profiles to landmarks can share communication strategies
- **Localization:** Quantized distance profiles provide robustness to measurement noise while preserving spatial structure

### Mesh Generation & Spatial Data Structures
- **Adaptive refinement:** Mesh regions with similar distance profiles to boundaries can use uniform refinement strategies
- **Complexity reduction:** Profile-based abstraction simplifies geometric algorithms on dense point sets

## Common Mistakes / Pitfalls

1. **Over-discretization:** Choosing $\delta$ too large loses critical geometric information. The bound $\delta = \varepsilon/(100R)$ is carefully calibrated—arbitrary choices break the separation guarantees.

2. **Confusing profiles as unique identifiers:** Distance profiles are *not* bijections to points. Multiple vertices can share identical profiles; this is the *point*—it enables grouping and complexity reduction. Using profiles to uniquely identify vertices is incorrect.

3. **Ignoring the context of $R$:** The scale $\delta$ depends on the minimum terminal distance $R$. Comparing profiles across instances with different $R$ values without rescaling is invalid.

4. **Misapplying separation bounds:** Lemma 5.6's $O(\alpha^4\varepsilon^{-4}(1+\beta\varepsilon^{-1})^4)$ bound requires that $X$ be contained in $\alpha$ paths of length $\leq \beta R$. If $X$ is distributed arbitrarily, the bound is vacuous.

5. **Profile independence assumption:** Distance profiles to different reference sets are *correlated*, not independent