---

---
## Optimality conditions first, numbers second

An indirect method doesn't search over trajectories directly. It first asks what any optimal trajectory must satisfy, then solves those conditions. The tool is **Pontryagin's principle**. Attach a **costate** $p(t)$, one entry per state, and form the **Hamiltonian**:

$$H(x, u, p) = g(x, u) + p^\top f(x, u)$$

The costate plays the role a Lagrange multiplier plays in ordinary optimization: it measures how much the cost would change if the state at time $t$ were nudged.

## The necessary conditions

Along an optimal trajectory:

$$\dot x = \frac{\partial H}{\partial p} = f(x, u), \qquad \dot p = -\frac{\partial H}{\partial x}, \qquad u^* = \arg\min_u H$$

When $u$ is unconstrained, the last condition becomes $\partial H / \partial u = 0$. Add the boundary conditions: $x(0) = x_0$ is fixed, and at the end either $x(t_f)$ is given, or it is free and $p(t_f) = \partial h / \partial x$ at $x(t_f)$.

## Worked example: the cart again

Take $\ddot q = u$ with state $(q, v)$, cost $\int_0^1 \tfrac12 u^2\, dt$, from rest at $0$ to rest at $1$. Then

$$H = \tfrac12 u^2 + p_1 v + p_2 u$$

- $\partial H/\partial u = u + p_2 = 0$, so $u = -p_2$.
- $\dot p_1 = -\partial H/\partial q = 0$, so $p_1 = c_1$ is constant.
- $\dot p_2 = -\partial H/\partial v = -p_1$, so $p_2 = c_2 - c_1 t$.

So the optimal input is linear in time, $u = c_1 t - c_2$. The four boundary conditions fix the two constants: $c_1 = -12$, $c_2 = -6$, giving $u = 6 - 12t$.

## A two-point boundary value problem

The example could be solved by hand; most can't. The trouble is that the conditions are split: $x$ is known at $t = 0$, but $p$ is only pinned down at $t_f$. You can't just integrate forward.

**Shooting** guesses the missing $p(0)$, integrates $x$ and $p$ forward together, measures how badly the end conditions are missed, and corrects the guess with a root finder. Because the costate equations are often unstable forward in time, small errors in the guess can blow up.

## Accurate, but touchy

When indirect methods converge they are very accurate, since they solve exact optimality conditions. The price:

- They need a good initial guess for the costate, which has no obvious physical meaning.
- Inequality constraints (torque limits, obstacles) split the trajectory into arcs where different conditions apply, and you must know the arc structure in advance.

That is why robotics software mostly uses direct methods, and keeps indirect ones for problems with clean structure, such as orbit transfers.

> **Common mistake:** treating any solution of these conditions as the optimum. Pontryagin's conditions are necessary, not sufficient: a trajectory can satisfy them and still be a local optimum, or not a minimum at all.
