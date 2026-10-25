---
video: TLe4otkRAts | Localization - 5 Minutes with Cyrill | Cyrill Stachniss | 4:35
video: PiCC-SxWlH8 | EKF Localization | Cyrill Stachniss | 36:21
---
## The goal

You know the map: a list of landmarks $m_1, \ldots, m_N$ at known positions. You don't know the robot's pose $x = (x, y, \theta)$. **EKF localization** tracks the pose as a Gaussian $\mathcal{N}(\mu, \Sigma)$ with the EKF from two lessons ago, using the motion and range-bearing models from the last lesson.

## The loop (the book's Algorithm 2)

**Predict** with the motion model and its Jacobian $F$:

$$\bar\mu = f(\mu, u), \qquad \bar\Sigma = F \Sigma F^\top + Q$$

**Correct** once for each landmark $j$ you saw:

$$S = H \bar\Sigma H^\top + R, \qquad K = \bar\Sigma H^\top S^{-1}, \qquad \bar\mu \leftarrow \bar\mu + K\,(z - h(\bar\mu, m_j)), \qquad \bar\Sigma \leftarrow (I - KH)\bar\Sigma$$

where $H$ is the Jacobian of the range-bearing model at the predicted pose. Because the measurements are independent given the pose, doing them one after another gives the same answer as all at once.

## The Jacobian you'll actually compute

With $\Delta x = m_{j,x} - \bar x$, $\Delta y = m_{j,y} - \bar y$ and $q = \Delta x^2 + \Delta y^2$:

$$H = \begin{bmatrix} -\dfrac{\Delta x}{\sqrt q} & -\dfrac{\Delta y}{\sqrt q} & 0 \\[2mm] \dfrac{\Delta y}{q} & -\dfrac{\Delta x}{q} & -1 \end{bmatrix}$$

The first row says moving toward the landmark shortens the range; the last entry says turning left by some angle decreases the bearing by the same angle.

## Worked example

Predicted pose $(1, 1, 0)$, landmark at $(4, 5)$: $\Delta x = 3$, $\Delta y = 4$, $q = 25$, so

$$H = \begin{bmatrix} -0.6 & -0.8 & 0 \\ 0.16 & -0.12 & -1 \end{bmatrix}$$

Now the sensor reads a bearing of $179^\circ$ when the filter expected $-179^\circ$. The raw innovation is $358^\circ$; wrapped into $(-\pi, \pi]$ it's $-2^\circ$, a tiny correction instead of a wild one.

## What it needs

EKF localization assumes **data association**: you know which landmark each measurement came from. The book's version for unknown associations picks, for each measurement, the landmark that makes it most likely under the predicted belief. It also needs a decent starting guess; if you don't know where you are at all, use Monte Carlo localization.

> **Common mistake:** skipping the angle wrap. Without it, one reading near $\pm 180^\circ$ yanks the pose estimate far off, and the filter may never recover.
