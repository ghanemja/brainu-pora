---
video: 6kpBqfgSPRc | Epipolar Geometry | Uncalibrated Stereo | First Principles of Computer Vision | 14:42
---
## A point in one image is a line in the other

Take a pixel $x$ in image 1. The 3-D point it came from lies somewhere on the ray through camera 1's optical center and $x$. Seen from camera 2, that ray is a line in image 2: the **epipolar line**. Its match $x'$ must lie on that line.

So the search for a match shrinks from the whole image to a single line, which is faster and has far fewer chances of a wrong match. All epipolar lines in image 2 pass through one point, the **epipole**, where camera 1's center appears in image 2.

## The essential matrix

Work in normalized coordinates, $\hat x = K^{-1} x$, and let camera 2's frame relate to camera 1's by $X_2 = R X_1 + t$. The vectors $X_2$, $t$ and $R X_1$ all lie in one plane, which gives the **epipolar constraint**:

$$\hat x'^\top E\, \hat x = 0, \qquad E = [t]_\times R$$

$[t]_\times$ is the matrix that computes a cross product with $t$. The **essential matrix** $E$ holds the relative pose. It has 5 degrees of freedom: 3 for rotation and 2 for the direction of $t$. The length of $t$ can't be recovered, since scaling the whole scene and baseline together changes no pixel.

## The fundamental matrix

With uncalibrated cameras, or just working in pixels, the same constraint becomes

$$x'^\top F\, x = 0, \qquad F = K'^{-\top} E\, K^{-1}$$

The epipolar line in image 2 is simply $l' = F x$: the coefficients $(a, b, c)$ of the line $a u' + b v' + c = 0$. $F$ is $3 \times 3$ with rank 2 and 7 degrees of freedom. The **eight-point algorithm** estimates it linearly from 8 or more matches, inside RANSAC to reject bad ones.

## Worked example: two cameras side by side

Let the cameras be identical and shifted sideways: $R = I$ and $t = (1, 0, 0)$. Then

$$E = [t]_\times = \begin{bmatrix} 0 & 0 & 0 \\ 0 & 0 & -1 \\ 0 & 1 & 0 \end{bmatrix}$$

For a point $\hat x = (x, y, 1)$, the epipolar line is $E \hat x = (0, -1, y)$, meaning $-y' + y = 0$, or $y' = y$. The match is on **the same row**. That's why stereo rigs are aligned, or images rectified, so that matching becomes a 1-D search along rows.

## Using it on a robot

Visual odometry estimates $E$ from matches between consecutive frames, then decomposes it into $R$ and the direction of $t$. Four $(R, t)$ combinations fit; the right one puts the triangulated points in front of both cameras. Robust estimation matters: real matches include outliers, so RANSAC with the 5-point (for $E$) or 8-point (for $F$) solver is the standard.

> **Common mistake:** running the eight-point algorithm on raw pixel coordinates. Values near 500 and values near 1 in the same equations make it badly conditioned. Shift and scale the points to have mean zero and average distance $\sqrt2$ first (Hartley normalization).
