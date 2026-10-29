---

---
## One point per pose

A robot's **configuration** $q$ is the smallest set of numbers that fixes where every point of the robot is. The set of all configurations is the **configuration space**, or C-space.

- A point robot on a floor: $q = (x, y)$, a 2-D C-space.
- A rigid body moving in a plane: $q = (x, y, \theta)$, 3-D.
- A 6-joint arm: the six joint angles, 6-D.

The dimension equals the robot's degrees of freedom. Moving the robot, however complicated its shape, becomes moving one point through this space.

## Obstacles grow in C-space

An obstacle in the world becomes a forbidden region of C-space:

$$\mathcal{C}_{\text{obs}} = \{\, q : \text{the robot at } q \text{ overlaps an obstacle} \,\}, \qquad \mathcal{C}_{\text{free}} = \mathcal{C} \setminus \mathcal{C}_{\text{obs}}$$

For a disk robot of radius $r$ described by its center, $\mathcal{C}_{\text{obs}}$ is every obstacle grown outward by $r$ (a **Minkowski sum**). The robot shrinks to a point and the obstacles swell to make up for it. A motion plan is then a continuous path from $q_{\text{start}}$ to $q_{\text{goal}}$ that stays in $\mathcal{C}_{\text{free}}$.

## Worked example: will it fit through the door?

A round vacuum robot has radius $r = 0.3$ m.

- A corridor 0.8 m wide: grow each wall by 0.3 m and the free strip for the robot's center is $0.8 - 2(0.3) = 0.2$ m wide. It fits, with 10 cm of slack on each side.
- A gap 0.5 m wide between two chairs: $0.5 - 0.6 = -0.1$ m. In C-space the gap is closed. No planner will find a path through it, and none should.

Seeing this in C-space is instant; seeing it from the robot's outline usually needs a picture.

## Rotation adds a dimension, and angles wrap

A rectangular robot fits through a gap sideways but not head-on, so whether $q$ is free depends on $\theta$ too. Its $\mathcal{C}_{\text{obs}}$ is a 3-D shape whose cross-section changes with heading.

Angles also wrap around: $\theta = 359°$ and $\theta = 1°$ are neighbors. So C-space isn't always a flat box. For a planar body it's a plane times a circle; for a two-joint arm with full rotation it's a torus.

> **Common mistake:** measuring distance between angles without wrapping. A planner that thinks $359°$ and $1°$ are $358°$ apart will turn the long way round, or miss a path entirely.

## Why the abstraction pays off

One planner now serves every robot: it only needs to ask "is $q$ in $\mathcal{C}_{\text{free}}$?" and "is the straight segment between two configurations free?". A collision checker answers both from the robot's geometry.

In 2-D or 3-D you can build $\mathcal{C}_{\text{obs}}$ explicitly, for example on a grid, and search it. For an arm with 6 or 7 joints that's hopeless, which is why high-dimensional planners sample configurations and check them one at a time instead.
