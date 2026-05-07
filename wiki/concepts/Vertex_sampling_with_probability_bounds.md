# Vertex sampling with probability bounds

## Definition

**Vertex sampling with probability bounds** is a distributed graph algorithmic technique where vertices are independently selected with specified probabilities to serve as sources for breadth-first search (BFS) trees. The method provides probabilistic guarantees that a random sample will contain vertices with desirable distance properties to critical structures (such as cycles) in the graph.

Formally, given a graph $G = (V, E)$ with $n = |V|$ vertices, we sample each vertex independently with probability $p$ to form a set $S \subseteq V$ of sources. The key insight is choosing $p$ such that with high probability, $S$ contains at least one vertex satisfying a distance constraint to a target subgraph.

## Key Equations

**Sampling probability for single-stage estimation:**
$$p = \tilde{\Theta}(n^{-1/2})$$

**Expected number of sampled vertices:**
$$\mathbb{E}[|S|] = p \cdot n = \tilde{\Theta}(\sqrt{n})$$

**Multi-stage sampling probability (stage $i$ of $f$ stages):**
$$p_i = \tilde{\Theta}(n^{-i/f})$$

**Expected sampled sources per stage:**
$$\mathbb{E}[|S_i|] = \tilde{\Theta}(n^{1 - i/f})$$

**Coverage guarantee for $k$-closest vertices:**
If a set $C$ of $m$ vertices each has at least $m$ sampled vertices among their $k$ closest vertices, then $C$ is "covered" by some sampled source with high probability when:
$$k \geq \tilde{\Omega}(n^{1/f})$$

## Physical Intuition / Derivation

### The Core Idea: Adaptive Spatial Sampling

The technique exploits a fundamental tension in distributed graph algorithms:
- **Problem**: Finding exact solutions (e.g., girth of a graph) requires querying potentially all vertices
- **Goal**: Balance approximation quality with communication rounds

### Single-Stage Analysis

Consider computing girth (shortest cycle length) $g$:

1. **Initial partial BFS construction**: Each vertex participates in BFS trees from its $\tilde{O}(\sqrt{n})$ nearest vertices, taking $\tilde{O}(\sqrt{n} + D)$ rounds.

2. **Observation**: If the shortest cycle $C$ is not fully captured in these partial trees, then there must exist $\Omega(\sqrt{n})$ vertices at distance $\leq g/2$ from $C$.

3. **Sampling argument**: If we sample with probability $p = \tilde{\Theta}(n^{-1/2})$, the expected number of sampled vertices within distance $g/2$ of $C$ is:
$$\mathbb{E}[\text{samples near } C] = \Omega(\sqrt{n}) \cdot \tilde{\Theta}(n^{-1/2}) = \tilde{\Omega}(1)$$

By concentration inequalities, at least one vertex is sampled with high probability.

4. **Full BFS from sampled sources**: Constructing complete BFS from $\tilde{O}(\sqrt{n})$ sources takes $\tilde{O}(\sqrt{n} + D)$ rounds and guarantees a 2-approximation.

### Multi-Stage Generalization

Extend to $f$ stages with decreasing sampling probabilities:

- **Stage $i$**: Sample with probability $p_i = \tilde{\Theta}(n^{-i/f})$, yielding $\tilde{\Theta}(n^{1-i/f})$ sources
- **Coverage guarantee**: At least one stage $i^*$ will have a sampled vertex within distance $(g/2) \cdot i^*$ from cycle $C$
- **Per-vertex cost**: Each vertex participates in BFS trees from its $\tilde{O}(n^{1/f})$ closest sampled sources
- **Total time**: $\tilde{O}(f \cdot n^{1/f} + f \cdot D)$ rounds

**The key insight**: By sampling at scale $n^{-i/f}$ and truncating participation to distance $n^{(i+1)/f}$, we guarantee exponentially decreasing approximation factors $(i+1)$ across stages while keeping communication polynomial in the base factor.

## Applications in Engineering

### 1. **Distributed Cycle Detection**
In peer-to-peer networks and distributed systems, quickly approximating graph girth enables bottleneck identification and network topology analysis without querying all vertices.

### 2. **Wireless Sensor Networks**
Computing approximate graph properties (diameter, shortest cycles) with limited communication rounds. Sampling reduces message overhead while maintaining approximation guarantees.

### 3. **Large-Scale Network Monitoring**
Sampling routers/monitors with probability bounds ensures distributed detection of critical topological features (e.g., loops in network paths) with probabilistic completeness.

### 4. **Approximation Algorithms for NP-Hard Problems**
The technique generalizes to approximating other graph properties by trading approximation factor for running time—useful for real-time constraint satisfaction in large graphs.

### 5. **Biological Network Analysis**
In systems biology, approximate identification of feedback loops in gene regulatory networks using sampled node activation queries.

## Common Mistakes / Pitfalls

### 1. **Confusing sampling probability with success probability**
Students often think $p = n^{-1/2}$ means "each vertex is found with probability $n^{-1/2}$". Actually, $p$ is the *sampling* probability; the *success* probability emerges from concentration bounds on many trials.

### 2. **Not accounting for "$\tilde{\Theta}$" notation**
The $\tilde{\Theta}$ hides logarithmic factors. Actual probabilities are $\Theta(n^{-i/f} \cdot \log^c n)$ for some constant $c$. Ignoring this leads to underestimating required samples.

### 3. **Assuming independence assumptions fail to scale**
The analysis relies on Chernoff/concentration bounds for independent samples. For small $n$ or correlated failures, these guarantees degrade. Not all synchronous communication