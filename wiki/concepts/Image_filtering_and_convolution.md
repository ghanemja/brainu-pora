---
source: pora
chapter: 8
layer: S
kind: classical
tags: [pora, robot-autonomy, classical]
---
# Image filtering & convolution

Slide small kernels over an image to smooth it, find edges, or match templates. The same operation later becomes the core of CNNs.

<!-- pora:begin -->
## In Principles of Robot Autonomy

- Read: [Chapter 8: Classical Methods for Perception](https://porabook.com/book/classical-perception/)
- Stack layer: Perception · classical
- Run: [Correlation Filter](https://colab.research.google.com/github/StanfordASL/pora-exercises/blob/main/ch08/exercises/correlation_filter.ipynb) ([source](https://github.com/StanfordASL/pora-exercises/blob/main/ch08/exercises/correlation_filter.ipynb))
- Watch: [AA174A lecture 10: Image Processing](https://youtu.be/8A3NmdQJRNc)

### Key ideas

1. Linear filtering computes each output pixel as a weighted sum of a neighborhood: g(i,j) = Σ_k,l h(k,l) f(i+k, j+l) (correlation); convolution is the same with the kernel flipped.
2. A box or Gaussian kernel smooths and suppresses noise; derivative kernels like Sobel approximate image gradients, and their magnitude highlights edges (Canny adds smoothing, non-max suppression and hysteresis).
3. Separable kernels such as the 2D Gaussian factor into a row and a column filter, cutting cost from k^2 to 2k operations per pixel; median filtering is nonlinear and removes salt-and-pepper noise well.

Try it: Add Gaussian noise to a step-edge image in NumPy, apply a Sobel filter with and without prior Gaussian blur, and compare the gradient-magnitude plots.

Needs first: [[Linear_algebra]]

Unlocks: [[Feature_detection_and_matching]], [[Classical_visual_recognition]], [[Convolutional_neural_networks]]

Part of [[Principles_of_Robot_Autonomy]]. Summary and study notes from the unofficial PoRA Atlas; the book is the authoritative reference.
<!-- pora:end -->
