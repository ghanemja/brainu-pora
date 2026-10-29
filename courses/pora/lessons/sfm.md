---
video: JlOzyyhk1v0 | Structure from Motion Problem | Structure from Motion | First Principles of Computer Vision | 3:56
video: lmj2Jk5tl60 | Bundle Adjustment - 5 Minutes with Cyrill | Cyrill Stachniss | 4:52
---
## Many images in, cameras and points out

**Structure from motion** (SfM) takes a set of overlapping photos and recovers two things at once: the **motion**, a pose $(R_i, t_i)$ for every camera, and the **structure**, a 3-D position $X_j$ for every tracked feature.

Neither is known at the start, and each depends on the other: with known poses you could triangulate points, and with known points you could solve for poses. SfM bootstraps out of this loop. It powers photo-based 3-D mapping, and it is the offline cousin of visual odometry and visual SLAM.

## Building it up one view at a time

A typical incremental pipeline:

- Detect and match features between all image pairs.
- Pick a good starting pair, estimate the essential matrix with RANSAC, recover $(R, t)$, and triangulate the first points.
- Add images one by one: match their features to existing 3-D points and solve **PnP** (camera pose from 2-D–3-D matches), then triangulate new points.
- After every few additions, refine everything with bundle adjustment so errors don't pile up.

## Bundle adjustment

**Bundle adjustment** refines every pose and every point together by minimizing the total reprojection error, the pixel distance between each observation $x_{ij}$ and where point $j$ projects in camera $i$:

$$\min_{\{R_i, t_i\},\, \{X_j\}} \; \sum_{i,j} \big\| x_{ij} - \pi(K, R_i, t_i, X_j) \big\|^2$$

It's nonlinear least squares, solved with Levenberg–Marquardt. The name refers to adjusting the bundles of rays from each camera until they meet their points.

## Worked example: sizing the problem

Take 50 images and 10,000 points, each seen in 5 images on average.

- Unknowns: $50 \times 6$ pose parameters plus $10{,}000 \times 3$ point coordinates, so $30{,}300$.
- Residuals: $10{,}000 \times 5 = 50{,}000$ observations, each giving 2 numbers ($u$ and $v$), so $100{,}000$.

That looks huge, but each residual touches only one camera (6 unknowns) and one point (3 unknowns). The Jacobian is extremely sparse, and solvers exploit that structure (the Schur complement eliminates the points first), so this solves in seconds.

## What anchors the scale

With one camera, the reconstruction is only defined up to a **similarity transform**: 3 for rotation, 3 for translation, and 1 for scale. Double every distance, including the camera baselines, and every image stays the same. So 7 degrees of freedom must be fixed by convention, for example by setting the first camera at the origin and the first baseline to length 1.

> **Common mistake:** treating monocular SfM units as meters. They're arbitrary. To get metric scale you need outside information: a known object size, a stereo baseline, GPS, or an IMU.
