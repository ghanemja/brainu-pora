# Convex Optimization

## Definition

**Convex optimization** is the problem of minimizing a convex objective function over a convex feasible set. Formally:

$$\min_{x \in X} f(x)$$

where:
- $f: \mathbb{R}^n \to \mathbb{R}$ is a **convex function** (i.e., $f(\lambda x + (1-\lambda)y) \leq \lambda f(x) + (1-\lambda)f(y)$ for all $x,y$ and $\lambda \in [0,1]$)
- $X \subseteq \mathbb{R}^n$ is a **convex set** (i.e., if $x, y \in X$, then $\lambda x + (1-\lambda)y \in X$ for all $\lambda \in [0,1]$)

A critical property: **any local minimum is a global minimum**. This distinguishes convex optimization from the much harder nonconvex case.

More generally, convex optimization considers problem classes $C$ of objective functions defined over a feasible region $X$. The structure of $X$ (convex vs. discrete) fundamentally determines computational tractability.

## Key Equations

**Convexity condition for functions:**
$$f(\lambda x + (1-\lambda)y) \leq \lambda f(x) + (1-\lambda)f(y), \quad \forall \lambda \in [0,1]$$

**Convexity condition for sets:**
$$x, y \in X \implies \lambda x + (1-\lambda)y \in X, \quad \forall \lambda \in [0,1]$$

**First-order optimality condition** (for differentiable $f$ over convex $X$):
$$\nabla f(x^*)^T(y - x^*) \geq 0 \quad \forall y \in X$$

At optimality $x^*$, the gradient cannot point into the feasible set in any direction.

**Controllability via linear perturbation:**
Given a convex feasible set $X$, a subset $S \subseteq E$ controls $X$ if for any target solution $x^* \in X$ and any objective function $c \in C$, there exists a linear perturbation $\delta_S$ on coordinates in $S$ such that:
$$x^* = \arg\max_{x \in X} (c + \delta_S)^T x$$

## Physical Intuition / Derivation

### Why Convexity Matters

Imagine you're trying to find the lowest point in a valley. If the terrain is convex (bowl-shaped), any descent algorithm will eventually find the global minimum. If the terrain is nonconvex (has multiple valleys, ridges), you could get stuck in a local valley that isn't the deepest one.

Convex problems are "well-behaved": the absence of local minima that aren't global minima means we can use efficient algorithms like **gradient descent**, **interior point methods**, or **polynomial-time algorithms**.

### Controllability & Identifiability

The source paper reveals a subtle but powerful equivalence: when $X$ is convex, determining whether we can "steer" a system to any desired state via partial controls is equivalent to asking whether those partial observations uniquely identify the full system state.

**Intuition:** In a convex setting, the affine hull of $X$ (the smallest affine subspace containing $X$) has special structure. If we observe coordinates in set $S$, and they uniquely pin down the entire solution, then we can perturb the objective on $S$ to induce any desired feasible solution as optimal.

This is provably *false* in discrete settings (e.g., path problems in graphs), showing that convexity is fundamental to this equivalence.

### Why Convex Hull Relaxations Work

For discrete optimization problems over $X$ (e.g., binary vectors, paths), the convex hull $\text{conv}(X)$ is often much easier to optimize. Solving the relaxation gives bounds and approximate solutions. The gap between discrete $X$ and its convex hull $\text{conv}(X)$ quantifies the "cost of discreteness."

## Applications in Engineering

### Operations Research & Network Control
- **Traffic flow management:** Control subset $S$ of edges with tolls to induce target traffic patterns; works efficiently because flow polyhedra are convex.
- **Supply chain optimization:** Allocate resources (convex constraints: capacity, budget) to minimize costs (convex objective: distance, time).

### Machine Learning & Signal Processing
- **Convex relaxations of rank-minimization:** Nuclear norm minimization relaxes rank constraints; convex but tight approximation to matrix completion.
- **Compressed sensing:** Recover sparse signals via $\ell_1$ minimization (convex) instead of $\ell_0$ (combinatorial).
- **Support vector machines (SVM):** Quadratic programming with convex hinge-loss constraints.

### Power Systems & Energy
- **Economic dispatch:** Minimize generation cost subject to convex transmission constraints; ensures global optimality.
- **Convex relaxations for optimal power flow:** Semidefinite programming (SDP) relaxations provide certificated bounds.

### Control Theory
- **Model predictive control (MPC):** Predict trajectories by solving convex quadratic programs repeatedly (when dynamics are linear).
- **Robust control design:** Semidefinite constraints from Lyapunov stability.

### Hardware Design & Resource Allocation
- **Convex optimization for chip design:** Placement, routing, thermal management use convex formulations.
- **Cloud resource allocation:** Convex models for load balancing, VM placement.

## Common Mistakes / Pitfalls

1. **Assuming all optimization is convex:** Many real problems are nonconvex. Without verifying convexity of both $f$ and $X$, local-minimum guarantees don't apply. Common culprits: bilinear terms, quadratic constraints without negative semidefiniteness, discrete variables.

2. **Confusing convex functions with convex sets:** A convex function $f$ doesn't automatically have a convex sublevel set $\{x : f(x) \leq t\}$ unless the set is defined that way. However, sublevel sets of *convex* functions *are* always conv