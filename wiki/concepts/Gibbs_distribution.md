# Gibbs Distribution

## Definition

A **Gibbs distribution** is a probability distribution over configurations of a system that describes the equilibrium state of a statistical mechanical system at thermal equilibrium. For a discrete system with configuration space and energy function $E(\sigma)$, the Gibbs distribution assigns probability:

$$\mu(\sigma) = \frac{1}{Z} \exp\left(-\beta E(\sigma)\right)$$

where:
- $\sigma$ is a configuration (state) of the system
- $\beta = 1/(k_B T)$ is the inverse temperature (with Boltzmann constant $k_B$ and absolute temperature $T$)
- $Z = \sum_{\sigma} \exp(-\beta E(\sigma))$ is the **partition function** (normalization constant)

The Gibbs distribution is also called the **Boltzmann distribution** in statistical mechanics contexts.

### Generalized Form

In more abstract settings (e.g., combinatorial systems), the Gibbs distribution on a graph $G = (V, E)$ takes the form:

$$\mu(\sigma) = \frac{1}{Z} \prod_{(u,v) \in E} w(u,v; \sigma_u, \sigma_v) \prod_{v \in V} \lambda_v(\sigma_v)$$

where $w(u,v; \sigma_u, \sigma_v)$ are edge weights (potentials) and $\lambda_v(\sigma_v)$ are vertex weights, with partition function $Z = \sum_{\sigma} \prod_{(u,v)} w(u,v; \sigma_u, \sigma_v) \prod_v \lambda_v(\sigma_v)$.

## Key Equations

### Partition Function and Free Energy

$$Z(\beta) = \sum_{\sigma} \exp(-\beta E(\sigma))$$

The **Helmholtz free energy** is related to the partition function by:
$$F(\beta) = -\frac{1}{\beta} \ln Z(\beta)$$

### Marginal Distribution

For a subset $\Lambda \subseteq V$ with pinning $\tau \in \{0,1\}^{\Lambda}$, the conditional (pinned) distribution is:

$$\mu_{\Lambda}(\tau) = \frac{1}{Z_{\Lambda}} \prod_{(u,v) \in E} w(u,v; \tau_u, \tau_v) \prod_{v \in \Lambda} \lambda_v(\tau_v)$$

when the pinning is feasible (i.e., $\mu_{\Lambda}(\tau) > 0$).

### Influence Matrix

For a binary distribution $\mu$ on $\{0,1\}^V$, the **influence matrix** quantifies conditional dependence:

$$\Psi_{\mu}(u, v) = \begin{cases}
\Pr[X_v = 1 \mid X_u = 1] - \Pr[X_v = 1 \mid X_u = 0] & \text{if } u \neq v \text{ and } \mathbb{E}[X_u] \in (0,1) \\
0 & \text{otherwise}
\end{cases}$$

A distribution is **$\rho$-spectrally independent** if $\lambda_{\max}(\Psi_{\mu_\tau}) \leq \rho$ for all feasible pinnings $\tau$.

## Physical Intuition / Derivation

### Maximum Entropy Principle

The Gibbs distribution is the unique probability distribution that:
1. Has fixed expected energy $\langle E \rangle$
2. Maximizes entropy $S = -\sum_\sigma \mu(\sigma) \ln \mu(\sigma)$

This principle explains *why* systems at equilibrium follow Gibbs distributions—they represent the most "random" distribution consistent with observed energy constraints.

### Temperature Effects

- **Low temperature** ($\beta \to \infty$): The distribution concentrates on minimum-energy configurations; the system "freezes"
- **High temperature** ($\beta \to 0$): The distribution approaches uniform; thermal noise dominates
- **Critical temperature**: Phase transitions often occur where the structure of the Gibbs distribution qualitatively changes

### Connection to Markov Chains

Glauert dynamics (a local MCMC sampler) has the Gibbs distribution as its stationary distribution. The rate at which the chain converges to $\mu$ governs computational efficiency for sampling and inference.

## Applications in Engineering

### 1. **Statistical Mechanics & Materials Science**
- Computing equilibrium properties of magnetic materials (Ising models, spin glasses)
- Phase transition analysis in ferromagnetic and antiferromagnetic systems
- Predicting material behavior at different temperatures

### 2. **Computational Statistics & Machine Learning**
- **Markov Random Fields (MRFs)**: Gibbs distributions are the canonical form for MRFs in graphical models
- **Bayesian inference**: Prior and posterior distributions in probabilistic models
- **Sampling algorithms**: Gibbs sampling is a foundational MCMC technique for drawing samples from complex distributions

### 3. **Combinatorial Optimization**
- Simulated annealing: Uses Gibbs distributions with decreasing temperature to minimize cost functions
- Constraint satisfaction: Modeling feasible configurations with energies encoding constraint violations

### 4. **Network & System Design**
- **Spectral independence analysis**: Understanding mixing time of sampling algorithms; critical for designing efficient randomized algorithms for graph coloring, matching, and other combinatorial problems
- **Information theory**: Relating concentration properties to computational complexity

### 5. **Critical Phenomena Analysis**
- Detecting and characterizing phase transitions in complex systems
- Analyzing behavior near criticality (where standard approximations fail)

## Common Mistakes / Pitfalls

### 1. **Confusing $\beta$ with Temperature**
Students often forget that $\beta = 1/(k_B T)$, so *higher* $\beta$ means *lower* temperature. At $\beta = 0$, the distribution is uniform; as $\beta \to \infty$, it concentrates on low-energy states.

### 2. **Ignoring the Partition Function**
The partition function $Z$ is essential: omitting it makes the distribution unnormalized. Computing