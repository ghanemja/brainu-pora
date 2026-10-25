---
video: mwn8xhgNpFY | Why Use Kalman Filters? | Understanding Kalman Filters, Part 1 | MATLAB | 6:47
video: o_HW6GnLqvg | Kalman Filter - 5 Minutes with Cyrill | Cyrill Stachniss | 4:02
---
## The Bayes filter, made cheap

A full belief over every possible state is expensive. The Kalman filter makes three assumptions so the belief is always a Gaussian, described by just a mean $\mu$ and a covariance $\Sigma$:

- the motion model is linear: $x_t = A x_{t-1} + B u_t + \epsilon_t$, with process noise $\epsilon_t \sim \mathcal{N}(0, Q)$
- the measurement model is linear: $z_t = C x_t + \delta_t$, with sensor noise $\delta_t \sim \mathcal{N}(0, R)$
- the starting belief is Gaussian.

Under those assumptions a Gaussian stays Gaussian through both steps, and the filter is exact.

## Predict

Move the mean with the model, and grow the uncertainty by the process noise:

$$\bar\mu = A\mu + Bu, \qquad \bar\Sigma = A \Sigma A^\top + Q$$

## Update

Compare the measurement with what you expected to see, and correct by a fraction $K$ of the difference:

$$K = \bar\Sigma C^\top (C \bar\Sigma C^\top + R)^{-1}, \qquad \mu = \bar\mu + K(z - C\bar\mu), \qquad \Sigma = (I - KC)\bar\Sigma$$

The **Kalman gain** $K$ is the inverse-variance weighting from the measurement-noise lesson, in matrix form. A noisy sensor (large $R$) gives a small $K$: trust the model. A confident sensor gives a large $K$: follow the measurement.

## Worked example: one dimension

A robot holds still ($A = 1$, $B = 0$, $C = 1$). Its belief is $\mu = 0$, $\Sigma = 1$. The model allows a little drift, $Q = 0.01$, and the sensor has $R = 1$. It measures $z = 0.8$.

- Predict: $\bar\mu = 0$, $\bar\Sigma = 1 + 0.01 = 1.01$.
- Gain: $K = \dfrac{1.01}{1.01 + 1} \approx 0.50$.
- Update: $\mu = 0 + 0.50 \times 0.8 \approx 0.40$ and $\Sigma = (1 - 0.50) \times 1.01 \approx 0.50$.

Prediction and measurement were equally trusted, so the estimate lands halfway, and the uncertainty halves.

For moving robots the book uses a constant-velocity model, $x = (p, v)$ with $A = \begin{bmatrix} 1 & \Delta t \\ 0 & 1 \end{bmatrix}$ and $C = \begin{bmatrix} 1 & 0 \end{bmatrix}$: you measure only position, and the filter still estimates velocity.

> **Common mistake:** setting $Q$ to zero because "my model is right". Then $\bar\Sigma$ shrinks every step, $K$ goes to zero, and the filter stops listening to its sensors. A small $Q$ keeps it honest.
