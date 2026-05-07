# Distributed MST

## Definition

**Distributed Minimum Spanning Tree (Distributed MST)** is the problem of computing a minimum spanning tree of a graph in a *distributed* setting, where:

- **Vertices are autonomous processors** that can communicate only with their neighbors in the graph
- **No vertex has global knowledge** of the network topology
- **Computation proceeds in synchronous rounds**, where each round permits:
  - Local computation at each vertex
  - Exchange of messages with neighbors
  - Storage in local memory (subject to constraints)

The goal is to determine which edges belong to the MST through **local-to-global coordination**, minimizing communication complexity (total messages), time complexity (rounds), and memory complexity (space per vertex).

### Formal Model
In the standard **LOCAL model** of distributed computing:
- Graph $G = (V, E)$ with $n = |V|$ vertices, diameter $D$
- Each vertex $v$ has a unique identifier and knows its neighbors' identifiers
- A **distributed algorithm** solves MST if every vertex learns which of its incident edges are in the MST
- Complexity measured in: **time** $T$ (rounds), **messages** $M$, **memory** $S$ (bits per vertex)

---

## Key Equations

### Complexity Bounds

**Time-optimal distributed MST:**
$$T = O(D + \sqrt{n})$$

**Message-optimal distributed MST:**
$$M = O(n \log n)$$

**Memory requirements (historical):**
$$S = \Omega(\sqrt{n}) \text{ bits per vertex (many classical algorithms)}$$

**Optimized memory-aware algorithms:**
$$S = \text{polylog}(n) \text{ bits per vertex}$$

---

## Physical Intuition / Derivation

### The Challenge

Unlike centralized MST algorithms (e.g., Kruskal, Prim), distributed MST faces a fundamental tension:

1. **No global view**: Vertices cannot directly compare all edge weights globally
2. **Communication bottleneck**: Bandwidth is limited to neighbor-to-neighbor links
3. **Synchronization overhead**: Agreeing on decisions requires message rounds proportional to $D$ or $\sqrt{n}$

### Classical Approach: The GHS Algorithm

The foundational **Gallager-Humblet-Spira (GHS) algorithm** illustrates the core strategy:

1. **Build fragments incrementally**: Start with each vertex as a singleton fragment (fragment = partial MST)
2. **Find minimum outgoing edges**: Each fragment finds its minimum-weight edge connecting to another fragment
3. **Merge fragments**: Adjacent fragments merge via their minimum-weight connecting edge
4. **Repeat** until one global tree remains

**Why memory explodes**: After $k$ GHS iterations, fragment count drops from $n$ to roughly $n/2^k$. However, to efficiently route messages about which edges connect fragments, algorithms construct a **BFS tree $T$** and store information about $\Omega(\sqrt{n})$ fragments at various vertices (especially the root of $T$).

### Modern Refinements

Recent algorithms (Haeupler et al., and others) avoid the $\Omega(\sqrt{n})$ memory requirement by:
- Using **asynchronous gossip** rather than tree-based broadcasts
- Employing **randomization** to break symmetry without storing fragment metadata
- Reducing per-vertex state to **polylogarithmic** rather than polynomial in $n$

---

## Applications in Engineering

### 1. **Wireless Sensor Networks**
- Sensors have **severely limited battery and memory**; distributed MST forms a backbone for energy-efficient routing
- Avoids concentrating all routing information at a sink node

### 2. **Ad-Hoc Mobile Networks**
- Nodes have **transient connectivity**; the MST provides a minimal-cost spanning topology that updates dynamically
- Distributed algorithms allow each node to compute locally without waiting for global agreement

### 3. **Biological Cell Networks & Bio-Inspired Computing**
- Cells communicate via **chemical signals** with spatial locality (only with neighbors)
- Distributed MST models emergence of efficient resource-sharing hierarchies
- **Constant-memory randomized algorithms** motivated by biological constraints

### 4. **Smart Grids and Power Distribution**
- Minimize transmission losses by computing MST over power network in a decentralized manner
- Vertices = substations; edges = power lines; weights = loss or cost

### 5. **Distributed Databases**
- Computing MST over replica placement graphs to minimize replication cost
- Each database node decides locally which replicas to maintain

### 6. **Massive Parallel Computation (MPC) Model**
- Modern cloud platforms (MapReduce-style) distribute graph processing; MST requires coordinating across machines with limited communication rounds

---

## Common Mistakes / Pitfalls

### 1. **Confusing "Distributed" with "Parallel"**
- Distributed MST assumes **restricted local communication** (only with neighbors)
- Parallel algorithms assume **global shared memory** or all-to-all communication
- These require fundamentally different algorithmic approaches

### 2. **Underestimating Memory Overhead**
- The "supergraph" approach (fragments as vertices) requires storing Ω(√n) state *per vertex in worst case*
- For wireless sensors, this can exceed total available RAM
- **Pitfall**: Assuming an algorithm is "distributed" = memory-efficient; many classic distributed MST algorithms are not

### 3. **Ignoring the Diameter Bottleneck**
- Time complexity $O(D + \sqrt{n})$ suggests time scales with **network diameter**
- In a line graph ($D = n-1$), even optimal algorithms take $\Omega(n)$ rounds
- Cannot always achieve sublinear time in $n$ without assumptions on $D$

### 4. **Message Complexity vs. Total Bits Sent**
- A "message" is typically one unit; but if each message contains $O(\log n)$ bits of ID information, total bits = $O(n \log^2 n)$
- **Pitfall**: Optimizing message count while ignoring bit complexity

### 5. **Assuming Synchronous Rounds**
- Standard analysis assumes **lock-step synchronous rounds**
- **Real networks are asynchronous**; actual implementations require careful handling of message delays and ordering
- Some recent algorithms trade synchrony assumptions for better