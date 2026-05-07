# flow-cut gap

## Definition

The **flow-cut gap** is the maximum possible ratio between the minimum integral multicut and the maximum multiflow (equivalently, the minimum fractional multicut) for a given graph and set of demand pairs.

Formally, given a directed graph $G = (V, E)$ with edge capacities and a set of demand pairs $P \subseteq V \times V$:

$$\text{flow-cut gap} = \max_{G,P} \frac{\text{OPT}_{\text{integral multicut}}(G, P)}{\text{OPT}_{\text{fractional multicut}}(G, P)}$$

where the maximum is taken over all possible graphs and demand sets of a given size (typically parameterized by the number of nodes $n$).

The flow-cut gap represents the **integrality gap** of the multicut problem—the loss incurred when restricting from fractional to integral solutions.

## Key Equations

By LP duality, the fractional multicut equals the maximum multiflow:
$$\text{OPT}_{\text{fractional multicut}}(G, P) = \text{OPT}_{\text{multiflow}}(G, P)$$

Therefore, the flow-cut gap can equivalently be expressed as:
$$\text{flow-cut gap} = \max_{G,P} \frac{\text{OPT}_{\text{integral multicut}}(G, P)}{\text{OPT}_{\text{multiflow}}(G, P)}$$

### Known Bounds (Directed Graphs)

**Upper bounds (state-of-the-art):**
- General $n$-node directed graphs: $\tilde{O}(n^{1/3})$ (Bodwin & Samborska, 2026)
- Weighted by fractional cut weight $W$: $\tilde{O}(W^{1/2})$
- Previous best: $\tilde{O}(n^{11/23})$ (Agarwal, Alon, Charikar, 2007)

**Lower bounds:**
- $\Omega(n^{1/7})$ (Chuzhoy & Khanna, 2009)

**Undirected graphs (essentially closed):**
- Both upper and lower bounds: $\Theta(\log n)$ (Leighton & Rao, 1988 and others)

## Physical Intuition / Derivation

### Why the Gap Exists

Consider the example in Figure 1 (from source material):
- Three demands: $(s_1, t_1)$, $(s_2, t_2)$, $(s_3, t_3)$
- Minimum **integral** multicut: must remove enough edges to disconnect all three pairs simultaneously → cost = 2
- Minimum **fractional** multicut: can "split" capacity across routes → cost = 3/2
- Gap in this instance: $2 / (3/2) = 4/3$

The fundamental reason: when flows must be routed integrally (as whole units), they cannot be distributed flexibly across multiple paths. A fractional solution can send partial flow along many paths, effectively "averaging" the routing cost.

### Connection to Min-Cut Max-Flow Theorem

The classical **Min-Cut Max-Flow (MCMF) Theorem** states that for a single source-sink pair $(s, t)$, the maximum flow equals the minimum cut:
$$\max_{s \text{-} t \text{ flow}} = \min_{s \text{-} t \text{ cut}}$$

This theorem holds for both integral and fractional flows because:
1. A single pair has only one "direction" to satisfy
2. Flow can be routed along a single path without loss of optimality
3. The integral and fractional solutions coincide

However, with **multiple demand pairs**, the presence of competing demands breaks this equivalence. Integral routings of different pairs can interfere constructively (requiring larger cuts), while fractional routings can weave around each other more efficiently.

### Why Directed Graphs Are Harder

Directed graphs exhibit far worse flow-cut gaps than undirected graphs:
- **Undirected**: $\Theta(\log n)$ (tight)
- **Directed**: $n^{1/7}$ to $n^{1/3}$ (loose gap in bounds)

Intuition: In undirected graphs, an "alternative route" in one direction is also an alternative in the reverse direction, providing symmetry. Directed graphs lack this symmetry; a cut separating $s \to t$ may not separate $t \to s$, leading to fundamentally different bottleneck structures.

## Applications in Engineering

### Network Design & Routing

- **Telecommunications**: Computing the integrality gap helps bound the worst-case over-provisioning needed when routing must use integer unit paths rather than fractional load-splitting
- **Data center networks**: Flow-cut gap bounds inform capacity requirements when routing protocols are restricted to integral flows (common in practice)

### Approximation Algorithms

- **Multicut approximation**: Upper bounds on the flow-cut gap immediately yield approximation algorithms (the gap bounds how well a fractional solution can be rounded)
- **Resource allocation**: If the gap is $\alpha$, then optimal integral solutions require at most $\alpha$ times the minimum fractional requirement

### Optimization Under Integrality Constraints

- **Logistics & transportation**: Routing whole shipments (integral) versus splitting shipments (fractional) across network
- **Supply chain optimization**: Quantifying the cost of requiring integer unit flows in multi-commodity flow problems

### Theoretical Complexity Analysis

- **Hardness of approximation**: Flow-cut gap lower bounds translate to approximation lower bounds for the multicut problem (assuming NP $\neq$ P)
- **Algorithm design**: Guides development of rounding schemes and approximation algorithms

## Common Mistakes / Pitfalls

### Mistake 1: Confusing with Single-Pair Cut

Students often assume that since MCMF holds for single $(s, t)$ pairs, it must hold for multiflows. The key difference: multiple pairs create *competing objectives* that cannot be simultaneously optimized in the integral setting.

### Mistake 2: Assuming Integrality = Fractional for Directed Graphs

A common misconception is that directed and undirected graphs should have similar flow-cut gaps. In fact, dir