# Contiguous Partitions

## Definition

A **contiguous partition** is a partition of an ordered domain $X = \{x_1, x_2, \ldots, x_n\}$ where each part (subset) consists of consecutive elements. Formally, a partition $P = \{X_1, X_2, \ldots, X_k\}$ is contiguous if for each $X_i$, there exist indices $a_i \leq b_i$ such that:

$$X_i = \{x_j : a_i \leq j \leq b_i\}$$

and the index intervals $[a_1, b_1], [a_2, b_2], \ldots, [a_k, b_k]$ partition $[1, n]$ without overlap.

In other words, when the domain elements are ordered along a line or axis, each part of a contiguous partition forms a single unbroken interval.

## Key Equations

For a contiguous partition $P = \{X_1, X_2, \ldots, X_k\}$ of domain $X$, the **cost** (measure of distance from calibration) is defined as:

$$\text{costD,f}(P) := \sum_{i=1}^{k} \sum_{x \in X_i} \mathcal{D}_x(x) \cdot \left| f(x) - \mu_\mathcal{D}(X_i) \right|$$

where:
- $\mathcal{D}_x(x)$ is the marginal probability mass at point $x$
- $f(x)$ is the predictor value at $x$
- $\mu_\mathcal{D}(X_i) = \frac{1}{\mathcal{D}(X_i)} \sum_{x \in X_i} \mathcal{D}_x(x) \cdot \mathbb{1}_{y(x)=1}$ is the empirical mean (label proportion) in partition $X_i$

The **calibration distance** is then:

$$\text{CalDist}_\mathcal{D}(f) := \min_P \text{costD,f}(P)$$

where the minimum is taken over all partitions (or all contiguous partitions when restricted).

## Physical Intuition / Derivation

### Why Contiguity Matters

When partitioning a naturally ordered domain (e.g., confidence scores, time, spatial position, or a ranking), forcing partitions to be contiguous provides a crucial computational advantage without loss of generality in many contexts:

1. **Reduced Search Space**: Rather than considering all $\mathcal{O}(2^n)$ possible partitions, contiguous partitions can be enumerated in polynomial time via dynamic programming. The number of contiguous partitions of $n$ elements into $k$ parts is only $\binom{n-1}{k-1}$.

2. **Physical/Semantic Consistency**: In calibration problems, if the underlying predictor is monotonic (or can be made monotonic through proper preprocessing), partitions should respect this structure. Contiguity aligns with monotonicity: if $f(x_i) \leq f(x_{i+1})$ for ordered $x_i, x_{i+1}$, then contiguous partitions preserve this relationship naturally.

3. **Sparsification Justification**: The source material notes that after sparsification (removing redundant elements that can be grouped together), restricting to contiguous partitions becomes **without loss of generality**. This means the optimal unrestricted partition can be transformed into a contiguous one with identical cost.

### Derivation Path

The problem arises from the observation (Fact 1) that every perfectly calibrated predictor corresponds to a partition: partition the domain $X$ into regions where within each region, the predictor's output equals the true label proportion. The challenge is finding the partition that minimizes distance from calibration:

$$\text{CalDist}_\mathcal{D}(f) = \min_{\text{all partitions}} \sum_i \text{costD,f}(X_i)$$

Constraining to contiguous partitions enables polynomial-time algorithms via the Bellman recurrence:

$$\text{OPT}(i, k) = \min_{j < i} \left[ \text{OPT}(j, k-1) + \text{costD,f}(X_{j+1}^i) \right]$$

where $\text{OPT}(i, k)$ is the minimum cost to partition the first $i$ elements into $k$ contiguous parts.

## Applications in Engineering

### 1. **Calibration in Machine Learning / Predictive Systems**
- Partitioning confidence scores or predicted probabilities into confidence bins where calibration can be verified
- Ensuring that a predictor assigning probability $p$ to an event is correct approximately $p\%$ of the time
- Example: medical risk scores must be contiguously binned (e.g., [0–0.1), [0.1–0.3), [0.3–1.0]) for regulatory compliance

### 2. **Quality Control & Process Monitoring**
- Partitioning ordered measurements (sensor readings, timestamps) into contiguous batches
- Each batch assigned a quality/rejection threshold based on empirical failure rates in that batch
- Minimizes recalibration cost when thresholds must change

### 3. **Dynamic Pricing & Revenue Management**
- Segmenting customers or time periods into contiguous tiers based on ordered features (willingness-to-pay)
- Each tier assigned a price equal to the historical conversion rate × value
- Contiguity ensures no "price jumps" between adjacent segments

### 4. **Autonomous Systems & Robotics**
- Partitioning continuous sensor input ranges (e.g., obstacle distance, velocity) into operational modes
- Contiguous partitions ensure smooth transitions between modes as conditions change
- Reduces mode-switching artifacts

### 5. **Network Traffic Engineering**
- Binning traffic flows by ordered QoS parameters (latency, packet loss) into resource allocation tiers
- Contiguity ensures fair handoff between tiers

## Common Mistakes / Pitfalls

1. **Assuming Contiguity is Always Optimal**