# publish-query sets

## Definition

A **publish-query set** is a scheduling mechanism that interleaves convergecast and broadcast operations in distributed tree networks to enable memory-efficient message routing without requiring intermediate nodes to buffer multiple messages.

Formally, in a hierarchical fragment structure where:
- Fragment $F_i$ is rooted at vertex $r_i$ and contains base fragments $B_{i1}, B_{i2}, \ldots$ rooted at vertices $r_{i1}, r_{i2}, \ldots$
- Messages $m_i$ flow from fragment roots to base fragment roots

A publish-query set is a time-slot arrangement that ensures:

1. **Publish phase**: Root $r$ receives message $m_i$ from fragment root $r_i$
2. **Query phase**: Root $r$ immediately receives queries from base fragment roots $\{r_{i1}, r_{i2}, \ldots\}$ that comprise $F_i$
3. **Response phase**: Upon receiving a query, $r$ sends $m_i$ to the requesting base fragment using the routing label contained in the query
4. **Memory release**: After all queries for $F_i$ are exhausted, $m_i$ is removed from memory before $m_{i+1}$ arrives

This ensures the root $r$ stores **at most one message** at any given time.

## Key Equations

Let:
- $T_p$ = time to publish (convergecast) one message
- $T_q$ = time for a single query-response cycle
- $k_i$ = number of base fragments in $F_i$

For fragment $F_i$, the total processing time is:

$$\text{Time}_i = T_p + k_i \cdot T_q$$

The memory requirement at root $r$ is bounded by:

$$M(r) = O(1) \text{ messages} = O(\log^2 n) \text{ bits}$$

compared to naive pipelined approaches requiring:

$$M_{\text{naive}}(r) = O(t) \text{ messages where } t = \text{number of fragments}$$

## Physical Intuition / Derivation

### The Problem with Naive Pipelining

Traditional distributed algorithms perform message routing in two sequential phases:
1. **Convergecast phase**: All messages stream upward to root $r$, which buffers them
2. **Broadcast phase**: Root then distributes messages downward

This requires root $r$ to maintain a buffer of size $O(t)$ for $t$ fragment messages—problematic in memory-constrained networks (e.g., sensor networks with polylogarithmic memory budgets).

### The Insight: Interleaving with Knowledge

The key observation is that **base fragments already know which message they need** through their routing labels. Rather than having the root choose what to send, we let base fragments query:

1. When root $r$ receives $m_1$, base fragments of $F_1$ simultaneously send **queries containing their routing labels**
2. Root $r$ uses these labels to immediately route $m_1$ to the correct fragment
3. No buffering occurs because fragments pull messages just-in-time

### Scheduling Invariant

The publish-query schedule maintains the invariant:

$$\text{message arrival time of } m_{i+1} > \text{departure time of last copy of } m_i$$

This ensures no overlap and thus no buffering.

## Applications in Engineering

### 1. Distributed Systems & Consensus

**Minimum Spanning Tree (MST) Construction**: In the CONGEST model for distributed graph algorithms, publish-query sets enable efficient broadcast of fragment connectivity information during MST construction (e.g., Borůvka's algorithm variants) without requiring superlinear memory at aggregation points.

### 2. Wireless Sensor Networks

In memory-constrained WSNs (e.g., IoT devices with $O(\log^2 n)$ RAM), publish-query scheduling allows data aggregation trees to route results from leaf nodes to the sink without intermediate buffering, enabling real-time in-network data fusion.

### 3. Network Routing Protocols

**Hierarchical routing** in large-scale networks (e.g., OSPF areas) can use publish-query mechanisms to distribute routing updates from area border routers to internal routers without queuing updates at aggregation points.

### 4. Database Query Processing

In distributed databases, a pull-based (query) rather than push-based (broadcast) execution model with interleaved publish phases reduces memory footprint at intermediate aggregation nodes during complex multi-join operations.

### 5. Parallel Computing

In tree-reduction patterns on distributed memory systems, publish-query sets can reduce memory overhead at reduction tree nodes by allowing child processes to query results just-in-time rather than forcing buffering at parents.

## Common Mistakes / Pitfalls

### 1. **Confusing with Simple Request-Response**
Students often think publish-query sets are just request-response RPCs. The key difference is the *scheduled interleaving*: the schedule is **predetermined** during preprocessing, not reactive. This determinism is essential for guaranteeing memory bounds.

### 2. **Assuming Broadcasts Are Multicast**
A "broadcast" in publish-query sets sends a message to *one* querying base fragment at a time, not to all simultaneously. It's a **unicast disguised in a broadcast phase**. The routing label in the query directs it appropriately.

### 3. **Ignoring Preprocessing Costs**
Building the routing labels and schedule (via tree routing tables during preprocessing) has non-zero cost. Students may overlook that publish-query sets shift burden from runtime memory to *preprocessing time*.

### 4. **Over-generalizing Memory Savings**
The $O(1)$ memory bound only holds if the schedule is *carefully designed*. Any deviation (e.g., allowing $m_1$ and $m_2$ to coexist) breaks the guarantee. This is problem-specific, not universal.

### 5. **Forgetting Synchronization Requirements**
Publish-query sets require **tight global synchronization** (communication cycles with slot-based timing). In asynchronous settings, the scheduling invariant cannot be maintained.

## See Also

- [[Communication cycle protocol]] — The underlying mechanism that enforces tight scheduling for publish-query sets
- [[Tree routing tables]] — Preprocessed data structures that enable directed queries without centralized knowledge
- [[Convergecast]] — The "publish"