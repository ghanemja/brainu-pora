# st-cut

## Definition

An **st-cut** (or **source-sink cut**) in a directed graph $G = (V, E)$ with designated vertices $s, t \in V$ is a subset $Z \subseteq E$ of edges whose removal disconnects all paths from $s$ to $t$. Equivalently, a cut partitions the vertices into two disjoint sets $S$ and $T$ such that $s \in S$, $t \in T$, and $Z$ consists of all edges crossing from $S$ to $T$.

**Formal statement:** An st-cut is a set of edges $Z$ such that every path from $s$ to $t$ contains at least one edge in $Z$.

**Capacity of a cut:** If each edge $e$ has a non-negative weight $c(e)$ (capacity), the capacity of cut $Z$ is:
$$\text{cap}(Z) = \sum_{e \in Z} c(e)$$

**Partition representation:** Equivalently, an st-cut corresponds to a partition $(S, T)$ with $S \cap T = \emptyset$, $S \cup T = V$, $s \in S$, $t \in T$. The cut then comprises all edges $(u,v) \in E$ where $u \in S$ and $v \in T$.

## Key Equations

**Minimum st-cut:**
$$\text{Min-Cut}(s,t) = \min_{Z \text{ is an st-cut}} \text{cap}(Z)$$

**Max-flow min-cut theorem:**
$$\max_{\text{flow } f: s \to t} \text{value}(f) = \min_{Z \text{ is an st-cut}} \text{cap}(Z)$$

This fundamental result states that the maximum flow from $s$ to $t$ equals the minimum capacity of any st-cut separating them.

**Parameterized variant (p-Split Min Cut):** Find an st-cut $Z$ that is the union of exactly $k$ bundles from a set $\mathcal{B}$ of pairwise disjoint edge sets, where each bundle contains at most one edge from each of $p$ components. The problem is parameterized by $k$ (not the graph size).

## Physical Intuition / Derivation

### Intuitive Understanding

Imagine a network where $s$ is a source (e.g., water supply) and $t$ is a sink (e.g., demand point). An st-cut represents a "barrier" of edges that, if removed, completely severs flow from source to sink. The minimum st-cut is the most efficient barrier—it requires the fewest resources to block all flow.

### Why Min-Cut Matters

The max-flow min-cut theorem reveals a deep duality: rather than computing the maximum amount of flow that can pass from $s$ to $t$, one can equivalently find the minimum "bottleneck" (cut) that constrains flow. This transforms an optimization problem into its dual, often yielding computational advantages.

### Parameterized Complexity Motivation

In **p-Split Min Cut**, the twist is that not all edge subsets form valid cuts—only unions of at most $k$ pre-defined bundles. This models scenarios where:
- Edges are grouped by function or resource type (the bundles)
- We wish to disable exactly $k$ functional groups to sever connectivity
- The goal is FPT algorithms or hardness results in the parameter $k$

The source material discusses $(p-\varepsilon)$-inapproximability: even approximating the minimum number of bundles needed to form an st-cut is computationally hard unless $p \leq \varepsilon$ (under ETH assumptions).

## Applications in Engineering

### Network Flow & Logistics
- **Supply chain optimization:** Identifying critical bottlenecks in distribution networks where removing $k$ suppliers/routes disconnects end customers from sources.
- **Telecommunications:** Finding minimum-cost link failures that partition a network; used in network resilience analysis.

### Electrical Power Systems
- **Cascading failure analysis:** Computing minimum edge cuts to identify vulnerability of power grids; related to resilience metrics.
- **Load balancing:** Finding critical transmission lines whose failure most impacts grid connectivity.

### Computer Networks
- **Routing protocols:** Determining minimum edge sets (firewalls, routing rules) needed to isolate malicious traffic or prevent unauthorized access.
- **Data center networking:** Identifying critical paths and redundancy requirements.

### Structural Engineering & Reliability
- **Failure mode analysis:** Interpreting st-cuts as minimal failure scenarios in systems modeled as graphs (e.g., steel frame connections, communication topologies).

### Algorithm Design for Combinatorial Optimization
- **Decomposition algorithms:** Min-cut oracles are building blocks in parametric search, binary search on objectives, and Lagrangian relaxation.
- **Approximation algorithms:** Rounding solutions from LP relaxations of min-cut yields constant-factor approximations for many NP-hard problems.

## Common Mistakes / Pitfalls

1. **Confusing cut with path:** A cut is a *set of edges* whose removal disconnects $s$ from $t$, not a path itself. Students sometimes think of cutting a single edge.

2. **Forgetting the partition view:** An st-cut must separate $s$ and $t$ into different partitions $(S, T)$. Not every edge set is a valid cut.

3. **Edge directionality:** In directed graphs, the cut $(S, T)$ only includes edges $u \to v$ with $u \in S, v \in T$. The reverse direction is ignored. This is critical for directed vs. undirected graphs.

4. **Parameterized hardness misinterpretation:** The $(p-\varepsilon)$-inapproximability of **p-Split Min Cut** does not mean standard min-cut is hard. Rather, it means if we restrict cuts to be unions of $k$ bundles (a stronger constraint), approximation becomes hard in the parameter $k$.

5. **Capacity weights:** Students may forget that min-cut depends on edge weights. An st-cut with many edges might have smaller capacity than a cut with fewer edges if weights are unequal.

6. **Confusing minimum with maximum:** Max-flow min-cut is a duality theorem; they are equal, not opposites. The dual of minimizing