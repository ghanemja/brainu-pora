# Structured Amnesia

## Definition

**Structured amnesia** is a protocol design principle where distributed nodes deliberately discard historical information about past transmissions while maintaining minimal state that is **functionally recomputed** from current network observations rather than accumulated over time.

In the context of the Round-Delayed Amnesiac Flooding (RDAF) protocol, structured amnesia means:

- Nodes **do not maintain records** of which neighbors previously sent or received messages in past rounds
- When receiving a message from new sources, nodes **completely recompute** their forwarding strategy based only on current receptions
- The destination set (forwarding list) is **stateless in the historical sense**—it is regenerated each round rather than evolved incrementally
- Once all delayed transmissions complete and no messages are pending, nodes return to their initial blank state

The term "amnesiac" is somewhat paradoxical: nodes *appear* forgetful, yet they maintain just enough state (destination sets, message possession flags) to ensure protocol correctness. The amnesia is **structured**—not total—because the recomputation rule is deterministic and based on measurable current conditions.

---

## Key Equations

**Message Possession Update:**
$$M(j+1, u) = \begin{cases}
1 & \text{if } u \text{ has pending delayed transmissions from round } j \\
1 & \text{if } u \text{ receives message in round } j+1 \\
0 & \text{otherwise}
\end{cases}$$

**Source Set (nodes that successfully delivered to } u \text{ in round } j+1 \text{):**
$$s(j+1, u) = \{v \in V : \{v,u\} \in E, \, u \in \text{dest}(j,v), \, d(j+1, v, \{v,u\}) = 0\}$$

**Destination Set (the core structured-amnesia rule):**
$$\text{dest}(j+1, u) = \begin{cases}
\{v \in \text{dest}(j, u) : d(j+1, u, \{u,v\}) = 1\} & \text{if continuing delayed transmission} \\
N(u) \setminus s(j+1, u) & \text{if newly receiving message} \\
\emptyset & \text{if no message possessed}
\end{cases}$$

where:
- $d(j, v, e)$ = adversarial delay on edge $e$ incident to node $v$ in round $j$ (1 = blocked, 0 = available)
- $N(u)$ = neighbors of $u$
- $\text{dest}(j, u)$ = set of neighbors $u$ intends to forward to in round $j$

**Persistence of Destination Sets (PDS) Property:**

If node $u$ receives a message in round $j$ from source $w \neq v$ and does **not** receive from $v$ in the same round, then $v \in \text{dest}(u)$ remains until either:
1. $u$ successfully delivers to $v$, or
2. $u$ receives the message from $v$

---

## Physical Intuition / Derivation

### Why Amnesia Helps

In traditional flooding protocols, nodes track the complete history of receptions:
- "I received from nodes {A, B, C} in round 5"
- "I received from nodes {A, D} in round 6"
- Logic becomes complex: *How should I handle incremental updates?*

**Structured amnesia inverts this**: instead of *tracking who sent before*, nodes use **current observations** to recompute *who should receive next*.

### The Recomputation Insight

When $u$ receives the message in round $j$ from a new neighbor $w$:

$$\text{dest}(j+1, u) = N(u) \setminus \{w, \text{other sources in round } j\}$$

This rule is elegant because:

1. **Sufficiency**: To propagate the message, $u$ only needs to forward to neighbors it hasn't received from yet (they may not have the message).
2. **Statelessness in history**: $u$ doesn't ask "did I send to $v$ in round 3?" Instead: "is $v$ in my current source set?"
3. **Automatic cleanup**: If no transmissions occur for a few rounds, $\text{dest}(j, u) \rightarrow \emptyset$ and state resets.

### Termination Guarantee

The amnesia principle ensures termination because:

- Each node's state is fully determined by: (i) message possession, (ii) current round delays, and (iii) current sources
- The state space is finite: each node either has or lacks the message; destination sets are subsets of neighbors
- No infinite loops storing outdated routing decisions—each recomputation "forgets" old preferences and re-derives them

### Trade-off: Correctness vs. Memory

This design trades **per-node memory** (very low) for **round complexity**:
- Memory: $O(|N(u)|)$ per node (only current neighbor sets and message flags)
- Round complexity: May take longer to disseminate if delays prevent direct recomputation (mitigated by the Persistence property)

---

## Applications in Engineering

### 1. **Wireless Ad Hoc Networks**
In mobile mesh networks, neighbor sets change frequently. Storing detailed transmission histories becomes obsolete as topology shifts. RDAF's amnesia naturally adapts: upon receiving from a new neighbor configuration, nodes recompute flooding paths without maintaining stale link-state tables.

### 2. **IoT Epidemic Protocols**
Resource-constrained sensors cannot afford large routing tables or message logs. Structured amnesia reduces flash memory and CPU usage. Devices flood greedily based only on *whom they just heard from*, not historical gossip records.

### 3. **Delay-Tolerant Networks (DTNs)**
In networks with unpredictable delays (satellite links, underground sensors), adversarial delay model mirrors real conditions. Structured amnesia handles intermittent connectivity: when a delayed transmission finally succeeds, the node simply recomputes its forwarding list—no need to reconcile old plans.

### 4. **Byzantine Resilience & Secure Flooding**