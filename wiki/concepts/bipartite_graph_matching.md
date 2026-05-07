# Bipartite Graph Matching

## Definition

A **bipartite graph matching** is a selection of edges in a bipartite graph $G = (A \cup O, E)$ such that no two edges share a common vertex. In the context of matching instances, we seek to assign agents $a \in A$ to objects $o \in O$ via edges $(a, o) \in E$, where each agent and object is matched to at most one counterpart.

Formally, a **matching** $M \subseteq E$ is valid if for all distinct edges $(a_1, o_1), (a_2, o_2) \in M$: $a_1 \neq a_2$ and $o_1 \neq o_2$.

**Perfect matching**: A matching covering all vertices (when $|A| = |O|$).

**Popular matching**: In preference-based settings, a matching $M$ is *popular* if no other matching $M'$ is preferred by a strict majority of agents relative to $M$.

**Weak Condorcet dimension**: The minimum size $k$ of a set of matchings such that every agent's top choice appears in at least one matching in the set.

## Key Equations

**Hall's Marriage Theorem** (existence condition for perfect matching):
A bipartite graph $G = (A \cup O, E)$ has a matching covering all agents in $A$ if and only if:
$$\forall X \subseteq A: |\Gamma_G(X)| \geq |X|$$
where $\Gamma_G(X)$ is the set of neighbors (adjacent objects) to vertices in $X$.

**Upper bound on weak Condorcet dimension** (partial-order preferences):
$$k \leq \left\lceil\sqrt{2|A|}\right\rceil$$

**Lower bound on weak Condorcet dimension**:
$$k \geq \sqrt{|A|} \text{ (up to polynomial factors)}$$

## Physical Intuition / Derivation

### The Matching Problem

Imagine assigning $n$ job applicants to $m$ positions where not all applicants qualify for all positions. This naturally forms a bipartite graph: applicants on one side, positions on the other, with edges representing eligibility.

A matching finds a valid assignment—no person gets two jobs, no job goes to two people.

### Why Preferences Matter

In practice, agents have preferences over objects. Hall's theorem tells us *when* a perfect matching exists (structurally), but says nothing about quality.

**Preference representation**: Under partial-order preferences, an agent $a$ has a partial preference relation $\prec_a$ over objects. Not all pairs need be comparable (they may be indifferent).

### Popular vs. Pareto-Optimal

- **Popular matching**: Robust to majority preference—no alternative matching makes more than 50% of agents strictly better off.
- **Pareto-optimal matching**: No agent can be made better off without harming another.

These are *fundamentally different* notions:
- Finding Pareto-optimal matchings under partial-order preferences is **NP-complete** (Theorem 6.2).
- Finding popular sets of matchings can be approximated in polynomial time (Theorem 5.2).

### Lower Bound Construction (Theorem 5.1)

The proof constructs a pathological instance with $k^2 + k + 1$ agents and objects:
- One "hotly contested" object $o^*$
- $k$ "acceptable" objects in $O_1$
- $k^2$ "undesirable" objects in $O_2$
- All agents have identical preferences: $o^* \succ \text{everything} \succ O_2$, indifferent over $O_1$

**Key insight**: With only $k$ disjoint matchings, at most $k$ agents can be assigned $o^*$ across all matchings (by pigeonhole). Remaining agents must be satisfied by $O_1 \cup O_2$. Since $k \cdot |O_1| = k^2 < k^2 + k$ agents remain, at least one agent lands in $O_2$ in *every* matching—forcing a new matching to satisfy them. This cascades until we need $\Theta(\sqrt{|A|})$ matchings.

## Applications in Engineering

### 1. **Resource Allocation**
- Assigning cloud computing tasks to servers
- Matching manufacturing jobs to machines with capability constraints
- Power grid load balancing (generators to demand zones)

### 2. **Logistics and Supply Chain**
- Vehicle routing: matching delivery routes to available trucks
- Warehouse slot assignment: storing items in appropriate bins
- Vendor-buyer matching under contract constraints

### 3. **Telecommunications**
- Call routing: connecting calls to available circuits
- Spectrum allocation: assigning frequency bands to users
- Network flow optimization via matching decomposition

### 4. **Human Resources**
- Project team formation (skills-to-roles)
- Shift scheduling with worker preferences
- Intern/apprentice placement programs

### 5. **Two-Sided Markets**
- Online marketplace seller-buyer matching
- Dating/social network recommendations
- Ride-sharing (drivers to passengers)

## Common Mistakes / Pitfalls

1. **Confusing matching with flow**: A matching is a *special case* of integer flow where capacities are 1. Not all flow-optimal solutions are matchings.

2. **Hall's theorem guarantees existence, not optimality**: Satisfying Hall's condition means a perfect matching *exists*, but says nothing about preference satisfaction.

3. **Assuming partial preferences are total orders**: In reality, agents may be indifferent between many options. Algorithms for total preferences (e.g., stable matching) may not apply.

4. **NP-hardness of Pareto-optimality doesn't mean popularity is hard**: Theorem 6.2 shows Pareto-optimality is hard under partial orders, but Theorem 5.2 gives a polynomial-time approximation for popularity.

5. **Greedy matching can fail spectacularly**: A greedy algorithm matching agents in order may violate Hall's condition downstream, leaving later agents unmatched—always use algorithmic approaches rooted in theorems.

6. **Assuming small preference sets imply easy computation**: Even with sparse preferences, counting/enumerating popular matchings can be exponential in the worst case.