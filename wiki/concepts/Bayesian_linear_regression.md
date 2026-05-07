# Bayesian Linear Regression

## Definition

**Bayesian linear regression** is a probabilistic approach to linear regression that treats the regression coefficients as random variables with prior distributions. Rather than computing point estimates of parameters, it derives a **posterior distribution** over parameters given the observed data, enabling principled uncertainty quantification, prediction intervals, and incorporation of prior knowledge.

Formally, given data $\{(\mathbf{x}_i, y_i)\}_{i=1}^n$ where $\mathbf{x}_i \in \mathbb{R}^d$ are inputs and $y_i \in \mathbb{R}$ are outputs, the model assumes:

$$y_i = \mathbf{w}^\top \mathbf{x}_i + \epsilon_i$$

where $\mathbf{w} \in \mathbb{R}^d$ is the coefficient vector and $\epsilon_i \sim \mathcal{N}(0, \sigma^2)$ is Gaussian noise.

Bayesian linear regression specifies:
- **Prior:** $p(\mathbf{w}) = \mathcal{N}(\mathbf{w}; \mathbf{0}, \Sigma_0)$ (typically, though other priors are possible)
- **Likelihood:** $p(y_i | \mathbf{x}_i, \mathbf{w}) = \mathcal{N}(y_i; \mathbf{w}^\top \mathbf{x}_i, \sigma^2)$
- **Posterior:** $p(\mathbf{w} | \mathcal{D})$ derived via Bayes' rule

The key distinction from frequentist regression is that parameters are **random variables**, not fixed unknowns.

---

## Key Equations

### Posterior Distribution (Closed Form)

For a Gaussian prior $\mathbf{w} \sim \mathcal{N}(\mathbf{0}, \Sigma_0)$ and Gaussian likelihood, the posterior is also Gaussian:

$$p(\mathbf{w} | \mathcal{D}) = \mathcal{N}(\mathbf{w}; \boldsymbol{\mu}_N, \Sigma_N)$$

where the posterior mean and covariance are:

$$\Sigma_N = \left(\Sigma_0^{-1} + \frac{1}{\sigma^2}\mathbf{X}^\top\mathbf{X}\right)^{-1}$$

$$\boldsymbol{\mu}_N = \Sigma_N \left(\Sigma_0^{-1}\mathbf{0} + \frac{1}{\sigma^2}\mathbf{X}^\top\mathbf{y}\right) = \frac{1}{\sigma^2}\Sigma_N \mathbf{X}^\top\mathbf{y}$$

where $\mathbf{X} \in \mathbb{R}^{n \times d}$ is the design matrix and $\mathbf{y} \in \mathbb{R}^n$ is the response vector.

### Special Case: Zero-Mean Prior with $\Sigma_0 = \lambda^{-1}\mathbf{I}$

$$\Sigma_N^{-1} = \lambda \mathbf{I} + \frac{1}{\sigma^2}\mathbf{X}^\top\mathbf{X}$$

$$\boldsymbol{\mu}_N = \frac{1}{\sigma^2}\Sigma_N \mathbf{X}^\top\mathbf{y}$$

This posterior mean is equivalent to the ridge regression estimator with regularization parameter $\lambda\sigma^2$.

### Predictive Distribution

The posterior predictive distribution for a new input $\mathbf{x}_*$ is:

$$p(y_* | \mathbf{x}_*, \mathcal{D}) = \mathcal{N}(y_*; \boldsymbol{\mu}_*, \sigma_*^2)$$

where:

$$\boldsymbol{\mu}_* = \boldsymbol{\mu}_N^\top \mathbf{x}_*$$

$$\sigma_*^2 = \sigma^2 + \mathbf{x}_*^\top \Sigma_N \mathbf{x}_*$$

The second term in $\sigma_*^2$ captures **epistemic uncertainty** (uncertainty due to parameter uncertainty); the first term is **aleatoric uncertainty** (irreducible noise).

### Log-Marginal Likelihood (Model Evidence)

$$\log p(\mathcal{D}) = -\frac{1}{2\sigma^2}\|\mathbf{y}\|^2 + \frac{1}{2}\boldsymbol{\mu}_N^\top\Sigma_N^{-1}\boldsymbol{\mu}_N - \frac{1}{2}\log\det(2\pi\Sigma_N)$$

This is used for hyperparameter optimization (e.g., selecting $\lambda$ or $\sigma^2$) and model comparison.

---

## Physical Intuition / Derivation

### Why Bayesian Regression?

**Traditional least-squares regression** minimizes $\|\mathbf{y} - \mathbf{X}\mathbf{w}\|^2$, yielding a point estimate. This has limitations:

1. **No uncertainty quantification:** How confident are we in predictions?
2. **No principled regularization:** Ridge regression appears ad-hoc without probability framework
3. **No prior knowledge incorporation:** How do we leverage domain expertise?
4. **Overfitting:** No automatic complexity penalization

**Bayesian regression addresses all of these** by:
- Maintaining a **distribution** over parameters, not a point estimate
- Computing full posterior $p(\mathbf{w}|\mathcal{D})$
- Using prior $p(\mathbf{w})$ to encode regularization
- Computing **credible intervals** for parameters and **prediction intervals** for future observations

### Derivation via Bayes' Rule

Starting with Bayes' theorem:

$$p(\mathbf{w} | \mathcal{D