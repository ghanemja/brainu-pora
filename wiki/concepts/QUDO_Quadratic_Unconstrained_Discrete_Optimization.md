# QUDO (Quadratic Unconstrained Discrete Optimization)

## Definition

**QUDO** is a discrete optimization framework for solving problems of the form:

$$\min_{\mathbf{x}} C(\mathbf{x}) = \sum_{i} Q_{ii}x_i^2 + \sum_{i<j} Q_{ij}x_ix_j + \sum_i D_i x_i$$

where $\mathbf{x} = (x_0, x_1, \ldots, x_{n-1})$ with each variable $x_i \in \{0, 1, \ldots, d-1\}$ taking discrete values in a finite domain. The problem is *unconstrained*—all variable assignments are feasible—making it suitable for representing combinatorial optimization problems without explicit constraints.

QUDO generalizes [[QUBO]] (Quadratic Unconstrained Binary Optimization) by allowing variables to take on more than two values, enabling representation of multi-valued discrete variables.

## Key Equations

### Cost State Vector Representation

The core tensor network construction uses an imaginary-time evolution representation:

$$|\psi\rangle = \sum_{\mathbf{x}} e^{-\tau C(\mathbf{x})} |\mathbf{x}\rangle$$

where:
- $C(\mathbf{x})$ is the cost function for configuration $\mathbf{x}$
- $\tau$ is the imaginary time constant (evolution parameter)
- The amplitude of each basis state encodes its cost
- For large $\tau$, the minimum-cost state has exponentially dominant amplitude

### Initial Superposition Layer

The algorithm begins with a uniform superposition over all possible assignments:

$$|\psi_0\rangle = \bigotimes_{i=0}^{n-1} \left(\sum_{x_i=0}^{d-1} |x_i\rangle\right) = \sum_{\mathbf{x} \in \{0,\ldots,d-1\}^n} |\mathbf{x}\rangle$$

This creates $d^n$ basis states, one for each possible configuration.

### Diagonal Interaction Layer

The diagonal (self-interaction) terms are applied via:

$$|\psi_1\rangle = \bigotimes_{i=0}^{n-1} \left(\sum_{x_i=0}^{d-1} e^{-\tau(Q_{ii}x_i^2 + D_i x_i)} |x_i\rangle\right)$$

Each tensor independently applies the cost contribution from variable $i$'s self-interaction and linear term.

### Cross-Interaction (Two-Body) Terms

Cross terms $Q_{ij}x_ix_j$ are implemented via staircase interaction tensors $S_{ij}$ that couple variables horizontally and propagate information vertically through the network. This layered structure maintains tensor contraction efficiency.

## Physical Intuition / Derivation

### Why Imaginary Time Evolution?

The exponential encoding $e^{-\tau C(\mathbf{x})}$ leverages a quantum mechanical principle: an operator $e^{-\tau H}$ (with Hamiltonian $H = C(\mathbf{x})$) suppresses high-energy (high-cost) states and amplifies low-energy (low-cost) states. As $\tau$ increases:

$$\lim_{\tau \to \infty} \frac{e^{-\tau C(\mathbf{x})}}{e^{-\tau C_{\min}}} = \begin{cases} 1 & \text{if } C(\mathbf{x}) = C_{\min} \\ 0 & \text{otherwise} \end{cases}$$

The optimal solution becomes **exponentially separated** in amplitude from suboptimal solutions.

### Tensor Network Construction

Rather than explicitly enumerate all $d^n$ states, the algorithm factorizes the state into a network of small tensors:

1. **Superposition tensors** initialize uniform amplitudes
2. **Cost tensors** apply diagonal energy terms (local interactions)
3. **Staircase tensors** apply cross-interaction terms in a structured chain

This hierarchical structure allows contraction algorithms (e.g., tensor train decomposition) to extract the minimum-cost state in polynomial time for certain problem structures, avoiding exponential blowup.

### Why Tensor Networks?

A tensor network represents:
$$|\psi\rangle = \bigotimes_{\text{layers}} T_{\text{layer}} \cdot |\psi_0\rangle$$

By organizing tensors hierarchically, the contraction order can be optimized. For 1D chain interactions, the tensor train format achieves $O(n \cdot d^3 \cdot \tau^p)$ complexity instead of $O(d^n)$ state enumeration.

## Applications in Engineering

### Combinatorial Optimization Problems

- **Portfolio optimization**: Variables represent quantities of assets; quadratic terms model correlations
- **Scheduling**: Assign tasks to time slots or resources with preference/penalty terms
- **Supply chain**: Optimize discrete production quantities with interaction costs

### Constraint Approximation

While QUDO is unconstrained, quadratic penalty terms can be added:
$$C(\mathbf{x}) = C_{\text{original}}(\mathbf{x}) + \lambda \sum_{\text{violated constraints}} \text{penalty}$$

The large penalty coefficients ($\lambda$) suppress infeasible solutions' amplitudes.

### Quantum-Inspired Classical Computing

QUDO algorithms provide:
- **Exact solutions** for small-to-medium problems via tensor contraction
- **Approximate solutions** using contraction schemes on large $\tau$ values
- **Warm starts** for classical solvers (heuristic initialization)

### Graph Problems

- **Maximum cut** (max-cut): Variables represent node partition; cross-terms penalize within-partition edges
- **Vertex coloring**: Multi-valued variables $x_i \in \{0,\ldots,k-1\}$ represent node colors; quadratic terms enforce edge conflicts

## Common Mistakes / Pitfalls

### 1. Confusing Convergence with Optimality

**Mistake**: Assuming small contraction error