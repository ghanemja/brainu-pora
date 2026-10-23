---
source: pora
chapter: 4
layer: P
kind: classical
tags: [pora, robot-autonomy, classical]
---
# Potential field methods

Attract the robot to the goal and repel it from obstacles with an artificial field. Fast and reactive, but prone to local minima.

<!-- pora:begin -->
## In Principles of Robot Autonomy

- Read: [Chapter 4: Motion Planning](https://porabook.com/book/motion-planning/)
- Stack layer: Planning · classical

### Key ideas

1. Define U(q) = U_att(q) + U_rep(q): an attractive bowl centered at the goal plus repulsive terms that grow as the robot nears obstacles, often only within an influence distance.
2. The robot follows the negative gradient, q' = -∇U(q), giving a cheap, reactive controller that can run at high rate and respond immediately to newly sensed obstacles.
3. Gradient descent can stop at local minima where attractive and repulsive forces cancel (e.g. inside a U-shaped obstacle), so it is not complete; navigation functions or random escapes address this.

Try it: Plot U(x, y) = 0.5·|q - q_goal|^2 + Σ 1/d_i(q)^2 on a grid with a U-shaped obstacle and run gradient descent from several starts to find where it stalls.

Needs first: [[Configuration_space]]

Part of [[Principles_of_Robot_Autonomy]]. Summary and study notes from the unofficial PoRA Atlas; the book is the authoritative reference.
<!-- pora:end -->
