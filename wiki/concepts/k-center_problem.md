# k-center problem

## Definition

The **k-center problem** is a fundamental optimization problem in computational geometry and clustering:

**Given:** A metric space $(V, \text{dist})$ with $n$ points and an integer $k \geq 1$

**Find:** A subset $C \subseteq V$ with $|C| = k$ (the "centers") that minimizes the maximum distance from any point in $V$ to its nearest center.

Formally:
$$\text{minimize}_{C \subseteq V, |C|=k} \max_{v \in V} \text{dist}(v, C)$$

where $\text{dist}(v, C) = \min_{c \in C} \text{dist}(v, c)$ is the distance from point $v$ to the closest center.

The objective value $r_k = \max_{v \in V} \text{dist}(v, C)$ is called the **covering radius** or **k-center cost**.

## Key Equations

**Covering radius:**
$$r_k(C) = \max_{v \in V} \min_{c \in C} \text{dist}(v, c)$$

**Optimal k-center value:**
$$\text{OPT}_k = \min_{|C|=k} r_k(C)$$

**Approximation guarantee ($\alpha$-approximation):**
An algorithm is an $\alpha$-approximation if it produces centers $C'$ satisfying:
$$r_k(C') \leq \alpha \cdot \text{OPT}_k$$

**ε-coreset size bounds** (from source material):
- **Planar graphs:** $\text{size}(S) = (1/\varepsilon)^{2^{O(k)}}$ (upper bound, Theorem 1.10)
- **Trees:** $\text{size}(S) = \Omega(2^{1/\varepsilon})$ when $k \sim 1/\varepsilon$ (lower bound)
- **Bounded genus $g$ surfaces:** $\text{poly}(g) \cdot (1/\varepsilon)^{2^{O(k)}}$ (upper bound)

## Physical Intuition / Derivation

### The Covering Problem

Think of the k-center problem as positioning $k$ emergency response stations (hospitals, fire stations, servers) to minimize the worst-case response time to any location. The goal is not to minimize average distance but to ensure **no point is too far from the nearest facility**.

### Why This is Hard

1. **NP-hardness:** The decision version ("is $\text{OPT}_k \leq r$?") is NP-complete for general metrics (in Euclidean spaces with $k \geq 2$).

2. **Greedy approximation:** A simple greedy algorithm achieves a **2-approximation**:
   - Start with an arbitrary center $c_1$
   - Repeatedly add the point farthest from current centers
   - This guarantee is tight; no polynomial-time $(2-\varepsilon)$-approximation exists (unless P=NP)

3. **Graph-restricted variants:** When the metric is induced by a graph, the complexity depends heavily on the graph structure:
   - **Trees:** Polynomial-time solvable
   - **Planar graphs:** Hard, but amenable to coreset-based approximation
   - **General graphs:** Worst-case exponential

### ε-Coresets for k-Center

A **coreset** is a small subset $S \subseteq V$ that approximately preserves the k-center cost: solving the problem on $S$ gives a good approximate solution for the full set $V$.

The size of ε-coresets depends on:
- **Graph structure** (genus, treewidth, minor-freeness)
- **Approximation parameter** $\varepsilon$
- **Number of centers** $k$

The source material shows a **surprising separation** between graph classes:
- Planar and bounded-genus graphs admit polynomial-in-$1/\varepsilon$ coresets
- For more general classes (K₅-minor-free, bounded treewidth), exponential dependence is unavoidable

## Applications in Engineering

### 1. **Facility Location**
- Positioning $k$ hospitals, fire stations, or data centers to minimize worst-case coverage distance
- Emergency response planning where uniform response time guarantees are critical

### 2. **Network Design**
- Placing $k$ routers or base stations in a communication network to minimize latency to the farthest node
- Server placement in distributed systems (CDN edge nodes, replica servers)

### 3. **Sensor Networks**
- Deploying $k$ sensors to monitor a spatial region with guaranteed coverage
- Robot docking/charging station placement to ensure battery life constraints

### 4. **Load Balancing**
- Partitioning compute workload among $k$ servers to minimize maximum latency
- Task scheduling on parallel architectures

### 5. **Clustering with Worst-Case Guarantees**
- Unlike k-means (which minimizes sum of squared distances), k-center minimizes maximum distance
- Useful when outlier protection is essential

### 6. **Circuit Design**
- Placement of $k$ power distribution units or clock trees to minimize skew
- Via placement in multilayer PCBs

## Common Mistakes / Pitfalls

1. **Confusing k-center with k-means:**
   - k-center minimizes **maximum distance** (min-max objective)
   - k-means minimizes **sum of squared distances** (sum-of-squares objective)
   - They have different complexity properties and approximation algorithms

2. **Ignoring the 2-approximation barrier:**
   - For general metrics, no polynomial-time $(2-\varepsilon)$-approximation exists (NP-hardness)
   - Algorithms claimed to beat 2x should be examined for restricted problem classes

3. **Overstating coreset benefits:**
   - Coresets reduce problem size but may not make the problem tractable on the coreset itself
   - Size of coresets can still be exponential in $k$ or $1/\varepsilon$ depending on graph structure

4. **Misunderstanding graph structure constraints:**