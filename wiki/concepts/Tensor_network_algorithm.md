# Tensor Network Algorithm

## Definition

A **tensor network algorithm** is a computational method that leverages tensor contraction and network structures to solve combinatorial optimization problems by representing them as interconnected multi-dimensional arrays (tensors). The algorithm encodes problem constraints and objectives into a tensor network, then solves the optimization via systematic contraction operations, often inspired by quantum mechanics principles such as superposition and imaginary time evolution.

In the context of quadratic optimization, tensor network algorithms target three problem classes:

- **QUBO** (Quadratic Unconstrained Binary Optimization): Variables $x_i \in \{0,1\}$
- **QUDO** (Quadratic Unconstrained Discrete Optimization): Variables $x_i \in \{0,1,\ldots,d-1\}$ for finite set sizes
- **T-QUDO** (Tensor QUBO): Higher-order tensor formulations of discrete optimization problems

## Key Equations

### General Objective Function (QUBO)

$$H(x) = \sum_{i} c_i x_i + \sum_{i<j} Q_{ij} x_i x_j$$

where $x = (x_1, \ldots, x_n) \in \{0,1\}^n$, $c_i$ are linear coefficients, and $Q_{ij}$ are quadratic coupling terms.

### QUDO Extension

$$H(x) = \sum_{i} c_i x_i + \sum_{i<j} Q_{ij} x_i x_j, \quad x_i \in \{0,1,\ldots,d-1\}$$

### Imaginary Time Evolution (MeLoCoToN Framework)

The algorithm evolves an initial superposition state through imaginary time:

$$|\psi(t)\rangle = e^{-\beta H} |\psi_0\rangle$$

where $\beta$ is the inverse temperature parameter, effectively concentrating amplitude on low-energy (near-optimal) states.

### Tensor Contraction (k-neighbors in Linear Chain)

For a chain with $k$-neighbor interactions, contraction reduces tensor dimensions:

$$T_{\text{contracted}}^{(i)} = \sum_{j,k,\ldots} T^{(i)}_{a,b,c,\ldots} \cdot T^{(i+1)}_{c,d,e,\ldots} \cdots$$

This operation is central to efficiently computing partition functions and ground state properties.

## Physical Intuition / Derivation

### Quantum-Inspired Framework

Tensor network algorithms adapt quantum computing principles to classical systems:

1. **Superposition Encoding**: The optimization landscape is encoded as a tensor network where each index represents a variable dimension. A superposition of all possible variable assignments is implicitly represented.

2. **Imaginary Time Evolution**: Unlike real time evolution (which preserves norm), imaginary time evolution $e^{-\beta H}$ amplifies low-energy solutions exponentially. This acts as a "cooling" mechanism in classical optimization—solutions with lower objective values accumulate higher amplitudes in the tensor representation.

3. **Projective Measurement**: After evolution, measurement collapses the tensor state, yielding a concrete variable assignment biased toward the optimal solution.

### Why Tensor Networks?

Tensor networks provide computational efficiency for certain problem structures:

- **Locality**: k-neighbor interactions in a chain can be represented as local tensors, avoiding full $d^n$ exponential blowup
- **Contraction Order**: Smart contraction sequences (guided by tree decomposition or matrix product state structure) reduce computational cost from exponential to polynomial in chain length for specific architectures
- **Sparsity Exploitation**: Many real optimization problems exhibit sparse coupling; tensor networks naturally exploit this

### Waterfall Technique

A specialized optimization technique within the tensor network algorithm framework that refines solutions by systematically cascading tensor updates through the network, improving solution quality without full recontraction.

## Applications in Engineering

### 1. **Logistics and Supply Chain**
- Vehicle routing with time windows (generalized TSP)
- Warehouse picking optimization with complex constraints
- Network flow optimization with quadratic costs

### 2. **Scheduling and Resource Allocation**
- Job shop scheduling with machine dependencies
- Power grid scheduling with quadratic generation costs
- Personnel rostering with soft constraints encoded as quadratic penalties

### 3. **Circuit Design and Layout**
- Chip placement optimization (minimizing wire lengths, modeled as QUBO)
- Graph partitioning for circuit decomposition
- Register allocation in compilers

### 4. **Machine Learning**
- Feature selection with quadratic interaction terms
- Hyperparameter optimization over discrete domains
- Constraint satisfaction in neural network training

### 5. **Financial Applications**
- Portfolio optimization with interaction terms (beyond Markowitz)
- Arbitrage detection in market graphs
- Risk assessment with correlated asset interactions

## Common Mistakes / Pitfalls

### 1. **Confusing Tensor Order with Problem Dimension**
**Mistake**: Assuming a 4th-order tensor directly solves a 4-variable problem.  
**Reality**: A tensor's order (rank) is independent of the problem size. A single 4th-order tensor can represent interactions among 4 variables, but scaling to $n$ variables requires careful network design (e.g., matrix product states with $O(n)$ tensors).

### 2. **Neglecting Contraction Complexity**
**Mistake**: Assuming tensor contraction is always faster than brute force.  
**Reality**: Arbitrary contraction sequences can be exponentially costly. Only certain graphical structures (trees, chains with low treewidth) guarantee polynomial-time contraction. Always analyze the tensor network's graph topology first.

### 3. **Misinterpreting "Quantum-Inspired"**
**Mistake**: Expecting quantum advantage or understanding the algorithm as actual quantum computation.  
**Reality**: These are classical algorithms inspired by quantum mechanics principles. They run entirely on classical hardware and offer no inherent speedup beyond algorithmic innovation—benefits depend on problem structure and parameter tuning.

### 4. **Improper Parameter Tuning of $\beta$**
**Mistake**: Using a fixed inverse temperature across diverse problem instances.  
**Reality**: $\beta$ must be tuned per problem; too small yields weak filtering of solutions, too large causes numerical underflow. Problem-aware heuristics or adaptive schedules are essential.

### 5. **