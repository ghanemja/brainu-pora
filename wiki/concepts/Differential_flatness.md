---
source: pora
chapter: 2
layer: D
kind: classical
tags: [pora, robot-autonomy, classical]
---
# Differential flatness

For some systems, all states and inputs follow from a few flat outputs and their derivatives, so smooth trajectories can be designed in those outputs directly.

<!-- pora:begin -->
## In Principles of Robot Autonomy

- Read: [Chapter 2: Open-Loop Control & Trajectory Optimization](https://porabook.com/book/open-loop-control/)
- Stack layer: Dynamics & control · classical
- Run: [Differentially Flat Planar Quadrotor](https://colab.research.google.com/github/StanfordASL/pora-exercises/blob/main/ch02/differentially_flat_planar_quadrotor.ipynb) ([source](https://github.com/StanfordASL/pora-exercises/blob/main/ch02/differentially_flat_planar_quadrotor.ipynb))
- Watch: [AA174A lecture 2: Trajectory Optimization](https://youtu.be/Kv5G2OlrIbU)

### Key ideas

1. A system is differentially flat if there exist outputs z (the flat outputs) such that every state and input can be written as a function of z and finitely many of its derivatives.
2. For the unicycle, z = (x, y) is flat: v = √(ẋ^2 + ẏ^2), θ = atan2(ẏ, ẋ), and ω follows from second derivatives, valid while v ≠ 0.
3. Planning becomes curve fitting: choose smooth z(t) (e.g. polynomials) meeting boundary conditions, and the dynamics are satisfied automatically.

Try it: Pick x(t) = t, y(t) = t^2 for t ∈ [0, 1] and compute the unicycle's v(t), θ(t) and ω(t) from the flat outputs.

Needs first: [[Kinematic_vs_dynamic_models]]

Unlocks: [[Trajectory_tracking]]

Part of [[Principles_of_Robot_Autonomy]]. Summary and study notes from the unofficial PoRA Atlas; the book is the authoritative reference.
<!-- pora:end -->
