---
source: pora
chapter: 18
layer: L
kind: classical
tags: [pora, robot-autonomy, classical]
---
# Value & policy iteration

Iterative algorithms that compute the optimal value function and policy when the model is known.

<!-- pora:begin -->
## In Principles of Robot Autonomy

- Read: [Chapter 18: Reinforcement Learning](https://porabook.com/book/reinforcement-learning/)
- Stack layer: Decisions & learning · classical
- Run: [Policy Iteration](https://colab.research.google.com/github/StanfordASL/pora-exercises/blob/main/ch18/policy_iteration.ipynb) ([source](https://github.com/StanfordASL/pora-exercises/blob/main/ch18/policy_iteration.ipynb))
- Watch: [AA203 lecture 9: Stochastic DP, Value Iteration, and Policy Iteration](https://youtu.be/C9mLpI8Td9g)

### Key ideas

1. Value iteration repeats V_k+1(s) = max_a [R(s, a) + γ Σ P(s'|s,a) V_k(s')]; the Bellman operator is a γ-contraction, so V_k converges to V* from any start.
2. Policy iteration alternates evaluation (solve V_π = R_π + γ P_π V_π exactly) and improvement (π(s) = argmax_a of the one-step lookahead), and terminates in finitely many iterations.
3. Both need the full model P and R; policy iteration usually needs few iterations but each is expensive, while value iteration has cheap iterations but may need many as γ approaches 1.

Try it: Implement value iteration on a 4x4 gridworld with a +1 goal and -0.04 step cost; count iterations to reach max change below 1e-6 for γ = 0.9 and γ = 0.99.

Needs first: [[dynamic_programming]]

Unlocks: [[Monte_Carlo_and_TD_learning]]

Part of [[Principles_of_Robot_Autonomy]]. Summary and study notes from the unofficial PoRA Atlas; the book is the authoritative reference.
<!-- pora:end -->
