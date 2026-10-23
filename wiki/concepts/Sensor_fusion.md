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

Needs first: [[Kalman_filter]], [[Robot_sensors]]

Unlocks: [[Learned_fusion_BEV_and_features]]

Part of [[Principles_of_Robot_Autonomy]]. Summary and links from the unofficial PoRA Atlas; the book is the authoritative reference.
<!-- pora:end -->
