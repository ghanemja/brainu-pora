---
video: PAvj6cP6lOM | Holonomic vs. Nonholonomic Constraints for Robots | Mecharithm - Robotics and Mechatronics | 12:48
video: XG4cODYVbJk | Modeling of a differential drive robot | Duckietown | 7:03
---
## Wheels that can't slide

A car or a wheeled robot can drive forward and turn, but it can't slide straight sideways: the wheels grip the floor. That's a limit on how the robot can *move right now*, a constraint on its velocity. For the unicycle with pose $(x, y, \theta)$, "no sideways motion" says the velocity has no component perpendicular to the heading:

$$\dot x \sin\theta - \dot y \cos\theta = 0$$

## Why it's called nonholonomic

Some constraints limit where you can *be*: a bead on a wire can never leave the wire. Those are **holonomic**. The no-slip rule is different. It limits velocity, but it can't be rewritten as a rule about position, so every pose is still reachable. That's what **nonholonomic** means. You've done this every time you parallel park: you can't slide into the space, but a sequence of allowed motions (back, turn, forward) gets the car there.

## The unicycle and the differential drive

The kinematic model that respects the constraint is the unicycle from lesson 2:

$$\dot x = v\cos\theta, \qquad \dot y = v\sin\theta, \qquad \dot\theta = \omega$$

Most indoor robots are **differential drive**: two wheels of radius $r$ on an axle of length $L$, each with its own motor. Their wheel speeds $\omega_R$ and $\omega_L$ map onto the unicycle's inputs:

$$v = \frac{r(\omega_R + \omega_L)}{2}, \qquad \omega = \frac{r(\omega_R - \omega_L)}{L}$$

Equal wheel speeds drive straight; opposite speeds spin in place.

## Worked example

A robot with $r = 0.05$ m and $L = 0.3$ m spins its wheels at $\omega_R = 12$ and $\omega_L = 8$ rad/s. Then

$$v = \frac{0.05 \times 20}{2} = 0.5\ \text{m/s}, \qquad \omega = \frac{0.05 \times 4}{0.3} \approx 0.67\ \text{rad/s}$$

so it drives a circle of radius $v/\omega = 0.75$ m. To drive straight at the same speed, set both wheels to 10 rad/s.

> **Common mistake:** concluding that a nonholonomic robot can't reach a sideways position. It can; it just can't get there in one straight move. Planners have to respect that, which is why parking takes maneuvers.
