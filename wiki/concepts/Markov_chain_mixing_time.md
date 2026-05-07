# Markov chain mixing time

## Definition

**Mixing time** is the time required for a Markov chain to converge from an arbitrary initial distribution to its stationary distribution $\mu$ within a specified total variation distance.

Formally, for a Markov chain $(X_t)_{t \geq 0}$ with transition matrix $P$ and stationary distribution $\mu$, the **mixing time** is:

$$T_{\text{mix}}(\epsilon) := \inf\{t : \|P^t(x, \cdot) - \mu(\cdot)\|_{\text{TV}} \leq \epsilon \text{ for all } x \in \Omega\}$$

where $\|\cdot\|_{\text{TV}}$ denotes total variation distance. The standard mixing time sets $\epsilon = 1/4$ (though the choice is arbitrary up to logarithmic factors).

In engineering contexts, mixing time quantifies how quickly a system (modeled as a Markov chain) forgets its initial conditions and reaches statistical equilibrium.

---

## Key Equations

### Decay of φ-entropy
A Markov chain satisfies **decay of φ-entropy with rate $\kappa$** if:

$$\text{Ent}_\mu^\phi[Pf] \leq (1 - \kappa)\text{Ent}_\mu^\phi[f]$$

for all functions $f : \Omega \to \mathbb{R}$. The divergence type $\phi$ (e.g., variance, KL divergence, $\chi^2$) determines the convergence guarantee.

### Mixing time bounds from spectral gap
For **reversible chains** with absolute spectral gap $\gamma^*(P)$:

$$T_{\text{mix}} = O\left(\gamma^{*-1} \log \frac{1}{\mu_{\min}}\right)$$

where $\mu_{\min} := \min_{\sigma \in \Omega} \mu(\sigma)$.

### Variance decay implies spectral gap
For reversible chains with decay of variance at rate $\kappa$:

$$\gamma^*(P) \geq \frac{1}{2\kappa}$$

### Entropy decay
If a reversible chain satisfies decay of entropy with rate $\kappa$:

$$T_{\text{mix}} \leq O\left(\kappa^{-1} \log \log \frac{1}{\mu_{\min}}\right)$$

### Approximate tensorization for Glauber dynamics
If a distribution $\mu$ on $\{0,1\}^n$ satisfies **$K$-approximate tensorization of variance**:

$$\text{Ent}_\mu^{\text{Var}}[f(X)] \leq K \sum_{i=1}^n \mathbb{E}\left[\text{Ent}_\mu^{\text{Var}}[f(X) | X_{-i}]\right]$$

then the Glauber dynamics mixing time satisfies:

$$T_{\text{mix}} \leq nK \log \frac{1}{\mu_{\min}}$$

### Spectral independence and influence matrix
The influence matrix entry (for $u \neq v$ with $\mathbb{E}[X_u] \in (0,1)$) is:

$$\Psi_\mu(u,v) := \Pr[X_v = 1 | X_u = 1] - \Pr[X_v = 1 | X_u = 0]$$

A distribution is **$\rho$-spectrally independent** if $\lambda_{\max}(\Psi_\mu^\tau) \leq \rho$ for all feasible pinnings $\tau$.

---

## Physical Intuition / Derivation

### Why mixing time matters

A Markov chain models stochastic processes evolving toward equilibrium. The mixing time answers: *How long must we run the system before it "forgets" where it started?*

**Example**: In Monte Carlo sampling (e.g., simulating a molecular system), we want to draw samples from the stationary distribution $\mu$. If we start with an arbitrary state, we must wait at least $T_{\text{mix}}$ steps before our sample is approximately unbiased.

### Connection to spectral gap

The spectral gap $\gamma^* = 1 - \lambda_2$ (where $\lambda_2$ is the second-largest eigenvalue magnitude) controls the decay rate of the chain. A **larger gap means faster mixing**:

$$\|P^t(x, \cdot) - \mu(\cdot)\|_{\text{TV}} \leq C(1-\gamma^*)^t$$

Thus: $T_{\text{mix}} \sim \gamma^{*-1} \log(1/\epsilon)$.

### Why φ-entropy decay is stronger

Rather than analyzing eigenvalues directly (hard for structured problems), **decay of φ-entropy** provides a functional inequality that propagates through the dynamics:

$$\text{Ent}[f \circ P] \leq (1-\kappa)\text{Ent}[f] \implies \text{Ent}[f \circ P^t] \leq (1-\kappa)^t \text{Ent}[f]$$

The choice of $\phi$ (variance vs. entropy) yields different convergence rates because:
- **Variance decay** → $O(\gamma^{-1} \log(1/\mu_{\min}))$ mixing
- **Entropy decay** → $O(\gamma^{-1} \log \log(1/\mu_{\min}))$ mixing (faster!)

### Approximate tensorization intuition

A product distribution naturally tensorizes: if $\mu = \bigotimes_{i=1}^n \mu_i$, then the entropy of any function decomposes as a sum of conditional entropies. **Approximate tensorization** ($K$-bounded) measures how "close to product" a distribution is. Near-product distributions mix rapidly because variables are nearly independent, reducing the state space effectively.

---

## Applications in Engineering

### 1. Monte Carlo Sampling & MCMC Algorithms
- **Application**: Estimate