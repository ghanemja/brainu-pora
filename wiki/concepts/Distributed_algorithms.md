# Distributed Algorithms

## Definition

A **distributed algorithm** is a computational procedure that executes on a network of autonomous processors (nodes/vertices) with the following characteristics:

- **Decentralized execution**: Each node runs the same or similar local algorithm without central coordination
- **Local communication**: Nodes exchange information only with neighbors in the network graph
- **Asynchronous or synchronous operation**: Nodes may operate independently or in synchronized rounds
- **Finite memory per node**: Each processor has limited local storage (typically $O(\log n)$ bits for $n$ nodes)
- **No global state**: Nodes lack knowledge of the complete network topology initially

In the **clean network model**, at the start of computation each vertex knows only:
- Its own unique identifier
- The identities of its immediate neighbors
- Edge weights (if applicable)

Distributed algorithms are fundamentally different from parallel algorithms: they must function correctly despite communication delays, limited bandwidth, and partial information.

## Key Equations

### Complexity Measures

For a distributed algorithm on graph $G = (V, E)$ where $n = |V|$ and $m = |E|$:

**Time complexity**: 
$$T(n, D) = \text{number of synchronous communication rounds}$$

where $D$ is the network diameter (maximum shortest path distance).

**Message complexity**: 
$$M(n, m) = \text{total number of messages exchanged across all edges}$$

**Memory complexity per node**: 
$$\text{Space} = O(\log n) \text{ to } O(n)$$

### Lower Bounds for MST

For deterministic algorithms in the clean network model:
$$M_{\text{lower}} = \Omega(m) \text{ messages (required)}$$

For time complexity:
$$T_{\text{lower}} = \tilde{\Omega}(\sqrt{n}) \text{ rounds (near-optimal)}$$

The $\tilde{\Omega}$ notation hides polylogarithmic factors.

## Physical Intuition / Derivation

### Why Distributed Algorithms Are Hard

Consider computing a minimum spanning tree (MST) in a distributed setting:

1. **Information locality**: A node at one end of the network cannot directly observe edges at the other end. Information must propagate through intermediate nodes.

2. **Communication bottleneck**: Each edge can carry only one message per round in the synchronous model. With $m$ edges and potentially $O(m)$ messages needed, time scales as $M/m$ rounds minimum.

3. **Coordination paradox**: To find the global MST, nodes must collectively make decisions about which edges to include, yet no single node sees the full picture. The algorithm must grow the tree locally while respecting global optimality.

### Three Classical Algorithm Families for MST

**1. GHS-type algorithms** (Gallager-Humblet-Spira)
- Strategy: Grow connected components, merge smallest edges between components
- Time: $O(n \log n)$ — linear in vertices (slow for large, sparse networks)
- Messages: $O(m + n \log n)$ — near-optimal
- Memory: $O(\log n)$ per node — optimal
- Reason for slowness: Sequential merging of components; even if diameter $D \ll n$, algorithm takes $\Omega(n)$ rounds

**2. GKP-type algorithms** (Garay-Kutten-Peleg)
- Strategy: Hierarchical decomposition; local MSTs merged with exponential speedup
- Time: $O(D + \sqrt{n} \log^* n)$ — near-optimal
- Messages: $O(m + n^{3/2})$ — suboptimal
- Memory: $O(n)$ or more per node — prohibitive for large networks
- Reason for memory use: Must maintain spanning forests of larger and larger diameter

**3. Recent algorithms** [Elkin et al., 2020s]
- Strategy: Hybrid approaches combining speed and memory efficiency
- Time: $O(D + \sqrt{n} \text{poly}(\log n))$ — near-optimal
- Messages: $O(m + n \log n)$ — optimal
- Memory: $O(\log n)$ per node — optimal
- Innovation: Clever scheduling avoids storing large auxiliary structures

### Intuition for the $\tilde{\Omega}(\sqrt{n})$ Lower Bound

Why can't we do better than $\sqrt{n}$ rounds?

- In $t$ rounds, a node can directly/indirectly communicate with nodes at distance $\leq t$
- Information from a distance-$d$ node takes $\geq d$ rounds to arrive
- The diameter spans the network; effective diameter for global consensus is $\Theta(\sqrt{n})$ in adversarial topologies
- Peleg-Rubinovich proved this is tight via information-theoretic arguments

## Applications in Engineering

### Network Routing and Protocol Design
- **OSPF/IS-IS protocols**: Distributed shortest-path tree computation
- **Consensus algorithms**: Byzantine fault-tolerant distributed consensus (Paxos, Raft)
- **Ad-hoc networks**: Mobile nodes must compute connected structures without infrastructure

### Sensor Networks
- **Data aggregation**: Minimize energy by computing aggregate sums/counts efficiently
- **Topology management**: Maintain sparse connected subgraphs (spanners, clustering)
- **Time synchronization**: Distributed clock synchronization with limited communication

### Cloud and Distributed Systems
- **MapReduce/Spark**: Distributed graph processing frameworks rely on algorithms similar to MST for partition coordination
- **Sharding decisions**: Hash-based or topology-aware data distribution
- **Fault detection**: Distributed monitoring of system health

### Social Networks and Blockchain
- **Peer-to-peer networks**: Bitcoin/Ethereum nodes execute distributed consensus
- **Community detection**: Distributed clustering algorithms
- **Broadcast protocols**: Efficient message propagation in unstructured P2P networks

### Control and Coordination
- **Robotic swarms**: Distributed decision-making without central authority
- **Power grid optimization**: Distributed control of generation and load balancing
- **Traffic network control**: Decentralized coordination at intersections

## Common Mistakes / Pitfalls

### 1. Confusing Time Complexity with Message Complexity
**Mistake**: Assuming fewer messages means faster execution.
- **Reality**: $O(n \log n)$ messages can be sent in $O