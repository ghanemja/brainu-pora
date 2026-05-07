# Imaginary Time Evolution

## Definition

**Imaginary time evolution** is a mathematical technique in which the real time variable $t$ in a quantum evolution operator is replaced by imaginary time $\tau = it$, transforming the unitary time evolution operator into a non-unitary contraction operator. This maps quantum state evolution into a classical optimization landscape where probability amplitudes decay exponentially with energy cost.

Formally, the state after imaginary time evolution is:
$$|\psi(\tau)\rangle = e^{-\tau H} |\psi(0)\rangle$$

where $H$ is a Hamiltonian and $\tau$ is the imaginary time parameter. When applied to a cost function $C(\vec{x})$, the resulting state amplitude for configuration $\vec{x}$ becomes:
$$\langle \vec{x} | \psi(\tau) \rangle \propto e^{-\tau C(\vec{x})}$$

## Key Equations

**State representation with cost-weighted amplitudes:**
$$|\psi\rangle = \sum_{\vec{x}} e^{-\tau C(\vec{x})} |\vec{x}\rangle \tag{12}$$

where:
- $C(\vec{x})$ is the cost function evaluated at configuration $\vec{x}$
- $\tau$ is the imaginary time parameter (positive real number)
- $|\vec{x}\rangle$ is a computational basis state

**Initial superposition state (uniform)**:
$$|\psi_0\rangle = \bigotimes_{i=0}^{n-1} \left( \sum_{x_i=0}^{d-1} |x_i\rangle \right) = \sum_{\vec{x} \in \{0,...,d-1\}^n} |\vec{x}\rangle \tag{13}$$

**After single-variable cost application:**
$$|\psi_1\rangle = \bigotimes_{i=0}^{n-1} \left( \sum_{x_i=0}^{d-1} e^{-\tau(Q_{ii}x_i^2 + D_i x_i)} |x_i\rangle \right) \tag{14}$$

## Physical Intuition / Derivation

### Why "Imaginary" Time?

In standard quantum mechanics, time evolution follows:
$$i\hbar \frac{\partial |\psi\rangle}{\partial t} = H|\psi\rangle \quad \Rightarrow \quad |\psi(t)\rangle = e^{-iHt/\hbar}|\psi(0)\rangle$$

This is **unitary**: probabilities are conserved, and phases oscillate. 

When we replace $t \to -i\tau$ (substituting real time with imaginary time):
$$|\psi(\tau)\rangle = e^{-\tau H/\hbar}|\psi(0)\rangle$$

This is **non-unitary**: amplitudes decay according to energy. It is *dissipative* rather than conservative.

### The Optimization Landscape

The key insight: after imaginary time evolution,
$$P(\vec{x}) = \frac{|e^{-\tau C(\vec{x})}|^2}{\sum_{\vec{y}} e^{-2\tau C(\vec{y})}}$$

For large $\tau$:
- Low-cost configurations $\vec{x}^*$ (where $C(\vec{x}^*)$ is minimal) have amplitudes exponentially larger than others
- High-cost configurations are exponentially suppressed: $e^{-\tau C(\vec{x})} \approx 0$
- The state concentrates on ground state(s) of the cost landscape

This is analogous to **thermal equilibration** at inverse temperature $\beta = 2\tau$, but deterministic rather than stochastic.

### Tensor Network Implementation

The paper uses **layered tensor contractions** to efficiently compute imaginary time evolution:

1. **Superposition layer**: Initialize equal superposition of all $d^n$ configurations
2. **Diagonal cost layer**: Apply single-variable costs $e^{-\tau Q_{ii}x_i^2}$ 
3. **Interaction layers**: Apply interaction costs $e^{-\tau Q_{ij}x_i x_j}$ via staircase structure
4. **Contraction**: Extract the state by merging tensor dimensions

This avoids exponentially-large state vectors by exploiting tensor product structure.

## Applications in Engineering

### 1. **Combinatorial Optimization (QUBO/QUDO)**
- Solve quadratically-unconstrained binary/discrete optimization problems
- Engineering: circuit design, resource allocation, scheduling
- Advantage: exponential suppression of high-cost solutions for large $\tau$

### 2. **Ground State Preparation in Quantum Computing**
- Variational quantum eigensolver (VQE) uses imaginary time as reference
- Adiabatic quantum computing exploits slow imaginary-time-like evolution
- Engineering: drug discovery, materials simulation

### 3. **Physics Simulations**
- Monte Carlo integration (Green's function Monte Carlo, diffusion Monte Carlo)
- Thermal state preparation in condensed matter physics
- Quantum path integrals use Euclidean (imaginary) time formulation

### 4. **Machine Learning & Neural Networks**
- Energy-based models (Boltzmann machines, restricted Boltzmann machines)
- Generative models learn probability distributions proportional to $e^{-\tau E(\vec{x})}$
- Hidden layer: implicit imaginary time evolution

### 5. **Gradient-Free Optimization**
- No need for derivative computation; based purely on cost evaluation
- Useful when gradients are unavailable or noisy

## Common Mistakes / Pitfalls

### 1. **Confusing with Real Time Evolution**
- **Mistake**: Treating $e^{-\tau H}$ as preserving normalization like $e^{-iHt}$
- **Reality**: Amplitudes shrink; must renormalize to extract probabilities
- **Fix**: Always track normalization factor: $Z(\tau) = \sum_{\vec{x}} e^{-2\tau C(\vec{x