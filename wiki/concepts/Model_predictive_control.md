---
source: pora
chapter: 3
layer: D
kind: classical
tags: [pora, robot-autonomy, classical]
---
# Model predictive control

Re-solve a short-horizon trajectory optimization at every step and apply only the first input. Handles constraints explicitly.

<!-- pora:begin -->
## In Principles of Robot Autonomy

- Read: [Chapter 3: Closed-Loop Control & Trajectory Tracking](https://porabook.com/book/closed-loop-control/)
- Stack layer: Dynamics & control · classical
- Run: [Linear MPC](https://colab.research.google.com/github/StanfordASL/pora-exercises/blob/main/ch03/exercises/linear_mpc.ipynb) ([source](https://github.com/StanfordASL/pora-exercises/blob/main/ch03/exercises/linear_mpc.ipynb))
- Watch: [AA203 lecture 11: Introduction to Model Predictive Control](https://youtu.be/3_gxaB_Pp3k)
- Watch: [AA203 lecture 12: Persistent Feasibility of MPC, Stability, and Explicit MPC](https://youtu.be/8Elrw30y0tg)

### Key ideas

1. MPC solves a finite-horizon optimal control problem from the current measured state at each step, applies only the first input, then shifts the horizon and repeats.
2. Constraints on inputs and states (actuator limits, obstacles) enter the optimization directly, which LQR and PID cannot do natively.
3. Re-solving from fresh measurements makes MPC a feedback controller; stability is usually encouraged with terminal costs or constraints, and computation time limits horizon length.

Try it: Implement MPC for a double integrator with |u| ≤ 1 using scipy.optimize over a 10-step horizon, and compare its response to an unconstrained LQR whose inputs are clipped.

Needs first: [[Direct_methods_and_transcription]], [[LQR]]

Part of [[Principles_of_Robot_Autonomy]]. Summary and study notes from the unofficial PoRA Atlas; the book is the authoritative reference.
<!-- pora:end -->
