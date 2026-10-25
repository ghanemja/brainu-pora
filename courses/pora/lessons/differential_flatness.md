---
video: tRrQPqJX_Uw | Differential Flatness | Control Systems and Robotics | 16:02
---
## The problem it solves

Planning a trajectory usually means finding inputs $u(t)$ so that integrating $\dot x = f(x, u)$ lands where you want, and that's hard. For some systems there's a shortcut: pick a few outputs, plan *those* freely, and every state and input follows by algebra, with no integration at all.

## The definition

A system is **differentially flat** if there are outputs $z$ (the **flat outputs**, as many as there are inputs) such that every state and every input can be written as a function of $z$ and a finite number of its derivatives:

$$x = \beta(z, \dot z, \ldots, z^{(q)}), \qquad u = \gamma(z, \dot z, \ldots, z^{(q)})$$

Cars, unicycles and quadrotors are all flat, which is why this idea is used so much in robotics.

## The unicycle is flat in $(x, y)$

For the unicycle, the position $(x, y)$ is a flat output. If you know the path $x(t), y(t)$ and its derivatives, the heading is the direction of motion, the speed is how fast you move along it, and the turn rate is how fast the heading changes:

$$\theta = \operatorname{atan2}(\dot y, \dot x), \qquad v = \sqrt{\dot x^2 + \dot y^2}, \qquad \omega = \frac{\dot x\,\ddot y - \dot y\,\ddot x}{\dot x^2 + \dot y^2}$$

So planning reduces to drawing a smooth curve in the plane, for example a polynomial in $t$ whose coefficients you pick to match the start and end positions and velocities.

## Worked example

Plan $x(t) = t$, $y(t) = t^2$ for $t \in [0, 1]$. Then $\dot x = 1$, $\dot y = 2t$, $\ddot x = 0$, $\ddot y = 2$, so

$$v(t) = \sqrt{1 + 4t^2}, \qquad \theta(t) = \operatorname{atan2}(2t, 1), \qquad \omega(t) = \frac{2}{1 + 4t^2}$$

At the start, $v = 1$, $\theta = 0$ and $\omega = 2$. At the end, $v = \sqrt 5 \approx 2.24$ and the robot is turning more gently, $\omega = 0.4$. Those $v(t)$ and $\omega(t)$ are the open-loop inputs that drive the robot along the parabola.

> **Common mistake:** planning a curve where the robot stops. At $v = 0$ the heading formula is undefined (the denominator $\dot x^2 + \dot y^2$ is zero), so keep the planned speed above zero, or treat stops as special cases.
