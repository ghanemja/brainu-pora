# upcast

## Definition

An **upcast** is a directed communication operation in distributed algorithms that propagates information toward a designated root node along a breadth-first search (BFS) tree structure. In the context of network communication cycles, an upcast carries a message from a source vertex toward the tree root $r_T$, following the parent pointers of the BFS tree in a convergecast pattern.

More formally, given a BFS tree $T$ with root $r_T$ and depth $d(T)$, an upcast in slot $j$ delivers a message to $r_T$ in round $j + d(T)$. The message is structured as a type-content pair: $\langle \text{type}, \text{content} \rangle$, where:
- **type** ∈ {P, Q} indicates whether the message is a *Publishing* (P) or *Query* (Q) operation
- **content** varies by type:
  - For type P: the broadcast message $\text{msg}_i$ from fragment leader
  - For type Q: the routing label $\text{lbl}_B$ identifying a subset root

## Key Equations

**Round arrival time for upcast in slot $j$:**
$$r_{\text{arrival}} = j + d(T)$$

where $d(T)$ is the depth of the BFS tree and $j \in [1, K + K_b]$ (the slot index).

**Query-response latency:**
$$\Delta_{\text{query}} = 2d(T) \text{ rounds}$$

(Query sent and response routed back down the tree)

**Complete extrinsic communication phase:**
$$T_{\text{extrinsic}} = 2d(T) + K + K_b \text{ rounds}$$

**Broadcast cycle complexity (including upcast aggregation):**
- **Time:** $O((d(T) + K) \log n + D_b)$ rounds
- **Messages:** $O((d(T) \cdot K) \log n + n)$ messages
- **Memory:** $O(\log^2 n)$ bits

## Physical Intuition / Derivation

### Why Upcast Matters

In distributed algorithms over networks, computation often requires gathering information from many nodes to a central location. An upcast is the dual operation to a *downcast* (broadcast): while downcast spreads information from root outward, upcast aggregates information from leaves inward.

### Slot Uniqueness Guarantee

The key insight is **slot uniqueness**: messages originating in distinct slots use distinct depths of the tree $T$ in each round. This ensures no collisions at the root—the root $r_T$ receives exactly one message per round from different slots. 

Think of it like a pipeline: slot $i$ carries a message through the tree layer-by-layer, taking exactly $d(T)$ rounds to traverse from leaf to root. If you stagger slots, you guarantee that at each round $t = i + d(T)$, the root receives the payload from slot $i$.

### Message Structure

Messages are **tagged** with their type:
- **Publishing (P)** messages carry actual data (e.g., $\langle P, \text{msg}_i \rangle$) that the root stores in a local variable $\text{msg}_T$
- **Query (Q)** messages are requests $\langle Q, \text{lbl}_B \rangle$ asking the root to respond with its stored message, routed back to subset $B$

This two-message pattern (query + response) implements a request-reply communication idiom across a tree hierarchy.

## Applications in Engineering

### 1. **Distributed Minimum Spanning Tree (MST) Construction**
Upcast operations enable the GKP (Gallagher-Humblet-Spira) algorithm variant for MST construction. Fragments use upcast to report minimum-weight outgoing edges (MWOEs) to a coordinator, which then makes merging decisions. The upcast aggregates local edge information into global decisions.

### 2. **Network Aggregation and Monitoring**
In sensor networks and IoT systems, upcast patterns collect aggregated statistics (sum, max, count, etc.) from leaf nodes to a sink root. This is common in monitoring pipelines where you need to periodically gather network-wide metrics.

### 3. **Hierarchical Consensus Protocols**
Byzantine fault-tolerant and crash-tolerant consensus algorithms use upcast phases to gather votes or attestations from all nodes up a tree hierarchy before the root makes a commitment decision.

### 4. **Wireless Sensor Networks (WSNs)**
In duty-cycled WSNs with convergecast trees, upcast timing (using slots) avoids medium access collisions and ensures the sink receives data without lost packets due to simultaneous transmissions.

### 5. **Datacenter Networking**
In tree-based datacenter architectures (e.g., hierarchical fat trees), upcast patterns are used for aggregation queries and telemetry collection from top-of-rack switches to core switches.

## Common Mistakes / Pitfalls

### 1. **Confusing Upcast with Simple Tree Traversal**
Students often think an upcast is just "sending a message up the tree." In reality, the **slot-based scheduling** is critical: without proper slot assignment, messages collide at intermediate nodes. Slot uniqueness is the mechanism preventing collisions, not just the tree structure.

### 2. **Ignoring Tree Depth in Complexity Analysis**
A common error is omitting the $d(T)$ term from latency estimates. Remember: an upcast in slot $j$ arrives at round $j + d(T)$, not round $j$. This $d(T)$ term is unavoidable and dominates if the tree is deep (e.g., $d(T) = O(\log n)$ in balanced trees, but can be $O(n)$ in worst case).

### 3. **Mixing Upcast and Convergecast**
While related, **convergecast** is a specific pattern of upcast where each non-root node receives from its children, processes locally, and sends up to its parent. An upcast is more general—it may simply forward or aggregate depending on the algorithm.

### 4. **Assuming Upcast is Free**
The message complexity $O((d(T) \cdot K) \log n + n)$ shows that upcast is