# Delaunay Triangulation

## Definition

The **Delaunay triangulation** is a geometric partitioning of a set of points in the plane (or higher dimensions) into non-overlapping triangles such that no point lies inside the circumcircle of any triangle. Equivalently, it is the triangulation that maximizes the minimum angle across all triangles—it avoids "sliver" triangles.

For a point set $P = \{p_1, p_2, \ldots, p_n\}$ in $\mathbb{R}^2$, the Delaunay triangulation $\mathcal{DT}(P)$ is the unique triangulation (given non-degenerate point configuration) satisfying the **empty circumcircle property**: for every triangle $T \in \mathcal{DT}(P)$, the circumcircle of $T$ contains no other points from $P$ in its interior.

## Key Equations

**Circumcircle condition:** A triangle with vertices $\mathbf{a}, \mathbf{b}, \mathbf{c}$ has circumcenter $\mathbf{o}$ and circumradius $R$ satisfying:

$$|\mathbf{o} - \mathbf{a}| = |\mathbf{o} - \mathbf{b}| = |\mathbf{o} - \mathbf{c}| = R$$

**Minimum angle maximization:** Delaunay triangulation solves:

$$\mathcal{DT}(P) = \arg\max_{\text{triangulations}} \min_{\text{triangles } T} \theta_{\min}(T)$$

where $\theta_{\min}(T)$ is the smallest interior angle of triangle $T$.

## Physical Intuition / Derivation

### Geometric Motivation
Imagine points in the plane representing cities or sites. A Delaunay triangulation emerges naturally as follows:

1. **Start with a point set:** Scatter $n$ points arbitrarily in the plane.
2. **Avoid "bad" triangles:** If you form a triangle whose circumcircle contains nearby points, those points are "wasted"—they create dependencies that stretch edge lengths and pinch angles.
3. **Greedy maximization:** By insisting the circumcircle of each triangle be empty, you force every nearby point into the local neighborhood, creating a well-distributed, balanced mesh.

### Dual Relationship
The Delaunay triangulation is the **dual** of the **Voronoi diagram**: each Delaunay triangle corresponds to three Voronoi cells meeting at a point (the circumcenter). Two Delaunay vertices are connected by an edge if and only if their Voronoi cells share a boundary.

### Why It Works
- **Angle maximization:** No thin slivers can form; all angles stay away from 0° and 180°.
- **Locality:** For each point, nearby points form natural neighbors (Delaunay edges). This property is exploited in the source material's use of Delaunay for identifying candidate source-target pairs without exhaustive search.
- **Uniqueness:** For non-degenerate point sets (no four cocircular points), the Delaunay triangulation is unique.

## Applications in Engineering

### Computational Geometry & Mesh Generation
- **Finite element analysis (FEA):** Delaunay meshes provide high-quality triangulations minimizing distortion and numerical error.
- **Terrain modeling:** Digital elevation models use Delaunay triangulation to interpolate height at arbitrary points from sparse survey data.

### Proximity & Neighbor Search
- **Nearest-neighbor queries:** The Delaunay graph provides efficient navigation—walking along Delaunay edges leads to nearest neighbors with high probability.
- **Vehicle routing (as in source material):** Identify candidate source-target pairs for efficient tree construction without checking all $O(n^2)$ pairs; the Delaunay neighbors form a sparse ($O(n)$-edge) candidate set.

### Computational Robotics
- **Roadmap construction:** Probabilistic roadmaps and visibility graphs use Delaunay to connect configuration-space nodes with minimal redundancy.
- **Collision avoidance:** Identify nearby obstacles efficiently via Delaunay neighbors.

### Spatial Interpolation
- **Natural neighbor interpolation (Sibson interpolation):** Use Voronoi/Delaunay duality to estimate function values at unmeasured locations.

### Graphics & Computer Vision
- **Surface reconstruction:** Build 3D meshes from point clouds; Delaunay (in 3D: tetrahedralization) is fundamental.
- **Point cloud processing:** Detect local topology and connectivity.

## Common Mistakes / Pitfalls

### Misconception 1: "Delaunay = Minimum Spanning Tree"
**False.** The Delaunay triangulation maximizes angles but does *not* minimize total edge length. It is not an MST. The source material uses Delaunay as a *filter* to reduce the candidate set for MST construction, not as the MST itself.

### Misconception 2: "All Delaunay triangulations are the same"
**True only for non-degenerate point sets.** If four or more points are cocircular, multiple valid Delaunay triangulations exist (the triangulation is not unique). In practice, perturbations or symbolic perturbation schemes ensure uniqueness.

### Misconception 3: "Delaunay triangles are always acute"
**False.** Delaunay triangulation maximizes the *minimum* angle but does not guarantee all angles are acute. In fact, obtuse Delaunay triangles are common (e.g., for points on a circle, the Delaunay triangulation is the fan, with very obtuse triangles).

### Misconception 4: "Delaunay works well in high dimensions"
**Partially false.** Delaunay triangulations exist in any dimension, but:
- The number of simplices grows exponentially with dimension.
- Computational complexity becomes prohibitive ($O(n^{d/2})$ in dimension $d$).
- The "quality" advantage of angle maximization diminishes in high dimensions.

### Pitfall in Implementation
- **Numerical robustness:** Circumcircle tests involve floating-point arithmetic and are prone to round-off error. Use **exact arithmetic