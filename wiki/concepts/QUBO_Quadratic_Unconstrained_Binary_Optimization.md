# QUBO (Quadratic Unconstrained Binary Optimization)

## Definition

**QUBO** is a combinatorial optimization problem that seeks to find a binary vector $\vec{x} \in \{0,1\}^n$ minimizing a quadratic polynomial cost function. The problem is entirely characterized by a symmetric matrix $Q \in \mathbb{R}^{n \times n}$.

QUBO belongs to the class of **NP-hard optimization problems**, making it computationally challenging for large instances. However, its restricted structure—binary variables and quadratic interactions—enables it to be solved by specialized algorithms and quantum computing approaches that exploit this specific form.

## Key Equations

### Standard QUBO Formulation

$$C(\vec{x}) = \sum_{i,j=0}^{n-1} Q_{ij} x_i x_j \quad \text{where } x_i \in \{0,1\}, \quad i \leq j$$

### Key Property: Idempotence

$$x_i^2 = x_i \quad \text{for binary } x_i$$

This property means **linear and quadratic terms are equivalent** for binary variables. Any linear term $\ell_i x_i$ can be absorbed into the diagonal element: $Q_{ii} := Q_{ii} + \ell_i$. Therefore, the general quadratic binary optimization reduces to the standard QUBO form without explicit linear terms.

### General Quadratic Form (Pre-Reduction)

$$C(\vec{x}) = \sum_{i=0}^{n-1} \ell_i x_i + \sum_{i,j=0}^{n-1} Q_{ij} x_i x_j \quad \xrightarrow{\text{idempotence}} \quad \sum_{i,j=0}^{n-1} Q'_{ij} x_i x_j$$

## Physical Intuition / Derivation

### Connection to the Ising Model

QUBO is mathematically equivalent to finding the **ground state of an Ising Hamiltonian**. The Ising model describes a system of binary spins, where the energy is:

$$H = \sum_{i,j} J_{ij} \sigma_i \sigma_j + \sum_i h_i \sigma_i$$

with $\sigma_i \in \{-1, +1\}$. By substituting $x_i = \frac{1 - \sigma_i}{2}$ (a change of variables from binary to spin representation), the Ising Hamiltonian becomes a QUBO problem. Thus, **minimizing a QUBO cost function is equivalent to finding the lowest-energy state of an Ising spin glass system**.

### Why Binary Variables Matter

The idempotence property $x_i^2 = x_i$ is **non-trivial and powerful**:

- It eliminates the need for separate handling of linear coefficients
- It means the problem has a special polynomial structure, not arbitrary polynomials
- It makes the problem amenable to quantum annealing, which exploits this algebraic constraint

### Hierarchical Problem Families

QUBO generalizes and specializes within a hierarchy:

1. **QUBO** (this page): binary variables only, quadratic interactions
2. **QUDO** (Quadratic Unconstrained Discrete Optimization): extends to integer variables $x_i \in \{0, 1, \ldots, d-1\}$
   - Cost: $C(\vec{x}) = \sum_{i,j} Q_{ij} x_i x_j + \sum_i D_i x_i$ (linear term no longer absorbable)
3. **Tensor-QUDO** (T-QUDO): tensorial cost function with full index freedom
   - Cost: $C(\vec{x}) = \sum_{i,j} \hat{Q}_{i,j,x_i,x_j}$ where $\hat{Q}$ is a 4-index cost tensor

## Applications in Engineering

### 1. **Combinatorial Optimization Problems**
- **Circuit design and chip placement**: Minimize power consumption and wire routing by assigning binary variables to gate placements
- **Graph partitioning**: Divide large networks into balanced, low-cut subsets
- **Maximum cut (MaxCut)**: Find the optimal partition of graph vertices (fundamental in machine learning and network analysis)

### 2. **Machine Learning**
- **Ising spin glass models**: Training neural networks with binary weights and connections
- **Feature selection**: Binary variables indicate which features to include in predictive models
- **Clustering**: Assigning data points to binary cluster memberships

### 3. **Logistics and Operations Research**
- **Traveling Salesman Problem (TSP)**: Encode permutations of cities as binary variables (via one-hot encoding)
- **Vehicle routing and scheduling**: Minimize fuel/time with binary assignment variables
- **Knapsack problems**: Select items (binary choice) to maximize value subject to capacity

### 4. **Financial Portfolio Optimization**
- **Portfolio selection**: Binary variables indicate which assets to hold
- **Risk hedging**: Optimize binary trading strategies

### 5. **Physics Simulations**
- **Quantum annealing and adiabatic quantum computing**: QUBO is the native problem formulation
- **Combinatorial materials discovery**: Binary selection of atom types in crystal structures

## Solution Methods

### Exact Algorithms
- **Branch-and-bound**: Systematically prunes the binary tree by bounding suboptimal branches
- **Branch-and-cut**: Combines branch-and-bound with cutting-plane methods to tighten feasible regions
- **Integer linear programming (ILP) solvers**: CPLEX, Gurobi formulate QUBO as constrained integer programs

### Classical Heuristics
- **Simulated annealing**: Probabilistically accepts worse solutions to escape local minima (inspired by physical annealing)
- **Tabu search**: Explores neighborhoods while maintaining a forbidden (taboo) list to avoid cycles
- **Genetic algorithms**: Population-based evolution through selection, crossover, and mutation

### Quantum and Emerging Methods
- **Quantum annealing**: Exploits adiabatic evolution on a quantum processor; encodes QUBO as an Ising Hamiltonian
- **Quantum Approximate