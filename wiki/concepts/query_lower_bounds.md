# Query Lower Bounds

## Definition

**Query lower bounds** establish fundamental information-theoretic limits on the minimum number of oracle queries (function evaluations) required to solve a computational problem within a specified accuracy. In the context of diffusion-based sampling, a query lower bound quantifies the irreducible number of score function evaluations needed to generate samples from a target distribution.

Formally, a query lower bound proves that for *any* algorithm solving a problem class, there exists an instance requiring at least $f(d, \varepsilon, \delta)$ queries, where:
- $d$ = problem dimension or complexity measure
- $\varepsilon$ = target accuracy (e.g., total variation distance, Wasserstein distance)
- $\delta$ = failure probability

This contrasts with **upper bounds**, which show that specific algorithms achieve a goal in at most $g(d, \varepsilon, \delta)$ queries.

## Key Equations

### Score Query Lower Bound (Diffusion Sampling)

For $d$-dimensional distributions with access to score estimates of polynomial accuracy $\varepsilon = d^{-O(1)}$ (in any $L^p$ norm):

$$\text{Query Complexity} = \tilde{\Omega}(\sqrt{d})$$

where $\tilde{\Omega}$ hides logarithmic factors.

### Connection to Noise Schedule Search

The lower bound implies that any sampler must search over:

$$\text{Distinct Noise Levels} = \tilde{\Omega}(\sqrt{d})$$

This formalizes the empirical observation that multiscale noise schedules are necessary.

## Physical Intuition / Derivation

### Why Lower Bounds Matter

Query complexity analysis separates *feasible* from *infeasible* acceleration strategies. If an algorithm uses $k$ queries and $k$ exceeds the proven lower bound, the algorithm is optimal (up to log factors). Conversely, if $k$ exceeds the lower bound, further improvement is information-theoretically impossible.

### Core Intuition: Covering Argument

The proof strategy for diffusion query lower bounds rests on a **geometric covering argument**:

1. **High-dimensional geometry problem**: Sampling from a $d$-dimensional distribution requires exploring a space of exponential volume. Without adaptive queries, the algorithm must "commit" to search strategies globally.

2. **Noise level discretization**: Diffusion sampling progressively denoises via a path parameterized by noise level $\sigma(t)$. Each noise level explores a different "scale" of the distribution. To locate and resolve structure at all relevant scales, an algorithm must query:
   - Very noisy intermediate stages (to navigate coarse structure)
   - Low-noise stages (to resolve fine structure)
   - Intermediate scales (to bridge them)

3. **Dimensional amplification**: In $d$ dimensions, the "number of distinct scales" needed grows as $\sqrt{d}$ because:
   - Typical distances scale as $\sqrt{d}$ (volume concentration)
   - Noise diffusion spreads information across scales logarithmically with dimension
   - Coupling them via diffusion PDEs requires $\sqrt{d}$ "resolution steps"

### Technical Building Block: Adversarial Instance

The lower bound proof constructs a specific "hard" distribution family and shows that:
- Any adaptive query algorithm must distinguish between instances differing at various scales
- Worst-case distributions force exploration of $\tilde{\Omega}(\sqrt{d})$ distinct regimes
- Even with perfect score estimates, geometric necessity enforces this limit

## Applications in Engineering

### 1. **Generative Model Design**
- **Sampling algorithm certification**: Engineers can verify whether proposed fast samplers (e.g., DDIM, flow matching) approach theoretical limits
- **Architecture decisions**: Determines feasibility of single-shot generation (would require $O(1)$ queries, provably impossible)

### 2. **Computational Resource Allocation**
- **Hardware budgeting**: Given a query budget (GPU memory, latency constraints), $\tilde{\Omega}(\sqrt{d})$ sets the minimum cost for guaranteed accuracy across all problem dimensions
- **Model scaling laws**: Predicts query cost growth when moving from 2D toy problems to high-resolution image generation (e.g., $512 \times 512 \times 3$)

### 3. **Neural Network Optimization**
- **Score network design**: Informs decisions about network depth/width—since $\sqrt{d}$ queries are required anyway, one can afford expensive per-query computation
- **Warm-start strategies**: Justifies using cached intermediate models at different noise scales

### 4. **Scientific Computing**
- **PDE/uncertainty quantification sampling**: When sampling from Bayesian posteriors ($d$ = parameter dimension), lower bounds inform the minimum ensemble size needed
- **Inverse problem design**: Guides whether iterative refinement is necessary or sufficient

### 5. **Practical Acceleration Limits**
- **Algorithm benchmarking**: Distinguishes between algorithmic improvements and fundamental speedup walls
- **Research direction assessment**: Shows that below $\tilde{\Omega}(\sqrt{d})$ queries, fundamentally new ideas (beyond better solvers) are needed

## Common Mistakes / Pitfalls

### 1. **Confusing Upper and Lower Bounds**
**Mistake**: Claiming "diffusion sampling requires $O(d)$ queries" when the literature shows $\tilde{O}(d)$ *upper* bound and $\tilde{\Omega}(\sqrt{d})$ *lower* bound.

**Correction**: Upper bounds say "this algorithm works in $\approx d$ queries." Lower bounds say "any algorithm needs $\approx \sqrt{d}$ queries minimum." There is a gap—space for improvement exists.

### 2. **Ignoring Problem Class Dependencies**
**Mistake**: Applying the $\tilde{\Omega}(\sqrt{d})$ bound to distributions with special structure (e.g., low-rank, sparse).

**Correction**: Query lower bounds apply to the *worst case* over a distribution class. Specialized structure may enable faster algorithms. Lower bounds must be re-derived for restricted classes.

### 3. **Overlooking Accuracy Dependencies**
**Mistake**: Thinking the bound $\tilde{\Omega}(\sqrt{d})$ is constant regardless of desired accuracy $\varepsilon$.

**Correction**: The bound applies at polynomial accuracy $\varepsilon = d^{-O(1)}$