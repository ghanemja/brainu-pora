# Euclidean Distance

## Definition

**Euclidean distance** is the straight-line distance between two points in Euclidean space, calculated as the length of the line segment connecting them. It is the most fundamental distance metric in geometry and represents the "as-the-crow-flies" distance when no obstacles are present.

In the context of location-based problems (as in delivery routing), when locations are represented by **latitude and longitude coordinates**, the Euclidean distance provides a planar approximation of separation between two geographic points.

## Key Equations

For two points $P_1 = (x_1, y_1)$ and $P_2 = (x_2, y_2)$ in 2D space:

$$d(P_1, P_2) = \sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2}$$

For the general $n$-dimensional case with points $P_1 = (x_1^{(1)}, x_1^{(2)}, \ldots, x_1^{(n)})$ and $P_2 = (x_2^{(1)}, x_2^{(2)}, \ldots, x_2^{(n)})$:

$$d(P_1, P_2) = \sqrt{\sum_{i=1}^{n} (x_2^{(i)} - x_1^{(i)})^2}$$

This is equivalent to the $L_2$ norm (Euclidean norm) of the difference vector:

$$d(P_1, P_2) = \|\mathbf{P_2} - \mathbf{P_1}\|_2$$

## Physical Intuition / Derivation

The Euclidean distance formula emerges directly from the **Pythagorean theorem**. Consider two points in a 2D plane:

1. The horizontal separation is $\Delta x = x_2 - x_1$
2. The vertical separation is $\Delta y = y_2 - y_1$
3. These form the legs of a right triangle
4. The hypotenuse (direct distance) satisfies: $d^2 = (\Delta x)^2 + (\Delta y)^2$

This geometric foundation extends naturally to higher dimensions. The term "Euclidean" honors Euclid's classical geometry, where this distance measure is fundamental to the definition of congruence and similarity.

**Why use it for geographic coordinates?**

At small scales (within a city or region), latitude/longitude coordinates can be treated as approximately Cartesian (planar) without significant error. The curvature of Earth becomes negligible over distances of a few kilometers. This justification underpins its use in the delivery routing application described in the source material, where orders and depots within a single city are modeled using coordinate-based Euclidean distances.

## Applications in Engineering

### 1. **Route Optimization & Logistics**
In vehicle routing problems (VRP) and delivery dispatch systems, Euclidean distance between depot-to-order and order-to-order pairs forms the cost basis for route construction. The baseline cheapest-insertion heuristic algorithm from the source material uses Euclidean distances to compute "additional travel time incurred" when inserting a new order into a route. This informs the greedy optimization criterion.

### 2. **Clustering & Spatial Analysis**
Euclidean distance is the standard metric in:
- **k-means clustering**: partitioning orders by nearest depot
- **Spatial indexing**: organizing locations in k-d trees or R-trees for fast nearest-neighbor queries
- **Demand pattern analysis**: identifying geographic clusters of high-density orders

### 3. **Computational Geometry**
- **Facility location problems**: determining optimal placement of depots to minimize average/maximum distance to orders
- **Convex hull & Voronoi diagrams**: delineating service regions
- **Motion planning**: computing clearance distances and obstacle avoidance paths

### 4. **Machine Learning & Data Science**
- **Distance-based similarity**: feature space for classification/regression tasks
- **Anomaly detection**: identifying outlier locations or unusual delivery patterns
- **Dimensionality reduction**: preserving distances in embedded representations

## Common Mistakes / Pitfalls

### 1. **Confusing Euclidean and Manhattan (Taxicab) Distance**
Euclidean distance $\sqrt{(x_2-x_1)^2 + (y_2-y_1)^2}$ differs from Manhattan distance $|x_2-x_1| + |y_2-y_1|$. Manhattan distance is appropriate when movement is restricted to orthogonal grids (city blocks); Euclidean distance assumes unrestricted straight-line travel.

### 2. **Using Euclidean Distance for Road Network Travel**
Euclidean distance between two addresses does **not** equal actual driving distance, which follows road networks, traffic patterns, and regulations. The source material's use of Euclidean distance is an **approximation**; real delivery systems typically use road-network distance (from routing APIs) for accurate time/cost estimates.

### 3. **Ignoring Coordinate System Differences**
Raw latitude/longitude coordinates should not be directly plugged into the Euclidean formula without considering:
- **Projection distortion**: at large geographic scales, Earth's curvature introduces non-negligible errors
- **Unit consistency**: degrees of latitude/longitude do not correspond uniformly to physical distance
- **Solution**: convert to a local projected coordinate system (e.g., UTM) or use haversine distance for long distances

### 4. **Treating Euclidean Distance as Always Optimal**
In constrained environments (e.g., buildings, traffic networks), the straight-line Euclidean path may be infeasible or suboptimal. Always verify that the metric aligns with operational constraints.

### 5. **Computational Efficiency Oversights**
- Computing full distance matrices for large $n$ (e.g., 69,103 orders) can be memory-intensive
- Distance calculations appear in inner loops of algorithms (e.g., the baseline's $O(n(k+n))$ cheapest-insertion requires $O(n^2)$ pairwise distances in the worst case)
- **Optimization**: use spatial indexing, lazy evaluation, or approximate distance functions

## See Also

- [[