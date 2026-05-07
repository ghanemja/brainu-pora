# Strong Spatial Mixing

## Definition

**Strong Spatial Mixing (SSM)** is a property of graphical models (probabilistic models with dependencies represented by graphs) that quantifies how quickly correlations decay as a function of spatial distance.

Formally, a marginally bounded graphical model $\mu$ satisfies strong spatial mixing if correlations between variables become exponentially small as the graph distance between them increases. For a dependence graph $G = (V, E)$ with variables indexed by vertices, strong spatial mixing ensures that the influence of conditioning a variable at one location on variables far away decays rapidly—typically exponentially—with distance.

**Key Characterization**: A graphical model exhibits SSM when:
- For any two disjoint sets of variables $A$ and $B$ with graph distance $d(A,B)$, the mutual information or total variation distance between conditional distributions decays as $\exp(-\Omega(d(A,B)))$.
- This decay is uniform across the state space of the model.

## Key Equations

$$\text{For sets } A, B \text{ with distance } d = d(A,B):$$

$$\left|\mu(x_A | x_B) - \mu(x_A)\right| \leq \text{poly}(|A|) \cdot \exp(-\Omega(d))$$

For a local iterative sampler with output partition $\{S_1, \ldots, S_K\}$:

$$P(\text{InvSamp}_i(y) = z_i \mid y) = P(\text{InvSamp}_i(y) = z_i \mid y_{T_i})$$

where $T_i$ denotes the polylog$(n)$-sized neighborhood of dependencies for coordinate $i$.

## Physical Intuition / Derivation

### Why SSM Matters

Strong spatial mixing captures the intuition that **distant parts of a system are nearly independent**. This is fundamentally important because:

1. **Localization of Information**: Information about variables far away becomes negligible, meaning local information suffices to characterize local behavior.

2. **Constructive Sampling**: Rather than needing global knowledge to sample variables, SSM enables **local iterative sampling**:
   - Partition outputs into sequential blocks $S_1, S_2, \ldots, S_K$
   - Sample each block conditioned only on polylog$(n)$ previously sampled outputs
   - This works because SSM guarantees variables outside this neighborhood have vanishing influence

3. **Efficient Inversion**: The key insight (Claim 2.5) is that under SSM with local iterative samplers:
   - Each local seed $z_i$ becomes **conditionally independent** of other seeds given the output $y$
   - Once $y_i$ is determined, no further dependence on $z_i$ propagates forward
   - Therefore: $\Samp^{-1}(y) = \bigotimes_{i=1}^n \Samp_i^{-1}(y_i; y_{T_i})$

### Constructive View

```
[SSM structure]
    Variable at position i
              ↓
    ┌─────────┴─────────┐
    │                   │
  Local             Exponentially decaying
  correlations      influence to distance d
  (polylog range)
```

The **local iterative sampler** exploits SSM by:
1. Sampling $y_i$ from $\mu_i(\cdot | y_{T_i})$ where $T_i$ = polylog$(n)$-sized conditioning set
2. Using rejection sampling to invert: find $z_i$ such that $\Samp_i(z_i; y_{T_i}) = y_i$
3. Because of SSM, $P(\text{accept}) \geq \text{poly}^{-1}(n)$ on average

## Applications in Engineering

### 1. **Probabilistic Inference in Graphical Models**
- **Markov Random Fields**: SSM enables efficient approximate inference on spatial/lattice-structured models (images, sensor networks)
- **Belief Propagation**: SSM guarantees rapid convergence of belief propagation algorithms; distant messages become negligible
- **Example**: Particle filters for robot localization benefit from SSM in spatial motion models

### 2. **Approximate Sampling & Inference**
- **Markov Chain Monte Carlo (MCMC)**: SSM implies fast mixing times for local MCMC samplers on grid-like or sparse graphs
- **Variational Methods**: SSM validates mean-field approximations and local variational bounds
- **Gibbs Sampling**: Restricted Gibbs updates (conditioning on neighborhood) remain near-optimal when SSM holds

### 3. **Sparse Recovery & Compressed Sensing**
- **Structured Sparsity**: Graphical models with SSM capture spatial correlation in sparse signals; enables efficient recovery
- **Optimal Decoding**: SSM structure in error-correcting codes (e.g., LDPC codes on expander graphs) guarantees efficient decoders

### 4. **Machine Learning & Statistical Physics**
- **Phase Transitions**: SSM typically holds away from critical points; failure of SSM signals phase transitions in statistical physics models
- **Learning Graphical Models**: SSM conditions ensure learnability of model parameters from samples

### 5. **Distributed Computing & Message Passing**
- **Distributed Algorithms**: SSM enables gossip algorithms and consensus protocols on graphs; locality ensures polylog communication
- **Network Optimization**: Decentralized optimization leverages SSM to avoid global synchronization

## Common Mistakes / Pitfalls

### 1. **Confusing SSM with Markov Property**
- **Wrong**: "A Markov Random Field automatically satisfies SSM"
- **Right**: Markov property only implies nearest-neighbor independence; SSM requires *exponential decay* of long-range correlations
- **Example**: A grid MRF with attractive long-range interactions may be Markov but fail SSM

### 2. **Ignoring the Dependence Graph Structure**
- **Wrong**: Applying local iterative samplers to arbitrary graphs
- **Right**: SSM requires careful graph structure; dense graphs (complete graphs) violate SSM
- **Requirement**: Dependence graph must have **polynomial growth** (e.g., lattices, trees