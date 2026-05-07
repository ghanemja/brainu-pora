# Intersection Graph of Polygons

## Definition

An **intersection graph of polygons** is a graph $G = (V, E)$ where:
- Each vertex $v \in V$ represents a polygon in the plane
- Two vertices $u, v \in V$ are connected by an edge $(u,v) \in E$ if and only if their corresponding polygons intersect (share at least one point)

The graph is given via a **geometric representation**: an explicit embedding of all polygons in $\mathbb{R}^2$ with polynomial complexity (polynomial in the number of vertices and coordinate bit-length).

### Related Classes

**δ-similarly-sized polygons**: All polygons have diameters within a factor of $\delta$ of each other.

**β-fat polygons**: A polygon $p$ is $\beta$-fat if 
$$\text{fatness}(p) = \frac{\text{diam}(p)}{r_{\text{inscribed}}(p)} \leq \beta$$
where $r_{\text{inscribed}}(p)$ is the radius of the largest inscribed disk.

**α-standard representation**: A representation satisfying geometric normalization conditions that bound coordinate magnitudes relative to polygon sizes.

**Simple polygons**: Non-self-intersecting polygons without holes.

## Key Equations

### Fatness Definition
$$\beta_{\text{fatness}} = \frac{\text{diameter}}{\text{inscribed disk radius}}$$

### Fatness Preservation Under Hole Removal
If polygon $p$ has holes and we construct $p'$ by removing a region $R_{p,h}$ that avoids the inscribed disk $d_p$ of radius $r_p \geq \frac{\beta}{4}\text{diam}(p)$, then the resulting simple polygon satisfies:
$$\text{fatness}(p') \leq \frac{\beta}{4}$$

### Slab Positioning
For consecutive x-coordinates $x_i, x_{i+1} \in X$, the narrow slab avoiding all polygon vertices satisfies:
$$x_{p,h} = \frac{2x_i + x_{i+1}}{3}, \quad x'_{p,h} = \frac{x_i + 2x_{i+1}}{3}$$

## Physical Intuition / Derivation

### Why Intersection Graphs Matter

Intersection graphs encode **combinatorial contact relationships** between geometric objects. Instead of maintaining expensive geometric data, we compress the problem into a graph where adjacency captures intersection.

### Hole Removal Algorithm (Lemma A.3)

The construction converts polygons-with-holes into simple polygons while preserving:
1. **Intersection adjacency**: If $p$ and $q$ intersected, $p'$ and $q'$ still intersect
2. **Fatness bounds**: Fatness degrades only by factor ~4, recoverable by rescaling
3. **Subpolygon property**: $p' \subseteq p$ ensures no false intersections created

**Key insight**: A vertical slab of width $\frac{1}{3}(x_{i+1} - x_i)$ is guaranteed to contain no polygon vertices (since vertices project to coordinates in $X$, which are spaced by unit distance in $X$). This allows safe removal of a trapezoid region neighboring each hole without cutting polygon interiors.

The algorithm exploits **top-to-bottom monotonicity**: within the vertex-free slab, the boundary $\partial p$ forms a sequence of non-crossing segments, creating a unique ordered list of alternating regions belonging to $p$ and $R^2 \setminus p$.

### Preservation of Standardness

If the original representation is $\alpha$-standard, rescaling the simplified representation by factor 4 yields $4\alpha$-standardness, allowing use in algorithms with coordinate-dependent complexity bounds.

## Applications in Engineering

### Computational Geometry & CAD
- **Collision detection**: Intersection graphs enable rapid broad-phase checks before expensive continuous collision tests
- **Layout optimization**: Determining which components in circuit or mechanical designs physically touch
- **Mesh processing**: Detecting self-intersections in CAD models with internal cavities

### Robotics & Motion Planning
- **Configuration space analysis**: Intersection graphs of obstacles (polygonal approximations) identify connectivity constraints
- **Grasping**: Determining contact points between end-effector and workpiece polygonal models

### GIS & Spatial Databases
- **Spatial indexing**: Intersection graphs accelerate range queries ("which parcels touch this region?")
- **Map overlay**: Computing intersections between polygonal map layers

### Approximation Algorithms
- **Geometric set cover**: Intersection graphs of disks/polygons yield constant-factor approximations for covering problems
- **Independent set**: Fat polygon intersection graphs have bounded chromatic number (PTAS exists)

## Common Mistakes / Pitfalls

1. **Confusing "intersection graph" with "visibility graph"**: Intersection requires geometric overlap; visibility only requires line-of-sight. These are distinct graph structures.

2. **Assuming fatness scales freely**: Fatness $\beta$ is *scale-invariant* (ratio of diameter to inscribed radius), but algorithms bounding complexity by $\beta^k$ become impractical for thin polygons ($\beta \gg 1$).

3. **Ignoring holes in complexity analysis**: Polygons-with-holes multiply the arrangement complexity. The hole-removal lemma is essential for reducing to simple polygon algorithms.

4. **Missing edge cases in hole removal**: A removed trapezoid $R_{p,h}$ must be chosen to avoid the inscribed disk $d_p$; removing the "wrong" region can destroy fatness or create self-intersections.

5. **Assuming δ-similarly-sized is free**: While theoretically cleaner, algorithms with complexity depending on $\delta$ (e.g., $\log \delta$) become prohibitive for wide size ranges.

6. **Confusing graph planarity with geometric planarity**: The intersection graph may be planar, but planarity depends on the *adjacency structure*, not the geometric embedding's planarity.

## See Also

- [[Polygon Arrangement]]
- [[Fatness and Inradius]]
- [[Geometric Set Cover]]
- [[Collision Detection Algorithms]]
- [[Chromatic Number of Geometric Graphs]]

## Sources