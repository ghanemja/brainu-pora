---
source: pora
chapter: 11
layer: F
kind: foundation
tags: [pora, robot-autonomy, foundation]
---
# Probability & Gaussians

Random variables, Bayes' rule, and the multivariate Gaussian. The book reviews these at the start of the estimation part, and they underpin every filter that follows.

<!-- pora:begin -->
## In Principles of Robot Autonomy

- Read: [Chapter 11: Introduction to Localization and Filtering](https://porabook.com/book/localization-filtering/)
- Stack layer: Foundations · foundation

### Key ideas

1. Bayes' rule p(x|z) = p(z|x) p(x) / p(z) turns a sensor model p(z|x) and a prior p(x) into a posterior belief; it is the core update step of every Bayes filter.
2. A multivariate Gaussian N(μ, Σ) is fully described by its mean and covariance; Σ is symmetric positive semidefinite and its eigenvectors give the axes of the uncertainty ellipse.
3. Gaussians are closed under linear maps: if x ~ N(μ, Σ) then A x + b ~ N(A μ + b, A Σ A^T), which is why the Kalman filter can propagate beliefs exactly for linear systems.

Try it: Draw 10,000 samples from N(0, I) in NumPy, multiply by A = [[2,0],[1,1]], and compare np.cov of the result with A @ A.T.

Unlocks: [[Sampling-based_planning_PRM_RRT]], [[Measurement_noise_models]], [[Recursive_Bayes_filter]], [[Markov_decision_processes]]

Part of [[Principles_of_Robot_Autonomy]]. Summary and study notes from the unofficial PoRA Atlas; the book is the authoritative reference.
<!-- pora:end -->
