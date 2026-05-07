# pair-sampling method

## Definition

The **pair-sampling method** is a statistical sampling technique that estimates a quantity of interest by repeatedly sampling pairs of elements (or representative subsets) from a population and aggregating the results across multiple rounds. In the context of graph algorithms, it involves:

1. Selecting a subset of edges or pairs in each sampling round
2. Computing an estimate from that subset
3. Repeating this process $r$ times and combining estimates
4. Using early termination criteria based on convergence of successive estimates

The method is particularly effective for large-scale graph analysis where full enumeration is computationally prohibitive. It trades accuracy for computational efficiency through controlled sampling.

## Key Equations

Let $G = (V, E)$ be a graph with $m = |E|$ edges. The pair-sampling method operates as follows:

**Single round estimation:**
$$\hat{x}_i = f(S_i)$$

where $S_i$ is a sampled subset in round $i$ and $f$ is an aggregation function.

**Aggregate estimate after $r$ rounds:**
$$\hat{x}_{final} = \frac{1}{r}\sum_{i=1}^{r}\hat{x}_i$$

**Relative error convergence criterion:**
$$\text{RelErr} = \frac{|\hat{x}_{current} - \hat{x}_{previous}|}{\hat{x}_{current}} < \epsilon$$

where $\epsilon$ is a convergence threshold (e.g., $\epsilon = 0.002$ for 0.2% change).

**Subset size scaling:**
$$s_1 \propto \sqrt{m}$$

where $s_1$ is the representative edge subset size per iteration, which scales with the square root of total edges.

## Physical Intuition / Derivation

### Why Pair-Sampling Works

The method exploits the **law of large numbers**: as we aggregate estimates from independent random samples, the variance of the aggregate estimate decreases, while bias can be controlled through proper sampling design.

**Variance reduction mechanism:**
- Each round's sample $S_i$ provides an unbiased (or nearly unbiased) estimate
- Averaging $r$ independent estimates reduces variance by factor of $\sqrt{r}$
- Early termination stops when additional rounds provide diminishing returns

### Intuitive Justification

Consider estimating a graph property (e.g., triangle count). Instead of:
- **Naive approach**: Enumerate all edge pairs → $O(m^2)$ cost
- **Pair-sampling**: Sample $\sqrt{m}$ edges per round for $r$ rounds → $O(r\sqrt{m})$ cost

For $r = 2 \times 10^4$ and large $m$, this is vastly cheaper while maintaining statistical reliability through 90% confidence intervals.

### Batch Processing Strategy

The method processes samples in batches:
$$s_2 = 0.1 \times \sqrt{m}$$

After each batch, check if the estimate changed by less than threshold $\delta$ (e.g., 2%). This adaptive approach prevents unnecessary computation on converged estimates.

## Applications in Engineering

### 1. **Large-Scale Graph Analytics**
- **Social networks**: Estimating clustering coefficients, centrality measures without full computation
- **Web graphs**: Computing PageRank estimates, community structure on billion-edge graphs
- **Biological networks**: Pathway analysis where exhaustive enumeration is infeasible

### 2. **Network Monitoring**
- Real-time statistics collection on high-speed networks
- Sampling packet flows to estimate quality-of-service metrics
- Trading off precision for response time in operations monitoring

### 3. **Machine Learning on Graphs**
- Stochastic gradient descent on graph neural networks
- Efficient mini-batch sampling for node embedding algorithms
- Reducing memory footprint in large-scale GNN training

### 4. **Database Query Optimization**
- Approximate query processing for aggregate statistics
- Join size estimation without full materialization
- Cost-based cardinality estimation for query planning

### 5. **Distributed Computing**
- MapReduce-style sampling for distributed graph algorithms
- Reducing communication overhead by sampling local estimates
- Streaming algorithms for continuous graph updates

## Common Mistakes / Pitfalls

### 1. **Confusing Fixed vs. Adaptive $r$**
**Mistake**: Setting $r$ arbitrarily large thinking "more rounds = better accuracy"
**Reality**: Once estimates converge (change < $\epsilon$), additional rounds waste computation. Adaptive termination is critical.

### 2. **Ignoring Bias from Non-Uniform Sampling**
**Mistake**: Sampling uniformly when the property of interest is non-uniformly distributed
**Reality**: Importance sampling or stratified sampling may be needed; uniform sampling can underestimate rare structures

### 3. **Setting Subset Size Incorrectly**
**Mistake**: Using constant $s_1$ instead of $s_1 \propto \sqrt{m}$
**Reality**: Sublinear scaling ($\sqrt{m}$) is asymptotically optimal; fixed size causes relative error to worsen on larger graphs

### 4. **Not Accounting for Correlation Between Rounds**
**Mistake**: Treating sequential estimates as independent
**Reality**: If samples overlap heavily, variance reduction is sublinear; need independent random sampling

### 5. **Misinterpreting Confidence Intervals**
**Mistake**: "90% confidence interval" means the true value has 90% probability of being in this range
**Reality**: The interval is constructed so that if we repeated the experiment many times, 90% of intervals would contain the true value

## See Also

- [[reservoir sampling]] – Related technique for uniform sampling from streaming data
- [[importance sampling]] – Variance reduction method for non-uniform distributions
- [[Monte Carlo estimation]] – Broader framework for stochastic approximation
- [[early stopping criteria]] – Convergence detection strategies in iterative algorithms
- [[approximate query processing]] – Database application of sampling-based estimation

## Sources

- Paper excerpt on WPS (Weighted Pair-Sampling) and TLS (Three-Layer Sampling) algorithm comparison
- Experimental results on Wikipedia graph datasets showing 85-99% reduction in query/time costs
- Parameter tuning discussion: $r = 2 \times 10^4$ rounds, $s_1 = 0.5\sqrt{m}$, batch size $0.1\sqrt