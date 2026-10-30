---
video: C_zFhWdM4ic | How Blurs & Filters Work - Computerphile | Computerphile | 7:52
video: uihBwtPIBxM | Finding the Edges (Sobel Operator) - Computerphile | Computerphile | 7:46
---
## A weighted average over a window

A linear filter replaces each pixel by a weighted sum of its neighbors. The weights form a small grid called a **kernel** $h$:

$$g(i, j) = \sum_{k, l} h(k, l)\, f(i + k,\, j + l)$$

This is **correlation**. **Convolution** is the same with the kernel flipped, $f(i - k, j - l)$; for symmetric kernels such as a blur, the two agree. Different kernels do very different jobs: smooth noise, find edges, sharpen, or match a template. The same sliding operation, with learned kernels, is the core of a CNN.

## Smoothing

A **box filter** averages a $3 \times 3$ window with equal weights $1/9$. A **Gaussian filter** weights nearby pixels more, using $h(k, l) \propto e^{-(k^2 + l^2)/2\sigma^2}$, which blurs more naturally and doesn't create blocky artifacts. A larger $\sigma$ removes more noise and more detail.

Not every useful filter is linear. A **median filter** takes the median of the window instead of a weighted mean. It removes salt-and-pepper noise (isolated black and white pixels) while keeping edges sharp, which no linear blur can do.

## Edges from derivative kernels

An edge is a place where brightness changes fast, so you find it with derivatives. The **Sobel** kernel approximates $\partial f / \partial x$ while smoothing a little across rows:

$$G_x = \begin{bmatrix} -1 & 0 & 1 \\ -2 & 0 & 2 \\ -1 & 0 & 1 \end{bmatrix}$$

Its transpose gives $\partial f/\partial y$. The **gradient magnitude** $\sqrt{G_x^2 + G_y^2}$ is large on edges, and its direction is perpendicular to them. The **Canny** detector adds smoothing, keeps only the thin ridge of the gradient (non-maximum suppression), and links edges with two thresholds.

## Worked example: Sobel on a vertical edge

Take a $3 \times 3$ patch where the left two columns are dark (10) and the right column is bright (50). Apply $G_x$ at the center:

$$(-1 \cdot 10 + 1 \cdot 50) + (-2 \cdot 10 + 2 \cdot 50) + (-1 \cdot 10 + 1 \cdot 50) = 40 + 80 + 40 = 160$$

The rows are identical, so $G_y = 0$. The magnitude is 160 and the gradient points along $+x$, from dark to bright, across the vertical edge. On a flat patch both responses would be 0.

## Separable kernels save time

A 2-D Gaussian factors into a 1-D row filter followed by a 1-D column filter. A $7 \times 7$ kernel then costs $7 + 7 = 14$ multiplications per pixel instead of $49$, and the result is identical. On a 640 × 480 image that's about 4.3 million operations saved per frame, which matters at 30 frames per second.

> **Common mistake:** taking derivatives of a raw, noisy image. Differencing amplifies pixel noise, so you get edges everywhere. Smooth first, or use a combined derivative-of-Gaussian kernel, then threshold.
