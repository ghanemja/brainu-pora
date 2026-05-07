# Batch Sampling

## Definition

**Batch sampling** is a computational technique that processes data or performs iterative estimation in groups (batches) of fixed or adaptive size, rather than element-by-element. It combines multiple independent sample draws within each batch and uses convergence criteria to terminate sampling when estimate changes fall below specified thresholds.

In the context of graph analytics and Monte Carlo estimation, batch sampling structures the sampling process hierarchically:
- **Inner batches** (size $s_2$): Group elementary samples collected in each iteration
- **Outer rounds** (count $r$): Multiple complete sampling cycles
- **Termination strategy**: Stop when the marginal contribution of a new batch falls below a tolerance threshold

## Key Equations

For a batch sampling estimator with convergence monitoring:

$$\hat{\theta}_{\text{iter}} = \frac{1}{r} \sum_{i=1}^{r} \hat{\theta}_i^{(s_2)}$$

where $\hat{\theta}_i^{(s_2)}$ is the estimate from the $i$-th outer round, computed using $s_2$ inner samples.

**Relative error stopping criterion (inner loop):**
$$\frac{|\hat{\theta}_{k} - \hat{\theta}_{k-1}|}{\hat{\theta}_{k}} < \delta_{\text{inner}}$$

where $\delta_{\text{inner}}$ is the tolerance (e.g., 2%) and $k$ indexes successive batches.

**Relative error stopping criterion (outer loop):**
$$\frac{|\hat{\theta}_{\text{round}} - \hat{\theta}_{\text{round}-1}|}{\hat{\theta}_{\text{round}}} < \delta_{\text{outer}}$$

where $\delta_{\text{outer}}$ is the outer tolerance (e.g., 0.2%).

**Batch size scaling (for graphs):**
$$s_1, s_2 \propto \sqrt{m}$$

where $m$ is the edge count, providing sublinear sampling cost relative to graph size.

## Physical Intuition / Derivation

### Why Batching?

Element-by-element sampling incurs high overhead: repeated convergence checks, context switching, and poor cache locality. Batching amortizes this overhead by:

1. **Grouping work**: Process $s_2$ samples in one loop, check convergence once
2. **Adaptive termination**: Rather than fixed sample budgets, stop when uncertainty plateaus
3. **Variance reduction**: Averaging within batches reduces per-estimate variance
4. **Hierarchical control**: Inner batches refine estimates; outer rounds provide robustness

### Convergence Mechanism

The stopping criteria exploit the **diminishing returns** property of Monte Carlo estimation. Early batches reduce error rapidly; later batches provide marginal gains. By monitoring relative change:

$$\text{Change}_k = \left|\hat{\theta}_k - \hat{\theta}_{k-1}\right|$$

we detect the plateau in error reduction. When $\text{Change}_k < \delta \cdot \hat{\theta}_k$, continued sampling is inefficient—computational cost grows faster than error reduction improves.

### Sublinear Scaling

Setting batch sizes as $s_1, s_2 \sim \sqrt{m}$ achieves **sublinear sampling complexity**. For a graph with $m$ edges, instead of sampling $O(m)$ edges, we sample $O(\sqrt{m})$ per iteration. With automatic termination, total cost becomes $O(r \cdot \sqrt{m})$ where $r \ll m$ in practice (empirically 85–95% cost reduction vs. fixed-budget methods).

## Applications in Engineering

### 1. **Graph Analytics & Network Sampling**
Graph algorithms (shortest paths, centrality, clustering) often require expensive traversals. Batch sampling estimates graph properties (triangle counts, densities) using $O(\sqrt{m})$ samples per round with early stopping, enabling real-time queries on billion-edge graphs.

### 2. **Monte Carlo Integration & Uncertainty Quantification**
Engineering simulations (structural mechanics, fluid dynamics) use batch sampling to estimate expectations of expensive functions. Adaptive batch sizes balance accuracy against computational budget, critical when each function evaluation requires hours of FEA or CFD.

### 3. **A/B Testing & Experimentation**
Online platforms (e-commerce, social media) employ batch sampling to decide when to stop experiments. Inner batches collect user interactions; outer rounds (daily or weekly) check if improvement is significant. Early stopping saves resources while controlling false discovery rate.

### 4. **Quality Control & Acceptance Sampling**
Manufacturing inspects batches of products. Batch sampling sequences decide whether to accept a lot based on cumulative defect rates, balancing inspection cost against risk of shipping defects.

### 5. **Stochastic Optimization**
SGD variants use batch sampling: mini-batches accumulate gradients; termination strategies check for convergence in validation loss. Larger batches stabilize updates; adaptive stopping prevents overfitting.

## Common Mistakes / Pitfalls

### 1. **Confusing Batch Size with Number of Batches**
Increasing batch size $s_2$ does *not* automatically reduce total samples if outer rounds $r$ remain fixed. The interaction matters: large $s_2$ with loose stopping criteria may sample more than necessary; small $s_2$ with tight criteria may terminate prematurely.

### 2. **Setting Tolerances Too Aggressively**
Setting $\delta_{\text{inner}} = 0.1\%$ or $\delta_{\text{outer}} = 0.01\%$ chases diminishing returns. Late-stage sampling contributes negligibly; tighter criteria increase computational cost without proportional error reduction. Best practice: choose tolerance based on acceptable relative error in the final estimate, not arbitrary precision targets.

### 3. **Ignoring Batch Size Scaling**
Fixed batch sizes (e.g., $s_2 = 100$ for all graphs) are inefficient. Small graphs waste computation; large graphs under-sample. The $\sqrt{m}$ scaling adapts naturally to problem size, enabling consistent relative error across inputs.

### 4. **Not Monitoring Variance in Batches**
A batch with 50% higher variance than previous batches may indicate distribution shift or outlier effects. Blindly averaging low-variance and high-variance batches inflates confidence intervals.