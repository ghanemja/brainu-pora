# LP Relaxation

## Definition

An **LP relaxation** is a linear programming (LP) formulation obtained by relaxing the integrality constraints of a combinatorial optimization problem. Specifically, if the original problem requires variables to take integer values (typically in $\{0, 1\}$ for binary problems), the LP relaxation allows these variables to take any real value within specified bounds (usually $[0, 1]$).

Formally, given an integer program (IP):
$$\text{minimize/maximize} \quad \mathbf{c}^T \mathbf{x}$$
$$\text{subject to} \quad A\mathbf{x} \leq \mathbf{b}, \quad \mathbf{x} \in \mathbb{Z}^n$$

The LP relaxation removes the integrality constraint:
$$\text{minimize/maximize} \quad \mathbf{c}^T \mathbf{x}$$
$$\text{subject to} \quad A\mathbf{x} \leq \mathbf{b}, \quad \mathbf{x} \in \mathbb{R}^n$$

The solution set of the LP relaxation contains the solution set of the original IP, making the LP relaxation a **continuous outer approximation** of the discrete problem.

## Key Equations

**Bounding Property:** For a minimization problem,
$$\text{OPT}_{\text{IP}} \geq \text{OPT}_{\text{LP}}$$

For a maximization problem:
$$\text{OPT}_{\text{IP}} \leq \text{OPT}_{\text{LP}}$$

This inequality holds because the feasible region of the LP is larger, and relaxing constraints only improves (or maintains) the objective.

**Approximation Ratio:** If $x_{\text{round}}$ is an integer solution obtained by rounding an LP relaxation solution $x_{\text{LP}}$, the approximation factor is:
$$\alpha = \frac{\text{OPT}_{\text{IP}}}{|c^T x_{\text{round}}|}$$

**Integrality Gap:** The integrality gap measures the worst-case ratio between the LP relaxation bound and the true integer optimum:
$$\text{Gap} = \frac{\text{OPT}_{\text{LP}}}{\text{OPT}_{\text{IP}}}$$

## Physical Intuition / Derivation

### Why Relax?

Many combinatorial problems are NP-hard (e.g., Vertex Cover, Set Cover). Direct solution is computationally intractable. LP relaxations are polynomial-time solvable (via interior-point or simplex methods), making them useful for:

1. **Lower bounds:** The LP value provides a certificate on solution quality
2. **Rounding schemes:** LP solutions guide construction of integer solutions
3. **Approximation algorithms:** Proven approximation guarantees via rounding

### Geometric Intuition

The integer program defines a discrete set of feasible points. The LP relaxation "fills in" this point set by replacing the integer lattice constraint with a continuous polytope. The optimal LP solution typically lies at a vertex of this polytope—often with fractional coordinates.

### Half-Integral Solutions

Some LP relaxations exhibit special structure. For example, the **vertex cover LP relaxation** has the property that there exists an optimal solution with all variables in $\{0, 1/2, 1\}$—the set of half-integral solutions. This structure can be exploited for better rounding algorithms.

## Applications in Engineering

### 1. **Combinatorial Optimization**
- **Vertex Cover / Edge Coloring:** LP relaxations approximate NP-hard graph problems. The source material discusses LPVC (LP relaxation of Vertex Cover), which admits a $(2 - 2/k)$-approximation algorithm.
- **Hypergraph Coloring (MinECC):** The paper uses LPECC relaxation to bound the chromatic number of hypergraphs with guaranteed approximation ratios.

### 2. **Network Design & Flow Problems**
LP relaxations model:
- Minimum-cost flow with integer demand constraints
- Multi-commodity flow with routing decisions
- Supply chain optimization

### 3. **Scheduling & Resource Allocation**
- Job scheduling with machine capacity constraints
- Resource allocation under budget constraints
- Crew scheduling in transportation

### 4. **Algorithm Design**
- **Rounding procedures:** Convert fractional LP solutions to integer solutions via deterministic (e.g., greedy) or randomized (e.g., probabilistic) rounding
- **Cutting plane methods:** Tighten LP relaxations iteratively
- **Branch-and-bound:** Use LP bounds to prune the search tree

### 5. **Computational Verification**
In the source material, LPECC-based approaches using Gurobi provide:
- Quality benchmarks (tighter bounds than combinatorial methods)
- Solution verification for small instances
- Though they suffer memory/runtime issues at scale compared to direct combinatorial algorithms

## Common Mistakes / Pitfalls

### 1. **Assuming LP Solution Equals IP Solution**
The LP relaxation and IP have the same objective value only when the LP solution happens to be integral. For fractional solutions, rounding is necessary and introduces loss.

### 2. **Ignoring Integrality Gap**
A seemingly good LP bound may have poor actual integrality gap. For example:
- Set Cover LP has $\Omega(\log n)$ integrality gap
- Vertex Cover LP has integrality gap of 2 (every LP solution rounds to a solution within factor 2)

### 3. **Naive Rounding**
Simple rounding schemes (e.g., round-up all fractional variables) may violate constraints or produce arbitrarily bad solutions. Principled rounding procedures (e.g., randomized rounding, greedy rounding respecting constraint structure) are required.

### 4. **Scalability Assumptions**
Direct LP solvers (Gurobi, CPLEX) may struggle on large instances due to:
- Explicit enumeration of variables/constraints (e.g., the bad edge pairs $B$ in MinECC can be exponentially large)
- Memory limitations
- Numerical stability issues

As shown in the source material, combinatorial algorithms that implicitly exploit problem structure can outperform direct LP solvers.

### 5