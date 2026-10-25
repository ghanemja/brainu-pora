---
video: HZGCoVF3YvM | Bayes theorem, the geometry of changing beliefs | 3Blue1Brown | 15:11
video: d_qvLDhkg00 | A pretty reason why Gaussian + Gaussian = Gaussian | 3Blue1Brown | 13:16
---
## Why probability

A robot's sensors are noisy and its motion is never exact, so "where am I?" never has one certain answer. Probability is the language for "I'm probably here, possibly there". Everything in Part III of the course uses three ideas from it.

## 1. Bayes' rule: update a belief with evidence

You have a **prior** belief $p(x)$ about the state, and a **sensor model** $p(z \mid x)$: how likely reading $z$ is if the state is $x$. After seeing $z$, the updated belief, the **posterior**, is

$$p(x \mid z) = \frac{p(z \mid x)\, p(x)}{p(z)}$$

The denominator $p(z)$ just makes the probabilities add up to one. In words: states that explain the reading well gain probability, states that don't lose it. This is exactly the correct step of the Bayes filter.

## 2. The Gaussian: a belief in two numbers

A **Gaussian** (normal distribution) $\mathcal{N}(\mu, \sigma^2)$ is the bell curve: mean $\mu$ at the centre, standard deviation $\sigma$ setting the width. About 68% of the probability lies within $\pm\sigma$ of the mean and 95% within $\pm 2\sigma$. For a vector state it becomes $\mathcal{N}(\mu, \Sigma)$, where the **covariance** matrix $\Sigma$ holds each variable's variance on the diagonal and how they vary together off it. Its eigenvectors are the axes of the uncertainty ellipse.

## 3. Gaussians stay Gaussian

Two facts make Gaussians the workhorse of estimation:

- **A linear map keeps a Gaussian Gaussian.** If $x \sim \mathcal{N}(\mu, \Sigma)$ then $Ax + b \sim \mathcal{N}(A\mu + b,\ A\Sigma A^\top)$. This is the Kalman filter's predict step.
- **Combining a Gaussian belief with a Gaussian measurement gives a Gaussian**, with the inverse-variance weighting from the measurement-noise lesson. This is its update step.

## Worked example

A robot believes its position along a hallway is $\mathcal{N}(0, 4)$: mean 0 m, variance 4 ($\sigma = 2$ m). A sensor reads 3 m with variance 1. Weighting each by the inverse of its variance:

$$\mu_{\text{post}} = \frac{0/4 + 3/1}{1/4 + 1} = \frac{3}{1.25} = 2.4\ \text{m}, \qquad \sigma^2_{\text{post}} = \frac{1}{1.25} = 0.8$$

The estimate moves most of the way toward the more trustworthy sensor, and the uncertainty ends up smaller than either one alone.

For the linear-map rule: if $\Sigma = \operatorname{diag}(1, 1)$ and $A = \operatorname{diag}(2, 1)$, the new covariance is $A\Sigma A^\top = \operatorname{diag}(4, 1)$, because stretching by 2 multiplies the variance by $2^2$.

> **Common mistake:** mixing up standard deviation and variance. Variances add and scale by the square; standard deviations don't. Doubling a quantity doubles $\sigma$ but quadruples $\sigma^2$.
