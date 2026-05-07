# quotient graph

## Definition

A **quotient graph** $G/P$ is a compressed representation of a graph $G = (V, E)$ with respect to a modular partition $P = \{M_1, M_2, \ldots, M_k\}$ of its vertices.

**Formal definition:**
- **Vertex set:** $V(G/P) = \{q_1, q_2, \ldots, q_k\}$, where each $q_i$ corresponds to module $M_i \in P$.
- **Edge set:** Two vertices $q_i$ and $q_j$ are adjacent in $G/P$ if and only if there exists at least one edge between a vertex in $M_i$ and a vertex in $M_j$ in the original graph $G$.

**Module:** A subset $M \subseteq V$ is a **module** if every vertex outside $M$ is either adjacent to all vertices in $M$ or to none of them (uniform external adjacency).

The quotient graph preserves inter-module connectivity information but discards intra-module edge structure, which is handled separately or recursively through modular decomposition.

## Key Equations

**Edge condition in quotient graph:**
$$q_i \sim q_j \text{ in } G/P \iff \exists u \in M_i, v \in M_j : (u,v) \in E(G)$$

**Modular partition property:**
$$V(G) = \bigcup_{i=1}^{k} M_i \quad \text{(disjoint union)}$$

**Modular width:** The maximum number of nodes across all quotient graphs in a complete modular decomposition tree:
$$\text{mw}(G) = \max \{|V(G/P_i)| : P_i \text{ is a modular partition in decomposition}\}$$

**Adjacency uniformity:** For module $M$ and vertex $v \notin M$:
$$\deg_M(v) \in \{0, |M|\}$$

## Physical Intuition / Derivation

### Why Quotient Graphs Matter

A quotient graph is fundamentally a **dimensionality reduction** tool for graph analysis. Consider a graph with internal structure: groups of vertices (modules) that behave identically with respect to the outside world.

**Intuitive example:** In a social network, suppose modules represent geographical regions. A quotient graph abstracts away internal community structure and shows only which regions are connected. This allows algorithms to work at the "region level" while still capturing essential connectivity.

### Modular Structure

The power of modularity lies in the **all-or-nothing principle**: 
- Within module $M_i$, vertices can have arbitrary internal connections
- Between modules $M_i$ and $M_j$, either:
  - **No edges exist** (isolated modules), or  
  - **All edge patterns are uniform** (every vertex in $M_i$ connects to the same subset in $M_j$)

This uniformity enables compression without information loss about inter-module relationships.

### Recursive Decomposition

The quotient graph doesn't lose information—it defers it:

$$G = \text{layers of abstraction}$$

1. Work with $G/P$ (macro view)
2. For each module $M_i$, recursively find a modular partition of the induced subgraph $G[M_i]$
3. Combine solutions recursively

This produces the **modular decomposition tree**, where quotient graphs appear at each level.

### Connection to Optimization

For graph problems like finding Maximum Average Degree (MAD) trees, quotient graphs enable powerful structural insights:

- A **poly-star** structure (at most one non-leaf per module) often suffices for optimality
- Vertices within the same module cannot both be internal nodes in the solution tree (except one per module)
- High-degree vertices in the root module become natural candidates for the solution

This dramatically reduces the search space from $2^n$ to polynomial.

## Applications in Engineering

### 1. **Network Clustering & Community Detection**
Quotient graphs model hierarchical community structure in large-scale networks (social networks, protein interaction graphs, autonomous systems). Engineers use them to detect and visualize nested communities without examining all-to-all connectivity.

### 2. **Circuit Design & Hierarchical Decomposition**
In digital circuit design, modules represent functional blocks (ALUs, cache, controllers). The quotient graph shows inter-block communication paths, enabling:
- Bandwidth optimization
- Latency analysis between blocks
- Layout planning

### 3. **Software Architecture Analysis**
Dependencies between software modules (packages/namespaces) form quotient graphs. Tools analyze:
- Cyclic dependencies between architectural components
- Coupling strength between subsystems
- Impact of code changes on module interfaces

### 4. **Transportation & Infrastructure Networks**
Cities/regions as modules; quotient graphs show traffic corridors and supply chain routes between regions. This enables:
- Congestion prediction
- Infrastructure bottleneck identification
- Route optimization at macro level

### 5. **Biological Networks**
Protein interaction networks or metabolic networks often decompose into functional modules (pathways, complexes). Quotient graphs enable:
- Understanding inter-pathway communication
- Identifying critical regulatory hubs between subsystems
- Reducing computational complexity for pathway analysis

### 6. **Graph Parameterized Algorithms**
Algorithms parameterized by modular width (like MAD tree computation) leverage quotient graphs for fixed-parameter tractability (FPT). This is crucial for **hard problems on restricted graph classes** where exact solutions are needed.

## Common Mistakes / Pitfalls

### 1. **Conflating Quotient Graphs with Module Decomposition**
**Mistake:** Thinking $G/P$ contains all information needed for the complete modular decomposition.
**Reality:** A single quotient graph $G/P$ only captures one level; full decomposition requires recursive analysis of $G[M_i]$ for each module. The quotient graph is a snapshot, not the tree.

### 2. **Losing Edge Information**
**Mistake:** Assuming that because $q_i \sim q_j$ in $G/P$, every vertex in $M_i$ connects to every vertex in $M_j$.
**Reality:** Only *at least one* edge must exist between the modules; the quotient graph cannot distinguish between sparse and dense