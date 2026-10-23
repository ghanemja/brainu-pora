---
source: pora
chapter: 7
layer: S
kind: classical
tags: [pora, robot-autonomy, classical]
---
# Visual odometry & loop closure

Estimate the camera's motion frame to frame, and recognize revisited places to correct the drift that accumulates.

<!-- pora:begin -->
## In Principles of Robot Autonomy

- Read: [Chapter 7: Stereo Vision and Structure From Motion](https://porabook.com/book/stereo-vision/)
- Stack layer: Perception · classical

### Key ideas

1. Visual odometry estimates incremental camera motion between consecutive frames (via feature matching and E/PnP, or direct photometric alignment) and chains the increments into a trajectory.
2. Because small errors in each increment compose, VO drifts without bound; monocular VO also drifts in scale, which is why it is often fused with an IMU (visual-inertial odometry).
3. Loop closure recognizes a revisited place (e.g. bag-of-words image retrieval), adds a constraint between the current and earlier pose, and a pose-graph optimization redistributes the accumulated error.

Try it: Simulate a square trajectory by chaining 2D relative poses with small Gaussian noise in yaw and plot how the endpoint error grows with the number of laps.

Needs first: [[Structure_from_motion]]

Related: [[SLAM_front_end]]

Part of [[Principles_of_Robot_Autonomy]]. Summary and study notes from the unofficial PoRA Atlas; the book is the authoritative reference.
<!-- pora:end -->
