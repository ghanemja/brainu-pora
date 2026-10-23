---
source: pora
chapter: 12
layer: E
kind: classical
tags: [pora, robot-autonomy, classical]
---
# Particle filter

Represent the belief with weighted samples, which handles multimodal and non-Gaussian distributions.

<!-- pora:begin -->
## In Principles of Robot Autonomy

- Read: [Chapter 12: Approximate Filters for State Estimation](https://porabook.com/book/approximate-filters/)
- Stack layer: Estimation & mapping · classical

### Key ideas

1. The belief is approximated by M samples x^[m] with weights w^[m]; more particles give a better approximation of arbitrary, including multimodal, distributions.
2. Each step samples every particle from the motion model, sets weight w^[m] proportional to p(z_t | x^[m]), then resamples particles with probability proportional to weight.
3. Resampling focuses particles in likely regions but causes particle deprivation; low-variance resampling and resampling only when effective sample size 1/Σ w^2 is low reduce this.

Try it: Implement a 1-D particle filter with 200 particles tracking a random walk; print the effective sample size 1/Σ w^2 each step and compare resampling every step versus only when it drops below 100.

Needs first: [[Recursive_Bayes_filter]]

Unlocks: [[Monte_Carlo_localization]]

Part of [[Principles_of_Robot_Autonomy]]. Summary and study notes from the unofficial PoRA Atlas; the book is the authoritative reference.
<!-- pora:end -->
