---

---
## The problem LQR solves

**LQR** (linear quadratic regulator) is optimal control for the one case with a clean answer: linear dynamics and a quadratic cost.

$$x_{k+1} = A x_k + B u_k, \qquad J = \sum_{k} \left( x_k^\top Q\, x_k + u_k^\top R\, u_k \right)$$

$Q \succeq 0$ says how much you dislike being away from zero (the setpoint), and $R \succ 0$ how much you dislike using effort. For a robot, $x$ is usually the error from a setpoint, and $A$, $B$ come from linearizing the dynamics there.

## The answer is a gain matrix

The optimal input is plain linear state feedback, $u_k = -K_k x_k$. The gains come from the **Riccati recursion**, run backward from the end of the horizon with $P_N = Q_f$:

$$K_k = (R + B^\top P_{k+1} B)^{-1} B^\top P_{k+1} A, \qquad P_k = Q + A^\top P_{k+1} (A - B K_k)$$

$x^\top P_k x$ is the optimal cost-to-go from state $x$ at step $k$. Run the recursion long enough and $P_k$ stops changing. That fixed point solves the **algebraic Riccati equation**, and gives one constant $K$: the infinite-horizon LQR you'll use most often.

## Worked example: a scalar system

Take $x_{k+1} = x_k + u_k$ with $Q = 1$, $R = 1$. The steady-state Riccati equation is

$$P = 1 + P - \frac{P^2}{1 + P} \quad\Longrightarrow\quad P^2 = 1 + P$$

so $P = (1 + \sqrt5)/2 \approx 1.618$ and $K = P/(1 + P) \approx 0.618$. The closed loop is $x_{k+1} = (1 - 0.618)\, x_k = 0.382\, x_k$: the error shrinks by 62% per step.

Raise effort cost to $R = 10$: now $P^2 - P - 10 = 0$, so $P \approx 3.70$, $K = P/(10 + P) \approx 0.27$, and the error shrinks only 27% per step. Gentler control, slower convergence.

## Tuning with Q and R

Only the ratio of $Q$ to $R$ matters. Larger $Q$ entries push their states to zero faster; larger $R$ entries make the matching inputs smaller and smoother. A practical start is **Bryson's rule**: make each weight one over the square of the largest acceptable value, so $Q_{ii} = 1/x_{i,\max}^2$ and $R_{jj} = 1/u_{j,\max}^2$.

LQR needs the full state. If you only measure part of it, pair it with a Kalman filter; that combination is called LQG.

> **Common mistake:** using an LQR gain far from where you linearized. $K$ is optimal for the linear model, and the linear model is only good near its operating point. A pendulum balancer designed at upright fails at 60 degrees.

## In continuous time

The same story holds for $\dot x = Ax + Bu$ with cost $\int (x^\top Q x + u^\top R u)\, dt$. The gain is $K = R^{-1} B^\top P$, where $P$ solves

$$A^\top P + P A - P B R^{-1} B^\top P + Q = 0$$

The continuous and discrete gains are not interchangeable: design in the same time base your controller runs in. Libraries solve both versions in one call (for example, `scipy.linalg.solve_continuous_are` and `solve_discrete_are`).
