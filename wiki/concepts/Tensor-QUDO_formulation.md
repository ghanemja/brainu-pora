# Tensor-QUDO Formulation

## Definition

**Tensor-QUDO** (Tensor Quadratic Unconstrained Discrete Optimization) is a generalized optimization framework that extends QUBO (Quadratic Unconstrained Binary Optimization) and QUDO (Quadratic Unconstrained Discrete Optimization) to higher-order tensor interactions. 

In Tensor-QUDO, the optimization problem seeks to find a discrete variable assignment $\vec{x} = (x_0, x_1, \ldots, x_{n-1})$ where each variable $x_i \in \{0, 1, \ldots, d-1\}$ takes integer values from a finite domain, that minimizes a cost function defined by indexed tensor lookups rather than algebraic products.

This formulation is particularly valuable for problems where interaction costs between variables cannot be decomposed into simple quadratic terms and require explicit specification via tensor indexing.

## Key Equations

### Standard QUBO (Binary Variables Only)
$$C(\vec{x}) = \sum_{i,j=0, \, i \leq j}^{n-1} Q_{ij} x_i x_j$$

where $\vec{x} \in \{0,1\}^n$ and $Q$ is a symmetric matrix. The property $x_i^2 = x_i$ allows linear terms to be absorbed into quadratic terms.

### QUDO (Discrete Variables, Quadratic Form)
$$C(\vec{x}) = \sum_{i,j=0, \, i \leq j}^{n-1} Q_{ij} x_i x_j + \sum_{i=0}^{n-1} D_i x_i$$

where $x_i \in \{0, 1, \ldots, d-1\}$, $Q$ is a symmetric matrix, and $\vec{D}$ is a linear coefficient vector. The linear term $D_i x_i$ cannot be absorbed because $x_i^2 \neq x_i$ for $d > 2$.

### Tensor-QUDO (General Tensor Interactions)
$$C(\vec{x}) = \sum_{i,j=0, \, i \leq j}^{n-1} \hat{Q}_{i,j,x_i,x_j}$$

where $\hat{Q}$ is a 4-index cost tensor with dimensions $n \times n \times d \times d$. The value $\hat{Q}_{i,j,x_i,x_j}$ directly specifies the cost contribution when variables at positions $i$ and $j$ take values $x_i$ and $x_j$ respectively.

**Relationships between formulations:**
- QUBO is a special case where $\hat{Q}_{i,j,a,b} = Q_{ij} \cdot a \cdot b$
- QUDO is a special case where $\hat{Q}_{i,j,a,b} = Q_{ij} \cdot a \cdot b$ (with linear terms handled separately)

## Physical Intuition / Derivation

### Motivation for Generalization

The progression from QUBO → QUDO → Tensor-QUDO addresses fundamental limitations in expressiveness:

1. **QUBO** assumes binary variables where the idempotent property $x_i^2 = x_i$ creates a mathematical convenience: any cost function over binary variables naturally decomposes into quadratic form. However, many practical problems involve multi-valued discrete choices (e.g., task scheduling where $x_i$ represents one of $d$ possible time slots).

2. **QUDO** extends to integer-valued variables $x_i \in \{0, 1, \ldots, d-1\}$, eliminating the idempotent property. Now linear and quadratic terms cannot be merged. However, the cost function is still algebraically defined—interaction costs are products of variable values.

3. **Tensor-QUDO** recognizes that many real problems have **non-multiplicative interaction costs**. For example:
   - In quantum chemistry, the interaction energy between two qubits depends on their combined quantum state in ways that cannot be factored as products
   - In circuit design, the crosstalk penalty between signal lines depends discretely on both signals' states
   - In scheduling, the communication overhead between two tasks depends on which specific time slots they occupy, not just linearly on those times

### Why the Tensor Formulation?

The tensor $\hat{Q}_{i,j,x_i,x_j}$ provides a **lookup table** that directly encodes arbitrary pairwise interaction costs. This is maximally expressive while remaining computationally tractable because:
- The interaction is still **pairwise** (limited to pairs of variables), avoiding exponential blowup
- Cost lookup is $O(1)$ per term
- The structure is compatible with standard discrete optimization solvers adapted for tensor forms

## Applications in Engineering

### 1. Quantum Circuit Optimization
Tensor-QUDO naturally models the cost of assigning qubits to physical qubits in a quantum processor where crosstalk penalties depend discretely on the physical distance and qubit states. The tensor $\hat{Q}$ encodes calibrated crosstalk matrices.

### 2. Task Scheduling and Resource Allocation
For scheduling $n$ tasks to $d$ time slots or resources:
- $x_i$ = resource assigned to task $i$
- $\hat{Q}_{i,j,a,b}$ = communication cost when task $i$ uses resource $a$ and task $j$ uses resource $b$

Non-multiplicative costs arise from contention, latency, and bandwidth limitations that depend on the specific resource pair, not just their values.

### 3. Graph Coloring and Constraint Satisfaction
In graph coloring with $d$ colors and soft constraints:
- $x_i$ = color assigned to node $i$
- $\hat{Q}_{i,j,a,b}$ = penalty for assigning color $a$ to node $i$ and color $b$ to node $j$ (depends on edge properties and color compatibility rules)

### 4. Circuit Design and Signal Integrity
Crosstalk and electromagnetic interference modeling where the coupling strength between two nets depends on both the signal states they carry.

### 5. Combinatorial