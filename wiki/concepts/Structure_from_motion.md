---
source: pora
chapter: 7
layer: S
kind: classical
tags: [pora, robot-autonomy, classical]
---
# Structure from motion

Jointly recover camera motion and 3D structure from many images, refined with bundle adjustment.

<!-- pora:begin -->
## In Principles of Robot Autonomy

- Read: [Chapter 7: Stereo Vision and Structure From Motion](https://porabook.com/book/stereo-vision/)
- Stack layer: Perception · classical

### Key ideas

1. Structure from motion recovers camera poses and 3D points from feature tracks across many images; with a single camera the reconstruction is only known up to a global scale.
2. A typical pipeline: match features, estimate two-view geometry with RANSAC, triangulate, then add views incrementally by solving PnP (pose from 2D-3D matches) and triangulating new points.
3. Bundle adjustment jointly refines all poses and points by minimizing total reprojection error Σ |x_ij - π(K, R_i, t_i, X_j)|^2, using sparse Levenberg-Marquardt.

Try it: Run OpenCV's recoverPose on two synthetic views, triangulate the points, and verify the result matches ground truth only after dividing by the true baseline length.

Needs first: [[Stereo_depth_and_triangulation]], [[Feature_detection_and_matching]], [[Numerical_optimization]]

Unlocks: [[Visual_odometry_and_loop_closure]]

Part of [[Principles_of_Robot_Autonomy]]. Summary and study notes from the unofficial PoRA Atlas; the book is the authoritative reference.
<!-- pora:end -->
