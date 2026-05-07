# BEST theorem

## Definition

The **BEST theorem** (de Bruijn, van Aardenne-Ehrenfest, Smith, and Tutte) is a fundamental result in graph theory that establishes a precise relationship between the number of Eulerian trails in a directed graph and the number of spanning arborescences rooted at a specific vertex.

**Formal statement:** For a directed graph $G = (V, E)$ with a distinguished root vertex $r$, the number of Eulerian trails starting from $r$ is given by:

$$z_T = t_r(G) \prod_{v \in V} (\delta^+(v) - 1)!$$

where:
- $z_T$ is the total number of Eulerian trails in $G$
- $t_r(G)$ is the number of spanning arborescences rooted at $r$ (out-arborescences)
- $\delta^+(v)$ is the out-degree of vertex $v$

**Existence condition:** A directed graph has an Eulerian trail if and only if:
1. For at most one vertex $u$: $\delta^+(u) - \delta^-(u) = 1$ (excess out-degree)
2. For at most one vertex $v$: $\delta^-(v) - \delta^+(v) = 1$ (excess in-degree)  
3. All other vertices satisfy $\delta^+(w) = \delta^-(w)$

## Key Equations

**BEST formula (expanded form):**
$$z_T = t_r(G) \prod_{v \in V \setminus \{r\}} (\delta^+(v) - 1)!$$

where $r$ is chosen appropriately based on degree conditions.

**Matrix-Tree Theorem connection:** The number of arborescences $t_r(G)$ can be computed in polynomial time via the Laplacian matrix:

$$t_r(G) = \text{cofactor of Laplacian matrix } L$$

where $L_{ij} = \begin{cases} \delta^+(i) & \text{if } i = j \\ -1 & \text{if } (i,j) \in E \\ 0 & \text{otherwise} \end{cases}$

## Physical Intuition / Derivation

The BEST theorem decomposes Eulerian trail counting into two tractable problems:

1. **Spanning arborescence constraint:** Any Eulerian trail must visit vertices in a way that respects a "tree backbone" structure. The arborescence $t_r(G)$ counts the number of such compatible tree structures rooted at the starting point.

2. **Local orderings:** At each vertex $v$ with out-degree $\delta^+(v)$, there are $(\delta^+(v) - 1)!$ ways to order the outgoing edges relative to the incoming edge used to reach $v$. This accounts for the combinatorial freedom in choosing which outgoing edge to take at each step, conditioned on respecting the arborescence structure.

**Why this factorization works:** Hierholzer's algorithm constructs Eulerian trails by decomposing them into cycles. The theorem shows that the count factors exactly into:
- The number of ways to build a "recursive structure" (arborescences)
- The number of ways to order local choices at each vertex (factorial terms)

This is why both factors are necessary: removing the arborescence term produces only the *potential* trail count; removing the factorial terms ignores the actual degrees of freedom in orderings.

## Applications in Engineering

### Bioinformatics / DNA Sequence Assembly
- **De Bruijn graphs:** Sequences are encoded as directed graphs where Eulerian paths represent DNA reads. The BEST theorem enables efficient counting of valid genomic reconstructions.
- **Shotgun sequencing:** Determines feasibility of assembling multiple sequences from overlapping fragments.

### Network Routing & Optimization
- **Postal delivery / Chinese Postman Problem:** Planning minimum-cost traversals that cover all edges exactly once (or minimally repeat edges).
- **VLSI circuit testing:** Generating test sequences that traverse all connections in integrated circuits.

### Data Privacy & Synthetic Data Generation
- **Directed graph sampling:** Generating random Eulerian trails for privacy-preserving data synthesis while preserving connectivity structure.
- **Markov chain analysis:** Counting equilibrium paths in state-transition systems.

### Combinatorial Enumeration
- **Optimal enumeration algorithms:** Computing $z_T$ in time $O(m + z_T)$ directly (as in Bals et al., improving naive $O(m \cdot z_T)$ bounds).
- **Counting de Bruijn sequences:** Applications to pseudorandom sequence generation in cryptography and communication systems.

## Common Mistakes / Pitfalls

1. **Confusing directed and undirected Eulerian conditions:** Undirected graphs require *all* vertices to have even degree for Eulerian cycles, while directed graphs require in-degree = out-degree. The BEST theorem only applies to directed graphs.

2. **Forgetting the arborescence root choice:** The BEST formula requires selecting $r$ carefully based on degree conditions (typically the excess-out-degree vertex if one exists). Different root choices can yield incorrect counts.

3. **Applying to disconnected components:** The theorem assumes *weakly connected* digraphs. Multi-component graphs require separate analysis of each component.

4. **Confusing trails with cycles:** Eulerian *trails* need not return to the starting vertex; *cycles* do. The BEST formula counts both, but the degree conditions differ.

5. **Over-complicating via arborescence enumeration:** Naive implementations enumerate $t_r(G)$ explicitly ($O(z_A \log^2 n)$ per earlier results), but direct enumeration of trails achieves $O(m + z_T)$ time by avoiding arborescence computation.

6. **Neglecting factorial terms:** Some applications focus only on $t_r(G)$ and forget the $\prod (\delta^+ - 1)!$ factor, leading to undercounting by exponential factors.

## See Also

- [[Eulerian path and circuit]]
- [[Spanning arborescence / out-arborescence]]
- [[Matrix-Tree Theorem / Kirchhoff's theorem]]
- [[De Bruijn graph]]
- [[Hierholzer