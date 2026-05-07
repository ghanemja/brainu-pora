# Destination set computation

## Definition

**Destination set computation** refers to the algorithmic process by which nodes in a distributed network determine which neighbors should receive forwarded messages in each round of communication. In the context of flooding protocols like Round-Delayed Amnesiac Flooding (RDAF), the destination set $\text{dest}(j, u)$ is a dynamically computed subset of a node $u$'s neighbors that represents forward propagation targets.

Formally, for node $u$ at round $j$:
$$\text{dest}(j, u) \subseteq N(u)$$

where $N(u)$ denotes the neighborhood of $u$ and depends on:
- Whether $u$ currently possesses the message
- The set of sources from which $u$ recently received the message
- The state of delayed transmissions

## Key Equations

### Core Update Rule

The destination set update follows a structured rule based on the node's message state:

$$\text{dest}(j+1, u) = \begin{cases}
\{v \in \text{dest}(j, u) : d(j+1, u, \{u,v\}) = 1\} & \text{if continuing delayed transmission} \\
N(u) \setminus s(j+1, u) & \text{if newly receiving message} \\
\emptyset & \text{if no message possessed}
\end{cases}$$

where:
- $d(j, u, e)$ is the delay function ($1$ if edge $e$ is blocked in round $j$, $0$ otherwise)
- $s(j, u)$ is the **source set**: neighbors from which $u$ successfully received the message in round $j$

### Source Set Update

$$s(j+1, u) = \{v \in V : \{v,u\} \in E, \, u \in \text{dest}(j, v), \, d(j+1, v, \{v,u\}) = 0\}$$

### Message Possession

$$M(j+1, u) = \begin{cases}
1 & \text{if } u \text{ has pending delayed transmissions} \\
1 & \text{if } u \text{ receives the message in round } j+1 \\
0 & \text{otherwise}
\end{cases}$$

## Physical Intuition / Derivation

### Why Destination Sets?

In a distributed flooding protocol, nodes must decide independently and without global knowledge which neighbors to forward to. Naive approaches (e.g., flooding to all neighbors) can cause:
- Exponential message duplication
- Inefficient use of bandwidth
- Difficulty in proving convergence

The destination set restricts forwarding to avoid re-transmitting to nodes that already have the message.

### The Structured Amnesia Principle

The protocol uses **structured amnesia**—nodes do not maintain historical records of past transmissions. Instead, destination sets are *recomputed from current information*:

1. **Upon receiving from new sources** (round $j$): A node immediately reconstructs its destination set as $N(u) \setminus s(j+1, u)$
   - This "forgets" the old destination set
   - It guarantees we never re-transmit to a node we just received from

2. **During persistent delays** (round $j+1$ following $j$): Only neighbors still experiencing transmission failures remain in the destination set
   - The node "remembers" to retry failed destinations
   - But this information is temporary and reconstructed dynamically

### Key Property: Persistence of Destination Sets (PDS)

**Observation 1**: If node $u$ receives the message from a neighbor $w \neq v$ in round $j$ but not from $v$, then $v \in \text{dest}(u)$ until either:
- $u$ successfully delivers to $v$, or  
- $u$ receives from $v$

This ensures eventual delivery despite adversarial delays.

### Derivation Intuition

The destination set rule encodes a simple principle:
$$\text{dest}(j+1, u) = \text{(neighbors to retry)} \cup \text{(all neighbors except sources)}$$

- **Retry clause**: $\{v \in \text{dest}(j,u) : d(j+1,u,\{u,v\})=1\}$ — if an edge was blocked and we couldn't send, keep it in the destination set
- **Fresh-reception clause**: When newly receiving, reset to $N(u) \setminus s(j+1,u)$ — everyone except those who just sent us the message

This design prevents redundant transmissions while guaranteeing retry in the face of transient failures.

## Applications in Engineering

### 1. **Ad Hoc and Sensor Networks**
Destination set computation enables efficient **multi-hop message dissemination** in mobile networks where:
- Link failures are frequent and transient
- Nodes have limited memory and bandwidth
- No central coordinator exists

Example: Wildfire detection networks where sensor nodes must propagate alerts with minimal redundancy.

### 2. **Network Protocol Design**
Used in **controlled flooding** and **broadcast algorithms** to balance:
- Reliability (eventual delivery despite transient failures)
- Efficiency (minimize message copies)
- Scalability (no per-message history)

Example: BATMAN (Better Approach To Mobile Ad-hoc Networking) routing protocols use similar destination recomputation principles.

### 3. **Distributed Systems Resilience**
Supports **gossip and epidemic protocols** for distributed consensus and state propagation in systems with:
- Byzantine adversaries controlling temporary link failures
- Highly dynamic topologies
- No shared memory

Example: State machine replication in cloud systems that must tolerate transient link partitions.

### 4. **IoT and Low-Power Networks**
Destination set computation is memory-efficient—nodes need not log transmission history. This is critical for:
- Devices with kilobytes of RAM
- Long-running deployments where memory fragmentation is expensive

### 5. **Network Management and Recovery**
Used in **Carrier-sense Multiple Access (CSMA)** and acknowledgment-based protocols to detect failed transmissions and adaptively recompute forwarding strategies.

## Common Mistakes / Pitfalls

### Mistake 1: Confusing Destination Sets with Actual Forw