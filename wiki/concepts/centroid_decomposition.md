# Centroid Decomposition

## Definition

**Centroid decomposition** is a recursive graph partitioning technique that hierarchically divides a graph (or path) into balanced subgraphs by repeatedly identifying and removing centroids. A **centroid** of a subgraph is a vertex whose removal results in no remaining component exceeding a specified size threshold.

In the context of DAG (Directed Acyclic Graph) covers, centroid decomposition is used to construct a hierarchical structure where:
- Each path $P$ is recursively partitioned into subpaths
- At each level, a centroid $x(P')$ is identified for subpath $P'$
- This centroid becomes a **hub vertex** connecting vertices in a covering DAG
- The recursion depth is $O(\log n)$, where $n$ is the number of vertices

For a vertex $v$ and path $P \in \mathcal{P}[v]$, the set $Q(y, P)$ represents subpaths containing vertex $y$, with $|Q(y, P)| = O(\log |P|)$.

## Key Equations

**Size bound on DAG center sets:**
$$|X_v| = O\left(\varepsilon^{-1} \cdot \log \Phi \cdot \log^2 n\right)$$

where:
- $X_v$ = set of DAG centers to which vertex $v$ connects
- $\varepsilon$ = approximation parameter
- $\Phi$ = path diversity parameter
- The set is constructed from $O(\log \Phi \cdot \log n)$ paths, each with $O(\varepsilon^{-1})$ covering vertices and $O(\log n)$ subpaths

**Total DAG edge count:**
$$|E(D_\sigma)| = O\left(n \cdot \varepsilon^{-1} \cdot \log \Phi \cdot \log^2 n\right)$$

**Distortion guarantee for shortest paths:**
$$d_{D_\sigma}(u,v) \leq (1+\varepsilon) \cdot d_G(u,v)$$

achieved by taking the minimum over two topologically ordered DAGs:
$$\min\{d_{D_\sigma}(u,v), d_{D_{\sigma^{-1}}}(u,v)\} \leq (1+\varepsilon) \cdot d_G(u,v)$$

## Physical Intuition / Derivation

### Why Centroid Decomposition Works

Imagine a long path in a graph. Rather than storing distances between every pair of vertices (expensive), centroid decomposition strategically places "relay stations" (centroids) such that:

1. **Balanced cuts**: Each centroid splits its subpath roughly in half by size, guaranteeing $O(\log n)$ recursion depth
2. **Minimal redundancy**: Each vertex connects to only $O(\log n)$ centroids per path, avoiding quadratic blowup
3. **Path coverage preservation**: The recursive structure ensures any shortest path passes through at least one centroid

### Construction Process

For a path $P$:
1. Identify centroid $x$ such that removing $x$ leaves all remaining subpaths with size $\leq |P|/2$
2. Recursively decompose left and right subpaths
3. Create edges from vertices near $x$ to $x$ itself

For a vertex $v$ involved in multiple paths $\mathcal{P}[v]$:
- For each path $P \in \mathcal{P}[v]$, identify $O(\varepsilon^{-1})$ covering vertices (using $\varepsilon$-covers)
- For each covering vertex $y$, find all $O(\log n)$ centroids in subpaths containing $y$
- Add all these centroids to $X_v$

### Distortion Analysis

Any shortest path from $u$ to $v$ in the original graph passes through:
- Some covering vertex $u' \in \mathcal{C}(u,P)$ near $u$
- Some covering vertex $v' \in \mathcal{C}(v,P)$ near $v$
- A **maximum subpath** $P'$ containing both $u'$ and $v'$

The centroid $x(P')$ of this maximum subpath lies in both $X_u$ and $X_v$, providing a detour through the DAG:
$$d_{D_\sigma}(u,v) \leq d_G(u, x(P')) + d_G(x(P'), v)$$

The covering property bounds total detour: $\leq (1+\varepsilon) \cdot d_G(u,v)$

## Applications in Engineering

### 1. **Network Routing & Distance Oracles**
- Construct compact routing tables with $O(\log^2 n)$ entries per vertex
- Answer distance queries with $(1+\varepsilon)$-approximation in $O(\log n)$ time
- Applications: Internet backbone routing, software-defined networks

### 2. **Approximation Algorithms for Directed Graphs**
- Build sparse spanners (subgraphs preserving distances)
- Construct distributed algorithms with polylogarithmic stretch
- Applications: peer-to-peer networks, wireless mesh networks

### 3. **Steiner Tree / DAG Covers**
- Generate Steiner DAGs where intermediate vertices (Steiner points) serve as hubs
- Reduce communication overhead in directed networks
- Applications: traffic engineering, network function placement

### 4. **Low-Diameter Decomposition (LDD)**
- Partition directed graphs into regions with small diameter
- Enable divide-and-conquer approaches for hard graph problems
- Applications: distributed computing, fault-tolerant routing

### 5. **Machine Learning on Graphs**
- Hierarchical feature extraction from road networks and citation graphs
- Efficient computation of graph kernels
- Multi-scale analysis of network structure

## Common Mistakes / Pitfalls

### 1. **Confusing Centroid with Center**
- A **centroid** minimizes maximum subtree size (balanced cut)
- A **center** minimizes the maximum eccentricity
- For decomposition, centroids provide the $O(\log n