---
source: pora
chapter: 3
layer: D
kind: classical
tags: [pora, robot-autonomy, classical]
---
# LQR

For linear dynamics and quadratic cost, the optimal feedback is a fixed gain matrix from a Riccati equation. The default controller for stabilizing a robot near a setpoint.

<!-- pora:begin -->
## In Principles of Robot Autonomy

- Read: [Chapter 3: Closed-Loop Control & Trajectory Tracking](https://porabook.com/book/closed-loop-control/)
- Stack layer: Dynamics & control · classical
- Run: [LQR](https://colab.research.google.com/github/StanfordASL/pora-exercises/blob/main/ch03/lqr.ipynb) ([source](https://github.com/StanfordASL/pora-exercises/blob/main/ch03/lqr.ipynb))
- Run: [Cartpole LQR Control](https://colab.research.google.com/github/StanfordASL/pora-exercises/blob/main/ch03/exercises/cartpole_lqr_control.ipynb) ([source](https://github.com/StanfordASL/pora-exercises/blob/main/ch03/exercises/cartpole_lqr_control.ipynb))
- Watch: [AA203 lecture 7: Dynamic Programming and Discrete-Time LQR](https://youtu.be/hy-e9g4nugE)

### Key ideas

1. LQR minimizes Σ (x_k^T Q x_k + u_k^T R u_k) subject to x_{k+1} = A x_k + B u_k; the optimal policy is linear state feedback u_k = -K x_k.
2. K comes from the Riccati equation, solved backward in time for finite horizons or as the algebraic Riccati equation for the infinite-horizon steady-state gain.
3. Q and R set the trade-off: larger Q penalizes state error and gives aggressive control, larger R penalizes effort and gives gentler control.

Try it: Use scipy.linalg.solve_discrete_are on a discretized double integrator, compute K = (R + B^T P B)^{-1} B^T P A, and see how K changes as R goes from 0.1 to 10.

Needs first: [[Linearization]], [[Optimal_control_problems]]

Unlocks: [[ILQR_and_DDP]], [[Model_predictive_control]]

Related: [[dynamic_programming]]

Part of [[Principles_of_Robot_Autonomy]]. Summary and study notes from the unofficial PoRA Atlas; the book is the authoritative reference.
<!-- pora:end -->
