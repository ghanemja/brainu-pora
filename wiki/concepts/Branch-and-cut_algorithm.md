# Branch-and-cut Algorithm

## Definition

The **branch-and-cut algorithm** is an exact optimization method that combines two complementary techniques for solving integer and combinatorial optimization problems:

1. **Branch-and-bound**: Systematically divides the solution space into smaller subproblems (branching) and eliminates suboptimal regions (bounding)
2. **Cutting planes**: Iteratively tightens the feasible region by adding linear constraints (cuts) that eliminate fractional solutions while preserving integer solutions

The algorithm explores a tree of partial solutions, pruning branches where the lower bound exceeds the best known solution, while strengthening the linear relaxation at each node through cutting-plane techniques. It guarantees finding the global optimum for problems of the form:

$$\min \mathbf{c}^T \mathbf{x} \quad \text{subject to} \quad A\mathbf{x} \leq \mathbf{b}, \; \mathbf{x} \in \mathbb{Z}^n$$

## Key Equations

### Linear Relaxation and Bounds

At each node $k$ of the branch-and-tree, solve the relaxed LP:
$$z_{\text{LP}}^k = \min \mathbf{c}^T \mathbf{x} \quad \text{subject to} \quad A\mathbf{x} \leq \mathbf{b}, \; \mathbf{x} \in \mathbb{R}^n$$

This provides a **lower bound** (for minimization):
$$z_{\text{LP}}^k \leq z_{\text{OPT}}$$

### Pruning Condition

A node is pruned (eliminated) when:
$$z_{\text{LP}}^k \geq z_{\text{incumbent}}$$

where $z_{\text{incumbent}}$ is the best integer solution found so far.

### Cutting Plane Constraint

A cutting plane is a valid inequality:
$$\mathbf{a}^T \mathbf{x} \leq b$$

that satisfies:
- All feasible integer points satisfy the constraint
- The current fractional LP solution violates it

## Physical Intuition / Derivation

### Why Branch-and-Cut Works

**The Core Challenge**: Integer programming is NP-hard. Naive enumeration requires exploring $2^n$ possibilities. Three mechanisms combat this:

1. **Relaxation Gap**: Solving the LP relaxation (dropping integrality) is polynomial-time. If the LP solution is integer, we're done. Otherwise, we obtain a lower bound that guides search.

2. **Branching**: When LP solution $\mathbf{x}^*$ is fractional (e.g., $x_i^* = 0.3$), branch into two subproblems:
   - $\mathbf{x}_i \leq \lfloor x_i^* \rfloor = 0$
   - $\mathbf{x}_i \geq \lceil x_i^* \rceil = 1$
   
   This recursively partitions the feasible region into integer-respecting subsets.

3. **Cutting Planes**: Rather than blind branching, *tighten the LP relaxation* by adding constraints that:
   - Cut off the fractional LP solution
   - Preserve all integer feasible points
   
   This **strengthens the bound** without branching, reducing tree size.

### Example: QUBO/QUDO Context

For problems like QUBO (minimizing $\sum_{i \leq j} Q_{ij}x_i x_j$ with $x_i \in \{0,1\}$):
- The quadratic objective is replaced by its linear relaxation or lifted formulation
- Cuts exploit structure (e.g., clique inequalities, lifting)
- Branch-and-cut explores $\{0,1\}^n$ space while maintaining tight bounds

## Applications in Engineering

### Integer Linear Programming (ILP)

- **Mixed-integer scheduling**: Production planning with discrete time slots and machine assignments
- **Network design**: Routing and facility location with binary decisions (deploy/don't deploy)
- **Resource allocation**: Assigning discrete resources (workers, machines) to tasks

### Combinatorial Optimization

- **Traveling Salesman Problem (TSP)**: Branch-and-cut via subtour elimination cuts
- **Graph coloring**: Scheduling, register allocation in compilers
- **Quadratic unconstrained binary optimization (QUBO)**: Quantum computing applications, hardware optimization

### Engineering Solvers

Commercial and open-source solvers implementing branch-and-cut:
- **CPLEX** (IBM): Industry standard for MIP
- **Gurobi**: High-performance parallel branch-and-cut
- **SCIP**: Open-source framework combining branch-and-cut with cutting-plane methods

### Real-World Examples

- **Supply chain optimization**: Minimize cost of shipments with binary "route used" variables
- **Chip design**: Placement and routing with discrete grid constraints
- **Power systems**: Unit commitment (start/stop generators) with continuous generation levels

## Common Mistakes / Pitfalls

### 1. **Assuming LP Relaxation Bound is Tight**
- The LP relaxation may be far from integer optimum
- Gap = $(z_{\text{LP}} - z_{\text{OPT}}) / z_{\text{OPT}}$ can be large without cutting planes
- **Fix**: Rely on cuts to tighten bounds; don't terminate early based on LP alone

### 2. **Ignoring Problem Structure**
- Generic branch-and-cut is slower than problem-specific cuts
- For TSP, subtour elimination cuts are exponentially more efficient than generic cuts
- **Fix**: Identify and implement domain-specific cutting planes

### 3. **Poor Branching Strategy**
- Arbitrary variable selection (e.g., smallest index) leads to deep, wide trees
- **Better**: Use strong branching, pseudocost, or reliability branching to choose high-impact variables
- **Pitfall**: Computational cost of advanced branching must be weighed against tree reduction

### 4. **Computational Explosion on Large Instances**
- Branch-and-cut is exact but may not scale to very large problems
- Mixing with heuristics (warm-starting with heuristic solutions) is often necessary