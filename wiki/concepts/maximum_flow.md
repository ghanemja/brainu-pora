# maximum flow

## Definition

**Maximum flow** is the greatest amount of "flow" (e.g., fluid, data, current) that can be sent from a source node $s$ to a sink node $t$ through a network graph $G = (V, E)$ while respecting edge capacity constraints.

Formally, given:
- A directed graph $G = (V, E)$ with edge capacities $c(e) \geq 0$ for each edge $e \in E$
- A source node $s \in V$ and sink node $t \in V$

A **flow** is a function $f: E \to \mathbb{R}_{\geq 0}$ satisfying:
1. **Capacity constraint**: $f(e) \leq c(e)$ for all $e \in E$
2. **Flow conservation**: For every node $v \neq s, t$: $\sum_{(u,v) \in E} f(u,v) = \sum_{(v,w) \in E} f(v,w)$

The **value** of a flow is: $|f| = \sum_{(s,v) \in E} f(s,v) - \sum_{(v,s) \in E} f(v,s)$

The **maximum flow problem** seeks to find a flow $f^*$ with maximum value $|f^*|$.

### Extensions

**Multiflow** generalizes the problem to multiple source-sink pairs $(s_i, t_i) \in P$. The goal is to simultaneously route flows for all pairs while respecting shared edge capacities.

**Multicut** is the dual problem: find a minimum-capacity set of edges (or vertices) whose removal disconnects all source-sink pairs.

## Key Equations

### Max-Flow Min-Cut Theorem

$$\max_{f} |f| = \min_{\text{cut}} \text{capacity}(\text{cut})$$

where a **cut** $C \subseteq E$ separates $s$ and $t$ if removing edges in $C$ disconnects $s$ from $t$.

### Flow Conservation (Node Constraint)

For $v \neq s, t$:
$$\sum_{(u,v) \in E} f(u,v) = \sum_{(v,w) \in E} f(v,w)$$

### Flow-Cut Gap (Directed Graphs)

For directed graphs with multiple demand pairs:
$$\text{Gap} = \frac{\text{min integral multicut}}{\text{max multiflow}}$$

Current known bounds:
- **Upper bound** (Bodwin & Samborska, 2026): $O(n^{1/3 + o(1)})$
- **Lower bound** (Chuzhoy & Khanna): $\Omega(n^{1/7})$
- **Undirected graphs** (Leighton & Rao): $\Theta(\log n)$ — tight

**Parameterized by cut weight $W$**: Gap $\leq W^{1/2}n^{o(1)}$

## Physical Intuition / Derivation

### Why Maximum Flow = Minimum Cut?

The max-flow min-cut theorem is intuitive:
1. Any flow from $s$ to $t$ must "cross" every cut separating them
2. Therefore, flow is upper-bounded by the capacity of any cut
3. The minimum-capacity cut gives the tightest upper bound
4. Optimization algorithms (Ford-Fulkerson, push-relabel) construct a flow that actually achieves this bound

### Why the Gap Matters (Directed vs. Undirected)

In the **single-pair case** (standard max-flow), the gap is always 1—integrality is free.

In the **multi-pair case** with **integral** routing:
- Each demand pair must use entirely separate paths (no fractional splitting)
- Different pairs compete for the same edges
- One integral path may "block" other pairs inefficiently
- Figure 1 example: integral cut must remove 2 edges (cost 2), but fractional cut needs only 3/2 capacity

**Directed graphs are harder** because:
- Edge directions create asymmetries; reversing flow direction may not be possible
- Undirected graphs can reroute flexibly in both directions
- The tight $\Theta(\log n)$ bound for undirected graphs does not hold for directed graphs

## Applications in Engineering

### 1. Network Routing & Telecommunications
- **Data center traffic**: Route multiple data flows maximizing throughput while respecting link bandwidths
- **VoIP networks**: Ensure concurrent calls reach destinations without congestion
- **SDN (Software-Defined Networks)**: Compute optimal routing policies using max-flow algorithms

### 2. Fluid & Gas Networks
- **Pipeline optimization**: Maximize oil/gas flow from production sites to refineries
- **Water distribution**: Route water through municipal networks meeting demand constraints
- **HVAC systems**: Balance heating/cooling fluid circulation

### 3. Electrical Power Systems
- **Power grid dispatch**: Route power from generators to loads without line overload
- **Fault tolerance**: Compute maximum power that can be rerouted after line failures

### 4. Transportation & Logistics
- **Vehicle routing**: Maximize commodity flow through highway/rail networks
- **Supply chain**: Route goods through warehouses and distribution centers
- **Airport capacity**: Optimize passenger flow through terminals and security checkpoints

### 5. Computational Complexity & Hardness
- **Approximation algorithms**: Used as subroutine for clustering, load balancing, and network design
- **Hardness reductions**: Flow-cut gap bounds give inapproximability results for related problems (e.g., multicut, sparsest cut)

## Common Mistakes / Pitfalls

### 1. Confusing Flow with Capacity
**Mistake**: Assuming all edges in the optimal solution carry flow equal to their capacity.
**Reality**: Optimal flows often leave edges partially utilized; max-flow doesn't require "saturating" every edge.

### 2. Assuming Integrality is Free
**Mistake**: Treating integral and fractional max-flow as equivalent in multi-pair settings.
**Reality**: In multiflow/multicut, fractional solutions can be much better. The gap grows with $n$, making integral approximation hard.