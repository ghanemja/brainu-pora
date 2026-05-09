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
