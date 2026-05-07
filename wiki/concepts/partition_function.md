# Partition Function

## Definition

The **partition function** is a fundamental mathematical object in statistical mechanics and mathematical physics that encodes all thermodynamic information about a system. For the hard-core model on a graph $G = (V, E)$, it is defined as:

$$Z_G(\lambda) = \sum_{I \subseteq V} \lambda^{|I|}$$

where the sum ranges over all independent sets $I$ of the graph (sets with no two adjacent vertices), $\lambda \geq 0$ is the **activity parameter** (or fugacity), and $|I|$ is the cardinality of the set.

More generally, the partition function is the **Laplace transform** (or generating function) of the ensemble of all possible configurations, weighted by their statistical probability.

## Key Equations

### Hard-Core Model Partition Function
$$Z_G(\lambda) = \sum_{I \in \mathcal{I}(G)} \lambda^{|I|}$$

where $\mathcal{I}(G)$ denotes the set of all independent sets in graph $G$.

### Gibbs Distribution
The partition function normalizes the probability of configuration $I$ (an independent set):
$$\mu_G^\lambda(I) = \frac{\lambda^{|I|}}{Z_G(\lambda)}$$

### Free Energy Density
The **free energy density** (thermodynamic limit) is defined as:
$$f_L(\lambda) = \lim_{n \to \infty} \frac{\log Z_{G_n}(\lambda)}{|V_{G_n}|}$$

for a sequence of finite graphs $G_n$ exhausting an infinite lattice $L$.

### Marginal Probability
The probability that vertex $v$ is occupied in the independent set:
$$P_{G,v} = \sum_{I \ni v} \mu_G^\lambda(I)$$

## Physical Intuition / Derivation

### Statistical Mechanics Perspective

The partition function is the **sum over states**, where each state $I$ is weighted by $\lambda^{|I|}$. Think of it as:
- Each occupied vertex contributes a factor $\lambda$ to the weight
- Independent sets are the **only allowed configurations** (hard-core constraint: no adjacent vertices can be occupied simultaneously)
- The partition function tracks all possible configurations and their relative statistical weights

At physical equilibrium, the probability of observing configuration $I$ is proportional to $\lambda^{|I|}$—higher activity $\lambda$ makes larger independent sets more probable.

### Connection to Graph Structure

The partition function encodes the **combinatorial structure** of the graph:
- On a tree (low structural complexity), zeros are far from the positive real axis
- On dense lattices (high structural complexity), zeros approach the real axis more closely
- The **connective constant** $\sigma$ measures exponential growth of self-avoiding walks and provides a sharper measure of complexity than maximum degree $\Delta$

### Lee-Yang Theory

The **location of complex zeros** of $Z_G(\lambda)$ in the complex $\lambda$-plane determines:
- **Analyticity** of the free energy $f(\lambda)$: if $Z_G(\lambda)$ is zero-free in a region, $f(\lambda)$ is analytic there
- **Absence of phase transitions**: regions of analyticity indicate no phase transition in that regime
- As $|V| \to \infty$, phase transitions occur where zeros approach the real axis

This is the content of **Lee-Yang theory**: phase transitions correspond to zero approaches on the real line.

## Applications in Engineering

### 1. **Approximation Algorithms**

The Barvinok–Patel–Regts framework converts zero-free regions into:
- **Fully Polynomial-Time Approximation Schemes (FPTAS)** for computing $Z_G(\lambda)$
- Runtime polynomial in $1/\epsilon$ (approximation error) and $\log(1/\delta)$ (failure probability)
- Critical for NP-hard combinatorial optimization problems on bounded-degree graphs

### 2. **Statistical Physics Computations**

- **Thermodynamic predictions**: free energy, entropy, correlation functions in lattice models
- **Phase transition detection**: determining critical points $\lambda_c$ where physical properties change discontinuously
- **Spin glass and lattice gas models**: partition functions encode disorder and phase behavior

### 3. **Probabilistic Inference**

- **Graphical models**: partition function relates to inference in Markov random fields
- **Counting problems**: hard-core model partition function equals the *number of independent sets* when $\lambda = 1$
- **Approximating rare events**: importance sampling using Gibbs distributions

### 4. **Sampling and MCMC**

- Efficient sampling from $\mu_G^\lambda(I)$ requires understanding the partition function's structure
- **Correlation decay** properties (related to zero-freeness) enable efficient Markov chain convergence
- Applications to spatial statistics and network models

## Common Mistakes / Pitfalls

### 1. **Confusing Partition Function with Free Energy**
- **Mistake**: Treating $Z_G(\lambda)$ and $f(\lambda) = \frac{\log Z_G(\lambda)}{|V|}$ interchangeably
- **Reality**: They're related but distinct; $f$ is the normalized logarithm and governs phase transitions
- **Why it matters**: Analyticity of $f$ (not $Z$) determines whether phase transitions occur

### 2. **Ignoring Finite-Size Effects**
- **Mistake**: Using partition functions on small graphs as proxies for infinite lattice behavior
- **Reality**: Zeros of finite $Z_{G_n}(\lambda)$ must be **uniformly zero-free** in a complex neighborhood (independent of $n$) to guarantee analyticity in the limit
- **Why it matters**: A single zero approaching the real axis as $n \to \infty$ indicates a phase transition, even if small systems appear smooth

### 3. **Maximum Degree vs. Connective Constant**
- **Mistake**: Using $\Delta$ (maximum degree) as the only measure of graph complexity
- **Reality**: For many graphs (especially lattices), the **connective constant** $\sigma$ is much smaller and provides tighter zero-free regions
- **Why it matters**: Better algorithmic thresholds; can handle regular lattices where $\Delta