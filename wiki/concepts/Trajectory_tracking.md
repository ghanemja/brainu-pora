---
source: pora
chapter: 3
layer: D
kind: classical
tags: [pora, robot-autonomy, classical]
---
# Trajectory tracking

Close the loop around a planned trajectory so the robot follows it despite disturbances and model error.

<!-- pora:begin -->
## In Principles of Robot Autonomy

- Read: [Chapter 3: Closed-Loop Control & Trajectory Tracking](https://porabook.com/book/closed-loop-control/)
- Stack layer: Dynamics & control · classical
- Run: [Unicycle Trajectory Tracking](https://colab.research.google.com/github/StanfordASL/pora-exercises/blob/main/ch03/exercises/unicycle_trajectory_tracking.ipynb) ([source](https://github.com/StanfordASL/pora-exercises/blob/main/ch03/exercises/unicycle_trajectory_tracking.ipynb))
- Watch: [AA174A lecture 3: Trajectory Tracking](https://youtu.be/nluc4rMiipA)

### Key ideas

1. Tracking controllers combine a feedforward input u_d(t) from the plan with feedback on the error: u = u_d(t) + K(x_d(t) - x).
2. Feedforward provides the input the model needs to follow the path; feedback corrects disturbances and model error, so neither alone suffices on a real robot.
3. For the unicycle, flatness supplies nominal (x_d, y_d) and their derivatives, and a tracking law can set virtual accelerations from position and velocity errors and map them back to (a, ω).

Try it: Simulate a 1D double integrator tracking x_d = sin t with u = K_p e + K_d ė, with and without the feedforward term ẍ_d = -sin t, and compare errors.

Needs first: [[PID_control]], [[Linearization]], [[Differential_flatness]]

Part of [[Principles_of_Robot_Autonomy]]. Summary and study notes from the unofficial PoRA Atlas; the book is the authoritative reference.
<!-- pora:end -->
