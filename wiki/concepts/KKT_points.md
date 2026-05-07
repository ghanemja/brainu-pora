# KKT Points

## Definition

A **KKT point** (Karush-Kuhn-Tucker point) is a candidate solution to a constrained optimization problem that satisfies the first-order necessary conditions for local optimality. More formally, given the constrained optimization problem:

$$\begin{align}
\min_{x} \quad & f(x) \\
\text{s.t.} \quad & g_i(x) \leq 0, \quad i = 1, \ldots, m \\
& h_j(x) = 0, \quad j = 1, \ldots, p
\end{align}$$

a point $x^* \in \mathbb{R}^n$ is a **KKT point** if there exist multipliers $\lambda^* \in \mathbb{R}^m$ and $\mu^* \in \mathbb{R}^p$ such that the following conditions hold:

1. **Stationarity**: $\nabla f(x^*) + \sum_{i=1}^{m} \lambda_i^* \nabla g_i(x^*) + \sum_{j=1}^{p} \mu_j^* \nabla h_j(x^*) = 0$

2. **Primal feasibility**: $g_i(x^*) \leq 0$ for all $i$; $h_j(x^*) = 0$ for all $j$

3. **Dual feasibility**: $\lambda_i^* \geq 0$ for all $i$

4. **Complementary slackness**: $\lambda_i^* g_i(x^*) = 0$ for all $i$

Under constraint qualification conditions (e.g., LICQ—Linear Independence Constraint Qualification), any local minimum must be a KKT point.

## Key Equations

The **Lagrangian** function is central to KKT theory:

$$L(x, \lambda, \mu) = f(x) + \sum_{i=1}^{m} \lambda_i g_i(x) + \sum_{j=1}^{p} \mu_j h_j(x)$$

The **stationarity condition** can equivalently be written as:

$$\nabla_x L(x^*, \lambda^*, \mu^*) = 0$$

The **complementary slackness** condition encodes the intuition that inactive inequality constraints have zero multiplier:

$$\lambda_i^* g_i(x^*) = 0 \quad \Rightarrow \quad \lambda_i^* > 0 \text{ only if } g_i(x^*) = 0$$

## Physical Intuition / Derivation

### Why KKT Points Matter

At a minimum of an unconstrained problem, the gradient is zero: $\nabla f(x^*) = 0$. In the constrained case, the objective gradient may not be zero at the minimum; instead, it must be balanced by the gradients of active constraints.

**Intuition**: Imagine minimizing $f(x)$ on a surface defined by active constraints. The objective's "pull" (gradient) must be countered by the constraints' "reaction forces" (weighted by multipliers $\lambda_i^*$). If you could move in a feasible direction, the objective would not improve—this is formalized by stationarity.

### Derivation via Lagrangian

The Lagrangian merges the objective and constraints:

$$L(x, \lambda, \mu) = f(x) + \sum_{i=1}^{m} \lambda_i g_i(x) + \sum_{j=1}^{p} \mu_j h_j(x)$$

At a local minimum $x^*$:
- The gradient with respect to $x$ must vanish: $\nabla_x L = 0$ (stationarity)
- We recover primal feasibility by requiring $g_i(x) \leq 0$ and $h_j(x) = 0$
- Dual feasibility ($\lambda_i \geq 0$) ensures the multipliers are consistent with inequality constraints being "inactive" (slack) or active
- Complementary slackness ensures that only active constraints have nonzero multipliers

### Connection to Convex Optimization

For **convex problems** (where $f$, $g_i$ are convex and $h_j$ are affine), KKT conditions are **sufficient** for global optimality. For non-convex problems, KKT points are only necessary local optimality conditions; multiple KKT points may exist, and some may be saddle points.

## Applications in Engineering

### 1. **Control Systems & Optimal Control**
KKT conditions underpin model predictive control (MPC) and trajectory optimization. Engineers solve constrained optimal control problems (minimize energy subject to state/actuator constraints) and use KKT multipliers to understand the "cost" of constraint tightening.

### 2. **Machine Learning & Convex Optimization**
Support Vector Machines (SVMs) are formulated as convex quadratic programs whose solutions satisfy KKT conditions. The dual problem derivation via Lagrangian is essential for kernel methods.

### 3. **Power Systems & Operations Research**
Optimal power flow (OPF) problems minimize generation cost subject to AC power flow equations and transmission limits. KKT conditions are used to analyze locational marginal prices (shadow prices on constraints).

### 4. **Structural & Mechanical Design**
Topology optimization and shape optimization problems constrain weight or volume while minimizing compliance. KKT analysis reveals which design constraints are active and their sensitivity to relaxation.

### 5. **Economics & Resource Allocation**
Welfare maximization, portfolio optimization, and mechanism design problems all reduce to constrained optimization where KKT multipliers represent equilibrium prices or Lagrange multipliers of scarcity.

## Common Mistakes / Pitfalls

### Mistake 1: Confusing KKT Points with Optima
**Error**: "I found a KKT point, so I found the global optimum."

**Reality**: KKT points are necessary but not sufficient for optimality in non-convex problems. They may be saddle points or local minima. For non-convex problems, you must check