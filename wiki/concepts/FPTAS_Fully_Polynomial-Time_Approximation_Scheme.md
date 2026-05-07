# FPTAS (Fully Polynomial-Time Approximation Scheme)

## Definition

A **Fully Polynomial-Time Approximation Scheme (FPTAS)** is a randomized or deterministic algorithm that, for any optimization problem instance and any error tolerance $\epsilon > 0$, produces a solution with value within a factor of $(1 + \epsilon)$ of the optimum in time polynomial in both the input size $n$ and $1/\epsilon$.

Formally, an FPTAS for a minimization problem is an algorithm $\mathcal{A}(\epsilon)$ such that:

$$\text{cost}(\mathcal{A}(\epsilon)) \leq (1 + \epsilon) \cdot \text{OPT}$$

with runtime bounded by $\text{poly}(n, 1/\epsilon)$.

**Contrast with PTAS:** A polynomial-time approximation scheme (PTAS) runs in time $\text{poly}(n) \cdot f(1/\epsilon)$ where $f$ can be arbitrary (e.g., exponential in $1/\epsilon$). An FPTAS additionally requires the dependence on $\epsilon$ to be polynomial.

---

## Key Equations

### Approximation Guarantee

For a minimization problem with optimal value $\text{OPT}$:

$$\text{cost}(\text{FPTAS}) \leq (1 + \epsilon) \cdot \text{OPT} \quad \forall \epsilon > 0$$

### Runtime Complexity

$$T(\mathcal{A}) = \text{poly}\left(n, \log \frac{1}{\epsilon}\right) \quad \text{or} \quad T(\mathcal{A}) = O(n^c / \epsilon^d)$$

where $c, d$ are constants independent of $\epsilon$.

### Lagrangian Relaxation Framework

For interdiction problems with linear objectives $w(S) = \sum_{e \in S} w(e)$ and interdiction budget constraints, truncated weights at Lagrange multiplier $\lambda$ are:

$$w_\lambda(e) = \min\{w(e), \lambda c(e)\}$$

At optimal $\lambda^*$, the witness is a **strict $\alpha$-approximate minimizer** of the reweighted problem, enabling enumeration strategies.

---

## Physical Intuition / Derivation

### Why FPTAS is Stronger Than PTAS

Consider the decision tree problem or separating subfamily problem. Naive approximation might achieve constant factor $(1 + c)$ for fixed $c$, but guaranteeing $(1 + \epsilon)$ for *arbitrary small* $\epsilon$ is harder:

- **PTAS:** Allows exponential blow-up in $1/\epsilon$ (e.g., $2^{1/\epsilon}$ time). Practical only for moderate error tolerance.
- **FPTAS:** Polynomial dependence on $1/\epsilon$ means you can afford very small errors while maintaining tractability. This is rare and valuable.

### Constructive Approach: Rounding + Enumeration

Many FPTAS constructions follow this pattern:

1. **Discretize** the problem by scaling and rounding weights (reducing the number of distinct values to $O(n/\epsilon)$)
2. **Solve exactly** on the rounded instance using pseudo-polynomial DP
3. **Map back** to original instance with controlled error loss

**Example:** For the Knapsack problem, scale weights by factor $\epsilon/n$, round, and use standard DP on the reduced state space: $O(n^2/\epsilon)$ time.

### Lagrangian Duality for Interdiction

Given a feasible set family $\mathcal{F}$ and linear objective, dualization of the interdiction budget constraint allows reweighting:

$$w_\lambda(e) = \min\{w(e), \lambda c(e)\}$$

At the optimal dual solution $\lambda^*$, any **2-approximate minimizer** of the reweighted problem is provably close to the true interdiction optimum. This reduces the search space from all sets to a sparse enumeration of 2-approximate solutions, making exact algorithms tractable.

---

## Applications in Engineering

### 1. **Scheduling & Resource Allocation**
- Assigning tasks to machines with minimizing makespan or weighted completion time
- FPTAS known for many variants (parallel machines with release dates, etc.)
- Enable precise trade-offs between solution quality and computational budget

### 2. **Network Design & Interdiction**
- Finding minimum-cost edge sets to separate connectivity in a graph (motivated by the source material)
- Adversarial problems: resilient routing, critical infrastructure protection
- Budget-constrained deletion problems benefit from tight approximations

### 3. **Knapsack & Packing Problems**
- 0/1 Knapsack: Classic FPTAS via DP with scaling
- Multi-dimensional variants: approximation for capacitated vehicle routing
- Fundamental in operations research and supply chain optimization

### 4. **Subset Selection under Constraints**
- Separating subfamily problem: select minimum-cost subsets to separate all pairs in a partition
- Maximum coverage: achieving $(1 - 1/e)$ approximation with budget guessing
- Machine learning: feature selection, submodular optimization with cardinality/budget constraints

### 5. **Combinatorial Optimization**
- Traveling Salesman Problem (TSP): FPTAS known for Euclidean TSP in fixed dimensions
- Tree/forest design: minimum spanning tree variants with additional constraints
- Portfolio optimization: balancing return and risk with discrete decisions

---

## Common Mistakes / Pitfalls

### 1. **Confusing FPTAS with PTAS**
Students often treat PTAS as equivalent to FPTAS. The key difference is the polynomial dependence on $1/\epsilon$. A PTAS with $O(2^{1/\epsilon} \cdot n^2)$ runtime is useless for $\epsilon = 0.01$ (making $2^{100}$ blowup).

### 2. **Assuming All NP-hard Problems Admit FPTAS**
FPTAS are rare. Many NP-hard problems have no known FPTAS and are suspected not to admit one under standard complexity assumptions. Examples: