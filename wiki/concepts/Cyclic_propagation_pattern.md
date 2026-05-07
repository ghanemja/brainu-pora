# Cyclic Propagation Pattern

## Definition

A **cyclic propagation pattern** is a periodic message transmission schedule on a cycle graph where messages circulate sequentially around the cycle in a predictable, repeating manner. Formally, for a cycle $C = (V_C, E_C)$ with nodes $V_C = \{v_1, v_2, \ldots, v_n\}$ arranged sequentially, the cyclic propagation pattern is satisfied when:

**Property 1 (Cyclic Propagation):** For every positive integer $i$, node $v_{i \bmod n}$ transmits to node $v_{(i+1) \bmod n}$ at round $c + i$, where $c$ is the earliest round at which any cycle node receives the message.

In essence, each node in the cycle receives the message, adds the next node to its destination set, and transmits exactly once per cycle period—creating a self-sustaining infinite message circulation pattern that never terminates.

## Key Equations

**Delay Function:**
$$d(j, u, e) = \begin{cases} 0 & \text{if } j - c \equiv i \pmod{n} \text{ and } e = \{v_i, v_{i+1 \bmod n}\} \\ 1 & \text{otherwise} \end{cases}$$

where:
- $j$ = current round
- $u$ = transmitting node
- $e$ = edge being used
- $i$ = node index relative to cycle numbering
- $n$ = cycle length

**Transmission Schedule:**
$$\text{Transmission at round } c + i: \quad v_{i \bmod n} \to v_{(i+1) \bmod n}$$

**Pattern Periodicity:** The pattern repeats with period $n$, such that node $v_k$ transmits in rounds $\{c + k, c + k + n, c + k + 2n, \ldots\}$.

## Physical Intuition / Derivation

### Why Cycles Cause Non-Termination

In acyclic graphs, messages propagate forward until reaching leaf nodes where flooding terminates. However, cycles introduce feedback: once a message reaches any node in the cycle, it can be directed to propagate around the cycle indefinitely.

### Construction of the Cyclic Pattern

The construction works by:

1. **Initialization:** When a message first reaches any node $v_1$ in cycle $C$ at round $c$, we designate this as the "start" and label remaining nodes sequentially around the cycle.

2. **Destination Set Maintenance:** Each node $v_k$ that receives a message adds its successor $v_{k+1}$ to its destination set and retains it indefinitely (until either transmitting successfully or receiving from $v_{k+1}$).

3. **Adversarial Scheduling:** The delay function $d$ is carefully designed so that:
   - At round $c + 1$: $v_1$ is allowed to transmit to $v_2$
   - At round $c + 2$: $v_2$ is allowed to transmit to $v_3$
   - At round $c + k$: $v_k$ is allowed to transmit to $v_{k+1}$

This is proven by induction (Lemma 2), showing that if the pattern holds through round $c + k$, then at round $c + (k+1)$, node $v_{k+1}$ will have the message and $v_{k+2}$ in its destination set, allowing the transmission to proceed.

### Disruption Characterization

The pattern can only be disrupted if a node transmits *backwards* along the cycle (Lemma 3): if $v_{k+1}$ transmits to $v_k$ while $v_k$ already has the message but hasn't yet completed its transmission to $v_{k+1}$. This removes $v_{k+1}$ from $v_k$'s destination set and breaks the cycle. Without such backwards transmissions, the pattern is guaranteed to persist infinitely.

## Applications in Engineering

### Distributed Algorithms & Consensus

- **Non-Termination Detection:** The cyclic propagation pattern is used to prove that flooding-based distributed algorithms (like RDAF—Round-Delayed Amnesiac Flooding) cannot terminate on graphs with cycles, even under adversarial message scheduling.
- **Liveness vs. Safety Trade-offs:** Understanding cyclic patterns helps identify when termination guarantees are achievable (acyclic networks) versus impossible (cyclic networks).

### Network Protocols & Routing

- **Loop Detection:** The pattern characterization helps identify and prevent message loops in routing protocols by detecting backwards transmissions.
- **Cycle-Breaking Algorithms:** Many spanning-tree or loop-detection protocols exploit the fact that preventing the cyclic pattern (via carefully controlled feedback) guarantees termination.

### Formal Verification

- **Adversarial Strategy Analysis:** The construction of infinite periodic schedules is used to prove non-termination in temporal logic and model-checking frameworks.
- **Reachability Analysis:** Characterizing which patterns can persist helps determine the set of reachable system states.

### Real-World Flooding Algorithms

- **Broadcast Protocols:** Understanding cyclic patterns informs the design of broadcast algorithms that must handle graphs with cycles (e.g., in mesh networks, ring topologies).
- **Gossip Protocols:** In peer-to-peer systems, cyclic propagation patterns explain why naive gossip protocols can create persistent message circulation.

## Common Mistakes / Pitfalls

1. **Confusing with Acyclic Termination:** Students often assume that because acyclic graphs guarantee termination, cycles only delay it. In fact, cycles admit *infinite non-terminating schedules*—not merely slow ones.

2. **Overlooking the Adversarial Role:** The cyclic pattern requires an adversary that *enables* transmissions at precisely the right rounds. Simply having a cycle doesn't guarantee the pattern—the scheduling must cooperate.

3. **Missing the Destination Set Semantics:** The pattern relies on nodes retaining the next-hop in their destination set across multiple rounds. Assuming immediate transmission or destination set clearing breaks the analysis.

4. **Backwards Transmission Oversight:** It's tempting to think any transmission along a cycle edge maintains the pattern. The key insight is that *backwards* transmissions (against the direction of