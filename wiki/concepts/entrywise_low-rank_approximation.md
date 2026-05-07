# entrywise low-rank approximation

## Definition

**Entrywise low-rank approximation** is the problem of finding the best rank-$k$ approximation to a matrix $A$ under the entrywise $\ell_p$ norm:

$$B^* = \operatorname{argmin}_{\text{rank}(B) \leq k} \|A - B\|_p$$

where the entrywise $\ell_p$ norm is defined as:

$$\|M\|_p = \left(\sum_{i,j} |M_{ij}|^p\right)^{1/p}$$

This is **distinct** from the Frobenius norm ($p=2$) or spectral norm ($p=\infty$) approaches, which have well-understood solutions via the singular value decomposition (SVD).

### Problem Variants

The problem generalizes to:
- **Matrix $p \to q$ norms**: Minimize $\|Ax\|_q$ over unit vectors in $\ell_p$ norm
- **Bi-criteria approximation**: Allow relaxation of rank constraint while approximating the objective
- **Additive approximation**: Guarantee solution within additive error $\varepsilon \cdot \|A\|_p$

---

## Key Equations

**Entrywise $\ell_p$ norm definition:**
$$\|M\|_p = \left(\sum_{i=1}^{m}\sum_{j=1}^{n} |M_{ij}|^p\right)^{1/p}$$

**Low-rank approximation objective:**
$$\min_{\text{rank}(B) \leq k} \|A - B\|_p$$

**SVD baseline (for $p=2$):**
$$\|A - A_k\|_2 = \sigma_{k+1}$$
where $A_k$ is the rank-$k$ truncated SVD and $\sigma_{k+1}$ is the $(k+1)$-th singular value.

**Approximation guarantee for $p > 2$ (prior work):**
$$\|A - B\|_p \leq (3 + \varepsilon) \min_{\text{rank}(B) \leq k} \|A - B\|_p$$

**Matrix $p \to q$ norm:**
$$\|A\|_{p \to q} = \max_{\|x\|_p = 1} \|Ax\|_q$$

---

## Physical Intuition / Derivation

### Why $p=2$ is Easy

For $p=2$, the Frobenius norm is **rotationally invariant** and convex in the entries. The SVD provides an optimal closed-form solution because:

1. The problem decomposes across singular components
2. Truncating at rank-$k$ simply zeros out the smallest singular values
3. No combinatorial search is needed

### Why $p \neq 2$ is Hard

For $p \neq 2$:

- **Non-convexity in rank constraint**: Rank is a discrete, non-convex constraint
- **Entry-level penalties**: The $\ell_p$ norm treats individual residuals nonlinearly:
  - For $p < 2$: Large errors penalized less (robust to outliers)
  - For $p > 2$: Large errors penalized more (sensitive to outliers)
- **No greedy optimality**: Removing a small-singular-value direction may not reduce the $\ell_p$ error monotonically
- **Lack of separation of variables**: Unlike Frobenius norm, you cannot optimize row-by-row or column-by-column independently

### Sherali-Adams Hierarchy Approach

Rather than combinatorial search or sketching, the algorithm:

1. **Relaxes the rank constraint** into a convex constraint via the Sherali-Adams (SA) hierarchy—a family of progressively tighter semidefinite programming (SDP) relaxations
2. **Solves the SDP** to obtain a fractional solution
3. **Rounds the fractional solution** using a **global correlation rounding** technique that respects the $\ell_p$ norm structure
4. **Extracts a low-rank matrix** from the rounded solution with controlled approximation loss

This avoids explicit enumeration of rank-$k$ matrices and bypasses the limitations of column selection methods.

---

## Applications in Engineering

### 1. **Signal Processing & Compressed Sensing**
- Recovering signals corrupted by different noise models ($p < 2$ for heavy-tailed noise, $p > 2$ for Gaussian)
- Robust PCA variants using entrywise norms instead of nuclear norm

### 2. **Machine Learning & Data Mining**
- **Robust matrix completion** under non-Gaussian noise
- **Outlier-resistant dimensionality reduction** for high-dimensional datasets with anomalies
- Learning latent factor models when standard MSE is inappropriate

### 3. **Control Theory & System Identification**
- Approximating high-order linear systems with lower-order models under $\ell_p$ error metrics
- Robust identification when measurement noise is non-Gaussian

### 4. **Quantum Information Theory**
- Matrix $p \to q$ norms relate to operational bounds in quantum state discrimination
- Characterizing quantum channel capacity under different information-theoretic norms

### 5. **Image & Video Compression**
- Rank reduction with robustness to salt-and-pepper noise ($p = 1$) or Gaussian noise ($p = 2$)
- Separating low-rank background from sparse foreground in video analysis

### 6. **Network Analysis & Graph Processing**
- Low-rank approximation of adjacency matrices under metrics robust to measurement errors

---

## Common Mistakes / Pitfalls

### 1. **Assuming SVD Optimality for All $p$**
❌ *Mistake*: Using truncated SVD and expecting it solves entrywise low-rank for $p \neq 2$

✓ *Correction*: SVD is only optimal for the Frobenius norm. For $p \neq 2$, use problem-specific algorithms.

### 2. **Confusing Norms**
❌ *Mistake