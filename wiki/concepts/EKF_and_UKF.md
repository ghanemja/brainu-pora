---
source: pora
chapter: 12
layer: E
kind: classical
tags: [pora, robot-autonomy, classical]
---
# EKF & UKF

Extend the Kalman filter to nonlinear systems, by linearizing (EKF) or by propagating sigma points (UKF).

<!-- pora:begin -->
## In Principles of Robot Autonomy

- Read: [Chapter 12: Approximate Filters for State Estimation](https://porabook.com/book/approximate-filters/)
- Stack layer: Estimation & mapping · classical
- Run: [EKF UKF Range Bearing](https://colab.research.google.com/github/StanfordASL/pora-exercises/blob/main/ch12/ekf_ukf_range_bearing.ipynb) ([source](https://github.com/StanfordASL/pora-exercises/blob/main/ch12/ekf_ukf_range_bearing.ipynb))
- Watch: [AA174A lecture 13: Parametric Filtering](https://youtu.be/pSBhRF6j-Zc)

### Key ideas

1. The EKF linearizes nonlinear f and h at the current mean using Jacobians F = ∂f/∂x and H = ∂h/∂x, then applies the standard Kalman covariance equations with those matrices.
2. The UKF instead picks 2n+1 sigma points that match the mean and covariance, pushes each through the true nonlinear function, and recomputes a weighted mean and covariance.
3. Both still assume a unimodal Gaussian belief; the UKF is typically more accurate for strong nonlinearities and needs no Jacobians, but neither can represent multimodal beliefs.

Try it: Take x ~ N(1, 0.5^2) and y = x^2. Compare the EKF estimate of E[y] (f(μ)=1) with a Monte Carlo estimate from 100k samples (true value 1.25) and with a 3-point unscented transform.

Needs first: [[Kalman_filter]], [[Linearization]]

Unlocks: [[EKF_localization]]

Part of [[Principles_of_Robot_Autonomy]]. Summary and study notes from the unofficial PoRA Atlas; the book is the authoritative reference.
<!-- pora:end -->
