---
video: QR3U1dgc5RE | Path Planning with A* and RRT | Autonomous Navigation, Part 4 | MATLAB | 17:55
video: rKe6HO8LDu0 | Modern Robotics, Chapter 10.5: Sampling Methods for Motion Planning (Part 1 of 2) | Northwestern Robotics | 3:12
---
## Why not just use a grid?

Grids grow exponentially with dimension. A 7-joint arm with 100 cells per joint would need $100^7 = 10^{14}$ cells, far beyond any computer's memory. And building $\mathcal{C}_{\text{obs}}$ explicitly for an arm is impractical anyway.

**Sampling-based planners** skip both problems. They pick random configurations, ask a collision checker whether each is free, and connect nearby free ones with short straight segments (also collision-checked). They never build the whole C-space; they only probe it where they need to.

## PRM: a roadmap you reuse

The **probabilistic roadmap** works in two phases.

- **Build**: sample $n$ free configurations. Connect each to its $k$ nearest neighbors whenever the segment between them is collision-free. The result is a graph of free space.
- **Query**: connect the start and goal to the roadmap the same way, then run graph search (Dijkstra or A*).

The roadmap is built once and answers many queries, which suits a static environment, such as an arm working in a fixed cell.

## RRT: a tree that grows toward the unknown

A **rapidly-exploring random tree** grows from the start for a single query. Each iteration:

- Sample a random configuration $q_{\text{rand}}$ (with a small probability, say 5%, use the goal instead).
- Find the tree node $q_{\text{near}}$ nearest to it.
- Step from $q_{\text{near}}$ toward $q_{\text{rand}}$ by at most $\eta$, giving $q_{\text{new}}$. If the segment is free, add it to the tree.

Nodes on the edge of big unexplored regions are nearest to more random samples, so they get extended more often. This **Voronoi bias** pulls the tree outward fast.

## Worked example: one RRT extension

The nearest node is $q_{\text{near}} = (1, 1)$, the sample is $q_{\text{rand}} = (4, 5)$, and the step size is $\eta = 0.5$.

The direction is $(4 - 1, 5 - 1) = (3, 4)$, which has length $5$, so the unit direction is $(0.6, 0.8)$. Then

$$q_{\text{new}} = (1, 1) + 0.5\,(0.6, 0.8) = (1.3, 1.4)$$

If the segment from $(1, 1)$ to $(1.3, 1.4)$ is collision-free, $(1.3, 1.4)$ joins the tree with $(1, 1)$ as its parent.

## What the guarantees are

These planners are **probabilistically complete**: if a path exists, the chance of finding it goes to 1 as the number of samples grows. They can't prove that no path exists.

Basic RRT is not **asymptotically optimal**: its paths stay jagged however long it runs. **RRT\*** and **PRM\*** rewire connections as they go so the path converges to the shortest one. Narrow passages remain hard for all of them, because few random samples land inside.

> **Common mistake:** checking collisions only at the sampled nodes. Two free configurations can have a wall between them. Check the whole edge, at a resolution finer than the thinnest obstacle.
