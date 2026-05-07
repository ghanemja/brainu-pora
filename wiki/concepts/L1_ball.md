# L1 ball

## Definition

An **L1 ball** (also called a **Manhattan ball** or **taxicab ball**) of radius $r$ centered at point $\mathbf{c} \in \mathbb{Z}^3$ is the set of all points whose L1 distance from $\mathbf{c}$ does not exceed $r$:

$$B_1(r) = \{\mathbf{x} \in \mathbb{Z}^3 : \|\mathbf{x} - \mathbf{c}\|_1 \leq r\}$$

where the **L1 distance** (also called **Manhattan distance** or **taxicab distance**) is defined as:

$$\|\mathbf{x} - \mathbf{c}\|_1 = |x_1 - c_1| + |x_2 - c_2| + |x_3 - c_3|$$

In three dimensions, an L1 ball of radius $r$ contains exactly $\frac{(r+1)(r+2)(2r+3)}{6}$ lattice points. For example, a radius-12 L1 ball contains **2625 lattice points**.

## Key Equations

The volume (lattice point count) of an L1 ball of radius $r$ in $\mathbb{R}^d$ is:

$$|B_1(r) \cap \mathbb{Z}^d| = \sum_{k=0}^{r} 2^d \binom{d+k-1}{k}$$

For $d=3$ specifically:

$$|B_1(r) \cap \mathbb{Z}^3| = \frac{(r+1)(r+2)(2r+3)}{6}$$

The L1 distance metric satisfies the triangle inequality:
$$\|\mathbf{x} - \mathbf{z}\|_1 \leq \|\mathbf{x} - \mathbf{y}\|_1 + \|\mathbf{y} - \mathbf{z}\|_1$$

**Relationship to L∞ ball:** An L∞ ball (the closed $\ell_\infty$-neighborhood) of radius $r$ forms a cube; the L1 ball is the diamond-shaped region inscribed within it.

## Physical Intuition / Derivation

### Why L1 Distance Matters

The L1 distance represents the minimum number of unit steps required to travel from one point to another on a **rectilinear grid** (moving only parallel to axes), as opposed to Euclidean (straight-line) distance. This is why it's called "taxicab" distance—it models movement in city grids.

### Geometry of the L1 Ball

In 2D, an L1 ball of radius $r$ is a diamond (square rotated 45°) with vertices at distance $r$ along each axis. In 3D, it forms an **octahedron-like shape** with vertices at:
- $(\mathbf{c} + r\hat{x}, \mathbf{c} - r\hat{x}, \mathbf{c} + r\hat{y}, \mathbf{c} - r\hat{y}, \mathbf{c} + r\hat{z}, \mathbf{c} - r\hat{z})$

### Counting Lattice Points

The cubic growth formula arises because we're counting integer solutions to:
$$|x| + |y| + |z| \leq r$$

This can be decomposed into nested "shells" where the number of lattice points at distance exactly $k$ grows quadratically: $4(k+1)^2$ points lie on the boundary at distance $k$ in 3D.

## Applications in Engineering

### 1. **Robotic Path Planning & Motion Control**
- L1 balls define reachable regions for rectilinear motion systems (e.g., manipulators constrained to orthogonal movements)
- Used to verify whether a configuration is attainable within a given number of unit steps

### 2. **Modular Robotics & Self-Reconfigurable Systems**
- In the source material, L1 balls determine valid neighborhoods for module aggregation
- The radius-12 L1 ball (2625 cells) defines the minimum region guaranteeing certain topological properties needed for snake formation
- Critical for analyzing **connectivity** and **structural completeness** in modular robot swarms

### 3. **Digital Geometry & Voxel-Based Simulation**
- Defines neighborhoods in 3D discrete grids (voxel space)
- Used in image processing, computational geometry, and volumetric analysis
- Preferred over L2 (Euclidean) when isotropy in rectilinear grids is needed

### 4. **Network Optimization & Coverage Problems**
- L1-ball neighborhoods model reachability in Manhattan-distance graphs
- Applied to facility location, broadcast coverage, and communication routing

### 5. **Compressed Sensing & Sparse Optimization**
- L1 norm (sum of absolute values) is fundamental to $\ell_1$-minimization for signal recovery
- L1 balls define constraint regions in optimization problems seeking sparse solutions

## Common Mistakes / Pitfalls

1. **Confusing L1 with L2 neighborhoods**
   - An L1 ball is **not** a sphere; it is diamond-shaped in 2D and octahedral in 3D
   - The L1 ball is the **interior** of a set of equidistant points under taxicab metric

2. **Incorrect point counting**
   - Assuming a radius-$r$ L1 ball contains $(2r+1)^3$ points (this is the L∞ ball, a cube)
   - The cubic formula $\frac{(r+1)(r+2)(2r+3)}{6}$ must be used for accurate counts

3. **Mixing continuous and discrete spaces**
   - L1 balls in continuous $\mathbb{R}^3$ vs. lattice point sets $\mathbb{Z}^3$ behave differently
   - Engineering applications usually require **discrete** counting

4. **Assuming isotropy**
   - L1 distance is **not