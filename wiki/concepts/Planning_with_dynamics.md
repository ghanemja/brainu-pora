---
source: pora
chapter: 4
layer: P
kind: classical
tags: [pora, robot-autonomy, classical]
---
# Planning with dynamics

Plan paths that respect the robot's dynamics, not just its geometry, so the result is something the robot can actually execute.

<!-- pora:begin -->
## In Principles of Robot Autonomy

- Read: [Chapter 4: Motion Planning](https://porabook.com/book/motion-planning/)
- Stack layer: Planning · classical

### Key ideas

1. Geometric paths ignore dynamics like nonholonomic constraints, velocity and acceleration limits; a car cannot follow a path with a sharp corner or a sideways step.
2. Kinodynamic planners search over state x (e.g. position and velocity) and extend the tree by integrating x' = f(x, u) forward under sampled or chosen controls, so every edge is dynamically feasible.
3. Connecting two exact states requires solving a two-point boundary value problem (steering), which is often hard; alternatives are forward propagation with random controls, motion primitives, or trajectory optimization.

Try it: Simulate a unicycle x'=v cosθ, y'=v sinθ, θ'=ω with 5 constant control primitives for 1 s each and plot the reachable endpoints after two steps.

Needs first: [[Sampling-based_planning_PRM_RRT]], [[Optimal_control_problems]]

Part of [[Principles_of_Robot_Autonomy]]. Summary and study notes from the unofficial PoRA Atlas; the book is the authoritative reference.
<!-- pora:end -->
