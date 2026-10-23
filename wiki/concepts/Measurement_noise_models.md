---
source: pora
chapter: 5
layer: S
kind: classical
tags: [pora, robot-autonomy, classical]
---
# Measurement noise models

Describe sensor error statistically, usually as bias plus Gaussian noise, so estimators can weigh each reading correctly.

<!-- pora:begin -->
## In Principles of Robot Autonomy

- Read: [Chapter 5: Introduction to Robot Sensors](https://porabook.com/book/robot-sensors/)
- Stack layer: Perception · classical

### Key ideas

1. A common model is z = h(x) + b + v with bias b and zero-mean Gaussian noise v ~ N(0, R); bias causes systematic error that averaging cannot remove, while noise averages down.
2. Averaging N independent readings shrinks noise standard deviation by √N; integrating a noisy rate signal produces random-walk error whose standard deviation grows like √t.
3. The covariance R tells an estimator how much to trust each sensor: in a Kalman-style fusion, a reading with smaller variance gets a larger weight (weight proportional to 1/σ^2).

Try it: Generate 1000 readings from each sensor in NumPy, fuse them with inverse-variance weights, and check that the empirical variance is about 0.8 cm^2.

Needs first: [[Robot_sensors]], [[Probability]]

Unlocks: [[Kalman_filter]], [[Probabilistic_motion_and_sensor_models]]

Part of [[Principles_of_Robot_Autonomy]]. Summary and study notes from the unofficial PoRA Atlas; the book is the authoritative reference.
<!-- pora:end -->
