---
source: pora
chapter: 18
layer: L
kind: learned
tags: [pora, robot-autonomy, learned]
---
# Policy gradients & actor-critic

Optimize a parameterized policy directly by gradient ascent on expected return, with a learned critic to reduce variance.

<!-- pora:begin -->
## In Principles of Robot Autonomy

- Read: [Chapter 18: Reinforcement Learning](https://porabook.com/book/reinforcement-learning/)
- Stack layer: Decisions & learning · learned
- Run: [Advantage Actor Critic](https://colab.research.google.com/github/StanfordASL/pora-exercises/blob/main/ch18/exercises/advantage_actor_critic.ipynb) ([source](https://github.com/StanfordASL/pora-exercises/blob/main/ch18/exercises/advantage_actor_critic.ipynb))
- Run: [Cartpole Balance](https://colab.research.google.com/github/StanfordASL/pora-exercises/blob/main/ch18/exercises/cartpole_balance.ipynb) ([source](https://github.com/StanfordASL/pora-exercises/blob/main/ch18/exercises/cartpole_balance.ipynb))
- Watch: [AA203 lecture 18: Model-free RL: Policy Optimization](https://youtu.be/a1g9U_5zO54)

### Key ideas

1. Policy gradient methods parameterize π_θ(a|s) and ascend J(θ) = E[Σ γ^t r_t] using ∇J = E[Σ_t ∇_θ log π_θ(a_t|s_t) G_t] (REINFORCE), which needs no dynamics model.
2. Subtracting a baseline b(s), such as V(s), from G_t leaves the gradient unbiased but lowers variance; using A(s, a) = Q(s, a) - V(s) gives the advantage form.
3. Actor-critic methods learn a critic (e.g. V_w via TD) to estimate advantages for the actor; PPO and similar methods also limit the policy change per update for stability.

Try it: For a 2-action softmax policy on a bandit with rewards 1 and 0, estimate the gradient with 1000 samples with and without a baseline of 0.5, and compare the means and variances.

Needs first: [[reinforcement_learning]]

Part of [[Principles_of_Robot_Autonomy]]. Summary and study notes from the unofficial PoRA Atlas; the book is the authoritative reference.
<!-- pora:end -->
