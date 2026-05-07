# Gibbs Sampling

## Definition

**Gibbs sampling** is a Markov Chain Monte Carlo (MCMC) method for generating samples from a multivariate probability distribution when direct sampling is intractable. The sampler sequentially draws each variable from its conditional distribution given the current values of all other variables.

Formally, given a target distribution $\pi(\mathbf{x})$ over variables $\mathbf{x} = (x_1, x_2, \ldots, x_n)$, Gibbs sampling at iteration $t$ updates each variable by:

$$x_i^{(t)} \sim \pi(x_i \mid x_1^{(t)}, \ldots, x_{i-1}^{(t)}, x_{i+1}^{(t-1)}, \ldots, x_n^{(t-1)})$$

This is repeated cyclically or randomly over all variables until convergence to the stationary distribution.

## Key Equations

**Conditional Distribution Update:**
$$P(x_i \mid x_{\setminus i}) = \frac{\pi(\mathbf{x})}{\sum_{x_i'} \pi(x_i', x_{\setminus i})}$$

where $x_{\setminus i}$ denotes all variables except $x_i$.

**Stationary Distribution (Detailed Balance):**
For a properly constructed Gibbs sampler:
$$\pi(\mathbf{x}) P(\mathbf{x} \to \mathbf{x}') = \pi(\mathbf{x}') P(\mathbf{x}' \to \mathbf{x})$$

This ensures the Markov chain has $\pi$ as its stationary distribution.

**Mixing Time:** For efficient sampling, the chain must reach near-stationarity in polynomial time. Key results include:
- **Uniqueness regime**: Glauert dynamics mixes in $O(\text{poly}(n))$ steps (proven via spectral gap bounds)
- **Non-uniqueness regime**: NP-hardness barriers exist—Gibbs sampling is intractable unless NP = RP
- **Critical threshold**: Recent breakthroughs [CCYZ25] show polynomial mixing at criticality for general graphs using localization schemes

## Physical Intuition / Derivation

Gibbs sampling exploits the **factorization structure** of graphical models. When the joint distribution factors according to a dependency graph, conditioning on neighbors makes conditional distributions tractable to compute.

**Why it works:**
1. Each conditional update preserves the stationary distribution (detailed balance)
2. Iterating these updates ergodically explores the support of $\pi$
3. After sufficient iterations (mixing time $\tau_{\text{mix}}$), samples are approximately drawn from $\pi$

**Connection to Physics:** In statistical mechanics contexts (e.g., Ising models, spin systems), Gibbs sampling corresponds to **Glauber dynamics**, where variables represent spins. At each step, a spin flips with probability determined by its interaction energy with neighbors—a stochastic process that naturally equilibrates to the Boltzmann distribution.

**Key Insight on Mixing:** The mixing time depends critically on whether the system exhibits **phase transitions**:
- *Uniqueness regime* (away from criticality): Conditional distributions are robust; mixing is fast
- *Non-uniqueness regime* (at criticality): Multiple competing configurations become nearly equally likely; local updates mix slowly due to entropic barriers

## Applications in Engineering

### 1. **Bayesian Inference & Machine Learning**
   - Sampling from posterior distributions in Bayesian neural networks and hierarchical models
   - Variational inference alternatives when exact posteriors are intractable
   - Structure learning in graphical models

### 2. **Statistical Physics & Materials Science**
   - Simulating Ising spin systems to study magnetic phase transitions
   - Estimating partition functions and free energies
   - Monte Carlo studies of antiferromagnetic materials and lattice models

### 3. **Image Processing & Computer Vision**
   - Denoising and inpainting via Markov Random Field priors
   - Texture synthesis and image reconstruction
   - Sampling from conditional distributions in spatial models

### 4. **Network & System Reliability**
   - Sampling network configurations for reliability analysis
   - Inferring hidden system states from observations in reliability networks

### 5. **Operations Research**
   - Sampling combinatorial structures (matchings, colorings) in optimization
   - Approximate counting via MCMC samplers

## Common Mistakes / Pitfalls

1. **Ignoring Burn-in:** Assuming the first few samples are from $\pi$. The chain must be allowed to converge before collecting samples; discarding the first $B \gg 1$ iterations (burn-in) is essential.

2. **Confusing Convergence with Mixing:** Theoretical convergence ($t \to \infty$) differs from practical mixing time. An empirically "converged-looking" trace may still suffer high autocorrelation.

3. **Assuming Fast Mixing Without Proof:** Not all Gibbs samplers mix rapidly. Near phase transitions (especially in non-uniqueness regimes), mixing can be exponentially slow. Hardness results [Sly10, SS12] show NP-hardness barriers for some systems.

4. **Underestimating Critical Behavior:** Systems at critical thresholds (e.g., the Ising model at $\beta = \beta_c$) have qualitatively different mixing behavior. Only recent advances [CCYZ25] have shown polynomial mixing at criticality for general graphs.

5. **Ignoring Autocorrelation:** Even after burn-in, successive samples are correlated. Effective sample size is $N_{\text{eff}} = N / \tau_{\text{autocorr}}$, where $\tau_{\text{autocorr}}$ can be large for poorly mixed chains.

6. **Inappropriate Variable Ordering:** While (standard) Gibbs sampling is order-independent in theory, poorly chosen orderings can increase mixing time in practice. Adaptive or random-scan orderings often perform better.

## See Also

- [[Markov Chain Monte Carlo (MCMC)]] – broader framework of which Gibbs sampling is a special case
- [[Glauber Dynamics]] – the physics interpretation of Gibbs sampling on spin systems
- [[Spectral