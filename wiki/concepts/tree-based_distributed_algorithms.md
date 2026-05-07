# Tree-Based Distributed Algorithms

## Definition

Tree-based distributed algorithms are coordinate-free communication protocols executed over spanning trees embedded in a network graph. They decompose global communication tasks (such as broadcast and convergecast) into hierarchical phases that route messages through tree edges, avoiding the need for centralized knowledge of network topology.

**Key characteristic**: Vertices require only local knowledge of tree structure (parent/children relationships and routing labels), enabling scalable communication in large networks without global state.

## Key Equations

### Time Complexity
$$T_{\text{broadcast}} = O\left((d(T) + K_b) \log n + D_b\right) \text{ rounds}$$

where:
- $d(T)$ = depth of the backbone spanning tree $T$
- $K_b$ = number of subsets in the broadcast partition
- $D_b$ = maximum depth of intrinsic subtrees
- $n$ = number of vertices
- $\log n$ factor arises from $O(\log^2 n)$-bit routing labels

### Message Complexity
$$M_{\text{broadcast}} = O(d(T) \cdot K_b \log n + n) \text{ messages}$$

### Memory Complexity per Vertex
$$\text{Mem}_{\text{vertex}} = O(\log^2 n) \text{ bits}$$

## Physical Intuition / Derivation

### Two-Phase Communication Model

Tree-based algorithms decompose distributed tasks into **extrinsic** and **intrinsic** phases:

#### Extrinsic Phase (Backbone Routing)
Messages traverse a coarse backbone tree $T$ connecting fragment representatives. This phase involves:
- **Upward path**: Messages ascend from leaves to tree root $r_T$ via parents
- **Downward path**: Replies descend from root back to destinations

The extrinsic phase works because:
1. Any two vertices can communicate via their lowest common ancestor (LCA) in $T$
2. Routing labels (of size $O(\log^2 n)$) encode sufficient path information to reach LCA
3. Tree structure guarantees loop-free, deadlock-free delivery

**Time cost**: $2d(T)$ hops for round-trip, multiplied by $O(\log n)$ message expansion rounds when labels are large.

#### Intrinsic Phase (Local Broadcasts)
Once backbone routing completes, messages are broadcast locally within disjoint fragment subtrees:
- No routing labels needed (messages stay within known tree)
- Simpler $O(\log n)$-bit message format
- Requires $O(D_b)$ rounds where $D_b$ is max subtree depth

**Why separation helps**: Intrinsic phase avoids long-label overhead by reusing already-established tree structure for local propagation.

### Why $O(\log^2 n)$ Routing Labels?

In a network with up to $n$ vertices, routing labels must encode:
- **Destination ID**: $O(\log n)$ bits
- **LCA path encoding**: $O(\log n)$ bits (to specify which of $O(n)$ possible paths to take)
- Total: $O(\log^2 n)$ bits per label

### Memory Efficiency

Per-vertex memory is dominated by routing label storage, not message buffering. The root $r_T$ only stores one message at a time ($O(\log n)$ bits), while all other vertices store static routing tables ($O(\log^2 n)$ bits).

## Applications in Engineering

### 1. **Distributed Systems & Cloud Computing**
- **Gossip protocols over DHT rings**: Tree structures reduce broadcast storms from $O(n^2)$ to $O(n \log n)$ messages
- **Hierarchical consensus** (e.g., Raft with multi-level leader election): Uses backbone trees to elect regional coordinators before global consensus

### 2. **Wireless Sensor Networks**
- **Multi-hop broadcasts**: Avoid flooding; use backbone tree to reach all clusters in $O(d(T))$ rounds instead of $O(n)$ random-walk steps
- **Energy efficiency**: Directed tree routing consumes far less power than broadcast to all neighbors

### 3. **Network Routing Protocols**
- **Spanning Tree Protocol (STP)**: Uses tree-based forwarding to prevent loops in Ethernet switches
- **OSPF/IS-IS**: Compute shortest-path trees for scalable IP routing

### 4. **Parallel Computing**
- **All-reduce in MPI**: Tree-based reduction (e.g., binary tree) achieves $O(\log p)$ stages for $p$ processes
- **Collective communication**: Broadcast and gather operations in distributed training (PyTorch distributed, Horovod)

### 5. **Peer-to-Peer Networks**
- **BitTorrent piece distribution**: Overlay network organizes peers into tree-like structures to reduce redundant uploads
- **Streaming (IPTV, video CDNs)**: Multicast trees minimize bandwidth on backbone links

## Common Mistakes / Pitfalls

### 1. **Confusing Extrinsic and Intrinsic Phases**
**Mistake**: Assuming intrinsic broadcast depth $D_b$ is included in backbone routing time.
**Reality**: The two phases have different message formats and traverse different graph structures. Time complexity is *additive*, not multiplicative: $O((d(T) + K_b) \log n + D_b)$, not $O((d(T) + K_b) \log n \cdot D_b)$.

### 2. **Ignoring Routing Label Overhead**
**Mistake**: Claiming message complexity is $O(d(T) \cdot K_b)$ without accounting for label size.
**Reality**: Large routing labels inflate each message; the $\log n$ factor in $O(d(T) \cdot K_b \log n)$ is unavoidable unless you use implicit routing (which increases memory or latency elsewhere).

### 3. **Assuming Optimal Backbone Tree**
**Mistake**: Using an arbitrary spanning tree and expecting $d(T) = O(\log n)$.
**Reality**: Tree depth can be $\Theta(n)$ in the worst case (e.g., a line graph). Must explicitly construct shallow trees (e.g., BFS trees, which guarantee $d(T) = O