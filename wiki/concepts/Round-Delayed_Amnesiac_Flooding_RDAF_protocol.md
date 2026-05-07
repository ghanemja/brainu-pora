# Round-Delayed Amnesiac Flooding (RDAF) Protocol

## Definition

The **Round-Delayed Amnesiac Flooding (RDAF) protocol** is a distributed message dissemination algorithm designed for networks subject to adversarial edge blocking and transmission delays. The protocol enables nodes to reliably forward a message throughout a network despite an adversary that can dynamically block edges and introduce bounded delays on transmissions.

**Core Characteristics:**
- **Synchronous operation**: Time proceeds in discrete rounds
- **Adversarial edge blocking**: An adversary can block any edge in any round, with the constraint that blocking cannot persist indefinitely on any edge
- **Structured amnesia**: Nodes do not retain historical information about past senders/receivers; forwarding decisions depend only on current round state
- **Local awareness**: Each node knows which of its incident edges are currently blocked (e.g., via carrier sensing or ACK/NACK feedback)

## Key Equations

**Message Possession Update:**
$$M(j+1, u) = \begin{cases} 
1, & \text{if } u \text{ has pending delayed transmissions from round } j \\
1, & \text{if } u \text{ receives message in round } j+1 \\
0, & \text{otherwise}
\end{cases}$$

**Source Set (nodes that delivered to $u$ in round $j+1$):**
$$s(j+1, u) = \{v \in V : \{v,u\} \in E, \, u \in \text{dest}(j, v), \, d(j+1, v, \{v,u\}) = 0\}$$

where $d(j, v, e) \in \{0,1\}$ indicates whether edge $e$ incident to node $v$ is blocked in round $j$.

**Destination Set (structured amnesia rule):**
$$\text{dest}(j+1, u) = \begin{cases}
\{v \in \text{dest}(j, u) : d(j+1, u, \{u,v\}) = 1\}, & \text{if } M(j, u) = 1 \text{ and continuing} \\
N(u) \setminus s(j+1, u), & \text{if } M(j, u) = 0 \text{ and newly received} \\
\emptyset, & \text{if } M(j+1, u) = 0
\end{cases}$$

**Edge Blocking Finiteness Assumption:**
$$\forall v \in V, \forall e \text{ incident to } v: \exists t_1, t_2 \in \mathbb{N}, \, t_2 > t_1 \text{ such that } \forall j \in [t_1, t_2], \, d(j, v, e) = 1 \implies (t_2 - t_1) \text{ is finite}$$

This captures: *no edge can remain blocked indefinitely*.

## Physical Intuition / Derivation

### The Problem Setting

Consider a network where:
1. An adversary controls which edges fail in each round
2. A node must propagate a message despite these failures
3. Nodes have limited memory and cannot maintain complete histories

**Why amnesia helps:** If nodes remembered all past senders, their destination sets would grow monotonically and never stabilize. By "forgetting" and recomputing based on current information, nodes can adapt to changing network conditions.

### Protocol Flow (Per Round)

```
Round j:
  1. [Delay Phase]  Adversary commits to edge failures d(j, ·, ·)
  2. [Transmit]     Nodes with M(j-1, u) = 1 send to dest(j-1, u) 
                    on unblocked edges
  3. [Receive]      Successful transmissions deliver messages
  4. [Update]       Nodes recompute M, s(·), dest(·) for round j+1
```

### Why This Design Works

**Persistence of Destination Sets (PDS) – Observation 1:**
If node $u$ receives from source $w \neq v$ in round $j$ but does NOT receive from $v$ in that round, then $v$ remains in $\text{dest}(j+1, u)$ until either:
- $u$ successfully transmits to $v$, or  
- $v$ delivers to $u$ (retroactively making $v$ a source)

This persistence ensures retransmission to "new" neighbors, preventing message loss when the adversary temporarily blocks edges.

**Termination guarantee:** Since no edge remains blocked forever, every neighbor eventually receives the message. Once all neighbors in $\text{dest}(u)$ are either sources or successfully reached, $\text{dest}(u)$ shrinks to $\emptyset$ and the node halts.

## Applications in Engineering

### 1. **Wireless Ad-Hoc Networks**
RDAF is applicable where:
- Collision or fading causes transient link failures (detectable via carrier sensing)
- Nodes run on batteries and cannot store message histories
- The network must eventually propagate a broadcast/control message

**Example:** Emergency broadcast in a mobile ad-hoc network where acknowledgments confirm delivery.

### 2. **Industrial Control Networks**
- Distributed PLCs (programmable logic controllers) must reliably share state updates
- Transmission errors are known to occur but expected to be transient
- Memory-constrained embedded controllers benefit from stateless designs

### 3. **Distributed Database Replication**
- Propagating schema changes or critical updates across replicas
- Transient network partitions must not cause permanent inconsistency
- Nodes forget metadata about previous replication attempts and recompute strategy per round

### 4. **Internet of Things (IoT)**
- Sensor networks with highly constrained devices
- Message flooding in mesh networks where nodes forget their routing history
- Trade memory efficiency for round complexity

### 5. **Resilient Communication Protocols**
- Foundation for designing higher-level gossip/epidemic protocols
- Provides formal guarantees even under adversarial (worst-case) edge scheduling

## Common Mistakes / Pitfalls

### Mistake 1: Confusing "Amnesia" with Complete Statelessness