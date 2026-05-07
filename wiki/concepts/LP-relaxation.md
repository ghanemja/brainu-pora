# LP-relaxation

## Definition

An **LP-relaxation** is a linear programming (LP) formulation derived from a combinatorial optimization problem by relaxing (weakening) its constraints or feasible region. Specifically, it replaces discrete or non-linear constraints with continuous linear inequalities, allowing real-valued (not just integer) variables.

Formally, given a combinatorial optimization problem:
$$\text{maximize/minimize } c^T x$$
$$\text{subject to } x \in \mathcal{S}$$

where $\mathcal{S}$ is a discrete feasible set (e.g., the set of all valid colorings of a matroid intersection), the LP-relaxation replaces $\mathcal{S}$ with a convex polytope $\mathcal{P}$ such that $\mathcal{S} \subseteq \mathcal{P}$:

$$\text{maximize/minimize } c^T x$$
$$\text{subject to } Ax \leq b$$
$$x \in \mathbb{R}^n$$

The optimal value of the LP-relaxation provides a bound (upper bound for maximization, lower bound for minimization) on the optimal value of the original integer problem.

## Key Equations

**Relaxation relationship:**
$$\text{OPT}_{\text{LP}} \geq \text{OPT}_{\text{integer}}$$
(for maximization problems)

**Integrality gap:**
$$\text{gap} = \frac{\text{OPT}_{\text{integer}}}{\text{OPT}_{\text{LP}}}$$

The integrality gap quantifies how much the relaxation "overestimates" the true optimum. A gap of 1 means the LP solution is integral (no relaxation needed).

**In matroid-intersection coloring** (from source context):
The LP-relaxation encodes a fractional coloring where element selections are continuous variables $x_e \in [0,1]$ per color class, subject to matroid rank constraints:
$$\sum_{e \in S} x_e \leq r_M(S) \quad \forall S \subseteq U$$

where $r_M(S)$ is the matroid rank function.

## Physical Intuition / Derivation

### Why Relax?

Combinatorial problems (integer programming) are NP-hard. The LP-relaxation is polynomial-time solvable using algorithms like the simplex method or interior-point methods. However, this speed comes at a price: the relaxation may overestimate the optimum.

### The Trade-off

1. **Exact problem**: Discrete, hard to solve, but optimal
2. **Relaxation**: Continuous, easy to solve, provides a bound
3. **Rounding**: Convert fractional LP solution back to discrete solution, incurring approximation loss

### Derivation by Example (Matroid Coloring)

**Original problem** (discrete):
- Assign elements of a matroid to color classes such that each color class is an independent set
- Minimize number of colors used (chromatic number $\chi$)

**LP-relaxation**:
- Allow fractional allocation: variable $x_{e,i} \in [0,1]$ represents fraction of element $e$ assigned to color $i$
- Constraints: $\sum_i x_{e,i} = 1$ (each element fully allocated), and $\sum_{e \in S} x_{e,i} \leq r_M(S)$ for all $S$ and colors $i$ (respect matroid independence)
- Minimize $\sum_i y_i$ where $y_i = 1$ if any fraction assigned to color $i$

The LP solution provides a lower bound on true $\chi$. An LP-rounding algorithm (e.g., randomized or greedy) then converts the fractional solution into an integer one.

## Applications in Engineering

### 1. **Combinatorial Optimization & Approximation Algorithms**
   - **Resource scheduling**: LP-relaxations bound optimal makespan or cost in job scheduling, vehicle routing
   - **Network design**: LP-relaxation of minimum spanning tree, Steiner tree problems yields bounds tighter than greedy alone
   
### 2. **Matroid Optimization** (primary context)
   - **Matroid intersection coloring**: As noted in source, LP-relaxation + rounding achieves $O(1)$-approximation for $k$-matroid coloring, improving upon $O(k \log n)$ combinatorial methods
   - **Basis selection**: Rota's Basis Conjecture verified algorithmically via LP-relaxation (Theorem 5)

### 3. **Machine Learning & Statistical Learning**
   - **Structured prediction**: LP-relaxations of integer quadratic programs in inference
   - **Clustering and assignment**: Relaxing discrete cluster assignments to continuous probabilities

### 4. **Electrical Engineering & Power Systems**
   - **Optimal power flow**: AC power flow is non-convex; LP/SDP relaxations provide feasible solutions with bounded sub-optimality
   - **Unit commitment**: Binary on/off decisions for generators relaxed to continuous dispatch

### 5. **Operations Research**
   - **Integer programming solvers**: LP-relaxations are bounds in branch-and-bound algorithms
   - **Facility location, facility assignment**: Fractional relaxations guide rounding heuristics

## Common Mistakes / Pitfalls

1. **Assuming LP optimality equals problem optimality**: The LP-relaxation is *weaker*; its solution may be infeasible for the original problem. Rounding is mandatory.

2. **Ignoring the integrality gap**: A good LP bound does not guarantee a good approximation ratio after rounding. For some problems, the gap can be large (e.g., $\Omega(\log n)$ for set cover).

3. **Confusing direction of bounds**: For a maximization problem, $\text{OPT}_{\text{LP}} \geq \text{OPT}_{\text{int}}$, so LP gives an *upper* bound on what's achievable. Rounding yields a *lower* bound on the integer optimum.

4. **Treating all relaxations equally**: The *type* of relaxation matters:
   - **Linear relaxation** (continuous variables): often loose
   - **Semidefin