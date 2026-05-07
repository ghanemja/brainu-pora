# φ-entropy decay

## Definition

**φ-entropy decay** is a property of Markov chains that characterizes the rate at which the φ-divergence of a function's distribution converges to the stationary distribution. Formally:

A Markov chain $(X_t)_{t \geq 0}$ over state space $\Omega$ with transition matrix $P$ and stationary distribution $\mu$ satisfies **decay of φ-entropy with rate $\kappa$** if for all measurable functions $f : \Omega \to \mathbb{R}$:

$$\text{Ent}_\mu^\varphi[Pf] \leq (1-\kappa)\text{Ent}_\mu^\varphi[f]$$

where $\text{Ent}_\mu^\varphi[f]$ denotes the φ-entropy of $f$ under distribution $\mu$.

The choice of divergence function $\varphi$ (e.g., variance, KL divergence, chi-squared) determines the specific notion of convergence being measured.

## Key Equations

### Decay of φ-entropy condition
$$\text{Ent}_\mu^\varphi[Pf] \leq (1-\kappa)\text{Ent}_\mu^\varphi[f]$$

### Spectral gap lower bound (time-reversible chains)
For reversible Markov chains satisfying decay of variance with rate $\kappa$:
$$\gamma_\star(P) \geq \frac{1}{2\kappa}$$
where $\gamma_\star(P)$ is the absolute spectral gap.

### Mixing time bounds
**For decay of variance** ($\varphi(x) = x^2$):
$$T_{\text{mix}} = O\left(\kappa^{-1} \log \frac{1}{\mu_{\min}}\right)$$

**For decay of entropy** ($\varphi(x) = x \log x$):
$$T_{\text{mix}} = O\left(\kappa^{-1} \log \log \frac{1}{\mu_{\min}}\right)$$

where $\mu_{\min} := \min_{\sigma \in \Omega} \mu(\sigma)$ is the minimum stationary probability.

### Approximate tensorization of φ-entropy
A distribution $\mu$ over $\Omega = \{0,1\}^n$ satisfies **$K$-approximate tensorization of φ-entropy** if:
$$\text{Ent}_\mu^\varphi[f(X)] \leq K \sum_{i=1}^n \mathbb{E}\left[\text{Ent}_\mu^\varphi[f(X) \mid X_{-i}]\right]$$

### Glauber dynamics mixing time
For a distribution satisfying $K$-approximate tensorization of variance:
$$T_{\text{mix}} \leq nK \log \frac{1}{\mu_{\min}}$$

## Physical Intuition / Derivation

### Why entropy decay matters

In Markov chain theory, understanding how quickly a chain forgets its initial condition is central. Rather than directly studying the convergence of distributions, φ-entropy decay provides a **functional inequality** that propagates decay information:

- When you apply the transition operator $P$ to a function $f$, the resulting function $Pf$ (which represents averaging $f$ over one step of the chain) has strictly smaller φ-entropy.
- The contraction factor $(1-\kappa)$ directly quantifies the rate: large $\kappa$ means rapid decay (fast mixing), small $\kappa$ means slow decay (slow mixing).

### Connection to spectral properties

For reversible chains, φ-entropy decay relates to spectral properties through:
- **Decay of variance** is the weakest φ-entropy condition and gives the weakest mixing bound (polylogarithmic in $1/\mu_{\min}$)
- **Decay of entropy** is stronger and gives a better bound (only logarithmic in $\log(1/\mu_{\min})$)
- The spectral gap $\gamma_\star(P) = 1 - \lambda_2(P)$ (second-largest eigenvalue magnitude) directly controls variance decay

### Approximate tensorization interpretation

For product distributions $\mu = \bigotimes_{i=1}^n \mu_i$, the φ-entropy tensorizes perfectly ($K=1$) because conditional entropies factorize. When $K > 1$, the distribution is "close to a product" in the sense that:
- Dependencies between coordinates are limited
- The distribution avoids strong correlations
- This enables divide-and-conquer mixing analysis via coordinate-wise updates (Glauert dynamics)

## Applications in Engineering

### 1. **Machine Learning & MCMC Sampling**
   - Analyzing convergence of Gibbs sampling for Bayesian inference in graphical models
   - Validating that posterior distributions mix rapidly (important for Markov chain Monte Carlo)
   - Proving polynomial-time guarantees for approximate inference in graphical models

### 2. **Randomized Algorithms**
   - Analyzing random walk-based algorithms (e.g., for sampling, counting, optimization)
   - Proving that randomized algorithms converge to correct answers in polynomial time
   - Studying metropolis-hastings algorithms for approximate sampling from hard distributions

### 3. **Distributed Computing & Network Algorithms**
   - Analyzing gossip algorithms for information dissemination
   - Studying consensus algorithms where mixing time determines convergence rate
   - Load balancing via random walk protocols

### 4. **Statistical Mechanics & Phase Transitions**
   - Determining when Glauber dynamics efficiently samples from spin systems (Ising, Potts models)
   - Identifying disorder-free regions where rapid mixing is achievable
   - Understanding relationship between temperature and mixing time near critical points

### 5. **Counting and Combinatorial Optimization**
   - FPTAS (fully polynomial-time approximation schemes) for counting problems via Markov chains
   - Proving #P-completeness hardness results via mixing time lower bounds

## Common Mistakes / Pitfalls

### 1. **Confusing decay rate with spectral gap