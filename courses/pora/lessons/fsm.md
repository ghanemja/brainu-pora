---
video: -Yicg2TTMPs | Understanding State Machines, Part 1: What Are They? | MATLAB | 3:18
video: gXrKGTPwfO8 | Behavior Trees vs Finite State Machines (BT intro part 4) | Petter Ögren | 9:14
---
## Modes and transitions

A **finite state machine** (FSM) splits a robot's job into a handful of discrete **modes**, such as EXPLORE, APPROACH, GRASP and RECOVER. Exactly one mode is active at a time, and each mode runs its own behavior: a planner goal, a controller, or a simple routine.

**Transitions** move between modes when an event or condition fires: "object detected", "gripper closed", "no progress for 10 s". The whole decision logic fits in a diagram you can draw on a whiteboard, which is why so many deployed robots use one to decide what to do next.

## Worked example: a delivery robot

A hospital delivery robot needs five modes and six transitions:

- IDLE → NAVIGATE when an order arrives.
- NAVIGATE → HANDOFF when it's within 0.5 m of the drop-off point.
- HANDOFF → RETURN when a nurse confirms pickup, or after 120 s with nobody there.
- RETURN → IDLE when it docks.
- NAVIGATE → RECOVER if blocked for more than 10 s; RECOVER → NAVIGATE once the path is clear.

Each transition is one testable rule. Note the timeout on HANDOFF: without it, an unattended robot would wait forever.

## Why engineers like them

FSMs are **transparent**: at any moment you know exactly which mode the robot is in and why it got there. Every transition can be logged, every mode can be tested on its own, and the whole thing can be checked by inspection, for example "is there a path from every mode back to IDLE?". That matters for safety reviews and certification, and for debugging at 2 a.m. A learned policy offers none of this.

## Where they break down

FSMs scale badly. Add a "battery low → go charge" behavior and it needs a transition out of nearly every mode, plus a way back to whatever the robot was doing. Add "pause when a person is close" and it multiplies again. Combining independent features multiplies modes: 5 task modes times 3 battery states times 2 safety states is 30 combinations.

**Hierarchical** FSMs nest machines inside modes, so "battery low" can interrupt the whole task machine at once.

## Behavior trees

**Behavior trees** are the popular alternative. Behaviors are leaves of a tree, combined by **sequence** nodes (do these in order until one fails) and **fallback** nodes (try these until one succeeds). The tree is re-evaluated ("ticked") many times per second, so higher-priority branches, such as "if battery low, charge", take over automatically. Subtrees are reusable modules, and adding a behavior rarely means rewiring the others.

> **Common mistake:** a mode with no way out. If GRASP only exits on "grasp succeeded", a single missed grasp leaves the robot frozen forever. Give every mode a timeout or failure transition, and a path back to a safe state.
