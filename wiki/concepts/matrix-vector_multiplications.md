# Matrix-Vector Multiplications

## Definition

A **matrix-vector multiplication** is a fundamental linear algebra operation where a matrix $A \in \mathbb{R}^{m \times n}$ multiplies a vector $\mathbf{v} \in \mathbb{R}^{n}$ to produce an output vector $\mathbf{b} \in \mathbb{R}^{m}$:

$$\mathbf{b} = A\mathbf{v}$$

In the context of tensor network contraction (particularly relevant for quantum optimization problems), matrix-vector multiplications serve as an efficient computational primitive for contracting high-dimensional tensor networks by reformulating rank-4 tensors as matrices. This approach leverages highly optimized linear algebra libraries and reduces algorithmic complexity through structured contraction schemes.

## Key Equations

**Standard matrix-vector product:**
$$b_i = \sum_{j=1}^{n} A_{ij} v_j \quad \text{for } i = 1, \ldots, m$$

**Computational complexity (naive):** $O(mn)$ scalar multiplications

**In tensor contraction context** (sparse tensors with $k$ neighbor interactions):
- Matrix dimension: $d^k \times d^k$ (where $d$ is physical dimension, $k$ is degree)
- Single multiplication cost: $O(d^{k+1})$ operations (accounting for sparsity)
- Full chain contraction (n multiplications): $O(nd^{k+1})$ operations per variable
- Total with reuse of intermediates: $O(nd^{k+1})$ vs. $O(n^2d^{k+1})$ without reuse

**Stair-structured tensor networks:**
$$\text{Complexity} = \begin{cases}
O(nd^2) & \text{if } k=1 \\
O(nd^3) & \text{if } k=2 \\
O(nkd^k) & \text{if } k \geq 3
\end{cases}$$

## Physical Intuition / Derivation

### Why Convert Tensors to Matrices?

Tensor networks naturally arise in quantum optimization (QUDO) and statistical mechanics problems. A rank-4 tensor with structure:
$$T_{i,j,\alpha,\beta}$$
encodes interactions between neighbors. However, directly contracting tensor networks requires specialized algorithms.

**Key insight:** Reshape the tensor into a matrix by grouping indices:
- Physical indices: combined into composite rows/columns
- Bond indices: encoded as matrix dimensions

For a tensor $M_3$ with 6 indices (say, 3 pairs of input-output), create a matrix $N_3$ of dimension $d^3 \times d^3$.

### Why This Helps

1. **Library optimization:** Standard BLAS (Basic Linear Algebra Subprograms) operations on matrices are heavily optimized in hardware
2. **Sparsity exploitation:** Many tensors in constraint problems are sparse (constraints couple only subsets of variables), meaning $k-1$ pairs have repeated indices
3. **Reuse of intermediates:** Once a row of tensors is contracted into a matrix-vector pair, subsequent contractions require only $O(d^2)$ work per variable instead of recomputing from scratch

### Contraction Strategy

For a tensor chain, the contraction sequence is:
$$\text{Vector}_1 \xrightarrow{\times M_1} \text{Vector}_2 \xrightarrow{\times M_2} \cdots \xrightarrow{\times M_n} \text{Result}$$

Each step: $\text{Vector}_{i+1} = M_i \cdot \text{Vector}_i$

## Applications in Engineering

### 1. **Quantum Optimization & QUDO Algorithms**
- Computing variable assignments in quantum optimization problems with low-connectivity constraints
- Solving with $O(nd^{k+1})$ complexity instead of exponential scaling

### 2. **Graphical Model Inference**
- Belief propagation and message passing algorithms
- Marginal probability computation in factor graphs with bounded degree

### 3. **Tensor Network Simulations**
- Matrix Product States (MPS) and tensor train decompositions
- Efficient simulation of low-entanglement quantum systems
- Classical simulation of quantum circuits with limited interactions

### 4. **Scientific Computing**
- Finite element assembly (sparse matrix-vector products are the kernel operation)
- Iterative linear solvers (GMRES, CG) rely entirely on efficient matrix-vector multiplications
- Preconditioner applications in computational physics

### 5. **Machine Learning**
- Neural network inference: forward pass is sequence of matrix-vector multiplications
- Kernel methods with sparse kernel matrices
- Dimensionality reduction in high-dimensional spaces

## Common Mistakes / Pitfalls

### 1. **Ignoring Sparsity Structure**
❌ **Mistake:** Treating a sparse tensor as dense, performing $O(d^{2k})$ operations instead of $O(d^{k+1})$

✓ **Correct approach:** Exploit sparse index patterns; only iterate over non-zero entries

### 2. **Forgetting Dimension Mismatch**
❌ **Mistake:** Attempting to multiply $A \in \mathbb{R}^{m \times n}$ by $\mathbf{v} \in \mathbb{R}^{p}$ where $n \neq p$

✓ **Correct approach:** Verify conformability: $A_{m \times n} \cdot \mathbf{v}_{n} \rightarrow \mathbf{b}_{m}$

### 3. **Not Reusing Intermediate Computations**
❌ **Mistake:** Contracting tensor chains independently for each variable, scaling as $O(n^2d^{k+1})$

✓ **Correct approach:** Cache intermediate vectors and reuse across variables (single contraction pass)

### 4. **Underestimating Memory Cost**
❌ **Mistake:** Assuming time complexity $O(nd^{k+1})$ implies memory is negligible

✓ **Correct approach:** Space complexity is $O(nd^{k+1})$ (must store intermediate contracted tensors), which can dom