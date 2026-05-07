# Quantum Annealing (QA)

## Definition

**Quantum Annealing** is a metaheuristic optimization technique that leverages quantum mechanical effects—primarily quantum tunneling and superposition—to explore the solution space of combinatorial optimization problems. The algorithm evolves a quantum system from an easily-prepared initial state to a final state encoding the solution of a target optimization problem, typically represented as an Ising model or Quadratic Unconstrained Binary Optimization (QUBO) problem.

Unlike adiabatic quantum computing (which relies on the adiabatic theorem), QA allows diabatic transitions and is designed for practical implementation on near-term quantum devices like D-Wave systems.

## Key Equations

### Ising Model Formulation
The target optimization problem is encoded as an Ising Hamiltonian:

$$H_{\text{Ising}} = \sum_{i} h_i Z_i + \sum_{i<j} J_{ij} Z_i Z_j$$

where $Z_i \in \{-1, +1\}$ are Ising spins and $h_i$, $J_{ij}$ are problem parameters.

### QUBO Formulation
Equivalently, a Binary Quadratic Model (BQM):

$$H_{\text{QUBO}} = \sum_{i} c_i x_i + \sum_{i<j} Q_{ij} x_i x_j$$

where $x_i \in \{0, 1\}$ are binary variables.

### Annealing Schedule
The effective Hamiltonian evolves as:

$$H(s) = A(s) H_{\text{driver}} + B(s) H_{\text{problem}}$$

where $s \in [0,1]$ is the annealing parameter, $A(s)$ decreases from 1 to 0, and $B(s)$ increases from 0 to 1. The driver Hamiltonian $H_{\text{driver}}$ (typically $H_{\text{driver}} = -\sum_i X_i$) maintains quantum tunneling.

### QAOA Connection
In the large-$n$ limit, the performance of log-depth Quantum Approximate Optimization Algorithm (QAOA) on sparse instances approaches:

$$\lim_{p \to \infty} \lim_{n \to \infty} E_J \langle \gamma, \beta | H_{\text{problem}} | \gamma, \beta \rangle = 1 - \frac{2\nu(D, \gamma, \beta)}{\sqrt{D}}$$

where $p$ is circuit depth, $\nu(D, \gamma, \beta)$ is a function dependent on graph degree $D$ and variational parameters $\gamma, \beta$.

## Physical Intuition / Derivation

### Why Quantum Tunneling Matters

In classical optimization, a system can become trapped in local minima. Quantum systems exploit **tunneling**—the ability to pass through energy barriers—allowing exploration beyond classically accessible regions. This is the core advantage of quantum annealing over purely classical methods.

### Adiabatic vs. Diabatic Evolution

- **Adiabatic limit**: If the system evolves slowly enough, the gap between ground and first excited state remains large, and the system stays in the ground state (encodes the solution). Achievable but requires very long annealing times.
- **Diabatic (practical QA)**: Real devices operate in a faster, non-adiabatic regime where the system can transition between energy levels. The final readout is probabilistic but requires no exponentially small gaps.

### Multi-Car Paint Shop Example

Consider scheduling $n$ cars through paint shops while minimizing swaps. The problem encodes naturally as:
- Variables: car-to-time slot assignments
- Constraints: collision avoidance, capacity limits
- Objective: minimize color-change penalties

For small instances ($n \lesssim 100$), QA shows promise. However, in the **asymptotic limit** ($n \to \infty$), empirical evidence shows QA performance degrades to match simple greedy algorithms—no proven quantum advantage emerges.

### Sparse Graph Structure

Real problems often exhibit local tree-like structure (especially degree-3 regular graphs, $D=3$). The cavity method or tensor network techniques can efficiently evaluate expected solution quality by exploiting this structure, reducing time complexity from $O(p \cdot 16^p)$ to $O(4^p)$ for depth-$p$ circuits.

## Applications in Engineering

### 1. **Combinatorial Optimization**
- **Vehicle Routing & Scheduling**: Paint shop scheduling, job shop scheduling, vehicle fleet routing
- **Graph Problems**: MaxCUT, Max-2-XORSAT, weighted graph coloring

### 2. **Constraint Satisfaction**
- Boolean satisfiability (SAT) problems on sparse instances
- Configuration problems in hardware design

### 3. **Machine Learning**
- Sampling from Boltzmann distributions for training
- Feature selection with combinatorial constraints

### 4. **Benchmarking & Comparison**
- D-Wave Advantage (quantum device): 100 μs annealing times, 100 readouts per instance
- Hybrid classical-quantum solvers (BQM solvers v2.2): Classical preprocessing with quantum acceleration
- Performance measured as: average cost, solution quality distribution, standard deviation normalized by problem size

## Common Mistakes / Pitfalls

### 1. **Assuming Asymptotic Quantum Advantage**
Many expect QA to scale better than classical methods as $n \to \infty$. Empirical and theoretical evidence suggests advantage is **problem-dependent** and often vanishes for dense problem instances. Small-to-medium instances are the sweet spot.

### 2. **Neglecting Problem Encoding**
The mapping from problem to Ising model is non-trivial. Poor encodings introduce spurious solutions or destroy structure; good encodings leverage sparsity (e.g., tree-like neighborhoods).

### 3. **Ignoring Device Limitations**
Real quantum annealers have:
- Limited qubit connectivity (Pegasus topology for D-Wave)
- Noise and calibration errors
- Finite annealing time constraints
These often dominate over algorithmic advantages on current hardware.

### 4. **Confusing QAOA with Quantum Annealing**
- **QA