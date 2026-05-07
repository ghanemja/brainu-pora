# Four Color Theorem

## Definition

The **Four Color Theorem (4CT)** states that every planar graph can be properly colored using at most 4 colors such that no two adjacent vertices share the same color.

Formally: For any planar graph $G = (V, E)$, there exists a function $f: V \to \{1, 2, 3, 4\}$ such that for all edges $(u, v) \in E$, we have $f(u) \neq f(v)$.

A **planar graph** is a graph that can be drawn on a plane without edge crossings. A **proper coloring** assigns colors to vertices so that adjacent vertices receive different colors. The **chromatic number** $\chi(G)$ is the minimum number of colors needed to properly color $G$; for planar graphs, $\chi(G) \leq 4$.

### Historical Context

The theorem was first conjectured in 1852 and represents one of the first major theorems requiring computer verification (Appel & Haken, 1976). Recent work has dramatically improved the algorithmic aspects, as demonstrated in the 2026 paper by Inoue et al., which achieves near-linear time complexity.

## Key Equations

### Chromatic Number Bound
$$\chi(G) \leq 4 \quad \text{for all planar graphs } G$$

### Planar Graph Constraint (Euler's Formula)
For a connected planar graph with $n$ vertices, $m$ edges, and $f$ faces:
$$n - m + f = 2$$

This implies:
$$m \leq 3n - 6 \quad \text{(linear edge density)}$$

### Reducibility via Discharging
The modern proofs use **combinatorial curvature**. For each vertex $v$ of degree $d_v$ in a triangulation:
$$\text{curvature}(v) = 6 - d_v$$

Vertices with positive curvature are reliably reducible; the key innovation of Inoue et al. is finding $\Theta(n)$ reducible configurations even in flat regions where curvature equals zero.

### Time Complexity Improvement
- **Previous result (Robertson et al., 1996):** $O(n^2)$ time
- **New result (Inoue et al., 2026):** $O(n \log n)$ time

The improvement arises from reducing the problem size by a constant factor per recursive step rather than by an additive constant.

## Physical Intuition / Derivation

### Why Planar Graphs Need Only 4 Colors

Consider the Euler characteristic constraint. A planar graph cannot be too densely connected (at most $3n - 6$ edges). This density bound severely limits the chromatic number:

1. **Local density control:** The edge sparsity means not every vertex can have many neighbors. By the pigeonhole principle, there exist regions where the graph is "loose" enough to admit reductions.

2. **Reducible configurations:** A subgraph configuration is **reducible** if once it is removed and the remaining graph is 4-colored, the removed vertices can always be recolored to maintain a valid 4-coloring. The classical proofs showed the existence of at least one such configuration in any minimal counterexample (a hypothetical minimal planar graph requiring 5 colors).

3. **The discharging method:** This combinatorial technique assigns "charge" to vertices based on their degree, then redistributes charge via local rules. Vertices ending with positive charge correspond to reducible configurations. The key insight:
   - Classical methods find one reducible region (additive reduction → quadratic time)
   - Inoue et al. find $\Theta(n)$ pairwise non-touching reducible configurations (multiplicative reduction → near-linear time)

### D-Reducibility

A configuration is **D-reducible** if membership in the configuration can be locally verified without examining the entire graph. This property ensures that:
- Configurations can be identified in linear time
- Multiple non-overlapping configurations can be processed independently and in parallel

### Flat Regions and Curvature

The curvature formula $\text{curvature}(v) = 6 - d_v$ is zero when $d_v = 6$. In large triangulations, many vertices have degree near 6. The innovation is proving that these "flat" regions also contain harvestable reducible configurations—previously missed by methods that only looked at positive-curvature regions.

## Applications in Engineering

### 1. **Circuit and VLSI Design**
- **Planarity testing and routing:** Before detailed routing, circuits are analyzed for planarity. The 4CT guarantees that planar netlists can be decomposed into 4 independent layers (metallization layers in chip design).
- **Frequency assignment:** In multi-layer PCB design, the near-linear 4-coloring algorithm enables real-time routing optimization.

### 2. **Network Design and Wireless Communications**
- **Frequency assignment in cellular networks:** Base stations form a planar-like topology; the 4CT proves that only 4 frequency bands are needed in principle for interference-free coverage (though practical systems use more for capacity).
- **Graph decomposition:** The fast coloring algorithm decomposes large network topologies into independent routing subproblems.

### 3. **Geographic Information Systems (GIS)**
- **Map coloring:** Political/administrative boundaries form naturally planar graphs. The theorem guarantees 4 colors suffice for any map; the fast algorithm enables dynamic re-coloring when boundaries change.
- **Spatial partitioning:** Planar subdivisions are fundamental in GIS; efficient coloring supports spatial indexing and queries.

### 4. **Compiler Design**
- **Register allocation:** In some register allocation problems, variables and their conflicts form planar graphs. The 4CT guarantees feasibility of allocation on RISC architectures with 4+ registers.

### 5. **Graph Drawing and Visualization**
- **Planar graph embeddings:** Determining if a graph is planar and can be drawn without crossings is fundamental. The coloring algorithm supports aesthetic graph layout.

### 6. **Scheduling and Resource Allocation**
- **Timetable generation:** If constraints form a planar conflict graph, 4 time slots suffice (e.g., university course scheduling in limited infrastructure).

## Common Mistakes / Pitfalls

### 1. **