---
video: qg4PchTECck | Gradient Descent in 3 minutes | Visually Explained | 3:07
video: uh1Dk68cfWs | The Karush–Kuhn–Tucker (KKT) Conditions and the Interior Point Method for Convex Optimization | Visually Explained | 21:58
---
## What an optimizer is looking for

An optimization problem asks for the $x$ that makes a cost $f(x)$ as small as possible. Without constraints, a smooth local minimum has two signatures:

- the gradient is zero, $\nabla f(x^*) = 0$, so no direction goes downhill to first order
- the Hessian $\nabla^2 f(x^*)$ is positive semidefinite, so the surface curves up, not down.

A zero gradient alone isn't enough: maxima and saddle points have it too. Trajectory optimization, calibration and SLAM all come down to this search, just with many more variables.

## Two ways to walk downhill

**Gradient descent** steps against the slope with a step size $\alpha$:

$$x_{k+1} = x_k - \alpha\, \nabla f(x_k)$$

It is cheap per step but slow in long, narrow valleys. **Newton's method** also uses curvature, jumping to the minimum of the local quadratic model:

$$x_{k+1} = x_k - \left[\nabla^2 f(x_k)\right]^{-1} \nabla f(x_k)$$

Near a minimum it converges much faster, but each step needs the Hessian and a linear solve, and far from a minimum it can head the wrong way. Practical solvers blend the two.

## Constraints and the KKT conditions

Most robot problems have constraints: minimize $f(x)$ subject to $h(x) = 0$ and $g(x) \le 0$. At a constrained optimum you can't go downhill without leaving the feasible set, so the cost gradient must be balanced by the constraint gradients:

$$\nabla f + \textstyle\sum_i \lambda_i \nabla h_i + \sum_j \mu_j \nabla g_j = 0$$

These are the **KKT conditions**, together with $\mu_j \ge 0$ and $\mu_j\, g_j(x) = 0$. The last one says an inequality only pushes back when it is active ($g_j = 0$). The weights $\lambda$ and $\mu$ are the **Lagrange multipliers**.

## Worked example: closest point on a line

Minimize $f = x^2 + y^2$ subject to $h = x + y - 1 = 0$. The gradients are $\nabla f = (2x, 2y)$ and $\nabla h = (1, 1)$, so KKT gives

$$2x + \lambda = 0, \qquad 2y + \lambda = 0, \qquad x + y = 1$$

The first two force $x = y$, the third gives $x = y = 0.5$, and then $\lambda = -1$. The cost is $0.5$. Geometrically, the circle $x^2 + y^2 = 0.5$ just touches the line there, so the two gradients are parallel.

## Convex problems are the easy ones

A problem is **convex** when the cost is convex and the feasible set is convex. Then every local minimum is a global minimum, and solvers come with guarantees. Least squares, LQR and many MPC problems are convex.

Most trajectory optimization isn't: nonlinear dynamics and obstacles bend the feasible set. Then the solver returns the local minimum nearest its starting guess, and two guesses can give two different answers.

> **Common mistake:** blaming the solver when a nonconvex problem gives different answers from different starts. That's expected. Give it a good initial guess, such as a straight-line path or the previous solution.
