---
source: pora
chapter: 1
layer: D
kind: classical
tags: [pora, robot-autonomy, classical]
---
# Nonholonomic wheeled robots

Wheels that cannot slide sideways constrain velocity but not position. The unicycle and differential-drive models capture this and recur through the book.

<!-- pora:begin -->
## In Principles of Robot Autonomy

- Read: [Chapter 1: Modeling Robot Dynamics](https://porabook.com/book/modeling-robot-dynamics/)
- Stack layer: Dynamics & control · classical
- Run: [Nonholonomic Wheeled Robot Dynamics](https://colab.research.google.com/github/StanfordASL/pora-exercises/blob/main/ch01/exercises/nonholonomic_wheeled_robot_dynamics.ipynb) ([source](https://github.com/StanfordASL/pora-exercises/blob/main/ch01/exercises/nonholonomic_wheeled_robot_dynamics.ipynb))
- Watch: [AA174A lecture 1: Course Overview and Mobile Robot Kinematics](https://youtu.be/Lgt5ONBtFI0)

### Key ideas

1. The unicycle model x_dot = v cos θ, y_dot = v sin θ, θ_dot = ω captures a robot that can drive forward and turn but cannot move sideways.
2. The no-slip condition x_dot sin θ - y_dot cos θ = 0 restricts velocity, but it cannot be integrated into a constraint on position, so every pose is still reachable.
3. A differential-drive robot maps to the unicycle via v = r(ω_R + ω_L)/2 and ω = r(ω_R - ω_L)/L, with wheel radius r and axle length L.

Try it: Integrate the unicycle with Euler steps for v = 1, ω = 0.5 for 4 seconds starting at the origin, and check that the path is an arc of radius v/ω = 2.

Needs first: [[Kinematic_vs_dynamic_models]]

Unlocks: [[Probabilistic_motion_and_sensor_models]]

Part of [[Principles_of_Robot_Autonomy]]. Summary and study notes from the unofficial PoRA Atlas; the book is the authoritative reference.
<!-- pora:end -->
