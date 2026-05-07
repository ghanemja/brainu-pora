# Furthest Neighbor ε-Coreset

## Definition

A **furthest neighbor ε-coreset** is a small representative subset of a point set that preserves approximate furthest-neighbor relationships for all query points.

Formally, given a metric space $(V, \text{dist})$, a point set $P \subseteq V$, and an error parameter $\varepsilon > 0$, a set $Q \subseteq P$ is a furthest neighbor ε-coreset if:

$$\forall v \in V, \exists q \in Q : \text{dist}(v, q) \geq (1-\varepsilon) \max_{p \in P} \text{dist}(v, p)$$

In other words, for every query point $v$, there exists at least one point in the coreset $Q$ whose distance to $v$ is at least $(1-\varepsilon)$ times the distance to the true furthest neighbor in $P$.

## Key Equations

**Coreset approximation guarantee:**
$$\text{dist}(v, q^*) \geq (1-\varepsilon) \cdot \text{FN}(v, P)$$

where $q^*$ is the coreset representative and $\text{FN}(v, P) = \max_{p \in P} \text{dist}(v, p)$ is the true furthest neighbor distance.

**Coreset size bounds by metric:**

| Metric Space | Coreset Size | Notes |
|---|---|---|
| Euclidean ($\mathbb{R}^d$) | $\varepsilon^{-O(d)}$ | Exponential in dimension $d$ (curse of dimensionality) |
| Doubling metric | $\varepsilon^{-O(d)}$ | $d$ is doubling dimension |
| Planar graphs | $2^{\text{poly}(1/\varepsilon)}$ | Exponential in $1/\varepsilon$; improved in recent work |
| General metric | $\Omega(n)$ | No non-trivial coreset exists without additional structure |

## Physical Intuition / Derivation

### Why Coresets for Furthest Neighbors are Hard

Unlike nearest-neighbor and clustering problems, furthest neighbor coresets face fundamental hardness barriers:

1. **Worst-case lower bound**: A simple configuration of $n$ points exists where removing any point loses the furthest neighbor guarantee for some query. Thus $|Q| = \Omega(n)$ in the general metric case.

2. **Curse of dimensionality**: In Euclidean spaces, points spread out exponentially with dimension. To guarantee coverage of all "extreme" directions, you need exponentially many coreset points: $\varepsilon^{-O(d)}$ size.

3. **Packing argument**: The number of points in $Q$ is bounded by the maximum number of points that can be placed in $P$ such that each is separated by a $(1-\varepsilon)$-fraction of the diameter. This count grows exponentially with dimension.

### Why Planar Graphs are Different

Planar metrics (shortest-path distances in planar graphs) admit coresets with size *independent of $n$*, though the dependence on $\varepsilon$ remains exponential: $2^{\text{poly}(1/\varepsilon)}$. This is because:

- Planar graphs have bounded treewidth and separator properties that constrain how points can be distributed
- The metric has geometric structure that can be exploited via decomposition techniques
- Recent improvements have reduced the exponent on $\varepsilon$ below the naive $2^{1/\varepsilon}$ bound

## Applications in Engineering

### 1. **Massive Data Processing**
- **Streaming/MapReduce**: Construct a coreset from each data shard, then merge coresets to answer furthest-neighbor queries (e.g., finding outliers, anomalies) without recomputing on full dataset
- **Time complexity reduction**: Replace $O(n)$ exhaustive search with $O(|Q|)$ search where $|Q| \ll n$

### 2. **Facility Location & Surveillance**
- **Maximin facility placement**: Place $k$ facilities to maximize the minimum distance to furthest "uncovered" point; use coreset to reduce computational load
- **Sensor network coverage**: Design monitoring networks where each sensor must monitor its furthest region; coreset identifies critical coverage points

### 3. **Computational Geometry**
- **Bounding volume hierarchies**: Construct efficient spatial indices by filtering to coreset representatives
- **Diameter computation**: Approximate the diameter of a point cloud via coreset (eccentricity of coreset points bounds true diameter)

### 4. **Metric-Space Search**
- **Approximate nearest-neighbor data structures**: In metric spaces where exact algorithms are prohibitive (e.g., doubling metrics, planar graphs), use coreset to build faster indexes
- **Graph analytics**: For road networks (planar metric), identify representative points that capture the graph's "extremal geometry"

## Common Mistakes / Pitfalls

### Mistake 1: Confusing with Nearest-Neighbor Coresets
**Pitfall**: Assuming coreset results for nearest neighbors transfer directly to furthest neighbors.

**Why it fails**: The two problems have opposite geometric structures. A nearest-neighbor coreset clusters points densely; a furthest-neighbor coreset must cover *extremal* directions. Doubling-dimension and packing-based bounds differ fundamentally.

### Mistake 2: Overlooking Dimension Dependence
**Pitfall**: Using Euclidean coreset size $\varepsilon^{-O(d)}$ in high-dimensional data without realizing the exponential blowup makes coresets impractical for $d > 10$ and $\varepsilon < 0.1$.

**Why it matters**: For $d=20, \varepsilon=0.1$, the coreset could have size $10^{20}$ or worse—larger than the original dataset!

### Mistake 3: Assuming Approximation is "Free"
**Pitfall**: Using a $(1-\varepsilon)$-approximation coreset without accounting for error accumulation in downstream algorithms.

**Best practice**: Propagate error bounds through the full pipeline. A $0.1