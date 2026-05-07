# Low-rank matrix approximation

## Definition

**Low-rank matrix approximation** is the problem of finding a matrix $\hat{A}$ of rank at most $k$ that minimizes the distance (usually Frobenius norm) to a given matrix $A \in \mathbb{R}^{n \times d}$:

$$\hat{A} = \arg\min_{\text{rank}(\tilde{A}) \leq k} \|A - \tilde{A}\|_F$$

The rank-$k$ approximation $A^{(k)}$ is optimal and given by the **truncated singular value decomposition (SVD)**. If $A = U\Sigma V^\top$ with singular values $\sigma_1 \geq \sigma_2 \geq \cdots$, then:

$$A^{(k)} = \sum_{i=1}^{k} \sigma_i u_i v_i^\top$$

where $u_i$ and $v_i$ are the corresponding left and right singular vectors.

### Related Concept: Projection-Cost Preserving Sketch

A matrix $M \in \mathbb{R}^{m \times d}$ is a **(1 + ε)-projection-cost preserving sketch** of $A$ if for all projection matrices $P \in \mathbb{R}^{d \times d}$:

$$(1-\varepsilon)\|A - AP\|_F^2 \leq \|M - MP\|_F^2 \leq (1+\varepsilon)\|A - AP\|_F^2$$

This captures the residual approximation error uniformly across all possible rank-$k$ subspaces.

---

## Key Equations

**Eckart-Young Theorem (optimality of truncated SVD):**
$$\|A - A^{(k)}\|_F = \sqrt{\sum_{i=k+1}^{\min(n,d)} \sigma_i^2}$$

**Rank-one update cost (Frobenius norm):**
$$\|P_t - P_{t-1}\|_F^2 = \|u_2 u_2^\top - u_1 u_1^\top\|_F^2 \leq 4$$
for unit vectors $u_1, u_2$ (generalizes to dimension 8 for 2-dimensional subspace changes).

**Recourse (total change under streaming updates):**
For a stream of $n$ rank-one perturbations maintaining optimal rank-$k$ approximation:
$$\text{Recourse}(P_t, P_{t-1}) \in O(n)$$

**Online coreset size (Theorem 2.6):**
$$|M| = O\left(\frac{k}{\varepsilon^2} \log n \log^2 \kappa\right)$$
where $\kappa$ is the condition number; improves to $O(k\varepsilon^{-2}\log^3 n)$ for poly$(n)$ condition numbers.

**SVD rank-one update time:**
$$T_{\text{update}} = O\left((n+d)k + k^3\right)$$

---

## Physical Intuition / Derivation

### Why Low-Rank Approximation Matters

Real-world matrices often have **hidden low-dimensional structure**. Noise, redundancy, and correlation mean the "true signal" lives on a $k$-dimensional subspace where $k \ll \min(n,d)$. Low-rank approximation recovers this structure by:

1. **Compression**: Represent $n \times d$ matrix with $k(n+d)$ parameters
2. **Denoising**: Remove components orthogonal to signal subspace
3. **Stability**: Improve conditioning by removing small singular values

### Why Truncated SVD is Optimal

The Eckart-Young theorem states that the best rank-$k$ approximation in any unitarily-invariant norm (Frobenius, spectral) is obtained by zeroing singular values $\sigma_{k+1}, \sigma_{k+2}, \ldots$. 

**Intuition**: The SVD orders directions by "importance" (variance). Discarding the smallest $d-k$ directions minimizes total squared reconstruction error.

### Streaming/Dynamic Setting

When data arrives as a stream or the matrix changes via rank-one updates (row insertion, deletion, or modification), maintaining the full SVD is expensive. Instead:

1. **Sketching** reduces the matrix to $O(k/\varepsilon^2 \log^3 n)$ rows via **online ridge leverage sampling**
2. The sketch preserves projection costs—approximation errors on the sketch match those on the original with $(1±\varepsilon)$ multiplicative error
3. Maintain SVD only on the sketch, incurring $O((n+d)k + k^3)$ work per update

---

## Applications in Engineering

### 1. **Data Compression & Storage**
- **Image/video compression**: JPEG uses 2D rank-k approximation of frequency blocks; Netflix uses low-rank approximation of rating matrices for recommendations
- **Scientific data**: Reduce storage of large sensor arrays, simulation outputs

### 2. **Noise Reduction**
- **Signal processing**: Remove high-frequency noise by truncating small singular values
- **Robust PCA**: Decompose matrix into low-rank signal + sparse noise for anomaly detection

### 3. **Dimensionality Reduction**
- **Principal Component Analysis (PCA)**: First $k$ left singular vectors form orthonormal basis of optimal $k$-dimensional subspace
- **Feature extraction**: Reduce data dimension before feeding to downstream ML models

### 4. **Streaming Applications**
- **Real-time analytics**: Maintain approximate rank-$k$ subspace as data streams in (networks, sensors, web logs)
- **Online recommendation systems**: Update low-rank approximation of user-item matrices incrementally
- **Control systems**: Track dominant modes of time-varying dynamical systems

### 5. **Numerical Linear Algebra**
- **Preconditioning**: Low-rank approximation accelerates iterative solvers
- **Matrix completion**: Recover missing entries assuming low-rank structure (Netflix Prize)

---

##