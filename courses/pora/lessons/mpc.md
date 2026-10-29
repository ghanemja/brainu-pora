---

---
## Plan, take one step, plan again

**Model predictive control** (MPC) turns trajectory optimization into feedback. At every control step:

- Measure (or estimate) the current state $x(t)$.
- Solve an optimal control problem over a short horizon of $N$ steps, starting from $x(t)$.
- Apply only the first input $u_0$ of that plan, and throw the rest away.

At the next step the horizon slides forward by one and you solve again from a fresh measurement. That's why it's also called **receding horizon control**. Because each plan starts from what actually happened, disturbances and model errors get corrected.

## The problem solved at every step

For a linear model the inner problem is usually

$$\min_{u_0, \dots, u_{N-1}} \; \sum_{k=0}^{N-1} \left( x_k^\top Q x_k + u_k^\top R u_k \right) + x_N^\top P\, x_N$$

subject to $x_{k+1} = A x_k + B u_k$, $x_0 = x(t)$, $u_{\min} \le u_k \le u_{\max}$, and $x_k$ inside a safe set. With linear dynamics and constraints this is a **quadratic program**, which solvers handle in microseconds to milliseconds. With nonlinear dynamics it's a nonlinear program, often solved with a few SQP or iLQR iterations.

## Why constraints are the selling point

LQR and PID don't know actuators have limits. When their command saturates, the robot does something the controller never planned for. MPC builds the limits into the plan, so it can, for example, start braking early because it knows braking force is limited, or slow down before a corner because it knows lateral acceleration is. Speed limits, joint limits, keep-out zones and actuator rates all go in the same way.

## Worked example: a limit that binds, then doesn't

Take $x_{k+1} = x_k + u_k$, horizon $N = 3$, cost $\sum_{k=1}^{3} x_k^2 + \sum_{k=0}^{2} u_k^2$, and the limit $|u_k| \le 1$. Start at $x = 2.5$.

- Without the limit, the best first move would be $u_0 \approx -1.54$, which isn't allowed.
- With it, MPC plans $(-1, -0.9, -0.3)$ and applies $u_0 = -1$. The state becomes $1.5$.
- Re-solving from $1.5$, the limit no longer binds: the new plan is about $(-0.92, -0.35, -0.12)$.

Notice the second step is $-0.92$, not the $-0.9$ planned a moment ago. MPC never commits to its old plan.

## Horizon, stability and compute

A longer horizon sees trouble sooner but costs more to solve, and the solve must finish within one control period: a 20 Hz loop leaves 50 ms. The terminal cost $x_N^\top P x_N$ stands in for everything beyond the horizon; using the LQR cost-to-go $P$ is a common choice that helps make the closed loop stable.

> **Common mistake:** making the horizon too short. A car whose plan covers only 1 s can't see that it needs 2 s to stop, and by the time the obstacle enters the horizon, no feasible plan is left. The horizon must cover the slowest thing the robot needs to anticipate.
