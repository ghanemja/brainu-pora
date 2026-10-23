---
source: pora
chapter: 4
layer: P
kind: classical
tags: [pora, robot-autonomy, classical]
---
# Configuration space

Represent every possible robot pose as a point, with obstacles becoming forbidden regions. Planning becomes finding a path between points.

<!-- pora:begin -->
## In Principles of Robot Autonomy

- Read: [Chapter 4: Motion Planning](https://porabook.com/book/motion-planning/)
- Stack layer: Planning · classical
- Watch: [AA174A lecture 5: Motion Planning: Graph Search Methods](https://youtu.be/hFCIZjVkSaw)

### Key ideas

1. The configuration q of a robot is the minimal set of parameters that fixes the position of every point on it: (x, y) for a point robot, (x, y, θ) for a planar rigid body, joint angles for an arm.
2. Obstacles map into C-space as C_obs, the set of q where the robot body intersects an obstacle; C_free is the rest. For a disk robot of radius r, C_obs is each obstacle grown (Minkowski-summed) by r.
3. Planning a collision-free motion for a shaped robot becomes finding a continuous path for a single point from q_start to q_goal inside C_free, which lets one algorithm serve many robot shapes.

Try it: Draw a square obstacle and a disk robot of radius r on paper, then sketch the C-space obstacle by sliding the disk around the square's boundary; note the rounded corners.

Needs first: [[Kinematic_vs_dynamic_models]]

Unlocks: [[Graph_search_and_A-star]], [[Sampling-based_planning_PRM_RRT]], [[Potential_field_methods]]

Part of [[Principles_of_Robot_Autonomy]]. Summary and study notes from the unofficial PoRA Atlas; the book is the authoritative reference.
<!-- pora:end -->
