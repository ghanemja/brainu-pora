---
video: dShtlMl69kY | Why Runge-Kutta is SO Much Better Than Euler's Method #somepi | Phanimations | 13:32
video: MstPeOTCVzQ | Deriving Forward Euler and Backward/Implicit Euler Integration Schemes for Differential Equations | Steve Brunton | 23:28
---
## Stepping a model forward in time

A state-space model $\dot x = f(x, u)$ says how fast the state is changing, not where it will be. To simulate, predict, or plan, you **integrate** it: step forward in small time increments $h$. The simplest scheme, **forward Euler**, assumes the rate stays constant over each step:

$$x_{k+1} = x_k + h\, f(x_k, u_k)$$

It's what you'd do by hand, and it's often good enough. But it makes an error every step, and those errors build up.

## Accuracy: Euler versus Runge–Kutta

Euler's global error is proportional to $h$: halve the step and the error halves. **Runge–Kutta 4** (RK4) samples the slope four times per step and combines them:

$$x_{k+1} = x_k + \frac{h}{6}\,(k_1 + 2k_2 + 2k_3 + k_4)$$

with $k_1 = f(x_k)$, $k_2 = f(x_k + \tfrac h2 k_1)$, $k_3 = f(x_k + \tfrac h2 k_2)$ and $k_4 = f(x_k + h k_3)$. Its error is proportional to $h^4$: halve the step and the error drops 16-fold. Four slope evaluations per step is usually a bargain.

## Worked example: one step of decay

Take $\dot x = -x$ with $x(0) = 1$ and one step of $h = 0.5$. The exact answer is $e^{-0.5} \approx 0.6065$.

- **Euler**: $x_1 = 1 + 0.5 \times (-1) = 0.5$, off by about $0.107$.
- **RK4**: $k_1 = -1$, $k_2 = -(1 - 0.25) = -0.75$, $k_3 = -(1 - 0.1875) = -0.8125$, $k_4 = -(1 - 0.40625) = -0.59375$. Then $x_1 = 1 + \frac{0.5}{6}(-4.71875) \approx 0.6068$, off by about $0.0002$.

Same step size, about 400 times more accurate.

## Stability: when the simulation blows up

Accuracy isn't the only issue. On $\dot x = -a x$, Euler gives $x_{k+1} = (1 - h a)\, x_k$, which only decays if $|1 - h a| < 1$, that is, if $h < 2/a$. Fast dynamics need tiny steps: with $a = 100$, a step of $h = 0.03$ multiplies $x$ by $-2$ each step, and a decaying system appears to explode.

On an undamped oscillator, Euler grows the amplitude by $\sqrt{1 + h^2 \omega^2}$ every step, adding energy that isn't there. **Semi-implicit** (symplectic) Euler and **implicit** methods avoid this, at extra cost per step.

## Choosing a step in practice

Set $h$ well below the fastest time scale in the system: a stiff contact or a fast motor needs a much smaller step than a slowly turning car. Library solvers such as `scipy.integrate.solve_ivp` adapt $h$ automatically to meet an error tolerance. When simulating a digital controller, keep the controller's own update period separate from the integration step: the controller may act at 100 Hz while the physics is integrated at 1000 Hz.

> **Common mistake:** trusting a simulation without checking the step. Run it again with $h$ halved. If the results change noticeably, the first run was measuring the integrator, not the robot.
