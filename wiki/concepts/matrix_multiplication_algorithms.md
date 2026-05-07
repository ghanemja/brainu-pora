# Matrix Multiplication Algorithms

## Definition

Matrix multiplication algorithms are computational procedures for computing the product of two matrices. Given matrices $A \in \mathbb{R}^{m \times n}$ and $B \in \mathbb{R}^{n \times p}$, the goal is to compute $C = AB$ where $C \in \mathbb{R}^{m \times p}$.

The fundamental definition is:
$$C_{ij} = \sum_{k=1}^{n} A_{ik} B_{kj}$$

However, different algorithms achieve this computation with vastly different time complexities, memory access patterns, and numerical stability properties. The algorithms range from the naive $O(mnp)$ approach to asymptotically faster methods exploiting algebraic structure.

## Key Equations

### Standard Matrix Multiplication (Naive)
$$C_{ij} = \sum_{k=1}^{n} A_{ik} B_{kj}$$
**Complexity:** $O(n^3)$ for $n \times n$ matrices

### Strassen's Algorithm (1969)
Reduces the exponent of matrix multiplication below 3 by recursive decomposition:

For $n \times n$ matrices divided into $2 \times 2$ blocks:
$$\begin{pmatrix} C_{11} & C_{12} \\ C_{21} & C_{22} \end{pmatrix} = \begin{pmatrix} A_{11} & A_{12} \\ A_{21} & A_{22} \end{pmatrix} \begin{pmatrix} B_{11} & B_{12} \\ B_{21} & B_{22} \end{pmatrix}$$

Strassen computes this using 7 multiplications instead of 8:
$$M_1, \ldots, M_7 = \text{products of linear combinations of blocks}$$

**Complexity:** $O(n^{\log_2 7}) \approx O(n^{2.807})$

### Coppersmith-Winograd & Recent Advances
The current best known exponent $\omega$ satisfies:
$$O(n^{\omega}), \quad \text{where } \omega < 2.372 \text{ (as of 2024)}$$

Recent work (Alman et al., 2025) demonstrates that **asymmetry yields faster algorithms**—exploiting different dimensions of input matrices improves the exponent further.

### Fast Matrix Multiplication Bound
For matrices of dimensions $m \times n$ and $n \times p$:
$$T(m,n,p) = O(mnp / \text{poly}(\log \max(m,n,p)))$$
with careful analysis of cache-oblivious and communication-optimal implementations.

## Physical Intuition / Derivation

### Why Naive Multiplication Is Expensive

The standard triple-nested loop performs $n^3$ scalar multiplications:
```
for i = 1 to n:
    for j = 1 to n:
        for k = 1 to n:
            C[i,j] += A[i,k] * B[k,j]
```

Each of the $n^2$ output elements requires $n$ operations—fundamentally unavoidable when computing the definition. However, algebraic tricks can reduce constant factors and exponents.

### Strassen's Key Insight

The 7 multiplications exploit the following algebraic identity. Define:
$$M_1 = (A_{11} + A_{22})(B_{11} + B_{22})$$
$$M_2 = (A_{21} + A_{22})B_{11}$$
$$\vdots$$
$$M_7 = A_{11}(B_{12} - B_{22})$$

Then:
$$C_{11} = M_1 + M_4 - M_5 + M_7$$
$$C_{12} = M_3 + M_5$$
$$C_{21} = M_2 + M_4$$
$$C_{22} = M_1 - M_2 + M_3 + M_6$$

**Why it works:** By replacing one multiplication with multiple additions (which are cheaper), we reduce total work from $8T(n/2)$ to $7T(n/2)$ at each recursion level. Over $\log_2 n$ levels, this compounds to the improved exponent.

### Why Further Improvements Are Possible

The Coppersmith-Winograd and subsequent algorithms use **higher-order tensors** and properties of bilinear forms. Matrix multiplication is reformulated as computing a trilinear form, and algebraic geometry techniques identify tensor decompositions with fewer multiplicative operations.

## Applications in Engineering

### 1. **Scientific Computing & Simulation**
- Solving large linear systems ($Ax = b$) via iterative methods repeatedly multiplying by $A$
- Finite element analysis and computational fluid dynamics (CFD)
- Structural mechanics for large-scale discretized PDEs

### 2. **Machine Learning & Neural Networks**
- Forward/backward passes in deep learning require billions of matrix multiplications
- GPU implementations of dense matrix multiplication dominate training time
- Techniques like low-rank approximation and quantization build on efficient algorithms

### 3. **Signal Processing**
- Image convolution can be reformulated as matrix multiplication (Winograd convolution)
- Fast Fourier Transforms exploit structure related to matrix factorization
- Beamforming in antenna arrays uses matrix multiplication on complex-valued signals

### 4. **Graph Algorithms**
- Computing powers of adjacency matrices (reachability, shortest paths)
- All-pairs shortest paths via matrix multiplication tricks
- Social network analysis and clustering

### 5. **Control Systems**
- State-space model evolution: $x_{k+1} = Ax_k + Bu_k$ requires repeated matrix multiplications
- Stability analysis through eigenvalue computation (which requires matrix operations)

### 6. **Tensor Computations & Data Processing**
- Mode-$n$ products in tensor decomposition (Tucker, CP decomposition)
- Multi-way data analysis in statistics and machine learning
- Sliding window linear algebra (streaming data algorithms)

## Common Mistakes / Pitfalls

### 1. **Ignoring Cache Locality**
- Naive algorithms have poor memory access patterns
- The simple row