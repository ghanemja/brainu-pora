# Contraction Decomposition

## Definition

**Contraction decomposition** is a graph algorithmic technique for systematically reducing graph complexity by selectively contracting vertices or regions while preserving key structural properties—particularly treewidth. It enables the transformation of hard optimization problems on general graphs into tractable problems on bounded-treewidth instances.

Formally, given a graph $G$ and a subgraph (or set of vertices) $X$, the contraction decomposition recursively:
1. Identifies a region $X$ and its neighborhood $X_r$
2. Contracts the neighborhood to a single supernode
3. Solves the resulting contracted problem on $G/X_c$ (the graph with $X_c$ contracted)
4. "Lifts" the solution back to the original graph

The technique is particularly valuable when combined with **tree decomposition**, which expresses graph structure as a hierarchical tree with bounded width.

## Key Equations

For a graph $G$ with metric structure defined by another graph $H$ (where the identity map is $c$-Lipschitz), the fundamental bound is:

$$\text{tw}(G/X_c) = O(\Delta c) \cdot \text{tw}(H/X)$$

where:
- $\text{tw}(\cdot)$ denotes treewidth
- $X_r = N_H(X, r)$ is the $r$-neighborhood of $X$ in $H$ (vertices within $H$-distance $r$ from $X$)
- $\Delta$ is the maximum degree of $H$
- $c$ is the Lipschitz constant
- $X_c$ is the contracted region in $G$

**Consequence for algorithm complexity:**  
If the skeleton/spanner has size $s = \text{poly}(1/\varepsilon) \cdot \text{OPT}$, then:
$$T_{\text{total}} = 2^{\text{poly}(1/\varepsilon)} \cdot n^{O(1)}$$

This arises from bounding treewidth to $2^{\text{poly}(1/\varepsilon)}$ via contraction decomposition.

## Physical Intuition / Derivation

### Why Contract Neighborhoods, Not Just Vertices?

The key insight from Lemma 2.5 is subtle: **contracting just $X$ is insufficient**; you must contract a neighborhood $X_c$ or $X_r$.

**Reason:** When translating a tree decomposition from the contracted graph $H/X$ back to the original graph $G$, the contraction introduces "phantom edges" between distant vertices in $G$ that become adjacent in $H/X$. The $c$-Lipschitz relationship means distances in $G$ can be up to $c$ times larger than in $H$. By contracting the neighborhood of radius $r$ in the metric defined by $H$, we absorb these phantom edges, preventing explosion in treewidth.

### Algorithmic Pipeline

For Steiner tree on planar graphs (motivating example):

1. **Construct spanner:** Build a subgraph containing a $(1+\varepsilon)$-optimal Steiner tree, with size $\text{poly}(1/\varepsilon) \cdot \text{OPT}$.

2. **Decompose into columns & bricks:** Partition faces of the skeleton using "columns"—shortest paths perpendicular to face boundaries spaced at intervals $\kappa = \text{poly}(1/\varepsilon)$.

3. **Build mortar graph:** Select every $\kappa$-th column; the resulting graph has bounded size and structure.

4. **Contract:** Apply contraction decomposition to reduce to treewidth $2^{\text{poly}(1/\varepsilon)}$.

5. **Solve:** Use dynamic programming on the bounded-treewidth instance.

6. **Lift:** Extend solution back to original graph using decomposition structure.

The columns don't cross in planar graphs (crucial for the algorithm), but for **intersection graphs** (e.g., disk graphs), additional technical work is needed to impose non-crossing structure.

## Applications in Engineering

### Optimization Problems on Planar/Sparse Graphs

- **Steiner tree approximation:** Achieves EPTAS (Efficient Polynomial-Time Approximation Scheme) on planar graphs via contraction decomposition + DP on bounded treewidth.
  
- **Subset TSP:** Similar approach yields EPTAS for traveling salesman on terminal subsets.

- **Routing & network design:** Contraction preserves planarity; useful for VLSI layout and chip design where sparsity is guaranteed.

### Parameterized Algorithms

- **Fixed-parameter tractability (FPT):** Many NP-hard problems become FPT when parameterized by treewidth; contraction decomposition reduces general graphs to bounded-treewidth cases, enabling FPT algorithms.

- **Graph minor/topological algorithms:** Contraction is fundamental in minor-closed families; used in Robertson-Seymour theory and structural graph algorithms.

### Practical Machine Learning & Data Structures

- **Graph neural networks on sparse graphs:** Contraction can reduce graph size before neural network inference while preserving essential structure.

- **Hierarchical clustering:** Contraction decomposition induces a tree hierarchy useful for multi-scale graph analysis.

## Common Mistakes / Pitfalls

1. **Contracting $X$ instead of $X_r$:**  
   Naively contracting only $X$ fails to account for edges created in $G$ by the metric distortion $c$. This leads to tree decompositions of the lifted instance with treewidth exponentially worse than the bound in Lemma 2.5.

2. **Forgetting the Lipschitz constant $c$:**  
   The bound $O(\Delta c)$ is multiplicative in $c$. Poor choice of $G$ and $H$ (large $c$) makes the final algorithm slow. Must carefully construct auxiliary metrics to minimize $c$.

3. **Assuming planarity is preserved:**  
   Contraction preserves planarity, but other metric/geometric properties may not. If non-crossing columns are required (intersection graphs), contraction alone is insufficient—additional structural techniques (e.g., careful orientation, flow-based arguments) are needed.

4. **Ignoring the $2^{\text{poly}(