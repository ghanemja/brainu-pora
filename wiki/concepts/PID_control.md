# PID control

**PID control** combines Proportional, Integral, and Derivative terms to drive a system to a setpoint.

## Equation

u(t) = Kp·e(t) + Ki·∫e(t)dt + Kd·de/dt

## Tuning

- Ziegler-Nichols
- Cohen-Coon
- Model-based (using [[State_space_model]])

## Limitations

Linear assumption breaks for nonlinear plants. [[Lyapunov_stability]] analysis required.

## Related

- [[State_space_model]]
- [[Lyapunov_stability]]
- [[Transfer_function]]
- [[Kalman_filter]]

<!-- pora:begin -->
## In Principles of Robot Autonomy

- Read: [Chapter 3: Closed-Loop Control & Trajectory Tracking](https://porabook.com/book/closed-loop-control/)
- Stack layer: Dynamics & control · classical
- Run: [PID Control](https://colab.research.google.com/github/StanfordASL/pora-exercises/blob/main/ch03/exercises/pid_control.ipynb) ([source](https://github.com/StanfordASL/pora-exercises/blob/main/ch03/exercises/pid_control.ipynb))

Needs first: [[State_space_model]]

Unlocks: [[Trajectory_tracking]]

Part of [[Principles_of_Robot_Autonomy]]. Summary and links from the unofficial PoRA Atlas; the book is the authoritative reference.
<!-- pora:end -->
