---
source: pora
chapter: 8
layer: S
kind: classical
tags: [pora, robot-autonomy, classical]
---
# Point cloud registration (ICP)

Align two 3D scans by alternating between matching nearest points and solving for the best rigid transform.

<!-- pora:begin -->
## In Principles of Robot Autonomy

- Read: [Chapter 8: Classical Methods for Perception](https://porabook.com/book/classical-perception/)
- Stack layer: Perception · classical
- Run: [ICP](https://colab.research.google.com/github/StanfordASL/pora-exercises/blob/main/ch08/exercises/icp.ipynb) ([source](https://github.com/StanfordASL/pora-exercises/blob/main/ch08/exercises/icp.ipynb))

### Key ideas

1. Registration finds a rigid transform (R, t) minimizing Σ |R p_i + t - q_i|^2; with known correspondences this has a closed-form solution via the SVD of the cross-covariance of the centered points (Kabsch/Umeyama).
2. ICP alternates: match each source point to its nearest neighbor in the target (with the current transform), then solve the closed-form alignment, and repeat until the error stops decreasing.
3. ICP converges only to a local minimum, so it needs a good initial guess (e.g. from odometry or feature-based global registration); point-to-plane error and outlier rejection speed it up and improve robustness.

Try it: Rotate a random 2D point set by 20 degrees, add noise, and recover R, t with a 15-line NumPy ICP using SVD; then try 90 degrees and watch it fail.

Needs first: [[Linear_algebra]], [[Numerical_optimization]]

Unlocks: [[SLAM_front_end]]

Part of [[Principles_of_Robot_Autonomy]]. Summary and study notes from the unofficial PoRA Atlas; the book is the authoritative reference.
<!-- pora:end -->
