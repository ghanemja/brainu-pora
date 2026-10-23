---
source: pora
chapter: 13
layer: E
kind: classical
tags: [pora, robot-autonomy, classical]
---
# Probabilistic motion & sensor models

Odometry and range-bearing models written as probability distributions, ready to plug into a filter.

<!-- pora:begin -->
## In Principles of Robot Autonomy

- Read: [Chapter 13: Robot Localization](https://porabook.com/book/robot-localization/)
- Stack layer: Estimation & mapping · classical

### Key ideas

1. A probabilistic motion model p(x_t | u_t, x_t-1) gives a distribution over the next pose; the odometry model decomposes motion into rotation, translation, rotation, each corrupted by noise.
2. A range-bearing sensor model predicts r = sqrt((m_x - x)^2 + (m_y - y)^2) and φ = atan2(m_y - y, m_x - x) - θ, with additive Gaussian noise, giving p(z | x, m).
3. Sampling from the motion model naturally produces the curved 'banana' distribution that a Gaussian over (x, y, θ) cannot capture well, because heading uncertainty bends the position spread.

Try it: Sample 1000 end poses for a robot starting at the origin driving 5 m with heading noise of 0.1 rad and distance noise of 0.1 m; scatter-plot x versus y and observe the arc.

Needs first: [[Nonholonomic_wheeled_robots]], [[Measurement_noise_models]]

Unlocks: [[EKF_localization]], [[Monte_Carlo_localization]], [[Graph_and_factor-graph_SLAM]]

Part of [[Principles_of_Robot_Autonomy]]. Summary and study notes from the unofficial PoRA Atlas; the book is the authoritative reference.
<!-- pora:end -->
