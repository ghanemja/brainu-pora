# Distributed Graph Partitioning

## Definition

Distributed graph partitioning is a technique for decomposing a graph $G = (V, E)$ into disjoint subgraphs (fragments) such that local computation can be performed within each partition independently, then coordinated across partition boundaries. In the context of distributed algorithms, partitioning enables:

1. **Locality of computation**: vertices operate only on their partition and adjacent partitions
2. **Memory efficiency**: each vertex stores only $O(\log^2 n)$ bits despite global coordination
3. **Parallel coordination**: multiple partitions process simultaneously with synchronized communication phases

Formally, given a partition $\mathcal{P} = \{P_i\}_{i=1}^{N}$ of vertices $V$, we define:
- **Part ID**: label $P_v$ assigned to vertex $v$ indicating its partition membership
- **Fragment ID**: identifier for connected components within the induced subgraph $H_{\mathcal{P}}$
- **MWOE (Minimum Weight Outgoing Edge)**: the lightest edge connecting vertices in different fragments but the same part

## Key Equations

**Time Complexity per Phase:**
$$T_{\text{phase}} = O\left((D + \sqrt{n}) \cdot \log n \cdot \log^* n\right) \text{ rounds}$$

**Message Complexity per Phase:**
$$M_{\text{phase}} = O\left(m + n\log n \log^* n\right) \text{ messages}$$

**Memory per Vertex:**
$$\text{Memory}_v = O(\log^2 n) \text{ bits}$$

where $D$ is graph diameter and $\log^* n$ is the iterated logarithm.

**Overall Algorithm (Multiple Phases):**
$$T_{\text{total}} = O\left((D + \sqrt{n})(\log^2 n)(\log^* n)\right) \text{ rounds}$$
$$M_{\text{total}} = O\left(m\log n + n\log^2 n \log^* n\right) \text{ messages}$$

## Physical Intuition / Derivation

### Why Partitioning Matters

In distributed algorithms, unconstrained global synchronization is expensive. Partitioning creates a hierarchy:

1. **Local phase**: Each vertex finds its MWOE candidate among edges connecting to neighbors with the same part ID but different fragment ID—this takes only $O(m)$ messages (one round per edge)

2. **Aggregation phase**: Information propagates across the partition via a **Minimum Spanning Forest (MSF)** constructed on $H_{\mathcal{P}}$. The MSF serves as a backbone for convergecast (bottom-up) and broadcast (top-down) operations

3. **Base fragment sizing**: The number of base fragments is chosen as $K_b = \min\{n/D, \sqrt{n}\}$ to balance two regimes:
   - **Dense graphs** ($D$ small): $K_b \approx \sqrt{n}$ fragments, diameter $O(\sqrt{n})$
   - **Sparse graphs** ($D$ large): $K_b \approx n/D$ fragments, diameter $O(D)$

### Memory Efficiency Argument

Each vertex $v$ only stores:
- Its part label $P_v$ (one integer)
- One aggregation input value $x_v$
- MST edges detected in each phase: at most $O(\log n)$ phases, one edge per phase → $O(\log^2 n)$ bits total

This avoids storing the full graph or all neighboring vertices' states, which would require $\Omega(n)$ bits.

### Communication Reduction

In each communication cycle:
- BFS tree depth: $O(D)$ (diameter-bounded exploration)
- Number of subsets: $K_b$
- Messages per cycle: $O(d(T) \cdot K_b \cdot \log n) = O(n\log n)$

The key insight: by limiting partition size to $O(\sqrt{n})$ or $O(D)$, the diameter of each partition is controlled, making tree-based aggregation efficient.

## Applications in Engineering

### 1. **Distributed Minimum Spanning Tree (MST) Computation**
   - Construct MST in networks with $n$ nodes in $O((D+\sqrt{n})(\log^2 n)(\log^* n))$ rounds
   - Essential for network design, backbone construction, and clustering

### 2. **Load Balancing in Distributed Systems**
   - Partition computational graphs to minimize inter-partition communication
   - Reduce synchronization overhead in MapReduce-style systems

### 3. **Sensor Networks**
   - Partition large sensor networks into manageable zones
   - Perform aggregation queries (sum, average, max) with minimal energy overhead
   - Memory constraint: sensors have $O(\log^2 n)$ bits → feasible on microcontrollers

### 4. **Large-Scale Graph Processing**
   - Systems like Pregel, GraphLab rely on graph partitioning for vertex-cut and edge-cut strategies
   - Reduces network bandwidth between machines by localizing computation

### 5. **Telecommunication Networks**
   - Design robust routing structures by partitioning networks into autonomous regions
   - Each region maintains local MSF; global MST emerges from inter-region edges

## Common Mistakes / Pitfalls

### 1. **Confusing Part ID with Fragment ID**
   - **Error**: Treating all vertices with the same part ID as a single connected component
   - **Reality**: A part may contain multiple fragments (disconnected components). MWOE search only considers edges between *different* fragments in the *same* part
   - **Fix**: Maintain separate fragment membership information during each phase

### 2. **Ignoring the $O(\log n)$ Phase Dependency**
   - **Error**: Assuming algorithm finishes in one phase
   - **Reality**: MST construction requires $O(\log n)$ phases because fragment sizes shrink by a constant factor each phase (like binary contraction)
   - **Fix**: Account for logarithmic overhead in asymptotic analysis

### 3. **Underestimating Memory for MST Storage**
   - **Error**: Thinking memory is only $O(\log^