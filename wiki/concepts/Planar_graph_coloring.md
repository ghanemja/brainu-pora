# Planar Graph Coloring

## Definition

**Planar graph coloring** is the assignment of colors to the vertices of a planar graph such that no two adjacent vertices share the same color, using the minimum number of colors necessary. A planar graph is one that can be drawn on a 2D plane without edge crossings.

The **chromatic number** $\chi(G)$ of a graph $G$ is the minimum number of colors needed for a proper coloring. For planar graphs, the **Four Color Theorem (4CT)** states:

$$\chi(G) \leq 4 \quad \text{for all planar graphs } G$$

The theorem is tight: some planar graphs require exactly 4 colors (e.g., the complete graph $K_4$).

## Key Equations

### Chromatic Number Definition
A proper $k$-coloring is a function $c: V(G) \to \{1, 2, \ldots, k\}$ such that:
$$c(u) \neq c(v) \quad \text{for all edges } (u,v) \in E(G)$$

### Combinatorial Curvature (Discharging Method)
For a planar triangulation with vertex set $V$ and face set $F$, the local combinatorial curvature at vertex $v$ is:
$$\kappa(v) = 1 - \frac{\deg(v)}{6}$$

where $\deg(v)$ is the degree of vertex $v$. By the Gauss-Bonnet theorem for discrete surfaces:
$$\sum_{v \in V} \kappa(v) = 2$$

This fundamental invariant ensures positive curvature exists *somewhere* in any planar graph, motivating inductive algorithms.

## Physical Intuition / Derivation

### Why Four Colors?

Planar graphs have special structure: Euler's formula relates vertices, edges, and faces:
$$V - E + F = 2$$

This constraint ensures the graph is "sparse" relative to general graphs. Specifically, for a simple planar graph:
$$E \leq 3V - 6$$

This sparsity means the average vertex degree is less than 6, guaranteeing vertices of degree $\leq 5$ exist.

### Traditional Approach (Quadratic Time)

Classical 4CT proofs use **reducible configurations**: small subgraphs that can be removed, the remaining graph colored inductively, then the configuration reinserted and colored with the same palette. The traditional algorithm:

1. Find a single reducible configuration or obstructing cycle in the graph
2. Remove it, recursively color the remaining graph (smaller by a constant)
3. Reinsert and complete the coloring

**Problem**: Each removal shrinks the graph by an *additive* constant $c$, requiring $O(n/c)$ recursive levels, each taking $O(n)$ time → $O(n^2)$ total.

### Modern Approach (Near-Linear Time)

The recent breakthrough identifies **linearly many** non-overlapping reducible configurations or non-crossing obstructing cycles of length $\leq 5$ simultaneously. This enables:

1. Find $\Theta(n)$ disjoint reducible configurations
2. Remove all of them at once, shrinking the problem by a *constant factor* $\alpha < 1$
3. Recursively color the reduced graph
4. Recolor configurations in batch

**Recurrence**: $T(n) = T(\alpha n) + O(n \log n)$ solves to $T(n) = O(n \log n)$.

### Discharging and Curvature

The discharging method assigns "charge" to vertices based on curvature:
- Initialize: $\text{charge}(v) = \kappa(v) = 1 - \deg(v)/6$
- Redistribute charge according to local rules
- Identify regions of positive curvature (or zero in "flat" regions) where configurations exist
- The key innovation: finding reductions even in *zero-curvature* regions

## Applications in Engineering

### 1. **Register Allocation (Compiler Design)**
In compiler optimization, variables must be assigned to CPU registers such that variables used simultaneously have different registers. The interference graph is often planar, making 4-coloring directly applicable.

### 2. **Circuit Design & VLSI**
Routing and placement problems reduce to planar graph coloring when minimizing crosstalk and signal interference in layer assignments.

### 3. **Frequency Assignment (Wireless Networks)**
Cell towers can be modeled as planar graphs; coloring assigns frequencies to adjacent towers. Planarity arises naturally in certain geographic topologies.

### 4. **Map Coloring (Geographic Information Systems)**
The original motivation: coloring administrative regions on maps so neighbors have different colors. Planar embedding is explicit.

### 5. **Scheduling with Spatial Constraints**
In robotics or manufacturing, tasks with spatial conflicts (modeled as planar graphs) must be scheduled at different time slots, corresponding to color classes.

## Common Mistakes / Pitfalls

1. **Confusing planarity with tree structure**: A planar graph is *not* necessarily a tree. Trees always have chromatic number $\leq 2$, but planar graphs need up to 4 colors.

2. **Assuming 4-coloring is constructive from the theorem**: The classical proof of 4CT is non-constructive (via computer verification of thousands of cases). Algorithmic versions require explicit constructions like reducible configurations.

3. **Underestimating the difficulty of efficient coloring**: While 4-coloring exists, *finding* it efficiently is computationally hard for general graphs. The near-linear result requires deep structural insights (discharging, curvature, linearly many reductions).

4. **Forgetting non-planarity breaks the bound**: A single additional edge can require 5+ colors. For example, $K_5$ (complete graph on 5 vertices) is non-planar and requires 5 colors.

5. **Assuming reducible configurations are "obvious"**: D-reducibility requires careful verification that removing and reinserting a configuration maintains 4-colorability—not all small subgraphs qualify.

6. **Ignoring the "obstructing cycles" clause**: Cycles of length $\leq 5$ that are non-crossing provide an alternative reduction mechanism