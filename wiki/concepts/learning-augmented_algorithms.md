# Learning-Augmented Algorithms

## Definition

**Learning-augmented algorithms** are algorithmic approaches that leverage machine learning on historical problem instances to improve decision-making on future instances. Unlike purely algorithmic solutions (which are instance-agnostic) or purely ML solutions (which may lack worst-case guarantees), learning-augmented algorithms combine both paradigms:

- **Input**: A sequence of problem instances $\{I_1, I_2, \ldots, I_T\}$ with access to solutions/data from earlier instances
- **Output**: Algorithmic decisions for instance $I_t$ informed by learning from $\{I_1, \ldots, I_{t-1}\}$
- **Goal**: Achieve near-optimal average performance across all instances while maintaining algorithmic efficiency

The framework bridges online learning and combinatorial optimization: rather than designing a single algorithm that works well on all possible instances, we design an algorithm that *adapts* to the specific distribution of instances encountered.

### Core Principle

The central insight is that real-world problem sequences are rarely worst-case adversarial. Historical data reveals underlying structure (e.g., clustering patterns, parameter distributions) that can be exploited while maintaining approximation guarantees if the predictions are wrong.

## Key Equations

### Performance Metric: Competitive Ratio with Learning

For a sequence of $T$ instances, the **average competitive ratio** is:

$$\text{ACR} = \frac{1}{T} \sum_{t=1}^{T} \frac{\text{ALG}(I_t)}{\text{OPT}(I_t)}$$

where:
- $\text{ALG}(I_t)$ = cost of the learning-augmented algorithm on instance $I_t$
- $\text{OPT}(I_t)$ = optimal cost on instance $I_t$

### Regret Bound (Online Learning Perspective)

The algorithm seeks to minimize **regret** relative to the best fixed solution in hindsight:

$$\text{Regret}_T = \sum_{t=1}^{T} \text{ALG}(I_t) - \min_{s \in \mathcal{S}} \sum_{t=1}^{T} \text{COST}(s, I_t)$$

where $\mathcal{S}$ is the solution space and $\text{COST}(s, I_t)$ is the cost of solution $s$ on instance $I_t$.

### k-Median Specific Formulation

For the k-median problem, the algorithm predicts a clustering center set $C^*$ from historical data, then uses:

$$\text{Cost}_t(C) = \sum_{x \in I_t} \min_{c \in C} d(x, c)$$

The learning-augmented approach achieves:

$$\mathbb{E}\left[\frac{1}{T}\sum_{t=1}^{T} \frac{\text{Cost}_t(\hat{C}_t)}{\text{Cost}_t(\text{OPT}_t)}\right] \approx \min_{C^* \text{ fixed}} \frac{1}{T}\sum_{t=1}^{T} \frac{\text{Cost}_t(C^*)}{\text{Cost}_t(\text{OPT}_t)}$$

## Physical Intuition / Derivation

### Why Learning Helps

Consider a clustering task where instances come from a slowly-drifting distribution:

1. **Without learning**: Apply k-median algorithm from scratch to each instance → always achieves worst-case approximation factor (e.g., $O(\log k)$ or constant factor depending on algorithm)
2. **With learning**: 
   - First few instances: algorithm performs with standard approximation ratio
   - After seeing patterns (e.g., clusters are centered near specific regions), algorithm can bias its search toward likely cluster centers
   - If distribution is stable, algorithm rapidly approaches near-optimal clusters
   - If distribution drifts, regret accumulates but algorithm adapts

### The Online Learning Connection

The framework mirrors **Follow-the-Leader (FTL)** or **Exponential Weights** methods:

- **Decision space**: Set of possible solutions (e.g., center configurations for k-median)
- **Loss function**: Cost of applying solution to current instance (learned from history)
- **Update rule**: Adjust solution selection based on cumulative historical performance

Instead of learning arbitrary weights, we learn instance-specific *hints* about good solutions, then apply proven combinatorial algorithms informed by those hints.

### Key Trade-off

$$\underbrace{\text{Better average case}}_{\text{exploits instance structure}} \text{ vs. } \underbrace{\text{Robustness to misprediction}}_{\text{maintains approximation guarantee}}$$

A well-designed learning-augmented algorithm should:
- Exploit learned structure when predictions are accurate
- Gracefully degrade when predictions fail (no worse than standard algorithm)

## Applications in Engineering

### 1. **Facility Location & Network Design**
- **Datacenter placement**: Historical user request patterns inform server placement for new deployments, reducing latency while maintaining backup-location guarantees
- **Supply chain optimization**: Warehouse locations learned from seasonal demand patterns; algorithm adapts to new demand distributions

### 2. **Clustering & Data Analysis**
- **Time-series clustering**: Given streaming sensor data, learn typical cluster patterns; algorithm adapts clusters for new sensor deployments with similar environments
- **Customer segmentation**: E-commerce platforms learn customer behavior patterns; new promotional campaigns adapt targeting based on learned segments

### 3. **Load Balancing & Scheduling**
- **Cloud resource allocation**: Historical workload patterns inform initial resource allocation; algorithm adjusts as new job types arrive
- **Traffic routing**: Network routers learn typical traffic patterns; routing decisions adapt to congestion patterns without full network recomputation

### 4. **Vehicle Routing & Logistics**
- **Last-mile delivery**: Learn delivery location clusters from past routes; optimize new routes informed by historical clusters while maintaining distance guarantees
- **Dynamic taxi dispatch**: Learn popular pickup/dropoff pairs; dispatch algorithms adapt to new demand patterns

### 5. **Edge Computing & IoT**
- **Mobile edge caching**: Learn popular content distribution; cache placement adapts to new content popularity patterns with guaranteed service levels

## Common Mistakes / Pitfalls

### 1. **Assuming Learned Predictions Are Always Correct**
**