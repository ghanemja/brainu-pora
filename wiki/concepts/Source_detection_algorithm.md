# Source Detection Algorithm

## Definition

A **source detection algorithm** is a distributed computing procedure that identifies and selects a subset of vertices (sources) in a network graph to efficiently estimate global graph properties, particularly the **girth** (shortest cycle length). The algorithm operates in a distributed setting where vertices communicate with neighbors over multiple communication rounds, and it strategically samples vertices as sources based on proximity and network topology.

More formally, given an undirected network $G = (V, E)$ with $|V| = n$ vertices and diameter $D$, a source detection algorithm:

1. Selects a subset $S \subseteq V$ of sources according to a sampling probability
2. For each vertex $v$, identifies $U(S, k, v)$ — the $k$ closest vertices to $v$ from the source set $S$
3. Constructs partial BFS (breadth-first search) trees rooted at selected sources
4. Enables detection of graph cycles by determining whether cycles are "covered" by the source set

## Key Equations

**Coverage condition:** A cycle $C$ is covered by source set $S$ if there exists at least one source $s \in S$ that lies in the $k$-nearest sources for *all* vertices in $C$:

$$\text{$C$ is covered by $S$} \iff \exists s \in S : s \in U(S, k, v) \text{ for all } v \in V(C)$$

**Distance to covered cycle:** The distance from $S$ to a covered cycle $C$ is:

$$d(S, C) = \min\{d(s, C) \mid s \in S \text{ covers } C\}$$

**Sampling probability (multi-layer approach):** In a $f$-layer estimation, the $i$-th layer samples vertices independently with probability:

$$p_i = \tilde{\Theta}(n^{-i/f})$$

Each vertex participates in partial BFS trees of its $\tilde{O}(n^{1/f})$ closest sampled sources.

**Approximation guarantee:** Using $f$ estimation layers yields an approximation factor of:

$$\text{Approximation ratio} \leq f$$

with total complexity:

$$T_{\text{total}} = \tilde{O}(f \cdot n^{1/f} + f \cdot D) \text{ rounds}$$

## Physical Intuition / Derivation

### Why Source Detection Matters

Computing global graph properties (like girth) in a distributed setting is fundamentally hard because vertices lack global information. A naive approach—constructing full BFS trees from all $n$ vertices—requires $\tilde{O}(n + D)$ rounds, which is prohibitive for large networks.

### The Core Insight: Sampling & Proximity

The key observation is that **not all vertices need to be sources**. Instead:

1. **Sample sources sparsely**: Use random sampling with probability $p \ll 1$ to reduce the number of sources from $n$ to roughly $p \cdot n$.

2. **Exploit locality**: For detecting a cycle $C$, we don't need a source *on* the cycle—we need a source "close enough" to the cycle. If a source is within distance $g/2$ (where $g$ is girth), it can participate in BFS trees that cover all vertices of $C$.

3. **High probability existence**: If we sample with probability $\tilde{\Theta}(n^{-1/2})$ and there are $\Omega(\sqrt{n})$ vertices within distance $g/2$ of cycle $C$ (by geometric arguments), then with high probability at least one gets sampled.

### Multi-Scale Refinement

The $f$-layer approach trades **approximation quality for speed**:

- **Layer 0** ($p_0 = \tilde{\Theta}(1)$): Very coarse sampling, fast but inaccurate
- **Layer $i$** ($p_i = \tilde{\Theta}(n^{-i/f})$): Medium density sampling
- **Layer $f-1$** ($p_{f-1} = \tilde{\Theta}(n^{-1})$): Dense, slower but more accurate

For each layer $i$, we ask: "Is there a sampled source within distance $(g/2) \cdot i$ of the true girth cycle?" By the pigeonhole principle and careful analysis, **at least one layer will succeed**, guaranteeing the $f$-approximation.

## Applications in Engineering

### 1. **Distributed Network Monitoring**
- Estimate network properties (cycle detection, bottlenecks) without centralized collection
- Deploy monitoring agents (sources) only at strategic locations rather than everywhere
- Relevant for IoT networks and sensor networks with limited bandwidth

### 2. **Graph Property Computation in Distributed Systems**
- **Girth estimation**: Essential for understanding redundancy in network topologies
- Directly applicable to:
  - Reliability analysis of distributed systems
  - Network resilience assessment
  - Cycle detection in dependency graphs (software engineering)

### 3. **Approximation Algorithms for Network Design**
- When exact girth is computationally expensive, source detection provides tunable approximations
- Enables time-quality tradeoffs in network optimization
- Used in designing fault-tolerant communication networks

### 4. **Load Balancing in Parallel Computing**
- Sources correspond to sampling points for load inference
- Distributed algorithms can estimate congestion/bottlenecks efficiently
- Reduces communication overhead compared to centralized approaches

### 5. **Wireless and Mobile Networks**
- Detect cycles (feedback loops) in ad-hoc routing topologies
- Identify shortest paths for quality-of-service (QoS) guarantees
- Work efficiently with dynamic network topologies where $D$ may be small

## Common Mistakes / Pitfalls

### 1. **Confusing Coverage with Proximity**
**Mistake:** Assuming a source "near" a cycle automatically covers it.
**Reality:** A source covers a cycle $C$ only if it is among the $k$ closest sources *for every single vertex* in $C$. A source that is close to one vertex of $C$ might be far from another.

### 2. **Underestimating the Sampling Probability**
**Mistake:** Using probability $p$ too small (e.g., $p