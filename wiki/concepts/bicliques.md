# bicliques

## Definition

A **biclique** is a complete bipartite subgraph in which every vertex in one partition is connected to every vertex in the other partition. An $m \times n$ **biclique** $K_{m,n}$ consists of two disjoint vertex sets $U$ and $V$ with $|U| = m$ and $|V| = n$, where every vertex in $U$ is adjacent to every vertex in $V$, and there are no edges within $U$ or within $V$.

The special case of a **butterfly** (also called a **2×2 biclique** or $K_{2,2}$) is particularly important in network analysis: it consists of exactly four vertices arranged as two pairs, where all four possible edges between the pairs exist. In bipartite graph $G = (A \cup B, E)$, a butterfly is formed by selecting two vertices $u_1, u_2 \in A$ and two vertices $v_1, v_2 \in B$ such that edges $(u_1, v_1), (u_1, v_2), (u_2, v_1), (u_2, v_2)$ all exist.

## Key Equations

For a bipartite graph $G = (A \cup B, E)$ with edge set $E$, the total butterfly count is:

$$b = \sum_{e = (u,v) \in E} \binom{d_A(u) - 1}{1} \cdot \binom{d_B(v) - 1}{1}$$

where $d_A(u)$ is the degree of vertex $u$ in partition $A$ and $d_B(v)$ is the degree of vertex $v$ in partition $B$.

Equivalently, the count of butterflies containing edge $e = (u,v)$ is:

$$b(e) = (d_A(u) - 1)(d_B(v) - 1)$$

For weighted butterfly counting with light edges $P_L \subseteq E$, the weight assignment for a butterfly $\bowtie$ containing $l > 0$ edges from $P_L$ is:

$$\text{wt}_{P_L}(\bowtie) = \frac{1}{l}$$

The total weighted count equals the number of butterflies intersecting $P_L$:

$$\sum_{\bowtie: \bowtie \cap P_L \neq \emptyset} \text{wt}_{P_L}(\bowtie) = |\{\bowtie : \bowtie \cap P_L \neq \emptyset\}|$$

## Physical Intuition / Derivation

**Why butterflies matter:** In bipartite networks (e.g., user-item networks, paper-author networks, query-document networks), butterflies represent a fundamental structural motif. A butterfly indicates that two users have similar preferences (both connected to the same two items), or two papers share two common authors. This makes butterflies a natural measure of local clustering and redundancy in bipartite systems.

**Why the degree formula works:** For any edge $e = (u, v)$, the number of butterflies containing $e$ equals the number of ways to choose a second neighbor from $u$ and a second neighbor from $v$. Since $u$ has $d_A(u)$ neighbors total (including $v$), there are $(d_A(u) - 1)$ choices for the second neighbor in partition $A$. Similarly, $v$ has $(d_B(v) - 1)$ choices. This gives the product $(d_A(u) - 1)(d_B(v) - 1)$.

**Heavy-light partition intuition:** The TLS algorithm partitions edges into "heavy" edges (high-degree endpoints) and "light" edges (low-degree endpoints) using the threshold $\bar{b}^{3/4}/\varepsilon^{1/4}$. This separation is crucial because:
- Heavy edges tend to appear in many butterflies, so systematic sampling is efficient
- Light edges are rare, so we can afford to examine more of them
- Most butterflies contain at least one light edge, allowing variance reduction through weighted sampling

## Applications in Engineering

### Network Analysis
- **Similarity detection**: Identifying groups of similar users or items in recommendation systems; butterflies indicate users with overlapping preferences
- **Anomaly detection**: Unusual clustering patterns in bipartite networks may indicate fraudulent or bot-like behavior
- **Data quality assessment**: Measuring redundancy in knowledge graphs or database schemas

### Distributed Systems
- **Query optimization**: Counting common attributes in distributed databases; butterflies represent queries touching multiple shared entities
- **Cache efficiency**: Identifying frequently co-accessed resource pairs to optimize memory hierarchies

### Bioinformatics
- **Protein-protein interaction networks**: Counting butterfly motifs in bipartite networks of proteins and their functions
- **Disease-gene association**: Finding genes associated with multiple diseases or diseases linked to multiple genes

### Information Retrieval
- **Web graph analysis**: Modeling bipartite relationships between pages and domains; butterflies reveal content similarity
- **Document clustering**: Identifying tightly coupled documents through shared keywords or citations

## Common Mistakes / Pitfalls

1. **Confusing general bicliques with butterflies**: A butterfly is specifically $K_{2,2}$. Generalizations to $K_{m,n}$ with $m, n > 2$ are distinct structures with different counting algorithms.

2. **Ignoring the partition structure**: Butterflies only exist in bipartite graphs where we distinguish between two vertex classes. Applying butterfly-counting to general graphs without proper bipartition is meaningless.

3. **Neglecting the $(d_A(u) - 1)$ subtraction**: A common error is computing $d_A(u) \cdot d_B(v)$ instead of $(d_A(u) - 1)(d_B(v) - 1)$. The subtraction is essential because we condition on the edge $(u,v)$ itself already existing.

4. **Misinterpreting heavy-light partition thresholds**: The threshold $\bar{b}^{3/4}/\varepsilon^{1/4}$ is not arbitrary; it balances the variance contributions from different edge classes. Using a different threshold breaks theoretical guarantees.

5. **Overestimating sample size**: