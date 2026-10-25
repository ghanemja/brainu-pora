---
video: FW_ay7K4jPE | What Is Feedforward Control? | Control Systems in Practice | MATLAB | 15:44
---
## Why a plan isn't enough

Differential flatness gives you a planned path and the inputs that would follow it, if your model were perfect. Replay those inputs on a real robot and it drifts: wheel slip, a bump and a wrong mass all add up, and nothing pulls it back. **Trajectory tracking** closes the loop around the plan.

## Feedforward plus feedback

Every good tracking controller has two parts:

$$u = \underbrace{u_d(t)}_{\text{feedforward: what the plan needs}} + \underbrace{K\,(x_d(t) - x)}_{\text{feedback: correct the error}}$$

Feedforward does most of the work. Without it, the controller only acts when there's already error, so it always lags behind a moving target. Feedback handles everything the model got wrong.

## The book's tracker: PD in flat outputs

For the dynamically extended unicycle (state $(x, y, v, \theta)$, inputs $(a, \omega)$), flatness lets you write the position accelerations directly in terms of the inputs:

$$\begin{bmatrix} \ddot x \\ \ddot y \end{bmatrix} = \underbrace{\begin{bmatrix} \cos\theta & -v\sin\theta \\ \sin\theta & v\cos\theta \end{bmatrix}}_{J(\theta, v)} \begin{bmatrix} a \\ \omega \end{bmatrix}$$

So choose the accelerations you want, a "virtual input" $w$: the planned acceleration plus PD feedback on the position and velocity errors,

$$w_1 = \ddot x_d + k_p (x_d - x) + k_d (\dot x_d - \dot x), \qquad w_2 = \ddot y_d + k_p (y_d - y) + k_d (\dot y_d - \dot y)$$

and recover the real inputs with $(a, \omega) = J^{-1} w$. The tracking error then obeys $\ddot e + k_d\,\dot e + k_p\,e = 0$ in each direction, which decays to zero for any $k_p, k_d > 0$.

## Worked example

Pick $k_p = 4$ and $k_d = 4$. The error equation $\ddot e + 4\dot e + 4e = 0$ has a repeated root at $-2$, so it's critically damped: no overshoot, and the error goes as $(c_1 + c_2 t)\,e^{-2t}$. A 1 m error that starts at rest is down to about 9 cm after 2 s and under 2 cm after 3 s. For the inversion, $\det J = v\cos^2\theta + v\sin^2\theta = v$, so $J$ is invertible whenever the robot is moving.

> **Common mistake:** starting the tracker from rest. At $v = 0$, $\det J = 0$ and $J^{-1}$ doesn't exist. Start with a small nonzero speed, or switch to a different controller near stops.
