# Linear Programming

## Definition

**Linear programming (LP)** is an optimization technique for finding the maximum or minimum of a linear objective function subject to a set of linear equality and inequality constraints. In the canonical form, an LP problem is stated as:

$$\text{minimize/maximize} \quad \mathbf{c}^T \mathbf{x}$$

subject to:
$$\mathbf{A}\mathbf{x} \leq \mathbf{b}, \quad \mathbf{x} \geq \mathbf{0}$$

where $\mathbf{c} \in \mathbb{R}^n$ is the cost vector, $\mathbf{A} \in \mathbb{R}^{m \times n}$ is the constraint matrix, $\mathbf{b} \in \mathbb{R}^m$ is the bound vector, and $\mathbf{x} \in \mathbb{R}^n$ is the decision variable vector.

An LP problem can equivalently be formulated in **standard form**:

$$\text{minimize} \quad \mathbf{c}^T \mathbf{x}$$

subject to:
$$\mathbf{A}\mathbf{x} = \mathbf{b}, \quad \mathbf{x} \geq \mathbf{0}$$

The feasible region defined by the constraints is a convex polytope, and the optimal solution (if it exists) occurs at a vertex of this polytope.

---

## Key Equations

**Dual LP Problem** (fundamental to LP theory):

Given the primal LP:
$$\min \mathbf{c}^T \mathbf{x} \quad \text{s.t.} \quad \mathbf{A}\mathbf{x} = \mathbf{b}, \mathbf{x} \geq 0$$

The dual is:
$$\max \mathbf{b}^T \mathbf{y} \quad \text{s.t.} \quad \mathbf{A}^T \mathbf{y} \leq \mathbf{c}$$

**Weak Duality:**
$$\mathbf{c}^T \mathbf{x}^* \geq \mathbf{b}^T \mathbf{y}^*$$

for any feasible $\mathbf{x}^*$ and $\mathbf{y}^*$. Under certain regularity conditions, **strong duality** holds: the optimal values are equal.

**Complementary Slackness:** At optimality,
$$x_i(\mathbf{A}^T\mathbf{y})_i - c_i) = 0 \quad \forall i$$

---

## Physical Intuition / Derivation

### Why Linear Programming Works

The power of LP stems from the geometry of linear constraints and objectives:

1. **Convex Feasible Region:** The set of points satisfying all linear constraints forms a convex polytope in $\mathbb{R}^n$. This convexity guarantees that any local optimum is a global optimum.

2. **Extreme Points:** Because the objective function $\mathbf{c}^T \mathbf{x}$ is linear, its level sets are hyperplanes. The optimal solution must lie at a *vertex* (extreme point) of the feasible polytope. This dramatic reduction in search space is exploited by algorithms like the **simplex method**.

3. **Polynomial Solvability:** Modern LP algorithms (interior-point methods, ellipsoid method) run in polynomial time, making LP tractable for large-scale problems.

### Example: Resource Allocation

Suppose a factory produces two products with:
- Decision variables: $x_1, x_2$ = units of products 1 and 2
- Objective: maximize profit $\max 5x_1 + 4x_2$
- Constraints: labor ($2x_1 + 3x_2 \leq 100$), materials ($4x_1 + 2x_2 \leq 80$)

The optimal $(x_1^*, x_2^*)$ lies at a corner of the constraint region (the intersection of two binding constraint boundaries).

---

## Applications in Engineering

### Operations Research & Manufacturing
- **Production planning:** Determining optimal product mix under resource constraints
- **Supply chain optimization:** Minimizing transportation costs while meeting demand
- **Scheduling:** Allocating workers/machines to tasks

### Electrical Engineering
- **Power flow optimization:** Minimizing generation cost while respecting transmission constraints
- **Optimal power dispatch:** Real-time grid management

### Civil Engineering
- **Water resource allocation:** Distributing water across competing users
- **Project scheduling:** Minimizing project duration with precedence constraints

### Telecommunications
- **Network routing:** Maximizing throughput or minimizing latency under bandwidth constraints
- **Frequency assignment:** Assigning channels to users/cells

### Machine Learning & Optimization
- **SVM formulation:** Support vector machines reduce to quadratic programs with LP subproblems
- **Relaxations:** LP relaxations of integer programs provide bounds for branch-and-bound algorithms
- **Surrogate formulations:** As mentioned in source material, LP can replace heavy machinery in geometric algorithms (e.g., determining isomorphism via Phase space constraints)

---

## Common Mistakes / Pitfalls

### 1. **Non-convex Objectives or Constraints**
LP requires *both* objective and constraints to be linear. If the problem has quadratic terms, products of variables, or nonlinear functions, LP cannot be directly applied.
- **Fix:** Use nonlinear programming (NLP), quadratic programming (QP), or convex optimization frameworks.

### 2. **Unbounded or Infeasible Problems**
A problem may have no optimal solution if:
- The feasible region is empty (infeasibility)
- The objective can increase indefinitely (unboundedness)

Always check solver output for these conditions.

### 3. **Integer Constraints Ignored**
In practice, solutions must often be integer (e.g., number of items to produce). The LP relaxation (dropping integrality) gives a lower bound but not necessarily an integer-feasible solution.
- **Fix:** Use integer linear programming (ILP) or mixed-integer programming (MIP) solvers