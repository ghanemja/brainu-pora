# Approximate Nearest Neighbors

## Definition

**Approximate Nearest Neighbors (ANN)** is a computational approach for efficiently identifying points in a metric space that are close to a query point, with guaranteed approximation bounds rather than exact optimality.

Formally, given:
- A metric space $(V, \text{dist})$
- A point set $P \subseteq V$
- A query point $v \in V$
- An approximation parameter $\varepsilon > 0$

An **$\varepsilon$-approximate nearest neighbor** of $v$ is a point $p \in P$ such that:

$$\text{dist}(v, p) \leq (1 + \varepsilon) \cdot \min\{d(v, q) \mid q \in P\}$$

That is, the distance to the returned point is at most $(1 + \varepsilon)$ times the distance to the true nearest neighbor.

### Related Concept: Coreset

A **coreset** is a data reduction technique used to accelerate ANN queries. A **furthest neighbor $\varepsilon$-coreset** is a subset $Q \subseteq P$ such that for every $v \in V$, there exists $q \in Q$ with:

$$\text{dist}(v, q) \geq (1 - \varepsilon) \cdot \max\{d(v, p) \mid p \in P\}$$

The coreset enables efficient query answering by reducing the search space from $|P|$ points to $|Q|$ points, where $|Q| \ll |P|$.

---

## Key Equations

**Approximation Ratio:**
$$c = \frac{\text{dist}(v, p^*)}{\text{dist}(v, p_{\text{true}})}$$
where $p^*$ is the approximate nearest neighbor, $p_{\text{true}}$ is the true nearest neighbor, and $c \leq 1 + \varepsilon$.

**Coreset Size Bound (Euclidean/Doubling Metrics):**
$$|Q| = O(\varepsilon^{-d})$$
where $d$ is the ambient dimension. This exhibits exponential dependence on dimension (curse of dimensionality).

**Planar Metric Coreset (Bourneuf-Pilipczuk):**
$$|Q| = 2^{\text{poly}(1/\varepsilon)}$$
This achieves dimension-independence but exhibits exponential dependence on $\varepsilon^{-1}$.

---

## Physical Intuition / Derivation

### Why Approximation Helps

Exact nearest neighbor search requires comparing the query point to all $n$ database points, or maintaining complex geometric structures (e.g., k-d trees) that scale poorly in high dimensions. By relaxing the requirement to find the *exact* nearest neighbor—accepting instead a point within $(1+\varepsilon)$ of the true nearest neighbor—we trade a small accuracy loss for dramatic computational gains.

### Intuition Behind Coresets

A coreset distills the essential "representative" points from the full dataset. Rather than storing all $n$ points, we preprocess and identify a much smaller subset $Q$ that captures the geometric structure. Any query answer on $Q$ translates to a provably good answer for the full dataset $P$.

**Key insight:** For furthest neighbor queries, the challenge is that arbitrary point sets require $\Omega(n)$ coreset size—you may need to store nearly all points. However:
- In **Euclidean and doubling metrics**, packing arguments yield exponentially smaller coresets: $O(\varepsilon^{-d})$ points suffice.
- In **planar metrics**, dimension-independence is possible but comes at the cost of exponential dependence on $\varepsilon^{-1}$.

### The Curse of Dimensionality

In high-dimensional Euclidean spaces, the coreset size bound $\varepsilon^{-O(d)}$ becomes impractical. For example, with $d=100$ and $\varepsilon = 0.1$, the required coreset size grows astronomically. This fundamental barrier motivates research into alternative metrics, data structures, and randomized methods.

---

## Applications in Engineering

### 1. **Nearest Neighbor Search in High Dimensions**
- **Computer Vision:** Image retrieval and feature matching (SIFT, ORB descriptors). Approximate methods are standard because exact nearest neighbor search is intractable in 128+ dimensions.
- **Machine Learning:** Fast k-NN classification, locality-sensitive hashing (LSH).

### 2. **Database and Information Retrieval**
- **Approximate range queries:** Quickly find all points within distance $r$ of a query.
- **Clustering on massive datasets:** Construct coresets for k-means or k-median clustering before running iterative algorithms on reduced data.

### 3. **Computational Geometry**
- **Robot motion planning:** Finding nearby obstacle-free configurations.
- **Mesh processing:** Identifying nearest surface patches for deformation or registration.

### 4. **Network and Graph Analysis**
- **Shortest path distances:** In road networks or social graphs, approximate eccentricity and diameter calculations.
- **Planar metric applications:** Route planning in geographic information systems (GIS).

### 5. **Scalable Machine Learning**
- **Kernel methods:** Selecting representative samples for large kernel matrices.
- **Neural network training:** Core-set sampling to reduce training set size while preserving model quality.

---

## Common Mistakes / Pitfalls

### 1. **Confusing Approximate Nearest Neighbor with Approximate Distance**
- ❌ *Mistake:* Thinking ANN returns a distance that is $(1+\varepsilon)$-approximate.
- ✓ *Correct:* ANN returns a *point* whose distance is $(1+\varepsilon)$-approximate relative to the true nearest neighbor distance.

### 2. **Ignoring Dimensionality in Coreset Size**
- ❌ *Mistake:* Assuming a coreset approach is universally effective.
- ✓ *Correct:* In high dimensions, coreset sizes become prohibitive ($\varepsilon^{-d}$ growth). Alternative approaches (LSH, randomized trees) may be more practical.

###