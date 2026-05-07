# k-median clustering

## Definition

**k-median clustering** is a partitioning problem that seeks to partition a dataset $P$ into $k$ clusters by minimizing the sum of distances from each point to its nearest cluster center (median).

Formally, given a metric space $(V, \text{dist})$ and a set of points $P \subseteq V$, the k-median problem seeks a set of $k$ centers $C = \{c_1, c_2, \ldots, c_k\} \subseteq V$ that minimizes the **total cost**:

$$\Phi(P, C) = \sum_{p \in P} \min_{c \in C} \text{dist}(p, c)$$

The optimal set $C^*$ achieves the minimum value $\Phi^*(P)$. An $\alpha$-**approximate solution** is a set $C$ such that:

$$\Phi(P, C) \leq \alpha \cdot \Phi^*(P)$$

For k-median in general metric spaces, the best polynomial-time approximation ratio known is $\alpha = 2.613$ (and $\alpha = 1 + \sqrt{3} \approx 2.732$ in Euclidean spaces). The problem is NP-hard for $k \geq 2$.

## Key Equations

**Cost function:**
$$\Phi(P, C) = \sum_{p \in P} d(p, C) \quad \text{where} \quad d(p, C) = \min_{c \in C} \text{dist}(p, c)$$

**Approximation guarantee** for algorithm $\mathcal{A}$:
$$\Phi(P, \mathcal{A}(P)) \leq \alpha \cdot \Phi^*(P)$$

**k-median with capacities** (variant): Restrict each cluster to contain at most $u_i$ points:
$$\Phi(P, C) = \sum_{p \in P} \text{dist}(p, c(p)) \quad \text{subject to} \quad \left|\{p : c(p) = c_i\}\right| \leq u_i$$

**Local search swap operation**: Replace a center $c_i \in C$ with a candidate point $p \in P$, yielding $C' = (C \setminus \{c_i\}) \cup \{p\}$. A locally optimal solution admits no improving swap.

## Physical Intuition / Derivation

### Core Concept

Unlike k-means (which minimizes squared Euclidean distances), k-median minimizes absolute distances in arbitrary metric spaces. This makes it more **robust to outliers** and applicable to non-geometric data where distances encode dissimilarity (e.g., edit distance, shortest-path distance in graphs).

### Why "Median"?

The name reflects the 1-median problem: given points on a line, the 1-median (optimal center) is the *median* in the statistical sense—the point minimizing total distance. Generalizing to multiple clusters and higher-dimensional spaces is straightforward.

### Hardness and Algorithms

**Why is it NP-hard?**
- Enumerating all $\binom{n}{k}$ possible center sets is exponential
- No known polynomial algorithm finds the optimum
- Connected to facility location (open facilities instead of closing them)

**Common algorithmic approaches:**

1. **Greedy**: Start with one arbitrary center; iteratively add the point minimizing incremental cost. Achieves $O(\ln n)$ approximation.

2. **Local search**: Begin with a random set of $k$ centers. Repeatedly swap a center with a point if it decreases cost. Yields $(3 + \epsilon)$-approximation (poly-time with correct parameters).

3. **LP-rounding**: Relax the problem to a linear program; round the fractional solution using randomization. Achieves $O(1)$-approximation in special metrics.

4. **Coreset approach**: Construct a small representative subset $Q \subseteq P$ preserving cost up to $(1+\epsilon)$ factor. Solve k-median on $Q$, then lift back to $P$. Enables scalability for massive datasets.

### Coreset Perspective

A **k-median $\varepsilon$-coreset** is a weighted subset $Q \subseteq P$ (with weights $w: Q \to \mathbb{R}^+$) such that for *any* set of $k$ centers $C$:

$$\left| \Phi(Q, C) - \Phi(P, C) \right| \leq \varepsilon \cdot \Phi^*(P)$$

This is crucial: solving k-median on a polylogarithmically-sized coreset gives an approximate solution for the original dataset, dramatically reducing computational burden.

## Applications in Engineering

### 1. **Data Center and Server Placement**
Minimize latency by placing $k$ data centers in a network. Points are users, distances are network latency. k-median finds centers minimizing aggregate latency.

### 2. **Vehicle Routing and Facility Location**
Locate $k$ distribution centers or warehouses to minimize total transportation cost to customers. Robust to occasional high-distance outliers (unlike k-means).

### 3. **Machine Learning: Document/Text Clustering**
Partition documents using document-distance metrics (cosine distance, edit distance, Wasserstein distance). k-median outperforms k-means when outlier documents exist.

### 4. **Sensor Networks**
Deploy $k$ sensor nodes in a region to minimize average distance to sensor locations, balancing coverage uniformly.

### 5. **Graph Clustering**
Partition vertices in networks (social graphs, road networks) using shortest-path distances. k-median respects graph structure better than Euclidean metrics.

### 6. **Image Segmentation**
Cluster pixels using color + spatial distance in a combined metric. More stable than k-means under illumination variation.

### 7. **Large-Scale Data Processing**
Coreset-based k-median solves clustering on datasets too large for memory:
- MapReduce implementations compute coresets in parallel
- Reduces $n$ points to $\text{poly}(k/\varepsilon)$