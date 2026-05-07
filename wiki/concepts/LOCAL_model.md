# LOCAL model

## Definition

The **LOCAL model** is a theoretical framework for analyzing **distributed algorithms** on networks, particularly for graph problems. In this model:

- A network is represented as an undirected graph $G = (V, E)$ with $n = |V|$ vertices
- Each vertex is a computational agent that operates **synchronously** in discrete rounds
- In each round, a vertex can:
  - Send arbitrary messages to all its neighbors
  - Receive messages from all its neighbors
  - Perform unlimited local computation
- **Runtime** is measured in the number of rounds until all vertices output their final answer and halt
- Vertices have **unique identifiers** but no global knowledge of the graph structure

The LOCAL model abstracts away **communication complexity** (message sizes are unlimited) and focuses on **time complexity** (number of synchronous rounds).

### Formal Runtime Notation

For a graph with $n$ vertices and maximum degree $\Delta$:

$$T_{\text{LOCAL}}(n, \Delta) = \text{number of rounds to solve problem}$$

Common bounds use $\tilde{O}(\cdot)$ notation (suppressing polylogarithmic factors):
- $\tilde{O}(\log^k n)$ — polylogarithmic in $n$
- $O(\log^* n)$ — iterated logarithm (extremely slow-growing)

## Key Equations

### Derandomization Trade-off

A central result in LOCAL theory (used in the source material):

$$T_{\text{deterministic}} = O\left((T_{\text{randomized}} + V_{\text{verification}}) \cdot T_{\text{decomposition}}\right)$$

where:
- $T_{\text{randomized}}$ = runtime of the randomized algorithm
- $V_{\text{verification}}$ = rounds needed to verify a solution is correct
- $T_{\text{decomposition}}$ = rounds to compute a network decomposition

### Degree Reduction in Iterative Coloring

From Lemma 5.1, after one random color trial:

$$\deg_R(v) \leq \max\left\{\left(1 - \frac{1}{180}\right) \deg_H(v), \Delta^{1/10}\right\} \quad \text{w.h.p.}$$

This exponential decay (constant-factor reduction per round) drives convergence of iterative coloring algorithms.

## Physical Intuition / Derivation

### Why the LOCAL model matters

In distributed systems (networks, sensor arrays, multi-agent systems), **communication is expensive** but **local computation is free**. The LOCAL model captures this asymmetry by measuring only synchronous rounds. A $T$-round LOCAL algorithm means:

> Information propagates outward from each vertex at a rate of one hop per round (bounded by the network diameter).

For a problem with a local structure (e.g., graph coloring), we can exploit the fact that a vertex's decision may only depend on vertices within distance $T$ (its $T$-hop neighborhood).

### Example: Graph Coloring

To color a vertex $v$ with $\Delta$ colors when neighbors are uncolored:

1. **Naive approach** (LOCAL model): Wait for all neighbors to color themselves → propagates color information hop-by-hop → $O(\text{diam}(G))$ rounds in worst case

2. **Smart approach**: Use probabilistic rounding or algebraic techniques to exploit local degree structure → reduce to $\tilde{O}(\log \Delta)$ rounds even on hard graphs

The source material demonstrates **derandomization**: converting a fast randomized LOCAL algorithm ($\tilde{O}(\log^4 \log n)$ rounds) into a deterministic one ($\tilde{O}(\log^2 n)$ rounds) by composing with network decomposition.

### Slack and the Coloring Pipeline

The Π-ous property ("slack") is key: if a vertex has degree $d$ but is allowed to use $d + \text{slack}$ colors, the coloring problem becomes tractable. The algorithm:

1. **Random color trials** reduce uncolored degree exponentially: $d \to (1 - 1/180) d$ per round
2. Once degree drops below some threshold (e.g., $\Delta^{1/10}$), **multi-color trials** finish rapidly
3. **Slack conservation** (Property CC) ensures all internal structure remains valid

## Applications in Engineering

### 1. **Distributed Network Algorithms**
- Scheduling in wireless sensor networks (MAC layer)
- Task assignment in multi-robot systems
- Load balancing in peer-to-peer networks

### 2. **Graph Processing Systems**
- Distributed graph databases (partitioning and coloring for locality)
- MapReduce-style frameworks (vertex-centric computing like Apache Giraph)

### 3. **Resource Allocation**
- Channel assignment in cellular networks
- Register allocation in compilers (analogous problem on interference graphs)

### 4. **Theoretical Computer Science**
- Lower bounds: Proving problems *cannot* be solved faster than $T$ rounds (via covering/packing arguments)
- Algorithm design: Finding optimal algorithms for distributed decision problems

### 5. **Consensus & Synchronization**
- Clock synchronization in distributed systems
- Agreement protocols with Byzantine robustness

## Common Mistakes / Pitfalls

### 1. **Confusing LOCAL with CONGEST**
- **LOCAL**: Messages of unlimited size
- **CONGEST**: Messages limited to $O(\log n)$ bits
- Many LOCAL algorithms do *not* immediately transfer to CONGEST!

### 2. **Ignoring the Synchronous Assumption**
- LOCAL assumes **perfect synchrony** (all vertices execute in lockstep)
- Real networks have asynchronous, variable-delay communication
- A $T$-round LOCAL algorithm may require $O(T \cdot D)$ wall-clock time where $D$ is max network delay

### 3. **Assuming Lower Bounds Transfer**
- A $\Omega(\log^* n)$ lower bound in LOCAL does *not* imply the problem is hard in CONGEST or in asynchronous models
- Different models have different barrier problems

### 4. **Misunderstanding "w.h.p." (with high probability)**
- Lemma 5.1 states properties hold "w.h.p." 
- This typically means