# Quadratic Unconstrained Discrete Optimization (QUDO)

## Definition

**Quadratic Unconstrained Discrete Optimization (QUDO)** is a class of combinatorial optimization problems in which the objective is to find an assignment of discrete (integer) values to decision variables that minimizes or maximizes a quadratic objective function, with no explicit constraints on the variable assignments.

Formally, a QUDO problem seeks to optimize:

$$\min_{\mathbf{x}} \, f(\mathbf{x}) = \sum_{i} c_i x_i + \sum_{i,j} Q_{ij} x_i x_j$$

where:
- $\mathbf{x} = (x_1, x_2, \ldots, x_n)$ are decision variables
- Each $x_i \in D = \{d_1, d_2, \ldots, d_m\}$ (a finite discrete set)
- $c_i$ are linear coefficients
- $Q_{ij}$ are quadratic interaction coefficients
- No explicit constraints on variable values (unconstrained)

### Related Variants

**QUBO** (Quadratic Unconstrained **Binary** Optimization) is a special case where $x_i \in \{0, 1\}$.

**QUDO** is the generalization allowing arbitrary finite discrete domains (e.g., $\{0, 1, 2, \ldots, k\}$).

---

## Key Equations

### Standard QUDO Formulation

$$\text{QUDO:} \quad \min_{\mathbf{x} \in D^n} \left( \mathbf{c}^T \mathbf{x} + \mathbf{x}^T Q \mathbf{x} \right)$$

### k-Neighbors Interaction Model

For problems with local interactions on a linear chain (k-neighbors), the objective simplifies to:

$$f(\mathbf{x}) = \sum_{i=1}^{n} c_i x_i + \sum_{i=1}^{n-k} \sum_{j=i+1}^{i+k} Q_{ij} x_i x_j$$

This structure enables efficient tensor network contraction, as interactions are restricted to local neighborhoods rather than all-pairs.

### Tensor Representation

A QUDO problem can be represented as a **Tensor QUDO (T-QUDO)** problem where:
- Each variable assignment is encoded as a tensor factor
- The objective function is expressed as a tensor network contraction
- The minimum energy state corresponds to the optimal solution

---

## Physical Intuition / Derivation

### Why Quadratic Optimization Matters

Many real-world combinatorial problems naturally decompose into pairwise interactions:
- **Graph coloring**: assign colors to nodes; penalty for conflicting adjacent nodes
- **Scheduling**: assign time slots to tasks; pairwise compatibility costs
- **Logistics**: route planning with distance penalties (quadratic in nature)

### Connection to Statistical Mechanics

QUDO problems are analogous to **spin systems** in statistical mechanics:
- Each discrete variable $x_i$ corresponds to a "spin" or state
- The objective function $f(\mathbf{x})$ plays the role of **Hamiltonian energy**
- The global minimum of $f$ corresponds to the ground state
- Temperature-based relaxation (imaginary time evolution) can help escape local minima

### Why "Unconstrained"?

The term *unconstrained* distinguishes QUDO from **constrained quadratic programs** (QP), where explicit constraints $g(\mathbf{x}) \leq 0$ restrict feasible regions. In QUDO:
- All assignments are technically feasible
- Infeasible regions are penalized indirectly through the objective function (if needed)
- This structure allows for quantum-inspired and tensor network solutions

### Tensor Network Approach (MeLoCoToN)

The source material's tensor network algorithm exploits the QUDO structure via:

1. **Superposition**: Initial quantum state represents all possible variable assignments
2. **Imaginary Time Evolution**: Exponential decay $e^{-\beta H}$ suppresses high-energy (poor) solutions
3. **Projective Measurement**: Collapse to lowest-energy classical state
4. **Tensor Contraction**: Efficient computation via local tensor operations on k-neighbor structure

---

## Applications in Engineering

### 1. **Scheduling and Resource Allocation**
- Assign jobs to machines minimizing total time/cost
- QUDO encodes job duration (linear term) + machine compatibility penalties (quadratic term)
- Example: manufacturing, cloud computing job placement

### 2. **Vehicle Routing & Logistics**
- Traveling Salesman Problem (TSP): variables = permutations encoded as discrete states
- Quadratic cost encodes distance penalties between consecutive cities
- Multi-vehicle variants use additional discrete variables

### 3. **Electrical Grid Optimization**
- Unit commitment: decide which power plants to activate (discrete on/off states)
- Quadratic objective: generation cost + transmission loss penalties + ramping costs
- k-neighbor structure reflects geographical grid topology

### 4. **Circuit Design & VLSI**
- Placement and routing: assign components to discrete grid positions
- Quadratic interactions model congestion and signal integrity penalties
- Natural k-neighbor structure from physical proximity

### 5. **Graph Coloring & Constraint Satisfaction**
- Assign discrete "colors" (or states) to nodes
- Pairwise penalties enforce constraints (e.g., adjacent nodes cannot share color)
- Application: frequency assignment in wireless networks, register allocation in compilers

### 6. **Quantum Annealing Hardware**
- QUBO/QUDO are the native problem class for quantum annealers (D-Wave, others)
- Directly map to hardware Ising/QUBO models
- Enables near-term quantum advantage exploration

---

## Common Mistakes / Pitfalls

### 1. **Confusing QUDO with QP (Quadratic Programming)**
- **Mistake**: Treating QUDO variables as continuous
- **Reality**: QUDO variables are *discrete* (integer-valued), making it NP-hard
- **Impact**: Continuous relaxation solvers (interior point, etc.) don't directly apply

### 2. **