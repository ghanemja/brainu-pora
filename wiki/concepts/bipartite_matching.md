# Bipartite Matching

## Definition

A **bipartite matching** is an assignment between two disjoint sets of vertices in a bipartite graph such that each vertex is incident to at most one edge in the matching. Formally, given a bipartite graph $G = (A \cup B, E)$ where $A$ and $B$ are disjoint vertex sets and $E \subseteq A \times B$, a matching $M \subseteq E$ is a set of edges where no two edges share a common endpoint.

**Key variants:**

- **Maximum matching**: a matching with the largest cardinality $|M|$
- **Popular matching**: a matching that is preferred by a weak majority of agents over any competing matching (a Condorcet winner)
- **Pareto-optimal matching**: a matching where no other matching makes every agent at least as satisfied and at least one agent strictly better off

When agents (on one side of the bipartite graph) have *preferences* over objects (on the other side), we extend the definition to preference-based matching problems. A **Condorcet-winning set** of matchings is a collection $\mathcal{M}$ such that for every competing matching outside $\mathcal{M}$, a majority of agents prefer their favorite matching in $\mathcal{M}$ over the competitor.

## Key Equations

### Cardinality Bounds

For a bipartite graph with $|A| = m$ agents and $|B| = n$ objects:

$$|M| \leq \min(m, n)$$

### Condorcet Dimension

The **Condorcet dimension** $\text{CD}(\text{instance})$ is the minimum cardinality of a Condorcet-winning set:

$$\text{CD} = \min_{\mathcal{M} \text{ is Condorcet-winning}} |\mathcal{M}|$$

**Key result from source material:**
- Under weak preference orders (total transitive preferences): $\text{CD} = 2$ (even with matroid constraints)
- Under partial orders: $\text{CD} = \Theta(\sqrt{n})$ without matroid constraints; $\text{CD} = \Theta(n)$ with matroid constraints

## Physical Intuition / Derivation

### Why Bipartite Structure Matters

The bipartite structure naturally models **two-sided allocation problems**: one side represents agents/workers/buyers, the other represents objects/tasks/resources. Edges represent feasible pairings. The restriction that each vertex appears in at most one edge enforces *capacity constraints*: each agent gets one item, each item goes to one agent.

### The Popularity vs. Optimality Tension

In practice, a single "optimal" matching rarely exists when multiple agents have conflicting preferences. Instead:

1. **Condorcet winner** (popular matching): No other matching is preferred by a strict majority—a minimal consensus criterion
2. **Challenge**: Condorcet winners may not exist even for simple preference instances
3. **Solution concept**: Relax to a small set of matchings such that within this set, agents can always find their favorite option and avoid being outvoted by others

This connects to **resource augmentation**—the Condorcet dimension quantifies how much we must expand capacity (allow matchings of slightly larger sets) to guarantee consensus-like outcomes.

### Why Pareto Optimality Helps

A Pareto-optimal *set* of matchings has strong guarantees: if you try to move to any matching outside the set, you make at least one agent worse off. This "no-one-worse-off" property is compatible with majority voting, yielding Condorcet-winning sets of size 2 under weak preferences.

Under partial orders (where agent preferences are incomplete), the relationship breaks down, and exponentially larger Condorcet-winning sets become necessary.

## Applications in Engineering

### 1. **Workforce Scheduling & Assignment**
- Assigning workers to shifts, projects, or teams where workers have ranked preferences
- Matching achieves fairness while respecting the constraint that each worker gets one assignment

### 2. **Network Routing & Resource Allocation**
- Matching edge-disjoint paths in communication networks (source-sink pairs)
- Server-to-client assignment in distributed systems with capacity constraints

### 3. **Organ Donation & Matching Markets**
- Matching donors to recipients in kidney exchange networks
- Popularity/Pareto concepts ensure fairness and reduce incentives to strategically misreport preferences

### 4. **Course Assignment**
- Assigning students to courses with capacity limits
- Agents' preferences over courses must be balanced against course capacities
- Condorcet concepts ensure no majority of students would prefer an alternative assignment

### 5. **Recommendation & Marketplace Systems**
- Matching buyers to products or sellers in two-sided markets
- Pareto optimality ensures no reassignment benefits everyone

### 6. **Manufacturing & Supply Chain**
- Matching jobs to machines with job preferences (due to processing times, tool requirements)
- Matching suppliers to manufacturers with mutual preference satisfaction

## Common Mistakes / Pitfalls

### 1. **Confusing Cardinality with Optimality**
- A maximum matching is not necessarily Pareto-optimal or popular
- Largest ≠ fairest. A matching of size $|A|-1$ can be preferable to all agents over a maximum matching

### 2. **Assuming Condorcet Winners Always Exist**
- Students often assume a "best" matching exists for all preference profiles
- **Reality**: Condorcet winners may not exist; Condorcet dimension captures how far you must relax to guarantee consensus

### 3. **Ignoring Preference Structure**
- Weak orders (total preferences) vs. partial orders behave *very differently*
- Under partial orders, exponential Condorcet dimension jumps from 2 to $\Theta(\sqrt{n})$ are possible
- Incomplete preferences are computationally harder (NP-hard to verify existence)

### 4. **Oversimplifying "Fairness"**
- Popularity (Condorcet winning) ≠ Pareto optimality ≠ envy-freeness
- Each is a different fairness criterion with different existence/computation properties

### 5. **Forgetting the Majority Requirement**
- A matching is popular if *no other* matching is preferred by *a strict majority*
- This is weaker