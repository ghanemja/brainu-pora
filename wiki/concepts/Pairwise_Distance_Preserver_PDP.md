# Pairwise Distance Preserver (PDP)

## Definition

The **Pairwise Distance Preserver (PDP)** problem is a graph optimization problem defined as follows:

**Input:** 
- A graph $G = (V, E)$ with edge weights (typically representing distances)
- A collection of terminal pairs $P \subseteq V \times V$ with $|P| = k$

**Output:** 
- A subgraph $H \subseteq G$ such that for every pair $(s, t) \in P$, the shortest path distance from $s$ to $t$ in $H$ equals the shortest path distance in $G$

**Objective:** 
Minimize the size of $H$ (number of edges or total edge weight) while preserving all pairwise distances in $P$.

### Special Case: Single-Source Distance Preserver (SDP)
The **Single-Source Distance Preserver (SDP)** is a restricted variant where all pairs share a common source: $P = \{(s, v) : v \in S\}$ for some source $s$ and set $S \subseteq V$. SDP is a strict special case of PDP.

## Key Equations

For a distance preserver $H$ to be valid, the following constraint must hold for all $(s, t) \in P$:

$$d_H(s, t) = d_G(s, t)$$

where $d_G(s,t)$ denotes the shortest path distance in the original graph $G$ and $d_H(s,t)$ denotes the shortest path distance in the preserver $H$.

The optimization objective is:

$$\min_{H \subseteq G} |E(H)| \quad \text{such that} \quad d_H(s,t) = d_G(s,t) \text{ for all } (s,t) \in P$$

Alternatively, for weighted versions:

$$\min_{H \subseteq G} \sum_{e \in E(H)} w(e) \quad \text{subject to distance preservation constraints}$$

## Physical Intuition / Derivation

### Motivation
In many network applications (transportation, communication, infrastructure), maintaining shortest-path information for specific node pairs is critical, but storing the entire graph is expensive. A distance preserver is a **minimal subgraph that certifies shortest paths for the pairs of interest**.

### Why PDP Matters
Consider a transportation network where:
- We need to preserve shortest routes between $k$ specific city pairs
- Storage/maintenance costs scale with the number of edges retained
- We want the smallest network subset that guarantees all route optimality

The distance preserver asks: *what is the smallest subnetwork that keeps all required shortest paths valid?*

### Connection to Path Packing
PDP can be reformulated as a **path packing problem**: find $|P|$ shortest paths (one for each terminal pair) that maximize edge sharing. This is the dual perspective to **$k$-Disjoint Shortest Paths**, where paths must be vertex-disjoint. In PDP, paths *cooperate* through shared edges; in disjoint paths, they *compete* for network resources.

### Why Hard to Compute
- **NP-hardness (general graphs):** Choosing which edges to include from potentially exponentially many shortest-path combinations is combinatorially hard
- **Approximation gap:** The best known factor is $O(n^{3/5+\varepsilon})$, indicating the problem is significantly harder than simple shortest-path computation
- **Structural dependency:** The complexity depends heavily on graph structure (planar vs. general) and the number of terminals

## Computational Complexity

### Established Results

| Parameter | Complexity | Remark |
|-----------|-----------|--------|
| General graphs | NP-hard | Even for unweighted graphs |
| Constant $\|S\|$ | P | Polynomial-time solvable |
| Constant $\|P\|$ | XP (fixed-parameter tractable) | Solvable in $f(k) \cdot n^{O(1)}$ time |
| Interval graphs | Restricted structure | Fewer branching vertices in preserver |
| Planar graphs | Structure-dependent | FPT under certain parameterizations |

### Approximation Results
- **Best known approximation:** $O(n^{3/5+\varepsilon})$-factor for minimum-weight PDP (Chlamtáč et al.)
- Gap between upper and lower bounds remains open for many settings

## Applications in Engineering

### 1. **Network Design & Infrastructure**
- **Telecommunication networks:** Preserve critical shortest paths between data centers while minimizing cable/fiber
- **Road networks:** Maintain optimal travel routes between major hubs with minimal edge redundancy
- **Power grids:** Ensure shortest transmission paths between generator-consumer pairs with minimal infrastructure

### 2. **Graph Compression & Indexing**
- **Distance oracles:** Build compact representations of shortest paths for query answering
- **Route caching:** Store only essential edges for frequently-queried origin-destination pairs
- **Memory-constrained systems:** Reduce graph representation size while maintaining distance guarantees

### 3. **Logistics & Routing**
- **Supply chain optimization:** Preserve shortest routes between key supplier-consumer nodes
- **Last-mile delivery:** Minimize road segment storage while ensuring optimal routing between distribution centers
- **Emergency response:** Maintain critical shortest paths for ambulance/fire routing between emergency nodes

### 4. **Computational Biology**
- **Protein interaction networks:** Identify essential interaction edges preserving pathway distances between key proteins
- **Metabolic networks:** Extract minimal subnetworks preserving metabolic distances between compounds

## Common Mistakes / Pitfalls

### 1. **Confusing with Minimum Spanning Tree (MST)**
**Mistake:** Assuming PDP is equivalent to computing an MST.

**Why it's wrong:** MST minimizes total edge weight without considering shortest paths. A preserver must preserve specific shortest-path distances, which may require non-tree edges (cycles with equal-length alternatives).

**Example:** In a triangle with edge weights 1-1-2, the MST uses two edges of weight 1, but the PDP for terminals at the endpoints of the weight-2 edge must include that edge.

### 2. **Forgetting the Special Case Nature**
**Mistake:** Treating all instances as general PDP without