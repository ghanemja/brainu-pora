# Ising model

## Definition

The Ising model is a fundamental probabilistic graphical model that defines a probability distribution over binary-valued variables (typically taking values in $\{\pm 1\}$ or $\{0,1\}$). It captures how variables interact with one another through pairwise interactions and external influences, and is foundational in statistical physics, machine learning, and applied engineering.

Formally, the Ising model specifies a probability distribution $\mu(\sigma)$ over configurations $\sigma \in \{\pm 1\}^n$ as:

$$\mu(\sigma) = \frac{1}{Z} \exp\left(-\frac{1}{2}\sigma^\top A\sigma + h^\top\sigma\right)$$

where:
- $\sigma \in \{\pm 1\}^n$ is a configuration (assignment of binary values to $n$ variables)
- $A \in \mathbb{R}^{n \times n}$ is the **interaction matrix** (symmetric), where $A_{ij}$ encodes the strength of interaction between variables $i$ and $j$
- $h \in \mathbb{R}^n$ is the **external field vector**, where $h_i$ represents external influence on variable $i$
- $Z = \sum_{\sigma \in \{\pm 1\}^n} \exp\left(-\frac{1}{2}\sigma^\top A\sigma + h^\top\sigma\right)$ is the **partition function**, a normalization constant ensuring $\sum_\sigma \mu(\sigma) = 1$

The model naturally encodes a **dependence graph** $G = ([n], E)$ where $(i,j) \in E$ if and only if $A_{ij} \neq 0$—that is, edges represent direct interactions between variables.

## Key Equations

**Energy (Hamiltonian):**
$$H(\sigma) = -\frac{1}{2}\sigma^\top A\sigma + h^\top\sigma$$

The probability is inversely proportional to energy: lower-energy configurations are more probable.

**Partition function (full sum):**
$$Z = \sum_{\sigma} \exp\left(\frac{1}{2}\sigma^\top A\sigma - h^\top\sigma\right)$$

**Marginal probability of variable $i$:**
$$P(\sigma_i = s) = \frac{\sum_{\sigma: \sigma_i = s} \exp\left(-\frac{1}{2}\sigma^\top A\sigma + h^\top\sigma\right)}{Z}$$

**Conditional distribution (conditioning on set $T \subseteq [n]$):**
$$P(\sigma_S | \sigma_T) \propto \exp\left(-\frac{1}{2}\sigma^\top A\sigma + h^\top\sigma\right)$$
where the exponent is evaluated with fixed values on $T$.

## Physical Intuition / Derivation

### Origin in Statistical Physics

The Ising model originated from condensed matter physics (Lenz, Ising, 1920s) to model ferromagnetism. Consider a lattice of atomic spins, each pointing up or down ($\pm 1$). The model captures:

1. **Interaction energy**: Neighboring spins prefer to align (ferromagnetic coupling, $A_{ij} < 0$) or anti-align (antiferromagnetic, $A_{ij} > 0$)
2. **External field**: A uniform magnetic field applies pressure in one direction

The Gibbs-Boltzmann distribution naturally arises when a system reaches thermal equilibrium at temperature $T$:
$$P(\sigma) \propto \exp\left(-\frac{E(\sigma)}{k_B T}\right)$$

Setting $k_B T = 1$ for simplicity gives the standard form above.

### Why This Functional Form?

The exponential form emerges from statistical mechanics: when a system can exchange energy with a heat reservoir, configurations with lower energy become exponentially more probable. The quadratic form $\sigma^\top A\sigma$ captures pairwise interactions because:
- Each pair $(i,j)$ contributes $A_{ij}\sigma_i\sigma_j$ to the energy
- When $A_{ij} > 0$: aligned spins (same sign) lower energy
- When $A_{ij} < 0$: anti-aligned spins lower energy
- Linear term $h_i\sigma_i$: external bias favors positive or negative values

### Strong Spatial Mixing

A key structural property is **strong spatial mixing (SSM)**: pinning variables far apart in the graph has negligible effect on each other's marginal distributions. Formally, for distant sets $S$ and $T$:
$$\left|\mu(\sigma_S = a | \sigma_T = b) - \mu(\sigma_S = a | \sigma_T = b')\right| \leq \text{decay in distance}(S,T)$$

This property ensures the system is not in a critical/phase-transition regime and enables efficient sampling and learning algorithms.

## Applications in Engineering

### 1. Statistical Physics & Materials Science
- **Ferromagnetism modeling**: Predicting phase transitions in magnetic materials
- **Alloy design**: Understanding order-disorder transitions in binary alloys
- **Lattice systems**: Canonical model for discrete spin systems

### 2. Machine Learning & Inference
- **Restricted Boltzmann Machines (RBMs)**: Deep learning architectures use Ising-like energy functions
- **Graphical model learning**: Learning interaction structure and parameters from observational data
- **Belief propagation & message passing**: Efficient inference algorithms exploit Ising structure
- **Sampling**: MCMC methods (Gibbs sampling, Metropolis-Hastings) for probabilistic inference

### 3. Computer Vision
- **Image restoration**: Variables represent pixel labels; interactions encode smoothness priors
- **Texture synthesis**: Modeling spatial correlations in natural images
- **Stereo vision & depth estimation**: Pairwise interaction models enforce smoothness

### 4. Combinatorial Optimization
- **Spin glass models**: NP-hard optimization via Ising formulation (e.g., MAX-CUT, graph coloring)
- **Constraint satisfaction**: Encoding SAT/CSP problems as Ising instances
- **Quantum