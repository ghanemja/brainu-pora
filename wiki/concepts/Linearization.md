---
source: pora
chapter: 3
layer: D
kind: classical
tags: [pora, robot-autonomy, classical]
---
# Linearization

Approximate nonlinear dynamics near a point or trajectory with a linear model so linear tools apply. Automatic differentiation makes the Jacobians cheap.

<!-- pora:begin -->
## In Principles of Robot Autonomy

- Read: [Chapter 3: Closed-Loop Control & Trajectory Tracking](https://porabook.com/book/closed-loop-control/)
- Stack layer: Dynamics & control · classical
- Run: [JAX Linearization](https://colab.research.google.com/github/StanfordASL/pora-exercises/blob/main/ch03/jax_linearization.ipynb) ([source](https://github.com/StanfordASL/pora-exercises/blob/main/ch03/jax_linearization.ipynb))

### Key ideas

1. Around an equilibrium (x*, u*) with f(x*, u*) = 0, dynamics are approximated as δx_dot ≈ A δx + B δu, with A = ∂f/∂x and B = ∂f/∂u evaluated there.
2. Linearizing about a trajectory instead of a point gives time-varying A(t), B(t), which is what trajectory tracking and iLQR use.
3. The approximation is only local: a controller designed on the linear model is guaranteed only near the linearization point, and automatic differentiation computes the Jacobians exactly to machine precision.

Try it: Linearize the pendulum θ_ddot = -(g/l) sin θ + u about θ = 0 and θ = π, and compare the eigenvalues of A in each case.

Needs first: [[State_space_model]], [[Ordinary_differential_equation]]

Unlocks: [[LQR]], [[Trajectory_tracking]], [[EKF_and_UKF]]

Part of [[Principles_of_Robot_Autonomy]]. Summary and study notes from the unofficial PoRA Atlas; the book is the authoritative reference.
<!-- pora:end -->
