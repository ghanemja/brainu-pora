---

---
## From space to graph

Graph search plans on a discrete version of the free space. Cover $\mathcal{C}_{\text{free}}$ with grid cells (or roadmap nodes), connect neighbors with edges, and give each edge a cost, usually its length. On a grid, each cell connects to 4 neighbors (cost 1) or 8 neighbors (diagonals cost $\sqrt2$).

The path you get is only as good as the grid: too coarse and narrow gaps vanish, too fine and the graph gets huge. In exchange, the search is exact on that graph.

## Dijkstra: always expand the cheapest node

Keep an **open list** of nodes to explore, ordered by **cost-to-come** $g(n)$, the cheapest known cost from the start to $n$. Repeatedly:

- Pop the node with the smallest $g$.
- For each neighbor, if going through this node is cheaper than its current $g$, update it and record this node as its parent.

When the goal is popped, its $g$ is the optimal cost, and following parents back gives the path. The catch: Dijkstra expands outward in every direction equally, including away from the goal.

## A*: add a guess of what's left

A* orders the open list by

$$f(n) = g(n) + h(n)$$

where the **heuristic** $h(n)$ estimates the cost from $n$ to the goal. Nodes that look like they're on a short route get explored first.

If $h$ is **admissible**, meaning it never overestimates the true cost-to-go, the first time A* pops the goal its path is optimal. Setting $h = 0$ gives back Dijkstra. The closer an admissible $h$ is to the truth, the fewer nodes A* expands.

## Worked example: an empty grid

On an open 4-connected grid, go from $(0, 0)$ to $(4, 3)$. The true cost is $4 + 3 = 7$.

- **Dijkstra** expands by $g$ until it reaches $g = 7$: up to the whole diamond of 113 cells with $g \le 7$.
- **A*** with the Manhattan heuristic $h = |\Delta x| + |\Delta y|$ (exact here, so $h(\text{start}) = 7$) only expands cells with $f = 7$, which all lie in the $5 \times 4$ rectangle between start and goal: at most 20 cells.
- Euclidean distance, $h(\text{start}) = \sqrt{4^2 + 3^2} = 5$, is also admissible but less informed, so A* expands more than 20.

## Trading optimality for speed

**Weighted A*** uses $f = g + \varepsilon\, h$ with $\varepsilon > 1$. It dives toward the goal and expands far fewer nodes, at the cost of paths that can be up to $\varepsilon$ times longer than optimal. Many robots use it when replanning speed matters more than the last few percent of path length.

> **Common mistake:** using the Manhattan heuristic on an 8-connected grid. A diagonal step from $(0, 0)$ to $(1, 1)$ really costs $\sqrt2 \approx 1.41$, but Manhattan says 2. That overestimates, so it isn't admissible and A* can return a longer path. Use the octile or Euclidean distance instead.
