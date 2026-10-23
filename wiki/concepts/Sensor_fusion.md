# Sensor fusion

**Sensor fusion** combines data from multiple sensors to produce more accurate, robust estimates than any single sensor could provide. Key for autonomous systems and missile guidance.

## Approaches

- [[Kalman_filter]] (linear, Gaussian)
- Extended Kalman filter (mild nonlinearity)
- Unscented Kalman filter (strong nonlinearity)
- Particle filter (non-Gaussian)

## Defense Applications

- IMU + GPS for inertial navigation
- Radar + EO/IR for target tracking
- Multi-static radar networks

## Related

- [[Kalman_filter]]
- [[State_space_model]]
- [[Observability]]
- [[Target_tracking]]

<!-- pora:begin -->
## In Principles of Robot Autonomy

- Read: [Chapter 15: Sensor Fusion and Object Tracking](https://porabook.com/book/sensor-fusion/)
- Stack layer: Estimation & mapping · classical
- Run: [Kalman Sensor Fusion](https://colab.research.google.com/github/StanfordASL/pora-exercises/blob/main/ch15/exercises/kalman_sensor_fusion.ipynb) ([source](https://github.com/StanfordASL/pora-exercises/blob/main/ch15/exercises/kalman_sensor_fusion.ipynb))

### Key ideas

1. Fusion combines sensors with complementary errors: an IMU is high-rate but drifts when integrated, while GPS is low-rate and noisy but drift-free, so together they give smooth, bounded error.
2. A common design uses the IMU to drive the prediction step at high rate and applies each GPS fix as a measurement update whenever it arrives, handling different rates naturally.
3. Correct fusion needs time-synchronized data, known extrinsic calibration between sensors, and honest noise covariances; overconfident R or Q makes the filter inconsistent.

Try it: Simulate 1-D motion with a noisy biased accelerometer at 100 Hz and noisy position fixes at 1 Hz; compare dead-reckoned position with a Kalman filter fusing both, including a 20 s gap without fixes.

Needs first: [[Kalman_filter]], [[Robot_sensors]]

Unlocks: [[Learned_fusion_BEV_and_features]]

Part of [[Principles_of_Robot_Autonomy]]. Summary and study notes from the unofficial PoRA Atlas; the book is the authoritative reference.
<!-- pora:end -->
