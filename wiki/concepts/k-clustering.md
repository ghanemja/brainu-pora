# k-clustering

## Definition

**k-clustering** is the problem of partitioning a set of $n$ points in a metric space (typically $\mathbb{R}^d$) into exactly $k$ clusters to minimize a cost function, most commonly the sum of squared distances from points to their nearest cluster centers (k-means objective).

**Formal Statement:**
Given a point set $P = \{p_1, p_2, \ldots, p_n\} \subset \mathbb{R}^d$ and an integer $k$, find a set of $k$ centers $C = \{c_1, c_2, \ldots, c_k\}$ that minimizes the clustering cost:

$$\text{Cost}(P, C) = \sum_{p \in P} \min_{c \in C} \|p - c\|^2$$

where $\|\cdot\|$ denotes Euclidean distance.

**Variants and Extensions:**
- **(k, z)-clustering:** Generalizes the cost to $\sum_{p \in P} d(p, C)^z$ for exponent $z > 0$
- **Dynamic k-clustering:** Handles streaming data with point insertions and deletions
- **Incremental k-clustering:** Handles insertion-only streams
- **Robust k-clustering:** Tolerates outliers in the point set

---

## Key Equations

### Standard k-means Objective
$$J(C) = \sum_{i=1}^{n} \min_{j=1}^{k} \|p_i - c_j\|^2$$

### Approximation Guarantee
An algorithm achieves an **$\alpha$-approximation** if:
$$\text{Cost}_{\text{algorithm}}(P, C) \leq \alpha \cdot \text{OPT}(P)$$

where $\text{OPT}(P)$ is the optimal clustering cost.

### Recourse (Consistency Metric)
For streaming/dynamic clustering, **recourse** at time $t$ measures cluster center changes:
$$\text{Recourse}_t = |C_{t-1} \triangle C_t|$$

where $\triangle$ denotes symmetric difference. Total recourse bounds the cumulative number of center updates.

---

## Physical Intuition / Derivation

### Why k-clustering Matters

Imagine you operate $k$ warehouses serving $n$ customer locations. The k-clustering problem finds optimal warehouse placements to minimize total customer-to-warehouse travel distance. This is fundamentally a **geometry + optimization** problem.

### The Core Challenge

The problem is **NP-hard** in general (even for $k=2$ in high dimensions), motivating research into:

1. **Approximation algorithms** (Lloyd's algorithm, k-means++)
2. **Streaming/dynamic variants** where data arrives online and we cannot recompute from scratch
3. **Consistency constraints** where clustering solutions must not change drastically as new data arrives

### Streaming Context (from source material)

In **incremental streams**, points arrive one-by-one. A naive approach recomputes clustering at each step—expensive. Instead, we maintain $k$ cluster centers with bounded **recourse** (number of center swaps):

- **Earlier work** ([LV17]): $O(k^2 \cdot \text{polylog}(n))$ recourse
- **Improved work** ([FLNS21]): $O(k \cdot \text{polylog}(n))$ recourse  
- **Recent advance** ([CJWZ25]): $(1+\varepsilon)$-approximation with sublinear recourse

The improvement from $k^2$ to $k$ recourse comes from **geometric ball-growing techniques**—build robust clusters by examining progressively larger geometric neighborhoods, reducing sensitivity to future arriving points.

---

## Applications in Engineering

### 1. **Facility Location & Logistics**
- Warehouse/distribution center placement
- Minimizes transportation costs across geographic regions
- Dynamic variant handles seasonal demand changes

### 2. **Data Center Networking**
- Group servers into fault domains
- Minimize latency by clustering geographically proximate machines
- Streaming variant handles server additions/failures

### 3. **Image Segmentation & Computer Vision**
- Partition pixels into $k$ regions by color/texture
- Used as preprocessing for object recognition
- Approximate k-means via Lloyd's algorithm suffices for real-time systems

### 4. **Sensor Networks**
- Group sensor nodes into $k$ clusters with cluster heads
- Reduces communication overhead in wireless networks
- Incremental clustering handles mobile/battery-limited devices

### 5. **Customer Segmentation (Market Analytics)**
- Cluster customers by purchasing behavior into $k$ segments
- Dynamic variant retrains as new transaction data streams in
- Recourse minimization = minimizing marketing strategy changes

### 6. **Gene Expression Analysis**
- Cluster genes with similar expression patterns
- $k$ clusters represent co-regulated gene groups
- Robust variants handle measurement noise

---

## Common Mistakes / Pitfalls

### 1. **Confusing NP-hardness with Unsolvability**
Students often believe NP-hardness means "no algorithm exists." In practice:
- Approximation algorithms (k-means++, Lloyd's) are highly effective
- For small $k$ and moderate $n$, exact methods or branch-and-bound work
- The distinction is polynomial vs. exponential worst-case runtime

### 2. **Applying Static Algorithms to Streaming Data**
Recomputing optimal clustering from scratch at each time step:
- Defeats the purpose of streaming (memory, computational efficiency)
- Ignores **recourse**—users may prefer suboptimal-but-stable solutions
- Requires $\Omega(n)$ memory (streaming algorithms use $O(k \cdot \text{polylog}(n))$)

### 3. **Ignoring the Role of Geometry**
The source material notes that techniques from k-clustering (e.g., ball-growing for robustness) are **specific to Euclidean geometry**:
- Do not generalize directly to abstract metrics or graph-based clustering
- Low-rank approximation problems lack these geometric properties

### 4. **Underestimating Outlier Impact**
- A single outlier can distort cluster centers
-