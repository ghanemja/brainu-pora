# singular value decomposition

## Definition

**Singular Value Decomposition (SVD)** is a fundamental matrix factorization that decomposes any $m \times n$ matrix $A$ into a product of three matrices:

$$A = U \Sigma V^T$$

where:
- $U$ is an $m \times m$ orthogonal matrix (columns are left singular vectors)
- $\Sigma$ is an $m \times n$ diagonal matrix with non-negative entries $\sigma_1 \geq \sigma_2 \geq \cdots \geq \sigma_{\min(m,n)} \geq 0$ (singular values)
- $V$ is an $n \times n$ orthogonal matrix (columns are right singular vectors)

The singular values $\{\sigma_i\}$ are the square roots of the eigenvalues of $A^T A$ (or equivalently, $AA^T$). They quantify the "importance" or "energy" associated with each dimension of the data.

## Key Equations

**Optimal Low-Rank Approximation (Eckart-Young Theorem):**

For any target rank $k < r = \text{rank}(A)$, the best rank-$k$ approximation in the Frobenius norm is:

$$A_k = \sum_{i=1}^{k} \sigma_i u_i v_i^T = U_k \Sigma_k V_k^T$$

with approximation error:

$$\|A - A_k\|_F = \sqrt{\sum_{i=k+1}^{r} \sigma_i^2}$$

This is also optimal for the spectral (operator) norm: $\|A - A_k\|_2 = \sigma_{k+1}$.

**Orthogonality Conditions:**

$$U^T U = I_m, \quad V^T V = I_n$$

**Frobenius Norm and Reconstruction:**

$$\|A\|_F^2 = \sum_{i=1}^{\min(m,n)} \sigma_i^2$$

## Physical Intuition / Derivation

SVD can be understood through several complementary perspectives:

### Geometric Interpretation
SVD reveals how a linear transformation $A$ acts on data. The matrix $V$ identifies the principal directions in the input space (data features), $\Sigma$ scales along these directions (importance), and $U$ rotates the result in output space. Any linear map can be visualized as: **rotate** → **scale** → **rotate**.

### Energy Concentration
The singular values decay (in typical real-world data), meaning most information is captured by the first few components. This is why truncating to rank $k$ often works well—the discarded dimensions contain primarily noise.

### Derivation via Eigendecomposition
SVD can be derived by recognizing that:
- $A^T A = V \Sigma^T \Sigma V^T$ (eigendecomposition of the Gram matrix)
- $AA^T = U \Sigma \Sigma^T U^T$ (eigendecomposition of the covariance matrix)

The left singular vectors $U$ are eigenvectors of $AA^T$, and right singular vectors $V$ are eigenvectors of $A^T A$.

### Optimality for $p=2$ Norm
When minimizing entrywise $\ell_2$ norm error $\|A - B\|_2$ over rank-$k$ matrices $B$, the SVD truncation is provably optimal. For $p \neq 2$, the problem becomes non-convex and computationally hard—the source material discusses this hardness and algorithmic approaches using convex hierarchies.

## Applications in Engineering

### 1. **Data Compression & Dimensionality Reduction**
- **Principal Component Analysis (PCA)**: SVD extracts the $k$ directions of maximum variance; used in image compression, feature extraction, and noise reduction.
- **Image processing**: Compress images by keeping only top singular values; reconstruction with 10-20% of components often preserves visual quality.

### 2. **Noise Filtering**
- Distinguish signal from noise by thresholding small singular values
- **Wiener filtering** and robust PCA rely on SVD structure

### 3. **Solving Linear Systems**
- **Pseudoinverse**: $A^+ = V \Sigma^{-1} U^T$ solves least-squares problems $\min_x \|Ax - b\|_2$
- Handles rank-deficient and ill-conditioned systems robustly

### 4. **Control Theory & Stability Analysis**
- Determine controllability and observability via rank properties
- Modal decomposition: singular values relate to natural frequencies and damping

### 5. **Machine Learning**
- **Collaborative filtering**: Factorize user-item matrices to recommend items
- **Latent Semantic Analysis (LSA)**: Uncover hidden topics in text corpora
- **Neural network initialization**: SVD guides weight matrix scaling

### 6. **Signal Processing**
- **Radar/sonar**: Subspace methods for direction of arrival (DoA) estimation (MUSIC, ESPRIT algorithms)
- **Communications**: Channel estimation and equalization

### 7. **Structural Analysis**
- Identify dominant modes and weaknesses in mechanical systems
- Sensitivity analysis for engineering designs

## Common Mistakes / Pitfalls

1. **Assuming SVD solves non-$\ell_2$ problems optimally**
   - SVD is optimal only for Frobenius/spectral norm. For entrywise $\ell_p$ norms with $p \neq 2$, truncated SVD can be far from optimal (see source material).

2. **Ignoring computational cost**
   - Full SVD costs $O(\min(m^2 n, m n^2))$ operations. Use randomized or sketching methods for large matrices.

3. **Not scaling data before PCA**
   - If variables have different units/ranges, standardize before SVD; otherwise large-scale variables dominate.

4. **Rank selection without validation**
   - Choosing $k$ requires problem-specific knowledge (cross-validation, scree plots, domain expertise). No universal rule exists.

5. **Confusing left and right singular vectors**
   