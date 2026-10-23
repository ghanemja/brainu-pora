---
source: pora
chapter: 2
layer: D
kind: classical
tags: [pora, robot-autonomy, classical]
---
# Direct methods & transcription

Discretize the trajectory and hand the whole problem to a nonlinear solver. The workhorse of practical trajectory optimization.

<!-- pora:begin -->
## In Principles of Robot Autonomy

- Read: [Chapter 2: Open-Loop Control & Trajectory Optimization](https://porabook.com/book/open-loop-control/)
- Stack layer: Dynamics & control · classical
- Watch: [AA174A lecture 4: Advanced Trajectory Optimization](https://youtu.be/Izu4_AUiHyk)
- Watch: [AA203 lecture 6: Direct Methods for Optimal Control](https://youtu.be/zX8raxUa2DE)

### Key ideas

1. Direct methods discretize first: choose decision variables such as x_0..x_N and u_0..u_{N-1}, then optimize with a nonlinear programming solver.
2. In direct collocation or multiple shooting, dynamics become equality constraints like x_{k+1} = x_k + h f(x_k, u_k), so infeasible guesses are allowed and the solver repairs them.
3. Path and input constraints (obstacles, torque limits) are added directly as inequalities, which is a main reason direct methods dominate in practice.

Try it: Use scipy.optimize.minimize (SLSQP) to move a double integrator from 0 to 1 in N = 20 steps, with x_k and u_k as variables and Euler dynamics as equality constraints.

Needs first: [[Optimal_control_problems]], [[Numerical_integration_and_simulation]]

Unlocks: [[Model_predictive_control]]

Part of [[Principles_of_Robot_Autonomy]]. Summary and study notes from the unofficial PoRA Atlas; the book is the authoritative reference.
<!-- pora:end -->
