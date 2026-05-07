# Minor-Free Graphs

## Definition

A graph $G$ is **$H$-minor-free** if $H$ does not appear as a minor of $G$. Formally, $H$ is a minor of $G$ if $H$ can be obtained from a subgraph of $G$ by contracting edges.

More precisely: A graph $G$ is $H$-minor-free if there does not exist a sequence of edge contractions that transforms a subgraph of $G$ into $H$.

**Special cases:**
- **Planar graphs**: $K_5$-minor-free and $K_{3,3}$-minor-free (by Kuratowski's theorem)
- **Apex-minor-free graphs**: Graphs where removing a single vertex (the "apex") yields an $H$-minor-free graph
- **$K_{3,h}$-minor-free graphs**: Graphs excluding the complete bipartite graph $K_{3,h}$ as a minor

## Key Equations

**Tree Decomposition Width Bound:** For certain restricted minor-free families, particularly apex-minor-free graphs with localized solutions:

$$\text{treewidth}(G[Z \text{ and neighborhood}]) = k^{O(1)}$$

when the solution set $Z$ intersects each bag in $\tilde{O}(\sqrt{k})$ vertices, where $\tilde{O}$ suppresses polylogarithmic factors.

**Algorithm Runtime for Bounded-Treewidth Graphs:**

$$T(n, k) = 2^{\tilde{O}(\sqrt{k})} \cdot n^{O(1)}$$

This represents a **subexponential** complexity when parameterized by solution size $k$ on graphs with restricted structure.

## Physical Intuition / Derivation

### Why Minor-Free Graphs Matter

The minor relation induces a partial order on graphs. The **Graph Minor Theorem** (Robertson-Seymour) establishes that any minor-closed family of graphs has a finite set of **forbidden minors**—roughly speaking, a small set of "minimal bad" graphs whose absence guarantees membership in the family.

### From Local to Global Structure

The key insight in the source material is that:

1. **Planar graphs** (which are $K_5$-minor-free) can have arbitrarily large treewidth, so local structure alone doesn't constrain global treewidth
2. **Adding a universal vertex** to a planar graph $G_0$ creates a $K_6$-minor-free graph $G$, but the treewidth can remain unbounded
3. However, **apex-minor-free graphs** admit better structural decompositions when solutions are "localized"

### The Localization Principle

The results rely on a crucial observation: if a solution set $Z$ (of size $k$) is constrained to intersect each bag in the tree decomposition in only $\tilde{O}(\sqrt{k})$ vertices, then dynamic programming becomes tractable even when the absolute treewidth is large.

This creates a spectrum:
- **Unrestricted**: $H$-minor-free graphs generally have no polynomial treewidth bound
- **Restricted**: Apex-minor-free graphs + localized solutions → subexponential algorithms
- **Intermediate**: $K_{3,h}$-minor-free graphs → algorithms for specific cases

## Applications in Engineering

### 1. **Network Design & Graph Algorithms**

Minor-free graph properties enable subexponential algorithms for:
- **Subgraph isomorphism detection**: Finding if a bounded-degree pattern $P$ appears in an apex-minor-free network in time $2^{\tilde{O}(\sqrt{|V(P)|})}\cdot |V(G)|^{O(1)}$
- **Facility location problems**: Optimal placement in planar or nearly-planar infrastructure networks
- **Constraint satisfaction**: CSP instances with planar constraint graphs

### 2. **VLSI Circuit Design**

Planar and minor-free graph theory applies to:
- **Routing problems**: Minimizing wire crossings in chip layouts
- **Floorplanning**: Arranging circuit blocks with connectivity constraints
- **Fault tolerance**: Analyzing connectivity under edge/vertex failures

### 3. **Transportation Networks**

Real-world road and rail networks approximate planar or sparse minor-free structures:
- **Shortest path computation**: Leverage treewidth bounds for sublinear query times
- **Traffic flow optimization**: Dynamic programming on decompositions
- **Network resilience**: Quantify "how far" from planarity a network is

### 4. **Computational Biology**

Phylogenetic trees and metabolic networks often have restricted minor-free structure:
- **Sequence alignment**: Graph-based dynamic programming on treewidth-bounded structures
- **Protein interaction networks**: Local clustering properties of minor-free networks

## Common Mistakes / Pitfalls

### 1. **Confusing Minor-Free with Treewidth**
**Mistake:** "A graph is $H$-minor-free, therefore it has bounded treewidth."

**Reality:** $K_5$-minor-free planar graphs can have arbitrarily large treewidth. Minor-freeness does *not* imply global treewidth bounds—only structural restrictions on how dense subgraphs can be.

### 2. **Overgeneralizing from Planar Results**
**Mistake:** Assuming algorithms that work for planar graphs extend to all $K_5$-minor-free graphs.

**Reality:** Many planar algorithms exploit embedding properties beyond just minor-freeness. General minor-free results often require additional restrictions (apex, bipartite components, etc.).

### 3. **Ignoring Localization Constraints**
**Mistake:** Expecting polynomial algorithms for arbitrary $H$-minor-free graphs.

**Reality:** The subexponential algorithms in the source material require:
- Apex-minor-free (not general minor-free), AND
- Solutions constrained to intersect decomposition bags minimally

Without both conditions, NP-hardness persists even for $K_6$-minor-free graphs.

### 4. **The Universal Vertex Trap**
The source material illustrates a critical example: adding one universal vertex to a planar graph preserves $K_6$-minor-freeness but destroys tractability. A common mistake is assuming sparse connectivity properties.

## See Also