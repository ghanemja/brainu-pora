# Bounded Genus Graphs

## Definition

A **bounded genus graph** is a graph that can be embedded in a closed orientable surface of genus $g$, where $g$ is a fixed (bounded) integer. Equivalently, these are graphs embeddable on a surface with at most $g$ "handles."

More formally: A graph $G = (V, E)$ has **Euler genus** at most $g$ if it admits a 2-cell embedding in a closed orientable surface with genus $g$, where:
- The **Euler characteristic** satisfies: $\chi = 2 - 2g = |V| - |E| + |F|$
- $|V|$ = number of vertices, $|E|$ = number of edges, $|F|$ = number of faces

**Key constraint:** For bounded genus graphs, the topological structure is fixed—the genus $g$ does not depend on the problem size $n = |V|$.

### Special Cases
- **$g = 0$**: Planar graphs (embeddable on a sphere)
- **$g = 1$**: Toroidal graphs (embeddable on a torus)
- **General $g \geq 0$**: Surfaces with $g$ handles

## Key Equations

For a metric space $(V, \text{dist})$ induced by a graph embedded on a surface of Euler genus at most $g$:

$$\text{ε-comatching index} \leq O(g^4 \varepsilon^{-8}) \cdot L_{\text{planar}}(1/\varepsilon)$$

where $L_{\text{planar}}(1/\varepsilon)$ is the bound for planar graphs (see Theorem 1.5 from source).

### $d$-comatching Definition (Unweighted Graphs)

A family $\mathcal{M}$ of vertex pairs is a **$d$-comatching** if:

1. **Separation condition:** $\forall (p,q) \in \mathcal{M}$, $\quad \text{dist}(p,q) > d$
2. **Domination condition:** $\forall$ distinct $(p,q), (p',q') \in \mathcal{M}$, $\quad \text{dist}(p,q') \leq d$

An $\varepsilon$-comatching generalizes this by replacing the distance threshold $d$ with $\varepsilon \cdot \text{diam}(V)$.

## Physical Intuition / Derivation

### Why Genus Matters

**Topological "compressibility":** The genus quantifies how "far" a graph is from being planar. Planar graphs have exceptional algorithmic properties because they have low separator structure. Bounded genus graphs preserve this property approximately:

- **Planar graphs ($g=0$)**: Can be cut into pieces by removing $O(1)$ vertices or edges
- **Bounded genus ($g$ fixed)**: Can be cut by removing $O(\sqrt{g})$ vertices, or decomposing along $O(g)$ shortest paths (surface reduction technique)

### Surface Cutting Technique

The proof of bounds for bounded genus graphs follows this strategy:

1. **Cut the surface** along $O(g)$ shortest paths and individual edges
2. **Reduce to planar case**: Each piece after cutting becomes planar
3. **Compose bounds**: Use results from planar metrics, weighted by the complexity of the cutting structure

This explains the polynomial dependence: $O(g^4 \varepsilon^{-8}) \times L_{\text{planar}}(1/\varepsilon)$

### Coreset Interpretation

For applications like **$k$-center** and **furthest neighbor queries**, a bounded genus graph of genus $g$ has coreset size:

$$\text{Coreset size} = \text{poly}(g) \cdot (1/\varepsilon)^{2^{O(k)}} \quad \text{(for k-center)}$$

This shows that:
- Dependence on $g$ is polynomial (manageable for small fixed genus)
- Dependence on $\varepsilon$ and $k$ matches planar case, with polynomial factors in $g$

## Applications in Engineering

### 1. **Spatial Networks & Infrastructure**
- Road networks on surfaces with topological constraints (e.g., graphs embedded on terrain with tunnels/bridges)
- Network design where planarity doesn't hold but genus is small and fixed
- Example: logistics networks in mountainous regions with limited crossing points

### 2. **Clustered Data Processing**
- **$k$-center problems** on bounded-genus networks: facility location, wireless sensor coverage
- Computing approximate solutions with certified coreset sizes
- Significantly smaller certificates needed vs. general graphs (exponential savings for small $g$)

### 3. **Graph Algorithms & Approximation**
- Approximation schemes (PTAS) for optimization problems on bounded-genus graphs
- Parameterized complexity: $O(g^c)$ factors often preferable to dependence on $n$
- Coreset-based streaming algorithms for distributed computation

### 4. **Computational Topology**
- Persistent homology computation on embedded graphs
- Fundamental domain extraction and geodesic distance queries
- Surface reconstruction algorithms with bounded topological complexity

### 5. **Minor-Closed Graph Classes**
- Bounded genus is part of the **H-minor-free** hierarchy
- Results here inform broader results for minor-closed families
- Treewidth-bounded graphs ($\text{tw} \leq c$) are more general; bounded genus provides a geometric interpretation

## Common Mistakes / Pitfalls

### 1. **Confusing Genus and Treewidth**
- **Mistake:** Assuming bounded genus = bounded treewidth
- **Reality:** A graph of genus $g$ can have treewidth $\Theta(\sqrt{g} \cdot \sqrt{n})$ in the worst case
- **Why it matters:** Treewidth-based algorithms may not directly apply; genus-specific structure must be exploited

### 2. **Ignoring the Polynomial Factor in $g$**
- **Mistake:** Treating $\text{poly}(g)$ as negligible
- **Reality:** For $g$ even moderately large