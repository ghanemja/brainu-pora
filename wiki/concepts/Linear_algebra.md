---
source: pora
chapter: background
layer: F
kind: foundation
tags: [pora, robot-autonomy, foundation]
---
# Linear algebra

Vectors, matrices, eigenvalues, and least squares. Nearly every model in robotics is written in this language.

<!-- pora:begin -->
## In Principles of Robot Autonomy

- Assumed background for the book.
- Stack layer: Foundations · foundation

### Key ideas

1. A matrix is a linear map: Ax mixes the columns of A weighted by the entries of x, so rank tells you how many independent directions the map can reach.
2. Eigenvalues of A govern repeated application: x_k+1 = A x_k decays to zero exactly when every eigenvalue has magnitude less than 1.
3. When Ax = b has no exact solution (more equations than unknowns), least squares picks x minimizing ‖Ax - b‖^2, given by the normal equations A^T A x = A^T b.

Try it: In NumPy, generate y = 2t + 1 plus noise for 50 points, build A = [t, 1], and compare np.linalg.lstsq(A, y) with solving A^T A x = A^T y directly.

Unlocks: [[Numerical_optimization]], [[Neural_network]], [[State_space_model]], [[Pinhole_camera_model]], [[Image_filtering_and_convolution]], [[Point_cloud_registration_ICP]], [[Kalman_filter]]

Part of [[Principles_of_Robot_Autonomy]]. Summary and study notes from the unofficial PoRA Atlas; the book is the authoritative reference.
<!-- pora:end -->
