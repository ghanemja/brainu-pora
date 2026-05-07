# minor-closed graph class

## Definition

A **minor-closed graph class** $\mathcal{G}$ is a family of graphs closed under the operation of taking minors. That is, if $G \in \mathcal{G}$ and $H$ is a minor of $G$, then $H \in \mathcal{G}$.

A graph $H$ is a **minor** of graph $G$ if $H$ can be obtained from $G$ by a sequence of the following operations:
1. **Vertex deletion**: remove a vertex (and all incident edges)
2. **Edge deletion**: remove an edge
3. **Edge contraction**: merge two adjacent vertices into a single vertex, redirecting all incident edges

Equivalently, $H$ is a minor of $G$ if there exists an injective function $\phi$ mapping vertices of $H$ to connected subgraphs of $G$ such that edges of $H$ correspond to edges connecting these subgraphs in $G$.

## Key Equations

For a proper minor-closed graph class $\mathcal{G}$, the **$\varepsilon$-semi-ladder index** (also called **$\varepsilon$-scatter dimension**) is bounded by:

$$\text{semi-ladder index}(\mathcal{G}, \varepsilon) \leq 2^{2^{\text{poly}_{\mathcal{G}}(1/\varepsilon)}}$$

where $\text{poly}_{\mathcal{G}}(1/\varepsilon)$ denotes a polynomial that depends on the specific graph class $\mathcal{G}$.

For metrics induced by edge-weighted graphs from $\mathcal{G}$:
$$|\text{ε-semi-ladder}| \leq 2^{\text{poly}_{\mathcal{G}}(1/\varepsilon)}$$

## Physical Intuition / Derivation

### Why Minor-Closure Matters

The concept of minor-closure captures a fundamental structural property: graphs in $\mathcal{G}$ cannot contain arbitrarily large "forbidden structures." By Wagner's theorem, a graph is **planar if and only if it contains neither $K_5$ nor $K_{3,3}$ as minors**—planar graphs form a minor-closed class.

### Hierarchical Sparsity

Minor-closed classes exhibit **structural sparsity**: they exclude large dense subgraphs. This has profound consequences:
- **Degeneracy bounds**: graphs in proper minor-closed classes have bounded degeneracy
- **Treewidth limitations**: planar graphs have $O(\sqrt{n})$ treewidth
- **Separator theorems**: planar graphs admit small vertex separators

### Connection to Metric Embedding

When a graph from $\mathcal{G}$ is weighted (edge weights represent distances), the minor-closure property constrains how "spread out" points can be. The $\varepsilon$-semi-ladder index measures how many points must be "sufficiently distant" from others, and minor-closure bounds this quantity.

The key insight from Bourneuf and Pilipczuk: the structural tools developed for analyzing sparse graph decompositions (treewidth, pathwidth decompositions) transfer directly to metric settings, providing polynomial (albeit exponential in $1/\varepsilon$) bounds on ladder indices.

## Applications in Engineering

### 1. **Geometric Data Structures & Coresets**
For planar maps and metric spaces induced by planar graphs, minor-closed properties enable construction of **furthest-neighbor coresets**—sparse point sets that approximate distances for all query points. Critical for:
- Geographic information systems (GIS)
- Mobile robotics path planning
- Sensor network deployment

### 2. **Algorithm Design on Sparse Graphs**
Minor-closed graph classes admit **parameterized algorithms** with runtime:
$$T(n) = f(k) \cdot n^{O(1)}$$
where $k$ depends on the excluded minor.

Applications:
- VLSI circuit routing (planar graphs)
- Network design on surfaces
- Social network analysis (sparse real-world graphs often have bounded treewidth)

### 3. **Approximation Algorithms**
Many NP-hard problems admit constant-factor approximations on minor-closed classes:
- Feedback vertex set on planar graphs: $O(1)$-approximation
- Dominating set: approximation schemes (PTAS) on bounded-genus graphs

### 4. **Network Optimization**
Wireless network design exploits planarity to develop efficient scheduling and resource allocation algorithms.

## Common Mistakes / Pitfalls

### Mistake 1: Confusing Planarity with Minor-Closure
**Wrong:** "A graph is minor-closed if it's planar."
**Correct:** Planar graphs form *one example* of a minor-closed class. So do all graphs embeddable on a fixed surface, bounded-treewidth graphs, and smaller classes.

### Mistake 2: Underestimating the Exponential Bound
**Wrong:** "Minor-closed classes guarantee polynomial bounds on ladder indices."
**Correct:** Bounds are $2^{\text{poly}(1/\varepsilon)}$—doubly exponential in $1/\varepsilon$. For $\varepsilon = 0.01$, this is astronomically large. The greedy coreset approach is impractical; Sokołowski showed $2^{\Omega(1/\varepsilon)}$ lower bounds are tight.

### Mistake 3: Assuming Closure Under All Operations
**Wrong:** "If a class is minor-closed, it's also closed under taking subgraphs."
**Correct:** Minor-closure $\Rightarrow$ subgraph-closure (always), but not conversely. Minor-closure is much more restrictive.

### Mistake 4: Ignoring Edge Weights
The results on metric embeddings critically depend on how edges are weighted. Unweighted graphs behave differently—the distance metric must be compatible with the graph structure.

## See Also

- [[graph minor theory]]
- [[treewidth and pathwidth]]
- [[metric embedding]]
- [[ε-coreset construction]]
- [[sparse graph classes]]
- [[degeneracy]]

## Sources

- Bourneuf & Pilipczuk (referenced as [9]): First systematic connection between graph-theoretic sparsity and metric