---
video: saVZtgPyyJQ | Understanding SLAM Using Pose Graph Optimization | Autonomous Navigation, Part 3 | MATLAB | 16:22
video: Alu59K8zvYs | Wolfram Burgard, Giorgio Grisetti, and Cyrill Stachniss: Graph-based SLAM in 20 Minutes | Cyrill Stachniss | 19:51
---
## Poses as nodes, measurements as edges

**Pose graph SLAM** stores the robot's trajectory as a graph. Each **node** is a pose $x_i$ at some moment. Each **edge** is a measured relative pose $z_{ij}$ between two nodes, with an **information matrix** $\Omega_{ij}$, the inverse of its covariance, saying how much to trust it.

- **Odometry edges** connect consecutive poses.
- **Loop-closure edges** connect the current pose to one from long ago, when the front end recognizes a place.

A **factor graph** is the general version: landmarks, GPS fixes and IMU readings become nodes or factors too.

## The cost: disagree as little as possible

For each edge, compare the measurement with what the current pose estimates predict. The error $e_{ij}$ is the difference between $z_{ij}$ and the predicted relative pose $x_i^{-1} x_j$, with angles wrapped. Then find the poses that minimize the total weighted error:

$$x^* = \arg\min_x \sum_{(i,j)} e_{ij}^\top\, \Omega_{ij}\, e_{ij}$$

Edges with high information pull hard; uncertain ones give way. It's nonlinear least squares, because rotations make the predicted relative poses nonlinear.

## Solving it: Gauss–Newton on a sparse system

Linearize each error around the current guess, $e_{ij}(x + \Delta x) \approx e_{ij} + J_{ij} \Delta x$, and solve the normal equations

$$H\, \Delta x = -b, \qquad H = \sum J_{ij}^\top \Omega_{ij} J_{ij}, \qquad b = \sum J_{ij}^\top \Omega_{ij}\, e_{ij}$$

then update and repeat. Each edge touches only two poses, so $H$ is mostly zeros, and sparse solvers handle tens of thousands of poses quickly. Fix the first pose, since the measurements only describe relative positions and say nothing about where the whole map sits.

## Worked example: a 1-D loop

Pose $x_0 = 0$ is fixed. Odometry says $x_1 - x_0 = 1.0$ and $x_2 - x_1 = 1.0$, but a loop closure says $x_2 - x_0 = 1.8$. With all three edges weighted 1, minimize

$$(x_1 - 1)^2 + (x_2 - x_1 - 1)^2 + (x_2 - 1.8)^2$$

Setting the derivatives to zero gives $x_2 = 2 x_1$ and $2 x_2 - x_1 = 2.8$, so $x_1 \approx 0.933$ and $x_2 \approx 1.867$. The 0.2 m disagreement is split equally, $0.067$ m per edge. Weight the loop closure 10 instead and the answer moves toward it: $x_1 \approx 0.905$, $x_2 \approx 1.810$.

## Why it replaced filtering

An EKF linearizes each measurement once and never revisits it. Graph optimization keeps all the poses and re-linearizes them on every iteration, so early mistakes get corrected when new evidence arrives. Sparsity keeps it fast, and libraries such as g2o, GTSAM and Ceres make it routine.

> **Common mistake:** giving every edge the same information matrix. Then a sloppy wheel-odometry edge counts as much as a precise scan match, and a single loop closure can't outvote fifty odometry edges, or outvotes them when it shouldn't. Use each measurement's real uncertainty.
