---
source: pora
chapter: 18
layer: L
kind: learned
tags: [pora, robot-autonomy, learned]
---
# Value-based RL (Q-learning)

Learn action values from experience and act greedily on them, scaling to large problems with function approximation.

<!-- pora:begin -->
## In Principles of Robot Autonomy

- Read: [Chapter 18: Reinforcement Learning](https://porabook.com/book/reinforcement-learning/)
- Stack layer: Decisions & learning · learned
- Watch: [AA203 lecture 17: Model-free RL: Value-based Methods](https://youtu.be/zanXSI7zSws)

### Key ideas

1. Q-learning updates Q(s, a) += α [r + γ max_a' Q(s', a') - Q(s, a)]; it is off-policy, learning the greedy policy's values while behaving, e.g., ε-greedily.
2. With a tabular Q and enough exploration plus decaying step sizes, Q-learning converges to Q*, and the optimal policy is π(s) = argmax_a Q*(s, a).
3. Deep Q-networks approximate Q with a neural net, stabilized by experience replay and a slowly updated target network; the max operator also causes overestimation, which Double DQN reduces.

Try it: Implement tabular Q-learning on a 4x4 FrozenLake-style gridworld (deterministic) with ε-greedy exploration; print the greedy policy as arrows after 2000 episodes.

Needs first: [[Monte_Carlo_and_TD_learning]]

Part of [[Principles_of_Robot_Autonomy]]. Summary and study notes from the unofficial PoRA Atlas; the book is the authoritative reference.
<!-- pora:end -->
