---
video: GUbWsXU1mac | Camera Calibration | Camera Calibration | First Principles of Computer Vision | 7:47
video: 26nV4oDLiqc | Intrinsic Camera Calibration - 5 Minutes with Cyrill | Cyrill Stachniss | 5:59
---
## Two kinds of parameters

Calibration estimates the numbers the camera model needs.

- **Intrinsics** describe the camera itself: focal lengths $f_x, f_y$, principal point $(c_x, c_y)$, sometimes a skew $s$, all collected in $K$, plus **lens distortion** coefficients.
- **Extrinsics** describe where the camera is: a rotation $R$ and translation $t$ relative to the world, a calibration target, or the robot's body.

Intrinsics stay fixed unless you change the lens or focus. Extrinsics change whenever the camera is bumped or re-mounted, and getting camera-to-robot extrinsics right matters as much as the intrinsics.

## Lens distortion

Wide lenses bend straight lines, most visibly near the edges. The usual radial model works in normalized coordinates $(x, y) = (X/Z, Y/Z)$ with $r^2 = x^2 + y^2$:

$$x_d = x\,(1 + k_1 r^2 + k_2 r^4), \qquad y_d = y\,(1 + k_1 r^2 + k_2 r^4)$$

Negative $k_1$ pulls points toward the center (**barrel** distortion); positive $k_1$ pushes them out (**pincushion**). Tangential terms $p_1, p_2$ handle a lens that's slightly tilted relative to the sensor.

## Worked example: how far distortion moves a pixel

A camera has $f = 500$ px and $k_1 = -0.2$ (with $k_2 = 0$). A point at normalized radius $r = 0.5$ would sit $500 \times 0.5 = 250$ px from the center in an ideal pinhole camera.

Distortion scales it by $1 + k_1 r^2 = 1 - 0.2 \times 0.25 = 0.95$, so it actually appears at $237.5$ px: **12.5 pixels** off. Near the center, at $r = 0.1$, the factor is $0.998$, only $0.1$ px off. Distortion barely matters in the middle and dominates at the edges.

## Calibrating with a checkerboard

Print a checkerboard with known square size and photograph it from many poses. Because the board is flat, each image is related to the board by a **homography** $H = K\,[\,r_1 \;\; r_2 \;\; t\,]$, where $r_1, r_2$ are the first two columns of $R$. Since $r_1$ and $r_2$ must be perpendicular and of equal length, each view gives two equations on $K$. With three or more views you can solve for $K$ in closed form: **Zhang's method**, used by OpenCV and MATLAB.

## Refining by reprojection error

The closed-form answer ignores noise and distortion, so it's only a starting point. Then nonlinear least squares adjusts every parameter at once to minimize the **reprojection error**, the pixel distance between each detected corner $x_{ij}$ and where the model projects it:

$$\min_{K,\, k,\, R_i,\, t_i} \sum_{i,j} \big\| x_{ij} - \pi(K, k, R_i, t_i, X_j) \big\|^2$$

A good calibration ends with an RMS error well under one pixel, often 0.1 to 0.3 px.

> **Common mistake:** taking every photo with the board flat-on and in the middle. Then the edges, where distortion lives, have no data, and focal length can't be separated from distance. Tilt the board and cover the corners of the image.
