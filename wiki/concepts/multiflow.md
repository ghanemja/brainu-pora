# Multiflow

## Definition

A **multiflow** is a generalization of single-source single-sink network flow to handle multiple concurrent demand pairs. Given a directed graph $G = (V, E)$ with edge capacities $c: E \to \mathbb{R}^+$ and a set of demand pairs $P \subseteq V \times V$, a multiflow assigns a flow value $f_{s,t}$ to each pair $(s,t) \in P$ such that:

1. For each pair $(s,t) \in P$, flow conservation holds at all intermediate nodes
2. For each edge $e \in E$, the total flow through $e$ respects its capacity: $\sum_{(s,t) \in P} f_{s,t}(e) \leq c(e)$

The **maximum multiflow value** is:
$$\text{OPT}_{\text{flow}} = \max \sum_{(s,t) \in P} f_{s,t}$$

where the maximum is over all feasible multiflows satisfying the constraints above.

In the **fractional** setting, flows are allowed to be arbitrary non-negative reals. In the **integral** setting, flows must be integer-valued (or equivalently, decomposable into unit-flow paths by the flow decomposition theorem).

## Key Equations

### Max-Flow Min-Cut Duality (Single Pair)
For a single source-sink pair $(s,t)$:
$$\max \text{ } s\text{-}t \text{ flow} = \min \text{ } s\text{-}t \text{ cut capacity}$$

### Fractional Multiflow-Multicut Duality
For multiple demand pairs:
$$\max \text{ fractional multiflow} = \min \text{ fractional multicut}$$

This holds by LP duality, where a **fractional multicut** assigns weights $w(S)$ to each cut that simultaneously separates all pairs in $P$, with total weight $\sum_{\text{cuts}} w(S) \cdot c(S)$.

### Flow-Cut Gap
The central quantity of interest is the **flow-cut gap**:
$$\text{gap}(n) = \max_{G, P, c} \frac{\text{OPT}_{\text{integral multicut}}}{\text{OPT}_{\text{fractional multiflow}}$$

Current best upper bound (Bodwin & Samborska, 2026):
$$\text{gap}(n) \leq n^{1/3 + o(1)}$$

Current best lower bound (Chuzhoy & Khanna, 2009):
$$\text{gap}(n) \geq \Omega(n^{1/7})$$

## Physical Intuition / Derivation

### Why the Gap Exists

The key insight is that **fractional flows can "split" across multiple paths** in ways that integral flows cannot. Consider the example from Figure 1:

- **Fractional multicut**: Can assign fractional capacities (e.g., 1/2 to three separate edges) to cut all demand pairs simultaneously, achieving total cost 3/2.
- **Integral multicut**: Must remove entire edges with integer costs. The minimum set of edges that separates all pairs has cost 2.
- **Multiflow**: The fractional multiflow achieves value 3/2, matching the fractional cut by duality.

The gap emerges because integer constraints are fundamentally more rigid—you cannot "waste" partial edge capacity on unfulfilled demand.

### Directed vs. Undirected Complexity

For **undirected graphs**, the flow-cut gap is $\Theta(\log n)$ (Leighton-Rao). This is because undirected graphs have rich symmetry: routing can bypass obstacles more flexibly.

For **directed graphs**, the gap is much larger: $n^{1/3 + o(1)}$. The asymmetry of directed edges severely constrains routing alternatives. If you must reach node $t$ from $s$ in a directed graph, you cannot "go around" in the reverse direction.

### Reduction to Structural Parameters

A recent contribution (Bodwin & Samborska) shows the gap depends more fundamentally on $W$, the sum of minimum fractional cut weights:
$$\text{gap}(W) \leq W^{1/2} n^{o(1)}$$

This suggests the gap is controlled by the **density of bottlenecks** rather than pure graph size.

## Applications in Engineering

### Network Design and Resource Allocation
- **Data center routing**: Multiple services (demand pairs) must be routed simultaneously through a network with limited link capacities. The gap quantifies how much extra infrastructure is needed when demands must be routed integrally (e.g., on MPLS paths rather than fractionally split).

### Telecommunications
- **Optical network provisioning**: Determining minimum fiber capacity needed when multiple circuits must be provisioned with integer demands, rather than allowing fractional wavelength sharing.

### Logistics and Supply Chain
- **Multi-commodity flow problems**: Routing multiple types of goods through transportation networks where each arc has limited capacity. The flow-cut gap bounds the inefficiency of requiring integral commodity units.

### Approximation Algorithms
- **Hardness of approximation**: The flow-cut gap directly relates to the approximation factor achievable for multicommodity flow and multicut problems. A gap of $g$ means no algorithm can simultaneously achieve a $g/2$ approximation to both the primal and dual formulations.

### Capacity Planning
- **Worst-case provisioning**: The gap answers: "How much larger must a network's capacity be to guarantee integral routing of any multicommodity demand compared to an optimal fractional routing?"

## Common Mistakes / Pitfalls

### 1. Confusing Flow and Multicut Optimization
**Mistake**: Assuming the minimum multicut directly equals the maximum multiflow without checking integrality.

**Correction**: The equality holds only for *fractional* versions (by LP duality). Integer versions differ by the flow-cut gap. Always specify whether you're working with integral or fractional variants.

### 2. Assuming Undirected Bounds Apply to Directed Graphs
**Mistake**: Using the $\Theta(\log n)$ bound for undirected graphs on directed problems.

**Correction**: Directed graphs have exponentially worse gaps: $\