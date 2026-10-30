---
video: 9X3jGGnbcvU | The Extended Kalman Filter (EKF): Why Taylor Expansions are Awesome | James Han | 6:20
video: c_6WDC66aVk | The Unscented Kalman Filter (UKF): A Full Tutorial | James Han | 9:31
---
## When the model isn't linear

Real robots are nonlinear: the unicycle has $\cos\theta$ in it, and a range sensor has a square root. Push a Gaussian through a nonlinear function and what comes out isn't Gaussian any more. Two fixes keep the Kalman filter's machinery:

$$x_t = f(x_{t-1}, u_t) + \epsilon_t, \qquad z_t = h(x_t) + \delta_t$$

## The EKF: linearize at the mean

The **extended Kalman filter** uses the linearization lesson. At the current mean, replace $f$ and $h$ by their Jacobians,

$$F = \frac{\partial f}{\partial x}\bigg|_{\mu}, \qquad H = \frac{\partial h}{\partial x}\bigg|_{\bar\mu}$$

and run the usual equations: $\bar\mu = f(\mu, u)$ and $\bar\Sigma = F\Sigma F^\top + Q$; then $K = \bar\Sigma H^\top(H\bar\Sigma H^\top + R)^{-1}$ $\mu = \bar\mu + K(z - h(\bar\mu))$ and $\Sigma = (I - KH)\bar\Sigma$. The mean goes through the true nonlinear functions; the covariance and the gain use the straight-line approximation.

## The UKF: push a few points through

The **unscented Kalman filter** skips the Jacobians. It picks $2n + 1$ **sigma points** (for an $n$-dimensional state) that have exactly the belief's mean and covariance, sends each one through the true nonlinear function, and computes a weighted mean and covariance of the results. It captures curvature that a straight-line approximation misses.

## Worked example: $y = x^2$

Take $x \sim \mathcal{N}(1, 0.5^2)$ and $y = x^2$. The true mean is $E[y] = \mu^2 + \sigma^2 = 1.25$.

- **EKF:** $E[y] \approx f(\mu) = 1$. It misses by 0.25 because it ignores the curve.
- **UKF** (one dimension, scaling $\kappa = 2$): sigma points at $1$ and $1 \pm \sqrt{3 \times 0.25} \approx 1 \pm 0.866$, with weights $\tfrac{2}{3}, \tfrac16, \tfrac16$. Squaring them gives $1$, $3.482$ and $0.018$, and

$$\tfrac23 \times 1 + \tfrac16 \times (3.482 + 0.018) = 0.667 + 0.583 = 1.25$$

which is exact.

Both are still a single Gaussian, so neither can say "I'm in one of two hallways". For that you need particles (Monte Carlo localization).

> **Common mistake:** linearizing far from the truth. If the EKF's mean is badly off, its Jacobians describe the wrong part of the curve and the filter can grow overconfident and diverge. A good initial estimate matters.
