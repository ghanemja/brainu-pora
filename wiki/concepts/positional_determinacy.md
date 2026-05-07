# Positional Determinacy

## Definition

**Positional determinacy** is a fundamental property of certain game-theoretic systems stating that optimal play by all players can be achieved using **stationary (memoryless) strategies**—that is, strategies that depend only on the current position/state and not on the history of play.

More formally: A game is **positionally determinate** if there exist optimal strategies $\sigma_i^*$ for each player $i$ such that:
$$\sigma_i^*(v) = a_v \in \text{Actions}(v) \quad \forall v \in V_i$$
where the action $a_v$ depends only on the vertex $v$, independent of the sequence of states visited before reaching $v$.

In the specific context of **mean-payoff games**, positional determinacy was proven by Ehrenfeucht and Mycielski [7]. It asserts that to play optimally in such games, neither player requires memory of past moves—each player can determine their optimal move at any vertex based solely on that vertex's identity.

## Key Equations

For a mean-payoff game on a graph with integer-weighted edges, denote:
- $V$ = set of vertices (game positions)
- $V_{\text{Max}}$, $V_{\text{Min}}$ = vertices controlled by Max and Min players
- $w(e)$ = weight on edge $e$
- $\text{Value}(v)$ = the mean-payoff value of vertex $v$ under optimal play

The **value function** satisfies:
$$\text{Value}(v) = \begin{cases}
\max_{a \in \text{Actions}(v)} \mathbb{E}_{\text{play}}[\text{mean-payoff} \mid \text{start at } a] & v \in V_{\text{Max}} \\
\min_{a \in \text{Actions}(v)} \mathbb{E}_{\text{play}}[\text{mean-payoff} \mid \text{start at } a] & v \in V_{\text{Min}}
\end{cases}$$

For a play sequence $\pi = v_0 \to v_1 \to v_2 \to \cdots$ with edge weights $w_i = w(v_i \to v_{i+1})$:
$$\text{Mean-payoff}(\pi) = \limsup_{n \to \infty} \frac{1}{n} \sum_{i=0}^{n-1} w_i$$

A stationary strategy $\sigma_{\text{Max}}$ is **optimal** if:
$$\text{Value}(v) = \mathbb{E}_{\pi \sim \sigma_{\text{Max}}, \sigma_{\text{Min}}^*}[\text{Mean-payoff}(\pi) \mid v_0 = v]$$

## Physical Intuition / Derivation

### Why Positional Strategies Suffice

Intuitively, positional determinacy emerges because **the long-run average payoff depends only on the recurrent structure** of the infinite play, not on how we arrived at the current state. Once play stabilizes into a cycle (which happens almost surely in finite games), all history is "forgotten" in terms of its contribution to the limiting average.

**Key insight**: In a finite-vertex game, any infinite play eventually revisits vertices. The mean-payoff depends only on which cycles are traversed infinitely often, not the transient path taken to reach them. Therefore:

1. Each player, upon reaching a vertex $v$, needs to know only the long-run value from $v$
2. The optimal action at $v$ is that which maximizes (for Max) or minimizes (for Min) the value from the *destination vertex*
3. This decision is independent of history—it's a local, stationary choice

### Consequence: NP ∩ coNP Membership

Positional determinacy immediately implies that:
- **"Is $\text{Value}(v) > 0$?" is in NP**: A non-deterministic algorithm guesses Max's stationary strategy and verifies the mean-payoff is positive
- **"Is $\text{Value}(v) \leq 0$?" is in NP**: A non-deterministic algorithm guesses Min's stationary strategy and verifies the mean-payoff is non-positive

Thus, the decision problem lies in $\text{NP} \cap \text{coNP}$.

## Applications in Engineering

### 1. **Verification of Reactive Systems**
Positional determinacy enables efficient model-checking of systems with adversarial environments (system vs. environment). Controllers need only "remember" their current state, not the full history, to guarantee safety/liveness properties.

### 2. **Game-Based Controller Synthesis**
In automated synthesis, positional determinacy guarantees that synthesized controllers are **implementable as finite-state machines** (with no memory beyond the current state). This is critical for embedded systems with limited resources.

### 3. **Network Protocol Design**
In distributed systems competing with adversarial agents (e.g., Byzantine fault tolerance), positional determinacy suggests that optimal routing/consensus decisions depend only on local state, enabling decentralized algorithms.

### 4. **Energy-Aware Resource Allocation**
In systems where "energy cost" is modeled as game payoff, positional strategies define stateless allocation policies that are optimal regardless of past consumption, useful for real-time resource schedulers.

### 5. **Reinforcement Learning Theory**
Positional determinacy provides theoretical justification for Markovian policies in multi-agent RL: agents can achieve optimality with memoryless strategies, reducing the hypothesis space and improving sample complexity.

## Common Mistakes / Pitfalls

### Mistake 1: Confusing Positional Determinacy with Determinism
**Error**: "Positional determinacy means the outcome is deterministic."  
**Fact**: Positional determinacy means *optimal strategies* are deterministic (memoryless), but outcomes may be stochastic if the game itself includes randomness.

### Mistake 2: Assuming It Applies to All Games
**Error**: Claiming positional determinacy holds for arbitrary games.  
**Fact**: Positional determinacy is a special property, proven for mean-payoff games but *not* for all games (e.g., it fails for some reach