# Quadratic Unconstrained Binary Optimization (QUBO)

## Definition

**QUBO** (Quadratic Unconstrained Binary Optimization) is a class of combinatorial optimization problems where the objective is to find a binary assignment that minimizes (or maximizes) a quadratic polynomial with no explicit constraints.

Formally, a QUBO problem is defined as:

$$\text{minimize} \quad f(\mathbf{x}) = \mathbf{x}^T Q \mathbf{x} + \mathbf{c}^T \mathbf{x}$$

where:
- $\mathbf{x} \in \{0, 1\}^n$ is a binary vector of $n$ decision variables
- $Q \in \mathbb{R}^{n \times n}$ is a symmetric matrix of quadratic coefficients
- $\mathbf{c} \in \mathbb{R}^n$ is a vector of linear coefficients
- The quadratic term can be written as $\sum_{i,j} Q_{ij} x_i x_j$ or more explicitly $\sum_i Q_{ii} x_i^2 + \sum_{i<j} 2Q_{ij} x_i x_j$

**Key Property**: QUBO problems are *unconstrained*—all constraints must be encoded implicitly into the objective function, typically via penalty terms.

---

## Key Equations

### Standard QUBO Formulation

$$f(\mathbf{x}) = \sum_{i=1}^{n} Q_{ii} x_i + \sum_{i<j} Q_{ij} x_i x_j$$

where $x_i \in \{0, 1\}$ for all $i$.

### Constraint Encoding via Penalties

Many real problems have constraints. These are converted to QUBO by adding penalty terms:

$$f(\mathbf{x}) = f_{\text{original}}(\mathbf{x}) + \lambda \cdot g_{\text{penalty}}(\mathbf{x})$$

where $\lambda$ is a penalty weight chosen sufficiently large that constraint violations become suboptimal.

### Ising Model Equivalence

QUBO is equivalent to the Ising spin-glass problem with a change of variables $x_i = \frac{1 + s_i}{2}$ where $s_i \in \{-1, +1\}$:

$$E(\mathbf{s}) = \sum_{i<j} J_{ij} s_i s_j + \sum_i h_i s_i$$

This equivalence is foundational for quantum annealing approaches.

---

## Physical Intuition / Derivation

### Origin from Quadratic Problems

Many real-world optimization problems are inherently quadratic:
- **Quadratic assignment**: minimizing weighted distances between facility pairs
- **Maximum cut**: maximizing edges between two vertex partitions (quadratic in binary partition variables)
- **Graph coloring with penalties**: quadratic penalty for same-color neighbors

### Why Binary Restriction?

Restricting to binary variables ($\{0, 1\}$) makes the problem NP-hard but:
1. **Reduces search space dimensionality** compared to arbitrary integers
2. **Models boolean decisions**: Yes/No, On/Off, Include/Exclude
3. **Maps naturally to physical systems**: spins, qubits

### Connection to Energy Landscapes

When viewed as an Ising model, the QUBO objective $f(\mathbf{x})$ represents an energy landscape. Finding the minimum is equivalent to finding the ground state of a statistical mechanics system. This perspective motivates **quantum annealing** and **tensor network** solvers—they exploit quantum tunneling or tensor structure to escape local minima.

### Why Unconstrained?

Removing explicit constraints simplifies the problem structure:
- Enables uniform treatment across many domains
- Allows use of specialized solvers (quantum annealers, tensor networks)
- Forces problem formulation to "bake in" domain knowledge via penalties

---

## Applications in Engineering

### 1. **Combinatorial Logistics & Scheduling**
- **Vehicle Routing Problems (VRP)**: Minimize distance/time for delivery routes
  - Binary variables: $x_{ij}$ = "vehicle $i$ visits customer $j$"
  - Quadratic coupling: interactions between consecutive stops
  
- **Job Scheduling**: Minimize makespan or tardiness
  - Quadratic penalties for conflicts (e.g., two jobs on same machine)

### 2. **Graph-Based Problems**
- **Maximum Cut (MaxCut)**: Partition vertices to maximize edges between groups
  - Direct QUBO formulation: $f(\mathbf{x}) = -\sum_{(i,j) \in E} x_i(1-x_j) + x_j(1-x_i)$
  
- **Graph Coloring**: Assign colors with minimum conflicts
  - Penalty term for adjacent same-colored vertices

### 3. **Circuit Design & Layout**
- **Placement & Routing**: Minimize wire length in chip design
  - Quadratic distance metrics between components
  
- **Partition & Clustering**: Divide circuits into balanced groups

### 4. **Machine Learning & Statistical Inference**
- **Quadratic Unconstrained Models**: Training certain ML models
- **Inference in Graphical Models**: MAP estimation with pairwise interactions

### 5. **Resource Allocation**
- **Portfolio Optimization**: Maximize return subject to variance (quadratic risk)
  - Quadratic covariance terms between assets
  
- **Power Grid Operations**: Demand-supply matching with transmission losses (quadratic)

### 6. **Distributed Systems**
- **Load Balancing**: Assign tasks to processors, minimizing imbalance penalties

---

## Computational Complexity & Hardness

- **NP-hard** in general (reduction from MaxCut, which is NP-complete)
- For sparse instances with $k$-neighbor interactions (only nearby variables coupled), approximation algorithms may exploit locality
- **No known polynomial-time optimal solver** for general instances

---

## Solution Approaches

### Classical Methods
- **Simulated Annealing**: Probabilistic local search with temperature scheduling
- **Tabu Search**: Guided local search with memory
- **Sem