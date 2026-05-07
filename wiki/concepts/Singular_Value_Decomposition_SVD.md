# Singular Value Decomposition (SVD)

## Definition

The Singular Value Decomposition is a fundamental matrix factorization that decomposes any rectangular matrix $A \in \mathbb{R}^{m \times n}$ into three matrices:

$$A = U \Sigma V^T$$

where:
- $U \in \mathbb{R}^{m \times k}$ contains **left singular vectors** (orthonormal columns spanning the column space of $A$)
- $\Sigma \in \mathbb{R}^{k \times k}$ is a diagonal matrix of **singular values** $\sigma_1 \geq \sigma_2 \geq \cdots \geq \sigma_k \geq 0$, ordered in decreasing magnitude
- $V \in \mathbb{R}^{n \times k}$ contains **right singular vectors** (orthonormal columns spanning the row space of $A$)
- $k = \min(m, n)$ is the rank of $A$

The SVD always exists for any matrix over the reals or complex numbers, making it one of the most robust matrix factorizations in numerical linear algebra.

## Key Equations

### Matrix Reconstruction
$$A = \sum_{i=1}^{k} \sigma_i u_i v_i^T$$

where $u_i$ and $v_i$ are the $i$-th columns of $U$ and $V$ respectively.

### Optimal Low-Rank Approximation
The **rank-$r$ truncated SVD** provides the best rank-$r$ approximation in both Frobenius and spectral norms:

$$A_r = \sum_{i=1}^{r} \sigma_i u_i v_i^T = U_r \Sigma_r V_r^T$$

The approximation error is:

$$\|A - A_r\|_F = \sqrt{\sum_{i=r+1}^{k} \sigma_i^2} \quad \text{(Frobenius norm)}$$

$$\|A - A_r\|_2 = \sigma_{r+1} \quad \text{(spectral norm)}$$

### Frobenius Norm
$$\|A\|_F = \sqrt{\sum_{i=1}^{k} \sigma_i^2}$$

### Relationship to Eigendecomposition
For symmetric matrices, the SVD coincides with eigendecomposition: the singular values are the absolute values of eigenvalues, and $U = V$.

## Physical Intuition / Derivation

### Geometric Interpretation

The SVD reveals how a linear transformation $A$ acts on geometric objects:

1. **Right singular vectors** ($V$): An orthonormal basis for the input space, representing the "principal directions" along which $A$ is most sensitive
2. **Singular values** ($\Sigma$): Multiplicative factors indicating how much $A$ stretches or contracts along each principal direction
3. **Left singular vectors** ($U$): The output directions corresponding to maximum variance

When you apply $A$ to data, it:
- Rotates the input via $V^T$
- Stretches along principal axes via $\Sigma$
- Rotates the output via $U$

### Why SVD Finds Optimal Low-Rank Approximations

The truncated SVD $A_r$ is optimal because of the **Eckart-Young theorem**: among all rank-$r$ matrices, $A_r$ minimizes both:
$$\min_{B: \text{rank}(B) \leq r} \|A - B\|_F \quad \text{and} \quad \min_{B: \text{rank}(B) \leq r} \|A - B\|_2$$

This follows from the orthonormality of $U$ and $V$: error in directions we've truncated cannot be compensated by choosing different coefficients.

### Computational Perspective

From the source material, the SVD is leveraged in **streaming algorithms** for dynamic low-rank approximation. The key insight is:

- When the Frobenius norm $\|A(t)\|_F^2$ increases by factor $(1+\varepsilon)$, recomputing SVD provides the optimal rank-$k$ approximation at that time
- Between recomputations, approximation quality degrades by at most $\varepsilon \cdot \|A(t)\|_F^2$ (additive error)
- Total recourse (number of factor updates) is $O\left(\frac{k}{\varepsilon}\log(ndM)\right)$ because the Frobenius norm can only increase by multiplicative $(1+\varepsilon)$ factor $O\left(\frac{1}{\varepsilon}\log(ndM)\right)$ times

## Applications in Engineering

### Data Compression & Dimensionality Reduction
- **Image compression**: Truncated SVD reduces image file size by discarding small singular values while preserving visual quality
- **Principal Component Analysis (PCA)**: Right singular vectors are the principal components; left singular vectors projected onto top-$r$ singular vectors give the reduced representation
- **Feature extraction**: Identify most significant patterns in high-dimensional data

### Signal Processing
- **Noise reduction**: Singular values corresponding to noise (typically the smallest ones) are discarded
- **Spectral analysis**: Identify dominant frequency components and separate signal from noise
- **Channel estimation** in communications: SVD of channel matrix guides precoding/equalization

### Control Systems
- **Balanced realization**: Controllability and observability Gramians are diagonalized via SVD for model reduction
- **H∞ control design**: SVD of sensitivity matrices determines robustness margins
- **Feedback control**: Singular values of sensitivity functions determine stability and disturbance rejection

### Structural Analysis
- **Finite element analysis**: SVD of stiffness matrices identifies rigid body modes and weak directions
- **Buckling analysis**: Singular values of geometric stiffness reveal critical buckling loads

### Machine Learning
- **Collaborative filtering**: Low-rank SVD approximates the user-item rating matrix to predict missing ratings
- **Latent semantic analysis**: SVD of term-document matrix discovers underlying topics
- **Regularization**: Limited-rank SVD prevents overfitting in linear models

### Fluid Dynamics & Control