# Butterfly Counting

## Definition

**Butterfly counting** is the problem of enumerating or approximating the number of **butterflies** (also called 2×2 bicliques) in a bipartite graph. A butterfly is the smallest non-trivial biclique structure: a subgraph comprising four distinct vertices arranged in two parts of the bipartition, where both vertices in one part connect to both vertices in the other part.

Formally, in a bipartite graph $G = (U \cup V, E)$, a butterfly is a 4-tuple of vertices $(u_1, u_2, v_1, v_2)$ where $u_1, u_2 \in U$, $v_1, v_2 \in V$, and all four edges $\{(u_1, v_1), (u_1, v_2), (u_2, v_1), (u_2, v_2)\}$ exist in $E$.

The butterfly counting problem seeks to compute:
$$B = \text{total count of all butterflies in } G$$

## Key Equations

### Butterfly Count via Edge Pairs
For any two edges $e_1 = (u, v_1)$ and $e_2 = (u, v_2)$ sharing a common vertex $u$ in one bipartition, they form the "top" of a butterfly. The number of butterflies they participate in equals the number of common neighbors in the other partition:

$$B = \sum_{u \in U} \binom{d_u}{2} \cdot (\text{common neighbor pairs from } V)$$

More generally, butterflies can be counted by summing over all **wedges** (paths of length 2):
$$B = \sum_{w \in \text{wedges}} |N(w)|$$
where $N(w)$ is the set of vertices closing the wedge into butterflies.

### Heavy-Light Partition
The algorithm partitions edges into heavy ($P_H$) and light ($P_L$) edges based on a degree threshold $\tau = \bar{b}^{3/4}/\varepsilon^{1/4}$:

$$P_H = \{e \in E : b(e) \geq \tau\}, \quad P_L = E \setminus P_H$$

where $b(e)$ denotes the number of butterflies containing edge $e$.

### Weighted Butterfly Scheme
To avoid double-counting while focusing computational effort on light edges, assign weights to butterflies:

$$\text{wt}_{P_L}(\text{butterfly}) = \begin{cases} 0 & \text{if no edges in } P_L \\ \frac{1}{l} & \text{if } l > 0 \text{ edges in } P_L \end{cases}$$

Edge weight: 
$$\text{wt}_{P_L}(e) = \sum_{e \in \text{butterfly}} \text{wt}_{P_L}(\text{butterfly}), \quad e \in P_L$$

The sum of all edge weights equals the count of butterflies intersecting $P_L$.

## Physical Intuition / Derivation

### Why Butterflies Matter
Butterflies represent the minimal dense local structure in bipartite networks. In real applications (user-item graphs, author-publication networks), butterflies indicate **clusters of tightly related entities**. Counting them reveals community structure and network density anomalies.

### The Sublinear Challenge
Traditional butterfly counting requires examining most/all edges, costing $O(|E|)$ or $O(|E| \cdot \sqrt{|E|})$ time. For massive graphs (billions of edges), this is prohibitive. The key insight: we can **estimate** $B$ by:

1. **Sampling** small subsets of edges and vertices
2. **Scaling up** via appropriate importance weighting
3. **Controlling variance** by distinguishing high-butterfly-count ("heavy") edges from low-count ("light") edges

### Two-Level Sampling (TLS) Intuition
The algorithm operates in two stages:

**Stage 1: Edge Sampling (Top Level)**
- Sample edges uniformly at random
- For each sampled edge, determine if it's heavy or light
- Heavy edges are mostly queried; light edges are sampled more carefully

**Stage 2: Wedge Sampling (Bottom Level)**
- For sampled edges, enumerate wedges (length-2 paths)
- Sample among wedges to close them into butterflies
- Weight samples inversely by sampling probability to correct bias

**Heavy-Light Partition Principle**: 
Heavy edges (those in many butterflies) can be handled exhaustively via queries. Light edges are rare individually but numerous collectively—sampling them efficiently avoids redundant computation.

### Variance Control via "Small-Degree-First"
When sampling wedges, prioritize vertices with small degree. A wedge $(u, v, w)$ through vertex $v$ can be completed by checking common neighbors. If $v$ has degree $d_v$, we sample $O(d_v^{\alpha})$ neighbors and scale, reducing variance compared to uniform sampling.

## Applications in Engineering

### 1. **Social Network Analysis**
Butterflies in user-follower graphs detect **mutual interest clusters**: groups where two users follow the same two accounts. Approximating butterfly counts reveals trending topics or influencer networks without scanning the entire graph.

### 2. **E-Commerce & Recommendation**
In customer-product bipartite graphs, butterflies indicate **co-purchase patterns**. Two customers buying the same two products signal product affinity. Fast butterfly estimates help recommend bundles or detect fraudulent behavior (coordinated fake purchases).

### 3. **Biological Network Analysis**
In protein-interaction or gene-regulatory bipartite networks, butterflies model **conserved regulatory modules**. Counting butterflies identifies functional subnetworks without exhaustive enumeration.

### 4. **Web Graph Mining**
In hyperlink graphs (bipartite: pages × domains), butterfly density reveals **reciprocal linking patterns** and potential SEO manipulation. Sublinear approximation enables real-time anomaly detection.

### 5. **Database Query Optimization**
In schema graphs (entities × attributes), butterflies represent correlated attribute groups. Approximate butterfly counting informs index design and query planning.

## Common Mistakes / Pitfalls

### 1. **