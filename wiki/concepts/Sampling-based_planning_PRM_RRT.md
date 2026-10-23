---
source: pora
chapter: 4
layer: P
kind: classical
tags: [pora, robot-autonomy, classical]
---
# Sampling-based planning (PRM, RRT)

Sample random configurations and connect them into a roadmap or tree. Scales to high-dimensional spaces where grids fail.

<!-- pora:begin -->
## In Principles of Robot Autonomy

- Read: [Chapter 4: Motion Planning](https://porabook.com/book/motion-planning/)
- Stack layer: Planning · classical
- Run: [RRT](https://colab.research.google.com/github/StanfordASL/pora-exercises/blob/main/ch04/exercises/rrt.ipynb) ([source](https://github.com/StanfordASL/pora-exercises/blob/main/ch04/exercises/rrt.ipynb))
- Run: [PRM*](https://colab.research.google.com/github/StanfordASL/pora-exercises/blob/main/ch04/prm_star.ipynb) ([source](https://github.com/StanfordASL/pora-exercises/blob/main/ch04/prm_star.ipynb))
- Watch: [AA174A lecture 6: Motion Planning: Sampling-Based Methods](https://youtu.be/AN4jXyWwV7Q)

### Key ideas

1. Instead of discretizing C-space explicitly, sample random configurations, keep those that pass a collision checker, and connect nearby ones with a local planner (e.g. straight lines checked for collision).
2. PRM builds a reusable roadmap for many queries; RRT grows a single tree from q_start by extending the nearest node toward each random sample, which biases growth into unexplored regions (Voronoi bias).
3. These methods are probabilistically complete: the chance of finding a path, if one exists, goes to 1 as samples grow. Basic RRT is not asymptotically optimal; RRT* and PRM* rewire connections to get optimality.

Try it: Implement a basic RRT for a point robot in a 2D square with two rectangular obstacles in NumPy and plot the tree after 200, 1000 and 5000 samples.

Needs first: [[Configuration_space]], [[Probability]]

Unlocks: [[Planning_with_dynamics]]

Part of [[Principles_of_Robot_Autonomy]]. Summary and study notes from the unofficial PoRA Atlas; the book is the authoritative reference.
<!-- pora:end -->
