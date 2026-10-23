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

Needs first: [[Linear_algebra]], [[Ordinary_differential_equation]]

Unlocks: [[Kinematic_vs_dynamic_models]], [[Numerical_integration_and_simulation]], [[Optimal_control_problems]], [[PID_control]], [[Linearization]], [[Recursive_Bayes_filter]], [[Model-based_RL_and_system_ID]]

Part of [[Principles_of_Robot_Autonomy]]. Summary and links from the unofficial PoRA Atlas; the book is the authoritative reference.
<!-- pora:end -->
