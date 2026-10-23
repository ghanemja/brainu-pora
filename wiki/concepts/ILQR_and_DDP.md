---
source: pora
chapter: 3
layer: D
kind: classical
tags: [pora, robot-autonomy, classical]
---
# iLQR & DDP

Repeatedly linearize about the current trajectory and solve an LQR problem, extending LQR to nonlinear systems.

<!-- pora:begin -->
## In Principles of Robot Autonomy

- Read: [Chapter 3: Closed-Loop Control & Trajectory Tracking](https://porabook.com/book/closed-loop-control/)
- Stack layer: Dynamics & control · classical
- Run: [Cartpole Iterative LQR](https://colab.research.google.com/github/StanfordASL/pora-exercises/blob/main/ch03/exercises/cartpole_iterative_lqr.ipynb) ([source](https://github.com/StanfordASL/pora-exercises/blob/main/ch03/exercises/cartpole_iterative_lqr.ipynb))
- Watch: [AA203 lecture 8: Tracking LQR, Iterative LQR, Differential Dynamic Programming](https://youtu.be/1YdgSwEtf_s)

### Key ideas

1. iLQR rolls out the current inputs to get a nominal trajectory, linearizes dynamics and quadratizes cost along it, and solves a time-varying LQR problem for an update.
2. The backward pass produces feedforward terms k_t and feedback gains K_t; the forward pass applies u_t = ū_t + α k_t + K_t (x_t - x̄_t), with a line search on α.
3. DDP is the same idea but keeps second-order dynamics terms in the backward pass; iLQR drops them, making each iteration cheaper while still converging well in practice.

Try it: Implement one iLQR iteration for a 1D system x_{k+1} = x_k + 0.1(x_k^2 + u_k) from zero inputs, and check the cost decreases after the forward pass.

Needs first: [[LQR]]

Part of [[Principles_of_Robot_Autonomy]]. Summary and study notes from the unofficial PoRA Atlas; the book is the authoritative reference.
<!-- pora:end -->
