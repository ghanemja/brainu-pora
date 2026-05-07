# Streaming Algorithm

## Definition

A **streaming algorithm** is an algorithm that processes a large data stream sequentially, one element at a time, using **severely limited memory**—typically $O(\text{poly}(k, \log n))$ space for a stream of $n$ elements. The algorithm must make irreversible decisions with each arriving data point, as revisiting past elements is prohibited.

Key constraints that define streaming algorithms:
- **Single-pass or limited-pass access**: Data arrives sequentially and cannot be stored in full
- **Sublinear space**: Memory usage $\ll n$ (the data size)
- **Fast updates**: Processing time per element must be small, typically $\text{poly}(k, \log n)$ amortized
- **Graceful degradation**: Solutions provide approximations with quantifiable error guarantees

Streaming algorithms are essential when the data volume exceeds available memory (e.g., network traffic, sensor data, social media feeds).

## Key Equations

### Low-Rank Approximation in Streaming

For an $n \times d$ matrix $A$ arriving row-by-row, let $A(t)$ denote the first $t$ rows. The low-rank approximation cost is:

$$\text{cost}_k(A(t)) = \min_{\text{rank-}k\text{ matrix } B} \|A(t) - B\|_F^2$$

where $\|\cdot\|_F$ denotes the Frobenius norm.

### Additive vs. Multiplicative Guarantees

**Additive $\varepsilon$-approximation:**
$$\text{cost}_k(\hat{A}(t)) \leq \text{cost}_k(A(t)) + \varepsilon \|A(t)\|_F^2$$

**Multiplicative $(1+\varepsilon)$-approximation:**
$$\text{cost}_k(\hat{A}(t)) \leq (1+\varepsilon) \cdot \text{cost}_k(A(t))$$

The latter is significantly stronger and harder to achieve.

### Recourse (Update Cost)

The number of times the optimal rank-$k$ subspace $V$ must be recomputed:

$$\text{Recourse} = |\{t : V(t) \neq V(t-1)\}|$$

**Theorem 1.1 result:**
$$\text{Recourse} = O\left(\frac{k}{\varepsilon} \log(ndM)\right)$$

for additive $\varepsilon \|A(t)\|_F^2$ error approximation.

**Theorem 1.2 result (restricted setting):**
$$\text{Recourse} = O\left(\frac{k}{\varepsilon^2} \log^3 n\right)$$

when online condition number $\leq \text{poly}(n)$.

## Physical Intuition / Derivation

### Why Streaming Matters

Imagine monitoring network traffic on a backbone router: petabytes of data flow daily, but you can't store it all. You must extract features (rank-$k$ approximation of traffic patterns) with minimal memory—perhaps only enough to store a few thousand vectors.

### The Core Tension

**Challenge:** The optimal rank-$k$ subspace can change drastically with each new row, potentially requiring $\Omega(nk)$ recourse (full recomputation $n$ times). 

**Resolution:** The source material reveals a key insight: **sublinear recourse is achievable if we accept additive error.** This is the crux of Theorem 1.1.

### Why Additive Error is Easier

The additive error bound $\varepsilon \|A(t)\|_F^2$ is weaker than multiplicative $(1+\varepsilon)$ error. Intuitively:
- Additive: error scaled by *total energy* in the data (can be large)
- Multiplicative: error scaled by *optimal cost* (much smaller for good low-rank structure)

Consider a rank-10 matrix corrupted by Frobenius norm 100. Achieving additive error 10 is much easier than $(1+0.1)$ multiplicative error (must be within error $\text{cost}_{10}(A) + 10$, where $\text{cost}_{10}$ might be $\ll 1$).

### Online Condition Number

When the **online condition number** $\kappa_{\text{online}} \leq \text{poly}(n)$, the spectrum remains stable as rows arrive. Rank-one perturbations cause only constant changes to the optimal subspace (Lemma 2.3). This allows:
- Better recourse bounds: $O(k/\varepsilon^2 \log^3 n)$
- Stronger guarantees: $(1+\varepsilon)$ multiplicative approximation
- Handling insertions and deletions with $O(n)$ total recourse

## Applications in Engineering

### 1. **Network Monitoring and Anomaly Detection**
Streaming PCA on router traffic matrices to detect DDoS attacks or anomalies. Algorithms maintain rank-$k$ traffic profiles with minimal router memory, updating only when traffic patterns shift significantly.

### 2. **Sensor Networks and IoT**
Environmental monitoring (temperature, humidity across thousands of sensors) streams high-dimensional data. Streaming low-rank approximation identifies dominant spatial/temporal patterns without backhaul to centralized data centers.

### 3. **Financial Data Analysis**
Stock market feeds contain millions of price ticks per second. Streaming algorithms extract principal market factors in real-time, with bounded memory on trading terminals.

### 4. **Video Streaming and Compression**
Frame sequences form long matrices. Streaming SVD compresses video by maintaining a rank-$k$ basis that adapts as scene content changes (motion, lighting). The additive error bound ensures quality remains above $\varepsilon \|F_{\text{current}}\|_F^2$.

### 5. **Query Processing in Databases**
Approximating the spectrum of unfinished table scans to optimize join ordering. Sublinear memory prevents database crashes; recourse bounds measure index rebuild costs.

### 6. **Machine Learning: Online Feature Learning**
Streaming data imposes constraints on feature extraction—cannot re-see training data. Streaming