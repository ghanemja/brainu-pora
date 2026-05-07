# induced subgraph

## Definition

An **induced subgraph** of a graph $G = (V, E)$ is a graph $H = (V', E')$ where:
- $V' \subseteq V$ is a subset of vertices
- $E' = \{(u,v) \in E : u, v \in V'\}$ contains all edges from $G$ whose endpoints are both in $V'$

In other words, $H$ is formed by selecting a subset of vertices from $G$ and including *every* edge between those vertices that existed in the original graph. This distinguishes it from a **subgraph**, which may include only some of the edges.

**Notation:** We write $H \subseteq_{\text{ind}} G$ to denote that $H$ is an induced subgraph of $G$.

## Key Equations

For a graph $G = (V,E)$ and vertex subset $V' \subseteq V$:

$$H = G[V'] = (V', E[V'])$$

where $E[V'] = \{(u,v) \in E : u,v \in V'\}$ is the edge set induced by $V'$.

The number of possible induced subgraphs of a graph with $n$ vertices is at most $2^n$ (one for each subset of vertices), though many may be isomorphic.

## Physical Intuition / Derivation

The induced subgraph captures the idea of **examining a local neighborhood or subset** while preserving all the relational structure within that subset. Think of it as:

- **Zooming in** on a portion of a network and asking: "What does the structure look like if I only consider these nodes and all their mutual connections?"
- **Removing nodes** from a graph and automatically losing only edges touching those removed nodes—edges between remaining nodes must stay.

This is fundamentally different from selecting arbitrary edges: if you keep vertices $\{A, B, C\}$ from a larger graph and they form a triangle in the original, that triangle *must* appear in the induced subgraph. You cannot "break" the triangle by selectively excluding edges.

**Why it matters:** Induced subgraphs are essential for pattern detection. When we ask "does $G$ contain $H$ as an induced subgraph?" we are asking whether $G$ has a configuration that matches $H$ exactly—not just topologically similar, but with no extra or missing edges.

## Applications in Engineering

### 1. **Graph Modification Problems (Computational Complexity)**
In the H-free subdivision problem cited in the sources, the goal is to eliminate all induced copies of some "forbidden" graph $H$ from a graph $G$ by modifying edges (subdividing them). This is crucial for:
- **Network design**: Ensuring a network avoids certain problematic substructures (e.g., feedback loops, cycles of specific types)
- **Complexity analysis**: Determining tractability of graph editing operations depending on which induced subgraphs are prohibited

### 2. **Pattern Recognition in Networks**
- **Social networks**: Detecting communities or anomalous interaction patterns (triangles, stars, complete bipartite subgraphs)
- **Biological networks**: Finding motifs in protein interaction networks or gene regulatory networks
- **Circuit design**: Identifying hazardous circuit topologies

### 3. **Streaming and Distributed Algorithms**
The node sampling approach described in the sources uses induced subgraphs to:
- **Estimate subgraph counts** (e.g., four-cycles) in graphs too large to store fully
- **Maintain compressed representations** of graphs for analysis in limited space ($O(m/\sqrt{T})$ space for sparse graphs)

### 4. **Database Query Optimization**
Graph induced subgraph matching is fundamental to:
- **RDF/semantic web queries**: Finding entities and their relationships matching a pattern
- **Knowledge graph querying**: Retrieving subgraph matches efficiently

## Common Mistakes / Pitfalls

### Mistake 1: Confusing "Subgraph" with "Induced Subgraph"
A student might think any subset of edges preserving endpoints gives an induced subgraph. **Wrong.** An induced subgraph is determined *solely* by the vertex subset—all qualifying edges are automatically included. If vertices $\{u,v\}$ appear in the induced subgraph and $(u,v) \in E(G)$, then $(u,v)$ *must* be in the induced subgraph.

### Mistake 2: Treating Induced Subgraph Matching as Graph Isomorphism
Finding whether $H$ appears as an induced subgraph of $G$ is NP-complete in general (even for small fixed $H$). Students sometimes assume this is "just like checking graph isomorphism"—it's actually harder in practice because the vertex correspondence is not given.

### Mistake 3: Underestimating Combinatorial Explosion
With $n$ vertices, there are $2^n$ possible induced subgraphs. For $n=20$, that's over a million. Many algorithms attempting exhaustive induced subgraph enumeration become infeasible quickly.

### Mistake 4: Ignoring Problem-Specific Structure
In hardness proofs (like those in the sources), the complexity of detecting induced subgraph problems depends *critically* on the structure of $H$ (its degree sequence, girth, triangles, etc.). Assuming uniform hardness across all forbidden graphs is incorrect.

## See Also

- [[subgraph]] — contrast: subgraphs may exclude edges; induced subgraphs cannot
- [[graph homomorphism]] — related abstraction allowing vertex mappings that are not injective
- [[motif]] — informal term for frequent induced subgraph patterns in biological/social networks
- [[NP-completeness]] — computational hardness of induced subgraph detection
- [[vertex separator]] — uses induced subgraph structure to decompose graphs

## Sources

- "On the complexity of edge subdivision to $H$-free graphs" — hardness results for eliminating induced subgraphs via edge modification
- Streaming/sampling algorithms for subgraph counting — induced subgraph approach for large-scale graph analysis under space constraints