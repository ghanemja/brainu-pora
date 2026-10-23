---
source: pora
chapter: 6
layer: S
kind: classical
tags: [pora, robot-autonomy, classical]
---
# Pinhole camera model

Project 3D points onto an image plane with homogeneous coordinates. The geometric basis for everything a camera tells a robot.

<!-- pora:begin -->
## In Principles of Robot Autonomy

- Read: [Chapter 6: Camera Models and Calibration](https://porabook.com/book/camera-models/)
- Stack layer: Perception · classical
- Watch: [AA174A lecture 7: Sensors and Introduction to Computer Vision](https://youtu.be/emb_KF3OSu0)
- Watch: [AA174A lecture 8: Camera Models & Calibration](https://youtu.be/QyG0PTgLBxQ)

### Key ideas

1. A 3D point (X, Y, Z) in the camera frame projects to pixel u = f_x X/Z + c_x, v = f_y Y/Z + c_y; the division by Z is why far objects look smaller and depth is lost.
2. In homogeneous coordinates projection is linear: λ [u, v, 1]^T = K [R | t] [X, Y, Z, 1]^T, where K holds intrinsics and [R | t] maps world to camera coordinates.
3. Every point along a ray through the optical center maps to the same pixel, so a single image determines direction but not distance; recovering depth needs another view, known size, or a depth sensor.

Try it: Build K with f = 500, c = (320, 240) in NumPy, project the 8 corners of a unit cube 5 m in front of the camera, and plot the resulting pixels.

Needs first: [[Linear_algebra]]

Unlocks: [[Intrinsics_extrinsics_and_calibration]]

Part of [[Principles_of_Robot_Autonomy]]. Summary and study notes from the unofficial PoRA Atlas; the book is the authoritative reference.
<!-- pora:end -->
