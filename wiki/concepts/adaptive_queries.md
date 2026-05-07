# Adaptive Queries

## Definition

**Adaptive queries** are information-theoretic requests made to a system (typically an algorithm or oracle) where each query can depend on the results of all previous queries. This contrasts with non-adaptive (batch) queries, where all queries must be specified in advance without knowledge of prior responses.

In the context of **diffusion sampling**, adaptive queries refer to successive evaluations of learned score estimates $\nabla \log p_t(\mathbf{x})$ at different noise levels and data points, where the choice of which noise level and location to query next depends on information from previous score evaluations. The algorithm adaptively determines the sequence of queries rather than following a predetermined schedule.

### Formal Distinction
- **Non-adaptive:** Query set $\{q_1, q_2, \ldots, q_n\}$ specified before seeing any responses
- **Adaptive:** Query $q_i$ chosen after observing responses $\{r_1, \ldots, r_{i-1}\}$ to previous queries

## Key Equations

For $d$-dimensional diffusion sampling with polynomial accuracy score estimates $\varepsilon = d^{-O(1)}$, the **lower bound on adaptive score queries** is:

$$\text{# queries} = \tilde{\Omega}(\sqrt{d})$$

where $\tilde{\Omega}$ denotes the Omega notation with logarithmic factors suppressed.

### Sampling Trajectory in Diffusion Models

The generative process iteratively denoises via the diffusion SDE or discrete update:

$$\mathbf{x}_t = \mathbf{x}_{t+1} - \eta_t \nabla \log p_t(\mathbf{x}_{t+1}) + \text{noise}$$

where:
- $t$ indexes noise level (time in reverse diffusion)
- $\eta_t$ is the step size
- Each $\nabla \log p_t(\mathbf{x})$ evaluation is one **adaptive query**

The bound implies:

$$\text{# distinct noise levels queried} = \tilde{\Omega}(\sqrt{d})$$

## Physical Intuition / Derivation

### Why Adaptive Queries Matter in Diffusion Sampling

1. **Information bottleneck:** Each score query provides limited information (a single gradient vector in $\mathbb{R}^d$). To navigate a $d$-dimensional space with polynomial accuracy, roughly $\sqrt{d}$ scales of exploration are necessary—finer granularity requires more intermediate noise levels.

2. **Multiscale necessity:** The lower bound formalizes an empirical observation: successful diffusion models use multiscale noise schedules (coarse → fine resolution). Adaptive query selection forces exploration across $\sqrt{d}$ distinct noise levels because:
   - Low noise levels provide fine geometric detail
   - High noise levels provide coarse structure
   - Intermediate levels are essential for smooth interpolation

3. **Why $\sqrt{d}$ and not $d$?** This appears to reflect a subtle geometry of high-dimensional denoising:
   - The "cost" of moving from noise level $\sigma_1$ to $\sigma_2$ scales with the distance traveled
   - Optimal progression requires $\sqrt{d}$ multiplicative noise-level steps
   - This is related to how manifold complexity grows with dimension

### Connection to Existing Theory

Prior work established:
- **Upper bound:** $\tilde{O}(d)$ queries suffice for sampling with bounded second moments
- **This work:** Lower bound of $\tilde{\Omega}(\sqrt{d})$ shows the $d$ upper bound is *not tight*
- **Gap:** Whether the true bound is $\Theta(\sqrt{d})$ or somewhere between remains open

## Applications in Engineering

### 1. Generative Model Design
- **Image/video synthesis:** Determining minimum score queries for acceptable quality requires understanding these bounds; helps allocate computational budgets
- **Flow matching:** Justifies why flow-matching acceleration techniques must span multiple noise scales to match theoretical lower bounds

### 2. Neural Architecture Optimization
- **Sampler design:** Engineers designing diffusion samplers can benchmark against the $\sqrt{d}$ lower bound to assess algorithmic efficiency
- **Step-size schedules:** Optimal discretization spacing should respect the $\sqrt{d}$ noise-level requirement

### 3. Hardware Acceleration
- **GPU/TPU scheduling:** Since $\sqrt{d}$ queries are unavoidable, hardware designers must ensure efficient score network evaluation for 100–300 separate forward passes (typical $d$ ranges from $10^4$ to $10^6$)
- **Computational bottleneck:** Confirms that score network inference, not data movement, dominates latency

### 4. Sampling for Scientific Computing
- **PDE solvers, uncertainty quantification:** Diffusion models increasingly sample from Bayesian posteriors and PDEs; the $\sqrt{d}$ bound clarifies computational cost for high-dimensional parameter spaces ($d = 10^3$ to $10^6$)

### 5. Algorithm Certification
- **Verification:** Claim that a sampler uses fewer than $\sqrt{d}$ queries becomes a falsifiable theoretical claim—useful for auditing claimed speedups

## Common Mistakes / Pitfalls

### 1. Confusing Query Complexity with Wall-Clock Time
**Error:** Assuming $\sqrt{d}$ lower bound means sampling is infeasible.  
**Reality:** $\sqrt{d}$ queries is *per sample*. For $d=10^6$, this is ~1000 queries—expensive but manageable. Actual runtime depends on network architecture and hardware parallelism.

### 2. Assuming the Bound Applies to All Noise Schedules
**Error:** Thinking any fixed schedule of $\sqrt{d}$ noise levels suffices.  
**Reality:** The bound applies to *adaptive* choice of noise levels. A fixed schedule may require more queries; adaptivity is essential to achieve the lower bound.

### 3. Misinterpreting "Polynomial Accuracy" Requirements
**Error:** Assuming $\varepsilon = d^{-O(1)}$ is a loose or impractical assumption.  
**Reality:** For high-dimensional distributions, polynomial accuracy (e.g., $L_2$ error $\sim 1/d$) is the natural regime. The bound is tight to the regime where diffusion models operate