# Markov chain mixing

## Definition

**Markov chain mixing** refers to the convergence rate of a Markov chain toward its stationary distribution. A Markov chain is said to **mix rapidly** (or **mix fast**) when it reaches its equilibrium distribution in polynomial time relative to the problem size, making it computationally tractable for sampling and inference tasks.

More formally, for a finite-state Markov chain with transition matrix $P$ and stationary distribution $\pi$, the **mixing time** $\tau_{\text{mix}}(\epsilon)$ is the smallest $t$ such that:

$$\|P^t(x, \cdot) - \pi(\cdot)\|_{\text{TV}} \leq \epsilon$$

for all initial states $x$, where $\|\cdot\|_{\text{TV}}$ denotes total variation distance. The chain exhibits **polynomial mixing** if $\tau_{\text{mix}}(\epsilon) = \text{poly}(n, \log(1/\epsilon))$ where $n$ is the system size.

## Key Equations

### Spectral Gap and Mixing Time

The fundamental connection between spectral properties and mixing:

$$\tau_{\text{mix}}(\epsilon) \leq \frac{\log(1/\epsilon)}{1 - \lambda_2}$$

where $\lambda_2$ is the second-largest eigenvalue of $P$ (the **spectral gap** is $\gamma = 1 - \lambda_2$).

### Influence Matrix and Spectral Independence

For a distribution $\mu$ over $\{0,1\}^V$, the **influence matrix** is:

$$\Psi_\mu(u, v) = \begin{cases}
\Pr[X_v = 1 \mid X_u = 1] - \Pr[X_v = 1 \mid X_u = 0] & \text{if } \mathbb{E}[X_u] \in (0,1), u \neq v \\
0 & \text{otherwise}
\end{cases}$$

A distribution is **$\rho$-spectrally independent** if $\lambda_{\max}(\Psi_\mu) \leq \rho$ for all feasible pinnings $\tau$.

### SI Bound for Antiferromagnetic Systems

For antiferromagnetic two-spin systems on a graph with maximum degree $\Delta$, satisfying uniqueness with slack $\delta \in (0,1)$:

$$\lambda_{\max}(\Psi_{\mu_\tau}) \leq \frac{\Delta(1-\delta)}{(\Delta-1)\delta}$$

This bound is **tight** (optimal up to constant factors).

## Physical Intuition / Derivation

### Why Mixing Matters

Markov chains are foundational tools for sampling from complex distributions in statistical physics and machine learning. However, a chain can be *theoretically correct* yet *computationally useless*—if it takes exponential time to approach equilibrium, we cannot generate reliable samples.

The core question: **How quickly does local information propagate?** When you condition the state of one variable (a "pinning"), does it strongly influence distant variables? If yes, the chain mixes slowly because the state becomes "locked in"; if no, the chain explores freely and mixes quickly.

### Spectral Independence as a Unifying Principle

Spectral independence quantifies local-to-global influence. The influence matrix $\Psi_\mu(u,v)$ measures how strongly conditioning variable $u$ alters the marginal distribution of $v$. A small spectral radius means:

- Variables are "weakly correlated" in a controlled sense
- Local Markov chain moves (like Glauert dynamics) can decorrelate the system efficiently
- Polynomial mixing time follows

For **critical phenomena** (phase boundaries), SI bounds must be tight because mixing time exponents are extremely sensitive to constant factors. A loose bound of $\rho(1 + o(1))$ versus true $\rho$ can hide exponential vs. polynomial behavior.

### Two-Spin Systems and Antiferromagnets

A two-spin system assigns energy to each edge based on the relative spin configuration. Antiferromagnetic interactions ($\beta > 0$ between unlike spins) suppress long-range correlations compared to ferromagnetic cases, aiding mixing. The parameter $\gamma$ relates spin-independent field biases; when $\gamma \leq 1$ or the graph is $\Delta$-regular, structural symmetries permit tighter SI bounds.

The slack $\delta$ encodes how far the system is from a uniqueness threshold—larger $\delta$ means less coupling, better mixing.

## Applications in Engineering

### 1. **Monte Carlo Sampling for Graphical Models**
In probabilistic graphical models (Bayesian networks, Markov random fields), exact inference is NP-hard. Markov chain samplers (Gibbs sampling, Glauert dynamics) enable approximate inference. Rapid mixing guarantees polynomial-time approximation schemes (PTAS) for computing partition functions and marginals in spin systems.

### 2. **Combinatorial Optimization**
Simulated annealing and parallel tempering use Markov chains to explore configuration spaces. Mixing time determines the schedule required to escape local minima; fast mixing enables effective optimization in reasonable wall-clock time.

### 3. **Statistical Physics Simulation**
Simulations of Ising models, hard-core lattice gases, and other interacting particle systems rely on Markov chain solvers. Critical phenomena (phase transitions) are where mixing is slowest; understanding mixing at criticality is essential for reliably measuring critical exponents.

### 4. **Machine Learning: Restricted Boltzmann Machines and Generative Models**
Training generative models by sampling from Gibbs distributions requires efficient samplers. Spectral independence analysis informs the design of accelerated sampling algorithms with provable convergence rates.

### 5. **Network Design and Load Balancing**
Markov chain models for network flows and job scheduling must mix rapidly to ensure transient dynamics don't persist. Spectral gap analysis guides buffer sizing and queueing discipline choices.

## Common Mistakes / Pitfalls

### 1. **Confusing Stationary with Equilibrium**
A Markov chain *always* has a stationary distribution (for finite, irreducible,