---
source: pora
chapter: 11
layer: E
kind: classical
tags: [pora, robot-autonomy, classical]
---
# Recursive Bayes filter

Maintain a belief over state with two alternating steps: predict with the motion model, correct with the measurement.

<!-- pora:begin -->
## In Principles of Robot Autonomy

- Read: [Chapter 11: Introduction to Localization and Filtering](https://porabook.com/book/localization-filtering/)
- Stack layer: Estimation & mapping · classical
- Watch: [AA174A lecture 12: Localization & Filters](https://youtu.be/dG3-D-vDwe8)

### Key ideas

1. The belief bel(x_t) = p(x_t | z_1:t, u_1:t) is a full probability distribution over the state, not a single guess, so it captures both the estimate and its uncertainty.
2. Predict: bel_bar(x_t) = ∫ p(x_t | u_t, x_t-1) bel(x_t-1) dx_t-1 spreads the belief through the motion model, which typically increases uncertainty.
3. Correct: bel(x_t) = η p(z_t | x_t) bel_bar(x_t) reweights by the measurement likelihood and renormalizes; recursion works because of the Markov assumption on state and measurements.

Try it: For a door/no-door world with prior P(door)=0.5, sensor P(z=door|door)=0.6 and P(z=door|no door)=0.2, compute the posterior after one 'door' reading by hand, then after two readings.

Needs first: [[Probability]], [[State_space_model]]

Unlocks: [[Discrete_histogram_filter]], [[Kalman_filter]], [[Particle_filter]]

Part of [[Principles_of_Robot_Autonomy]]. Summary and study notes from the unofficial PoRA Atlas; the book is the authoritative reference.
<!-- pora:end -->
