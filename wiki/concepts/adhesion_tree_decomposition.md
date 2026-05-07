# adhesion (tree decomposition)

## Definition

An **adhesion** of an edge $e \in E(T)$ in a tree decomposition $(T, \beta)$ is a separator induced by removing that edge. Specifically, it is the set of vertices that appear in bags on both sides of the decomposition tree after edge removal.

More formally: Given a tree decomposition $(T, \beta)$ where $T$ is a tree and $\beta: V(T) \to 2^{V(G)}$ assigns bags to nodes, the adhesion of edge $e = (t_1, t_2) \in E(T)$ is:

$$\text{Adhesion}(e) = \beta(t_1) \cap \beta(t_2)$$

This represents the "gluing interface" between two parts of the decomposed structure. In the context of planar graph decompositions, the adhesion often forms a separator that can be represented as a planar loop $\xi_S$ with interior and exterior regions.

## Key Equations

For a tree decomposition $(T, \beta)$ and edge $e \in E(T)$:

$$|E(T)| = |V(T)| - 1 \quad \text{(tree structure)}$$

$$\text{width}(T, \beta) = \max_{t \in V(T)} |\beta(t)| - 1$$

The **adhesion width** relates to tree-width:
$$\text{adhesion-width} \leq \text{tree-width} \leq \text{adhesion-width} + 1$$

For vertex counts in clean instances:
$$|V(G)| = O(L^4) \quad \text{(where } L \text{ is the number of terminals)}$$

## Physical Intuition / Derivation

### Geometric Interpretation

In planar graphs, an adhesion of edge $e$ corresponds to a **separator curve** that divides the plane into interior and exterior regions. This separator is formed by:
1. Two vertex-disjoint upward paths in a planar embedding
2. A closing edge connecting their endpoints

When we remove edge $e$ from the decomposition tree $T$, it splits into two connected components. The adhesion ensures that:
- All vertices in the interior of the loop $\xi_S$ are contained in bags from one component
- All vertices in the exterior belong to bags from the other component

### Why Adhesions Matter

Adhesions quantify how much information must pass between regions of a decomposition. A smaller adhesion means less communication between parts—this is crucial for:
- **Algorithm design**: separators enable divide-and-conquer strategies
- **Parameter bounds**: adhesion size constrains graph structure properties
- **Optimization problems**: small adhesions allow efficient dynamic programming

### Classification of "Bad Pairs"

When a pair $\sigma$ (typically representing a potential edge or vertex pair) creates a link $\gamma_\sigma$ that intersects the planar loop $\xi_S$, it becomes "bad." This occurs in exactly two cases:

1. **Separated pairs**: Endpoints of $\sigma$ lie on opposite sides of $\xi_S$
2. **Contaminating pairs**: At least one edge $e \in S$ satisfies $e \notin G_{\neg\sigma}$ (the pair "contaminates" the separator by depending on it)

**Claim 5.9** establishes this dichotomy: every bad pair falls into one of these categories because if endpoints are on the same side but the link intersects the loop, it must cross at least two edges of $S$—forcing contamination.

## Applications in Engineering

### Algorithm Design
- **Planar graph algorithms**: Tree decompositions with small adhesions enable linear-time exact algorithms for NP-hard problems via dynamic programming on the decomposition tree
- **Network routing**: Adhesions correspond to minimum cut separators; their size bounds routing complexity

### VLSI Circuit Design
- **Circuit partitioning**: Adhesions define cut sizes between circuit regions, directly relating to interconnect complexity and signal delay
- **Power distribution networks**: Separator sizes constrain physical metal layer requirements

### Computational Geometry
- **Mesh processing**: Tree decompositions of mesh graphs use adhesions to guide hierarchical refinement and coarsening
- **Planar subdivision**: Adhesions enable efficient point location and range query data structures

### Optimization & Operations Research
- **Integer programming**: Tree decompositions with controlled adhesion allow branch-and-bound algorithms with better complexity
- **Supply chain networks**: Adhesions identify critical bottleneck connections between network regions

## Common Mistakes / Pitfalls

1. **Confusing adhesion with bag size**: The adhesion (intersection of adjacent bags) is distinct from individual bag sizes. A tree decomposition can have large bags but small adhesions.

2. **Assuming adhesions are symmetric**: While adhesion$(e)$ is well-defined, the structure asymmetry in directed graphs or rooted trees means adhesions behave differently depending on orientation.

3. **Treating all small adhesions equally**: Not all small adhesions enable efficient algorithms—the *decomposition tree structure* (depth, balance) matters equally. A long, thin decomposition tree can be harder to exploit than a balanced one even with identical adhesions.

4. **Ignoring planar embedding dependency**: In planar graph decompositions, the adhesion loop $\xi_S$ is embedding-specific. Topological properties (interior/exterior) only make sense with respect to a fixed planar embedding.

5. **Overcounting separator crossings**: When analyzing contamination, it's easy to miscount how many edges of $S$ a link $\gamma_\sigma$ intersects. The claim that at most one crossing can be the "closing edge" requires careful geometric reasoning.

## See Also

- [[tree decomposition]] — parent concept defining the overall structure
- [[tree-width]] — measure of decomposition quality using bag sizes
- [[planar separator theorem]] — classical result on planar graph cuts
- [[dynamic programming on tree decompositions]] — algorithmic application exploiting adhesion structure
- [[vertex separator]] — related concept in graph partitioning

## Sources

- Lecture/paper excerpt on tree decomposition of planar graphs (Theorem 3.5 context)
- Claim 5.9: Classification of bad pairs with respect to separators
- Claim 5.10: Vertex count bounds for clean instances
- Discussion of easily-coverable spanning trees and path-based constructions