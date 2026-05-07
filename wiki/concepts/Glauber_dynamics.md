# Glauber dynamics

## Definition

**Glauert dynamics** is a Markov chain Monte Carlo (MCMC) algorithm for sampling from Gibbs distributions (equilibrium distributions of statistical mechanics systems). At each step, the chain selects a variable uniformly at random and resamples it conditioned on the current state of all other variables.

More formally, for a system with state space $\Sigma$ and target distribution $\pi$ (a Gibbs measure), the transition kernel $P$ performs:
- Select a coordinate $i \in [n]$ uniformly at random
- Resample $\sigma_i \sim \pi(\cdot | \sigma_{-i})$ where $\sigma_{-i}$ denotes all coordinates except $i$

This creates a reversible Markov chain with stationary distribution $\pi$. The algorithm is fundamental because it naturally respects the conditional independence structure of graphical models and is guaranteed to converge to the target distribution.

## Key Equations

**Mixing time definition:**
$$\tau_{\text{mix}}(\epsilon) = \min\{t : \|P^t(\sigma, \cdot) - \pi(\cdot)\|_{\text{TV}} \leq \epsilon \text{ for all } \sigma \in \Sigma\}$$

where $\|\cdot\|_{\text{TV}}$ denotes total variation distance.

**Spectral gap and exponential mixing:**
$$\tau_{\text{mix}}(\epsilon) = O\left(\frac{\log(1/\epsilon)}{1 - \lambda_2}\right)$$

where $\lambda_2$ is the second-largest eigenvalue of the transition matrix $P$. A large spectral gap (small $\lambda_2$) ensures **rapid mixing** (polynomial in system size and $\log(1/\epsilon)$).

**Conductance (Cheeger inequality):**
$$\Phi = \min_{S: \pi(S) \leq 1/2} \frac{P(S \to S^c)}{\pi(S)}$$

relates the conductance $\Phi$ to mixing time: $\tau_{\text{mix}}(\epsilon) = O(\Phi^{-2} \log(1/\epsilon))$.

## Physical Intuition / Derivation

Glauber dynamics models **local relaxation** in physical systems. Each coordinate attempts to equilibrate with its neighbors, mirroring how real materials reach thermal equilibrium through local interactions.

**Why it works:**
1. **Locality**: Only one variable is updated per step, reflecting local dynamics in physical systems
2. **Balance**: The transition probabilities satisfy detailed balance with respect to $\pi$, guaranteeing convergence to equilibrium
3. **Implementability**: Easy to sample from local conditional distributions, especially for graphical models

**Critical regimes:**
- **Unique phase (low temperature/density)**: The system has a unique Gibbs measure. Here, local information doesn't propagate globally, leading to **rapid mixing** (polynomial in $n$)
- **Critical threshold**: At phase transitions, correlation length diverges. Mixing time typically exhibits a **power-law** behavior (e.g., $O(n^{1/4})$ for 2D Ising)
- **Non-unique phase**: Multiple Gibbs measures coexist. Glauert dynamics becomes **torpidly mixing** unless NP = RP (presumed intractable)

The source material indicates a recent breakthrough: **spectral independence** and **high-dimensional expander** techniques now prove rapid mixing up to and even at critical thresholds for broad classes of systems (antiferromagnetic two-spin systems, hardcore model, zero-field Ising).

## Applications in Engineering

### Computational Statistics
- **Bayesian inference**: Sampling from posterior distributions in machine learning (probabilistic graphical models, Bayesian neural networks)
- **Parameter estimation**: MCMC samplers for latent variable models in engineering design and optimization

### Statistical Physics Simulation
- **Monte Carlo simulation**: Computing equilibrium properties (energy, magnetization, susceptibility) in materials modeling
- **Phase diagram mapping**: Determining critical phenomena and phase transitions experimentally and in simulation

### Systems with Constraints
- **Spin glass models**: Optimization in disordered systems relevant to combinatorial optimization problems
- **Constraint satisfaction**: Sampling feasible solutions from high-dimensional constrained spaces

### Network and Graph Problems
- **Ising models on networks**: Analyzing consensus formation, synchronization, or cooperative phenomena in networked systems
- **Graph colorings and independent sets**: Sampling valid colorings of graphs (relevant to scheduling, frequency assignment)

### Materials Science
- **Polymer and protein folding**: Sampling conformational states via local moves (variants of Glauert dynamics)
- **Crystal growth simulation**: Modeling equilibration of atomic configurations

## Common Mistakes / Pitfalls

1. **Confusing mixing time with burn-in**: The burn-in period is heuristic; rigorous mixing time bounds are much stricter. Use rigorous analysis rather than rule-of-thumb burn-in.

2. **Assuming rapid mixing without verification**: Just because Glauert dynamics is "natural" doesn't mean it mixes rapidly. **Always check the spectral gap or mixing time bounds** for your specific model and parameters.

3. **Ignoring phase transitions**: Near criticality, mixing time degrades sharply. Blindly applying uniform sampling strategies without monitoring for critical behavior leads to poor samples. The source material shows this is subtle—even at criticality, bounds are polynomial but potentially high-degree.

4. **Choosing step size incorrectly**: The number of steps to decorrelate depends on mixing time. Collecting samples every step gives correlated draws. Use appropriate **thinning** based on autocorrelation.

5. **Model parameter pitfalls**: 
   - For two-spin systems, mixing time depends critically on whether you're in the **uniqueness regime** (below critical threshold). Above it, polynomial-time sampling is intractable unless P = NP.
   - Unbounded-degree graphs require specialized analysis (the 2022 breakthrough by CFYZ extends results to such graphs).

6. **Forgetting high-dimensional geometry**: Glauert dynamics can be slow on high-dimensional problems where the mixing time scales exponentially with dimension, unless the model has strong conditional independence structure.

## See Also

- [[Markov Chain Monte Carlo (MCMC)]] — General framework encompassing Glauert dynamics
- [[Spect