# Glauert dynamics

## Definition

**Glauert dynamics** (more commonly called **Glauber dynamics**) is a Markov chain method for sampling from complex probability distributions, particularly Gibbs distributions over discrete spin systems. The dynamics work by iteratively updating individual variables (spins) according to local conditional probabilities, allowing the system to explore the state space in a way that eventually converges to the target distribution.

In the context of statistical physics and probabilistic inference, Glauber dynamics provide a practical algorithm for:
- Sampling from Gibbs distributions $\mu$ over binary or discrete state spaces
- Estimating partition functions and free energies
- Analyzing phase transitions in critical systems

### Formal Setup

For a distribution $\mu$ over states $\{0,1\}^V$ (where $V$ is a set of variables), one step of Glauber dynamics proceeds as:

1. **Select a variable** $v \in V$ (uniformly at random or by some schedule)
2. **Resample** variable $X_v$ from its conditional distribution:
$$X_v \sim \mu(\cdot \mid X_{V \setminus \{v\}})$$
3. **Update** the current state with the new value of $X_v$

## Key Equations

For a Gibbs distribution with energy function $H(\mathbf{x})$, the conditional probability of setting variable $v$ to state $s \in \{0,1\}$ is:

$$\Pr[X_v = s \mid X_{V \setminus \{v\}} = \mathbf{x}_{V \setminus \{v\}}] = \frac{\exp(-\beta H(\mathbf{x}_v^{(s)}))}{\sum_{s' \in \{0,1\}} \exp(-\beta H(\mathbf{x}_v^{(s')}))}$$

where $\beta$ is the inverse temperature parameter and $\mathbf{x}_v^{(s)}$ denotes the state with $X_v = s$.

### Mixing Time

The rate at which Glauber dynamics converges to $\mu$ is quantified by the **mixing time** $\tau_{\text{mix}}(\epsilon)$—the number of steps needed to reach $\epsilon$-total variation distance from the stationary distribution. A key result from the source material is that Glauber dynamics achieves **optimal mixing** in the **subcritical regime**:

$$\tau_{\text{mix}}(\epsilon) = \mathcal{O}(\text{poly}(n, \log(1/\epsilon)))$$

under appropriate uniqueness and spectral independence conditions.

## Physical Intuition / Derivation

### Why Glauber Dynamics Works

The intuition behind Glauber dynamics is **local balance**: by repeatedly resampling each variable according to its conditional distribution given all others, the chain preserves the target Gibbs distribution as a stationary distribution. This follows from the **detailed balance condition**:

$$\mu(\mathbf{x}) P(\mathbf{x} \to \mathbf{x}') = \mu(\mathbf{x}') P(\mathbf{x}' \to \mathbf{x})$$

where $P$ is the transition kernel. Provided the chain is **irreducible** (can reach any state from any other), it will converge to $\mu$.

### Rapid Mixing in Subcritical Regimes

The source material establishes that Glauber dynamics exhibits **rapid mixing** when the system satisfies:

1. **Spectral Independence (SI)**: The influence matrix 
$$\Psi_\mu(u,v) := \begin{cases}
\Pr[X_v = 1 \mid X_u = 1] - \Pr[X_v = 1 \mid X_u = 0] & \text{if } u \neq v \\
0 & \text{otherwise}
\end{cases}$$
has bounded spectral norm: $\lambda_{\max}(\Psi_\mu) \leq \rho$.

2. **Uniqueness conditions**: The system parameters satisfy uniqueness on the infinite $\Delta$-regular tree (guaranteeing absence of phase transitions).

The connection is intuitive: when variables have **weak long-range correlations** (low spectral independence), local resampling steps efficiently decorrelate the entire system, accelerating convergence.

### Critical Regime Dynamics

At criticality (phase transition boundaries), standard Glauber dynamics becomes **critically slowed**—mixing time can grow exponentially. The source material overcomes this via:

- **Edge-tilting field dynamics**: Introducing auxiliary tilted parameters to navigate through critical points
- **Localization framework**: Analyzing how mixing properties propagate through hierarchical decompositions of the state space
- **Tight SI bounds**: Theorem 1.7 establishes that for antiferromagnetic two-spin systems:
$$\lambda_{\max}(\Psi_{\mu_\tau}) \leq \frac{\Delta(1-\delta)}{(\Delta-1)\delta}$$
where $\delta$ is a slack parameter and $\Delta$ is maximum degree. This bound is **asymptotically tight**, crucial for achieving polynomial-time mixing at criticality.

## Applications in Engineering

### 1. **Monte Carlo Sampling for Probabilistic Models**
Glauber dynamics enable efficient sampling from high-dimensional probabilistic graphical models (Markov Random Fields, Bayesian networks) used in machine learning and uncertainty quantification.

### 2. **Statistical Physics Simulation**
- Simulating Ising model dynamics in materials science
- Computing phase diagrams and critical exponents
- Studying ferromagnetic/antiferromagnetic spin systems relevant to magnetic materials

### 3. **Optimization via Simulated Annealing**
Glauber dynamics with time-varying temperature $\beta(t)$ form the basis of simulated annealing algorithms for combinatorial optimization (traveling salesman problem, MAX-SAT, etc.).

### 4. **Inference in Graphical Models**
Computing partition functions and marginal probabilities in probabilistic inference, essential for:
- Belief propagation algorithms
- Variational inference
- Counting problems (#CSP)

### 5. **Spectral Independence Analysis**
The tight SI bounds