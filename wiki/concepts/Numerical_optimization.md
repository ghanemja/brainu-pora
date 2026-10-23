---
source: pora
chapter: background
layer: F
kind: foundation
tags: [pora, robot-autonomy, foundation]
---
# Numerical optimization

Minimizing a cost subject to constraints: gradients, optimality conditions, and the solvers that trajectory optimization and calibration run on.

<!-- pora:begin -->
## In Principles of Robot Autonomy

- Assumed background for the book.
- Stack layer: Foundations · foundation
- Watch: [AA203 lecture 1: Course Overview and Intro to Nonlinear Optimization](https://youtu.be/Au2stLALZew)
- Watch: [AA203 lecture 2: Optimization Theory](https://youtu.be/FbkNYklySak)

### Key ideas

1. For unconstrained smooth problems, a local minimum has zero gradient and positive semidefinite Hessian; gradient descent steps along -∇f, while Newton's method uses the Hessian for faster local convergence.
2. With constraints, the KKT conditions generalize ∇f = 0: at an optimum the cost gradient is a combination of active constraint gradients, weighted by Lagrange multipliers.
3. Convex problems (convex cost, convex feasible set) have every local minimum global; nonconvex ones, like most trajectory optimization, depend on initialization.

Try it: Minimize f(x) = x^4 - 3x^2 + x with gradient descent starting from x = -2 and x = 2, and note which local minimum each run finds.

Needs first: [[Linear_algebra]], [[Ordinary_differential_equation]]

Unlocks: [[Neural_network]], [[Optimal_control_problems]], [[Intrinsics_extrinsics_and_calibration]], [[Structure_from_motion]], [[Point_cloud_registration_ICP]], [[Graph_and_factor-graph_SLAM]]

Part of [[Principles_of_Robot_Autonomy]]. Summary and study notes from the unofficial PoRA Atlas; the book is the authoritative reference.
<!-- pora:end -->
