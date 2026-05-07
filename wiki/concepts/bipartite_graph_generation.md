# bipartite graph generation

## Definition

**Bipartite graph generation** is the algorithmic problem of constructing bipartite networks satisfying prescribed degree sequences when only partial network information is available. A bipartite graph $G = (U, V, E)$ consists of two disjoint vertex sets $U$ and $V$ with edges only between the sets (never within). The **degree sequence** specifies $d_u$ for each $u \in U$ and $d_v$ for each $v \in V$—the number of edges incident to each vertex.

The generation problem asks: *Given desired degree sequences for both vertex sets, construct a valid bipartite graph (or sample from all valid configurations, or enumerate them).*

This differs from arbitrary graph generation because:
- **Bipartiteness is structural**: connections are restricted to cross between $U$ and $V$
- **Partial information**: the full network is unknown; only aggregate degree constraints are specified
- **Feasibility**: not all degree sequences are realizable; necessary and sufficient conditions must be verified

## Key Equations

### Degree Sequence Feasibility

For bipartite graphs, the **necessary and sufficient condition** for a degree sequence $(d_1^{(U)}, \ldots, d_{m}^{(U)}, d_1^{(V)}, \ldots, d_n^{(V)})$ to be graphical is the **Gale-Ryser theorem**:

$$\sum_{i=1}^{m} d_i^{(U)} = \sum_{j=1}^{n} d_j^{(V)}$$

(total degrees must match), and after sorting in decreasing order:

$$\sum_{i=1}^{k} d_i^{(U)} \leq \sum_{j=1}^{n} \min(k, d_j^{(V)}) \quad \forall k = 1, \ldots, m$$

### Sequential Feasibility Interval

At step $t$ in sequential construction, when connecting vertex $u_t \in U$ (or $v_t \in V$), the **admissible interval** for new edges is:

$$\left[\max(0, d_t - |V|_{\text{saturated}}), \min(|V|_{\text{available}}, d_t)\right]$$

where $|V|_{\text{saturated}}|$ counts vertices in $V$ already at their degree limit, and $|V|_{\text{available}}|$ is the remaining capacity.

The key contribution of Sun et al. is establishing that respecting this interval at each step **guarantees global feasibility**, eliminating costly backtracking in enumeration and sampling.

## Physical Intuition / Derivation

### Why Bipartite Graphs?

Bipartite structures naturally model many real-world networks:
- **Supply chain networks**: suppliers (set $U$) ↔ buyers (set $V$)
- **Financial systems**: banks ↔ assets or counterparties
- **Epidemiology**: infected ↔ susceptible populations
- **Recommendation systems**: users ↔ items

The constraint that edges only cross between sets reflects the *fundamental categorical distinction* between the two populations.

### Sequential Construction Logic

Building graphs edge-by-edge from left to right offers computational advantages:

1. **Process vertex $u_1 \in U$ first**: decide how many edges it will have (must be $d_1^{(U)}$)
2. **Distribute degree among $V$**: spread these $d_1^{(U)}$ connections across vertices in $V$
3. **Check feasibility before committing**: once $u_1$ edges are placed, remaining subproblem must still be solvable with the remaining degree sequence
4. **Move to $u_2, \ldots, u_m$**: repeat

The **interval condition** arises from:
- **Lower bound**: must leave enough "room" in $V$ for high-degree vertices not yet connected
- **Upper bound**: cannot exceed remaining capacity in the vertices we connect to

### Necessity of the Interval

If we violate the interval, future steps may become infeasible. For example:
- Connecting $u_t$ to too few vertices in $V$ may leave $V$-vertices with unsatisfiable remaining degree
- Connecting to too many saturates $V$ prematurely, blocking connections needed by later $U$-vertices

## Applications in Engineering

### 1. **Systemic Risk Assessment**
Generate plausible financial network structures given only:
- Number of banks and their observed portfolio sizes
- Market data on total interconnection volume

Enables stress testing and contagion modeling without complete disclosure of bilateral exposures.

### 2. **Supply Chain Resilience**
Given aggregate supplier capacity and buyer demand:
- Enumerate feasible supplier-buyer matching topologies
- Identify structural vulnerabilities to single-node failures
- Design robust matching strategies

### 3. **Epidemiological Modeling**
With only aggregate contact rates (not individual pairs), generate contact networks for stochastic disease simulation under different structural assumptions.

### 4. **Recommendation System Design**
Sample bipartite user-item interaction networks respecting:
- User activity constraints (items each user engages with)
- Item popularity constraints (users per item)

Enables privacy-preserving algorithm evaluation.

### 5. **Network Inference Problems**
When observing only degree sequences (not edges), generate the set of *all consistent networks* to:
- Bound estimates of systemic risk
- Quantify uncertainty in network-based metrics

## Common Mistakes / Pitfalls

### 1. **Assuming All Degree Sequences Are Realizable**
**Mistake**: Not checking Gale-Ryser conditions before attempting graph construction.  
**Consequence**: Algorithms fail without clear diagnostic information.  
**Fix**: Always verify necessary conditions first; use bipartite-specific theorems, not general graph conditions.

### 2. **Greedy Assignment Without Lookahead**
**Mistake**: Sequentially assigning edges without checking if remaining vertices can satisfy their degree requirements.  
**Consequence**: Dead ends; backtracking required or incomplete graphs generated.  
**Fix**: Compute and respect the **interval bounds** at each step before committing edges.

### 3. **Confusing Bipartite with Directed**
**Mistake**: Applying undirected graph algorithms