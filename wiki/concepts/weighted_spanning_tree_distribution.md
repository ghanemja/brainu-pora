# Weighted Spanning Tree Distribution

## Definition

A **weighted spanning tree distribution** is a probability distribution over all spanning trees of a weighted graph, where the probability of selecting any particular spanning tree is proportional to the product of its edge weights.

Formally, given a graph $G = (V, E)$ with edge weights $\{w_e : e \in E\}$ where $w_e > 0$, the weighted spanning tree distribution assigns probability:

$$P[T] = \frac{\prod_{e \in T} w_e}{Z}$$

where $T$ is a spanning tree and $Z$ is the normalizing partition function (sum over all spanning trees).

**Special case:** When all weights are uniform ($w_e = 1$ for all $e$), this reduces to the **uniform spanning tree distribution**, where each spanning tree is equally likely.

## Key Equations

### Probability Mass Function
$$P[T] \propto \prod_{e \in T} w_e$$

### Partition Function
$$Z = \sum_{T \in \mathcal{ST}(G)} \prod_{e \in T} w_e$$

where $\mathcal{ST}(G)$ denotes the set of all spanning trees of $G$.

### Matrix-Tree Theorem Connection
The partition function can be computed via the determinant of a weighted Laplacian matrix $L^{(w)}$:

$$Z = \det(L^{(w)}_{\text{reduced}})$$

where $L^{(w)}$ is the weighted Laplacian with diagonal entries $L^{(w)}_{ii} = \sum_{j \sim i} w_{ij}$ and off-diagonal entries $L^{(w)}_{ij} = -w_{ij}$.

### Log-Likelihood Form
For numerical stability in computation, probabilities are often expressed as:

$$\log P[T] = \sum_{e \in T} \log w_e - \log Z$$

## Physical Intuition / Derivation

### Why Weight by Edge Products?

The weighted spanning tree distribution naturally arises from a **maximum entropy** perspective. When we want to sample spanning trees while preferring those with higher-weight edges, the distribution that maximizes entropy subject to expected edge weight constraints takes exactly the form $P[T] \propto \prod_{e \in T} w_e$.

### Connection to Random Walks & Electrical Networks

In the uniform case ($w_e = 1$), the distribution emerges from **random walk based methods** (Aldous-Broder algorithm):
- Start a random walk from an arbitrary node
- Each time the walk first visits a new node $v$ via edge $e = (u,v)$, include $e$ in the spanning tree
- This generates each uniform spanning tree with equal probability

For weighted graphs, edge weights can be interpreted as **electrical conductances** in an equivalent resistance network. The probability of an edge appearing in a sampled tree correlates with its effective conductance.

### Generative Perspective

Think of the distribution as follows:
- Edges with high weights are "preferred" or have higher probability of inclusion
- The product form ensures that a spanning tree with all high-weight edges is exponentially more likely than one with low-weight edges
- This is useful for applications where edge costs or capacities matter

## Applications in Engineering

### 1. Graph Sparsification
Weighted spanning tree sampling is used to construct graph sparsifiers—sparse subgraphs that preserve spectral properties. Edges sampled according to the weighted distribution (with weights proportional to effective resistances) yield spectral sparsifiers with logarithmic number of edges.

### 2. Approximation Algorithms for TSP
The Christofides algorithm and modern TSP approximation routines use spanning tree sampling to find low-cost Hamiltonian cycles. Weighting edges by their costs and sampling spanning trees provides structured solutions.

### 3. Network Design & Reliability
In communication and power networks:
- Edge weights represent capacity, cost, or reliability
- Sampling from the weighted distribution identifies diverse spanning trees that could serve as backup routes
- Supports **k-edge-connected multisubgraph** design problems

### 4. Machine Learning: Sampling for Uncertainty
In graphical models and Bayesian inference:
- Used to sample diverse graph structures
- Weights encode prior beliefs or learned scores
- Applied in structure learning for probabilistic graphical models

### 5. Distributed Systems
Recent work extends sampling to the **Broadcast Congested Clique model**—a distributed computing environment:
- Nodes compute and sample spanning trees in parallel over a complete communication network
- Each round allows $O(\log n)$-bit messages between all pairs
- Applications include distributed graph analysis and maintenance in large networks

### 6. Matroid Optimization
Weighted spanning tree distributions generalize to matroid base distributions, enabling applications in:
- Submodular optimization
- Combinatorial algorithms for constrained resource allocation

## Common Mistakes / Pitfalls

### 1. Confusion About Edge Independence
**Mistake:** Assuming sampled edges are independent given their weights.

**Reality:** Edges are highly correlated; sampling is constrained by the spanning tree structure (exactly $n-1$ edges, no cycles). High-weight edges tend to co-occur.

### 2. Thinking Uniform Distribution is Easy
**Mistake:** Assuming uniform spanning tree sampling is straightforward or polynomial-time trivial.

**Reality:** Efficient centralized sampling (nearly linear time) requires sophisticated Laplacian-based techniques or careful random walk implementation. Distributed sampling (polylogarithmic rounds) is a recently solved problem.

### 3. Normalization Constant as Afterthought
**Mistake:** Treating $Z$ (the partition function) as a minor detail or assuming it cancels out.

**Reality:** Computing $Z$ is #P-hard in general; it equals a matrix determinant (Matrix-Tree Theorem) and is central to many algorithmic approaches.

### 4. Mixing Weight Semantics
**Mistake:** Ambiguity about whether weights represent costs (minimize) vs. preferences (maximize).

**Reality:** In $P[T] \propto \prod_{e \in T} w_e$, higher weights increase probability. Transform costs appropriately: use $w_e = e^{-\text{cost}_e}$ or $w_e = 1/\text{cost}_e$ if needed.

### 5. Neglecting Numerical Stability
**Mistake