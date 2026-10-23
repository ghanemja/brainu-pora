---
source: pora
chapter: 1
layer: D
kind: classical
tags: [pora, robot-autonomy, classical]
---
# Kinematic vs. dynamic models

Kinematic models relate velocities to motion and ignore forces; dynamic models include mass, inertia, and actuation. Choosing the right fidelity is a design decision.

<!-- pora:begin -->
## In Principles of Robot Autonomy

- Read: [Chapter 1: Modeling Robot Dynamics](https://porabook.com/book/modeling-robot-dynamics/)
- Stack layer: Dynamics & control · classical
- Run: [Double Integrator Dynamics](https://colab.research.google.com/github/StanfordASL/pora-exercises/blob/main/ch01/exercises/double_integrator_dynamics.ipynb) ([source](https://github.com/StanfordASL/pora-exercises/blob/main/ch01/exercises/double_integrator_dynamics.ipynb))
- Watch: [AA174A lecture 1: Course Overview and Mobile Robot Kinematics](https://youtu.be/Lgt5ONBtFI0)

### Key ideas

1. A kinematic model treats velocities (or wheel speeds) as the inputs and integrates them to get pose; it ignores mass, inertia, and forces.
2. A dynamic model takes forces or torques as inputs and includes mass and inertia, so velocities become states that cannot change instantly.
3. Kinematic models suffice at low speeds and accelerations where actuators track commanded velocities well; at high speed, tire slip and inertia make dynamic models necessary.

Try it: Simulate a 1D cart both as x_dot = v (kinematic) and as x_ddot = (u - b x_dot)/m (dynamic) for a step command, and plot how the dynamic one lags.

Needs first: [[State_space_model]]

Unlocks: [[Nonholonomic_wheeled_robots]], [[Differential_flatness]], [[Configuration_space]]

Part of [[Principles_of_Robot_Autonomy]]. Summary and study notes from the unofficial PoRA Atlas; the book is the authoritative reference.
<!-- pora:end -->
