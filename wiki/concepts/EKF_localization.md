---
source: pora
chapter: 13
layer: E
kind: classical
tags: [pora, robot-autonomy, classical]
---
# EKF localization

Estimate the robot's pose in a known map by fusing odometry with landmark measurements.

<!-- pora:begin -->
## In Principles of Robot Autonomy

- Read: [Chapter 13: Robot Localization](https://porabook.com/book/robot-localization/)
- Stack layer: Estimation & mapping · classical
- Run: [EKF Localization](https://colab.research.google.com/github/StanfordASL/pora-exercises/blob/main/ch13/exercises/ekf_localization.ipynb) ([source](https://github.com/StanfordASL/pora-exercises/blob/main/ch13/exercises/ekf_localization.ipynb))
- Watch: [AA174A lecture 14: EKF Localization](https://youtu.be/9y_lJdQmKcY)

### Key ideas

1. The state is the pose (x, y, θ) with a known landmark map; prediction uses the motion model with its Jacobian G with respect to the state, and process noise mapped from control space.
2. Each landmark observation z = h(x, m_j) + v is linearized with H = ∂h/∂x, and the innovation z - h(μ) updates the pose; bearing innovations must be wrapped to [-π, π].
3. It requires known data association (which landmark was seen) and a reasonably good initial pose; a wrong association or huge initial error can make it diverge.

Try it: Write the 2x3 Jacobian H of the range-bearing model with respect to (x, y, θ) for a landmark at (m_x, m_y), then verify it numerically with finite differences at one pose.

Needs first: [[EKF_and_UKF]], [[Probabilistic_motion_and_sensor_models]]

Unlocks: [[EKF_SLAM]]

Part of [[Principles_of_Robot_Autonomy]]. Summary and study notes from the unofficial PoRA Atlas; the book is the authoritative reference.
<!-- pora:end -->
