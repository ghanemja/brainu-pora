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

<!-- pora:begin -->
## In Principles of Robot Autonomy

- Read: [Chapter 12: Approximate Filters for State Estimation](https://porabook.com/book/approximate-filters/)
- Stack layer: Estimation & mapping · classical
- Run: [Kalman Filter](https://colab.research.google.com/github/StanfordASL/pora-exercises/blob/main/ch12/exercises/kalman_filter.ipynb) ([source](https://github.com/StanfordASL/pora-exercises/blob/main/ch12/exercises/kalman_filter.ipynb))
- Watch: [AA174A lecture 13: Parametric Filtering](https://youtu.be/pSBhRF6j-Zc)

### Key ideas

1. With x_t = A x_t-1 + B u_t + w, w ~ N(0, Q), and z_t = C x_t + v, v ~ N(0, R), a Gaussian belief stays Gaussian, so the filter only tracks a mean μ and covariance Σ.
2. Predict: μ = A μ + B u, Σ = A Σ A^T + Q. Update: K = Σ C^T (C Σ C^T + R)^-1, μ = μ + K (z - C μ), Σ = (I - K C) Σ.
3. The gain K weighs prediction against measurement: large R (noisy sensor) shrinks K toward trusting the model, small R pushes the estimate toward the measurement.

Try it: Write a 1-D Kalman filter for a constant-position model (A=1, C=1) with Q=0.01 and R=1; feed it noisy readings of a constant and plot how K converges to a steady-state value.

Needs first: [[Recursive_Bayes_filter]], [[Linear_algebra]], [[Measurement_noise_models]]

Unlocks: [[EKF_and_UKF]], [[Sensor_fusion]], [[Object_tracking_and_data_association]]

Part of [[Principles_of_Robot_Autonomy]]. Summary and study notes from the unofficial PoRA Atlas; the book is the authoritative reference.
<!-- pora:end -->
