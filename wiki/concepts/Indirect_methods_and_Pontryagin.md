---
source: pora
chapter: 2
layer: D
kind: classical
tags: [pora, robot-autonomy, classical]
---
# Indirect methods & Pontryagin

Derive necessary conditions for optimality first, then solve them. This turns trajectory optimization into a boundary value problem.

<!-- pora:begin -->
## In Principles of Robot Autonomy

- Read: [Chapter 2: Open-Loop Control & Trajectory Optimization](https://porabook.com/book/open-loop-control/)
- Stack layer: Dynamics & control · classical
- Run: [TPBVP](https://colab.research.google.com/github/StanfordASL/pora-exercises/blob/main/ch02/tpbvp.ipynb) ([source](https://github.com/StanfordASL/pora-exercises/blob/main/ch02/tpbvp.ipynb))
- Run: [Free Final Time Optimal Control](https://colab.research.google.com/github/StanfordASL/pora-exercises/blob/main/ch02/free_final_time_optimal_control.ipynb) ([source](https://github.com/StanfordASL/pora-exercises/blob/main/ch02/free_final_time_optimal_control.ipynb))
- Run: [Zermelos Problem](https://colab.research.google.com/github/StanfordASL/pora-exercises/blob/main/ch02/zermelos_problem.ipynb) ([source](https://github.com/StanfordASL/pora-exercises/blob/main/ch02/zermelos_problem.ipynb))
- Watch: [AA203 lecture 4: Indirect Methods for Optimal Control](https://youtu.be/7rejaoMWviw)
- Watch: [AA203 lecture 5: Pontryagin's Minimum Principle and Computational Methods](https://youtu.be/R4_fHzTo0IM)

### Key ideas

1. Pontryagin's principle introduces costates p and the Hamiltonian H = g(x, u) + p^T f(x, u); the optimal input minimizes H at each time.
2. Necessary conditions are x_dot = ∂H/∂p, p_dot = -∂H/∂x, plus boundary conditions on x(0) and on x(t_f) or p(t_f), giving a two-point boundary value problem.
3. Indirect methods can be very accurate but are sensitive: shooting on the costate initial value often diverges without a good guess, and inequality constraints complicate the conditions.

Try it: For x_dot = u minimizing ∫ u^2/2 dt from x(0)=0 to x(1)=1, form H, derive p_dot = 0 and u = -p, and solve for the constant optimal u.

Needs first: [[Optimal_control_problems]]

Part of [[Principles_of_Robot_Autonomy]]. Summary and study notes from the unofficial PoRA Atlas; the book is the authoritative reference.
<!-- pora:end -->
