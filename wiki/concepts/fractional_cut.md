# Fractional Cut

## Definition

A **fractional cut** is a relaxation of the classical integral multicut problem in graph theory. For a directed graph $G = (V, E)$ with a set of demand pairs $P \subseteq V \times V$, a fractional cut assigns non-negative real weights $w_e \in [0, 1]$ to each edge $e \in E$ such that for every demand pair $(s_i, t_i) \in P$, the total weight along any path from $s_i$ to $t_i$ is at least 1.

Formally, a fractional cut must satisfy:
$$\sum_{e \in \text{path}(s_i, t_i)} w_e \geq 1 \quad \forall (s_i, t_i) \in P$$

The **cost** or **weight** of a fractional cut is:
$$\text{FCut}(G, P) = \min \sum_{e \in E} c_e \cdot w_e$$

where $c_e$ denotes the capacity of edge $e$.

## Key Equations

**Flow-Cut Gap (undirected):**
$$\text{Gap}_{\text{undi}} = \frac{\min(\text{integral multicut})}{\max(\text{multiflow})} = \Theta(\log n)$$

**Flow-Cut Gap (directed):**
$$\text{Gap}_{\text{dir}} \leq n^{1/3 + o(1)}$$

**Parametrized by sum of fractional cuts:**
$$\text{Gap}(W) \leq W^{1/2}n^{o(1)}$$

where $W = \min \text{(sum of fractional cut weights)}$.

**LP Duality (fundamental relationship):**
$$\max(\text{multiflow}) = \min(\text{fractional multicut})$$

## Physical Intuition / Derivation

### Why Fractional Relaxation?

The classical **integral multicut** problem requires edges to be either fully assigned to cut a pair (weight = 1) or not (weight = 0). This is computationally intractable for multiple demand pairs. The fractional relaxation allows edges to be "partially cut," which makes the problem linear (solvable in polynomial time via LP) while providing a lower bound for the integral solution.

### The Gap Phenomenon

A critical insight from Figure 1 in the source material illustrates why the gap exists:

- **Integral solution:** Must completely remove edges, so the minimum cost is 2 (removing one edge blocks multiple pairs but is wasteful)
- **Fractional solution:** Can assign weight $1/2$ to edges, distributing the "cutting load" across multiple edges to achieve cost $3/2$

This mismatch arises because integral solutions are "brittle"—they cannot distribute work flexibly. The fractional relaxation is always ≤ integral optimum, and the ratio between them is the flow-cut gap.

### Why Directed Graphs Are Harder

Undirected graphs benefit from geometric structure (embeddings with logarithmic distortion). Directed graphs lack this structure, making tight bounds elusive. Current understanding:
- **Lower bound:** $\Omega(n^{1/7})$ (Chuzhoy & Khanna)
- **Upper bound:** $O(n^{1/3 + o(1)})$ (Bodwin & Samborska, 2026)

The gap between these bounds remains substantial, indicating the problem's inherent difficulty.

## Applications in Engineering

### Network Design & Routing
- **Capacity planning:** Fractional cuts provide polynomial-time lower bounds for minimum capacity needed to support multi-commodity flows
- **Load balancing:** Distributing traffic fractionally guides integral routing algorithms

### Telecommunications
- **Multi-hop routing:** Fractional solutions help determine minimal shared infrastructure (fibers, wavelengths) needed for multiple point-to-point connections
- **Fault tolerance:** Fractional cuts model partial redundancy and weighted failure modes

### Optimization & Approximation Algorithms
- **Rounding techniques:** Fractional cuts serve as relaxations; randomized/deterministic rounding converts fractional solutions to feasible integral ones with bounded loss
- **Approximation guarantees:** The flow-cut gap directly bounds approximation ratios for multicut problems

### Distributed Systems
- **Bottleneck identification:** Fractional analysis identifies critical resources in communication networks without discrete constraints

## Common Mistakes / Pitfalls

1. **Confusing the constraint direction:** A fractional cut assigns weights to *edges*, not paths. Students often invert the problem by assigning weights to (source, sink) pairs.

2. **Neglecting integrality gap:** The fractional cut is always ≤ integral optimum. If your fractional solution is "better than expected," you likely have an infeasible fractional cut (e.g., paths not properly constrained to have total weight ≥ 1).

3. **Assuming fractional = trivial:** While solvable in polynomial time, computing the exact optimal fractional cut still requires solving a large LP. For large instances, numerical stability matters.

4. **Treating directed and undirected gaps as equivalent:** The $\Theta(\log n)$ bound for undirected graphs does **not** transfer to directed graphs. The directed gap remains largely open.

5. **Misinterpreting parametrization by $W$:** The bound $W^{1/2}n^{o(1)}$ means the gap depends on the minimum weight of fractional cuts—sparse instances with small $W$ have better gaps than dense ones.

## See Also

- [[Min-Cut Max-Flow Theorem]]
- [[Multicut Problem]]
- [[Multiflow]]
- [[LP Relaxation and Rounding]]
- [[Flow-Cut Gap]]
- [[Integral Multicut]]

## Sources

- Bodwin, G., & Samborska, L. (2026). "Improved Upper Bounds for the Directed Flow-Cut Gap." *arXiv preprint arXiv:2604.03412v2*
- Leighton, T., & Rao, S. (1989). "An Approximate Max-Flow Min-Cut Theorem for Uniform Multicommodity Flow Problems with Applications to Approximation Algorithms." *FOCS*
- Chuzhoy, J., &