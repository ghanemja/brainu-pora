# Partial Order Preferences

## Definition

**Partial order preferences** describe agent preferences over alternatives when agents can only comparatively rank some pairs of alternatives, without requiring a total ordering over all options. In contexts with structured constraints (e.g., graph-based matching), agents' preferences over elementary choices (edges, arcs) are **lifted** to preferences over feasible compound alternatives (matchings, arborescences, branchings).

Formally, given an agent $a$ and two alternatives $X, X'$:
- Agent $a$ has a **partial order** $\succ_a$ over a set of base elements (e.g., incoming arcs $\delta^-_D(a)$)
- This preference extends to compound structures via **restriction**: 
$$X \succ_a X' \iff (X \cap S_a) \succ_a (X' \cap S_a)$$
where $S_a$ is the set of relevant elements for agent $a$.

This lifting is crucial because agents typically cannot express preferences directly over all feasible solutions; instead, they naturally prefer alternatives based on their constituent parts.

## Key Equations

For arborescence instances with incoming arc preferences:

$$T \succ_a T' \iff T \cap \delta^-_D(a) \succ_a T' \cap \delta^-_D(a)$$

where:
- $T, T'$ are $r$-arborescences (directed spanning trees rooted at $r$)
- $\delta^-_D(a)$ is the set of incoming arcs to agent $a$ in directed graph $D$
- $T \cap \delta^-_D(a)$ is the incoming arc selected by arborescence $T$ for agent $a$

For matroid-constrained matching with object preferences:

$$M \succ_a M' \iff M(a) \succ_a M'(a)$$

where $M(a)$ denotes the object matched to agent $a$ in matching $M$, and the constraint is:
$$M(A) \in \mathcal{I}$$
meaning the set of matched objects forms an **independent set** of the underlying matroid.

## Physical Intuition / Derivation

### Why Partial Orders?

In many real-world problems, agents cannot express complete rankings over all feasible outcomes. Instead, they have **local preferences** over elements directly affecting them:

- **Delegation networks**: A person cares whom they delegate to (their incoming arcs) but may be indifferent between distant nodes' configurations
- **Supply chain routing**: A node prefers certain incoming suppliers but has no opinion on unrelated subgraph structures
- **Resource allocation**: An agent ranks feasible resource bundles they receive but doesn't rank hypothetical bundles for others

### Lifting Preferences

The lifting mechanism converts **local preferences** into **global preferences** on feasible outcomes by comparing only the locally-relevant parts:

1. Agent $a$ has preferences $\succ_a$ over the arcs/objects they directly interact with
2. Two alternatives $X$ and $X'$ are compared by extracting only the part relevant to $a$
3. This extraction creates a **projection** of complex alternatives onto agent-specific subspaces

**Key insight**: This lifting preserves the structure of agents' true preferences—they only care what reaches *them*, not the global configuration.

### Reduction to Matroid-Constrained Matching

The arborescence problem (with partial order preferences) reduces to matroid-constrained matching because:

1. **Graphic matroid** captures acyclicity: independent sets = acyclic edge subsets
2. **Bases of graphic matroid** = $r$-arborescences (acyclic, spanning, rooted)
3. **Objects** = directed edges; **agents** = nodes receiving those edges
4. Agent $a$ "matches" to (one of) their incoming edges
5. Feasibility constraint: matched edges form an acyclic subgraph (enforced by matroid independence)

This shows partial order preferences over constrained combinatorial structures are unifying frameworks across multiple domains.

## Applications in Engineering

### 1. Delegation and Liquid Democracy
In blockchain-based governance or liquid democracy systems, individuals delegate voting power to representatives. Each person cares about *who receives their delegation*, not the global delegation structure. Partial orders capture this local preference, enabling efficient preference aggregation over feasible delegation trees.

### 2. Supply Chain Networks and Routing
In logistical networks, each facility prefers incoming suppliers/routes (partial preference) without caring about distant network segments. Partial order preferences optimize local decisions while respecting global acyclicity constraints (no circular dependencies), critical for just-in-time supply chains.

### 3. Organizational Hierarchy and Command Structures
In designing hierarchies, each subordinate ranks preferred supervisors. Partial order preferences ensure valid tree structures (one manager per subordinate) while respecting agents' local preferences, important for matrix organizations balancing authority structures.

### 4. Wireless Network Routing
In ad-hoc networks, each node prefers certain parent nodes (for routing) based on signal strength and latency. Partial orders aggregate these local preferences into spanning tree topologies without redundant cycles, minimizing congestion and latency.

### 5. Matroid-Constrained Resource Allocation
Engineers allocating resources (bandwidth, computing, memory) to agents under independence constraints (e.g., non-overlapping frequency bands, disjoint data segments) leverage matroid-constrained matching with partial order preferences to ensure stability and efficiency.

## Common Mistakes / Pitfalls

### 1. Confusing Partial Orders with Total Orders
**Mistake**: Assuming agents have complete rankings and can always decide between any two alternatives.
**Reality**: Partial orders may leave some alternatives incomparable. An agent might not prefer $T$ over $T'$ nor $T'$ over $T$—they could be incomparable.
**Fix**: Verify that your preference structure is actually a partial order (reflexive, transitive, antisymmetric on comparable pairs) before applying solution concepts.

### 2. Forgetting the Lifting Operation
**Mistake**: Stating agent preferences directly over arborescences/matchings without clarifying how local arc/object preferences induce them.
**Reality**: The lifting must preserve the logical structure—alternatives are only comparable if agents' local components differ in a way they can rank.
**Fix**: Always explicitly write the projection operation (e.g., $T \cap \delta^-_D(