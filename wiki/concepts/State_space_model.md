# State-space model

A **state-space model** represents a physical system using first-order ODEs in matrix form, capturing internal state variables.

## Form

ẋ = Ax + Bu
y = Cx + Du

## Concepts

- A = system matrix
- B = input matrix
- C = output matrix
- Eigenvalues of A determine [[Lyapunov_stability]]

## Related

- [[Kalman_filter]]
- [[Lyapunov_stability]]
- [[PID_control]]
- [[Observability]]
- [[Transfer_function]]

<!-- pora:begin -->
## In Principles of Robot Autonomy

- Read: [Chapter 1: Modeling Robot Dynamics](https://porabook.com/book/modeling-robot-dynamics/)
- Stack layer: Dynamics & control · classical
- Watch: [AA174A lecture 1: Course Overview and Mobile Robot Kinematics](https://youtu.be/Lgt5ONBtFI0)

### Key ideas

1. The state x is the smallest set of variables that, together with future inputs u, determines the future evolution; dynamics are written x_dot = f(x, u) or x_{k+1} = f(x_k, u_k).
2. A higher-order ODE becomes first-order state-space form by stacking derivatives: m q_ddot = u becomes x = (q, q_dot) with x_dot = (q_dot, u/m).
3. Linear time-invariant models x_dot = A x + B u, y = C x are the special case where controllability, stability, and estimation have clean matrix tests.

Try it: Write the pendulum m l^2 θ_ddot = -m g l sin θ + u in the form x_dot = f(x, u) with x = (θ, θ_dot).

Needs first: [[Linear_algebra]], [[Ordinary_differential_equation]]

Unlocks: [[Kinematic_vs_dynamic_models]], [[Numerical_integration_and_simulation]], [[Optimal_control_problems]], [[PID_control]], [[Linearization]], [[Recursive_Bayes_filter]], [[Model-based_RL_and_system_ID]]

Part of [[Principles_of_Robot_Autonomy]]. Summary and study notes from the unofficial PoRA Atlas; the book is the authoritative reference.
<!-- pora:end -->
