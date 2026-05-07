# Convex Hull

## Definition

The **convex hull** of a planar point set $P = \{p_1, p_2, \ldots, p_n\}$ is the smallest convex polygon that encloses all points in $P$. Equivalently, it is the intersection of all half-planes containing $P$, or the set of all convex combinations of points in $P$.

Formally, the convex hull is:
$$\text{ConvexHull}(P) = \left\{ \sum_{i=1}^{n} \lambda_i p_i : \lambda_i \geq 0, \sum_{i=1}^{n} \lambda_i = 1 \right\}$$

The **boundary** of the convex hull consists of vertices (extreme points) and edges connecting them in counter-clockwise order. A point $p \in P$ is a **vertex** of the convex hull if and only if it cannot be expressed as a convex combination of other points in $P$.

## Key Equations

**Convex combination:** A point $q$ is in the convex hull if:
$$q = \sum_{i=1}^{k} \alpha_i p_i \quad \text{where} \quad \alpha_i \geq 0, \sum_{i=1}^{k} \alpha_i = 1$$

**Cross product test (collinearity):** For three points $p_a, p_b, p_c$, the signed cross product determines orientation:
$$(p_b - p_a) \times (p_c - p_a) = (b_x - a_x)(c_y - a_y) - (b_y - a_y)(c_x - a_x)$$
- Positive: counter-clockwise turn
- Negative: clockwise turn
- Zero: collinear points

## Physical Intuition / Derivation

Imagine stretching an elastic rubber band around a set of scattered nails on a board. The shape the rubber band takes is the convex hull—it touches only the outermost points and "shortcuts" across any indentations.

**Why is this useful?**

1. **Geometric bounding:** The convex hull provides a tight convex approximation of a point set, useful for collision detection and spatial queries.

2. **Extremal properties:** Hull vertices represent the extreme points in various directions (northernmost, southernmost, etc.), making them natural anchors for geometric analysis.

3. **Incremental construction:** Starting from an empty hull, inserting one point at a time reveals how the hull grows—some insertions don't change it (interior points), while others add new vertices and edges.

**Key insight:** In 2D, if $n$ points are in general position, the convex hull typically has $O(\sqrt{n})$ to $O(n)$ vertices, depending on the point distribution. This sparsity is why convex hulls are computationally attractive.

## Algorithms & Complexity

### Static Computation
The classic $O(n \log n)$ algorithms (Graham scan, Quickhull) sort points and build the hull incrementally by maintaining the property that turns are always counter-clockwise.

### Fully Dynamic Setting
The paper presents a **fully dynamic convex hull** that maintains the hull under both insertions and deletions:

- **Update time (amortized):** $O(\log n \log \log n)$ per insertion or deletion
- **Query time:** $O(\log^2 n)$ for point-location and geometric queries
- **Approach:** Combines the *logarithmic method* (maintains $O(\log n)$ deletion-only structures at different scales) with efficient query support

**Logarithmic method:** Rather than updating a single convex hull, maintain a collection of $O(\log n)$ auxiliary convex hulls (each supporting deletion only) organized by size. This amortizes the cost of insertions across multiple levels.

## Applications in Engineering

### 1. **Collision Detection & Path Planning**
Convex hulls provide simplified geometry for rapid collision checking in robotics and animation. Two objects with convex hull geometries cannot collide if their hulls don't overlap (Separating Axis Theorem).

### 2. **Spatial Data Analysis**
In GIS and environmental engineering, convex hulls characterize the extent of phenomena (flood zones, contamination spread, wildlife habitat boundaries). Dynamic hulls allow real-time updates as new measurement data arrives.

### 3. **Point-Location Queries**
Given a dynamic point set, determine if a query point is inside the current convex hull. Applications include:
- Feasibility checking in optimization (is a candidate solution within the region of interest?)
- Geographic information system containment queries

### 4. **Computer Vision & Shape Analysis**
Convex hulls approximate object silhouettes and extract shape descriptors (eccentricity, solidity). The ratio of object area to hull area measures object convexity.

### 5. **Computational Finance**
Portfolio optimization uses the convex hull of return vectors to identify the efficient frontier. As assets are added/removed, dynamic hull updates enable rapid rebalancing.

### 6. **Mesh Processing**
In 3D graphics, convex hulls serve as low-detail approximations and bounding volumes for hierarchical collision detection (Convex Hull Trees).

## Common Mistakes / Pitfalls

### 1. **Confusing hull with bounding box**
A bounding box (axis-aligned or oriented) is different from a convex hull. The hull is tighter and more faithful to the actual point distribution, but requires more computation.

### 2. **Assuming collinear points are always excluded**
Different convex hull algorithms handle collinear points inconsistently. Some include all collinear boundary points; others report only vertices. Specification matters in practice.

### 3. **Forgetting that insertion cost depends on geometry**
Inserting a point far from the current hull can be cheaper (fewer edge updates) than inserting one near the boundary. Worst-case $O(n)$ per update is possible (e.g., inserting into a fully refined point set along the hull perimeter).

### 4. **Ignoring numerical robustness**
Orientation tests using floating-point arithmetic can suffer from rounding errors, leading to degenerate or inconsistent hulls. The paper emphasizes that existing fully dynamic implementations often fail on real-world inputs; robust implementation requires careful numerical handling or exact arithmetic.