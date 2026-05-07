# Tensor Network

## Definition

A **tensor network** is a computational framework for representing and manipulating multi-dimensional arrays (tensors) as a network of interconnected nodes and edges. Each node represents a tensor with a specific rank (number of indices), and edges connecting nodes represent tensor contractions or shared indices.

In the context of quantum simulation and optimization, a tensor network encodes:
- **Quantum states** and their superpositions
- **Interaction terms** in Hamiltonians (such as single-body and pairwise interactions)
- **Temporal evolution** through imaginary time evolution operators
- **Measurement and trace operations** via partial tracing

The network structure provides a graphical notation where:
- Nodes = individual tensors with labeled indices
- Edges = index contractions or shared quantum degrees of freedom
- The overall network = the complete mathematical expression for a state or operator

## Key Equations

### Basic Tensor Types

**Initial Superposition Tensor:**
$$+_i^d = 1 \quad \forall i \in \{1, \ldots, d\}$$
Creates an equal superposition state across $d$ dimensions.

**Partial Trace Superposition Tensor:**
$$P+_i^d = 1 \quad \forall i \in \{1, \ldots, d\}$$
Similar to initial superposition but applied in trace regions of the network.

**Single-Index Evolution Tensor (Non-cross Interaction):**
$$S_\mu^l = e^{-\tau(Q_l^i i/2 + D_l^i)} \quad \text{where } \mu = i$$
Dimensions: $S^l \in \mathbb{C}^{d \times d}$

Implements imaginary time evolution: $e^{-\tau H}$ for a local term.

**Three-Index Evolution Tensor (Last Row Cross Interaction):**
$$S_{i\mu j}^{n-1,m} = e^{-\tau Q_{n-1,m}^{ij}} \quad \text{where } \mu = i$$
Dimensions: $S^{n-1,m} \in \mathbb{C}^{d \times d \times d}$

Encodes pairwise interactions for boundary variables.

**Control (Identity) Tensor:**
$$C_{i\mu\nu} = \delta_{i\mu}\delta_{\mu\nu} = \begin{cases} 1 & \text{if } i = \mu = \nu \\ 0 & \text{otherwise} \end{cases}$$
Dimensions: $C \in \mathbb{C}^{d \times d \times d}$

Routes indices without modification; enforces index consistency.

**Four-Index Evolution Tensor (Cross Interaction):**
$$S_{i\mu j\nu}^{lm} = e^{-\tau Q_{lm}^{ij}} \quad \text{where } \mu = i, \nu = j$$
Dimensions: $S^{lm} \in \mathbb{C}^{d \times d \times d \times d}$

Encodes two-body interactions between non-adjacent qubits/variables.

## Physical Intuition / Derivation

### Motivation

Tensor networks arise naturally when simulating quantum systems or solving constrained optimization problems (like QUBO—Quadratic Unconstrained Binary Optimization). Instead of storing the full state vector (which scales exponentially), networks decompose the problem into local, manageable chunks.

### Network Construction Logic

1. **Spatial Structure**: Each physical degree of freedom (qubit, variable) corresponds to one or more tensor indices. Variables interact through shared indices.

2. **Temporal Evolution**: Imaginary time evolution $e^{-\tau H}$ decomposes into a product of local operators. Each operator becomes a tensor. The sequence forms a layered network.

3. **Index Naming Convention**:
   - $i, j, k$: physical indices (input/output quantum state)
   - $\mu, \nu$: bond indices (carry information between layers)
   - Index contractions are performed by summation: $\sum_\mu A_{i\mu} B_{\mu j} = (AB)_{ij}$

4. **Superposition Initialization**: The initial state $|+\rangle^{\otimes n}$ (equal superposition) is encoded as tensors with all components equal to 1, ensuring uniform amplitude distribution.

### Why This Structure Works

- **Locality**: Interactions between variables are explicit; non-interacting terms don't share indices.
- **Efficiency**: Rather than exponential full-state representation ($2^n$ amplitudes), the network scales with bond dimension and number of interactions.
- **Composability**: Networks naturally express sequential operations (time steps) as layer concatenation.

## Applications in Engineering

### 1. **Quantum Simulation**
- Simulate quantum many-body systems with temporal dynamics
- Encode Hamiltonian evolution for analog quantum computers
- Study phase transitions and equilibrium properties via imaginary time evolution

### 2. **Optimization & Constraint Solving**
- Encode QUBO problems for quantum annealing and variational algorithms
- Represent penalty Hamiltonians for constraint satisfaction
- Enable hybrid classical-quantum solvers

### 3. **Machine Learning**
- **Tensor network classification**: Discriminative models for structured data
- Represent probability distributions for generative models
- Dimensionality reduction via tensor decomposition

### 4. **Circuit Synthesis**
- Decompose unitary operations into local gate sequences
- Optimize gate count and connectivity constraints
- Design efficient quantum circuits from tensor network templates

### 5. **Classical Simulation of Quantum Algorithms**
- Approximate classical evaluation of variational quantum algorithms (VQA)
- Post-select and analyze quantum circuit behavior
- Validation against classical benchmarks

## Common Mistakes / Pitfalls

### 1. **Index Mismatch**
**Error**: Attempting to contract tensors with incompatible dimension mismatch.
**Correction**: Verify all shared index dimensions match before contraction. Use consistent $d$ (bond dimension) across the network.

### 2. **Confusing Physical vs. Bond Indices**
**Error**: Contracting over physical indices ($i, j$) when you intend to contract bond indices ($\mu, \nu$).
**