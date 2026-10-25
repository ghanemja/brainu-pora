---
video: HqNdBiej23I | Kinematic bicycle model | Prof. Georg Schildbach, University of Lübeck | 12:09
---
## Two levels of detail

A **kinematic model** treats velocities as the inputs. It captures the geometry of how a robot can move and ignores what it takes to get those velocities: mass, inertia and forces. A **dynamic model** treats forces or torques as the inputs, so velocities become part of the state and can't change instantly.

## The unicycle: the kinematic workhorse

A wheeled robot that drives forward at speed $v$ and turns at rate $\omega$, with pose $(x, y, \theta)$:

$$\dot x = v\cos\theta, \qquad \dot y = v\sin\theta, \qquad \dot\theta = \omega$$

Notice what's missing: there's no way to move sideways. The wheels roll but don't slide. That's the robot's geometry, and the kinematic model gets it exactly right with only three states.

## Adding dynamics

Real motors can't change speed instantly. The book's **dynamically extended unicycle** makes speed a state and acceleration the input:

$$\dot x = v\cos\theta, \quad \dot y = v\sin\theta, \quad \dot v = a, \quad \dot\theta = \omega$$

with state $(x, y, v, \theta)$ and inputs $(a, \omega)$. Going further, a full dynamic model adds mass, tire forces and motor torques.

## Which to use

Use the kinematic model when the robot is slow and its motors track the speeds you command well: indoor robots, warehouse carts, path planning. Use a dynamic model when forces matter: high speed, hard braking, tire slip, heavy loads. The trade-off is fidelity against simplicity, and choosing it is a design decision.

## Worked example

Drive the unicycle with constant $v = 1\ \text{m/s}$ and $\omega = 0.5\ \text{rad/s}$. The heading grows at a constant rate while the speed stays fixed, so the robot drives a circle of radius

$$r = \frac{v}{\omega} = \frac{1}{0.5} = 2\ \text{m}$$

and comes back around after $2\pi/\omega \approx 12.6$ s. In the dynamically extended model, you'd first have to accelerate from rest: with $a = 0.5\ \text{m/s}^2$, it takes 2 s to reach $v = 1$.

> **Common mistake:** trusting a kinematic plan at high speed. The kinematic model will happily command an instant change of speed that the real robot can't follow.
