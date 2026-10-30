---

---
## Geometric paths can be impossible to drive

A geometric planner returns a collision-free curve, but says nothing about whether the robot can follow it. A car can't step sideways or turn on the spot. A path with a sharp corner forces a full stop. A quadrotor at speed can't change direction instantly.

**Kinodynamic planning** respects the dynamics while planning, so every path it returns is one the robot can actually execute. "Kino" refers to velocity-level limits, "dynamic" to forces and accelerations.

## Plan in state space, extend by simulating

The planner searches over the full state $x$, usually position plus velocity, not just over configurations. Edges aren't straight lines. Instead, a tree is extended by picking a control $u$ and a duration, then integrating

$$\dot x = f(x, u)$$

forward from an existing node. Because every edge is a simulated trajectory, it is dynamically feasible by construction. Collision checks run along the simulated trajectory, and velocity or acceleration limits become limits on $x$ and $u$.

## The steering problem

RRT and PRM need to connect two specific configurations. With dynamics, that means finding inputs that take state $x_a$ exactly to state $x_b$: a **two-point boundary value problem**, which is as hard as an optimal control problem. Practical workarounds:

- **Forward propagation**: try a few random controls from $q_{\text{near}}$ and keep the one that ends closest to the sample.
- **Motion primitives**: a fixed library of short feasible maneuvers, chained together on a **state lattice**.
- **Local trajectory optimization** to connect nearby states when exact connection matters.

## Worked example: three motion primitives

A unicycle obeys $\dot x = v\cos\theta$, $\dot y = v\sin\theta$, $\dot\theta = \omega$. Use $v = 1$ m/s for $T = 1$ s, with $\omega \in \{-0.5, 0, 0.5\}$ rad/s, starting from $(0, 0, 0)$.

- Straight: end at $(1, 0, 0)$.
- Left: a circle of radius $v/\omega = 2$ m, so $x = 2\sin 0.5 \approx 0.96$, $y = 2(1 - \cos 0.5) \approx 0.25$, $\theta = 0.5$.
- Right: the mirror image, $(0.96, -0.25, -0.5)$.

Chaining these from each endpoint builds a tree in which every branch is drivable.

## The price of dynamics

The state space is typically twice the dimension of C-space, since every position comes with a velocity, so the search is much bigger. Nearest-neighbor queries also get harder, because distance in state space no longer reflects how easy it is to get somewhere.

> **Common mistake:** using plain Euclidean distance to pick the nearest node. A car pose 0.5 m directly to its side looks close but needs a long maneuver to reach. Weight heading and velocity in the metric, or use an estimated time-to-reach.
