# Round-Delayed Amnesiac Flooding (RDAF)

## Definition

**Round-Delayed Amnesiac Flooding (RDAF)** is a distributed flooding protocol variant that disseminates information across a network while operating under two key constraints:

1. **Amnesiac operation**: Nodes maintain *no message history* and make forwarding decisions based solely on current local state, eliminating the memory overhead of traditional flooding algorithms.

2. **Round-based asynchrony with adversarial delays**: Message propagation occurs in discrete rounds, but an adversary controls communication delays—messages may arrive in any round (or not at all), modeling realistic network conditions without assuming perfect synchrony.

The protocol must guarantee information eventually reaches all reachable nodes despite these constraints and adversarial message scheduling.

### Formal Model

RDAF operates on a directed graph $G = (V, E)$ with $|V| = n$ nodes. At each round $t$:
- A source node $s$ initiates a message
- Each node $v$ maintains only current local state (no history)
- For each outgoing edge $(v, u) \in E$, the adversary decides whether the message arrives in round $t$ or is delayed to future rounds
- A node forwards a received message only if its local decision rule determines it has not seen this information "recently enough"

## Key Equations

### Termination Condition

A flooding protocol **terminates** if, for any source $s \in V$ and target $u \in V$ reachable from $s$:

$$\exists t_{\text{term}} : \text{all nodes reachable from } s \text{ have received the message by round } t_{\text{term}}$$

regardless of adversarial delay choices (within the model's constraints).

### Undecidability Bound

For arbitrary computable adversaries $\mathcal{A}$, the termination problem is undecidable:

$$\text{TERMINATE}_{\text{RDAF}}^{\mathcal{A}} \notin \text{Decidable}$$

This follows from reduction to the halting problem: the adversary can encode arbitrary computations into delay schedules.

### Eventually Periodic Adversaries (EPA)

Under the EPA model, adversary behavior is characterized by a periodic structure:

$$\exists P \in \mathbb{N}, t_0 \in \mathbb{N} : \forall t \geq t_0, \text{ delay pattern at round } t = \text{ delay pattern at round } (t + P)$$

Under EPA, termination becomes **decidable** via finite-state reachability analysis.

## Physical Intuition / Derivation

### Why Amnesiac Flooding Matters

Traditional flooding (e.g., controlled flooding with TTL) requires nodes to remember which messages they've already seen. In large-scale sensor networks or IoT systems with thousands of nodes and limited RAM per device, this state explosion is impractical. Amnesiac flooding trades perfect efficiency for constant memory per node.

### The Asynchrony Gap

Previous amnesiac flooding analyses assumed synchronous rounds: all messages sent in round $t$ arrive by round $t+1$. But real networks exhibit:
- Variable latency (WiFi vs. wired connections)
- Route changes (mobile networks)
- Congestion (queued packets)

RDAF models this via **adversarial delays**: the adversary chooses delay schedules, representing the worst-case behavior an algorithm must survive.

### Key Insight: Graph Structure Determines Termination

The paper's central result separates two cases:

**Acyclic graphs (DAGs):** Flooding always terminates
- Intuition: Information flows "downhill" toward sinks
- Any cycle would require re-forwarding old messages, which amnesiac protocols struggle with
- Proof technique: Potential function argument on topological ordering

**Cyclic graphs:** Non-termination is *possible* for adversarial delays
- Example: In a cycle $v_1 \to v_2 \to v_3 \to v_1$, an adversary can delay messages to create perpetual re-forwarding loops
- The amnesiac node cannot distinguish between "message I just saw" and "message from five rounds ago"

### Why EPA Makes Termination Decidable

With arbitrary computable adversaries, the adversary can simulate halting problem instances—deciding termination requires solving undecidable problems. However, **Eventually Periodic Adversaries** have finite "behavior entropy": after some prefix, the adversary repeats a fixed cycle of delay patterns. This finiteness allows:
- Unfolding the protocol into a finite-state graph
- Using reachability algorithms to verify if all reachable nodes are eventually reached
- Leveraging classic decidability results from automata theory

## Applications in Engineering

### 1. Wireless Sensor Networks (WSN)
- **Problem**: Nodes have 32 KB RAM; traditional flood tables consume entire memory
- **Solution**: Deploy RDAF with EPA adversary model (realistic given periodic sensor sampling)
- **Benefit**: Memory-efficient broadcast of critical sensor fusion data (e.g., wildfire alerts)

### 2. IoT Emergency Alert Systems
- Deploy RDAF on DAG-structured networks (e.g., mesh with designated gateways)
- Guarantees termination despite WiFi/cellular variability
- Example: Building evacuation signal propagation with no per-device state overhead

### 3. Mobile Ad Hoc Networks (MANETs)
- Network topology is cyclic and time-varying
- RDAF analysis reveals: protocol designers must architect for eventual periodicity (e.g., periodic beacons force EPA behavior)
- Prevents infinite re-forwarding loops from propagation delays

### 4. Delay-Tolerant Networks (DTNs)
- Spacecraft networks, underwater sensor arrays with high latency and long delays
- RDAF decidability under EPA informs whether a routing protocol can be verified before deployment
- Guides choice between bounded delays (decidable) vs. unbounded delays (undecidable)

### 5. Blockchain/Distributed Ledger Consensus
- Flood-based transaction propagation in peer-to-peer networks
- RDAF asynchrony model mirrors Nakamoto-style networks with arbitrary message delays
- Analysis informs parameters for transaction finality guarantees

## Common Mistakes / Pitfalls

### 1. **Confusing "Amnesiac" with "Stateless"**