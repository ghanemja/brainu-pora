---
source: pora
chapter: 14
layer: E
kind: classical
tags: [pora, robot-autonomy, classical]
---
# Graph & factor-graph SLAM

Treat poses as graph nodes and measurements as constraints, then solve for the configuration that best satisfies them all. Standard in modern SLAM.

<!-- pora:begin -->
## In Principles of Robot Autonomy

- Read: [Chapter 14: Simultaneous Localization and Mapping (SLAM)](https://porabook.com/book/slam/)
- Stack layer: Estimation & mapping · classical
- Run: [Pose Graph SLAM](https://colab.research.google.com/github/StanfordASL/pora-exercises/blob/main/ch14/pose_graph_slam.ipynb) ([source](https://github.com/StanfordASL/pora-exercises/blob/main/ch14/pose_graph_slam.ipynb))

### Key ideas

1. Nodes are robot poses (and optionally landmarks); edges are relative measurements z_ij with information matrices Ω_ij from odometry, scan matching, or loop closures.
2. The estimate minimizes Σ e_ij^T Ω_ij e_ij, where e_ij is the error between measured and predicted relative pose, a nonlinear least squares problem solved by Gauss-Newton or Levenberg-Marquardt.
3. The resulting system is sparse because each factor touches few variables, so sparse solvers scale to large maps; unlike filtering, it re-linearizes past poses, reducing linearization error.

Try it: Build a 1-D pose graph with poses x0..x4, odometry edges of +1.0 each, a loop edge x4 - x0 = 3.6, and x0 fixed at 0; solve the linear least squares with NumPy and see how the error is distributed.

Needs first: [[Probabilistic_motion_and_sensor_models]], [[Numerical_optimization]], [[SLAM_front_end]]

Related: [[Point_cloud_registration_ICP]], [[Structure_from_motion]]

Part of [[Principles_of_Robot_Autonomy]]. Summary and study notes from the unofficial PoRA Atlas; the book is the authoritative reference.
<!-- pora:end -->
