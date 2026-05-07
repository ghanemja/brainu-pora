# k-center coreset

## Definition

A **k-center coreset** is a small weighted subset of a metric space that preserves the optimal k-center clustering solution within a $(1+\varepsilon)$ approximation factor. Formally, for a metric space $(V, \text{dist})$ and parameters $k$ and $\varepsilon > 0$, an ε-coreset $S \subseteq V$ is a weighted point set such that for any choice of $k$ centers in $V$, the maximum distance from points in $V$ to their nearest center differs from the maximum distance for points in $S$ by at most a factor of $(1+\varepsilon)$.

More precisely, a subset $S$ with weights $w: S \to \mathbb{R}^+$ is an ε-coreset for k-center if:

$$\max_{p \in V} \text{dist}(p, C) \leq (1+\varepsilon) \max_{q \in S} \text{dist}(q, C)$$

for any choice of $k$ centers $C = \{c_1, \ldots, c_k\}$ in the metric space.

## Key Equations

**Coreset Size Bound (Planar Metrics):**

For ε-coreset construction on planar metrics or metrics of bounded genus $g$, the size scales as:

$$|S| = (1/\varepsilon)^{2^{O(k)}}$$

**General Size Bound:**

The coreset size depends on the maximum size of a $(k,\varepsilon)$-comatching $M_{k,\varepsilon}$:

$$|S| = O\left(\varepsilon^{-2} \cdot M_{k,\varepsilon} \cdot \log M_{k,\varepsilon}\right)$$

**Bounded Genus Extension:**

For graphs embedded in a surface of Euler genus $g$:

$$|S| = O(g^4 \varepsilon^{-8}) \cdot L_{\text{planar}}(1/\varepsilon)$$

where $L_{\text{planar}}$ is the polynomial bound for planar metrics.

## Physical Intuition / Derivation

### Why Coresets Matter

In large-scale clustering problems, maintaining all $n$ data points is computationally prohibitive. A coreset dramatically reduces problem size while guaranteeing solution quality. The k-center coreset specifically targets the **minimax criterion**: minimizing the maximum distance any point must travel to reach its cluster center.

### Construction Strategy

The coreset construction proceeds in phases:

1. **Identify Critical Points**: Use graph-theoretic structures (ε-matchings, ε-double ladders) to identify which points are "most constraining" for the k-center objective.

2. **Comatching Analysis**: An ε-comatching is a set of point pairs $(p_i, q_i)$ where:
   - $\text{dist}(p_i, q_i) > R$ (far apart)
   - $\text{dist}(p_i, q_j) \leq (1-\varepsilon)R$ for $i \neq j$ (each point blocks neighbors)
   
   These pairs capture topological constraints in the metric. The number of such pairs is polynomial in $1/\varepsilon$ for planar metrics due to the planar embedding's geometric constraints.

3. **Double Ladder Bounds**: A double ladder is a configuration of shortest paths in a planar graph that captures the interaction structure between constraint pairs. **Theorem 1.17** establishes that an ε-double ladder has size at most $L_{\text{planar}}(1/\varepsilon)$, a polynomial bound arising from planarity.

4. **Weighted Selection**: Select representative points proportionally to the comatching structure, weighted to account for point multiplicities.

### Why Planarity is Essential

The construction exploits the planar embedding to ensure:
- Shortest path interactions are geometrically constrained (paths cannot cross arbitrarily)
- The number of independent constraint configurations grows polynomially rather than exponentially
- **Non-planar graphs** (e.g., bounded treewidth) lack these guarantees, leading to exponential coreset bounds

## Applications in Engineering

### Facility Location & Network Design
- **Data center placement**: Approximate optimal placement of $k$ servers to minimize worst-case user latency in a road network
- **Distribution center problems**: Minimize maximum distance from any geographic region to nearest facility

### Mobile & Sensor Networks
- **Base station deployment**: Position $k$ communication hubs to cover a geographic area with bounded worst-case latency
- **Sensor network design**: Select representative sensors for real-time monitoring while maintaining coverage guarantees

### Computational Geometry & Graphics
- **Mesh simplification**: Identify critical mesh vertices such that coarser mesh preserves maximum deviation bounds
- **Point cloud processing**: Reduce point clouds while maintaining worst-case approximation to original geometry

### Machine Learning & Data Mining
- **Clustering on massive datasets**: Enable k-center clustering on graphs too large to store completely (e.g., social networks, biological networks)
- **Coreset-based approximation algorithms**: Construct approximate solutions faster by solving on coreset, then expanding

### Geographic Information Systems (GIS)
- **Road network analysis**: k-center solutions on planar planar-embedded road graphs with polynomial guarantees
- **Regional clustering**: Partition large geographic regions using bounded worst-case distance metrics

## Common Mistakes / Pitfalls

### 1. **Confusing $(1+\varepsilon)$ vs $\varepsilon$-approximation**
Coresets provide $(1+\varepsilon)$ relative approximation, not absolute ε-guarantees. For instance, if the true k-center distance is 100 and $\varepsilon=0.1$, the coreset gives distance ≤ 110, not ≤ 100.1.

### 2. **Assuming Size Independence from $k$**
Coreset size is **exponential** in $k$ even for planar metrics: $(1/\varepsilon)^{2^{O(k)}}$. Doubling $k$ can square the coreset size. This limits practical application to small $k$.

### 3. **Neglecting Metric Structure Requirements**