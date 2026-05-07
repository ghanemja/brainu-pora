# mean-payoff games

## Definition

A **mean-payoff game** is a two-player infinite-duration game played on a directed graph with integer-weighted edges. Two players—Min and Max—alternately move a token along edges, starting from an initial vertex. The game never terminates, and the **value** of a play (infinite sequence of moves) is defined as the long-run average weight of traversed edges.

Formally, given:
- A directed graph $G = (V, E)$ with $V = V_{\text{Max}} \cup V_{\text{Min}}$ (vertices controlled by each player)
- Edge weights $w: E \to \mathbb{Z}$
- An infinite play $\pi = e_0, e_1, e_2, \ldots$ where $e_i \in E$

The **mean payoff** is:
$$\text{val}(\pi) = \limsup_{n \to \infty} \frac{1}{n} \sum_{i=0}^{n-1} w(e_i)$$

The **value** $\text{val}(v)$ at vertex $v$ is the outcome under optimal play from $v$.

### Key Properties (Positional Determinacy)

A fundamental result by Ehrenfeucht and Mycielski (1976) establishes:
- Mean-payoff games are **determined**: every vertex has a well-defined value
- **Positional strategies** are optimal: players need no memory and can use memoryless strategies that depend only on the current vertex
- The game belongs to **NP ∩ coNP**

## Key Equations

**Value Definition via Minimax:**

For a vertex $v$ controlled by Max:
$$\text{val}(v) = \max_{(v,u) \in E} \text{val}(u)$$

For a vertex $v$ controlled by Min:
$$\text{val}(v) = \min_{(v,u) \in E} \text{val}(u)$$

The value accumulates as a weighted average over the infinite path. At equilibrium, from any vertex $v$:
$$\text{val}(v) = w(e_v) + \text{val}(u_v)$$
where $(v, u_v)$ is the chosen edge under optimal play, and $w(e_v)$ is its weight.

**Decision Problem:**

Determine which vertices have positive value:
$$\{v \in V : \text{val}(v) > 0\}$$

## Physical Intuition / Derivation

### Why Long-Run Average?

Consider a token moving through a weighted graph. If we sum all edge weights indefinitely, the total diverges. Instead, we care about the **average rate** at which weight accumulates. This reflects steady-state behavior:

$$\text{Long-run average} = \lim_{n \to \infty} \frac{\text{total weight in } n \text{ steps}}{n}$$

### Why Positional Strategies Suffice

Intuitively, in an infinite game with averaging payoff, history beyond "which vertex am I at now" becomes negligible. The optimal strategy depends only on current position because:
1. Any finite history contributes zero to the long-run average
2. The game is **memoryless** in steady state
3. Max wants to maximize the limiting average; Min wants to minimize it

### Algorithm Intuition (Recursive Symmetry)

The Ohlmann algorithm exploits symmetry: instead of treating Max and Min differently, both players face the same recursive decision structure. The algorithm works by:
1. Partitioning vertices based on whether they are "winning" (positive value) for Max
2. **Recursively** analyzing subgames with weights shifted to expose different behavior
3. Maintaining symmetry between players throughout

This contrasts with prior algorithms (GKK, value iteration) that compute explicit energy values or use directed strategies.

## Applications in Engineering

### 1. **Formal Verification & Model Checking**

Mean-payoff games model systems with **resource consumption** (e.g., energy, latency):
- Verify properties: "Can the system maintain average energy usage below a threshold?"
- **Reactive synthesis**: Compute winning strategies for controllers in adversarial environments
- Applicable to cyber-physical systems where both desired and malicious behaviors compete

### 2. **Scheduling & Resource Allocation**

In multi-agent systems (e.g., manufacturing, cloud clusters):
- Min (adversarial scheduler) vs. Max (system wanting good throughput)
- Value represents sustainable throughput or resource cost
- Determines if a system can achieve a target average performance metric

### 3. **Network Flow & Congestion Games**

- Model repeated interactions where cumulative cost matters (not just individual rounds)
- Average delay/congestion drives decisions
- Applicable to dynamic routing in packet networks

### 4. **Temporal Logic Synthesis**

- **LTL specifications** with average-case semantics
- Properties like: "Maximize uptime while minimizing average power consumption"
- Mean-payoff games reduce the synthesis problem to game solving

### 5. **Stochastic Control & Markov Games**

- Deterministic mean-payoff games approximate optimal control in Markov decision processes
- Solution algorithms inform approximate algorithms for stochastic games
- Relevant in autonomous systems balancing competing objectives

## Common Mistakes / Pitfalls

### 1. **Confusing Limiting Average with Sum**

**Mistake:** Treating $\sum_{i=0}^{\infty} w(e_i)$ as the payoff (diverges).  
**Correct:** Use $\limsup_{n \to \infty} \frac{1}{n}\sum_{i=0}^{n-1} w(e_i)$.

### 2. **Assuming Memory is Required**

**Mistake:** "To play optimally, the player needs to remember the history."  
**Correct:** Positional strategies (memoryless, depending only on current vertex) are optimal.

### 3. **Misunderstanding NP ∩ coNP Membership**

**Mistake:** Believing NP ∩ coNP means the problem is in P.  
**Correct:** NP ∩ coNP is a larger class; membership here just rules out NP-completeness (unless