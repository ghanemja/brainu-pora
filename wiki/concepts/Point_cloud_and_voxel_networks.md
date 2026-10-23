---
source: pora
chapter: 9
layer: S
kind: learned
tags: [pora, robot-autonomy, learned]
---
# Point cloud & voxel networks

Architectures such as PointNet and 3D convolutions that consume lidar and depth data directly instead of images.

<!-- pora:begin -->
## In Principles of Robot Autonomy

- Read: [Chapter 9: Deep Learning Architectures for Perception](https://porabook.com/book/deep-learning-perception/)
- Stack layer: Perception · learned

### Key ideas

1. Point clouds are unordered and irregular, so a network must be invariant to point order; images-style convolution does not apply directly.
2. PointNet applies a shared MLP to each point independently and aggregates with a symmetric function (max pooling) into a global feature; PointNet++ adds hierarchical local grouping to capture local structure.
3. Voxel methods grid the space and use 3D (often sparse) convolutions; pillar methods like PointPillars collapse height into a 2D bird's-eye-view pseudo-image so fast 2D CNNs can be used.

Try it: Write a tiny NumPy 'PointNet': random shared weights, ReLU, max over points; verify the output is identical after shuffling the input points.

Needs first: [[Neural_network]]

Unlocks: [[3D_object_detection]]

Part of [[Principles_of_Robot_Autonomy]]. Summary and study notes from the unofficial PoRA Atlas; the book is the authoritative reference.
<!-- pora:end -->
