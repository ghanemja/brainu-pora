# Distributed Graph Representation

## Definition

**Distributed graph representation** is a memory-efficient scheme for storing graph structure (particularly trees and subgraphs) across a network where vertices have limited local storage. Rather than requiring each vertex to maintain complete knowledge of all adjacent edges, the representation only requires that **for every edge $e = \{u,v\}$ in the represented subgraph $G'$, at least one endpoint (either $u$ or $v$) stores knowledge of that edge**.

Formally, for a vertex $v' \in V'$, let $E'_{v'}$ denote the set of edges in $E'$ that $v'$ knows about:

$$\bigcup_{v' \in V'} E'_{v'} = E'$$

This is weaker than the "full" representation where every vertex knows all adjacent edges:

$$E'_{v'} \supseteq \{e \in E' : e \text{ is incident to } v'\}$$

### Special Cases for Rooted Trees

For rooted trees, stricter conditions enable efficient convergecast (upward aggregation):
- Every parent-child edge $e = (u, v)$ must be known to the child $v$
- Each parent vertex must store the count of its children
- Each vertex may store a parent pointer (the edge connecting it to its parent's information source) using $O(\log n)$ bits

## Key Equations

**Space Complexity:**
$$\text{Memory per vertex: } O(\log n) \text{ bits}$$

**Broadcast & Convergecast Complexity:**
$$\begin{align}
\text{Time complexity: } &O(D) \text{ rounds (where } D \text{ is tree diameter)}\\
\text{Message complexity: } &O(n) \text{ messages}\\
\text{Local storage: } &O(\log n) \text{ bits per vertex}
\end{align}$$

## Physical Intuition / Derivation

### Why Asymmetric Knowledge Suffices

The key insight is that **each edge only needs to exist in one endpoint's memory**, not both:

1. **Broadcast phase**: A source vertex $w$ sends a message over all edges in $E'_w$ it knows about. Upon receiving a broadcast message, any vertex $u$ automatically forwards it in the next round over its known edges $E'_u$.

2. **Convergecast phase**: In a rooted tree, the edge structure naturally directs information flow. A child vertex $v$ knows its parent edge $(u,v)$, so it can reliably send aggregated results upward. The parent doesn't need to "remember" each child edge—it simply waits for messages from all children.

3. **Request buffering**: The protocol uses edges as memory buffers. During initialization, vertices send "requests" over their known tree edges. These requests persist in the buffer without needing repeated transmission, enabling subsequent broadcasts to be routed correctly.

### Why $O(\log n)$ Bits is Sufficient

- **Vertex IDs**: $\log n$ bits to identify parent or information source
- **Child count**: At most $\log n$ bits to represent the number of children
- **Path reconstruction**: One parent pointer per vertex to retrace paths in aggregation queries

The logarithmic bound leverages the tree structure: each vertex needs only constant metadata, and tree properties (no cycles, $n-1$ edges for $n$ vertices) prevent exponential state growth.

## Applications in Engineering

### 1. **Distributed Algorithms on Networks**

- **Minimum spanning tree (MST) computation**: The GHS (Gallager-Humblet-Spira) algorithm uses distributed tree representations to build MSTs with $O(n \log n)$ message complexity
- **Consensus and leader election**: Trees enable reliable broadcast/convergecast for voting and result aggregation in distributed systems

### 2. **Wireless Sensor Networks**

- Sensors have severely limited memory; $O(\log n)$ bits per node is critical for networks with thousands of nodes
- Broadcast (e.g., routing updates) and convergecast (e.g., data aggregation to a sink) are primary operations

### 3. **Fault-Tolerant Computing**

- Tree-based communication for Byzantine fault tolerance requires knowing only incident edges, not global graph topology
- Sparse local representation enables systems to scale to large node counts

### 4. **Internet of Things (IoT)**

- Edge devices maintain minimal routing state using distributed tree representations
- Multicast and aggregation queries (e.g., "sum sensor values across cluster") execute in $O(D)$ rounds over logarithmic-sized state

### 5. **Peer-to-Peer (P2P) Networks**

- Overlay tree construction (e.g., for streaming or DHT tree-repair) requires each peer to know only a few incident edges
- Gossip and aggregation protocols become feasible with $O(\log n)$ memory per peer

## Common Mistakes / Pitfalls

### 1. **Confusing "Asymmetric Knowledge" with Asymmetric Edges**

❌ **Wrong**: Assuming $E'_u$ contains undirected edges known only at $u$, creating a directed graph.  
✓ **Correct**: $E'_u$ stores that edge $\{u,v\}$ exists, but $v$ may also know it (via $E'_v$). The edge itself remains undirected; only knowledge is asymmetric.

### 2. **Overestimating Memory Savings**

❌ **Wrong**: Claiming that compact representation saves $50\%$ memory (factor of 2).  
✓ **Correct**: For a tree, the dominant cost is storing edge pointers. Compact representation still requires $O(1)$ or $O(\log n)$ metadata per edge in worst case. The asymmetry matters more when comparing to full adjacency list storage.

### 3. **Forgetting the Rooted Tree Requirement**

❌ **Wrong**: Applying child-knows-parent-edge rule to unrooted trees.  
✓ **Correct**: For convergecast in rooted trees, children must know parent edges; for unrooted trees, symmetric knowledge is safer.

### 4. **Ignoring the "Request Buffer" Protocol**

❌ **Wrong**: Assuming vertices must re-broadcast requests every round.  
✓ **Correct**: Edges act