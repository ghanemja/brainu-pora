# Maximal Matching

## Definition

A **maximal matching** in a graph $G = (V, E)$ is a subset of edges $M \subseteq E$ such that:

1. **No two edges in $M$ share a common vertex** (matching property): for all $e_1, e_2 \in M$ with $e_1 \neq e_2$, $e_1 \cap e_2 = \emptyset$
2. **No additional edge can be added without violating property 1** (maximality): there is no edge $e \in E \setminus M$ such that $M \cup \{e\}$ is also a matching

A **maximum matching** is a maximal matching with the largest possible cardinality; note that maximal matchings are not necessarily maximum.

In the context of distributed graph algorithms (particularly MSF/MST computations), maximal matching serves as a mechanism to partition fragments or components in a controlled manner, enabling hierarchical tree structures and efficient communication phases.

## Key Equations

**Size bounds on maximal matching $M$:**

For any maximal matching $M$ in graph $G = (V, E)$:

$$|M| \geq \frac{|M^*|}{2}$$

where $|M^*|$ is the size of a maximum matching. This establishes that any maximal matching contains at least half the edges of an optimal matching.

**Communication cost in matching phase:**

$$\text{Cost} = O(m) \text{ messages and } O(\log n) \text{ memory per round}$$

where $m$ is the number of edges in the graph.

## Physical Intuition / Derivation

### Why Maximal Matching?

In distributed MSF algorithms (e.g., GKP—Gallager, Humblet, Spira algorithm variants), the challenge is partitioning fragments efficiently without losing connectivity properties.

**Intuitive process:**

1. **Fragment identification**: At the start of each phase, fragments identify their Minimum Weight Outgoing Edges (MWOE-candidates)
2. **Local matching**: Instead of naively merging all fragments with their MWOE, we use maximal matching to select a subset of these edges
3. **Controlled merging**: Maximal matching ensures:
   - Each fragment is incident to at most one selected edge
   - The matching cannot be extended (no fragment left unmatched if possible)
   - This prevents starvation and maintains progress guarantees

### Why Not Maximum Matching?

- Computing maximum matching has higher distributed complexity ($O(\log^2 n)$ rounds in general)
- Maximal matching can be computed greedily in $O(\log n)$ rounds, sufficient for phase-based algorithms
- The $\frac{1}{2}$-approximation bound is acceptable for hierarchical decomposition

### Terminated Fragments

A critical detail: **terminated fragments do not participate in maximal matching**. This is because:
- Terminated fragments have no MWOE (no outgoing edges to other fragments)
- They cannot be matched to anything
- They can still forward communication traffic but don't inject phase input
- This reduces the problem size in subsequent phases

## Applications in Engineering

### 1. **Distributed Minimum Spanning Tree/Forest (MST/MSF)**
The primary application. In asynchronous distributed networks, maximal matching controls how many fragment merges occur per phase, guaranteeing $O(\log n)$ phases total and $O(m \log n)$ total messages.

### 2. **Network Clustering & Hierarchical Decomposition**
Maximal matching creates a natural hierarchy:
- Level 0: Individual vertices
- Level $k$: Fragments formed by matching at level $k-1$
- Used in locality-sensitive clustering and hierarchical network design

### 3. **Parallel Graph Algorithms**
In PRAM and distributed-memory models, maximal matching is a building block for:
- Connected components
- Graph coloring
- Load balancing across processors

### 4. **Resource Allocation in Communication Networks**
- **Link scheduling**: Maximal matching identifies non-interfering links that can transmit simultaneously
- **Slot allocation**: In the source material, fragment leaders allocate communication slots based on matching structure ($k$ subsets → $k$ slots)

### 5. **Load-Balanced Tree Merging**
When fragments merge in MSF algorithms:
$$\text{Slots per fragment leader} = |\text{base fragments in merged component}|$$
This ensures broadcast/convergecast communication cycles can serve all sub-components without congestion.

## Common Mistakes / Pitfalls

### 1. **Confusing Maximal with Maximum**
**Error**: Assuming a maximal matching is the largest possible matching.
**Reality**: A maximal matching is locally-maximal; a smaller matching might be maximum. For example, in a path of 4 vertices (1—2—3—4), matching $\{(1,2), (3,4)\}$ is maximum, but $\{(2,3)\}$ is also maximal (no edge can be added).

### 2. **Ignoring Cardinality Guarantees**
**Error**: Not leveraging the $\frac{1}{2}$-approximation bound in complexity analysis.
**Reality**: For distributed algorithm complexity, knowing $|M| \geq \frac{|M^*|}{2}$ guarantees that each phase merges enough fragments to ensure logarithmic phase count.

### 3. **Forgetting Terminated Fragments**
**Error**: Applying matching to all fragments uniformly.
**Reality**: Terminated fragments (those with no MWOE) must be excluded from matching computations to avoid wasted messages and incorrect slot allocation. They participate only in forwarding.

### 4. **Underestimating Message Complexity**
**Error**: Counting matching computation as $O(1)$ per phase.
**Reality**: Even greedy maximal matching requires:
- $O(m)$ messages to communicate MWOE candidates
- $O(\log n)$ rounds for convergecast/broadcast of matching decisions
- This dominates each phase but is necessary for correctness

### 5. **Misunderstanding Slot Allocation**
**Error**: Allocating slots based only on fragment count, not subset structure.
**Reality**: In communication cycles, the fragment leader needs slots matching the **number of base fragments** (subtrees), plus