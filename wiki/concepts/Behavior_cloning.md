---
source: pora
chapter: 19
layer: L
kind: learned
tags: [pora, robot-autonomy, learned]
---
# Behavior cloning

Train a policy by supervised learning on expert demonstrations. Fast to set up, but errors compound once the robot drifts from what it saw.

<!-- pora:begin -->
## In Principles of Robot Autonomy

- Read: [Chapter 19: Imitation Learning](https://porabook.com/book/imitation-learning/)
- Stack layer: Decisions & learning · learned
- Watch: [AA203 lecture 15: Imitation Learning](https://youtu.be/udHX5Auj7ik)

### Key ideas

1. Behavior cloning treats imitation as supervised learning: fit π_θ(a | s) to expert pairs (s, a) by minimizing a loss such as squared error or negative log-likelihood.
2. It needs no reward and no environment interaction during training, making it simple and data-efficient when demonstrations cover the states the policy will visit.
3. Multimodal demonstrations (e.g. passing an obstacle left or right) break a unimodal regressor, which averages them; mixture models, diffusion policies, or action discretization help.

Try it: Create a dataset where s is in [-1, 1] and the action is +1 or -1 at random; fit a linear regressor and a 2-component mixture (or classifier) and compare predictions at s = 0.

Needs first: [[Neural_network]], [[Markov_decision_processes]]

Unlocks: [[Covariate_shift]], [[Inverse_reinforcement_learning]]

Part of [[Principles_of_Robot_Autonomy]]. Summary and study notes from the unofficial PoRA Atlas; the book is the authoritative reference.
<!-- pora:end -->
