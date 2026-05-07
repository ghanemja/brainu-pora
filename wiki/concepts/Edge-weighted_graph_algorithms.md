# Edge-weighted graph algorithms

## Definition

**Edge-weighted graph algorithms** are computational methods operating on graphs $G = (V, E, w)$ where each edge $e \in E$ carries a numerical weight $w(e) > 0$. These algorithms solve optimization and decomposition problems that account for heterogeneous edge costs, distances, or capacities.

A foundational concept in this domain is the **Low-Diameter Decomposition (LDD)**, a randomized algorithm that partitions a graph by cutting edges while preserving distance properties. An LDD takes as input:
- An edge-weighted graph $G = (V, E, w)$
- A diameter parameter $\Delta$

And returns a cut set $X \subseteq E$ satisfying two properties:

1. **Separation guarantee** (deterministic): Every node pair $(s, t)$ with $\text{dist}_w(s, t) \geq \Delta$ is separated by $X$
2. **Low cut probability** (probabilistic): For any edge $e \in E$,
$$\Pr[e \in X] \leq \frac{w(e)}{\Delta} \cdot \text{LOSS}$$

where LOSS is a bounded quality measure.

## Key Equations

### Distance-weighted cut probability
$$\Pr[e \in X] \leq \frac{w(e)}{\Delta} \cdot \text{LOSS}$$

### Expected cut cost
By linearity of expectation, if $w$ forms a fractional cut for separated pairs:
$$\mathbb{E}[|X|] \leq \text{LOSS} \cdot \|w\|$$

### Approximation bounds for directed graphs
For $n$-node directed graphs, tight bounds exist:
$$\text{LOSS} \leq \min\left\{\tilde{O}(n^{1/3}), \tilde{O}(W^{1/2})\right\}$$

where $W$ relates to the graph weight structure and $\tilde{O}$ suppresses polylogarithmic factors.

### Roundtrip distance constraint (directed setting)
For demands $(s,t)$ requiring roundtrip separation:
$$\text{dist}_w(s, t) + \text{dist}_w(t, s) \geq 1$$

Current state-of-the-art: $\text{LOSS} = O(\log n \log \log n)$ for roundtrip LDDs.

## Physical Intuition / Derivation

**Why do we need edge-weighted algorithms?** In practice, not all edges are equal. A road might be 10 km (weight 10) while another is 1 km (weight 1). A cable might carry heavy current (low resistance, low weight) or light current (high resistance, high weight). Standard unweighted graph algorithms (like BFS) ignore these physical quantities.

**The LDD intuition:**
Imagine decomposing a weighted network into regions. We want to:
1. Ensure distant nodes (farther than $\Delta$) are definitely separated—this prevents "accidentally" keeping far-apart nodes connected
2. Make minimal cuts—but we must account for edge weights. A "heavy" edge (large $w(e)$) should be cut less often than a "light" edge

The parameter $\Delta$ acts as a diameter threshold: if I set $\Delta = 10$ km, nodes 15 km apart must be cut apart, but nodes 5 km apart might stay connected.

**Why LOSS matters:** A perfect decomposition would cut with probability exactly $\frac{w(e)}{\Delta}$. LOSS measures how much worse we do. For directed graphs, LOSS can be as high as $n^{1/3}$ in worst case, meaning the cut cost is $n^{1/3}$ times larger than the fractional optimum—a fundamental hardness limit.

**Connection to flow-cut gaps:** By rescaling so $\Delta = 1$, the weighted values $w(e)$ themselves form a fractional cut for distant pairs. The integrality gap (ratio of integer to fractional solutions) exactly equals LOSS. This reduction shows that LDD quality is equivalent to how well we can round fractional cuts to integral cuts.

## Applications in Engineering

### 1. **Network Routing & Shortest Path Computation**
   - Compute shortest paths under negative edge weights (critical in commodity pricing, game theory)
   - Directed LDDs enable scalable algorithms for networks with cost asymmetries
   - Example: routing in bidirectional transportation networks where forward/reverse costs differ

### 2. **Metric Embeddings & Dimensionality Reduction**
   - Use LDD to decompose weighted metrics into hierarchical trees
   - Reduces high-dimensional metric spaces to tree metrics with bounded distortion
   - Application: low-latency network design, facility location problems

### 3. **Distributed & Parallel Graph Processing**
   - LDD provides natural partition schemes respecting edge weights
   - Minimizes inter-partition communication (edges cut = communication overhead)
   - Frameworks: load balancing in distributed computing, graph partitioning for GPU processing

### 4. **Approximation Algorithms**
   - Weak LDD is a subroutine for many approximation algorithms
   - Applications include:
     - Sparsest cut approximation: $\tilde{O}(n^{1/3})$-approximation
     - Balanced partition problems in VLSI design
     - Clustering with weighted similarity metrics

### 5. **Telecommunications & Network Design**
   - Design resilient network topologies accounting for heterogeneous link costs/capacities
   - Decompose networks to identify critical cut edges
   - Multi-objective optimization: minimize cuts while respecting weight constraints

### 6. **Machine Learning on Graphs**
   - Graph sampling with probability proportional to edge weight
   - Spectral clustering on weighted graphs
   - Graph neural network sampling strategies

## Common Mistakes / Pitfalls

### 1. **Confusing unweighted and weighted cases**
   - ❌ *Mistake:* Applying unweighted BFS distances to weighted graphs
   - ✓ *Correct:* Use Dijkstra or weighted distance computations; edge weight directly affects $\Pr[e \in X]$

### 2. **Misinterpreting LOSS as negligible**
   -