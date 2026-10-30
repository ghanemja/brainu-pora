---
video: 8Vva0bnMIEI | Modern Robotics, Chapter 10.6: Virtual Potential Fields | Northwestern Robotics | 5:10
---
## A bowl and some hills

A potential field method doesn't plan a path at all. It defines a landscape $U(q)$ over configuration space, low at the goal and high near obstacles, and lets the robot roll downhill:

$$U(q) = U_{\text{att}}(q) + U_{\text{rep}}(q), \qquad \dot q = -\nabla U(q)$$

The goal attracts, the obstacles repel, and the robot follows the combined force. Each step needs only the gradient at the current $q$, so it's cheap enough to run at hundreds of hertz and reacts the moment a new obstacle shows up in the sensor data.

## The usual formulas

The attractive part is a bowl centered on the goal:

$$U_{\text{att}} = \tfrac12 k_{\text{att}}\, \|q - q_{\text{goal}}\|^2$$

The repulsive part only acts within an influence distance $\rho_0$ of an obstacle. With $\rho(q)$ the distance to the nearest obstacle:

$$U_{\text{rep}} = \tfrac12 k_{\text{rep}} \left( \frac{1}{\rho} - \frac{1}{\rho_0} \right)^2 \text{ if } \rho \le \rho_0, \text{ else } 0$$

Its force, $-\nabla U_{\text{rep}} = k_{\text{rep}} \left( \frac1\rho - \frac1{\rho_0} \right) \frac{1}{\rho^2} \nabla\rho$, points away from the obstacle and grows without bound as $\rho \to 0$.

## Worked example: one step's force

The robot is at $q = (2, 0)$, the goal at $(5, 0)$, with $k_{\text{att}} = 1$. The attractive force is $-k_{\text{att}}(q - q_{\text{goal}}) = (3, 0)$.

The nearest obstacle point is $(2, 1)$, so $\rho = 1$. With $\rho_0 = 2$ and $k_{\text{rep}} = 1$, the repulsive magnitude is $(1 - 0.5) \times 1/1^2 = 0.5$, along $\nabla \rho = (0, -1)$ (away from the obstacle). So the repulsive force is $(0, -0.5)$.

The total is $(3, -0.5)$: mostly toward the goal, nudged away from the obstacle.

## The local-minimum trap

Gradient descent stops wherever $\nabla U = 0$, not only at the goal. Inside a U-shaped obstacle facing the robot there is a point where attraction and repulsion cancel. The robot drives in and stays.

So potential fields are **not complete**: they can fail even when a path exists. Fixes include random walks to escape, **navigation functions** (fields built to have only one minimum, at the goal), or using the field as a fast local layer under a global planner.

> **Common mistake:** setting $\rho_0$ or $k_{\text{rep}}$ too large in a corridor. Repulsion from both walls overlaps, and the robot oscillates side to side, or a doorway becomes impassable even though it's wide enough.
