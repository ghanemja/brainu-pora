# 2-approximation algorithm

## Definition

A **2-approximation algorithm** is a polynomial-time algorithm that solves an optimization problem and produces a solution with cost at most **twice** the optimal cost (for minimization problems) or at least **half** the optimal value (for maximization problems).

Formally, for a minimization problem with optimal value $\text{OPT}$, an algorithm $\mathcal{A}$ is a 2-approximation if:

$$\text{cost}(\mathcal{A}(I)) \leq 2 \cdot \text{OPT}(I)$$

for every instance $I$.

The factor 2 is the **approximation ratio** or **approximation factor**. More generally, a $\rho$-approximation algorithm satisfies $\text{cost}(\mathcal{A}) \leq \rho \cdot \text{OPT}$ for some constant $\rho > 1$.

## Key Equations

**Approximation ratio definition:**
$$\rho = \frac{\text{cost(computed solution)}}{\text{OPT}}$$

**For minimization problems:**
$$\text{ALG}(I) \leq \rho \cdot \text{OPT}(I) \quad \forall \text{ instances } I$$

**Greedy k-center approximation bound:**
If $\hat{c}_i(j)$ is the cost of the greedy k-center solution with $j$ centers on point set $P_i$, and $c^*_i(j)$ is the optimal cost:
$$\hat{c}_i(j) \leq 2 \cdot c^*_i(j) \quad \forall i, j$$

## Physical Intuition / Derivation

### Why 2-approximations matter

Many important optimization problems (e.g., k-center, vertex cover, Steiner tree) are NP-hard, making exact algorithms computationally infeasible for large instances. A 2-approximation offers a practical guarantee: **the algorithm is provably no worse than twice the optimal solution**, while running in polynomial time.

### The k-center example (Gonzalez 1985)

The greedy k-center algorithm illustrates how 2-approximations work:

1. **Start** with an arbitrary point as the first center
2. **Iterate**: At each step $j \leq k$, choose the point farthest from all previously selected centers
3. **Result**: The maximum distance from any point to its nearest center is at most twice the optimal maximum distance

**Why does this work?** Suppose the greedy algorithm produces maximum radius $r_{\text{greedy}}$, and the optimal solution has radius $r^*$. When the greedy algorithm selects its $(k+1)$-th point as farthest from the first $k$ centers, that point must be at distance $> r_{\text{greedy}}$ from all $k$ centers. But the optimal solution uses only $k$ centers, so at least two of the greedy centers must be served by a single optimal center—which is impossible if $r_{\text{greedy}} > 2r^*$. Thus $r_{\text{greedy}} \leq 2r^*$.

### Lagrangian duality perspective

In problems like interdiction, 2-approximations arise naturally through Lagrangian relaxation. When you dualize a constraint with multiplier $\lambda^*$ (the optimal Lagrange multiplier), any strict 2-approximate minimizer of the reweighted problem provides a witness to the optimal solution of the original problem. This connects approximation quality to duality gaps.

## Applications in Engineering

### 1. **Facility Location and Clustering**
- **k-center problem**: Place $k$ service facilities to minimize the maximum distance any demand must travel. The 2-approximation greedy algorithm is widely used in logistics, hospital placement, and network coverage planning.
- **Best Representatives problem**: Allocating cluster centers across multiple datasets simultaneously (e.g., medical imaging where you must maintain representatives for multiple patient cohorts within a budget).

### 2. **Vertex Cover** 
- **Problem**: Find a minimum set of vertices such that every edge has at least one endpoint in the set.
- **2-approximation**: Greedily select edges, adding both endpoints to the cover until all edges are covered. Guarantees a solution at most twice the optimal.
- **Applications**: Network design, circuit testing, and conflict resolution in distributed systems.

### 3. **Interdiction and Robustness**
- In network optimization under adversarial deletion (e.g., protecting power grids or communication networks), the duality-based 2-approximation framework allows exact algorithms by:
  - Computing optimal reweighted solutions via truncated costs
  - Enumerating 2-approximate minimizers
  - Solving the residual knapsack problem for the adversary's budget
- This approach is computationally tractable when exact interdiction is otherwise intractable.

### 4. **Metric Facility Design**
- **Spanning tree approximations**: Find a low-cost spanning tree with balanced connectivity properties.
- **Learning-augmented variants**: Use machine-learning predictions to improve on the 2-approximation baseline (e.g., better spanning tree algorithms via metric forest completion).

### 5. **Resource Allocation Under Uncertainty**
- Dynamic programming combined with 2-approximations (as in BESTREPS) allocates shared budgets across multiple instances while maintaining approximation guarantees.
- Applications: cloud resource provisioning, hospital staffing across multiple units.

## Worked Example: Vertex Cover for Network Security

**Scenario:** You manage a network of 8 switches. Each link connects two switches. An attacker can exploit any unprotected link if both endpoints are unprotected. You can install security firmware on switches (expensive) to protect all incident links.

**Network topology:**
```
Switches: 0, 1, 2, 3, 4, 5, 6, 7
Links: (0,1), (1,2), (2,3), (0,4), (4,5), (5,6), (6,7), (3,7), (2,4)
```
**Exact solution** (minimum vertex cover): Select switches {1, 2, 4, 6, 7} = 5 switches. Every link has at least one protected endpoint.

**Greedy 2-approximation (poly-time):**
1. While edges remain:
   - Pick an uncovered edge (u, v)
   - Add both u and v to cover
   - Remove all edges incident to u or v
2. Result: Selects pairs greedily → might select {0,1}, {2,3}, {4,5}, {6,7} = 8 switches (worst case)

**Guarantee:** Your greedy solution uses ≤ 2× the optimal switches, so you're safe in polynomial time.

**Real-world trade-off:** Optimal ≈ 5 switches (requires exponential search), greedy ≈ 8 switches (linear time). Protecting 3 extra switches is acceptable if exact solution takes days to compute.

## Common Mistakes / Pitfalls

### 1. **Confusing approximation ratio with error percentage**
- A 2-approximation does **not** mean 100% error. It means the cost is within a factor of 2, which could be 50% worse, or could be optimal.
- $\rho = 1.5$ means at most 50% worse; $\rho = 2$ means at most 100% worse.

### 2. **Assuming 2-approximation is "good enough"**
- In practice, a 2-approximation may be unacceptable if:
  - The problem domain requires guarantees closer to optimal (e.g., financial trading)
  - The constant factors hidden in $O(\cdot)$ complexity are large
  - Many instances admit much better approximations