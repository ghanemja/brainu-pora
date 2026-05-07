# Ising Models

## Definition

The **Ising model** is a mathematical model of ferromagnetism and a fundamental object in statistical physics and computer science. It describes a system of binary random variables (spins) arranged on a graph, where each spin interacts with its neighbors according to a Hamiltonian energy function.

Formally, let $G = (V, E)$ be a graph with $n$ vertices, and let $\sigma \in \{+1, -1\}^n$ be a spin configuration. The probability distribution over configurations under the Ising model with parameters $\beta$ (inverse temperature) and external field $h$ is:

$$\mu(\sigma) = \frac{1}{Z} \exp\left(\beta \sum_{(i,j) \in E} J_{ij}\sigma_i\sigma_j + \sum_{i \in V} h_i\sigma_i\right)$$

where $Z$ is the partition function (normalization constant) and $J_{ij}$ are coupling constants. The model exhibits a **phase transition**: at low temperatures, spins align strongly; at high temperatures, the system behaves nearly like independent random bits.

## Key Equations

**Partition Function (normalization)**
$$Z(\beta, h) = \sum_{\sigma \in \{+1,-1\}^n} \exp\left(\beta \sum_{(i,j) \in E} J_{ij}\sigma_i\sigma_j + \sum_{i \in V} h_i\sigma_i\right)$$

**High-Temperature Expansion (for weak coupling)**
At high temperature, the Ising model is well-approximated by a mixture of product distributions via the **Hubbard-Stratonovich transform**, which linearizes the quadratic interaction term:
$$\exp\left(\beta \sum_{(i,j) \in E} J_{ij}\sigma_i\sigma_j\right) \approx \int_{\mathbb{R}^n} \exp\left(\sum_i \lambda_i\sigma_i - \text{quadratic terms}\right) d\lambda$$

**Influence Bounds (concentration)**
For a bounded-degree graph $G$ with max degree $d$, the $\mu$-influence of variable $i$ on a Boolean function $f$ is bounded by:
$$\text{Inf}_i(f) \leq O\left(\sqrt{(d+1)n}\right)$$

This bound is tight and follows from Chatterjee's method of **exchangeable pairs**, controlling influence through variance with respect to conditional mean given all other spins.

**Polynomial Approximation of Linear Threshold Functions**
Under marginally-bounded and subgaussian Ising models, any linear threshold function $f \in F$ can be approximated by a polynomial $p$ of degree:
$$\deg(p) = O\left(\frac{\log^2(1/\varepsilon)}{\varepsilon^2}\right)$$
satisfying $\mathbb{E}_{y \sim \mu}[|f(y) - p(y)|] \leq \varepsilon$.

## Physical Intuition / Derivation

### Origin and Physical Picture

The Ising model originated in the 1920s to describe ferromagnetic materials. Each site on a lattice holds a spin that can point "up" (+1) or "down" (−1). Neighboring spins prefer to align in the same direction (at low temperature) due to the $J_{ij}\sigma_i\sigma_j$ interaction term, which is minimized when spins are parallel. An external magnetic field $h_i$ biases spins in one direction.

The energy (Hamiltonian) is:
$$E(\sigma) = -\sum_{(i,j) \in E} J_{ij}\sigma_i\sigma_j - \sum_{i} h_i\sigma_i$$

The Boltzmann distribution reflects statistical mechanics: configurations with lower energy are exponentially more likely at temperature $T$ (or equivalently, at inverse temperature $\beta = 1/k_B T$).

### Why High Temperature Matters

At **high temperature** ($\beta \to 0$), the exponential weights flatten, and the model approaches uniform randomness. This regime is computationally tractable: 
- Sampling becomes efficient (Glauert dynamics converges rapidly)
- The system behaves nearly independently
- Influence of variables on functions is bounded

At **low temperature** ($\beta \to \infty$), spins lock into correlated patterns, creating hard computational problems (NP-hard inference in many cases).

### The Hubbard-Stratonovich Transform

This is a mathematical trick to linearize interactions:
$$\exp\left(\beta J\sigma_i\sigma_j\right) = \int_{\mathbb{R}} \frac{1}{\sqrt{2\pi/\beta}} \exp\left(-\frac{\beta}{2}\lambda^2 + \lambda(\sigma_i + \sigma_j)\sqrt{\beta J}\right) d\lambda$$

By writing the quadratic interaction as a linear coupling to auxiliary continuous variables, one reveals that the Ising model can be expressed as a **mixture of product distributions** (one for each choice of auxiliary variables). This is crucial for proving concentration and anti-concentration properties.

## Applications in Engineering

### 1. **Machine Learning & Learning Theory**
- **Agnostic learning of linear threshold functions**: Using polynomial approximations under Ising models to design efficient learning algorithms for low-complexity concept classes
- **Sample complexity bounds**: Influence bounds constrain VC dimension and generalization
- Ising models provide natural distributional assumptions where many learning problems transition from hard to tractable

### 2. **Sampling & Inference**
- **Markov Chain Monte Carlo**: Glauert dynamics (a local MCMC algorithm) efficiently samples from high-temperature Ising models
- Applications in probabilistic inference for graphical models, Bayesian networks, and factor graphs
- Used in constraint satisfaction problem solvers

### 3. **Statistical Physics & Materials Science**
- Modeling ferromagnetic phase transitions in magnetic materials
- Predicting critical phenomena and universality classes
- Understanding domain formation in thin films and bulk magnets

### 4. **Optimization & Combinatorial Problems**
- Mapping combinatorial optimization (MAX-SAT, graph coloring) to Ising models
- Quantum an