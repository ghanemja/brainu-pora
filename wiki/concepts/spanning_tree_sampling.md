# Spanning Tree Sampling

## Definition

**Spanning tree sampling** is the problem of generating a random spanning tree from a given graph according to a specified probability distribution. For a connected graph $G = (V, E)$ with edge weights $\{w_e : e \in E\}$, the **weighted spanning tree distribution** is defined as:

$$P[T] \propto \prod_{e \in T} w_e$$

where $T$ ranges over all spanning trees of $G$. The **uniform spanning tree distribution** is the special case where all edge weights are equal ($w_e = 1$ for all $e \in E$), giving each spanning tree equal probability.

In distributed settings, spanning tree sampling refers to algorithms that solve this problem in communication-constrained models such as the **Congested Clique** (each node exchanges $O(\log n)$ bit messages per round with all others) and **Broadcast Congested Clique** (single broadcast channel).

## Key Equations

**Weighted spanning tree probability:**
$$P[T] = \frac{\prod_{e \in T} w_e}{Z}$$

where $Z = \sum_{T' \in \mathcal{T}(G)} \prod_{e \in T'} w_e$ is the partition function (sum over all spanning trees $\mathcal{T}(G)$).

**Total variation distance bound:** For approximate sampling algorithms, the quality is measured by:
$$d_{\text{TV}}(\mathcal{D}_{\text{alg}}, \mathcal{D}_{\text{true}}) \leq O(n^{-c})$$

where $\mathcal{D}_{\text{alg}}$ is the algorithm's output distribution and $\mathcal{D}_{\text{true}}$ is the true target distribution.

**Centralized complexity (nearly-linear):**
$$T(n) = O(m \log^{O(1)}(n \kappa))$$

where $m$ is the number of edges and $\kappa$ is the condition number of the Laplacian.

## Physical Intuition / Derivation

### Why Sample Spanning Trees?

Spanning trees are fundamental combinatorial objects representing minimal connected subgraphs. Sampling them according to their edge-weight-dependent probability naturally encodes graph structure: edges with higher weights are more likely to appear in sampled trees, making this a powerful tool for:

- **Graph compression**: Selecting representative edges while preserving connectivity
- **Randomized algorithms**: Structured randomization for approximation (e.g., TSP)
- **Probabilistic analysis**: Understanding typical graph properties

### Core Insight: Laplacian-Based Methods

The key mathematical insight linking spanning trees to linear algebra is **Kirchhoff's matrix-tree theorem**:

$$\text{# spanning trees} = \det(\mathbf{L}_{\text{reduced}})$$

where $\mathbf{L}$ is the **graph Laplacian** matrix. This connection means:
- Sampling becomes equivalent to solving linear systems
- Weighted spanning tree distributions can be sampled via random walks on effective conductance (edge weights)

### Distributed Challenge

In the Congested Clique model, each node knows only its incident edges initially. The fundamental challenge is:

$$\text{Information propagation distance} \geq \Omega(\log n)$$

because the graph diameter can be $\Theta(\log n)$ (or larger), and each round allows only local message passing of $O(\log n)$ bits.

**Previous approaches** (Pemmaraju, Roy, Sobel 2025) required $\tilde{O}(n^{1/2 + \alpha})$ rounds, where $\alpha$ is the exponent for distributed matrix multiplication. This was fundamentally bottlenecked by requiring near-global synchronization.

**Modern approach** (Anari & Haqi) achieves $\tilde{O}(1)$ rounds by:
1. Leveraging fast approximate Laplacian solvers in distributed settings
2. Using **matroid exchange walk** techniques that avoid explicit global matrix construction
3. Carefully controlling error propagation to achieve $O(n^{-c})$ total variation distance for any constant $c$

## Applications in Engineering

### 1. Network Design & Resilience
- **Critical infrastructure**: Sample diverse spanning trees to identify edge criticality; redundant paths for fault tolerance in power grids, communication networks
- **Load balancing**: Distribute network flow across sampled spanning trees to avoid bottlenecks

### 2. Combinatorial Optimization
- **Traveling Salesman Problem (TSP)**: The Christofides approximation algorithm uses spanning tree sampling as a subroutine; achieves 1.5-approximation
- **Steiner tree approximation**: Sampled trees provide structured solutions for multi-terminal connectivity

### 3. Graph Sparsification
- **Effective resistance-based sparsification**: Sampling spanning trees with probability proportional to effective resistance edges preserves spectral properties while reducing edge count
- Application: Speeding up convergence in distributed optimization algorithms

### 4. Distributed Machine Learning
- **Gossip algorithms**: Spanning trees define communication topologies for averaging and consensus in federated learning
- **Randomized gradient descent**: Tree-based aggregation reduces communication rounds

### 5. Electrical Network Analysis
- **Circuit reliability**: Spanning trees represent possible current paths; weighted sampling models failure probabilities
- **Power grid optimization**: Determine redundant transmission lines via spanning tree ensemble analysis

## Common Mistakes / Pitfalls

### 1. Confusing Uniform with Weighted Sampling
**Mistake:** Treating all spanning tree distributions as equivalent.
**Reality:** Weighted distributions are fundamentally different—edge weights determine selection probability. An edge with weight $w_e$ is NOT selected with probability proportional to $w_e$; the probability depends on all spanning trees containing it.

### 2. Underestimating Communication Overhead
**Mistake:** Assuming $\tilde{O}(1)$ distributed algorithms are "trivial" or faster than centralized methods.
**Reality:** The hidden $\log^{O(1)}(n)$ factor can be substantial; total rounds may be $\log^{10}(n)$ or worse. Compare asymptotic complexity to wall-clock time in practice.

### 3. Ignoring Total Variation Distance
**Mistake:** Using an "approximately correct"