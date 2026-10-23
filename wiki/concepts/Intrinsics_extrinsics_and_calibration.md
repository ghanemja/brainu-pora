---
source: pora
chapter: 6
layer: S
kind: classical
tags: [pora, robot-autonomy, classical]
---
# Intrinsics, extrinsics & calibration

Estimate a camera's focal length, distortion, and pose relative to the robot from images of a known pattern.

<!-- pora:begin -->
## In Principles of Robot Autonomy

- Read: [Chapter 6: Camera Models and Calibration](https://porabook.com/book/camera-models/)
- Stack layer: Perception · classical
- Run: [Camera Intrinsics](https://colab.research.google.com/github/StanfordASL/pora-exercises/blob/main/ch06/exercises/camera_intrinsics.ipynb) ([source](https://github.com/StanfordASL/pora-exercises/blob/main/ch06/exercises/camera_intrinsics.ipynb))
- Run: [Camera Extrinsics](https://colab.research.google.com/github/StanfordASL/pora-exercises/blob/main/ch06/exercises/camera_extrinsics.ipynb) ([source](https://github.com/StanfordASL/pora-exercises/blob/main/ch06/exercises/camera_extrinsics.ipynb))
- Watch: [AA174A lecture 8: Camera Models & Calibration](https://youtu.be/QyG0PTgLBxQ)

### Key ideas

1. Intrinsics K = [[f_x, s, c_x], [0, f_y, c_y], [0, 0, 1]] plus lens distortion coefficients describe the camera itself; extrinsics R, t describe its pose relative to the world or robot.
2. Calibration images a known pattern (e.g. a checkerboard) from many poses; each view gives a homography from the planar pattern to the image, which constrains K (Zhang's method).
3. A closed-form initial estimate is refined by nonlinear least squares minimizing reprojection error, the pixel distance between observed corners and corners projected with the estimated parameters.

Try it: Use OpenCV's calibrateCamera on 15 checkerboard photos from your phone and compare the estimated f_x to the focal length in the photo metadata converted to pixels.

Needs first: [[Pinhole_camera_model]], [[Numerical_optimization]]

Unlocks: [[Epipolar_geometry]]

Part of [[Principles_of_Robot_Autonomy]]. Summary and study notes from the unofficial PoRA Atlas; the book is the authoritative reference.
<!-- pora:end -->
