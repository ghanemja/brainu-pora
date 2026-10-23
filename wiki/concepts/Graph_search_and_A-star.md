---
source: pora
chapter: 4
layer: P
kind: classical
tags: [pora, robot-autonomy, classical]
---
# Graph search & A*

Discretize the space into a grid or graph and search it with label-correcting algorithms such as A*, using a heuristic to explore toward the goal first.

<!-- pora:begin -->
## In Principles of Robot Autonomy

- Read: [Chapter 4: Motion Planning](https://porabook.com/book/motion-planning/)
- Stack layer: Planning · classical
- Run: [A*](https://colab.research.google.com/github/StanfordASL/pora-exercises/blob/main/ch04/exercises/a_star.ipynb) ([source](https://github.com/StanfordASL/pora-exercises/blob/main/ch04/exercises/a_star.ipynb))
- Watch: [AA174A lecture 5: Motion Planning: Graph Search Methods](https://youtu.be/hFCIZjVkSaw)

### Key ideas

1. Discretize C_free into a graph (grid cells or roadmap nodes) with edge costs, then search for a lowest-cost path; Dijkstra expands nodes in order of cost-to-come g(n).
2. A* orders its open list by f(n) = g(n) + h(n), where h estimates cost-to-go. If h is admissible (never overestimates) the first time the goal is expanded, the returned path is optimal.
3. A better-informed admissible h (closer to the true cost-to-go) expands fewer nodes; h = 0 reduces A* to Dijkstra, while an inflated h (weighted A*) is faster but can return suboptimal paths.

Try it: Write a 20-line A* on a 10×10 NumPy occupancy grid with 4-connected moves; count expanded nodes with h = 0 versus h = Manhattan distance.

Needs first: [[Configuration_space]]

Related: [[dynamic_programming]]

Part of [[Principles_of_Robot_Autonomy]]. Summary and study notes from the unofficial PoRA Atlas; the book is the authoritative reference.
<!-- pora:end -->
