# k-means clustering

## Definition

**k-means clustering** is an unsupervised learning algorithm that partitions a set of $n$ data points in a metric space into $k$ disjoint clusters by iteratively minimizing the sum of squared distances (in Euclidean spaces) between points and their assigned cluster centroids.

Formally, given a dataset $P = \{p_1, p_2, \ldots, p_n\} \subseteq \mathbb{R}^d$, k-means seeks to find $k$ cluster centers (centroids) $C = \{c_1, c_2, \ldots, c_k\}$ and an assignment function $\sigma: P \to [k]$ that minimize the **k-means objective**:

$$\text{KM}(C, \sigma) = \sum_{i=1}^{n} \|p_i - c_{\sigma(i)}\|^2$$

where $\sigma(i)$ denotes the cluster index assigned to point $p_i$.

## Key Equations

### Objective Function
The k-means cost for a fixed set of centroids is:
$$\text{Cost}_k(P) = \min_{\sigma} \sum_{p \in P} \min_{j \in [k]} \|p - c_j\|^2$$

### Centroid Update (Closed-form solution)
For a fixed partition $\sigma$, the optimal centroid for cluster $C_j$ is the **geometric mean** of all assigned points:
$$c_j^* = \frac{1}{|C_j|} \sum_{p \in C_j} p$$

### Inertia (Within-cluster sum of squares)
$$\text{Inertia} = \sum_{j=1}^{k} \sum_{p \in C_j} \|p - c_j\|^2$$

Lower inertia indicates tighter, more cohesive clusters.

## Physical Intuition / Derivation

### Iterative Refinement Process

k-means employs a **coordinate descent** strategy, alternating between two steps:

1. **Assignment Step**: Assign each point to its nearest centroid
   $$\sigma(p) = \arg\min_{j \in [k]} \|p - c_j\|^2$$

2. **Update Step**: Recompute centroids as the mean of assigned points
   $$c_j \leftarrow \frac{1}{|C_j|} \sum_{p: \sigma(p)=j} p$$

### Convergence Intuition

Each iteration monotonically decreases (or leaves unchanged) the objective function:
- The assignment step reassigns points to minimize distance, reducing cost
- The update step replaces each centroid with the mean of its cluster, which provably minimizes the within-cluster variance for that cluster (by calculus: setting $\frac{\partial}{\partial c_j} \sum_p \|p - c_j\|^2 = 0$)

Since the objective is bounded below by zero and decreases with each iteration, the algorithm converges to a **local minimum** (not necessarily global). Convergence typically occurs within tens of iterations in practice, though the number of iterations can be exponential in the worst case.

### Why the Centroid is the Mean

For a fixed cluster $C_j$, the centroid minimizing $\sum_{p \in C_j} \|p - c\|^2$ is found by:
$$\frac{\partial}{\partial c} \sum_{p \in C_j} \|p - c\|^2 = -2\sum_{p \in C_j} (p - c) = 0$$
$$\Rightarrow c = \frac{1}{|C_j|} \sum_{p \in C_j} p$$

This is the arithmetic mean, which minimizes the sum of squared Euclidean distances.

## Applications in Engineering

### Machine Learning & Data Mining
- **Customer segmentation**: Partitioning user bases by behavior for targeted marketing
- **Image compression**: Quantizing colors by clustering pixel values; k-means on RGB space reduces color palettes
- **Document clustering**: Grouping similar documents for information retrieval

### Signal Processing & Sensor Networks
- **Vector quantization**: Codebook design for speech/audio compression (e.g., VQ-based speech coding)
- **Sensor data aggregation**: Clustering sensor readings to identify representative measurements in large distributed networks
- **Anomaly detection**: Normal behavior clusters vs. outliers

### Mechanical & Manufacturing Engineering
- **Quality control**: Clustering defect patterns to classify failure modes
- **Predictive maintenance**: Grouping similar machine states to predict failures
- **Process optimization**: Identifying distinct operating regimes in multi-mode processes

### Robotics & Computer Vision
- **Feature clustering**: Grouping visual features (SIFT, ORB) for scene understanding
- **Robot path planning**: Clustering waypoints to identify corridors or critical regions
- **Motion segmentation**: Separating different motion patterns in video sequences

### Power Systems & Energy
- **Load profiling**: Clustering consumption patterns across buildings/microgrids
- **Demand response**: Grouping similar consumers for coordinated control

## Common Mistakes / Pitfalls

### 1. **Assuming Global Optimality**
k-means converges to *local* minima. The solution depends heavily on initialization. Running k-means multiple times with different random seeds and selecting the best result (lowest objective) is standard practice.

### 2. **Arbitrary Choice of k**
The algorithm requires specifying $k$ *a priori*. Common heuristics:
- **Elbow method**: Plot inertia vs. $k$; look for "elbow" (diminishing returns)
- **Silhouette score**: Measures cluster cohesion and separation
- **Domain knowledge**: Use prior understanding of natural groupings

*Mistake*: Assuming a single "correct" $k$ exists; in reality, the optimal $k$ is problem-dependent and interpretation-dependent.

### 3. **Sensitivity to Feature Scaling**
k-means uses Euclidean distance, so features with larger ranges dominate the metric. Always **normalize or standardize** features (zero mean, unit variance) before clustering.

### 4. **Categorical or Non-Euclidean Data**
k