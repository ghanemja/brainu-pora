---
source: pora
chapter: 19
layer: L
kind: learned
tags: [pora, robot-autonomy, learned]
---
# Inverse reinforcement learning

Infer the reward an expert seems to be optimizing, then learn a policy for that reward.

<!-- pora:begin -->
## In Principles of Robot Autonomy

- Read: [Chapter 19: Imitation Learning](https://porabook.com/book/imitation-learning/)
- Stack layer: Decisions & learning · learned
- Watch: [AA203 lecture 15: Imitation Learning](https://youtu.be/udHX5Auj7ik)

### Key ideas

1. Inverse RL assumes the expert is near-optimal for an unknown reward R and seeks an R under which the expert's behavior beats alternatives, then solves RL for that R.
2. The problem is ill-posed: many rewards (including R = 0) explain the same behavior, so methods add structure such as feature matching or the maximum entropy principle.
3. A learned reward can transfer to new dynamics or environments better than a cloned policy, but IRL is expensive since it typically solves an RL problem inside its loop.

Try it: In a 1-D chain of 5 states, write two different reward functions (including a shaped one) that both make 'always move right' optimal, illustrating why IRL is ill-posed.

Needs first: [[Behavior_cloning]], [[reinforcement_learning]]

Part of [[Principles_of_Robot_Autonomy]]. Summary and study notes from the unofficial PoRA Atlas; the book is the authoritative reference.
<!-- pora:end -->
