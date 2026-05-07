# Tensor Contraction

## Definition

**Tensor contraction** is a fundamental operation in tensor algebra that reduces the rank of a tensor by summing over pairs of specified indices. Given a tensor $T$ with indices $i_1, i_2, \ldots, i_n$, contracting indices $i_a$ and $i_b$ (where $i_a$ and $i_b$ have the same dimension) produces a new tensor with rank reduced by 2.

Formally, for a tensor $T$ of shape $(d_1, d_2, \ldots, d_n)$, contracting indices $i_a$ and $i_b$ yields:

$$C_{i_1 \ldots \hat{i_a} \ldots \hat{i_b} \ldots i_n} = \sum_{k=1}^{d} T_{i_1 \ldots k \ldots k \ldots i_n}$$

where $\hat{i_a}$ denotes the omitted index and $d$ is the shared dimension of indices $i_a$ and $i_b$.

**Special cases:**
- **Full contraction** (scalar product): contracting all indices of a tensor yields a scalar
- **Partial contraction**: contracting only some index pairs, leaving others free
- **Matrix trace**: contraction of a $2^{\text{nd}}$-order tensor (matrix) along its two indices: $\text{tr}(M) = \sum_i M_{ii}$
- **Vector dot product**: contraction of two rank-1 tensors: $\langle u, v \rangle = \sum_i u_i v_i$

## Key Equations

**General tensor contraction formula:**

$$C = \sum_{i,j,\ldots} T_1^{(1)}(i,j,\ldots) \cdot T_2^{(2)}(j,k,\ldots)$$

For a 4-order tensor contraction (as used in QUBO tensor network algorithms):

$$R_{i_3, i_4} = \sum_{i_1, i_2} T^{(1)}_{i_1, i_2, i_3} \cdot T^{(2)}_{i_1, i_2, i_4}$$

**Einstein summation notation** (compact form):
$$C_{ik} = A_{ij} B_{jk} \quad \Rightarrow \quad \text{einsum('ij,jk->ik', A, B)}$$

**Computational complexity** for contracting tensors of orders $n_1$ and $n_2$ with shared indices:
$$\mathcal{O}(d^{n_1 + n_2 - 2c})$$
where $d$ is the typical dimension size and $c$ is the number of contracted indices.

## Physical Intuition / Derivation

### Why Contraction Matters

Tensor contraction is the natural generalization of matrix multiplication and dot products to higher-dimensional arrays. It captures the idea of "overlapping" shared indices and summing over their combinations.

**Intuitive picture:** Imagine a 3D tensor $T_{ijk}$ as a collection of 2D matrices stacked along a third dimension. Contracting indices $i$ and $j$ with another tensor creates a weighted superposition, effectively reducing the data structure's dimensionality while preserving relevant information.

### Connection to Tensor Networks

In tensor network diagrams:
- Each tensor is a node (or vertex)
- Each index is an edge
- **Contraction** corresponds to connecting two edges and summing over their shared indices

For example, contracting two rank-3 tensors $A_{ijk}$ and $B_{jkl}$ along indices $j$ and $k$:

$$C_{il} = \sum_{j,k} A_{ijk} B_{jkl}$$

visually represents merging two nodes via shared edges.

### Derivation from Index Notation

Starting with explicit summation:
$$C_{il} = \sum_{j=1}^{d_j} \sum_{k=1}^{d_k} A_{ijk} B_{jkl}$$

Contracted indices ($j$ and $k$) become **dummy variables**—they appear exactly twice (once in each tensor) and are summed over. Free indices ($i$ and $l$) appear exactly once and become dimensions of the output tensor.

## Applications in Engineering

### 1. **Combinatorial Optimization (QUBO/QUDO)**
Tensor contraction enables efficient computation of cost functions in quadratic unconstrained optimization via tensor network algorithms. The method contracts tensors representing constraint interactions, reducing the problem dimensionality iteratively.

### 2. **Quantum Computing & Simulation**
- **PEPS (Projected Entangled Pair States)**: Contracting boundary MPSs to compute expectation values
- **MPS (Matrix Product States)**: Contracting along the chain to compute observables or free energy
- **Ground state simulation**: Imaginary time evolution relies on repeated contractions

### 3. **Machine Learning & Neural Networks**
- **Tensor decomposition**: Contracting CP or Tucker decompositions for dimensionality reduction
- **Graph neural networks**: Aggregating neighbor information via contractions
- **Attention mechanisms**: Softmax-weighted contractions in transformer architectures

### 4. **Physics Simulations**
- **Lattice gauge theories**: Computing partition functions via tensor network contraction
- **Condensed matter**: Computing correlation functions in spin systems
- **Quantum field theory**: Numerical evaluation of path integrals using tensor methods

### 5. **Signal Processing & Image Analysis**
- **Multi-way ANOVA**: Contracting design tensors with observation tensors
- **Spectral analysis**: Computing mode projections in multi-modal data
- **Compressed sensing**: Dictionary learning via tensor contractions

### 6. **Sparse Computation Optimization**
The "Waterfall" technique mentioned in source material exploits sparsity patterns during contraction, dramatically reducing computational cost in k-neighbor interactions by avoiding explicit enumeration of zero elements.

## Common Mistakes / Pitfalls

### 1. **Index Dimension Mismatch**
**Error:** Attempting to contract indices with different dimensions
```python
# ❌ WRONG: A has shape