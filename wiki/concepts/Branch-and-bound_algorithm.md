# Branch-and-bound Algorithm

## Definition

**Branch-and-bound** is an exact optimization algorithm that systematically explores the solution space of a combinatorial optimization problem by recursively partitioning (branching) the feasible region and discarding (bounding) suboptimal branches. It guarantees finding the optimal solution through intelligent pruning of the search tree.

The algorithm maintains:
- A **lower bound** (or upper bound, depending on maximization/minimization) on the best solution achievable within each subproblem
- A **current best solution** (incumbent) found so far
- A **search tree** of partial solutions

Any branch whose bound cannot improve upon the incumbent is pruned, reducing computational complexity from exhaustive enumeration.

## Key Equations

For a minimization problem with cost function $C(\vec{x})$:

$$\text{Prune branch } B \text{ if } \quad \text{LB}(B) \geq \text{UB}_{\text{incumbent}}$$

where:
- $\text{LB}(B)$ = lower bound on the cost of any complete solution in branch $B$
- $\text{UB}_{\text{incumbent}}$ = cost of the best solution found so far

**Search tree structure:**
Each node $n$ at depth $d$ represents a partial assignment of variables $\vec{x}_{1:d}$. The bound for node $n$ is computed as:

$$\text{LB}(n) = \min_{\vec{x}_{d+1:n}} C(\vec{x}_{1:d}, \vec{x}_{d+1:n})$$

(This minimum is itself typically computed via relaxation—linear programming relaxation, Lagrangian relaxation, etc.)

## Physical Intuition / Derivation

### Why Branch-and-Bound Works

Consider a binary decision tree where each level assigns one variable to 0 or 1. Naive enumeration explores all $2^n$ leaves. Branch-and-bound exploits **monotonicity of bounds**:

1. **Relaxation provides a lower bound:** Replace the hard constraint set with an easier one (e.g., allow continuous variables instead of binary). Any solution to the relaxed problem bounds the original.

2. **Pruning eliminates subtrees:** If a partial solution's lower bound already exceeds the best complete solution found, all extensions of that partial solution will be suboptimal. The entire subtree can be discarded without loss of optimality.

3. **Incumbent tightening:** As better feasible solutions are discovered, the pruning threshold $\text{UB}_{\text{incumbent}}$ tightens, enabling more aggressive pruning of remaining branches.

**Example:** For a QUBO problem (Equation 1), a linear programming relaxation replaces binary constraints $x_i \in \{0,1\}$ with $0 \leq x_i \leq 1$. The LP solution provides a lower bound. If this bound is worse than the best integer solution found, that branch is pruned.

### Search Strategy Trade-offs

- **Depth-first search (DFS):** Low memory, finds feasible solutions quickly (good incumbents for pruning)
- **Best-first search:** Explores most promising nodes first, tighter bounds, higher memory
- **Breadth-first search:** Explores level by level; rarely used due to memory constraints

## Applications in Engineering

### 1. **Integer Linear Programming (ILP)**
- Industrial scheduling (job shop, flow shop)
- Resource allocation and project management
- Vehicle routing problems (VRP)
- Used extensively in solvers like **CPLEX** and **Gurobi**

### 2. **Combinatorial Optimization**
- **QUBO/QUDO problems** (binary/integer quadratic optimization) arising in:
  - Quantum annealing preprocessing
  - Portfolio optimization
  - Circuit design optimization
  - Constraint satisfaction
  
### 3. **Mixed-Integer Programming (MIP)**
- Engineering design with discrete choices (e.g., discrete component sizes)
- Network design with topology selection
- Facility location problems

### 4. **Traveling Salesman Problem (TSP) & Variants**
- Logistics route optimization
- Printed circuit board drilling optimization

### 5. **Graph Coloring & Partitioning**
- Register allocation in compilers
- Frequency assignment in wireless networks

## Common Mistakes / Pitfalls

### 1. **Poor Bound Quality**
**Mistake:** Using a weak lower bound relaxation that provides little pruning.
- **Fix:** Invest in tight relaxations (e.g., Lagrangian duals, cutting planes) even if they increase per-node cost.

### 2. **No Primal Feasibility for Large Problems**
**Mistake:** The algorithm finds the first feasible solution very late, limiting pruning.
- **Fix:** Use construction heuristics or local search early to establish a good incumbent.

### 3. **Inefficient Node Selection**
**Mistake:** Exploring nodes in arbitrary order, missing promising branches.
- **Fix:** Use problem-specific branching rules and node selection strategies (e.g., best-first for tight bounds).

### 4. **Ignoring Problem Structure**
**Mistake:** Treating all problems as generic MIP; ignoring special structure.
- **Fix:** Exploit sparsity (e.g., tri-diagonal Q in T-QUDO), special substructures, and decomposition opportunities.

### 5. **Memory Explosion in DFS**
**Mistake:** Storing the entire search tree in memory for large instances.
- **Fix:** Use depth-first search with iterative deepening, or implement node recycling.

### 6. **Confusing Bounds for Different Objectives**
**Mistake:** Using maximization bounds in a minimization context.
- **Fix:** Always verify whether you're computing a lower bound (for minimization) or upper bound (for maximization).

## See Also

- [[Integer Linear Programming (ILP)]]
- [[QUBO (Quadratic Unconstrained Binary Optimization)]]
- [[Branch-and-Cut]]
- [[Lagrangian Relaxation]]
- [[Cutting Plane Method]]

## Sources

- *QUBO, QUDO and Tensor-QUDO formulations* – Lecture excerpt on combinatorial optimization methods
- Standard reference: Nemhauser & Wolsey, *Integer and Combinatorial Optimization* (