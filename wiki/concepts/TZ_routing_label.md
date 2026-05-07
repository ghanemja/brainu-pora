# TZ Routing Label

## Definition

A **TZ routing label** is a compact routing scheme for tree-based networks, named after Thorup and Zwick. For a vertex $v \in V$ in a rooted tree $T$, the routing label consists of:

1. **Compressed path information**: A sequence of edges from the tree root to $v$, reduced from $O(D)$ edges (where $D$ is tree diameter) to $O(\log n)$ edges by selectively omitting edges
2. **Vertex number**: A unique identifier for $v$
3. **Subtree interval**: An associated interval for the subtree rooted at $v$

The key innovation is **heavy-edge omission**: an edge from parent $u$ to child $v$ is omitted from the label if the subtree rooted at $v$ contains at least half the nodes of the subtree rooted at $u$. Each vertex has at most one such omissible edge.

## Key Equations

**Label and Table Sizes:**
$$\text{Label size} = O(\log^2 n) \text{ bits}$$
$$\text{Routing table size} = O(\log n) \text{ bits}$$

**Setup Complexity (CONGEST Model):**
$$\text{Time complexity} = O(D \log n)$$
$$\text{Message complexity} = O(n \log n)$$

**Depth Separation (Convergecast):**
$$t = i + d(T) - d(v)$$

where:
- $t$ = round number
- $i$ = fragment identifier  
- $d(T)$ = depth of tree
- $d(v)$ = depth of vertex $v$

## Physical Intuition / Derivation

### Why Compression Works

In a tree of $n$ vertices with depth $D$, a naive path label storing all edges requires $O(D)$ space. However, most trees have logarithmic depth: $D = O(\log n)$. The TZ scheme exploits **depth balance** further.

**Heavy-Edge Decomposition**: By omitting edges leading to "heavy" subtrees (those containing $\geq 50\%$ of parent's nodes), we drastically reduce label size:

- Following any path from root to leaf, we can encounter **at most $\log n$ light edges** (edges not omitted)
- This is because each time we traverse a light edge, the subtree size drops to $< 50\%$
- After $\log n$ halvings, subtree size reaches 1 (a leaf)

**Result**: The compressed path contains $O(\log n)$ edges instead of $O(D)$ edges.

### Convergecast Congestion Avoidance

The depth separation formula $t = i + d(T) - d(v)$ ensures that for each fragment $F_i$:
- Different fragments perform aggregation at different depths in each round
- A vertex $v$ receives messages for fragment $F_i$ in exactly **one round** at depth $d(v) = d(T) - t + i$
- This prevents queuing and congestion by temporally staggering convergecast operations across the tree height

## Applications in Engineering

### 1. **Distributed Computing & CONGEST Model**
- Enables efficient routing in large-scale distributed systems without maintaining full routing tables at each node
- Critical for networks where $n$ can reach millions but node memory is limited

### 2. **Wireless & Ad-Hoc Networks**
- Reduces storage overhead in memory-constrained devices (sensors, IoT nodes)
- Balances lookup time ($O(\log^2 n)$ bit complexity) against label storage

### 3. **Tree-Based Aggregation & Sensor Networks**
- Depth separation scheduling ensures convergecast operations (gathering sensor data to a root) complete without congestion
- Example: Environmental monitoring networks collecting distributed sensor readings

### 4. **Hierarchical Network Routing**
- Applicable to hierarchical routing protocols in internet-scale networks
- Heavy-edge decomposition mirrors natural network topology (backbone vs. edge networks)

### 5. **Compile-Time Network Code Generation**
- Setup performed once; labels pre-computed and distributed with minimal message overhead ($O(n \log n)$)
- Suitable for static or slowly-changing network topologies

## Common Mistakes / Pitfalls

### 1. **Confusing Light/Heavy Edge Orientation**
**Error**: Thinking heavy edges are omitted (they're not). 
**Correction**: Only edges to heavy subtrees ($\geq 50\%$ of parent) are omitted. Light edges must be retained to reach smaller branches.

### 2. **Assuming Linear Space Savings**
**Error**: Believing compression reduces labels from $O(D)$ to $O(D/2)$.
**Correction**: The savings are **logarithmic**—from $O(D)$ to $O(\log n)$—because heavy-edge elimination creates exponential decay in subtree sizes.

### 3. **Misapplying to General Graphs**
**Error**: Attempting to use TZ labels on arbitrary (non-tree) graphs.
**Correction**: The scheme fundamentally relies on tree structure; generalization to general graphs requires different techniques.

### 4. **Overlooking Setup Cost**
**Error**: Ignoring $O(D \log n)$ time and $O(n \log n)$ messages needed to build labels.
**Correction**: Setup is non-negligible; cost is amortized only if routing persists for many operations or if dynamic updates are infrequent.

### 5. **Depth Separation Timing**
**Error**: Assuming convergecast fragments can run simultaneously.
**Correction**: Fragments must strictly follow the schedule $t = i + d(T) - d(v)$ to achieve congestion-free execution; violations cause collisions.

## See Also

- [[Heavy-Light Decomposition]] — foundational tree partitioning technique underlying TZ labels
- [[Distributed Routing Schemes]] — broader class of compact routing methods
- [[CONGEST Model]] — distributed computing framework where TZ routing is analyzed
- [[Tree Convergecast]] — aggregation protocol using depth-separated schedules
- [[Thorup-Zwick Distance Oracle]] — related distance labeling scheme by same authors

## Sources

- Source material: TZ routing label definition, convergecast