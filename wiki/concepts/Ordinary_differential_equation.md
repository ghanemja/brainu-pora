---
source: pora
chapter: background
layer: F
kind: foundation
tags: [pora, robot-autonomy, foundation]
---
# Calculus & ODEs

Derivatives, Jacobians, and ordinary differential equations, used to describe how state changes over time.

<!-- pora:begin -->
## In Principles of Robot Autonomy

- Assumed background for the book.
- Stack layer: Foundations · foundation

### Key ideas

1. An ODE x_dot = f(x, u) specifies how the state changes at each instant; given an initial condition and input history, it determines the whole future trajectory (under mild smoothness conditions).
2. The Jacobian ∂f/∂x is the matrix of partial derivatives; it gives the best linear approximation f(x + δx) ≈ f(x) + (∂f/∂x) δx near a point.
3. Equilibria satisfy f(x*, u*) = 0; for the scalar ODE x_dot = a x the solution is x(t) = e^{a t} x(0), which decays if a < 0 and grows if a > 0.

Try it: Compute the Jacobian of f(x) = [x2, -sin(x1)] (a pendulum) by hand, then check it at x = (0, 0) against finite differences in NumPy.

Unlocks: [[Numerical_optimization]], [[State_space_model]], [[Linearization]]

Part of [[Principles_of_Robot_Autonomy]]. Summary and study notes from the unofficial PoRA Atlas; the book is the authoritative reference.
<!-- pora:end -->
