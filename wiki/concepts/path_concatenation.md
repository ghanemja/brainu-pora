# Path Concatenation

## Definition

**Path concatenation** is the operation of joining multiple directed paths sequentially to form a longer path or cycle, where the endpoint of one path coincides with the starting point of the next.

In formal terms, given a sequence of directed paths $P_1, P_2, \ldots, P_l$ in a digraph $\bar{D} = (A, \bar{E})$, where:
- Each $P_i$ is an $a_i$-to-$a_{i+1}$ path (with $a_{l+1} := a_1$)
- The endpoint of $P_i$ equals the starting point of $P_{i+1}$

the **concatenation** $C = P_1 \circ P_2 \circ \cdots \circ P_l$ produces a directed cycle when $l > 1$ and the paths form a closed loop.

In the context of matching theory and resource allocation, path concatenation is used to construct cycles that may violate efficiency (Pareto-optimality) by enabling beneficial reassignments across multiple agents.

## Key Equations

Given paths $P_i: a_i \to a_{i+1}$ for $i \in [l]$ where $a_{l+1} = a_1$:

$$C = P_1 \circ P_2 \circ \cdots \circ P_l$$

The concatenated cycle $C$ satisfies:
- All nodes appear in a single connected component: $C \subseteq B \subseteq \bar{E}$
- Each path $P_i$ is contained in some exchange graph: $P_i \subseteq D_{M_i}$ for $M_i \in \mathcal{M}$

### Cycle Reduction Property

If the concatenation violates property (3) below, we replace $C$ with a shorter cycle formed by:

$$C' = P_{j+1} \circ \cdots \circ P_{i-1} \circ P' \circ \emptyset$$

where $P'$ traverses from the end of $P_{i-1}$ to node $a$, takes arc $(a,b)$, then follows $P_j$ from $b$ onward.

## Physical Intuition / Derivation

### Building Understanding

Path concatenation emerges naturally when analyzing cycles in matching markets with preferences. Consider agents $a_1, a_2, \ldots, a_l$ where:
1. Agent $a_1$ prefers $a_2$'s current assignment
2. Agent $a_2$ prefers $a_3$'s current assignment
3. ... and so on cyclically

Rather than store these preferences as a complex graph, we can **concatenate paths** representing the sequence of "improvement opportunities":
- Path $P_1$ encodes why $a_1$ wants to trade with $a_2$
- Path $P_2$ encodes why $a_2$ wants to trade with $a_3$
- Concatenating these reveals the *cycle of blocking coalitions*

### Three Key Properties

The source material emphasizes that useful concatenated cycles must satisfy:

**(1) No source agents:** No agent in the cycle is in set $A^-$ (agents with no outgoing arcs)

**(2) Path consistency:** For each $i \in [l]$:
   - $P_i$ is a unique $a_i$-to-$a_{i+1}$ path respecting cycle direction
   - $P_i \subseteq D_{M_i}$ for some matching $M_i \in \mathcal{M}$
   - $M_i \neq M_{i+1}$ (paths come from different matchings)

**(3) No redundant arcs:** Once property (3) is satisfied, we cannot shorten the cycle further by removing redundant cross-edges. This ensures **minimality**—the cycle is truly blocking.

### Iterative Refinement

The algorithm **iteratively shortens** concatenations that violate property (3) until a *minimal* cycle is obtained. This is crucial because:
- Every iteration reduces the number of arcs
- The process terminates in finite time
- The final cycle represents an irreducible blocking coalition

## Applications in Engineering

### 1. **Matching Markets & Resource Allocation**
In two-sided matching problems (e.g., job markets, hospital-resident programs), path concatenation identifies cycles of mutually beneficial trades that violate Pareto-optimality. This enables detection and elimination of blocking coalitions.

### 2. **Mechanism Design**
When designing incentive-compatible allocation mechanisms, concatenated paths reveal preference cycles that could lead to agents abandoning the mechanism. Identifying these cycles is essential for proving stability.

### 3. **Supply Chain Networks**
In multi-agent procurement networks, concatenation can model sequences of exchanges: supplier $A$ prefers supplier $B$'s vendor contract, $B$ prefers $C$'s, etc. Detecting such cycles helps prevent inefficient procurement patterns.

### 4. **Graph Algorithms & Cycle Detection**
Path concatenation is a fundamental technique in:
- Negative cycle detection in shortest-path algorithms
- Strongly connected component analysis
- Deadlock detection in distributed systems

### 5. **Network Flow & Circulation Problems**
In min-cost circulation problems, augmenting cycles are constructed by concatenating paths along residual graphs to improve solution cost.

## Common Mistakes / Pitfalls

### 1. **Confusing Path Concatenation with Arbitrary Sequencing**
❌ **Mistake:** Treating any sequence of arcs as a valid concatenation.
✓ **Correct:** Ensure endpoints match exactly: the terminal node of $P_i$ must be the initial node of $P_{i+1}$.

### 2. **Ignoring Minimality**
❌ **Mistake:** Accepting any cycle that satisfies properties (1) and (2).
✓ **Correct:** Property (3) is essential—apply reductions until no cross-edges between non-consecutive paths exist.

### 3. **Forgetting the Matching Constraint**
❌ **Mistake:** Allowing $P_i$ and $P_j$ to come from the same matching ($M_i = M_j$).
✓ **Correct:** Property (2c) requires $