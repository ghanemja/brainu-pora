---

---
## Discretize first, then optimize

A direct method turns the infinite-dimensional problem (a whole function $u(t)$) into a finite one. Split $[0, t_f]$ into $N$ steps of length $\Delta t$, and make the states and inputs at each step the unknowns:

$$z = (x_0, x_1, \dots, x_N,\; u_0, \dots, u_{N-1})$$

The integral cost becomes a sum, $J \approx h(x_N) + \sum_k g(x_k, u_k)\, \Delta t$. Now it is an ordinary **nonlinear program**, and a general solver (IPOPT, SNOPT, or an SQP method) can take it from there.

## The dynamics become equality constraints

The solver doesn't simulate. Instead, each step of the dynamics is a constraint that ties neighboring variables together. With Euler integration:

$$x_{k+1} = x_k + \Delta t\, f(x_k, u_k), \qquad k = 0, \dots, N-1$$

This is the **collocation** (or multiple shooting) view. Its big practical advantage: the initial guess doesn't have to obey the dynamics. You can start from a straight line that cuts through obstacles, with zero inputs, and the solver repairs the violated constraints while it lowers the cost. **Single shooting**, which keeps only the inputs as unknowns and simulates, is smaller but much more sensitive to the guess.

## Constraints go straight in

Anything you can write as an equation or inequality on $z$ becomes part of the problem:

- input limits, $-u_{\max} \le u_k \le u_{\max}$
- obstacles, $\|p_k - c\| \ge r$ for a round obstacle at $c$ with radius $r$
- start and goal, $x_0 = x_{\text{start}}$, $x_N = x_{\text{goal}}$.

This ease with constraints is the main reason direct methods dominate practical trajectory optimization. Indirect methods need the constraint structure worked out by hand.

## Worked example: counting the unknowns

Take the cart $\ddot q = u$ with state $(q, v)$, from rest at $0$ to rest at $1$.

With $N = 2$ and $\Delta t = 0.5$: there are $3 \times 2 = 6$ state variables and $2$ inputs, so $8$ unknowns. Constraints: $2$ (start) $+ 4$ (dynamics) $+ 2$ (goal), also $8$. So the answer is forced: Euler gives $q_2 = 0.25\,u_0 = 1$ and $v_2 = 0.5(u_0 + u_1) = 0$, so $u_0 = 4$, $u_1 = -4$. Nothing is left to optimize.

With $N = 10$: $22 + 10 = 32$ unknowns and $2 + 20 + 2 = 24$ constraints, leaving $8$ degrees of freedom for the cost to choose.

## Why the solver stays fast

The problem looks big, but each dynamics constraint touches only $x_k$, $u_k$ and $x_{k+1}$. The constraint Jacobian is therefore mostly zeros, in a banded pattern, and solvers exploit that sparsity. Problems with thousands of variables solve in milliseconds to seconds.

> **Common mistake:** trusting a plan built on a coarse grid. The solver satisfies the discretized dynamics exactly, so it happily exploits Euler's errors. Simulate the inputs with a fine, accurate integrator before you run them on a robot.
