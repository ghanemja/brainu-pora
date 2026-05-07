# Minimum-cost flow

## Definition

The **minimum-cost flow problem** is a fundamental optimization problem on directed graphs that simultaneously optimizes two objectives:

1. **Flow conservation**: Route a specified amount of flow from source to sink nodes
2. **Cost minimization**: Minimize the total cost of routing that flow

Formally, given:
- A directed graph $G = (V, E)$ with $n$ vertices and $m$ edges
- Edge capacities $c_e \geq 0$ for each edge $e \in E$
- Edge costs (weights) $w_e \in \mathbb{R}$ for each edge $e$
- Supply/demand values $b_v \in \mathbb{R}$ at each vertex $v$ (where $\sum_v b_v = 0$ for feasibility)

Find a flow $f: E \to \mathbb{R}_{\geq 0}$ that:

$$\text{minimize} \quad \sum_{e \in E} w_e \cdot f_e$$

Subject to flow conservation constraints:
$$\sum_{e \in \delta^{\text{out}}(v)} f_e - \sum_{e \in \delta^{\text{in}}(v)} f_e = b_v \quad \forall v \in V$$

And capacity constraints:
$$0 \leq f_e \leq c_e \quad \forall e \in E$$

where $\delta^{\text{out}}(v)$ and $\delta^{\text{in}}(v)$ denote outgoing and incoming edges at vertex $v$.

## Key Equations

**Cost of a flow:**
$$\text{Cost}(f) = \sum_{e \in E} w_e \cdot f_e$$

**Flow conservation at vertex $v$:**
$$\text{inflow}(v) - \text{outflow}(v) = b_v$$

**Residual capacity of edge $e$ with flow $f_e$:**
$$c_e^{\text{residual}} = c_e - f_e$$

**Reduced cost (for dual methods with potential $\pi: V \to \mathbb{R}$):**
$$\bar{w}_e(u,v) = w_e + \pi_u - \pi_v$$

## Physical Intuition / Derivation

### Why both objectives matter

Consider distributing resources (electricity, data packets, goods) through a network. A naive solution ignores cost and simply routes flow; an optimal solution balances routing *sufficiently* to meet demand *while keeping total expense minimal*.

### Connection to shortest paths

When each edge has unit capacity and we demand unit flow from one source to one sink, minimum-cost flow reduces to the **single-source shortest path problem**. This is why breakthrough algorithms for shortest paths (like the $n^{2+o(1)}$ Bellman-Ford improvement cited in the source material) directly improve minimum-cost flow solvers.

### Successive shortest paths method

A classic algorithmic approach builds on shortest paths:

1. While unsatisfied demand remains:
   - Compute shortest path from supply node to demand node using current edge costs
   - Send maximum feasible flow along this path (limited by edge capacities and remaining demand)
   - Update residual graph and edge costs

The number of iterations equals the number of flow augmentations; each iteration runs a shortest-path algorithm. **This explains why faster shortest-path algorithms directly yield faster minimum-cost flow algorithms.**

### Dual perspective: potentials and reduced costs

The dual problem assigns vertex potentials $\pi_v$ to satisfy:
$$w_e + \pi_u - \pi_v \geq 0 \quad \text{for edges }(u,v) \text{ with zero reduced cost}$$

At optimality, flow only travels on edges with zero reduced cost—these form a shortest-path DAG. This is the foundation for **cost-scaling algorithms** and explains the role of potentials in modern solvers.

## Applications in Engineering

### Power grid operations
Minimize fuel costs while meeting regional electricity demand; edges represent transmission lines with capacities, costs reflect generation prices.

### Transportation and logistics
Route vehicles through networks minimizing fuel/labor costs while meeting delivery requirements. Vertices are distribution centers, edge costs include distance and congestion penalties.

### Telecommunications
Route data packets through networks minimizing bandwidth costs (or delay) while delivering all traffic. Real-time formulations must solve this repeatedly.

### Supply chain optimization
Find minimum-cost ways to move raw materials and products through multi-stage manufacturing and distribution networks with capacity constraints.

### Air traffic management
Schedule aircraft along flight paths minimizing fuel while respecting airport capacity and airspace constraints.

### Water resource management
Allocate water through canal and pipeline networks, minimizing pumping costs while meeting irrigation and municipal demand.

## Common Mistakes / Pitfalls

1. **Forgetting flow conservation:** Beginners write only capacity constraints and forget that flow in must equal flow out at every intermediate node.

2. **Confusing with single-source shortest paths:** Not all minimum-cost flow problems are shortest-path problems—shortest paths have special structure (unit demand, unit capacities, no supplies elsewhere).

3. **Assuming integer solutions exist:** Even with integer capacities and integer costs, fractional flows may be required for optimality. (However, if all data is integer and a feasible solution exists, there exists an optimal *integer* solution—a useful property for some applications.)

4. **Ignoring negative cycles:** Algorithms must detect and handle negative cycles. An optimal solution exists if and only if the residual graph contains no negative cycles.

5. **Misunderstanding "cost":** The edge weight $w_e$ need not be distance or time; it can be any marginal cost of routing one unit on that edge. Confusing units (cost per unit vs. total cost) is common.

6. **Scaling pitfall in successive shortest paths:** If demands are very large, the number of augmentation iterations can be prohibitive. **Capacity scaling** (routing larger quantities per iteration) is essential for large flows.

## See Also

- [[Single-source shortest paths]] — the special case that reduced the bottleneck in general minimum-cost flow
- [[Successive shortest paths algorithm]] — classical augmentation-based approach
- [[Cost scaling algorithm]] — dual-based polynomial-time approach
- [[Bellman-Ford algorithm]] — handles negative weights, key subroutine for integer weight MCF
- [[Max flow min cost theorem]] —