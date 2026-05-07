# Message Flooding

## Definition

**Message flooding** is a distributed communication protocol in which nodes in a network disseminate information by forwarding messages to all neighbors, except those from whom the message was recently received. In the **Round-Delayed Amnesiac Flooding (RDAF)** protocol, this is formalized as a synchronous multi-round process where:

- Nodes maintain limited state: message possession $M(j,v)$, source sets $s(j,v)$ (neighbors that delivered the message), and destination sets $\text{dest}(j,v)$ (neighbors to forward to)
- The protocol exhibits **structured amnesia**: destination sets are recomputed based on current information rather than historical transmission logs
- An adversary model captures time-varying link failures through edge delay functions $d(j,v,e)$, where $d(j,v,e)=1$ indicates edge $e$ incident to node $v$ is blocked in round $j$

The protocol guarantees that delays are finite: for all nodes $v$ and incident edges $e$, if $d(j,v,e)=1$ for $j \in [t_1, t_2]$, then $t_2 - t_1 < \infty$.

## Key Equations

**Message Possession Update:**
$$M(j+1, u) = \begin{cases}
1, & \text{if } u \text{ has pending delayed transmissions from round } j \\
1, & \text{if } u \text{ receives message in round } j+1 \\
0, & \text{otherwise}
\end{cases}$$

**Source Set Update:**
$$s(j+1, u) = \{v \in V : \{v,u\} \in E, \, u \in \text{dest}(j,v), \, d(j+1, v, \{v,u\}) = 0\}$$

This captures which neighbors successfully delivered the message to $u$ in the current round.

**Destination Set Update (Structured Amnesia):**
$$\text{dest}(j+1, u) = \begin{cases}
\{v \in \text{dest}(j,u) : d(j+1, u, \{u,v\}) = 1\}, & \text{if continuing delayed transmission} \\
N(u) \setminus s(j+1, u), & \text{if newly receiving message} \\
\emptyset, & \text{if no message possessed}
\end{cases}$$

where $N(u)$ is the set of neighbors of $u$.

**Edge Delay Model:**
$$d(j, v, e) \in \{0, 1\} \quad \forall j \in \mathbb{N}, v \in V, e \in E$$

with the requirement:
$$\forall v \in V, \, e \text{ incident to } v: \quad |I_e(T)| < \infty$$

where $I_e(T) = \{j \leq T : d(j,v,e) = 1\}$ is the set of blocked rounds.

## Physical Intuition / Derivation

### Why Structured Amnesia?

Traditional flooding maintains explicit history: "I received from nodes $X$, so don't forward back to them." This requires unbounded memory in dynamic networks where link failures occur.

**Structured amnesia inverts this logic:** When a node receives the message, it immediately recomputes its forwarding set as **all neighbors minus current sources**. This works because:

1. **Persistence of Destination Sets (PDS):** If node $u$ receives from source $w \neq v$ in round $j$ but not from $v$, then $v$ remains a destination until either:
   - $u$ successfully transmits to $v$, or  
   - $v$ delivers to $u$ (at which point $v$ is removed as a source)

2. **Delayed transmissions are tracked explicitly** via the destination set, not through message history. If $d(j+1, u, \{u,v\}) = 1$ (link blocked), the edge $(u,v)$ remains in the destination set to retry.

3. **State reset on fresh delivery:** When a link that was blocked becomes available, or new sources appear, the destination set is recomputed—effectively forgetting previous forwarding intent and adapting to the new topology.

### Protocol Operation Flow

Each round $j$ proceeds in four phases:

1. **Delay Phase:** Adversary sets $d(j,v,e)$ for all nodes and incident edges
2. **Transmission Phase:** Nodes with $M(j-1,v)=1$ transmit to all $u \in \text{dest}(j-1,v)$ where $d(j,v,\{v,u\})=0$
3. **Reception Phase:** Successful transmissions are received
4. **State Update Phase:** Each node updates $M$, $s$, and $\text{dest}$ according to the rules above

The key insight: **nodes need not remember who they sent to last round**—they only need to know who just delivered, and forward to everyone else.

## Applications in Engineering

### 1. **Ad Hoc & Mobile Networks**
Message flooding is fundamental in protocols like AODV (Ad Hoc On-Demand Distance Vector) for route discovery. The RDAF model captures realistic scenarios where:
- Carrier sensing detects link failures
- Nodes cannot maintain routing tables in high-mobility scenarios
- Memory is constrained

### 2. **Sensor Networks**
In wireless sensor networks (e.g., TinyOS, Zigbee), flooding is used for:
- Data dissemination across large deployments
- Network bootstrapping and neighbor discovery
- The "amnesia" property suits low-power devices with limited persistent storage

### 3. **Blockchain & Distributed Ledgers**
Message propagation in peer-to-peer networks relies on variants of flooding:
- Block and transaction broadcast in Bitcoin, Ethereum
- Structured amnesia parallels local state management: peers forward to neighbors they haven't heard from yet
- Delay model captures network propagation delays and temporary disconnections

### 4. **Epidemic/Gossip Protocols**
Flooding generalizes to probabilistic gossip:
- Each node forwards to subset of neighbors