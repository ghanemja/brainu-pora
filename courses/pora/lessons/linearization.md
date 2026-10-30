---
video: 5gEattuH3tI | What Is Linearization? | MATLAB | 14:01
---
## The idea

Linear models have clean tools (eigenvalues, LQR, the Kalman filter); robots are nonlinear. **Linearization** replaces a nonlinear model with a linear one that's accurate near a chosen operating point, using the first-order Taylor expansion.

## The recipe

Pick an equilibrium $(\bar x, \bar u)$ with $f(\bar x, \bar u) = 0$, or a whole nominal trajectory $(\bar x(t), \bar u(t))$ that obeys the dynamics, $\dot{\bar x} = f(\bar x, \bar u)$. Write the true state as nominal plus a small deviation, $x = \bar x + \delta x$ and $u = \bar u + \delta u$. Expanding $f$ to first order gives deviation dynamics:

$$\dot{\delta x} \approx A\,\delta x + B\,\delta u, \qquad A = \frac{\partial f}{\partial x}\bigg|_{\bar x, \bar u}, \quad B = \frac{\partial f}{\partial u}\bigg|_{\bar x, \bar u}$$

$A$ and $B$ are Jacobians: matrices of partial derivatives. Along a trajectory they change with time, $A(t)$ and $B(t)$, but the model for the deviations is still linear.

## Worked example: the unicycle driving straight

The unicycle with state $(x, y, \theta)$ and inputs $(v, \omega)$ has $f = (v\cos\theta,\ v\sin\theta,\ \omega)$. The Jacobians are

$$A = \begin{bmatrix} 0 & 0 & -v\sin\theta \\ 0 & 0 & v\cos\theta \\ 0 & 0 & 0 \end{bmatrix}, \qquad B = \begin{bmatrix} \cos\theta & 0 \\ \sin\theta & 0 \\ 0 & 1 \end{bmatrix}$$

Linearize about the nominal trajectory of driving straight along $x$ at $\bar v = 1$, $\bar\theta = 0$:

$$A = \begin{bmatrix} 0 & 0 & 0 \\ 0 & 0 & 1 \\ 0 & 0 & 0 \end{bmatrix}, \qquad B = \begin{bmatrix} 1 & 0 \\ 0 & 0 \\ 0 & 1 \end{bmatrix}$$

Read off the physics: $\dot{\delta y} = \delta\theta$, so a small heading error makes the robot drift sideways at a rate equal to that error. And $\delta\omega$ steers $\delta\theta$. That's exactly the structure a lateral controller needs to correct drift.

> **Common mistake:** trusting the linear model far from the operating point. At a heading error of $0.1$ rad, $\sin(0.1) \approx 0.0998$, which is fine. At $1$ rad, $\sin(1) \approx 0.84$, which is badly off. Re-linearize along the trajectory.
