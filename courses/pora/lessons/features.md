---
video: Z_HwkG90Yvw | Corner Detection | Edge Detection | First Principles of Computer Vision | 14:58
video: 4AvTMVD9ig0 | SIFT - 5 Minutes with Cyrill | Cyrill Stachniss | 5:12
---
## What makes a good feature

To match images, you need points you can find again in another view: **distinctive** (unlike their neighbors) and **repeatable** (found again despite changes in viewpoint, scale and lighting).

Slide a small window around an image and watch how its contents change:

- In a **flat** region, nothing changes in any direction.
- On an **edge**, moving along the edge changes nothing, so the position along it is ambiguous.
- At a **corner**, every direction of movement changes the patch.

Corners pin down position in both directions, so they make good features.

## Harris corners

Harris turns that test into math with the **structure tensor**, a sum over a window of image-gradient products:

$$M = \sum_{\text{window}} \begin{bmatrix} I_x^2 & I_x I_y \\ I_x I_y & I_y^2 \end{bmatrix}, \qquad R = \det M - k\,(\operatorname{tr} M)^2$$

with $k \approx 0.04$ to $0.06$. Two large eigenvalues of $M$ means a corner, and gives $R > 0$. One large eigenvalue means an edge, and gives $R < 0$. Both small means flat, and $R \approx 0$.

## Worked example: corner or edge?

Use $k = 0.05$.

- An edge: $M = \begin{bmatrix} 100 & 0 \\ 0 & 1 \end{bmatrix}$. Then $\det M = 100$, $\operatorname{tr} M = 101$, and $R = 100 - 0.05 \times 101^2 \approx -410$. Negative, so an edge.
- A corner: $M = \begin{bmatrix} 100 & 0 \\ 0 & 90 \end{bmatrix}$. Then $\det M = 9000$, $\operatorname{tr} M = 190$, and $R = 9000 - 0.05 \times 190^2 = 7195$. Large and positive, so a corner.

## Descriptors: SIFT and friends

A detector says where a feature is; a **descriptor** summarizes what the patch around it looks like, as a vector you can compare. **SIFT** finds blobs at their natural scale (extrema of a difference-of-Gaussians across scales), rotates the patch to its dominant gradient direction, and builds a 128-number vector: a $4 \times 4$ grid of cells, each with an 8-bin histogram of gradient directions. That makes it robust to scale, rotation and lighting. **ORB** is a fast binary alternative, popular on robots.

## Matching, then the ratio test

To match, find each descriptor's nearest neighbor in the other image. But in repeated textures, such as a row of identical windows, the nearest match is often wrong.

**Lowe's ratio test** keeps a match only if the best distance $d_1$ is clearly smaller than the second-best $d_2$, e.g. $d_1/d_2 < 0.8$. Distances $0.20$ vs $0.50$ (ratio $0.4$) pass; $0.30$ vs $0.33$ (ratio $0.91$) are ambiguous and get dropped. Then **RANSAC** fits a geometric model to the survivors and removes the rest.

> **Common mistake:** trusting raw nearest-neighbor matches. Even a small fraction of wrong matches can wreck a pose or calibration estimate. Always apply the ratio test and a geometric check.
