# Brick Regions

## Definition

Brick regions are the **faces of a mortar graph** that partition a planar domain into rectangular-like subdivisions. Given a mortar graph $\tilde{M}$, the brick regions $B$ are all faces of $\tilde{M}$ (viewed as closed subsets of $\mathbb{R}^2$) except possibly one special unbounded region.

Each brick region $B$ defines a corresponding **brick** $\mathcal{B} := G|_B$—the induced subgraph of the underlying graph $G$ restricted to vertices and edges within that region.

### Compass Structure

A brick region's geometry is characterized by its **compass**, which partitions the boundary cycle $\partial B$ of a brick region $B$ into six oriented paths:

- **South**($\partial B$)
- **East**$^-$($\partial B$) and **East**$|$($\partial B$)
- **North**($\partial B$)
- **West**$|$($\partial B$) and **West**$^-$($\partial B$)

These are ordered **anticlockwise** for bounded brick regions and **clockwise** for the unbounded region. The composite paths are defined as:

$$\text{West}(\partial B) := \text{West}^-(\partial B) \cup \text{West}|(\partial B)$$
$$\text{East}(\partial B) := \text{East}^-(\partial B) \cup \text{East}|(\partial B)$$

### Corner Vertices

Six special corner vertices (shared between consecutive boundary paths) are marked:
- $\dot{v}^B_{SSE}$, $\dot{v}^B_{SE}$, $\dot{v}^B_{NE}$, $\dot{v}^B_{NW}$, $\dot{v}^B_{SW}$, $\dot{v}^B_{SSW}$

Their projections into brick $\mathcal{B}$ are denoted $v^B_{SE}$, etc.

### Small vs. Large Bricks

A brick $\mathcal{B}$ is classified based on geometric constraints (parametrized by $\lambda = 1/\varepsilon^{7.5}$):

**Small brick**: All vertices satisfy $\text{dist}(v, \text{Perim}(\mathcal{B})) \leq \lambda$, and vertices near both North and South boundaries are within distance $2\lambda/\varepsilon^2$ of side corners.

**Large brick**: Does not satisfy small brick conditions; contains "deep" interior vertices or poorly-distributed geometry.

## Key Equations

### Approaching Path Property

A path $P$ is **$c$-approaching** a set $Q$ (containing exactly one endpoint $y$ of $P$) if for every vertex $x \in V(P)$:

$$|P[x,y]| \leq c \cdot \text{dist}_G(x, Q)$$

This ensures that paths don't stray far from $Q$ relative to shortest paths in the underlying graph.

### Mortar Graph Complexity

Given precision parameter $\varepsilon \in (0, 0.1)$ and parameters:
$$\kappa = \frac{1}{\varepsilon^3}, \quad \lambda = \frac{1}{\varepsilon^{7.5}}$$

The total complexity of a mortar graph is bounded by:

$$\text{compl}(\tilde{M}) = O\left(\frac{n^4}{\varepsilon^2}\right) \cdot \text{compl}(\mathcal{A}(G))$$

### Path Approximation Quality

The key mortar graph guarantees (Theorem 9.3) ensure:
- **M2**: North($\mathcal{B}$) is an exact shortest path
- **M2**: West$^-$($\mathcal{B}$) $\cup$ South($\mathcal{B}$) $\cup$ East$^-$($\mathcal{B}$) is an internally $(1+\varepsilon)$-approximate shortest path
- **M3**: East$|$($\mathcal{B}$) and West$|$($\mathcal{B}$) are $c$-approaching North($\mathcal{B}$)
- **M4**: Total boundary path length satisfies $$\sum_B \left|\text{North}(\mathcal{B})\right| + \left|\text{South}(\mathcal{B})\right| + \left|\text{West}^-(\mathcal{B})\right| + \left|\text{East}^-(\mathcal{B})\right| = O\left(\frac{1}{\varepsilon}\right)\text{StTree}(G, T)$$

## Physical Intuition / Derivation

### Geometric Motivation

Brick regions are a **discretization strategy** for partitioning a planar domain into manageable rectangular zones:

1. **Coarse Structure**: The mortar graph creates a multi-scale decomposition—like dividing a city into neighborhoods (bricks) with connecting roads (mortar edges).

2. **Compass Orientation**: The six-path compass mimics compass directions, providing an intuitive **coordinate system** for each region. The North/South/East/West paths serve as "arterial routes" through each brick.

3. **Small/Large Distinction**: This classification reflects a **quality-of-shape** criterion:
   - **Small bricks** are "nice" rectangles with bounded aspect ratios—paths through them are well-behaved
   - **Large bricks** may be elongated or have complex interior structure, requiring careful handling

### Construction Intuition

The approach builds a hierarchical **multi-scale approximation**:
- Partition space into bricks (controlling complexity via $O(n^4/\varepsilon^2)$ factor)
- Within each brick, identify skeleton paths (North, South, East, West) that serve as **approximate geodesics**
- Use approaching properties (M3) to ensure interior columns of vertices don't deviate far from these main routes
- Trade off approximation quality ($\varepsilon$) against structural complexity