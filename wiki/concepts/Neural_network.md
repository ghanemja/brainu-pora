---
source: pora
chapter: background
layer: F
kind: foundation
tags: [pora, robot-autonomy, foundation]
---
# Neural networks & training

Layers, losses, backpropagation, and stochastic gradient descent. Needed for learned perception and learned policies.

<!-- pora:begin -->
## In Principles of Robot Autonomy

- Assumed background for the book.
- Stack layer: Foundations · foundation

### Key ideas

1. A neural network composes layers h = σ(W x + b); the nonlinearity σ (ReLU, tanh) is what lets stacks of layers represent functions beyond a single linear map.
2. Training minimizes a loss (e.g. mean squared error or cross-entropy) over parameters; backpropagation is the chain rule applied efficiently to get the gradient of the loss with respect to every weight.
3. Stochastic gradient descent updates weights using gradients from small minibatches; it is cheaper per step than full-batch descent and the noise is tolerated or even helpful.

Try it: In NumPy, fit y = sin(x) on [-3, 3] with a one-hidden-layer ReLU network trained by hand-coded backprop and SGD, and plot the fit after 2000 steps.

Needs first: [[Linear_algebra]], [[Numerical_optimization]]

Unlocks: [[Convolutional_neural_networks]], [[Attention_and_vision_transformers]], [[Point_cloud_and_voxel_networks]], [[reinforcement_learning]], [[Behavior_cloning]]

Part of [[Principles_of_Robot_Autonomy]]. Summary and study notes from the unofficial PoRA Atlas; the book is the authoritative reference.
<!-- pora:end -->
