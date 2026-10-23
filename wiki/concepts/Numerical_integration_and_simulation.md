---
source: pora
chapter: 1
layer: D
kind: classical
tags: [pora, robot-autonomy, classical]
---
# Numerical integration & simulation

Step continuous dynamics forward in time with Euler or Runge–Kutta schemes, and understand when discretization error matters.

<!-- pora:begin -->
## In Principles of Robot Autonomy

- Read: [Chapter 1: Modeling Robot Dynamics](https://porabook.com/book/modeling-robot-dynamics/)
- Stack layer: Dynamics & control · classical
- Run: [Simulation](https://colab.research.google.com/github/StanfordASL/pora-exercises/blob/main/ch01/exercises/simulation.ipynb) ([source](https://github.com/StanfordASL/pora-exercises/blob/main/ch01/exercises/simulation.ipynb))
- Run: [Numerical Integration](https://colab.research.google.com/github/StanfordASL/pora-exercises/blob/main/ch01/numerical_integration.ipynb) ([source](https://github.com/StanfordASL/pora-exercises/blob/main/ch01/numerical_integration.ipynb))

### Key ideas

1. Forward Euler x_{k+1} = x_k + h f(x_k, u_k) is simple but first-order: its global error scales with step size h.
2. Runge-Kutta 4 combines four slope evaluations per step and has global error of order h^4, so it is far more accurate for the same step size.
3. Explicit methods can go unstable on fast or oscillatory dynamics: Euler on x_dot = -a x is stable only when h < 2/a, and on an undamped oscillator it spirals outward, adding energy.

Try it: Simulate x_ddot = -x for 20 s with h = 0.1 using Euler and RK4, and plot the energy (x^2 + x_dot^2)/2 for both.

Needs first: [[State_space_model]]

Unlocks: [[Direct_methods_and_transcription]]

Part of [[Principles_of_Robot_Autonomy]]. Summary and study notes from the unofficial PoRA Atlas; the book is the authoritative reference.
<!-- pora:end -->
