# Two-Level Sampling Algorithm

## Definition

A **two-level sampling algorithm** is a variance-reduction technique for approximate counting problems in large graphs, particularly suited to scenarios where full graph access is prohibitively expensive. The algorithm operates under a **query model** (degree query, neighbor query, vertex-pair query) and uses hierarchical partitioning to stratify the problem into tractable subproblems.

In the context of butterfly counting (2×2 bicliques in bipartite graphs), the two-level structure refers to:

1. **First level**: Partition edges into "heavy" ($P_H$) and "light" ($P_L$) subsets based on a threshold determined by degree statistics
2. **Second level**: Apply differentiated sampling strategies to each partition, with importance weighting to reconstruct the global count

The algorithm estimates the total butterfly count $b$ by:
$$\hat{b} = \text{EstimateHeavy}(P_H) + \text{EstimateLight}(P_L)$$

where each term uses appropriate sampling and reweighting.

## Key Equations

### Heavy-Light Partition Threshold

Given target approximation parameter $\varepsilon$, define threshold:
$$\tau = \frac{\bar{b}^{3/4}}{\varepsilon^{1/4}}$$

An edge $e$ is classified as:
- **Heavy** ($e \in P_H$): if $b(e) \geq \tau$ (butterflies containing $e$)
- **Light** ($e \in P_L$): if $b(e) < \tau$

### Butterfly Weight Assignment (Partition-based)

For a butterfly $\bowtie$ intersecting light edges $P_L$:

$$w_{P_L}(\bowtie) = \begin{cases}
0 & \text{if } \bowtie \cap P_L = \emptyset \\
\frac{1}{l} & \text{if } \bowtie \text{ contains } l > 0 \text{ edges in } P_L
\end{cases}$$

For edge $e \in P_L$:
$$w_{P_L}(e) = \sum_{e \in \bowtie} w_{P_L}(\bowtie)$$

The total butterfly weight equals butterflies intersecting $P_L$:
$$B_{intersect} = \sum_{e \in P_L} w_{P_L}(e)$$

### Approximation Guarantee

The algorithm achieves **(1+ε)-approximation** with failure probability $\delta$ when:

$$\text{samples} \geq \frac{\bar{b}^{3/4}}{\varepsilon^{1/4}} \quad \text{or} \quad d_e > \frac{\bar{w}}{\varepsilon \bar{b}^{1/4}}$$

where $\bar{b}$ is average butterfly count and $\bar{w}$ is average wedge count.

## Physical Intuition / Derivation

### Why Two Levels?

Traditional single-pass sampling over all edges suffers from **high variance** when:
- Some edges participate in very few butterflies (add noise)
- Most butterflies concentrate in sparse regions (undersampled)

**Solution via stratification**: Treat high-contribution and low-contribution edges separately.

### Heavy Partition Strategy

Heavy edges ($b(e) \geq \tau$) are **deterministic or lightly sampled** because:
- Few edges meet the threshold, so enumerating them exactly is feasible
- They account for significant butterfly count, so sampling noise is tolerable

Query cost: $O(\text{poly}(\log n, 1/\varepsilon))$ for degree queries on a small set.

### Light Partition Strategy

Light edges ($b(e) < \tau$) use **wedge sampling**:
- Sample wedges (paths of length 2 in the bipartite graph) that could close into butterflies
- Use small-degree-first sampling to access only necessary neighbors
- Reweight sampled wedges by partition membership frequency

**Key insight**: Most butterflies have $\geq 1$ light edge (by concentration bounds), so sampling the light partition captures coverage.

### Guess-and-Prove Technique

Since $\bar{b}$ is unknown a priori:
1. **Guess** rough estimate $\hat{\bar{b}}$ of butterfly density
2. Compute threshold $\tau$ based on guess
3. **Prove** via sampling that guess satisfies theoretical requirements
4. If proof fails, refine guess and retry

This allows adaptive threshold selection without prior statistical knowledge.

## Applications in Engineering

### 1. **Social Network Analysis**
- Count 4-cliques (butterflies in co-follow graphs) to detect coordinated behavior or bot networks
- Scale to graphs with billions of edges using sublinear query access

### 2. **Recommendation Systems**
- Bipartite user-item graphs contain "butterflies" indicating item co-preference patterns
- Approximate butterfly counts guide collaborative filtering without full graph scans

### 3. **Database Query Optimization**
- Estimate join sizes (analogous to butterfly counting) before executing expensive joins
- Stratified sampling reduces cost from $O(n^2)$ to $O(\text{poly-log}(n))$ queries

### 4. **Subgraph Pattern Mining**
- Extends beyond butterflies to larger bicliques via hierarchical partitioning
- Applicable to fraud detection (circular transaction patterns)

### 5. **Graph Streaming & Sketching**
- Maintains small data structures (heavy partition + light sampled wedges)
- Enables approximate counting on streaming/dynamic graphs

## Common Mistakes / Pitfalls

### 1. **Incorrect Threshold Interpretation**
**Error**: Treating $\tau = \bar{b}^{3/4}/\varepsilon^{1/4}$ as fixed threshold independent of graph structure.

**Reality**: $\tau$ depends on average butterfly density $\bar{b}$, which varies significantly across graphs. Must estimate or guess-and-prove.

### 2. **Confusing Butterfly vs. Edge Sampling**
**Error**: Sampling edges uniformly and counting butterfly contributions.

**Reality**: Stratified partition requires non-uniform sampling—heavy edges need enumeration, light edges need wedge