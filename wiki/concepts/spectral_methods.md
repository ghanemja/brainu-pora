# Spectral Methods

## Definition

Spectral methods are computational techniques that analyze and solve problems through the lens of **eigenvalues, eigenvectors, and singular values** of matrices. Rather than working directly with a matrix $M$, spectral methods decompose it into its spectral components:

$$M = U \Sigma V^\top$$

where $U$ and $V$ contain the singular vectors and $\Sigma$ contains the singular values. These methods exploit the spectral structure to:

- Identify low-dimensional structure in high-dimensional data
- Solve differential equations via Galerkin projections onto eigenbases
- Perform clustering and dimensionality reduction
- Analyze convergence and stability of algorithms

In the context of matrix perturbation theory, spectral methods rigorously characterize which vectors can be "compressed" (expressed as sparse combinations) and use concentration inequalities to prove that compressible singular vectors are exponentially unlikely under random perturbations.

## Key Equations

**Singular Value Decomposition (SVD):**
$$M = U \Sigma V^\top, \quad U^\top U = I_r, \quad V^\top V = I_r$$

where $r = \text{rank}(M)$, and singular values satisfy $\sigma_1 \geq \sigma_2 \geq \cdots \geq \sigma_r > 0$.

**Spectral norm (operator norm):**
$$\|M\| = \sigma_{\max}(M) = s_{\max}(M)$$

**Minimum singular value:**
$$s_{\min}(M) = \min_{i} \sigma_i(M)$$

**Compressibility condition:** A vector $v$ is *compressible* with parameters $(c_0, c_1)$ if:
$$\|v\|_1 \leq c_0 \sqrt{p} \|v\|_2 \quad \text{and} \quad \|v\|_\infty \leq \frac{c_1}{\sqrt{p}}\|v\|_2$$

where the first bound constrains the $\ell^1$-$\ell^2$ ratio (sparsity proxy) and the second bounds the maximum entry.

**Separation guarantee for singular vectors:** If $u$ is a right singular vector with value $\sigma^2$ for matrix $M = XX^\top YY^\top$ (where $X, Y$ are random), then:
$$\|MM^\top u - \sigma^2 u\| \geq \|v_\parallel\|^2 \cdot (s_{\min}(X)^2 \cdot s_{\min}(Y)^2) + \sigma^4 \|v_\perp\|^2$$

where $v_\parallel$ and $v_\perp$ are projections onto the row spaces of $X$ and orthogonal complement.

## Physical Intuition / Derivation

### Why Spectral Structure Matters

When solving linear systems $Mx = b$ or finding solutions to $Mu = \sigma u$, the eigenspectrum determines:
- **Conditioning:** Problems with small $s_{\min}(M)$ are ill-conditioned
- **Convergence rate:** Determined by the spectral gap (ratio of largest to smallest singular values)
- **Stability:** Perturbations propagate according to the condition number $\kappa(M) = \sigma_{\max}/\sigma_{\min}$

### The Compressible Singular Vector Problem

The source material addresses a fundamental obstruction in high-dimensional statistics: if a singular vector $u$ is "compressible" (sparse or concentrated), standard perturbation bounds may fail. The key insight is:

**Lemma (Informal):** Compressible singular vectors of random matrices are exponentially unlikely. Specifically, if $M$ is a random matrix and $u$ satisfies both:
- Sparsity: $\|u\|_1 \ll \sqrt{p}\|u\|_2$ (few large entries)
- Concentration: $\|u\|_\infty \gg \|u\|_2/\sqrt{p}$ (entries not uniformly distributed)

then with probability $1 - e^{-\Theta(p)}$, there is no eigenvalue $\sigma^2$ such that $M^\top M u = \sigma^2 u$.

**Proof Strategy (Discretization + Union Bound):**
1. Discretize the spectrum: partition possible singular values $\sigma^2 \in [(\sqrt{n}-K\sqrt{p})^2, (\sqrt{n}+K\sqrt{p})^2]$ into a net with spacing $\approx c\sqrt{np}$, yielding $O(K\sqrt{n}/c)$ intervals
2. For each fixed $\sigma^2$, show via eigenvalue separation (Theorems 3.8–3.9) that $\|MM^\top u - \sigma^2 u\| \geq \hat{c}n - c_1\Theta(n) > 0$ with high probability
3. Apply union bound over all $O(2^{H(c_0)n})$ possible supports in the compressibility class
4. Conclude $\mathbb{P}[\text{compressible eigenvector exists}] \leq e^{H(c_0)n} \cdot e^{-\Theta(n)} = e^{-\Theta(n)}$ for small enough $c_0$

The constant $\hat{c}$ is **independent of $c_1$**, so one can shrink $c_1$ arbitrarily to strengthen the result.

## Applications in Engineering

### 1. **Numerical Solution of PDEs**
Spectral methods expand solutions in orthogonal basis functions (e.g., Fourier, Chebyshev) and project the PDE onto a finite-dimensional subspace. The spectral Galerkin method achieves exponential convergence for smooth solutions:
$$u_N(x,t) = \sum_{k=1}^{N} u_k(t) \phi_k(x)$$
where $\{\phi_k\}$ are eigenfunctions.

### 2. **Data Dimension