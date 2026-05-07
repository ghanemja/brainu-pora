# directed graphs

## Definition

A **directed graph** (or **digraph**) $G = (V, E)$ consists of:
- A finite set of **vertices** (nodes) $V$
- A set of **directed edges** $E \subseteq V \times V$, where each edge $(u, v)$ is an ordered pair indicating direction from $u$ to $v$

In a **weighted directed graph**, each edge carries an associated weight or capacity $c(e) \in \mathbb{R}^+$.

A **directed path** from $s$ to $t$ is a sequence of vertices $s = v_0, v_1, \ldots, v_k = t$ where $(v_i, v_{i+1}) \in E$ for all $i$.

A **directed acyclic graph (DAG)** is a directed graph containing no directed cycles.

### Flow-Cut Framework

In the context of flow problems on directed graphs:
- A **multicut** is a set of edges whose removal disconnects all pairs in a demand set $P \subseteq V \times V$
- A **multiflow** is a set of feasible flows routing demand between pairs in $P$
- The **flow-cut gap** is the maximum ratio between the minimum integral multicut capacity and the maximum multiflow value across all instances

$$\text{Flow-Cut Gap} = \sup_{G, P, c} \frac{\text{MinCut}(G, P, c)}{\text{MaxFlow}(G, P, c)}$$

## Key Equations

### Min-Cut Max-Flow Theorem (Single Pair)
For a directed graph with source $s$, sink $t$, and edge capacities $c(e)$:

$$\max_{\text{flow } f} \sum_{e \text{ out of } s} f(e) = \min_{\text{cut } S} \sum_{e: S \to \bar{S}} c(e)$$

This equality holds when we allow **fractional flows** (LP relaxation).

### Flow-Cut Gap Bounds
Current best-known bounds for $n$-node directed graphs:

$$\text{Gap} \leq n^{1/3 + o(1)} \quad \text{(upper bound, Bodwin–Samborska)}$$

$$\text{Gap} \geq \Omega(n^{1/7}) \quad \text{(lower bound, Chuzhoy–Khanna)}$$

For fractional multicut problems parametrized by $W$ (sum of minimum fractional cut weights):

$$\text{Gap} \leq W^{1/2} n^{o(1)}$$

### Contrast with Undirected Graphs
For undirected graphs:

$$\text{Gap} = \Theta(\log n) \quad \text{(Leighton–Rao)}$$

The **polynomial gap** in directed graphs vs. **logarithmic gap** in undirected graphs represents a fundamental difference in graph structure.

## Physical Intuition / Derivation

### Why the Gap Exists

The Min-Cut Max-Flow theorem guarantees equality for **fractional solutions** (where flow can be split arbitrarily among paths). However, in many practical applications, we need **integral solutions** where each unit of flow must follow a single path.

**Example (Figure 1 from source):**
- Consider a directed graph with three sources $\{s_1, s_2, s_3\}$ and three sinks $\{t_1, t_2, t_3\}$
- Each demand pair $(s_i, t_i)$ requires routing 1 unit of flow
- The **fractional multicut** can separate demands with total capacity $3/2$ (using 1/2 on each edge)
- The **integral multicut** requires removing entire edges, needing capacity at least $2$
- This creates a gap of $2/(3/2) = 4/3$

### Why Directed Graphs Are Harder

1. **Asymmetry**: In undirected graphs, removing an edge breaks connectivity in both directions. In directed graphs, you must carefully account for directionality.

2. **Demand Routing Flexibility**: Fractional flows can route demands through many paths simultaneously. Integral flows must commit fully to discrete paths, creating inefficiencies when paths interfere.

3. **Reduction to Vertex Cuts**: The source paper proves that vertex-based and edge-based flow-cut gaps are nearly equivalent in directed graphs, expanding the problem complexity.

## Applications in Engineering

### Network Flow Optimization
- **Telecommunication routing**: Finding minimum-cost edge sets to remove for network segmentation (directed graph of routers)
- **Data center networking**: Integral multicut problems arise when migrating workloads (flows must use distinct physical paths)
- **Supply chain logistics**: Directed flow networks model material flow; gap bounds inform bounds on robust routing strategies

### Scheduling and Constraint Systems
- **Job scheduling on DAGs**: Directed acyclic graphs represent task dependencies; flow algorithms solve critical-path problems
- **Fault tolerance**: Computing minimum edge sets whose failure disconnects certain server pairs (integral multicut)

### Algorithm Design
- **Approximation algorithms**: Flow-cut gap bounds directly provide approximation ratios for integral multicut solvers
- **Hardness of approximation**: Lower bounds on the gap provide conditional hardness results for optimization problems

### Graph Algorithms
- **Reachability analysis**: Directed graphs model state transitions; flow techniques compute strongly connected components
- **Compiler optimization**: Control-flow graphs in compilers are directed; dead-code elimination uses minimum cuts

## Common Mistakes / Pitfalls

1. **Confusing directed and undirected gaps**: The $\Theta(\log n)$ bound does not apply to directed graphs; directed gap is polynomial in $n$.

2. **Assuming fractional = integral**: The fundamental difference is that LP relaxations (fractional) can be strictly better than integral solutions in directed graphs.

3. **Ignoring edge direction**: In directed multicut problems, removing edge $(u,v)$ does **not** affect paths using $(v,u)$.

4. **Misapplying MCMF**: The standard Min-Cut Max-Flow theorem applies to single $(s,t)$ pairs. For multiple demand pairs, use **fractional multicut** (which equals maximum multiflow) or study **integral multicut** separately.

5. **