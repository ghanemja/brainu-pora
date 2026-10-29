---
video: _EhY31MSbNM | Pinhole and Perspective Projection | Image Formation | First Principles of Computer Vision | 20:43
video: ND2fa08vxkY | Camera Intrinsics and Extrinsics - 5 Minutes with Cyrill | Cyrill Stachniss | 5:59
---
## From a 3-D point to a pixel

Light from a point passes through a single hole, the **optical center**, and lands on the image plane. For a point $(X, Y, Z)$ in the camera's frame ($Z$ pointing out of the lens), the pixel it lands on is

$$u = f_x \frac{X}{Z} + c_x, \qquad v = f_y \frac{Y}{Z} + c_y$$

$f_x$ and $f_y$ are the focal length measured in pixels, and $(c_x, c_y)$ is the **principal point**, where the optical axis hits the image, usually near its center. The division by $Z$ is the whole story of perspective: farther things look smaller.

## Projection as one matrix

Dividing by $Z$ isn't linear, but **homogeneous coordinates** hide it: add a 1 to every vector and allow an overall scale $\lambda$. Then, for a point given in world coordinates,

$$\lambda \begin{bmatrix} u \\ v \\ 1 \end{bmatrix} = K \,[R \mid t]\, \begin{bmatrix} X_w \\ Y_w \\ Z_w \\ 1 \end{bmatrix}, \qquad K = \begin{bmatrix} f_x & 0 & c_x \\ 0 & f_y & c_y \\ 0 & 0 & 1 \end{bmatrix}$$

$[R \mid t]$ (the **extrinsics**) moves the point from world to camera coordinates; $K$ (the **intrinsics**) maps it to pixels. The scale $\lambda$ comes out as the depth $Z$, and you divide it away at the end.

## Worked example: projecting a point

A camera has $f_x = f_y = 500$ px and $(c_x, c_y) = (320, 240)$. A point sits at $(0.4, -0.2, 2.0)$ m in the camera frame.

$$u = 500 \cdot \frac{0.4}{2.0} + 320 = 420, \qquad v = 500 \cdot \frac{-0.2}{2.0} + 240 = 190$$

Now double every coordinate to $(0.8, -0.4, 4.0)$: the ratios $X/Z$ and $Y/Z$ don't change, so it lands on the same pixel $(420, 190)$. In the same way, a 1.7 m tall person 10 m away spans $500 \times 1.7 / 10 = 85$ pixels.

## A single image loses depth

Every point on the ray from the optical center through a pixel projects to that same pixel. So one image tells you the **direction** to a point, never its distance. A toy car up close and a real car far away can produce identical pixels.

To get depth back, a robot needs extra information: a second view (stereo or motion), an object of known size, an assumption such as "it's on the flat ground", or a depth sensor such as lidar.

## What the pinhole model leaves out

Real lenses gather light through a wide aperture and bend straight lines near the image edges (**lens distortion**). The pinhole model is still the core, because calibration estimates the distortion and removes it first. After that, the formulas above hold to within a fraction of a pixel.

> **Common mistake:** mixing up frame conventions. In the camera frame $Z$ points forward, $X$ right and $Y$ down; robot body frames usually have $x$ forward and $z$ up. Forgetting the rotation between them puts every detection in the wrong place.
