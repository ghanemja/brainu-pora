---
source: pora
chapter: 7
layer: S
kind: classical
tags: [pora, robot-autonomy, classical]
---
# Epipolar geometry

Two views of a scene constrain where a point in one image can appear in the other, captured by the essential and fundamental matrices.

<!-- pora:begin -->
## In Principles of Robot Autonomy

- Read: [Chapter 7: Stereo Vision and Structure From Motion](https://porabook.com/book/stereo-vision/)
- Stack layer: Perception · classical
- Watch: [AA174A lecture 9: Stereo Vision](https://youtu.be/idD08N4rgJU)

### Key ideas

1. A point x in image 1 back-projects to a ray; that ray projects into image 2 as the epipolar line, so the match x' must lie on a line rather than anywhere in the image.
2. For calibrated cameras x'^T E x = 0 with essential matrix E = [t]× R (normalized coordinates); with pixel coordinates x'^T F x = 0 where F = K'^(-T) E K^(-1).
3. F has rank 2 and 7 degrees of freedom and can be estimated from 8 correspondences (eight-point algorithm) inside RANSAC; E has 5 degrees of freedom since translation scale is unobservable.

Try it: Pick R and t, form E = [t]× R in NumPy, project random 3D points into both normalized views, and check that x2^T E x1 ≈ 0 for every point.

Needs first: [[Intrinsics_extrinsics_and_calibration]]

Unlocks: [[Stereo_depth_and_triangulation]]

Part of [[Principles_of_Robot_Autonomy]]. Summary and study notes from the unofficial PoRA Atlas; the book is the authoritative reference.
<!-- pora:end -->
