# Variance Analysis

## Definition

**Variance analysis** is a statistical technique for controlling and bounding the variance of estimators in algorithms, particularly in streaming and sampling-based computational models. In the context of subgraph counting and graph algorithms, variance analysis involves:

1. **Identifying dependencies** among sampled elements (nodes, edges, subgraphs) that contribute to estimator variance
2. **Isolating high-variance contributions** by excluding or separately handling elements that participate in disproportionately many occurrences of the target structure
3. **Establishing individual thresholds** (rather than uniform thresholds) based on sampling probabilities and structural properties
4. **Bounding total variance** to ensure estimator concentration around the true value

In particular, variance analysis is critical when sampling probabilities are non-uniform or when the structure being counted exhibits high correlation—such as four-cycles appearing in overlapping neighborhoods.

## Key Equations

### Basic Variance Decomposition

For an estimator $\hat{X}$ based on sampling:

$$\text{Var}[\hat{X}] = \mathbb{E}[\hat{X}^2] - (\mathbb{E}[\hat{X}])^2$$

### Contribution to Variance from Correlated Samples

When multiple samples contribute to a single count, the variance depends on covariance terms:

$$\text{Var}[\hat{X}] = \sum_i \text{Var}[X_i] + 2\sum_{i<j} \text{Cov}[X_i, X_j]$$

where $X_i$ are contributions from individual sampled units.

### Heavy Element Threshold (Sampling-Dependent)

For element $u$ sampled with probability $p_u$, define heaviness $h_u$ as the count of target structures containing $u$. Element $u$ is declared heavy if:

$$h_u > \tau_u$$

where the threshold $\tau_u$ is **dependent on sampling probability $p_u$**, not uniform across the graph. Typically:

$$\tau_u \propto \frac{1}{p_u} \quad \text{or} \quad \tau_u \propto \sqrt{\frac{1}{p_u}}$$

This ensures that high-variance contributions are removed while maintaining unbiasedness or bounded bias.

### Space-Variance Tradeoff

In streaming models with $T$ passes, the space-variance tradeoff is:

$$\text{Space} \propto \frac{m}{\sqrt{T}} \quad \Leftrightarrow \quad \text{Var}[\hat{X}] \text{ is controlled}$$

where $m$ is the number of edges. More passes allow lower sampling rates, which reduce variance.

## Physical Intuition / Derivation

### Why Variance Control Matters

In **streaming algorithms** and **sampling-based estimators**, the fundamental challenge is that we do not observe the entire graph—we see only a random sample. When counting structures like four-cycles:

- Not all four-cycles are equally likely to be sampled
- Some nodes or edges participate in *many* four-cycles
- If we sample an edge adjacent to a high-degree node, we "pick up" many four-cycles at once
- This creates **high variance**: the estimator fluctuates wildly depending on which high-density region is sampled

### The Heavy Element Principle

Uniform heaviness thresholds (used in prior work) define a node $v$ as heavy if $h_v > \tau$ for some fixed $\tau$. However, this is insufficient when sampling probabilities vary:

- A node sampled with low probability $p_u$ acts as a **bottleneck**: each sample of $u$ reveals many four-cycles
- The variance contribution is proportional to $(h_u / p_u)^2$—the "amplification" effect
- Setting a uniform threshold fails to account for this amplification

**Solution**: Define individual thresholds $\tau_u(p_u)$ such that:
$$\text{Var}[\text{contribution from } u] \leq \text{allowable variance budget}$$

This scales the threshold inversely with sampling probability: nodes sampled rarely must be more "selective" about which four-cycles they contribute to the count.

### Refined Heaviness and Overcounting Control

The refined notion of heaviness addresses a practical constraint: **computing the true heaviness $h_u$ requires multiple passes or extra space**, violating the target space bound.

Instead, use a computable surrogate (e.g., degree-based or neighborhood-based estimates) that:
- Over-approximates true heaviness: $\tilde{h}_u \geq h_u$
- Remains efficient to compute
- Leads to some four-cycles being marked as heavy (and excluded) when they shouldn't be

The key insight: **overcounting affects only an $\varepsilon$-fraction** of all four-cycles if $\varepsilon$ is set appropriately. This small error is absorbed into the final error bounds.

## Applications in Engineering

### 1. **Streaming Graph Analytics**
- **Subgraph counting** in dynamic networks (social networks, transaction graphs, web graphs)
- **Motif detection** to identify recurring patterns or anomalies
- **Space-efficient monitoring** with multiple passes over the data stream

### 2. **Distributed Systems**
- **MapReduce-style graph processing**: variance analysis guides batch sizes and sampling rates
- **Federated learning**: controlling variance of model updates across non-IID data samples
- **Database query optimization**: estimating subgraph counts without full scans

### 3. **Network Analysis & Security**
- **Detecting dense subgraph structures** (cliques, cycles) indicative of malicious behavior (bot networks, fraud rings)
- **Botnet and fraud ring detection**: four-cycles appear frequently in coordinated behavior
- **Link prediction**: variance-controlled sampling reduces false positives/negatives

### 4. **Machine Learning (SGD and Sampling)**
- **Stochastic gradient descent**: variance of gradient estimators depends on minibatch sampling probabilities
- **Importance sampling**: non-uniform sampling requires adaptive variance thresholds for efficiency
- **Variance reduction techniques** (e.g., control variates) rely on variance decomposition

### 5. **Approximate Computing**
- **Cardinality estimation**: HyperLogLog and similar sketching algorithms