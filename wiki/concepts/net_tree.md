# net tree

## Definition

A **net tree** is a hierarchical data structure that organizes a finite metric space (or point set) into a laminar family of nets at successively finer scales. Formally, given a metric space $(X, d)$ and a sequence of scales $r_0 < r_1 < \cdots < r_h$, a net tree $T$ is a tree where:

1. **Nets form a laminar hierarchy**: At each level $i$, there exists a $r_i$-net $N_i \subseteq X$ (a maximal set of points with pairwise distances $\geq r_i$)
2. **Containment structure**: $N_h \subseteq N_{h-1} \subseteq \cdots \subseteq N_0 = X$ 
3. **Tree edges**: Each point in $N_i$ is connected to a point in $N_{i+1}$ (its parent), forming a tree structure
4. **Doubling metric applicability**: The tree depth is $O(\log n)$ in doubling metrics

The net tree naturally captures the hierarchical structure of metric spaces and enables efficient proximity queries through its tree organization.

## Key Equations

**Scale sequence** (for doubling metrics with doubling dimension $d$):
$$r_i = c \cdot \lambda^i$$
where $\lambda > 1$ is a scaling factor and $c$ is a base radius.

**Tree depth** (for doubling metrics):
$$h = O(\log_\lambda n)$$

**Lightness bound** (inherent limitation):
$$\text{lightness}(\text{spanner from net tree}) = \Omega(\log n)$$

The lightness $\ell$ of a spanner is the ratio of total edge weight to the minimum spanning tree weight:
$$\ell = \frac{w(\text{spanner})}{w(\text{MST})}$$

## Physical Intuition / Derivation

A net tree emerges naturally when hierarchically partitioning a metric space by scale:

1. **Bottom level** ($i=0$): All points form the finest net $N_0 = X$ at scale $r_0$ (near 0)
2. **Coarsening process**: At level $i$, select a maximal subset $N_i$ where any two points are distance $\geq r_i$ apart. This forces connectivity through the parent level.
3. **Spanner construction**: Connect each point to nearby points in its own level and to its ancestor in the parent level. This provides $(1+\varepsilon)$-distortion paths.

**Why lightness degrades ($\Omega(\log n)$)**:

Consider a path graph with unit-weight edges (Figure 1 from source). The net at scale $2^i$ selects vertices $\{v_j : j \bmod 2^i = 0\}$. To connect unselected vertices to the hierarchy, edges of length $|i - j|$ are added between levels. Since there are $n/2^i$ vertices at each level and $\log n$ levels, the total weight becomes $\sum_i (n/2^i) \cdot 2^i = \Theta(n \log n)$, yielding lightness $\Omega(\log n)$ against an MST of weight $n-1$.

## Applications in Engineering

### Dynamic Spanners in Computational Geometry
Net trees underpin classical fully-dynamic spanner algorithms for doubling metrics:
- **Insertion-only**: Amortized $O(\log n)$ update time (Roditty [Rod12])
- **Deletion operations**: Amortized $\tilde{O}(n^{1/3})$ time with $O(n/\varepsilon^d)$ edges
- **Constant-degree spanners**: Worst-case $\varepsilon^{-O(d)} \log n$ updates (Gottlieb & Roditty [GR08b])

### Proximity Data Structures
Net trees enable efficient:
- Approximate nearest neighbor queries
- Radius searches at multiple scales
- Metric space indexing for databases

### Machine Learning & High-Dimensional Data
- Hierarchical clustering of point sets
- Construction of cover trees for similarity search
- Fast approximate algorithms in doubling spaces

### Network Design
- Distributed network models can leverage net tree hierarchy for efficient routing
- Spanner-based network topologies with logarithmic stretch

## Common Mistakes / Pitfalls

1. **Confusing nets with nets in analysis**: A $r$-net is not a topological net; it is a maximal $r$-separated set. Every pair has distance $\geq r$, not $\leq r$.

2. **Assuming optimality for lightness**: Net tree spanners are not lightweight. The $\Omega(\log n)$ lightness lower bound is inherent and unavoidable for this construction. Modern work uses **locality-sensitive orderings** (LSO) instead for better lightness bounds.

3. **Ignoring doubling dimension dependence**: Update times like $\varepsilon^{-O(d)} \log^3 n$ have severe dependence on metric doubling dimension $d$, making them impractical in high dimensions.

4. **Tree reconstruction cost**: Deletions may require rebuilding subtrees. The amortized analysis hides worst-case $\Omega(n)$ costs in individual operations.

5. **Assuming universality across metrics**: Net tree constructions rely heavily on metric properties (doubling dimension). They do not extend to general graphs without significant modifications.

## See Also

- [[spanner|Geometric spanner]] — weighted subgraph preserving approximate distances
- [[doubling metric]] — metric spaces with controlled growth rate
- [[locality-sensitive ordering]] — improved alternative for lightweight spanners
- [[minimum spanning tree]] — baseline for measuring spanner quality via lightness
- [[dynamic data structures]] — framework for insertion/deletion algorithms

## Sources

- Abam et al. [AdBG08] — $O(\log n)$ dynamic spanner algorithm for Euclidean plane
- Roditty [Rod12] — First fully dynamic $(1+\varepsilon)$-spanner for doubling metrics with $O(\log n)$ insertion time
- Gottlieb & Roditty [GR08a], [GR