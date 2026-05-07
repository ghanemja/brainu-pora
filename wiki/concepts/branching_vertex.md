# branching vertex

## Definition

A **branching vertex** is a vertex in a graph (particularly in the context of geometric graphs on grid-like structures) that has degree greater than 2. In other words, it is a vertex where three or more edges meet.

In the specific context of **distance-preserving graphs** and **Hanan grid** analysis, a branching vertex is of particular interest when it lies outside the grid intersections. A branching vertex $w$ is called a **non-grid branching vertex** if it satisfies:
- Degree 3 or 4 in the host graph $H$
- Does not lie at an intersection of the Hanan grid (i.e., either its row contains no terminal or its column contains no terminal)

## Key Equations

For a branching vertex $w$ with adjacent sets $A$ (from row above) and $B$ (from row below):

$$\text{deg}(w) \geq 3$$

After transformation operations, the edge count evolves as:

$$|E(H')| \leq |E(H)| + |B| - |A|$$
$$|E(H'')| \leq |E(H)| + |A| - |B|$$

where $H'$ and $H''$ are modified graphs obtained by shifting the maximal horizontal path containing $w$ upward and downward, respectively.

## Physical Intuition / Derivation

### Why Branching Vertices Matter

In routing and network design problems, branching vertices represent decision points where paths diverge or converge. The key insight in the source material is that **unnecessary branching vertices outside grid intersections can be eliminated without increasing total path length**.

### The Argument Structure

1. **Starting Premise**: Consider a distance preserver $H$ (a sparse subgraph that preserves all pairwise terminal distances).

2. **Elimination Strategy**: If a branching vertex $w$ exists that is not at a Hanan grid intersection, it means:
   - It lies on a row (or column) that contains no terminals
   - It has degree ≥ 3, creating a "junction" in the graph
   
3. **Geometric Observation**: The Hanan grid is defined as the grid formed by vertical lines through terminals and horizontal lines through terminals. Any shortest path between two grid intersections can be realized entirely within the grid (using Manhattan distance).

4. **Key Transformation**: Given a non-grid branching vertex $w$ on a row with no terminals:
   - Let $P_{uv}$ be the maximal horizontal path through $w$
   - Consider $A$ = vertices above connected to $P_{uv}$
   - Consider $B$ = vertices below connected to $P_{uv}$
   - The path can be shifted one row up (creating $H'$) or one row down (creating $H''$)
   - At least one shift preserves or reduces the edge count: $\min(|E(H')|, |E(H'')|) \leq |E(H)|$

5. **Iterative Elimination**: By repeatedly applying this transformation, all non-grid branching vertices can be moved to grid intersections without increasing the total number of edges. Eventually, the graph becomes contained entirely within the Hanan grid.

## Applications in Engineering

### 1. **VLSI Routing**
Branching vertex analysis is fundamental to chip routing algorithms. Minimizing branching vertices reduces:
- Wire congestion
- Capacitive coupling between nets
- Manufacturing complexity

### 2. **Rectilinear Steiner Tree Problem**
In rectilinear (Manhattan) geometry, the structure and location of branching vertices directly affects tree length and feasibility:
- Optimal Steiner trees have branching vertices only at terminals or grid-determined locations
- Identifying unnecessary branching allows heuristic improvements

### 3. **Network Design**
In telecommunications and utility routing:
- Branching vertices represent junction boxes or relay points
- Reducing unnecessary junctions lowers infrastructure cost
- Constraint on branching vertex location improves optimality

### 4. **Path Planning**
In robotic motion planning and autonomous systems:
- Branching vertices represent decision points in path trees
- Minimizing extraneous branching reduces control complexity
- Grid-aligned branching improves predictability and fault tolerance

### 5. **Supply Chain Logistics**
In warehouse and logistics network design:
- Distribution centers act as branching vertices
- Strategic placement on "grid intersections" (market intersections) optimizes flow

## Common Mistakes / Pitfalls

1. **Confusing Degree with Necessity**: A vertex with high degree is not inherently problematic. The issue is whether that branching can be *relocated* to a grid intersection while preserving distances.

2. **Ignoring Grid Structure**: Assuming any point can serve as a branching vertex. In rectilinear metric, not all locations are equally valid—alignment with the terminal-induced grid structure matters.

3. **Local vs. Global Optimization**: Locally eliminating a branching vertex may increase total edge count if the cost of routing around it is higher. The argument requires *global* analysis across all paths.

4. **Grid Definition**: The Hanan grid is specifically defined by terminal positions, not arbitrary point sets. Many students mistakenly apply this to general graphs without terminal-defined grid structure.

5. **Direction Assumptions**: The proof asymmetrically considers rows vs. columns. Assuming symmetry without verifying that the "deficient" row/column actually exists is a logical error.

## See Also

- [[Hanan grid]] – The canonical grid structure formed by horizontal and vertical lines through terminal points
- [[Distance preserver]] – Sparse subgraph that maintains all terminal-to-terminal distances
- [[Rectilinear Steiner tree]] – Optimization problem where branching vertex placement is critical
- [[Manhattan metric]] – Geometric distance measure underlying rectilinear routing
- [[Graph reduction]] – General technique of eliminating non-essential vertices while preserving graph properties

## Sources

- Simonov, K., Soheil, F., and Verma, S. – Analysis of branching vertices in distance-preserving graphs and their relationship to Hanan grid intersections; context from rectilinear Steiner tree and graph optimization theory.