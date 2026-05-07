# s-t-flows

## Definition

An **s-t-flow** is a function $f: E \to \mathbb{R}_{\geq 0}$ on the edge set $E$ of a directed graph $G = (V, E)$ that satisfies flow conservation constraints at all intermediate vertices. For distinguished source vertex $s$ and sink vertex $t$:

$$\sum_{e \text{ entering } v} f(e) = \sum_{e \text{ leaving } v} f(e) \quad \forall v \in V \setminus \{s, t\}$$

The **value** of the flow is the net outflow from $s$ (or equivalently, net inflow to $t$).

In the context of controllability and identifiability, an **s-t-flow set** $X$ refers to the convex hull of all valid integer-valued s-t-flows in a network, forming a polyhedron in $\mathbb{R}^{|E|}$.

## Key Equations

**Flow conservation (Kirchhoff's law):**
$$\sum_{e=(u,v)} f(e) - \sum_{e=(v,w)} f(e) = \begin{cases} -F & v = s \\ F & v = t \\ 0 & \text{otherwise} \end{cases}$$

where $F$ is the total flow value.

**Capacity constraints (variant):**
$$0 \leq f(e) \leq c(e) \quad \forall e \in E$$

**Identifying set condition for s-t-flows:**
An edge set $S \subseteq E$ is *identifying* for s-t-flows if knowledge of $f|_S$ (flow values restricted to $S$) uniquely determines the entire flow $f$. By Theorem 4.1, $S$ is identifying if and only if its complement $E \setminus S$ is a cut in the cographic matroid sense.

## Physical Intuition / Derivation

### Why s-t-flows matter

s-t-flows model transport phenomena across networks—electricity through power grids, data through networks, fluid through pipes, or traffic through roads. The fundamental constraint is **conservation**: flow entering a junction equals flow leaving it (except at source and sink).

### Identifying sets intuition

In practice, we cannot measure flow on every edge. The question naturally arises: *which edges must we monitor to uniquely determine all flows?*

Consider a simple example with parallel edges between two nodes:
- If we measure flow on only one edge, we cannot distinguish between different distributions across parallel edges
- But if we measure flow entering and leaving the entire set of parallel edges, we've "identified" all possible flow distributions across them

More formally, suppose edges form a cycle. By flow conservation, if we know flow on all but one edge in the cycle, the remaining edge's flow is determined. Thus, **cycles create redundancy**—we don't need to measure every edge.

The cographic matroid captures precisely this structure. An identifying set's complement must form a cut, meaning removing those edges disconnects $s$ from $t$. Equivalently, we must measure enough edges that the unmeasured edges cannot form a cycle.

### Why s-t-paths vs. s-t-flows differ

- **s-t-paths**: discrete objects (sequences of edges with $f(e) \in \{0,1\}$)
- **s-t-flows**: continuous convex hull of all paths (allowing $f(e) \in [0,\infty)$)

A minimum identifying set for s-t-flows can be significantly smaller than for paths. The source material shows a $\sqrt{m}$ gap (where $m = |E|$) for acyclic networks.

## Applications in Engineering

### 1. **Electrical Network Monitoring**
Monitor a subset of power lines to uniquely infer all line flows, enabling:
- Grid fault detection
- Load balancing verification
- Loss accounting

Theorem 4.1 provides polynomial-time algorithms to minimize the number or total length of monitored lines.

### 2. **Fluid/Gas Pipeline Networks**
- Determine unknown flow distributions from partial measurements
- Verify integrity of multi-branch pipeline systems
- Design sensor placement for supply chain networks

### 3. **Communication Networks**
- Infer complete traffic patterns from measurements at subset of links
- Anomaly detection: unexpected deviations from flow conservation
- Network tomography and inference

### 4. **Transportation Networks**
- Infer vehicle flows on unmeasured road segments
- Design optimal placement of traffic sensors
- Validate origin-destination demand matrices

### 5. **Supply Chain / Logistics**
- Track commodity flows through distribution networks with minimal counting/measuring
- Detect unaccounted diversions or losses

## Computational Complexity

The difficulty of finding minimum-size identifying sets varies dramatically by setting:

| Setting | Complexity | Algorithm |
|---------|-----------|-----------|
| General s-t-paths (cyclic networks) | $\Sigma_P^2$-complete | None polynomial |
| s-t-paths (acyclic networks) | NP-hard | $\sqrt{m}$-approximation available; 2-hardness |
| s-t-flows | Polynomial | Uses cographic matroid (Theorem 4.1) |
| Matroid bases | Polynomial | Partition matroid characterization |
| Explicit binary vectors | NP-hard | $2\ln\|X\|$-approximation (optimal up to constants) |

## Common Mistakes / Pitfalls

1. **Confusing paths with flows:** Not all identifying sets for paths identify flows. Flows are richer (convex combinations), requiring fewer measurements.

2. **Assuming edge-level measurement:** Students often think "measure flow on each edge." In reality, we measure net flow across cuts or at selected nodes/edges.

3. **Overlooking cycles:** Cycles create dependencies. Edges in a cycle carry dependent information; not all need measurement. The cographic matroid makes this precise.

4. **Ignoring hardness gaps:** For paths in general networks, the problem becomes dramatically harder (from polynomial to $\Sigma_P^2$-complete). A small graph difference matters enormously.

5. **Forgetting integrality:** The framework works for both integral and fractional flows, but identifying sets for integral flows may be larger due to discrete constraints.

## See Also

- [[Matroid and