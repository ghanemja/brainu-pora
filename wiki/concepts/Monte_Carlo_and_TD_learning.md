---
source: pora
chapter: 18
layer: L
kind: learned
tags: [pora, robot-autonomy, learned]
---
# Monte Carlo & TD learning

Estimate values from sampled experience, either from full episodes or by bootstrapping from the next state's estimate.

<!-- pora:begin -->
## In Principles of Robot Autonomy

- Read: [Chapter 18: Reinforcement Learning](https://porabook.com/book/reinforcement-learning/)
- Stack layer: Decisions & learning · learned

### Key ideas

1. Monte Carlo estimates V(s) by averaging complete returns G_t observed after visiting s; it is unbiased but has high variance and must wait until episode end.
2. TD(0) updates V(s) toward r + γ V(s') after each step: V(s) += α [r + γ V(s') - V(s)], bootstrapping from the current estimate of the next state.
3. TD learns online and has lower variance but is biased by its own estimates; n-step returns and TD(λ) interpolate between TD(0) and Monte Carlo.

Try it: On the 5-state random walk (terminal reward 1 on the right), run MC and TD(0) for 100 episodes with α = 0.1 and compare RMS error against the true values 1/6, 2/6, ..., 5/6.

Needs first: [[reinforcement_learning]], [[Value_and_policy_iteration]]

Unlocks: [[Value-based_RL_Q-learning]]

Part of [[Principles_of_Robot_Autonomy]]. Summary and study notes from the unofficial PoRA Atlas; the book is the authoritative reference.
<!-- pora:end -->
