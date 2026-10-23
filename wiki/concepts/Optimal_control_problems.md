---
source: pora
chapter: 2
layer: D
kind: classical
tags: [pora, robot-autonomy, classical]
---
# Optimal control problems

Pose motion as choosing inputs that minimize a cost while respecting dynamics and constraints, producing an open-loop plan.

<!-- pora:begin -->
## In Principles of Robot Autonomy

- Read: [Chapter 2: Open-Loop Control & Trajectory Optimization](https://porabook.com/book/open-loop-control/)
- Stack layer: Dynamics & control · classical
- Run: [Unicycle Optimal Control](https://colab.research.google.com/github/StanfordASL/pora-exercises/blob/main/ch02/exercises/unicycle_optimal_control.ipynb) ([source](https://github.com/StanfordASL/pora-exercises/blob/main/ch02/exercises/unicycle_optimal_control.ipynb))
- Watch: [AA174A lecture 2: Trajectory Optimization](https://youtu.be/Kv5G2OlrIbU)
- Watch: [AA203 lecture 3: Calculus of Variations](https://youtu.be/duZJ2_ajLso)

### Key ideas

1. An optimal control problem chooses u(t) to minimize J = h(x(t_f)) + ∫ g(x, u) dt subject to x_dot = f(x, u), initial conditions, and state and input constraints.
2. The cost encodes design trade-offs: penalizing u^2 trades effort for speed, terminal costs pull toward goals, and changing weights changes which trajectory is 'optimal'.
3. The solution is an open-loop input sequence; it is optimal only for the model and initial state assumed, so disturbances require feedback or replanning.

Try it: For a double integrator, write out the cost, dynamics, and boundary conditions for moving from rest at 0 to rest at 1 in 2 s while minimizing ∫ u^2 dt.

Needs first: [[State_space_model]], [[Numerical_optimization]]

Unlocks: [[Indirect_methods_and_Pontryagin]], [[Direct_methods_and_transcription]], [[LQR]], [[Planning_with_dynamics]]

Part of [[Principles_of_Robot_Autonomy]]. Summary and study notes from the unofficial PoRA Atlas; the book is the authoritative reference.
<!-- pora:end -->
