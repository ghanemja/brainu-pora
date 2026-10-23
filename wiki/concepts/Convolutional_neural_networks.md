---
source: pora
chapter: 9
layer: S
kind: learned
tags: [pora, robot-autonomy, learned]
---
# Convolutional neural networks

Stack learned convolution filters so the network discovers its own features from data.

<!-- pora:begin -->
## In Principles of Robot Autonomy

- Read: [Chapter 9: Deep Learning Architectures for Perception](https://porabook.com/book/deep-learning-perception/)
- Stack layer: Perception · learned
- Run: [CNN](https://colab.research.google.com/github/StanfordASL/pora-exercises/blob/main/ch09/exercises/cnn.ipynb) ([source](https://github.com/StanfordASL/pora-exercises/blob/main/ch09/exercises/cnn.ipynb))

### Key ideas

1. A convolutional layer applies learned kernels shared across all positions, so it has far fewer parameters than a dense layer and responds the same way to a pattern wherever it appears (translation equivariance).
2. Stacking convolutions, nonlinearities (ReLU) and pooling/striding grows the receptive field, so early layers learn edge-like filters and deeper layers respond to parts and objects.
3. Output size per dimension is floor((W - K + 2P)/S) + 1; a K×K conv from C_in to C_out channels has K·K·C_in·C_out weights plus C_out biases, independent of image size.

Try it: Write a naive 2D convolution in NumPy, apply a hand-set vertical-edge kernel to an image, then verify the output shape formula for stride 2 and padding 1.

Needs first: [[Neural_network]], [[Image_filtering_and_convolution]]

Unlocks: [[Object_detection_and_recognition]], [[Semantic_and_instance_segmentation]]

Part of [[Principles_of_Robot_Autonomy]]. Summary and study notes from the unofficial PoRA Atlas; the book is the authoritative reference.
<!-- pora:end -->
