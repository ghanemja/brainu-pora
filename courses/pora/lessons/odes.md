---
video: p_di4Zn4wz4 | Differential equations, a tourist's guide | 3Blue1Brown | 27:16
---
## What an ODE says

A derivative is a rate of change: $\dot x = \frac{dx}{dt}$ is how fast $x$ moves right now. An **ordinary differential equation** says how that rate depends on where you are and what you do:

$$\dot x = f(x, u)$$

Every model in this course has this shape. A robot rolling forward, a drone climbing, a car turning: each is a rule for the rate of change of its state $x$ given its input $u$.

## Solving one means rolling time forward

The ODE doesn't hand you $x(t)$ directly. You get it by adding up all the small changes, which is integration. A few simple ODEs have exact answers. The most important one:

$$\dot x = -a\,x \quad\Longrightarrow\quad x(t) = x_0\, e^{-a t}$$

For $a > 0$ it decays to zero, faster for bigger $a$. For $a < 0$ it grows without bound. You'll see this decay shape again every time a controller pulls an error to zero.

## When there's no formula: step it

Most robot models have no closed-form solution, so we step them on a computer. The simplest method, **forward Euler**, assumes the rate stays fixed for a short time $h$:

$$x_{k+1} = x_k + h\, f(x_k, u_k)$$

Smaller $h$ is more accurate but takes more steps. Better methods (Runge-Kutta) take a few looks at $f$ inside each step.

## Higher derivatives become more state

Newton's law for a cart, $m\,\ddot q = u$, has a second derivative. Stack position and velocity into one vector, $x = (q, \dot q)$, and it becomes first-order: $\dot x = (\dot q,\ u/m)$. This trick is how every mechanical system gets into the form $\dot x = f(x, u)$, and it's the subject of the state-space lesson.

## Worked example

Step $\dot x = -2x$ from $x_0 = 1$ with Euler, $h = 0.1$: each step multiplies by $1 + h(-2) = 0.8$, so $x_1 = 0.8$ and $x_2 = 0.64$. The exact answer is $e^{-0.4} \approx 0.670$ at $t = 0.2$, so Euler is a little low after two steps. Halve $h$ to $0.05$ and the four-step answer, $0.9^4 \approx 0.656$, is closer.

> **Common mistake:** picking $h$ too big. Here, $h = 1.5$ gives a multiplier of $1 - 3 = -2$, so the simulation flips sign and explodes even though the true system decays.
