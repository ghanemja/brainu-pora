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

Needs first: [[Recursive_Bayes_filter]], [[Linear_algebra]], [[Measurement_noise_models]]

Unlocks: [[EKF_and_UKF]], [[Sensor_fusion]], [[Object_tracking_and_data_association]]

Part of [[Principles_of_Robot_Autonomy]]. Summary and links from the unofficial PoRA Atlas; the book is the authoritative reference.
<!-- pora:end -->
