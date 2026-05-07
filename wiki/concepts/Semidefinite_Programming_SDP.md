# Semidefinite Programming (SDP)

## Definition

**Semidefinite Programming** is a convex optimization framework that optimizes a linear objective function over the cone of positive semidefinite matrices. A standard SDP problem has the form:

$$\begin{align}
\text{minimize} \quad &\mathbf{c}^T \mathbf{x} \\
\text{subject to} \quad &\sum_{i=1}^{n} x_i \mathbf{A}_i + \mathbf{B} \succeq 0 \\
&\mathbf{x} \in \mathbb{R}^n
\end{align}$$

where $\mathbf{A}_i, \mathbf{B} \in \mathbb{S}^m$ (symmetric matrices), and the constraint $\mathbf{M} \succeq 0$ denotes positive semidefiniteness (all eigenvalues $\geq 0$).

Equivalently, an SDP can be formulated directly over matrix variables:
$$\text{minimize} \quad \langle \mathbf{C}, \mathbf{X} \rangle \quad \text{subject to} \quad \mathcal{A}(\mathbf{X}) = \mathbf{b}, \quad \mathbf{X} \succeq 0$$

where $\langle \mathbf{C}, \mathbf{X} \rangle = \text{tr}(\mathbf{C}^T \mathbf{X})$ is the trace inner product, and $\mathcal{A}$ represents linear constraints.

## Key Equations

### Positive Semidefiniteness Condition
A symmetric matrix $\mathbf{M}$ is positive semidefinite ($\mathbf{M} \succeq 0$) if and only if:
- All eigenvalues $\lambda_i(\mathbf{M}) \geq 0$, or equivalently
- There exists $\mathbf{L}$ such that $\mathbf{M} = \mathbf{L}\mathbf{L}^T$ (Cholesky decomposition)

### Dual SDP
The dual of the primal SDP is:
$$\begin{align}
\text{maximize} \quad &\mathbf{b}^T \mathbf{y} \\
\text{subject to} \quad &\sum_{j=1}^{p} y_j \mathbf{A}_j^T + \mathbf{Z} = \mathbf{C} \\
&\mathbf{Z} \succeq 0
\end{align}$$

Weak duality always holds: optimal primal value $\geq$ optimal dual value. **Strong duality** typically holds at optimality (if Slater's constraint qualification is satisfied).

### SDP Relaxation of Combinatorial Problems
For discrete optimization problems (e.g., maximum cut, graph coloring), SDP provides a convex relaxation by replacing discrete variables with matrix variables constrained to be positive semidefinite. The relaxation bound satisfies:
$$\text{SDP optimum} \geq \text{Combinatorial optimum}$$

## Physical Intuition / Derivation

### Why Matrices and Positive Semidefiniteness?

SDP extends linear programming (LP) by replacing the non-negative orthant constraint $\mathbf{x} \geq 0$ with the positive semidefinite cone—a much larger convex set that captures higher-order (quadratic) structure.

**Key insight**: Many combinatorial problems embed discrete decisions into quadratic forms. For example:
- A binary vector $\mathbf{b} \in \{0,1\}^n$ satisfies $\mathbf{b}\mathbf{b}^T \succeq 0$
- Correlations between binary variables appear as off-diagonal entries in $\mathbf{b}\mathbf{b}^T$

By optimizing over the relaxed cone $\mathbb{S}^n_+ = \{\mathbf{X} : \mathbf{X} \succeq 0\}$ instead of rank-1 matrices, we obtain a tractable (polynomial-time solvable) upper bound.

### Rounding and Primal Recovery

Since SDP relaxations typically allow non-integral or rank $> 1$ solutions, a **rounding scheme** recovers a feasible solution to the original problem:

1. Solve the SDP relaxation → obtain $\mathbf{X}^*$
2. Decompose: $\mathbf{X}^* = \mathbf{L}(\mathbf{L})^T$ via eigenvalue decomposition
3. Round projected solutions (e.g., via randomized hyperplane rounding) back to the feasible set

The gap between relaxation and rounded solution is bounded by approximation ratios (e.g., 1.138 for maximum cut via Goemans-Williamson algorithm).

### Computational Complexity

SDP can be solved in polynomial time via **interior-point methods** (typically $O(n^6)$ or better with specialized solvers), making it much faster than combinatorial search for large instances but slower than LP.

## Applications in Engineering

### 1. **Phylogenetic Inference (Computational Biology)**
- **Problem**: The Balanced Minimum Evolution (BME) problem seeks tree topologies minimizing weighted edge sums
- **SDP approach**: Relax tree topology constraints to positive semidefinite cone, solve efficiently, then round to valid trees
- **Advantage**: Provably better convergence than heuristic methods (MCMC, local search) for moderate dataset sizes

### 2. **Control Theory & Robust Control**
- **Linear Matrix Inequalities (LMIs)**: Stability, $\mathcal{H}_\infty$ control, and robustness constraints are naturally expressed as $\mathbf{A}(\mathbf{K}) \succeq 0$
- **Application**: Controller synthesis with guaranteed stability margins

### 3. **Signal Processing & Sensor Networks**
- **Localization**: Position estimation from distance measurements via distance geometry SDP
- **Compressed sensing**: Convex relaxations of sparse recovery (nuclear norm minim