# Kalman filter

The **Kalman filter** is a recursive Bayesian estimator that produces optimal estimates of system state from noisy sensor measurements. Foundation of GPS, missile guidance, and autonomous navigation.

## Two steps

1. **Predict**: project state forward using dynamics model
2. **Update**: correct prediction with sensor measurement weighted by Kalman gain

## Applications

- Inertial navigation systems
- Sensor fusion (IMU + GPS)
- Target tracking radar
- Autonomous vehicle localization

## Related

- [[State_space_model]]
- [[Lyapunov_stability]]
- [[PID_control]]
- [[Sensor_fusion]]
- [[Observability]]
