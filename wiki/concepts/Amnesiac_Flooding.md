# Amnesiac Flooding

## Definition

**Amnesiac Flooding (AF)** is a distributed message dissemination protocol in which nodes forward received messages without maintaining any history of previously transmitted messages. Each forwarding decision is made based solely on current local information, without memory of past transmissions.

**Round-Delayed Amnesiac Flooding (RDAF)** extends AF by incorporating asynchronous communication through adversarial message delays bounded within rounds. In RDAF, nodes operate synchronously in rounds, but an adversary controls message delivery times within round boundaries, introducing realistic network conditions (packet delays, out-of-order delivery) while preserving theoretical analyzability.

### Formal Model

In RDAF, the system is characterized by:
- **Nodes** $V = \{v_1, v_2, \ldots, v_n\}$ organized as a directed graph $G = (V, E)$
- **Rounds** $t = 1, 2, 3, \ldots$ as discrete time steps
- **Adversarial Delays** $\delta(e,t) \in \{0, 1\}$ for edge $e$ and round $t$: message sent in round $t$ arrives in round $t$ or $t+1$
- **Amnesiac State** at node $v$: only current round status, no persistent message history

## Key Equations

### Termination Condition

A flooding protocol **terminates** if there exists a finite time $T$ such that:
$$\forall t > T, \forall v \in V: \text{node } v \text{ has no message to forward}$$

### Round-Delay Model

For edge $e = (u,v)$ and message sent from $u$ in round $t$:
$$\text{arrival\_round}(e, t) = t + \delta(e,t)$$

where $\delta(e,t) \in \{0, 1\}$ represents the adversary's choice.

### Acyclic Graph Termination Bound

For **DAGs** with diameter $d$ and maximum degree $\Delta$:
$$T_{\text{acyclic}} \leq d + 1$$

No adversarial delay can prevent termination on acyclic graphs.

## Physical Intuition / Derivation

### Why Memory-Less Forwarding?

Traditional flooding maintains a **message history** to prevent duplicate transmissions: "Have I seen this message before?" In resource-constrained environments (IoT sensors, mobile ad-hoc networks), storing this history is prohibitively expensive—both in memory footprint and synchronization overhead.

AF eliminates this overhead by trusting the topology: on acyclic graphs, a message can only traverse finitely many paths before exhausting all reachable nodes. Without cycles, **repetition is impossible in principle**, making history unnecessary.

### The Role of Adversarial Delays

Real networks don't have synchronized clocks. Packets arrive out of order; some paths are slower than others. RDAF captures this by:

1. **Bounding** delays within a single round (realistic: nanoseconds to milliseconds depending on scale)
2. **Adversarially controlling** delay to show worst-case behavior
3. **Proving termination despite** the adversary—if RDAF terminates under adversarial delays, it terminates under any real delay pattern

This is more realistic than perfect synchrony (every message arrives instantly) yet still provably analyzable.

### Termination on DAGs: Intuitive Proof Sketch

On a DAG with topological ordering $\sigma$:
- A message originating at $v$ can only reach nodes $u$ where $\sigma(v) < \sigma(u)$
- Even with delays, the message must follow directed paths respecting this order
- After $d+1$ rounds, all reachable nodes at distance $d$ have received the message
- **No node can receive the same message twice** (acyclicity prevents returning to the source)
- Therefore, **flooding terminates** regardless of adversarial delays

### Non-Termination on Cycles

A single cycle $v_1 \to v_2 \to \cdots \to v_k \to v_1$ allows a message to re-enter nodes indefinitely. The adversary can orchestrate delays such that:
- Message from $v_1$ reaches $v_2$ in round 1
- Delay on $v_2 \to v_3$ causes $v_3$ to receive it in round 2
- By controlling delays around the cycle, messages circulate forever
- **Non-termination is constructible** on any cyclic graph

## Applications in Engineering

### 1. **Sensor Networks & IoT**
In battery-constrained sensor networks, amnesiac flooding reduces memory overhead critical for deployment at scale. RDAF's asynchronous model matches real wireless sensor networks with variable link latencies.

**Example**: Event dissemination in smart city deployments where thousands of nodes must relay alerts without maintaining per-message state.

### 2. **Mobile Ad-Hoc Networks (MANETs)**
Nodes in MANETs have volatile connectivity and limited storage. AF suits scenarios where the network topology remains acyclic (e.g., tree-structured clusters) or where bounded forwarding is tolerable.

### 3. **Emergency Broadcast Systems**
Critical information (evacuation alerts, safety warnings) must propagate rapidly without centralized coordination. RDAF guarantees dissemination on all acyclic network topologies regardless of link delays.

### 4. **Blockchain & Peer-to-Peer Networks**
P2P protocols use flooding variants for transaction/block propagation. Understanding termination bounds under asynchronous conditions is essential for network stability and fork prevention.

### 5. **Network Diagnosis & Discovery**
RDAF can model network topology discovery protocols that operate without maintaining explicit state tables, reducing synchronization overhead in exploratory phases.

## Common Mistakes / Pitfalls

### 1. **Confusing "Amnesiac" with "Stateless"**
Amnesiac flooding **maintains local state** (current round, active flag), but not **history**. Nodes know their own identity and neighbor list; they simply don't remember past messages. Students often incorrectly assume nodes have zero state.

### 2. **Assuming Termination on All Graphs**
The most critical error: RDAF **terminates on DAGs** but **does not terminate on cyclic graphs**