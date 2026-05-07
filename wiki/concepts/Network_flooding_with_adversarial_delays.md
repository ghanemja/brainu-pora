# Network Flooding with Adversarial Delays

## Definition

**Network flooding with adversarial delays** is a distributed information dissemination problem where a message must propagate through a network despite an adversary that can selectively block edges (communication links) on a per-round basis. The adversary has **temporal control**: it can introduce arbitrary delays to individual node-edge pairs, but cannot block an edge indefinitely.

The **Round-Delayed Amnesiac Flooding (RDAF) protocol** is a distributed algorithm that solves this problem by having nodes forward messages based only on current reception patterns, without maintaining historical information about prior transmissions.

### Formal Model

- **Network graph**: $G = (V, E)$ with nodes and undirected edges
- **Adversarial delay function**: $d(j, v, e) \in \{0, 1\}$ for round $j$, node $v$, incident edge $e$
  - $d(j, v, e) = 0$: edge available for transmission in round $j$
  - $d(j, v, e) = 1$: edge blocked in round $j$
- **Finite blocking guarantee** (Key Model Assumption): For all $v \in V$, incident edges $e$, if $d(j, v, e) = 1$ for $j \in [t_1, t_2]$, then $t_2 - t_1$ is finite
  - *Interpretation*: No edge is blocked forever; the adversary cannot permanently sever connectivity

---

## Key Equations

### Node State Variables

Each node $v$ maintains:

$$M(j, v) \in \{0, 1\} \quad \text{(message possession in round } j \text{)}$$

$$s(j, v) \subseteq V \quad \text{(source set: neighbors that delivered message to } v \text{ in round } j \text{)}$$

$$\text{dest}(j, v) \subseteq V \quad \text{(destination set: neighbors to forward to)}$$

### Message Possession Update Rule

$$M(j+1, u) = \begin{cases}
1, & \text{if } u \text{ has pending delayed transmissions from round } j \\
1, & \text{if } u \text{ receives message in round } j+1 \\
0, & \text{otherwise}
\end{cases}$$

### Source Set Update Rule

$$s(j+1, u) = \{v \in V : \{v, u\} \in E, \, u \in \text{dest}(j, v), \, d(j+1, v, \{v,u\}) = 0\}$$

This captures: neighbors from whom $u$ successfully received in round $j+1$.

### Destination Set Update Rule (Structured Amnesia)

$$\text{dest}(j+1, u) = \begin{cases}
\{v \in \text{dest}(j, u) : d(j+1, u, \{u,v\}) = 1\}, & \text{if continuing delayed transmission} \\
N(u) \setminus s(j+1, u), & \text{if newly receiving message \\
\emptyset, & \text{if no message possessed}
\end{cases}$$

where $N(u)$ denotes the neighborhood of $u$.

### Protocol Round Structure

Each round $j$ proceeds in four phases:

1. **Delay Phase**: Adversary specifies $d(j, v, e)$ for all $(v, e)$ pairs
2. **Transmission Phase**: Node $v$ with $M(j-1, v) = 1$ transmits to all $u \in \text{dest}(j-1, v)$ where $d(j, v, \{v,u\}) = 0$
3. **Reception Phase**: Nodes receive successfully transmitted messages
4. **State Update Phase**: All nodes update according to rules above

---

## Physical Intuition / Derivation

### Why "Amnesiac"?

The protocol is called **amnesiac** because nodes deliberately discard history:

- When node $u$ receives the message from new sources in round $j+1$, it **completely recomputes** its destination set as $N(u) \setminus s(j+1, u)$ (all neighbors except those who just sent it)
- Nodes do not remember which neighbors sent the message in previous rounds
- This *structured forgetting* prevents nodes from being "stuck" retransmitting to nodes that already have the message

**Key insight**: While nodes do maintain destination sets across rounds, this state is **not historical**—it is recomputed based on *current reception patterns*. When the destination set becomes empty and all delayed transmissions complete, the node returns to initial state.

### Why Adversarial Delays Matter

Without the finite-blocking assumption, an adversary could:
- Block edge $(u, v)$ in all rounds $j > j_0$
- Prevent the message from reaching nodes beyond $v$
- Cause flooding to fail entirely

The assumption $t_2 - t_1 < \infty$ guarantees that **every edge eventually becomes available**, ensuring eventual message propagation.

### Persistence of Destination Sets (PDS)

**Observation 1**: If node $u$ receives the message from neighbor $w \neq v$ in round $j$ but does NOT receive from $v$ in the same round, then $v \in \text{dest}(j+1, u)$ until either:
- $u$ successfully delivers to $v$, **or**
- $u$ receives the message from $v$

This property ensures that nodes with the message persist in attempting to reach neighbors that haven't acknowledged receipt, preventing message loss.

---

## Applications in Engineering

### 1. **Mobile Ad Hoc Networks (MANETs)**

Flooding is the foundational dissemination mechanism for:
- Routing protocol route discovery (AODV, DSR)
- Network management and topology updates
- Emergency broadcast during link failures
- **Challenge**: Channel fading and shadowing create intermittent link failures indistinguishable from adversarial blocking

### 2. **Satellite and Deep Space Networks**

- Links to spacecraft experience predictable blockage (antenna reorientation, eclipses)