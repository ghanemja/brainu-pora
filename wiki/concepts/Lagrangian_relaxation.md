# Lagrangian Relaxation

## Definition

**Lagrangian relaxation** is an optimization technique that decomposes a constrained optimization problem by relaxing (removing) complicating constraints and incorporating them into the objective function via dual variables (Lagrange multipliers). This transforms a difficult primal problem into a series of easier subproblems whose solutions provide bounds and insight into the original problem.

For a primal problem:
$$\min_x f(x) \quad \text{s.t.} \quad g(x) \leq 0$$

the Lagrangian relaxation creates a dual problem in the multipliers $\lambda \geq 0$:
$$\mathcal{L}(x, \lambda) = f(x) + \lambda^T g(x)$$

The **dual function** is then:
$$q(\lambda) = \min_x \mathcal{L}(x, \lambda)$$

and the **dual problem** maximizes this lower bound:
$$\max_{\lambda \geq 0} q(\lambda)$$

The source material illustrates this with dual prices $\lambda_l$ converging to optimal values (e.g., $\lambda_l = 160$) that unlock better primal solutions by revealing true shadow prices of resources.

## Key Equations

**Duality Gap:**
$$\text{Gap} = f(x^*) - q(\lambda^*)$$

where $f(x^*)$ is the optimal primal objective and $q(\lambda^*)$ is the optimal dual objective. A gap of zero implies the relaxed solution is optimal for the original problem.

**Frank-Wolfe Dual Update** (as used in the source):
The algorithm iteratively solves the relaxed subproblem for fixed $\lambda$, then updates $\lambda$ via a first-order method. The error metric is:
$$g = \max_l |\lambda_l^{(t+1)} - \lambda_l^{(t)}|$$

Convergence to $g = 0$ with $q(\lambda) = 0.3$ indicates the dual has converged and primal feasibility is achieved.

**Dual-to-Primal Recovery:**
In the transportation/procurement setting:
- Dual variable $\lambda_l$ represents the shadow price (marginal value) of load $l$
- Spot price $p_l = 130$ emerges from the equilibrium condition between contract capacity utilization and spot market dynamics
- Non-procurement probability $q_l(\lambda_l) = 0.3$ encodes market acceptance probability

## Physical Intuition / Derivation

### Why Relax?

Consider a complex constrained problem where constraints couple many variables, making direct optimization intractable. Lagrangian relaxation "breaks" these couplings by penalizing constraint violations with multipliers $\lambda$.

**Key insight:** Rather than enforcing $g(x) \leq 0$ hard, we ask: *"What price $\lambda$ on violating these constraints would make a decision-maker naturally respect them?"*

### The Dual Ascent Interpretation

Start with an infeasible or suboptimal solution. The dual variables $\lambda$ act as **prices** or **shadow prices**:
- If constraint $i$ is violated ($g_i(x) > 0$), increase $\lambda_i$ to penalize violations
- If constraint $i$ is slack ($g_i(x) < 0$), decrease $\lambda_i$ to relax the penalty

The source demonstrates this: dual prices $\lambda_l$ converge via Dual Frank-Wolfe (a subgradient ascent variant), discovering that $\lambda_l = 160$ is the equilibrium price at which loads are optimally allocated between spot markets, contracts, and alternate channels.

### Why It Provides Bounds

$$q(\lambda) = \min_x \mathcal{L}(x, \lambda) \leq \min_x f(x) \quad \forall \lambda \geq 0$$

This is because any feasible $x^*$ satisfies $g(x^*) \leq 0$, so:
$$\mathcal{L}(x^*, \lambda) = f(x^*) + \lambda^T g(x^*) \leq f(x^*)$$

Thus $q(\lambda) \leq f(x^*)$ always, making the dual a **lower bound** on the primal optimum.

## Applications in Engineering

### 1. **Operations Research & Supply Chain**
- **Vehicle routing & scheduling:** Relax demand coupling constraints; dual variables guide fleet allocation
- **Procurement optimization** (as in source): Relax contract/spot-market coupling to decompose load allocation. DFW achieves 30%+ cost savings vs. naive heuristics by discovering optimal dual prices $\lambda_l$
- **Resource allocation:** Relax capacity constraints to price out bottlenecks

### 2. **Power Systems & Energy**
- **Unit commitment:** Relax generator ramping/coupling constraints; dual prices guide economic dispatch
- **Market clearing:** Dual variables represent locational marginal prices (LMP) that equilibrate supply and demand

### 3. **Network Optimization**
- **Minimum cost flow:** Relax capacity constraints; dual variables become edge costs that guide decomposition
- **Telecommunications:** Routing & bandwidth allocation under capacity constraints

### 4. **Machine Learning & Optimization**
- **Distributed learning:** Consensus problems relax averaging constraints to enable decentralized training
- **Constraint generation:** Iteratively add violated constraints; dual variables guide which constraints matter most

## Common Mistakes / Pitfalls

### 1. **Confusing Optimality with Feasibility**
A dual solution $\lambda^*$ **maximizes a lower bound**; it does not guarantee the primal solution is feasible or optimal. You must solve the primal subproblem and check feasibility separately.

*Source example:* The algorithm found $q(\lambda_l) = 0.3$ (dual objective) but still had to recover the primal solution with spot prices $p_l = 130$.

### 2. **Incorrect Relaxation Selection**
Relaxing the "wrong" constraints can yield a dual problem that is still hard to solve or provides a very loose bound. Choose constraints that:
- Couple variables (create integrality or coupling structure)
- Are expensive to enforce