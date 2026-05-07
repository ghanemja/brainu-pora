# Competitive Analysis

## Definition

**Competitive analysis** is a mathematical framework for evaluating the performance of an online or learning-augmented algorithm by comparing its cost to that of an optimal offline algorithm (which has complete future information) on the same instance.

The **competitive ratio** (or approximation factor) is formally defined as:

$$C = \sup_{\text{all instances}} \frac{\text{Cost}_{\text{algorithm}}}{\text{Cost}_{\text{optimal}}}$$

For an algorithm $\mathcal{A}$, a $c$-competitive ratio means the algorithm guarantees performance within a factor of $c$ of the optimal solution for any possible input sequence.

In the context of **learning-augmented algorithms**, competitive analysis is extended to measure average performance across multiple instances:

$$\text{Average Competitive Ratio} = \frac{1}{n}\sum_{i=1}^{n} \frac{\text{Cost}_{\text{algorithm}}(i)}{\text{Cost}_{\text{optimal}}(i)}$$

where the goal is to match the performance of the best fixed solution in hindsight.

## Key Equations

**Standard Competitive Ratio (worst-case):**
$$\rho_c(\mathcal{A}) = \inf\{c : \text{Cost}_{\mathcal{A}}(\sigma) \leq c \cdot \text{Cost}_{\text{OPT}}(\sigma) \text{ for all sequences } \sigma\}$$

**Average Case (learning-augmented):**
$$\bar{\rho}(\mathcal{A}) = \mathbb{E}\left[\frac{1}{n}\sum_{i=1}^{n} \frac{\text{Cost}_{\mathcal{A}}(I_i)}{\text{Cost}_{\text{OPT}}(I_i)}\right]$$

where $I_i$ represents problem instances in a sequence.

**Regret Bound (connection to online learning):**
$$\text{Regret} = \sum_{i=1}^{n} \text{Cost}_{\mathcal{A}}(I_i) - \min_{j \in \mathcal{S}} \sum_{i=1}^{n} \text{Cost}_j(I_i)$$

The regret measures cumulative loss relative to the best fixed action in hindsight.

## Physical Intuition / Derivation

### Why Competitive Analysis Matters

Traditional offline algorithms assume complete knowledge of future problem instances. Real-world systems (routing, caching, scheduling) must make decisions without this information. Competitive analysis quantifies the "cost of uncertainty."

### Two Perspectives

**1. Adversarial Worst-Case (Classical)**
- An adversary designs the worst possible input sequence
- The algorithm must guarantee a bounded ratio regardless
- Example: A 2-competitive online algorithm for ski rental guarantees cost ≤ 2× optimal

**2. Learning-Augmented Average-Case (Modern)**
- Past instances inform future decisions
- Performance measured over a distribution of instances
- Algorithm "learns" patterns to approach oracle performance

### Derivation for $k$-median Example

For the $k$-median clustering problem:
- **Offline optimum**: Compute optimal $k$ cluster centers knowing all data points
- **Online/Learning-augmented**: Propose clusters based on prior instances
- **Competitive ratio**: $\frac{\text{Cost}_{\text{proposed}}(\text{new instance})}{\text{Cost}_{\text{optimal}}(\text{new instance})}$

If an algorithm achieves average competitive ratio of 1.5 across instances, it means on average, solutions cost 50% more than optimal—a meaningful improvement over worst-case ratios (which might be 10×).

## Applications in Engineering

### 1. **Caching and Memory Management**
- **Problem**: Decide which pages to keep in fast cache without knowing future accesses
- **Competitive analysis**: LRU (Least Recently Used) achieves $\Theta(n)$ competitive ratio; can be improved with ML predictions
- **Improvement**: Learning algorithms that predict access patterns achieve near-optimal average performance

### 2. **Online Routing and Logistics**
- **Problem**: Route vehicles given a sequence of arriving delivery requests
- **Competitive analysis**: Greedy nearest-neighbor algorithms have poor worst-case guarantees
- **Improvement**: ML-augmented routing learns demand patterns to adjust fleet positioning

### 3. **Cloud Resource Allocation**
- **Problem**: Allocate compute resources to jobs arriving over time
- **Competitive analysis**: Measure makespan (total completion time) against optimal offline allocation
- **Improvement**: Predictive scheduling uses historical workload patterns to pre-allocate resources

### 4. **Facility Location ($k$-median, $k$-means)**
- **Problem**: Place $k$ facilities (servers, warehouses) serving sequentially arriving clients
- **Competitive analysis**: Competitive ratio depends on number of facilities and cost structure
- **Improvement**: Learning from past client distributions reduces average cost while maintaining worst-case guarantees

### 5. **Financial Trading and Portfolio Management**
- **Problem**: Rebalance portfolio given uncertain future prices
- **Competitive analysis**: Compare to best fixed portfolio allocation in hindsight
- **Improvement**: ML predictions improve decision-making while bounding loss vs. oracle

## Common Mistakes / Pitfalls

### 1. **Confusing Competitive Ratio with Approximation Ratio**
- **Mistake**: Treating them as identical concepts
- **Reality**: 
  - **Approximation ratio** compares algorithm cost to optimal for a *single instance* (polynomial-time algorithm)
  - **Competitive ratio** compares online algorithm cost to offline optimal across *all possible sequences*
- **Key difference**: Competitive analysis must handle adversarial or uncertain inputs

### 2. **Assuming Competitive Ratio Applies to Average Case**
- **Mistake**: Claiming a worst-case competitive ratio of 2 means "algorithms perform within 2× on average"
- **Reality**: Worst-case ratio is for adversarial inputs; average performance can be much better
- **Fix**: Explicitly separate worst-case guarantees from average-case empirical results

### 3. **Ignoring the Importance of Algorithm Predictions**
- **Mistake**: In learning-augmented settings, treating predictions as perfect or worthless
- **Reality**: Competitive analysis should de