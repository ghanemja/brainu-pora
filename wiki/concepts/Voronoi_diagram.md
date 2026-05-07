# Voronoi diagram

## Definition

A **Voronoi diagram** is a spatial partition that divides a plane (or higher-dimensional space) into regions called *Voronoi cells*, where each cell is associated with a generator point (or object). The Voronoi cell of a generator contains all points in space that are **closer to that generator than to any other generator**.

For a set of generators $\mathcal{G} = \{G_1, G_2, \ldots, G_n\}$, the Voronoi cell $V_i$ associated with generator $G_i$ is defined as:

$$V_i = \{p \in \mathbb{R}^d : d(p, G_i) \leq d(p, G_j) \text{ for all } j \neq i\}$$

where $d(\cdot, \cdot)$ denotes the distance metric (typically Euclidean distance).

**Weighted Voronoi diagrams** extend this concept by associating weights $w_i$ with each generator, modifying the distance metric to a **weighted distance** $d_p(G_i) = d(p, G_i) - w_i$. The weighted Voronoi cell then contains all points closer to $G_i$ accounting for its weight.

### Key Terminology

- **Voronoi cell (or region)**: The region of space assigned to a single generator
- **Voronoi vertex**: A point where three or more Voronoi cells meet (in 2D)
- **Voronoi edge**: A boundary segment between two adjacent Voronoi cells
- **Bisector** (or *bisector line*): The boundary separating two Voronoi cells, consisting of points equidistant from two generators
- **Adjacency**: Two Voronoi cells are adjacent if their boundaries share an edge or vertex

## Key Equations

### Standard Voronoi Cell
$$V_i = \bigcap_{j \neq i} H_{ij}$$

where $H_{ij}$ is the half-plane of points closer to $G_i$ than to $G_j$:

$$H_{ij} = \{p : d(p, G_i) \leq d(p, G_j)\}$$

### Weighted Distance (Power Distance)
For weighted generators with weights $w_i$ and $w_j$:

$$d_p(p, G_i) = \sqrt{d(p, G_i)^2 - w_i^2}$$

This is the **power distance**, commonly used in geometric algorithms.

### Bisector Equation
The bisector $\gamma_{ij}$ between generators $G_i$ and $G_j$ satisfies:

$$d_p(p, G_i) = d_p(p, G_j)$$

For disks (weighted points), if $G_i$ and $G_j$ are centers with radii $r_i$ and $r_j$:

$$d(p, c_i) - r_i = d(p, c_j) - r_j$$

### Triple Point (Voronoi Vertex)
A point $v_{ijk}$ where three cells meet satisfies:

$$d_p(v_{ijk}, G_i) = d_p(v_{ijk}, G_j) = d_p(v_{ijk}, G_k)$$

This point lies at distance $r_{ijk}$ from each of three generators, where $r_{ijk}$ is called the **circumradius** of the triple.

## Physical Intuition / Derivation

### Why Voronoi Diagrams Matter

Imagine scattering seed points across a landscape. Each seed "claims" the territory closest to it—this is your Voronoi diagram. The resulting partition has remarkable properties:

1. **Locality**: Each cell is determined only by its own generator and its immediate neighbors
2. **Optimality**: The Voronoi diagram minimizes the maximum distance from any point to its nearest generator
3. **Duality**: The Voronoi diagram and Delaunay triangulation are dual structures—understanding one illuminates the other

### Geometric Construction

In 2D, the Voronoi diagram can be constructed by:

1. **Bisector intersection**: Draw perpendicular bisectors between pairs of neighboring generators
2. **Vertex formation**: Extend bisectors until they intersect, forming Voronoi vertices
3. **Cell closure**: Bound each region by the edges and vertices that separate it from neighbors

The **half-plane intersection** interpretation makes this clear: each Voronoi cell is the intersection of half-planes defined by all bisectors pointing toward that cell's generator.

### Weighted Variant (Disk Voronoi Diagrams)

In the source material, generators are **disks** with:
- Center $p_i$ (location)
- Radius $r_i$ (weight)

The weighted distance replaces geometric distance with **power distance**:

$$d_p(p, D_i) = d(p, p_i) - r_i$$

This means:
- A point "inside" a disk has negative power distance (the disk "reaches out")
- Larger radii expand the disk's Voronoi cell
- The bisector between two disks is generally not a straight line—it's more complex

**Strong convexity** (mentioned in the source) is a geometric constraint ensuring that the boundary of the union of disks is convex when properly ordered.

## Applications in Engineering

### 1. **Facility Location & Urban Planning**
- Determine service areas for hospitals, fire stations, or retail outlets
- Each facility's Voronoi cell represents its natural service region
- Optimize placement by analyzing cell areas and distances

### 2. **Mesh Generation & Finite Element Analysis**
- **Centroidal Voronoi Tessellation (CVT)**: Generate high-quality unstructured meshes for FEA
- Iteratively move generator points to cell centroids, improving mesh quality
- Used in structural analysis, fluid dynamics simulations

### 3. **Computational Geometry & Path Planning**
- **Robot motion planning**: Voronoi edges represent safe corridors equidistant from obstacles
- Generate collision-free paths through high-clearance regions
- Simplified graph search in configuration space

### 4. **Materials Science