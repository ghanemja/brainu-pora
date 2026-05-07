# tensor isomorphism

## Definition

**Tensor isomorphism (TI)** is the computational problem of determining whether two order-$k$ tensors are equivalent under the action of a group $G$ (typically the general linear group $\text{GL}(n)$, orthogonal group $O(n)$, or unitary group $U(n)$).

More formally: Given two tensors $\mathcal{T}, \mathcal{S} \in \mathbb{R}^{n_1 \times n_2 \times \cdots \times n_k}$ (or over $\mathbb{C}$ or finite fields), determine whether there exist group elements $g_1, g_2, \ldots, g_k \in G$ such that:

$$\mathcal{T} = (g_1 \otimes g_2 \otimes \cdots \otimes g_k) \cdot \mathcal{S}$$

The three principal variants are:
- **Tensor Orthogonal Isomorphism (TOI)**: $G = O(n)$ (orthogonal transformations)
- **Tensor Unitary Isomorphism (TUI)**: $G = U(n)$ (unitary transformations)  
- **General Linear Tensor Isomorphism (GLI)**: $G = \text{GL}(n)$ (invertible linear transformations)

## Key Equations

**Tensor-by-tensor contraction action:**
$$[\mathcal{T}]_{i_1 i_2 \cdots i_k} = \sum_{j_1, j_2, \ldots, j_k} g^{(1)}_{i_1 j_1} g^{(2)}_{i_2 j_2} \cdots g^{(k)}_{i_k j_k} [\mathcal{S}]_{j_1 j_2 \cdots j_k}$$

**Wishart ensemble (canonical random tensor model):**
$$W(p, n) = MM^T \quad \text{where } M \in \mathbb{R}^{p \times n}, \; M_{ij} \sim \mathcal{N}(0,1) \text{ i.i.d.}$$

**Higher-Order Singular Value Decomposition (HOSVD) canonical form:**
$$\mathcal{T} = \mathcal{S} \times_1 U^{(1)} \times_2 U^{(2)} \times_k U^{(k)}$$
where $U^{(i)} \in O(n_i)$ and $\mathcal{S}$ is the core tensor.

## Physical Intuition / Derivation

### Why This Problem Matters

Tensor isomorphism captures a fundamental question: **can we transform one data structure into another using only coordinate changes?** This arises naturally in:
- Determining if two experiments measured the same phenomenon in different bases
- Recognizing invariant structure in multilinear data
- Certifying optimality in multilinear optimization

### Complexity Landscape

**Hard cases (worst-case):**
- 3-tensor isomorphism under $\text{GL}(n)$ is NP-hard over finite fields (proven exponential hardness)
- The problem remains open for $\mathbb{R}$ and $\mathbb{C}$ (Open Problem 1)

**Tractable cases (average-case):**
The source material suggests that **3-tensor isomorphism is tractable on average** for:
- Tensor Orthogonal Isomorphism (TOI)
- Tensor Unitary Isomorphism (TUI)

This is because random isotropic tensors (with Haar-distributed transformation matrices) have simpler structure. The orthogonal/unitary constraints eliminate the "wild" behaviors that cause worst-case hardness.

### The Wishart Connection

When tensors have i.i.d. $\mathcal{N}(0,1)$ entries, the marginal spectral properties (eigenvalues and eigenvectors) become tractable:
- Eigenvectors are **Haar distributed** on $O(p)$ and **independent of eigenvalues**
- This structural simplicity is what enables average-case algorithms for TOI/TUI
- The tall case ($n > p$) and square case ($n = p$) have **identical structural conclusions** due to orthogonal invariance

### Smoothed Analysis Perspective

The source material highlights that in practice, tensor spectra may have degeneracies (repeated eigenvalues). A **small perturbation** of tensor entries reliably removes these degeneracies, making the problem simpler. This motivates studying TI under noise—a first step toward understanding when isomorphism-testing is "easy."

## Applications in Engineering

### 1. **Signal Processing & Blind Source Separation**
Tensor isomorphism determines whether two multi-sensor recordings captured the same independent components under unknown mixing. Algorithms for TUI enable efficient identification of unknown basis changes in multidimensional signals.

### 2. **Machine Learning & Deep Learning**
- **Neural network compression**: Detecting equivalent tensor representations across different network architectures
- **Transfer learning**: Verifying whether learned features (stored as tensors) are the same across domains despite different parameterizations
- **Equivariant networks**: Checking structural equivalence of learned feature tensors under group actions

### 3. **Chemoinformatics & Quantum Computing**
- **Molecular orbital comparisons**: Determining if quantum states (represented as tensors) are identical under unitary basis changes
- **Tensor network states**: Verifying equivalence of tensor network representations in quantum simulation algorithms
- **Variational quantum algorithms**: Detecting redundancy in parameterized tensor families

### 4. **Computer Vision**
- **3D shape recognition**: Checking whether two 3D tensor representations of objects are equivalent under orthogonal rotations/reflections
- **Multi-view geometry**: Verifying that tensors from different camera views represent the same scene under coordinate transforms

### 5. **Noncommutative Optimization**
- **Orbit closure intersection (TOCI)**: A foundational problem in polynomial optimization where TUI serves as a subroutine
- **Certifying linear algebra problems**: Detecting equivalent formulations of matrix/tensor decom