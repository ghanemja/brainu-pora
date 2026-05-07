# Cost Function Optimization

## Definition

**Cost function optimization** is the process of finding the variable assignment $\vec{x}$ that minimizes a scalar cost function $C(\vec{x})$. In the context of quantum and tensor network algorithms, this involves encoding the cost landscape into quantum amplitudes such that optimal solutions have exponentially larger probability than suboptimal ones.

Formally, the goal is to solve:
$$\vec{x}^* = \arg\min_{\vec{x}} C(\vec{x})$$

where $\vec{x} = (x_0, x_1, \ldots, x_{n-1})$ is a vector of $n$ variables, each taking discrete values in the range $\{0, 1, \ldots, d-1\}$.

## Key Equations

### Amplitude Encoding via Imaginary Time Evolution

The fundamental strategy encodes the cost function into quantum state amplitudes:

$$|\psi\rangle = \sum_{\vec{x}} e^{-\tau C(\vec{x})} |\vec{x}\rangle \tag{1}$$

where:
- $C(\vec{x})$ is the cost function for configuration $\vec{x}$
- $\tau$ is the **imaginary time evolution constant** (inverse temperature parameter)
- $e^{-\tau C(\vec{x})}$ is the amplitude (weight) assigned to each configuration

**Key property:** For sufficiently large $\tau$, the minimum-cost configuration dominates the state, since its amplitude grows exponentially relative to higher-cost configurations:

$$\text{Amplitude ratio} = \frac{e^{-\tau C(\vec{x}^*)}}{e^{-\tau C(\vec{x})}} = e^{\tau[C(\vec{x}) - C(\vec{x}^*)]} \to \infty \quad \text{as } \tau \to \infty$$

### Superposition Layer (Initial State)

For variables with $d$ possible values per dimension:

$$|\psi_0\rangle = \bigotimes_{i=0}^{n-1} \left(\sum_{x_i=0}^{d-1} |x_i\rangle\right) = \sum_{\vec{x} \in \{0,\ldots,d-1\}^n} |\vec{x}\rangle \tag{2}$$

This creates equal superposition over all $d^n$ possible configurations.

### Cost Decomposition (QUBO/QUDO Form)

The cost function is typically decomposed into:

$$C(\vec{x}) = \sum_{i=0}^{n-1} (Q_{ii}x_i^2 + D_i x_i) + \sum_{i<j} Q_{ij}x_i x_j \tag{3}$$

where:
- **Diagonal terms:** $Q_{ii}x_i^2 + D_i x_i$ (self-interactions)
- **Off-diagonal terms:** $Q_{ij}x_i x_j$ (pairwise interactions)

This corresponds to **Quadratic Unconstrained Binary Optimization (QUBO)** or **Quadratic Unconstrained Discrete Optimization (QUDO)** when variables are continuous or discrete-valued.

### State After Cost Application

After applying the diagonal cost layer:

$$|\psi_1\rangle = \bigotimes_{i=0}^{n-1} \left(\sum_{x_i=0}^{d-1} e^{-\tau(Q_{ii}x_i^2 + D_i x_i)} |x_i\rangle\right) \tag{4}$$

Interaction terms are applied via additional tensor layers.

## Physical Intuition / Derivation

### Why Exponential Encoding?

The exponential weighting $e^{-\tau C(\vec{x})}$ mirrors the **Boltzmann distribution** from statistical mechanics:

$$P(\vec{x}) \propto e^{-\beta E(\vec{x})}$$

where $\tau$ acts as inverse temperature. As temperature decreases (τ increases), the system concentrates probability on the ground state (minimum energy/cost).

### The Tensor Network Approach

Rather than explicitly storing a state with $d^n$ amplitude components (exponential memory), the tensor network exploits **structure** in the cost function:

1. **Superposition layer** creates initial equal-weight state (Eq. 2)
2. **Diagonal layer** applies single-variable costs locally (Eq. 4)
3. **Staircase/interaction layers** apply pairwise terms $Q_{ij}x_i x_j$ via contracted tensor products

Each layer is a tensor that modulates amplitudes for specific variables. Contraction of these layers yields the full state in Eq. 1, with computational complexity far better than naive $\mathcal{O}(d^n)$ enumeration.

### Limit of Large τ

In the limit $\tau \to \infty$:
$$|\psi\rangle \approx e^{-\tau C(\vec{x}^*)} |\vec{x}^*\rangle$$

The state becomes sharply peaked on the optimal solution. For *finite* but large $\tau$, the approximation error is controlled by the spectral gap between ground and first excited state.

## Applications in Engineering

### 1. **Combinatorial Optimization**
- **Traveling Salesman Problem (TSP):** Encode route cost as $C(\vec{x})$; find minimum-cost tour
- **Graph coloring:** Cost penalizes adjacent same-colored vertices
- **Scheduling:** Minimize makespan or resource conflicts via quadratic penalties

### 2. **Machine Learning & Signal Processing**
- **Sparse recovery:** Minimize $\|A\vec{x} - \vec{b}\|_2^2 + \lambda\|\vec{x}\|_0$ (L0 penalty is quadratic in indicator variables)
- **Matrix factorization:** Decompose data matrices by optimizing factorization cost
- **Clustering:** K-means reformulated as quadratic assignment problem

### 3. **Quantum Computing**
- **QAOA (Quantum Approximate Optimization Algorithm):** Leverages cost-encoded