---
source: pora
chapter: 17
layer: L
kind: classical
tags: [pora, robot-autonomy, classical]
---
# Markov decision processes

States, actions, transition probabilities, and rewards: the formal model of sequential decisions under uncertainty.

<!-- pora:begin -->
## In Principles of Robot Autonomy

- Read: [Chapter 17: Sequential Decision Making and Dynamic Programming](https://porabook.com/book/decision-making/)
- Stack layer: Decisions & learning · classical

### Key ideas

1. An MDP is (S, A, P, R, γ): states, actions, transition probabilities P(s' | s, a), reward R(s, a), and discount γ in [0, 1).
2. The Markov property means the next state depends only on the current state and action, so an optimal policy can be a function of the current state alone.
3. The objective is to maximize expected discounted return E[Σ γ^t r_t]; γ < 1 keeps infinite sums finite and trades off immediate versus future reward.

Try it: Write a 3-state, 2-action MDP as NumPy arrays P[a, s, s'] and R[s, a]; check each row of P sums to 1 and compute the value of a fixed policy by solving V = R_π + γ P_π V.

Needs first: [[Probability]]

Unlocks: [[dynamic_programming]], [[reinforcement_learning]], [[Behavior_cloning]]

Part of [[Principles_of_Robot_Autonomy]]. Summary and study notes from the unofficial PoRA Atlas; the book is the authoritative reference.
<!-- pora:end -->
