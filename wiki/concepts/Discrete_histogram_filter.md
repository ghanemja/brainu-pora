---
source: pora
chapter: 11
layer: E
kind: classical
tags: [pora, robot-autonomy, classical]
---
# Discrete (histogram) filter

Run the Bayes filter over a grid of possible states. Exact but limited to small spaces.

<!-- pora:begin -->
## In Principles of Robot Autonomy

- Read: [Chapter 11: Introduction to Localization and Filtering](https://porabook.com/book/localization-filtering/)
- Stack layer: Estimation & mapping · classical
- Run: [Discrete Bayes](https://colab.research.google.com/github/StanfordASL/pora-exercises/blob/main/ch11/discrete_bayes.ipynb) ([source](https://github.com/StanfordASL/pora-exercises/blob/main/ch11/discrete_bayes.ipynb))

### Key ideas

1. The state space is partitioned into cells, and the belief is a vector of probabilities, one per cell, that sums to 1.
2. Prediction becomes a matrix-vector product (or a convolution for shift-invariant motion) with the transition probabilities; correction is elementwise multiplication by the likelihood followed by normalization.
3. It can represent any multimodal belief exactly up to discretization, but memory and compute grow exponentially with state dimension, so it suits 1-D to 3-D problems.

Try it: In NumPy, make a 1-D circular corridor of 20 cells with doors at 3 positions; implement predict as np.roll plus a small blur kernel and correct with a door sensor, and watch the belief go from multimodal to unimodal.

Needs first: [[Recursive_Bayes_filter]]

Part of [[Principles_of_Robot_Autonomy]]. Summary and study notes from the unofficial PoRA Atlas; the book is the authoritative reference.
<!-- pora:end -->
