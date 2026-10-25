---
video: wkfEZmsQqiA | What Is PID Control? | Understanding PID Control, Part 1 | MATLAB | 11:42
---
## Feedback in one line

Measure the error between where you want to be and where you are, $e(t) = r(t) - y(t)$, and push in proportion to it. A **PID controller** adds two more terms:

$$u(t) = K_p\, e(t) + K_i \int_0^t e(\tau)\, d\tau + K_d\, \dot e(t)$$

## What each term does

- **Proportional** ($K_p$) reacts to the error now. Bigger $K_p$ is faster but overshoots more.
- **Integral** ($K_i$) adds up past error. It keeps pushing until the error is exactly zero, which is the only way to cancel a constant disturbance such as gravity, friction or a slope.
- **Derivative** ($K_d$) reacts to how fast the error changes. It acts like damping and stops overshoot, but it amplifies sensor noise, so it's usually filtered.

## Why the integral term is needed

Take a cart $m\,\ddot q = u + d$ with a constant push $d$ (a slope, say) and PD control. When everything settles, $\dot q = \ddot q = 0$, so $K_p e + d = 0$: the cart sits at a steady error $e = -d/K_p$. Raising $K_p$ shrinks the offset but never removes it. Add $K_i$ and the integral keeps growing until it supplies $-d$ by itself, at zero error.

## Worked example: tuning by matching a second-order system

With PD on the cart and no disturbance, the closed loop is

$$\ddot q + \frac{K_d}{m}\,\dot q + \frac{K_p}{m}\,q = \frac{K_p}{m}\,r$$

That's a standard second-order system with natural frequency $\omega_n = \sqrt{K_p/m}$ and damping ratio $\zeta = \frac{K_d}{2\sqrt{m K_p}}$. For $m = 1$ kg, if you want $\omega_n = 2$ rad/s with no overshoot ($\zeta = 1$): $K_p = m\,\omega_n^2 = 4$ and $K_d = 2\zeta\sqrt{m K_p} = 4$.

> **Common mistake:** integral windup. If the motor saturates, the integral keeps growing during the saturation and then overshoots badly. Real controllers clamp the integral (anti-windup).
