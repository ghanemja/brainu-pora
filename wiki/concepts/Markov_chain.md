# Markov Chain

## Definition

A **Markov chain** is a discrete-time stochastic process that evolves over a state space $\Omega$ such that the probability distribution of the next state depends only on the current state, not on the history of states visited. This property is called the **Markov property** or **memorylessness**.

Formally, let $\{X_n\}_{n=0}^{\infty}$ be a sequence of random variables taking values in a countable state space $\Omega$. The process is a Markov chain if:

$$P(X_{n+1} = x_{n+1} \mid X_n = x_n, X_{n-1} = x_{n-1}, \ldots, X_0 = x_0) = P(X_{n+1} = x_{n+1} \mid X_n = x_n)$$

for all $n \geq 0$ and all possible state sequences.

**Transition probabilities** are specified by a matrix $\mathbf{P}$ where:
$$P_{ij} = P(X_{n+1} = j \mid X_n = i)$$

In the context of the source material, the **edge-tilting field dynamics** and **vertex-field dynamics** are specific Markov chains on configuration spaces $\Omega(\mu)$ where configurations are labeled by binary assignments $\sigma \in \{0,1\}^V$.

## Key Equations

**Markov Property (Transition Formula):**
$$P(X_n = x_n) = P(X_0 = x_0) \prod_{k=0}^{n-1} P(X_{k+1} = x_{k+1} \mid X_k = x_k)$$

**Stationary Distribution** (if it exists):
$$\pi = \pi \mathbf{P}$$

where $\pi$ is a probability vector satisfying $\sum_{i} \pi_i = 1$.

**Edge-Tilting Distribution** (from source):
$$\theta \otimes \mu(\sigma) \propto \mu(\sigma) \cdot \theta^{m(\sigma)}$$

where $m(\sigma) = |\{\{u,v\} \in E \mid \sigma_u = \sigma_v\}|$ is the number of monochromatic edges, and $\theta \in (0,1)$ is the tilt parameter.

**Vertex-Field Distribution** (alternative formulation):
$$\theta * \mu(\sigma) \propto \mu(\sigma) \cdot \theta^{\|\sigma\|}$$

where $\|\sigma\|$ counts vertices with $\sigma_v = 1$.

## Physical Intuition / Derivation

### Fundamental Concept

A Markov chain abstracts systems where future evolution depends only on the **present state**, not the entire past. This simplification is powerful because it enables analytical tractability while remaining valid for many physical, biological, and engineering systems.

### Intuition via Field Dynamics

The source material illustrates Markov chains through **field dynamics** on binary spin configurations:

1. **Current state:** A configuration $\sigma \in \{0,1\}^V$ assigns values to vertices in a graph.

2. **Transition mechanism (Down-Up step):**
   - **Down step:** Stochastically remove edges (or vertices) based on the tilt parameter $\theta$.
   - **Up step:** Resample the restricted configuration from a tilted distribution (e.g., $\theta \otimes \mu$ or $\theta * \mu$).

3. **Why it's Markovian:** The next configuration depends only on the current configuration, not how we arrived at it.

### Why Tilting Matters

The tilt parameter $\theta$ acts as a **control knob**:
- $\theta$ small → favors monochromatic edges (critical behavior)
- $\theta$ large → tilts toward subcritical (high-temperature) regime

By tilting **edges** (rather than vertices) in a controlled manner, the edge-tilting variant avoids uncontrolled drifts that arise in stochastic localization. This controlled dynamics is crucial for analyzing phase transitions in antiferromagnetic systems.

### Convergence to Equilibrium

For well-designed Markov chains (aperiodic, irreducible, finite state space), the distribution $P(X_n)$ converges to a **stationary distribution** $\pi$ independent of initial conditions. This is essential for sampling from complex distributions in applications.

## Applications in Engineering

### 1. **Monte Carlo Simulation & Sampling**
- **Gibbs sampling:** A Markov chain that samples from high-dimensional distributions in Bayesian inference, machine learning, and computational statistics.
- **Metropolis-Hastings:** Constructs a Markov chain whose stationary distribution is a target distribution; used extensively in physics simulations and uncertainty quantification.

### 2. **Statistical Physics & Phase Transitions**
- Modeling spin systems (Ising, Potts models) undergoing critical phenomena.
- The source material applies Markov chain techniques to analyze antiferromagnetic two-spin systems at criticality.

### 3. **Network & Queue Analysis**
- **Queueing networks:** Customer arrivals and service completions form Markov chains; used to design reliable communication systems, data centers.
- **Reliability engineering:** Component failures and repairs modeled as Markov processes; enables steady-state availability calculations.

### 4. **Control Systems & Optimization**
- **Markov Decision Processes (MDPs):** Extend Markov chains with actions and rewards; foundation for reinforcement learning and dynamic programming.
- Optimal control in uncertain environments.

### 5. **Computational Methods in Statistical Mechanics**
- **Localization schemes** (as in the source) use field dynamics to reduce complex critical phenomena to tractable subcritical problems.
- Enabling rigorous analysis of phase transitions in lattice models.

## Common Mistakes / Pitfalls

### 1. **Assuming Markov Property When Not Valid**
Markov chains require strict memorylessness. If future behavior depends on how long the process has been in a state (age-dependent processes), the system is not Markovian without expanding the state space.

### 2. **Confusing Transition Probabilities with