# Distributed Aggregation

## Definition

**Distributed aggregation** is a fundamental distributed computing operation in which information (values, statistics, results) from all vertices in a network must be collected and combined (aggregated) efficiently while respecting the topology and communication constraints of the system.

In the context of graph algorithms, distributed aggregation typically operates over a **spanning tree** that covers a communication graph $G = (V, E)$. The aggregation process requires:

1. **Tree structure**: A spanning tree $T$ of the communication graph where every vertex knows:
   - The overall tree depth $d(T)$
   - Its own depth $d(v)$ in $T$
   
2. **Routing infrastructure**: A tree-routing scheme where each vertex $v$ knows:
   - Its own routing label $\text{lbl}_v$
   - The routing label of its base fragment leader
   
3. **Fragment organization**: The network is partitioned into **base fragments** $B$, each with:
   - A unique slot number from $[1, \ldots, K_b]$
   - A spanning subtree $T_B$ of depth bounded by $D_b$

The goal is to compute aggregate functions (sum, max, min, average, etc.) across the distributed network with minimal time, messages, and memory overhead.

---

## Key Equations

**Time Complexity:**
$$T_{\text{setup}} = O\left((D + \sqrt{n}) \log n\right) \text{ rounds}$$

where $D$ is the diameter of the graph and $n$ is the number of vertices.

**Message Complexity:**
$$M_{\text{setup}} = O(m + n \log n) \text{ messages}$$

where $m$ is the number of edges.

**Memory Complexity (per vertex):**
$$S = O(\log^2 n) \text{ bits}$$

**Fragment Parameters** (achieved after $O(\log n)$ phases):
- Number of base fragments: $K_b = O\left(\min\left\{\frac{n}{D}, \sqrt{n}\right\}\right)$
- Spanning tree diameter: $D_b = O\left(\max\left\{D, \sqrt{n}\right\}\right)$

---

## Physical Intuition / Derivation

### Why Distributed Aggregation is Hard

In a centralized system, aggregation is trivial: send all data to one location. In distributed systems, several challenges arise:

1. **No single point of collection**: Data is scattered across the network; vertices cannot simultaneously communicate with a central authority.

2. **Communication cost dominates**: Each message sent consumes resources. The total number of messages directly impacts runtime and energy in real networks.

3. **Topology constraints**: Vertices can only communicate with neighbors. Information must travel through intermediate nodes, and routing becomes non-trivial.

### The Tree-Based Solution

The source material describes a **tree-based aggregation** approach:

**Phase 1: Setup (Prerequisites)**
- Construct a **BFS tree** from some root: $O(D)$ rounds, establishing known structure
- Establish **tree-routing labels**: Each vertex learns how to reach fragment leaders via tree paths
- Allocate **slot numbers**: Organize fragments and assign contiguous time slots

The BFS tree is critical because:
- Tree paths are unique, avoiding loops
- Tree depth is $O(D)$, minimizing hop count
- All vertices share knowledge of the tree structure

**Phase 2: Aggregation Execution** (not detailed in source, but implied)
- Once setup is complete, aggregate values flow **bottom-up** through the tree
- Leaves contribute their local values
- Internal nodes combine (aggregate) values from their children
- Root eventually holds the global aggregate

**Why the Complexity Bounds Hold:**

- **Time**: $O(D)$ for BFS (one BFS wave per tree level) + $O(D \log n)$ for routing setup (tree routing with $O(\log n)$-bit labels over depth $D$) + $O((D + \sqrt{n})\log n)$ for leader broadcast
  
- **Messages**: $O(m)$ for BFS (each edge examined once) + $O(n \log n)$ for broadcasts (each node sends $O(\log n)$-bit message on tree, $n$ nodes)

- **Memory**: Each vertex stores $O(\log n)$-bit values (parent, children count, slot number) plus $O(\log^2 n)$-bit routing label for itself and fragment leader

### Fragment-Based Optimization

Rather than aggregating directly over $T$, the algorithm partitions into fragments with:
- $K_b = O(\min\{n/D, \sqrt{n}\})$ fragments (roughly balanced in number of nodes)
- $D_b = O(\max\{D, \sqrt{n}\})$ depth per fragment tree

This balancing ensures that:
- No single fragment dominates the aggregation time
- Total time is not worse than naive tree aggregation
- The Lenzen phase technique (applied $O(\log n)$ times) progressively refines fragments

---

## Applications in Engineering

### 1. **Wireless Sensor Networks**
Aggregate sensor readings (temperature, humidity, pressure) from distributed nodes to a sink node. Distributed aggregation minimizes message transmissions, extending battery life.

### 2. **Distributed Machine Learning**
In parameter servers and federated learning, distributed aggregation collects gradient updates from worker nodes to perform collective model updates. The memory and message bounds ensure scalability.

### 3. **Distributed Consensus & Fault Tolerance**
Leader election algorithms (like RAFT, Paxos) use aggregation to count votes and determine majority consensus. Fragment-based aggregation provides fault tolerance by grouping votes into quorums.

### 4. **Network Monitoring & Performance Analysis**
Collect statistics (packet counts, latency metrics, error rates) from all routers/switches in a large network to compute global network health indicators.

### 5. **Graph Analytics at Scale**
Computing graph metrics (connectivity, centrality, community detection) on large distributed graphs requires aggregation of local computations (e.g., summing path lengths).

### 6. **Distributed Minimum Spanning Tree (MST)**
The source context emphasizes MST construction. Aggregation is used to verify edge weights and determine global minimum, which is required for building the spanning tree fragments.

---

##