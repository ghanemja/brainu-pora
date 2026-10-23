---
source: pora
chapter: 16
layer: L
kind: classical
tags: [pora, robot-autonomy, classical]
---
# Finite state machines

Hand-designed modes and transitions that sequence behaviors. Still how many deployed robots decide what to do next.

<!-- pora:begin -->
## In Principles of Robot Autonomy

- Read: [Chapter 16: Finite State Machines](https://porabook.com/book/finite-state-machines/)
- Stack layer: Decisions & learning · classical

### Key ideas

1. A finite state machine has a set of discrete modes (e.g. EXPLORE, APPROACH, GRASP, RECOVER), each running a behavior, and transitions triggered by events or conditions.
2. FSMs are transparent and easy to verify by inspection, which is why they sequence behaviors in many deployed robots; each transition can be logged and tested.
3. They scale poorly: the number of states and transitions grows quickly with features, so hierarchical FSMs or behavior trees are used to keep structure manageable.

Try it: Write a small Python FSM for a line-following robot with states FOLLOW, LOST, SEARCH, STOP using a dict of transitions; simulate a sequence of sensor events and print the state trajectory.

Needs first: [[Autonomy_software_stack]]

Part of [[Principles_of_Robot_Autonomy]]. Summary and study notes from the unofficial PoRA Atlas; the book is the authoritative reference.
<!-- pora:end -->
