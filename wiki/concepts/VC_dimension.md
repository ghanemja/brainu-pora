# VC Dimension

## Definition

**VC dimension** (Vapnik-Chervonenkis dimension) is a fundamental measure of the capacity or complexity of a hypothesis class—the maximum number of points that can be shattered by the class.

A set of points is **shattered** by a hypothesis class $\mathcal{H}$ if, for every possible binary labeling of those points, there exists a hypothesis $h \in \mathcal{H}$ that correctly classifies them. The VC dimension is the size of the largest set that can be shattered; if arbitrarily large sets can be shattered, the VC dimension is infinite.

**Formal definition:** 
$$\text{VC-dim}(\mathcal{H}) = \max\{d : \exists \text{ set } S \text{ with } |S| = d \text{ shattered by } \mathcal{H}\}$$

If no maximum exists, $\text{VC-dim}(\mathcal{H}) = \infty$.

---

## Key Equations

### Relationship to Sample Complexity (PAC Learning)

For **realizable PAC learning** (when the target concept lies in the hypothesis class), the sample complexity bound is:

$$n(\alpha, \beta, \text{VC-dim}) = O\left(\frac{\text{VC-dim} \cdot \log(1/\beta)}{\alpha}\right)$$

where $\alpha$ is the error tolerance and $\beta$ is the failure probability.

### Generalization Error Bound

By the fundamental theorem of statistical learning, the generalization error $\text{err}(h) - \widehat{\text{err}}_S(h)$ is bounded with high probability by:

$$\Pr\left[\sup_{h \in \mathcal{H}} |\text{err}(h) - \widehat{\text{err}}_S(h)| \leq O\left(\sqrt{\frac{\text{VC-dim} \cdot \log(n)}{\beta n}}\right)\right] \geq 1 - \beta$$

This shows that VC dimension directly controls the uniform convergence rate over all hypotheses in the class.

### Growth Function

The **growth function** $\Pi_\mathcal{H}(n)$ counts the maximum number of distinct binary labelings a class $\mathcal{H}$ can induce on any set of $n$ points:

$$\Pi_\mathcal{H}(n) \leq \sum_{i=0}^{d} \binom{n}{i}$$

where $d = \text{VC-dim}(\mathcal{H})$. For $n > d$, this is polynomial in $n$; for $n \leq d$, the growth function can be exponential.

---

## Physical Intuition / Derivation

### Why VC Dimension Matters

VC dimension quantifies **how many independent binary decisions** a model class can make. A larger VC dimension means:
- The hypothesis class is more expressive (more flexible)
- More training data is needed to avoid overfitting
- The class can fit more diverse patterns, but risks memorizing noise

### Intuitive Examples

1. **Linear classifiers in 2D:** VC-dim = 3
   - Any 3 non-collinear points can be shattered by lines
   - Some 4-point configurations cannot be shattered (e.g., vertices of a square cannot all be separated as required)

2. **Threshold functions over finite domain $\{0, 1, \ldots, d\}$:** VC-dim = 1
   - Only a single point can be shattered (any singleton set)
   - The class can only make one binary split, not independent splits at multiple thresholds

3. **Axis-aligned rectangles in 2D:** VC-dim = 4
   - Four points at corners of a square can be shattered
   - Cannot shatter 5 points in general position

### Derivation of Sample Complexity

The connection flows from **shattering** → **growth function** → **uniform convergence** → **sample size**:

1. VC dimension bounds the growth function: if $d = \text{VC-dim}(\mathcal{H})$, then for $n > d$,
   $$\Pi_\mathcal{H}(n) \leq \left(\frac{en}{d}\right)^d$$

2. The growth function bounds the union bound over all hypotheses:
   $$\Pr\left[\exists h : |\text{err}(h) - \widehat{\text{err}}_S(h)| > \epsilon\right] \leq 2 \Pi_\mathcal{H}(2n) e^{-2n\epsilon^2}$$

3. Setting the failure probability to $\beta$ and solving for $n$ gives:
   $$n = O\left(\frac{d \log(1/\epsilon)}{\epsilon^2} + \frac{\log(1/\beta)}{\epsilon^2}\right) = \tilde{O}\left(\frac{d + \log(1/\beta)}{\epsilon^2}\right)$$

---

## Applications in Engineering

### Machine Learning & Statistical Learning Theory

- **Model selection:** VC dimension helps compare hypothesis classes; simpler models (lower VC-dim) generalize better with limited data
- **PAC learning framework:** Guarantees that if VC-dim$({\mathcal{H}}) = d$ is small, a polynomial (in $d$, $1/\alpha$, $\log(1/\beta)$) number of samples suffice
- **Regularization justification:** Penalizing model complexity is equivalent to controlling VC dimension

### Testing & Verification (Algorithmic Soundness)

From the source material on **replicability**, VC dimension directly reduces sample complexity for verified learners:
- Realizable PAC learning over hypothesis classes with VC-dim $= 1$ requires only $\tilde{O}(\log(1/\beta)/\alpha)$ samples
- For threshold functions (VC-dim = 1), replicable algorithms achieve sample complexity:
$$n(\rho, \alpha, \beta) \leq \tilde{O}\