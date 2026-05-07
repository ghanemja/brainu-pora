# Graph Eccentricity

## Definition

The **eccentricity** of a vertex $v$ in a graph $G = (V, E)$ is the maximum distance from $v$ to any other vertex in the graph:

$$\text{ecc}(v) = \max_{u \in V} \text{dist}(v, u)$$

where $\text{dist}(v, u)$ denotes the shortest path distance between vertices $v$ and $u$.

In metric space terminology, eccentricity represents the distance to a vertex's **furthest neighbor**—the most distant reachable point from a given starting point.

### Related Graph Diameter Concepts

From eccentricity, several fundamental graph metrics are derived:

- **Graph Diameter**: $\text{diam}(G) = \max_{v \in V} \text{ecc}(v)$ — the largest eccentricity in the graph
- **Graph Radius**: $\text{rad}(G) = \min_{v \in V} \text{ecc}(v)$ — the smallest eccentricity
- **Center**: The set of vertices $C = \{v \in V : \text{ecc}(v) = \text{rad}(G)\}$ — vertices with minimum eccentricity

## Key Equations

**Eccentricity of vertex $v$:**
$$\text{ecc}(v) = \max_{u \in V} \text{dist}(v, u)$$

**Diameter-radius relationship:**
$$\text{rad}(G) \leq \text{diam}(G) \leq 2 \cdot \text{rad}(G)$$

**Furthest neighbor $\varepsilon$-coreset condition** (from source material):

A subset $Q \subseteq P$ is a furthest neighbor $\varepsilon$-coreset if for every $v \in V$, there exists $q \in Q$ such that:
$$\text{dist}(v, q) \geq (1 - \varepsilon) \max_{p \in P} \{\text{dist}(v, p)\}$$

This approximates eccentricity within a $(1-\varepsilon)$ multiplicative factor.

## Physical Intuition / Derivation

### Why Eccentricity Matters

Imagine a communication network where vertices are nodes and edges represent communication links:

- A node's **eccentricity** answers: *"What is the worst-case latency to reach another node from here?"*
- The **diameter** tells us the worst-case latency *anywhere* in the network
- The **center** identifies vertices with best worst-case performance—ideal locations for hub nodes or emergency services

### Computational Challenge

Computing exact eccentricities requires an all-pairs shortest path analysis. For a graph with $n$ vertices:
- Naive approach: $O(n^2)$ or $O(n^3)$ depending on algorithm
- This becomes prohibitive for massive networks (social graphs, web graphs with billions of nodes)

**Coreset-based approximation** is a dimensionality reduction technique: instead of computing distances to all $n$ points, identify a small "representative" subset $Q$ whose sizes grow as $2^{\text{poly}(1/\varepsilon)}$ (depending on metric geometry), not $O(n)$.

The key insight: A small coreset allows approximate eccentricity queries via:
$$\text{ecc}(v) \approx (1+\varepsilon) \max_{q \in Q} \{\text{dist}(v, q)\}$$

## Applications in Engineering

### Network and Systems Design

1. **Communication Networks**: Routing protocols use graph diameter estimates to bound message propagation delays. Eccentricity identifies bottleneck vertices.

2. **Data Center Networking**: Finding the graph center helps place load balancers or caches to minimize maximum latency.

3. **Social Network Analysis**: Eccentricity identifies "central" users (low ecc) vs. "peripheral" ones (high ecc) for influence propagation studies.

### Sensor Networks

- Eccentricity of sensor nodes determines coverage guarantees and worst-case response times
- Center vertices are optimal placement locations for base stations

### Transportation & Logistics

- Road network graphs: eccentricity bounds travel time from any location to furthest service point
- Critical for ambulance/fire station placement optimization

### Algorithm Optimization

- **Approximate nearest/furthest neighbor search**: Preprocessing via coresets reduces query time from $O(n)$ to $O(|Q|)$ with small $|Q|$
- **Clustering algorithms**: Furthest-point heuristics for k-means initialization use eccentricity approximations

## Common Mistakes / Pitfalls

### 1. **Confusing Eccentricity with Degree**
   - **Wrong**: "High eccentricity = high degree (many neighbors)"
   - **Correct**: Eccentricity measures *distance* to furthest point, not local connectivity. A low-degree node in a "star" graph can have low eccentricity.

### 2. **Forgetting the Graph is Unweighted/Weighted**
   - In unweighted graphs, $\text{dist}(v,u)$ = hop count
   - In weighted graphs (realistic networks), distances accumulate edge weights—eccentricity can be unbounded
   - Always clarify metric space assumptions

### 3. **Assuming Coreset Size is Polynomial**
   - From the source: coreset size is $2^{\text{poly}(1/\varepsilon)}$ for general Euclidean/doubling metrics
   - This exhibits the **curse of dimensionality**: exponential dependence on dimension $d$ as $\varepsilon^{-O(d)}$
   - For high-dimensional data, coresets may be impractical despite theoretical guarantees

### 4. **Misinterpreting Center vs. Centroid**
   - **Graph center**: vertices with minimum eccentricity
   - **Geometric centroid**: average position (only meaningful for embedded graphs)
   - These are *not* the same thing

### 5. **Ignoring Disconnected Components**
   - In disconnected graphs, eccentricity = $\infty$ for vertices in different components
   - Always