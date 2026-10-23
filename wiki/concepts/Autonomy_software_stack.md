---
source: pora
chapter: 0
layer: F
kind: foundation
tags: [pora, robot-autonomy, foundation]
---
# Autonomy software stack

The Python tooling and the idea of a modular stack where perception, estimation, planning, and control run as connected components.

<!-- pora:begin -->
## In Principles of Robot Autonomy

- Read: [Getting started: Robot Autonomy Software](https://porabook.com/book/software/)
- Stack layer: Foundations · foundation

### Key ideas

1. An autonomy stack splits the robot's job into modules: perception turns raw sensor data into features or objects, estimation tracks the robot's state, planning picks a path, and control turns it into actuator commands.
2. Modules communicate through well-defined messages (e.g. publish/subscribe topics as in ROS), so each can be developed, tested, and replaced independently.
3. Modules run at different rates: a low-level controller may run at hundreds of Hz while a global planner replans only occasionally, so interfaces must tolerate stale or asynchronous data.

Try it: Sketch a block diagram for a robot that drives to a goal: list each module, the message it publishes, the topics it subscribes to, and a plausible update rate.

Unlocks: [[Finite_state_machines]]

Part of [[Principles_of_Robot_Autonomy]]. Summary and study notes from the unofficial PoRA Atlas; the book is the authoritative reference.
<!-- pora:end -->
