---
video: hpeKrMG-WP0 | Introduction to State-Space Equations | MATLAB | 14:12
---
## What "state" means

The **state** $x$ is the smallest set of numbers that, together with the inputs you'll apply from now on, fixes everything that happens next. If two identical robots have the same state and get the same inputs, they do exactly the same thing. A **state-space model** writes the rule for how state changes:

$$\dot x = f(x, u), \qquad y = h(x)$$

Here $u$ is the input you control (forces, wheel speeds) and $y$ is what your sensors measure. The output and the state are often different: you might measure only position while the state also includes velocity.

## Finding the state of a mechanical system

Newton's law gives second derivatives, so position alone is never enough. For a cart of mass $m$ pushed by force $u$, $m\,\ddot q = u$. Knowing where the cart is doesn't tell you where it will be: you also need how fast it's moving. So the state is $x = (q, \dot q)$, and

$$\dot x = \begin{bmatrix} \dot q \\ u/m \end{bmatrix}$$

## The linear special case

When $f$ is linear, the model becomes matrices:

$$\dot x = A x + B u, \qquad y = C x$$

For the cart: $A = \begin{bmatrix} 0 & 1 \\ 0 & 0 \end{bmatrix}$, $B = \begin{bmatrix} 0 \\ 1/m \end{bmatrix}$, and $C = \begin{bmatrix} 1 & 0 \end{bmatrix}$ if you measure position. Linear models matter because questions like "is it stable?", "can I steer it anywhere?" and "can I estimate the state from $y$?" become linear-algebra tests on $A$, $B$ and $C$.

## In discrete time

Computers act in steps, so you'll also see $x_{k+1} = f(x_k, u_k)$. With Euler steps of length $h$, the cart becomes $q_{k+1} = q_k + h\,\dot q_k$ and $\dot q_{k+1} = \dot q_k + h\,u_k/m$.

## Worked example

A pendulum of length $l$ and mass $m$ with torque $u$ obeys $m l^2\, \ddot\theta = -m g l \sin\theta + u$. Take $x = (\theta, \dot\theta)$:

$$\dot x = \begin{bmatrix} \dot\theta \\ -\dfrac{g}{l}\sin\theta + \dfrac{u}{m l^2} \end{bmatrix}$$

That's nonlinear because of $\sin\theta$. The linearization lesson shows how to approximate it with $A$ and $B$ near a point.

> **Common mistake:** putting the input in the state. Force $u$ is something you choose at each moment, so it's not part of $x$.
