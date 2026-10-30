---
video: PHC2dm4E_VQ | CS 285: Lecture 10, Part 4 | RAIL | 13:23
---
## LQR for nonlinear systems, one linearization at a time

LQR needs linear dynamics and a quadratic cost. **iLQR** (iterative LQR) handles nonlinear $x_{k+1} = f(x_k, u_k)$ by repeating three steps:

- **Roll out** the current inputs $\bar u_k$ through the real dynamics to get a nominal trajectory $\bar x_k$.
- **Approximate** around it: linearize the dynamics and take a second-order expansion of the cost at every step.
- **Solve** that time-varying LQR problem for a correction, apply it, and repeat until the cost stops improving.

Each pass is cheap, and the approximation gets better as the trajectory settles.

## The local model

For small deviations $\delta x_k = x_k - \bar x_k$ and $\delta u_k = u_k - \bar u_k$, the dynamics become

$$\delta x_{k+1} \approx A_k\, \delta x_k + B_k\, \delta u_k, \qquad A_k = \frac{\partial f}{\partial x}\Big|_{\bar x_k, \bar u_k},\quad B_k = \frac{\partial f}{\partial u}\Big|_{\bar x_k, \bar u_k}$$

The cost gets the same treatment: gradients and Hessians of the step cost at each $(\bar x_k, \bar u_k)$. Unlike plain LQR, the model now includes linear terms, because the nominal trajectory isn't at the cost's minimum.

## Backward pass, then forward pass

The **backward pass** runs a Riccati-like recursion from the last step to the first. At each step it produces a feedforward correction $k_k$ and a feedback gain $K_k$.

The **forward pass** simulates the true nonlinear dynamics with

$$u_k = \bar u_k + \alpha\, k_k + K_k (x_k - \bar x_k)$$

starting with $\alpha = 1$. If the new cost isn't lower, halve $\alpha$ and try again: a line search. The feedback term matters even during optimization, because it keeps the new rollout close to where the linear model is valid.

## Worked example: one step

Take $x_{k+1} = x_k + 0.1 \sin x_k + u_k$ with $x_0 = 1$, cost $\tfrac12 u_0^2 + 5 x_1^2$, and initial guess $\bar u_0 = 0$.

- Rollout: $\bar x_1 = 1 + 0.1 \sin 1 \approx 1.084$, cost $5 \times 1.084^2 \approx 5.88$.
- Backward pass: the terminal cost has slope $10\,\bar x_1 \approx 10.84$ and curvature $10$; with $B_0 = 1$, the correction is $k_0 = -10.84/(1 + 10) \approx -0.986$.
- Forward pass: $u_0 = -0.986$ gives $x_1 \approx 0.099$ and cost $\approx 0.53$.

With one step and fixed $x_0$, the dynamics are linear in $u$, so one iteration is exact. Over longer horizons the $\sin x$ term makes it take several.

## iLQR versus DDP

**DDP** (differential dynamic programming) is the older, fuller version. It keeps second derivatives of the dynamics in the backward pass; iLQR drops them. iLQR iterations are cheaper and in practice converge almost as fast, so it's the usual choice. Both return a locally optimal trajectory plus the gains $K_k$, which you can keep as a tracking controller around it.

> **Common mistake:** running iLQR without regularization. If the quadratic model isn't positive definite in $u$, the backward pass divides by a non-positive number and the step goes wild. Add $\mu I$ to that term, raising $\mu$ when a step fails and lowering it when steps succeed.
