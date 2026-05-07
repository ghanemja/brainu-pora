# matrix p→q norms

## Definition

A **matrix $p \to q$ norm** is a norm that measures how a linear operator (represented as a matrix) transforms vectors under different $\ell_p$ and $\ell_q$ norms. Formally, given a matrix $A \in \mathbb{R}^{m \times n}$, the $p \to q$ norm is:

$$\|A\|_{p \to q} = \max_{\|x\|_p \leq 1} \|Ax\|_q$$

This is the operator norm (or induced norm) with respect to the $\ell_p$ input norm and $\ell_q$ output norm.

**Special cases:**
- $\|A\|_{2 \to 2}$ is the **spectral norm** (largest singular value)
- $\|A\|_{1 \to \infty}$ is the **maximum absolute row sum**
- $\|A\|_{\infty \to 1}$ is the **maximum absolute column sum**

The matrix $p \to q$ norm captures the worst-case amplification of signals as they pass through a linear transformation, with the amplification measured differently on input and output.

## Key Equations

**Definition via supremum:**
$$\|A\|_{p \to q} = \sup_{\mathbf{x} \neq 0} \frac{\|A\mathbf{x}\|_q}{\|\mathbf{x}\|_p}$$

**Duality relationship** (Hölder's inequality gives):
$$\|A\|_{p \to q} = \|A^T\|_{q' \to p'}$$
where $\frac{1}{p} + \frac{1}{p'} = 1$ and $\frac{1}{q} + \frac{1}{q'} = 1$.

**Vector $\ell_p$ norms** (for reference):
$$\|\mathbf{x}\|_p = \left(\sum_{i=1}^{n} |x_i|^p\right)^{1/p}$$

**Entrywise $\ell_p$ norm** (distinct from operator norm):
$$\|A\|_p^{\text{entrywise}} = \left(\sum_{i,j} |A_{ij}|^p\right)^{1/p}$$

Note: The $p \to q$ norm is an **operator norm** (measures input-output behavior), not an entrywise norm (measures individual entries).

## Physical Intuition / Derivation

### Why Different Norms Matter

In signal processing and control, signals have natural norms reflecting their physical meaning:
- **$\ell_2$ norm**: Energy (root mean square)
- **$\ell_1$ norm**: Total magnitude (sparse signals, errors)
- **$\ell_\infty$ norm**: Peak value (worst-case amplitude)

A matrix $p \to q$ norm answers: *"If I send a signal with bounded $\ell_p$ norm through this system, what's the largest possible $\ell_q$ norm of the output?"*

### Geometric Picture

For $p = q = 2$: The norm equals the largest singular value $\sigma_1(A)$, which represents the maximum stretch applied by $A$ to any unit-norm input vector.

For $p \neq q$: The geometry is more complex. A unit ball in the $\ell_p$ norm has different shape (diamond for $p=1$, sphere for $p=2$, square for $p=\infty$), and the maximum magnification depends on both:
- The directions favored by $A$ (its singular vectors)
- How those directions align with the input norm ball shape
- How the output norm measures the result

### Low-Rank Approximation Connection

The **entrywise low-rank approximation problem** seeks:
$$\min_{\text{rank}(B) \leq k} \|A - B\|_p^{\text{entrywise}}$$

Matrix $p \to q$ norms arise naturally in analyzing approximation algorithms because:
1. They appear in error bounds for reconstruction problems
2. They relate to **small-set expansion** through sum-of-squares relaxations
3. The Sherali-Adams hierarchy (a convex relaxation) provides approximation guarantees in terms of $p \to q$ norms

## Applications in Engineering

### 1. **Signal Processing & Communication**
- Characterize distortion when signals pass through linear channels
- Design robust filters that control amplification across different signal types
- Analyze noise propagation: if noise has bounded $\ell_p$ norm, what $\ell_q$ distortion results?

### 2. **Control Theory**
- Quantify robustness of linear systems to perturbations
- Analyze gain of systems with mixed norm specifications ($H_\infty$ uses $\infty \to \infty$ norm)
- Design controllers minimizing worst-case error under bounded input disturbances

### 3. **Machine Learning & Statistics**
- **Matrix completion**: approximating missing data when low-rank structure exists
- **Robust PCA**: separating low-rank matrices from sparse corruption
- Regularization via entrywise $\ell_p$ norms; operator norms bound generalization

### 4. **Quantum Information Theory**
- Matrix $p \to q$ norms relate to **quantum channel capacity** and **trace norms**
- Quantify information loss through noisy quantum channels
- Used in quantum error correction analysis

### 5. **Numerical Linear Algebra**
- Analyze conditioning of linear systems under different perturbation models
- Bound approximation error in randomized algorithms (sketching, sampling)

## Common Mistakes / Pitfalls

### 1. **Confusing Operator and Entrywise Norms**
**Mistake:** Writing $\|A\|_2$ when you mean the entrywise $\ell_2$ norm (Frobenius norm).

**Reality:** Standard notation $\|A\|_p$ without additional context denotes the $p \to p$ operator norm. Use $\|A\|_F$ for Frobenius (entrywise $\ell_2