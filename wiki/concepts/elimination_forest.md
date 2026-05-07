# Elimination Forest

## Definition

An **elimination forest** is a forest-structured decomposition of a graph that captures hierarchical vertex elimination orderings. Formally, given a graph $G = (V, E)$, an elimination forest is a rooted forest where:

1. Each vertex of $G$ corresponds to a node in the forest
2. The depth $\tau$ of the forest bounds the length of any root-to-leaf path
3. The structure encodes an elimination order: vertices can be processed level-by-level from leaves to root

The **treedepth** of a graph $G$ is the minimum depth of any elimination forest for $G$, denoted $\text{td}(G)$ or simply $\tau$. Equivalently, treedepth is the minimum depth of a centroid decomposition or the maximum number of "forget nodes" in any optimal tree decomposition of $G$.

**Key property**: A graph has treedepth $\tau$ if and only if it can be colored with $\tau$ colors such that every path in $G$ contains all colors (a "proper coloring of paths").

## Key Equations

For a graph $G$ with treedepth $\tau$ and $n$ vertices:

$$\text{td}(G) \leq O(\log n)$$
for all graphs, with equality for complete graphs.

**Running times achievable via elimination forest algorithms:**

| Problem | Time Complexity | Space |
|---------|-----------------|-------|
| Independent Set | $2^\tau n^{O(1)}$ | Polynomial |
| $q$-Coloring | $q^\tau n^{O(1)}$ | Polynomial |
| Dominating Set | $3^\tau n^{O(1)}$ | Polynomial or $O(\tau \log n)$ |
| Perfect Matching Counting | $2^\tau n^{O(1)}$ | Polynomial |
| Hamiltonian Cycle | $(4w)^\tau n^{O(1)}$ | $O(w\tau n \log n)$ |

## Physical Intuition / Derivation

### Why Elimination Forests Matter

Traditional dynamic programming on graphs requires tracking changing vertex states (e.g., a vertex transitioning from undominated to dominated). This is difficult to encode in branching algorithms, which naturally assign fixed states. **Elimination forests solve this** by providing a static hierarchy:

1. **Hierarchical decomposition**: The forest decomposes the problem into layers. Vertices at the same depth level have similar "roles" in the problem structure.

2. **Branching-friendly structure**: Unlike treewidth (which uses tree decompositions with complex node types), treedepth yields a simpler hierarchy amenable to branching algorithms. Each branch of the forest represents a distinct partial solution space.

3. **Depth-bounded search**: Algorithms traverse the forest from leaves to root. The bounded depth $\tau$ ensures exponential runtime is $2^\tau$ (not $2^n$) while maintaining polynomial space by avoiding memoization tables that would require exponential memory.

### Branching Algorithm Sketch

For **Independent Set** on a graph with treedepth $\tau$:
- Build an elimination forest of depth $\tau$
- Branch on each vertex: include it or exclude it
- Prune infeasible branches (conflicting edges within the forest structure)
- Total branches: $2^\tau$ (depth-limited)
- Verification: $n^{O(1)}$ per branch
- **Result**: $2^\tau n^{O(1)}$ time, polynomial space (no memoization table needed)

Compare to treewidth-based approaches, which often require $2^w n^{O(1)}$ space where $w$ is treewidth.

## Applications in Engineering

### 1. **Parameterized Algorithm Design**
- Algorithm engineers use treedepth-parameterized algorithms when space is critically constrained (embedded systems, real-time processing)
- Preferable to treewidth methods when $\tau \ll w$ (common in sparse, tree-like structures)

### 2. **Network Analysis**
- Sparse communication networks (wireless sensor networks, ad-hoc networks) often have small treedepth
- Enables efficient verification of graph properties (connectivity, dominating sets, cycles) in memory-limited environments

### 3. **VLSI & Circuit Design**
- Circuit graphs often exhibit tree-like structure; treedepth captures this better than general treewidth
- Algorithms for routing, coloring, and component placement can exploit small treedepth

### 4. **Compiler Optimization**
- Control-flow graphs and dependency graphs in programs often have small treedepth
- Enables efficient analysis (liveness, register allocation) with bounded memory

### 5. **Structural Biology**
- Phylogenetic trees and protein interaction networks can be analyzed via treedepth
- Supports efficient enumeration of substructures with polynomial space

## Common Mistakes / Pitfalls

1. **Confusing treedepth with treewidth**: 
   - Treedepth $\tau$ can be much larger than treewidth $w$ (e.g., $\tau = \Theta(\log n)$ while $w = O(1)$)
   - Conversely, a path has $\tau = O(\log n)$ but $w = 1$
   - Choice depends on problem structure

2. **Assuming elimination forests are unique**:
   - A graph admits many elimination forests; only the *minimum depth* (treedepth) is well-defined
   - Different orderings yield different algorithmic efficiencies

3. **Overlooking space vs. time tradeoff**:
   - Treedepth algorithms trade exponential time for polynomial space
   - If space is abundant, treewidth-based algorithms (with polynomial-space techniques like cut-and-count) may be faster in practice

4. **Misapplying to dynamic settings**:
   - Early DP transfers to branching work only for "static" problems (Coloring, Independent Set)
   - Dynamic problems (with state changes) require algebraization techniques (Fürer & Yu [14]) or cut-and-count adaptations

5. **Ignoring hidden constants**:
   - $2^\tau n^{O(1)}$ hides polynomial factors that can be substantial; Dominating Set achieves $3^\tau n^{O(1)}$ only with