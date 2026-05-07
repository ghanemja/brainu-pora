# Hanan grid

## Definition

The **Hanan grid** is a geometric graph structure defined over a set of terminal points in the plane. Given a finite set $T$ of terminal points (nodes), the Hanan grid is constructed by drawing vertical and horizontal lines through each terminal's coordinates. Formally, if $T = \{(x_1, y_1), (x_2, y_2), \ldots, (x_n, y_n)\}$, the Hanan grid consists of:

- **Vertices**: All points $(x_i, y_j)$ where $x_i$ and $y_j$ are x- and y-coordinates that appear in at least one terminal
- **Edges**: Unit-length horizontal and vertical segments connecting adjacent grid vertices

The Hanan grid has the fundamental property that **every optimal rectilinear Steiner tree connecting a set of terminals can be represented using only vertices and edges from the Hanan grid**. This makes it a critical structure in network design and routing problems.

## Key Equations

**Grid size bound**: For $n$ terminals, the Hanan grid contains at most $O(n^2)$ vertices:
$$|V(\text{Hanan grid})| \leq n^2$$

since there are at most $n$ distinct x-coordinates and $n$ distinct y-coordinates.

**Distance preservation**: A subgraph $H$ of the Hanan grid is a **distance preserver** if for every pair of terminals $u, v$:
$$d_H(u,v) = d_{\text{grid}}(u,v)$$

where $d$ denotes the shortest path distance using rectilinear (Manhattan) metric.

## Physical Intuition / Derivation

### Why the Hanan Grid Works

Consider the problem: given a set of terminals, find a minimal-length network connecting them all using only horizontal and vertical segments (rectilinear routing). Intuitively, you might think you could place routing nodes anywhere—but this is unnecessary.

**The key insight** is that any routing node (Steiner point) not aligned with existing terminals is "wasteful." Here's why:

1. **Alignment principle**: If a branching vertex $w$ exists at a location where its row contains no terminals and its column contains no terminals, we can shift it along its row without increasing total path length (since no terminal is directly above or below it).

2. **Optimality through replacement**: The proof in the source material shows that if $H$ is any optimal distance preserver and contains a branching vertex $w$ not on the Hanan grid, we can construct an equally-good (or better) network $H'$ by:
   - Removing the horizontal segment containing $w$
   - Adding a parallel segment one row higher (or lower)
   - Adjusting vertical connections accordingly

3. **Termination**: By repeatedly applying such shifts until no branching vertex lies outside the Hanan grid, we obtain an optimal solution confined to the grid.

### Practical Example

Consider three terminals at $(0,0)$, $(3,0)$, and $(1,2)$:
- The Hanan grid has vertical lines at $x \in \{0, 1, 3\}$ and horizontal lines at $y \in \{0, 2\}$
- Any optimal routing can use only the 9 grid intersection points: $(0,0), (0,2), (1,0), (1,2), (3,0), (3,2)$, etc.
- Placing a Steiner point at, say, $(2, 1)$ would be suboptimal—the same connectivity can be achieved using only the grid

## Applications in Engineering

### 1. **VLSI Circuit Routing**
In integrated circuit design, the Hanan grid is foundational for routing wires between circuit components. Designers use it to:
- Minimize total wire length and congestion
- Compute rectilinear Steiner trees for net routing
- Guarantee that optimal solutions exist on a discrete grid (enabling efficient algorithms)

### 2. **Floor Planning and Facility Layout**
In manufacturing and logistics:
- Design of warehouse layouts with rectangular aisles and corridors aligned to a grid
- Minimize travel distance between key facilities (terminals)
- The grid provides natural structural constraints

### 3. **Urban Network Design**
City planning problems use rectilinear metrics (Manhattan distance) due to grid-like street layouts:
- Optimal placement of utility lines (water, power, telecommunications)
- Emergency service station routing
- The Hanan grid reduces the solution space to tractable size

### 4. **Distance-Preserving Graph Compression**
In network theory and database indexing:
- Construct compact graphs that preserve shortest-path distances between query terminals
- Used in distance oracles and spanners
- The Hanan grid principle extends beyond geometric graphs to abstract distance-preserving structures

### 5. **Antenna Placement and Network Optimization**
Wireless and sensor networks:
- Position relay nodes on a grid to minimize infrastructure cost
- Ensure line-of-sight or coverage constraints are met using grid-aligned geometry

## Common Mistakes / Pitfalls

### 1. **Confusing Hanan Grid with Uniform Grid**
**Mistake**: Assuming the Hanan grid is a regular rectangular lattice with fixed spacing.  
**Correction**: The Hanan grid is *adaptive* to terminal positions. Spacing between grid lines varies based on terminal coordinates. Only the lines passing through terminal x- and y-coordinates matter.

### 2. **Assuming All Hanan Grid Vertices Are Needed**
**Mistake**: Using all $O(n^2)$ grid vertices in a distance preserver.  
**Correction**: A minimal distance preserver typically uses far fewer vertices. Many Hanan grid intersections may not contribute to any optimal path. The proof technique shows how to eliminate unnecessary vertices while preserving distances.

### 3. **Forgetting Rectilinear vs. Euclidean Metrics**
**Mistake**: Applying Hanan grid reasoning to Euclidean (straight-line) distance problems.  
**Correction**: The Hanan grid is specific to rectilinear (Manhattan) distances. For Euclidean problems, Steiner points can lie anywhere in the plane, and a discrete grid doesn't capture all optimal solutions.

### 4. **Misunderstanding Branching Vertices**
**Mistake**: Thinking every grid intersection is a candidate for a branching vertex.  
**