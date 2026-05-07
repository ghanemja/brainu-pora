# (k, c)-flooding problem

## Definition

The **(k, c)-flooding problem** is a discrete optimization problem in distributed network algorithms that asks:

**Given a graph $G$ and parameters $k$ and $c$, determine whether there exists a set $S$ of $k$ nodes such that the Amnesiac Flooding (AF) algorithm, when initiated from nodes in $S$, is guaranteed to terminate within $c$ rounds regardless of adversarial message delays.**

More formally: Find a source set $S \subseteq V(G)$ with $|S| = k$ such that for all possible adversarial delay schedules on edge deliveries, the AF algorithm completes within round $c$.

**Key Characteristics:**
- **Optimization variant** of amnesiac flooding termination analysis
- **Decision problem**: Does such a set $S$ exist?
- **Parameters**: $k$ (number of source nodes), $c$ (round budget)
- **Adversary model**: An adversary controls message delivery delays on edges but cannot prevent delivery indefinitely

## Key Equations

The termination round bounds for AF are:

$$\text{Rounds}_{\text{bipartite}} = e(S)$$

$$\text{Rounds}_{\text{non-bipartite}} \in [e(S), e(S) + d + 1]$$

where:
- $e(S)$ = maximum eccentricity of nodes in source set $S$ (distance from $S$ to farthest node)
- $d$ = graph diameter

For the $(k,c)$-problem, we seek $S$ with $|S| = k$ minimizing $e(S)$ such that:

$$e(S) \leq c$$

The problem complexity class is:

$$\text{(k,c)-flooding} \in \mathbf{NP}\text{-complete}$$

## Physical Intuition / Derivation

### The Core Tension

Consider a distributed system where:
1. We must **place exactly $k$ sources** in a network
2. We want **all information to propagate** to all nodes
3. An **adversary delays messages** (but doesn't lose them)
4. We need termination **within $c$ rounds**

The key insight is that source placement directly controls **how far information must travel**:
- If sources are clustered (e.g., all in one corner), distant nodes take many rounds to receive information
- If sources are spread strategically, the maximum distance any node must wait is reduced

### Why It's NP-Hard

The problem is NP-complete because:

1. **Verification is polynomial**: Given a candidate set $S$, computing $e(S)$ (the farthest distance to any node) takes $O(k \cdot n)$ time via BFS from each source.

2. **No known polynomial algorithm**: Finding the *optimal* $k$-node set that minimizes eccentricity requires examining combinatorial arrangements. The brute-force approach is $\binom{n}{k}$, which is exponential.

3. **Reduction from Set Cover** shows hardness: One can encode set cover instances as (k,c)-instances, proving NP-completeness.

### Bipartite vs. Non-Bipartite Disparity

A critical finding is that graphs exhibit **fundamentally different behavior**:

| Graph Type | Termination Bound | Reason |
|---|---|---|
| Bipartite | $e(S)$ (tight) | Synchronous flooding exploits bipartite structure; parity ensures clean termination |
| Non-bipartite | $e(S) + d + 1$ | Odd cycles create "echo" effects; worst case adds diameter |

This means for the same $k$ and $c$, different graph classes may have different solvability.

## Applications in Engineering

### 1. **Network Broadcast Protocols**
When designing fault-tolerant broadcasting (e.g., in IoT networks), the (k,c)-problem answers:
- *Where should we place $k$ base stations to ensure full coverage within $c$ time steps?*
- Example: Emergency alert systems need to guarantee all devices receive updates within strict time windows

### 2. **Distributed Consensus & Synchronization**
In consensus protocols with asynchronous message delivery:
- Determine minimum number of **designated initiators** to guarantee agreement by deadline $c$
- Used in blockchain synchronization, distributed databases

### 3. **Sensor Networks**
Placing $k$ relay nodes to propagate sensor readings:
- Minimize number of relays while meeting latency $c$
- Trade cost (relay deployment) against performance (response time)

### 4. **Epidemic/Information Diffusion Models**
Epidemiological simulations on contact networks:
- Determine number of initially infected nodes to reach herd immunity information level within $c$ generations
- Public health modeling in social networks

### 5. **Power Grid Control**
In smart grids with distributed control:
- Place $k$ control nodes to disseminate frequency adjustment commands within $c$ cycles
- Critical for cascading failure prevention

## Common Mistakes / Pitfalls

### 1. **Confusing Eccentricity with Distance**
❌ **Wrong**: "Eccentricity of $S$ is the sum of distances from $S$ to all nodes"
✓ **Correct**: Eccentricity is the *maximum* distance: $e(S) = \max_{v \in V} d(S,v)$

### 2. **Assuming Greedy Placement Works**
❌ **Wrong**: Placing sources at highest-degree nodes always minimizes $e(S)$
✓ **Correct**: Optimal placement depends on distance structure, not just degree. A greedy solution is not guaranteed optimal due to NP-hardness.

### 3. **Ignoring Graph Bipartiteness**
❌ **Wrong**: Termination bounds are independent of bipartiteness
✓ **Correct**: Non-bipartite graphs add $\Theta(d)$ overhead. Must check graph structure.

### 4. **Over-interpreting Adversarial Delays**
❌ **Wrong**: The adversary can prevent message delivery
✓ **Correct**: Adversary only *delays* delivery; messages are guaranteed to arrive eventually. The algorithm ensures persistence with "keep trying" semantics.

### 5. **Conflating