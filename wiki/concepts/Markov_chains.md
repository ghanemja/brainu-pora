# Markov Chains

## Definition

A **Markov chain** is a stochastic process $\{X_t\}_{t=0}^{\infty}$ taking values in a discrete state space $\mathcal{S}$ that satisfies the **Markov property**:

$$P(X_{t+1} = s' \mid X_t = s, X_{t-1}, \ldots, X_0) = P(X_{t+1} = s' \mid X_t = s)$$

This property states that the future state depends only on the current state, not on the entire history. The conditional probability $P(X_{t+1} = s' \mid X_t = s)$ is called the **transition probability**, often denoted $P(s \to s')$ or $P_{ss'}$.

A Markov chain is:
- **Homogeneous** (or time-homogeneous) if transition probabilities are independent of time $t$
- **Irreducible** if every state is reachable from every other state
- **Aperiodic** if the greatest common divisor of return times to any state is 1
- **Ergodic** if irreducible and aperiodic

## Key Equations

### Transition Matrix

For a finite state space, the transition probabilities form a **transition matrix** $\mathbf{P}$:

$$P_{ij} = P(X_{t+1} = j \mid X_t = i), \quad \sum_{j} P_{ij} = 1$$

where rows sum to 1 (stochastic matrix).

### Chapman-Kolmogorov Equation

The $n$-step transition probability satisfies:

$$P_{ij}^{(n)} = \sum_{k} P_{ik}^{(m)} P_{kj}^{(n-m)}$$

or equivalently:
$$\mathbf{P}^{(n)} = \mathbf{P}^n$$

### Stationary Distribution

A distribution $\pi$ is **stationary** if:

$$\pi = \pi \mathbf{P} \quad \text{or equivalently} \quad \pi_j = \sum_i \pi_i P_{ij}$$

For an irreducible, aperiodic (ergodic) chain, a unique stationary distribution exists and:

$$\lim_{n \to \infty} P_{ij}^{(n)} = \pi_j \quad \forall i, j$$

### Mixing Time and Poincaré Inequality

The **mixing time** measures convergence to stationarity. The **Poincaré inequality** (used in the source material for high-temperature distributions) provides a bound:

$$\text{Var}_\pi[f] \leq \lambda_{\text{gap}}^{-1} \mathbb{E}_\pi[\mathcal{D}(f)]$$

where $\lambda_{\text{gap}} = 1 - \lambda_2$ is the spectral gap (difference between 1 and the second-largest eigenvalue of $\mathbf{P}$), and $\mathcal{D}(f)$ is a suitable Dirichlet form. Larger spectral gaps imply **faster mixing** (rapid convergence to stationarity).

## Physical Intuition / Derivation

### Why the Markov Property?

The Markov property—that the future depends only on the present—emerges naturally in systems where:
1. The state encodes all relevant information for prediction
2. The process is memoryless (no residual correlations)

Consider a random walk on a graph: given your current position, your next position depends only on available edges, regardless of how you arrived there.

### Stationary Distributions as Equilibrium

For a system in equilibrium, the long-run proportion of time spent in state $j$ equals $\pi_j$. This is equivalent to **detailed balance** in reversible chains:

$$\pi_i P_{ij} = \pi_j P_{ji}$$

This symmetry condition ensures no net flow of probability between states in equilibrium.

### Rapid Mixing and Spectral Gap

The spectral gap $\lambda_{\text{gap}}$ quantifies how quickly a chain "forgets" its initial state. Intuitively:
- Large $\lambda_{\text{gap}} \approx 1$: convergence in $O(1)$ steps
- Small $\lambda_{\text{gap}} \approx 0$: slow convergence, possibly exponential in $n$

The Poincaré inequality connects this gap to variance reduction, crucial for **variance reduction** in MCMC sampling (as referenced in the source material for analyzing graphical models at high temperature).

## Applications in Engineering

### 1. Markov Chain Monte Carlo (MCMC) Sampling
Constructing local Markov chains with carefully designed transition probabilities to sample from complex distributions (Ising models, graphical models). The rapid mixing property ensures efficient convergence to the target distribution in polynomial time.

### 2. Queueing Theory
Modeling arrival and service processes. An $M/M/1$ queue uses a Markov chain where the state is the number of customers. Transition probabilities depend on arrival and service rates, enabling analysis of queue length, wait time, and throughput.

### 3. Reliability and Maintenance
Modeling equipment degradation states: from healthy → worn → failed. Transition probabilities encode failure rates, enabling optimal maintenance scheduling and availability prediction.

### 4. Information Theory & Channel Coding
Hidden Markov Models (HMMs) for decoding corrupted transmissions. The underlying Markov chain represents transmitted symbols; observations are noisy versions, enabling maximum-likelihood or Viterbi decoding.

### 5. Machine Learning & NLP
- **Language modeling**: $n$-gram models approximate language as low-order Markov chains
- **Recommendation systems**: User state (past behavior) predicts next item via transition probabilities
- **Learning under distributional assumptions** (as in the source): Markov chains on graphical models enable agnostic learning of halfspaces over structured (non-product) distributions

### 6. Network Routing & Traffic Engineering
Modeling packet or vehicle flow transitions between network nodes. Stationary distribution gives long-run traffic load on each link.

##