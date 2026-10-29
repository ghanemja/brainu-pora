---
video: 26sP4QIXgVA | L3.1 - Introduction to optimal control: motivation, optimal costs, optimization variables | aa4cc | 8:54
---
## The problem in one line

Optimal control picks the input signal $u(t)$ that makes a cost as small as possible while obeying the dynamics:

$$\min_{u(\cdot)}\; J = h\big(x(t_f)\big) + \int_0^{t_f} g\big(x(t), u(t)\big)\, dt$$

subject to $\dot x = f(x, u)$, a known start $x(0) = x_0$, and limits on states and inputs. Here $h$ is a terminal cost (how far from the goal you end up) and $g$ is a running cost (effort, time, discomfort). The answer is a whole trajectory, not a single number.

## The cost is where you make design choices

The "optimal" trajectory is only optimal for the cost you wrote. Some common terms:

- $g = 1$ gives minimum time.
- $g = u^\top R\, u$ penalizes effort, giving smoother, gentler motion.
- $h = (x - x_g)^\top Q_f (x - x_g)$ pulls the final state toward a goal $x_g$.

Changing the weights changes the answer. A large $R$ gives a slow, efficient move; a small $R$ gives a fast, aggressive one. Choosing weights is engineering judgment, not something the math decides for you.

## Worked example: moving a cart in one second

A cart with $\ddot q = u$ starts at rest at $q = 0$ and must stop at rest at $q = 1$ at $t_f = 1$ s, minimizing effort $\int_0^1 u^2\, dt$. The optimal input turns out to be a straight line in time:

$$u(t) = 6 - 12t, \qquad q(t) = 3t^2 - 2t^3$$

Check: $q(1) = 3 - 2 = 1$, $\dot q = 6t - 6t^2$ is zero at both ends, and $\ddot q = 6 - 12t = u$. The cart pushes hard at first, coasts through the middle, and brakes at the end. The total cost is $\int_0^1 (6 - 12t)^2\, dt = 12$.

## An open-loop plan only fits the model you assumed

The solution is a schedule of inputs, computed once from $x_0$. If the real cart is heavier than modeled, or someone bumps it, the schedule keeps playing anyway and the cart misses the goal.

So in practice an optimal trajectory is paired with feedback: a tracking controller (PID, LQR) that corrects deviations from the plan, or model predictive control, which re-solves the problem from the measured state every few milliseconds.

> **Common mistake:** expecting an optimal open-loop trajectory to be robust. It is the best plan for a perfect model, and often the most fragile, because it uses every margin the model allows.

## Two ways to solve it

- **Indirect methods** first derive optimality conditions (Pontryagin's principle), then solve those equations numerically.
- **Direct methods** first chop the trajectory into time steps, then hand the resulting finite problem to a numerical optimizer.

Indirect methods can be very accurate; direct methods handle constraints easily and are what most robotics software uses. The next two lessons cover each.
