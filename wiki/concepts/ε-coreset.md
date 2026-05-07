# ε-coreset

## Definition

An **ε-coreset** is a compact subset of a metric space that preserves distance properties within a multiplicative error factor $\epsilon$. Formally, for a metric space $(V, \text{dist})$ and a problem instance (e.g., furthest neighbor or $k$-center), an ε-coreset $S \subseteq V$ is a weighted or unweighted subset such that solutions computed on $S$ approximate the optimal solutions on the full set $V$ within a factor of $(1 \pm \epsilon)$.

More specifically:
- For **furthest neighbor problems**: An ε-coreset is a set of representative points such that the furthest point from any query in the coreset approximates the furthest point in the original set within error $\epsilon$.
- For **$k$-center problems**: An ε-coreset $S$ satisfies the property that for any subset $X \subseteq V$, the $k$-center cost on $X \cap S$ approximates the $k$-center cost on $X$ within relative error $\epsilon$.

## Key Equations

The size of an ε-coreset depends critically on the geometric structure of the underlying metric space. For different graph classes:

$$\text{Size}(\text{ε-coreset}) \in \begin{cases}
O(1/\epsilon^2) & \text{Simple polygons} \\
\text{poly}(1/\epsilon) & \text{Planar graphs} \\
\text{poly}(g, 1/\epsilon) & \text{Bounded genus } g \\
2^{\Omega(1/\epsilon)} & \text{Treewidth} \leq 5
\end{cases}$$

For $k$-center problems on specific graph families:

$$\text{Size}(S_k, \epsilon) \leq \begin{cases}
(1/\epsilon)^{2^{O(k)}} & \text{Planar graphs (fixed } k \text{)} \\
\text{poly}(g) \cdot (1/\epsilon)^{2^{O(k)}} & \text{Bounded genus } g \\
k^{\text{poly}_H(1/\epsilon)} & \text{H-minor-free graphs}
\end{cases}$$

For a query point $v$ and a subset $X \subseteq V$, the distance function satisfies:
$$\text{dist}(v, X) = \min_{x \in X} \text{dist}(v, x)$$

## Physical Intuition / Derivation

### Why Coresets Matter

When working with large metric spaces (e.g., road networks, point clouds), computing exact solutions to geometric problems is prohibitively expensive. A coreset solves this by answering: **"How small can we make our data while preserving the structure needed to answer queries approximately?"**

### Building Intuition through Examples

**Example 1: Simple Polygon**
Consider a convex polygon with $n$ vertices. To find the furthest vertex from a query point, we might need all $n$ vertices in the worst case. However, for an ε-coreset, we can discretize the polygon boundary into $O(1/\epsilon^2)$ representative points. The maximum distance error is bounded by the arc length between consecutive representatives, which scales with $\epsilon$.

**Example 2: Planar Graph**
A planar road network has bounded local complexity. By cutting the surface along $O(1)$ cycles, we reduce the problem to tree-like structures with $O(\text{poly}(1/\epsilon))$ carefully chosen "hubs" (points of high traffic/branching). This polynomial dependence—rather than exponential—reflects the topological constraint that planarity imposes.

### The Role of Surface Topology

The genus $g$ of a surface (roughly, the number of "holes") directly affects coreset size. Intuitively:
- **$g = 0$ (sphere)**: Planar graphs; coreset size is polynomial in $1/\epsilon$
- **$g > 0$ (torus, etc.)**: Size grows polynomially in both $g$ and $1/\epsilon$
- **Unbounded genus** (general graphs): Exponential blowup becomes inevitable

The cutting argument works by choosing $O(g)$ disjoint cycles whose removal renders the surface simply connected, reducing the problem to a planar (or tree) setting locally.

### Lower Bounds: Hardness of Approximation

The surprising result is that beyond bounded-genus surfaces, exponential lower bounds emerge:

$$\text{Size}_{\min}(\epsilon\text{-coreset}) \geq 2^{c/\epsilon}$$

for graphs with treewidth $\leq 5$ or $K_5$-minor-free families. This gap reveals a **fundamental threshold**: minor-closed graph families of bounded genus admit efficient coresets, while all other minor-closed families require exponential size in $1/\epsilon$.

## Applications in Engineering

### 1. **Spatial Data Structures & Indexing**
Geographic information systems (GIS) and location-based services use ε-coresets to compress point-of-interest databases. A navigation app can precompute a small coreset of landmarks, reducing query time from $O(n)$ to $O(|S|)$ while guaranteeing that routing decisions remain near-optimal.

### 2. **$k$-Center Facility Location**
In facility placement problems (e.g., emergency service stations, data centers), we want to cover a large region with $k$ facilities. ε-coresets allow us to solve the $k$-center problem on a small representative subset, then lift solutions back to the original space, achieving $(1+\epsilon)$-approximation guarantees.

### 3. **Motion Planning in Bounded Complexity Environments**
Robot path planning in planar or low-genus environments (e.g., building floors, planar workspaces) can use ε-coresets of critical waypoints. The polynomial dependence on $1/\epsilon$ (rather than exponential) makes real-time planning feasible.

### 4. **Mesh Simplification & Geometry Processing**
In computer graphics, an ε-coreset of vertices can approximate the shape of a dense mesh while drastically reducing storage and rendering cost. The guarantees ensure that