# Hamiltonian Monte Carlo (HMC)

## Definition

**Hamiltonian Monte Carlo (HMC)** is a Markov Chain Monte Carlo (MCMC) sampling method that uses Hamiltonian dynamics to propose states with high acceptance probability. It augments the target distribution $\pi(\mathbf{x})$ on $\mathbb{R}^d$ with auxiliary momentum variables $\mathbf{p} \in \mathbb{R}^d$ and exploits geometric properties of the resulting energy landscape to generate proposals.

**Notation distinction**: In literature, "HMC" often refers to *Metropolized HMC (MHMC)*, which applies a Metropolis filter to accept/reject proposals. This wiki distinguishes:
- **HMC**: unadjusted, non-Metropolized trajectory-based sampling
- **MHMC**: HMC with Metropolis acceptance step

## Key Equations

### Hamiltonian Formulation

The joint distribution over position and momentum is:
$$\pi(\mathbf{x}, \mathbf{p}) \propto \exp\left(-H(\mathbf{x}, \mathbf{p})\right)$$

where the Hamiltonian (total energy) is:
$$H(\mathbf{x}, \mathbf{p}) = -\log \pi(\mathbf{x}) + \frac{1}{2}\mathbf{p}^T \mathbf{p}$$

The potential energy is $U(\mathbf{x}) = -\log \pi(\mathbf{x})$, and kinetic energy is $K(\mathbf{p}) = \frac{1}{2}\|\mathbf{p}\|^2$.

### Hamiltonian Dynamics

Hamilton's equations govern evolution:
$$\frac{d\mathbf{x}}{dt} = \nabla_\mathbf{p} H = \mathbf{p}$$
$$\frac{d\mathbf{p}}{dt} = -\nabla_\mathbf{x} H = \nabla \log \pi(\mathbf{x})$$

### Leapfrog Integrator

The standard discretization with step size $h$ over $L$ steps:
$$\mathbf{p}_{n+1/2} = \mathbf{p}_n + \frac{h}{2}\nabla \log \pi(\mathbf{x}_n)$$
$$\mathbf{x}_{n+1} = \mathbf{x}_n + h \mathbf{p}_{n+1/2}$$
$$\mathbf{p}_{n+1} = \mathbf{p}_{n+1/2} + \frac{h}{2}\nabla \log \pi(\mathbf{x}_{n+1})$$

### MHMC Acceptance Probability

After integrating for continuous time $T$ using $T/h$ leapfrog steps:
$$\alpha = \min\left(1, \exp\left(-\Delta H\right)\right)$$

where $\Delta H = H(\mathbf{x}', \mathbf{p}') - H(\mathbf{x}, \mathbf{p})$ is the energy change due to discretization error.

## Physical Intuition / Derivation

### Why Hamiltonian Dynamics?

**Standard random walk MCMC** (e.g., Metropolis-Hastings) proposes moves by adding noise to the current state, leading to highly correlated samples and slow exploration. **HMC solves this** by using dynamics that:

1. **Respect the geometry** of $\pi$: proposals move *with* the gradient, not perpendicular to it
2. **Generate distant proposals** in few steps while maintaining high acceptance
3. **Exploit reversibility and volume preservation** of Hamiltonian flow (symplectic structure)

### Physical Analogy

Imagine sampling from $\pi(\mathbf{x})$ as finding equilibrium configurations of a particle in potential $U(\mathbf{x})$. Hamiltonian dynamics is like releasing a particle with random momentum and letting physics guide it:
- The particle rolls downhill (toward high probability regions)
- Momentum carries it through low-probability valleys
- Energy conservation ensures trajectories explore efficiently

The auxiliary momentum $\mathbf{p}$ is *resampled* (usually from $\mathcal{N}(0, I)$) between trajectory segments, decoupling successive samples.

### Why Leapfrog?

Exact Hamiltonian evolution preserves phase space volume (Liouville's theorem), making acceptance probability 1. The discretized leapfrog integrator is **symplectic** (preserves volume to order $\mathcal{O}(h^2)$), so discretization error is small. This is critical: non-symplectic integrators accumulate bias rapidly.

## Dimensional Dependence and Cold-Start Failure

A critical finding from recent analysis [CG23, LST21a]:

### Warm Start (Good Initialization)
- **Step size**: $h \asymp d^{-1/4}$
- **Acceptance probability**: bounded away from 0
- **Mixing time**: $\tilde{O}(d^{1/4})$ for isotropic Gaussian targets
- **Caveat**: requires starting from a "warm" distribution close to equilibrium

### Cold Start (Poor Initialization)
- **Problem**: Starting far from typical set (e.g., at mode of Gaussian) forces use of $h \asymp d^{-1/2}$ to maintain non-vanishing acceptance
- **Traversal time**: $1/h \asymp d^{1/2}$ steps just to cross state space
- **Mixing time lower bound**: $\tilde{\Omega}(d^{1/2})$
- **Mechanism**: Small steps + rejection feedback create geometric "cold start trap"

This is **not a limitation of analysis**—it's fundamental and observable empirically (Figure 1).

## Applications in Engineering

### 1. **Uncertainty Quantification in Computational Models**
- Sampling from posterior distributions in Bayesian inverse problems (e.g., parameter inference from noisy observations)
- HM