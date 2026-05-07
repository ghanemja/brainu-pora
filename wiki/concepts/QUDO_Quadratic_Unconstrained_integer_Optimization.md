# QUDO (Quadratic Unconstrained integer Optimization)

## Definition

**QUDO** is a generalization of the **QUBO** (Quadratic Unconstrained Binary Optimization) problem that allows variables to take on integer values from a finite domain, rather than being restricted to binary values.

Formally, QUDO is the problem of minimizing a cost function over integer variables:

$$\text{minimize} \quad C(\vec{x}) = \sum_{i,j=0, i \leq j}^{n-1} Q_{ij} x_i x_j + \sum_{i=0}^{n-1} D_i x_i$$

subject to:
$$x_i \in \{0, 1, 2, \ldots, d-1\} \quad \forall i$$

where:
- $Q$ is a symmetric matrix encoding quadratic interaction coefficients
- $\vec{D}$ is a vector of linear coefficients
- $d$ is the maximum domain size (can vary per variable)
- $n$ is the number of variables

The problem is **unconstrained** in the sense that there are no explicit constraints beyond the domain restrictions on variables; all problem structure is encoded in the cost function.

---

## Key Equations

### Standard QUDO Formulation
$$C(\vec{x}) = \sum_{i,j=0, i \leq j}^{n-1} Q_{ij} x_i x_j + \sum_{i=0}^{n-1} D_i x_i$$

### Tensor QUDO (T-QUDO) Extension
$$C(\vec{x}) = \sum_{i,j=0, i \leq j}^{n-1} \hat{Q}_{i,j,x_i,x_j}$$

where $\hat{Q}$ is a 4-index tensor with shape $[n] \times [n] \times [d] \times [d]$, and the indices $x_i, x_j$ directly index into the tensor.

### Comparison with QUBO
QUBO is a special case of QUDO where $x_i \in \{0, 1\}$. The key difference is the idempotent property:

**QUBO:** $x_i^2 = x_i$ (absorption of linear terms into quadratic)

**QUDO:** $x_i^2 \neq x_i$ (linear and quadratic terms remain distinct)

---

## Physical Intuition / Derivation

### Why Distinguish QUDO from QUBO?

In binary optimization, the constraint $x_i \in \{0,1\}$ automatically satisfies $x_i^2 = x_i$. This means any term like $c_i x_i$ can be absorbed into the quadratic term $Q_{ii} x_i^2 = Q_{ii} x_i$. Thus QUBO needs only one coefficient per variable pair.

For integer variables with $d > 2$, this algebraic property breaks down:
- $x_i = 2 \Rightarrow x_i^2 = 4 \neq 2$
- $x_i = 3 \Rightarrow x_i^2 = 9 \neq 3$

Therefore, **linear and quadratic terms carry independent information** and must be kept separate. This is why QUDO requires both a matrix $Q$ and a vector $\vec{D}$.

### Connection to Ising Models and Quantum Computing

QUDO problems can be mapped to energy minimization problems analogous to the **Ising Hamiltonian** in statistical physics:
$$H = -\sum_{i,j} J_{ij} s_i s_j - \sum_i h_i s_i$$

where $s_i$ are spins. QUBO/QUDO can be reformulated to fit this framework, motivating quantum annealing approaches that seek the ground state (minimum energy configuration).

---

## Applications in Engineering

### 1. **Combinatorial Optimization**
- **Graph partitioning and coloring:** Partition nodes with multi-level objectives
- **Resource allocation:** Assign resources at integer levels (number of workers, materials units, etc.)
- **Scheduling:** Assign tasks to time slots with integer durations

### 2. **Machine Learning & Neural Networks**
- **Quantization:** Integer weights and activations for neural network compression
- **Clustering:** Multi-level cluster assignment (hard $k$-means generalizations)

### 3. **Hardware/VLSI Design**
- **Gate sizing:** Assign discrete transistor sizes to minimize power/delay
- **Placement & routing:** Route signals through discrete channel widths
- **Power management:** Set supply voltage levels (often quantized) per domain

### 4. **Operations Research**
- **Vehicle routing:** Assign vehicle types (with capacity levels) to routes
- **Bin packing variants:** Pack items into bins with multiple bin types
- **Portfolio optimization:** Discrete holdings in investment assets

### 5. **Emerging Quantum Computing Applications**
- **Quantum annealing on D-Wave systems:** Specialized for QUBO, but QUDO can be embedded
- **QAOA (Quantum Approximate Optimization Algorithm):** Polynomial encoding of QUDO into QUBO via ancilla variables

---

## Common Mistakes / Pitfalls

### 1. **Assuming QUDO = QUBO**
QUDO is fundamentally different for multi-valued domains. Don't try to absorb linear terms into quadratic; they are independent. Algorithms designed for QUBO may be inefficient for QUDO.

### 2. **Forgetting the Linear Term**
The vector $\vec{D}$ is not optional for $d > 2$. Omitting it loses expressive power.

### 3. **Embedding QUDO in QUBO Naively**
A common approach is to use **one-hot encoding**: represent each integer variable as a set of binary variables. However, this:
- Exponentially increases problem size
- Introduces artificial constraints (exactly one bit per variable set)
- Destroys sparsity in the problem structure
- Should only be used if your solver truly requires binary inputs

### 4. **Confusing T-QUDO with QUDO**
T