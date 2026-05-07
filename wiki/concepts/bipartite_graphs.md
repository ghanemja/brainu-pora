# Bipartite Graphs

## Definition

A **bipartite graph** is an undirected graph $G = (U \cup V, E)$ where the vertex set can be partitioned into two disjoint sets $U$ and $V$ such that every edge in $E$ connects a vertex in $U$ to a vertex in $V$. No edges exist between vertices within the same partition.

Formally, for all edges $(u, v) \in E$: either $u \in U, v \in V$ or $u \in V, v \in U$.

### Related Structure: Bicliques

A **biclique** (complete bipartite subgraph) $K_{m,n}$ is a bipartite graph where every vertex in one partition is connected to every vertex in the other. A **butterfly** (or **2×2 biclique**, denoted $K_{2,2}$) is the minimal non-trivial biclique: four vertices arranged as two pairs, with all four possible cross-partition edges present.

Formally, a butterfly consists of two edges $(u_1, v_1)$ and $(u_2, v_2)$ that share a common vertex, plus the two additional edges $(u_1, v_2)$ and $(u_2, v_1)$.

## Key Equations

### Butterfly Definition (Graph-Theoretic)

A butterfly exists for vertices $u_1, u_2 \in U$ and $v_1, v_2 \in V$ when:
$$\{(u_1, v_1), (u_1, v_2), (u_2, v_1), (u_2, v_2)\} \subseteq E$$

This can be counted via **wedge closure**: for each edge $e = (u, v)$, count pairs of common neighbors. If $u$ has degree $d_u$ and $v$ has degree $d_v$, the number of wedges (2-paths) centered at $e$ is:
$$\text{wedges}(e) = (d_u - 1) + (d_v - 1)$$

The number of butterflies containing edge $e$ is the number of pairs of common neighbors:
$$b(e) = \binom{|N(u) \cap N(v)|}{2}$$

where $N(u)$ denotes the neighborhood of $u$.

### Weighted Butterfly Counting

For a partition of edges $(P_H, P_L)$ into "heavy" and "light" edges, the weight assigned to butterflies intersecting $P_L$ is:

$$w_{P_L}(\text{⊲⊳}) = \begin{cases} 0 & \text{if butterfly contains no edges in } P_L \\ \frac{1}{l} & \text{if butterfly contains } l > 0 \text{ edges in } P_L \end{cases}$$

where weights are equally distributed across light edges in the butterfly.

The total weight of an edge $e \in P_L$:
$$w_{P_L}(e) = \sum_{e \in \text{⊲⊳}} w_{P_L}(\text{⊲⊳})$$

This ensures: $\sum_{e \in P_L} w_{P_L}(e) = $ number of butterflies intersecting $P_L$.

## Physical Intuition / Derivation

### Why Bipartite Graphs?

Bipartite graphs naturally model **heterogeneous relationships** between two distinct entity types:
- Authors ↔ Papers (in citation networks)
- Users ↔ Items (in recommender systems)
- Proteins ↔ Genes (in biological networks)
- Web pages ↔ Terms (in information retrieval)

The key advantage is structural clarity: no edges within a type, only across types.

### Why Butterflies Matter

Butterflies represent the simplest **non-trivial dense structures** in bipartite graphs. They signal:
- **Clustering**: Two users who interact with the same pair of items
- **Anomalies**: Potentially coordinated behavior in social networks
- **Community cohesion**: Mutual reinforcement in heterogeneous networks

Counting butterflies is a proxy for network density without the computational cost of enumerating all cliques (which is NP-hard in general graphs).

### Heavy-Light Partition Intuition

The algorithm partitions edges by degree threshold $\bar{b}^{3/4}/\varepsilon^{1/4}$:

- **Heavy edges** ($e$): High-degree endpoints → appear in many butterflies → sample with high probability
- **Light edges** ($e$): Low-degree endpoints → rare → sample with lower probability, but controllable variance

This partition minimizes query complexity because high-degree vertices contain most structural information, while low-degree vertices require careful handling via variance-reduction techniques.

## Applications in Engineering

### 1. Recommender Systems
In user-item bipartite graphs, butterflies indicate groups of users with overlapping preferences. Algorithms can use butterfly density to identify niche communities or recommend items to similar users without explicit similarity computation.

### 2. Anomaly Detection in Networks
In financial transaction networks (customers ↔ merchants), butterfly abundance may signal:
- Money laundering rings (sudden clusters of cross-transactions)
- Coordinated fraud (multiple customers interacting with multiple merchants in loops)

Sublinear approximate counting enables real-time monitoring of graph streams.

### 3. Social Network Analysis
In follower networks (users ↔ hashtags or users ↔ pages), butterflies represent:
- Co-trending topics
- Coordinated information propagation
- Bot-like behavior (artificial symmetry in mutual interactions)

### 4. Biological Networks
In protein-gene interaction graphs, butterflies may represent:
- Gene regulatory modules
- Pathway interactions
- Disease-associated network motifs

### 5. Large-Scale Graph Processing
Query-based algorithms (degree query, neighbor query, vertex-pair query) are critical when:
- Graph is stored remotely and network I/O is expensive
- Graph is dynamic and only recent snapshots are accessible
- Graph is too large to fit in memory

The TLS algorithm achieves $\widetilde{O}(\bar{b}^{3/4}/\varepsilon^{1/4})$ query complexity instead of $O(