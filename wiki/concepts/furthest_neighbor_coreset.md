# furthest neighbor coreset

## Definition

A **furthest neighbor ε-coreset** is a subset $Q \subseteq P$ of a point set $P$ in a metric space $(V, \text{dist})$ such that every point $v \in V$ has at least one point in $Q$ within an $(1+\varepsilon)$-factor of its furthest point in $P$. Formally:

$$\forall v \in V: \max_{p \in Q} \text{dist}(v, p) \geq \frac{1}{1+\varepsilon} \max_{p \in P} \text{dist}(v, p)$$

Equivalently, if $R_v = \max_{p \in P} \text{dist}(v, p)$, then $Q$ must satisfy:

$$\forall v \in V: \exists q \in Q \text{ such that } \text{dist}(v, q) \geq (1-\varepsilon) R_v$$

The **size** of the coreset, denoted $|Q|$, is a key quality metric—smaller coresets are more useful for downstream applications.

## Key Equations

**ε-semi-ladder index upper bound** (for minor-closed graph classes):
$$\lambda_\varepsilon(G) \leq 2^{p_G(1/\varepsilon)}$$

where $p_G$ is a polynomial depending on the graph class $G$ (e.g., planar graphs, bounded treewidth, surfaces).

**Lower bound for planar metrics:**
$$\exists \text{ planar metric with ε-ladder index } \geq 2^{\Omega(1/\varepsilon)}$$

**ε-comatching relation** (formal connection):
For an inclusion-wise minimal ε-coreset $Q$ in the special case where $\max_{p \in P} \text{dist}(v, p) = R$ for all $v$, the pairs $\{(v_p, p) : p \in Q\}$ form an **ε-comatching**—a matching where paired points are approximately maximum distance apart.

## Physical Intuition / Derivation

### Motivation

In coverage and facility location problems, we often ask: *"What is the furthest any point is from the nearest facility?"* A furthest neighbor coreset answers: *"What is the minimum set of facilities needed to approximate this worst-case distance for all points?"*

### Why This Matters

Consider a metric space induced by a weighted graph (e.g., road networks). For a location $v$, the furthest point $\max_p \text{dist}(v,p)$ represents the worst-case travel distance. A coreset $Q$ ensures that we can approximate this maximum for every location using only $|Q|$ representative points, rather than storing all of $P$.

### The Greedy Algorithm and Its Limits

A natural greedy approach: iteratively add the point that maximizes the minimum distance to already-selected points. This is tightly connected to the **ε-semi-ladder index**—the length of the longest "ladder" structure in the metric. 

**Key insight:** For planar metrics, the greedy approach yields coresets of size $2^{\Omega(1/\varepsilon)}$ because planar metrics can encode exponentially long ε-semi-ladders (Sokołowski, [48]). This barrier is **fundamental to the greedy approach**.

### Circumventing the Exponential Barrier

The paper identifies a richer structure: **ε-comatching**, which is similar to but potentially more powerful than ε-semi-ladder. The key observation is that minimal coresets in restricted cases naturally induce comatchings. The challenge is:

1. **Obstacle (i):** Prove that ε-comatching index and ε-coreset size are polynomially related.
2. **Obstacle (ii):** Bound the ε-comatching index as a polynomial in $1/\varepsilon$ (potentially separating it from the exponential ε-semi-ladder index).

## Applications in Engineering

### 1. **Facility Location & Logistics**
- Determine minimum number of distribution centers to guarantee worst-case service time for all customers
- Reduce computational burden in large supply chain networks

### 2. **Sensor Networks**
- Select a small subset of sensors to monitor all regions with bounded approximation error
- Trade coverage quality for energy efficiency and communication cost

### 3. **Computational Geometry & Nearest Neighbor Data Structures**
- Reduce index size while preserving nearest/furthest neighbor query approximation guarantees
- Accelerate range queries in metric spaces

### 4. **Clustering & Data Summarization**
- Create compact representatives of high-dimensional datasets
- Maintain worst-case distance bounds for downstream ML tasks

### 5. **Geographic Information Systems (GIS)**
- Query optimization in spatial databases
- Approximate furthest-site Voronoi diagrams with fewer sites

## Common Mistakes / Pitfalls

### 1. **Confusing Furthest vs. Nearest Neighbor Coresets**
A furthest neighbor coreset bounds $\max_p \text{dist}(v,p)$; it does *not* control the minimum distance. The approximation factor applies asymmetrically—we preserve worst-case distances, not average distances.

### 2. **Assuming Greedy Optimality**
The greedy algorithm is *not* optimal for minimizing coreset size in general metrics. It produces solutions with exponential dependence on $1/\varepsilon$ for structured metrics like planar graphs.

### 3. **Conflating ε-Semi-Ladder and ε-Comatching**
While related, these are distinct structures. ε-Semi-ladder index is well-studied via sparse graph theory; ε-comatching index may be polynomially smaller, but requires novel techniques to bound.

### 4. **Ignoring Metric Structure**
Coreset size depends crucially on the underlying metric's geometric/topological properties. Bounds valid for planar metrics may not hold for arbitrary metrics or Euclidean spaces.

### 5. **Minimality Assumptions**
When claiming $|Q|$ bounds, ensure $Q$ is **inclusion-wise minimal** (cannot remove any point without violating the ε-coreset property).