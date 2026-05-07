# Minimum Weight Perfect Matching

## Definition

**Minimum Weight Perfect Matching (MWPM)** is a combinatorial optimization problem on a graph where one seeks to find a set of edges such that:

1. **Perfectness**: Every vertex in the graph is incident to exactly one edge in the matching
2. **Minimality**: The sum of edge weights is minimized over all possible perfect matchings

Formally, given a complete graph $G = (V, E)$ with edge weights $w: E \to \mathbb{R}^+$, a perfect matching $M \subseteq E$ is a set of edges such that:

$$|V| = 2|M| \quad \text{(all vertices covered exactly once)}$$

and we seek:

$$M^* = \arg\min_{M \text{ perfect}} \sum_{e \in M} w(e)$$

**Key constraint**: Perfect matchings only exist for graphs with an even number of vertices.

## Key Equations

**Optimality Condition (Primal-Dual)**:
A matching $M$ is optimal if and only if there exist dual variables $\{y_v : v \in V\}$ (node potentials) satisfying:

$$y_u + y_v \leq w(u,v) \quad \forall \, (u,v) \in E$$

with equality for all edges in $M$.

**Computational Complexity**:
- **Time**: $\mathcal{O}(|V|^3)$ via the Hungarian algorithm or Blossom algorithm
- **Space**: $\mathcal{O}(|V|^2)$ for dense graphs

## Physical Intuition / Derivation

### The Graph Matching Picture

In **topological quantum error correction**, syndrome information (excitations/defects) appears as vertices in a code graph. When a physical error occurs, it typically creates an even number of excitations. The error recovery string connecting these defects forms the natural correspondence to edges.

**Example: Toric Code**
- A single **Z-error** on a qubit creates exactly **2 excitations** (at opposite ends of the error chain)
- The correction is a minimum-length Z-string connecting these two excitations
- This maps naturally to finding a minimum-weight edge between the two defect vertices

### Why MWPM Works Here

The toric code exhibits a special property:

$$\text{Each physical qubit} \leftrightarrow \text{Graph edge (couples exactly 2 checks)}$$

This ensures that:
- Single-qubit errors produce exactly 2 excitations
- The decoding problem reduces to finding minimum-weight pairings
- MWPM becomes **near-optimal** for the syndrome graph induced by i.i.d. noise

### Breaking Down to General Codes

In general 2D topologically ordered codes, this clean picture breaks:

$$\text{Each qubit can couple to} > 2 \text{ checks}$$
$$\Rightarrow \text{Single errors create} > 2 \text{ excitations}$$

This requires **hypergraph matching** (NP-hard in general), motivating decomposition strategies.

## Applications in Engineering

### 1. **Quantum Error Correction**
   - **Toric codes** and surface codes: MWPM decoding is standard
   - Achieves near-optimal logical error rates for realistic noise
   - Runtime: $\mathcal{O}(V^3)$ acceptable for $V \sim 10^4$ syndrome measurements
   - **Impact**: Enabling fault-tolerant quantum computing

### 2. **Classical Combinatorial Optimization**
   - **Assignment problems**: Assigning $n$ workers to $n$ tasks minimizing cost
   - **Vehicle routing**: Matching depots to delivery routes
   - **Bipartite matching**: Scheduling, marriage problems
   - **Weighted bipartite matching** reduces to MWPM via graph doubling

### 3. **Machine Learning & Computer Vision**
   - **Object tracking**: Matching detected objects across video frames
   - **Point cloud registration**: Aligning 3D point sets by finding minimum-distortion correspondences
   - **Hungarian algorithm** foundation for data association in multi-target tracking

### 4. **Network Design**
   - **Telecommunications**: Optimal pairing of nodes in mesh networks
   - **Supply chain**: Matching suppliers to warehouses

## Common Mistakes / Pitfalls

### 1. **Confusing with Maximum Matching**
   - MWPM finds *minimum* total weight (for error correction, path length)
   - Maximum matching maximizes *number* of edges (different problem)
   - These are NOT equivalent even on the same graph

### 2. **Assuming Greedy Works**
   - **Mistake**: Greedily pairing closest defects gives optimal correction
   - **Reality**: Greedy can be arbitrarily suboptimal (factor of 2+ errors possible)
   - **Requires**: Global optimization via Hungarian or Blossom algorithms

### 3. **Graph Construction in Error Correction**
   - **Mistake**: Using Hamming distance directly as edge weights
   - **Correct approach**: Weight = minimum *path distance* on syndrome graph in code space
   - In toric code: weight = Manhattan distance between defects

### 4. **Assuming Bipartite Structure**
   - General MWPM works on *arbitrary* graphs (with even $|V|$)
   - Bipartite matching is a special case (faster: $\mathcal{O}(V^{2.5})$)
   - General case requires **Edmond's Blossom algorithm** to handle odd cycles

### 5. **Perfect Matching Necessity**
   - Only valid when $|V|$ is even
   - Odd-sized graphs require different formulations (e.g., **minimum cost circulation**)
   - In quantum codes: syndrome count must be even by parity conservation

## See Also

- [[Hungarian Algorithm]] — polynomial-time algorithm for bipartite matching
- [[Blossom Algorithm]] — handles general graphs with odd cycles
- [[Topological Order]] — context for error correction applications
- [[Hypergraph Matching]] — generalization to higher-order defects (NP-hard)
- [[Toric Code]] — canonical application in quantum error correction

## Sources

- Excised from quantum error correction paper on 