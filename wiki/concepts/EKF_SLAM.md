---
source: pora
chapter: 14
layer: E
kind: classical
tags: [pora, robot-autonomy, classical]
---
# EKF SLAM

Add landmark positions to the state so the robot estimates its pose and the map together.

<!-- pora:begin -->
## In Principles of Robot Autonomy

- Read: [Chapter 14: Simultaneous Localization and Mapping (SLAM)](https://porabook.com/book/slam/)
- Stack layer: Estimation & mapping · classical
- Run: [EKF SLAM](https://colab.research.google.com/github/StanfordASL/pora-exercises/blob/main/ch14/exercises/ekf_slam.ipynb) ([source](https://github.com/StanfordASL/pora-exercises/blob/main/ch14/exercises/ekf_slam.ipynb))
- Run: [Range Bearing EKF SLAM](https://colab.research.google.com/github/StanfordASL/pora-exercises/blob/main/ch14/range_bearing_ekf_slam.ipynb) ([source](https://github.com/StanfordASL/pora-exercises/blob/main/ch14/range_bearing_ekf_slam.ipynb))

### Key ideas

1. The state stacks the robot pose and all landmark positions, e.g. [x, y, θ, m1x, m1y, ..., mNx, mNy], with a full joint covariance of size (3+2N)².
2. Correlations between robot and landmarks are essential: observing one landmark again also corrects other correlated landmarks, which is why loop closure shrinks the whole map uncertainty.
3. Each update costs O(N²) due to the dense covariance, and it is sensitive to wrong data association and linearization errors, limiting it to a few hundred landmarks.

Try it: For a robot with 3 pose states and 50 landmarks, compute the size of the covariance matrix and how many numbers it stores; then estimate how this scales if you map 5000 landmarks.

Needs first: [[EKF_localization]]

Part of [[Principles_of_Robot_Autonomy]]. Summary and study notes from the unofficial PoRA Atlas; the book is the authoritative reference.
<!-- pora:end -->
