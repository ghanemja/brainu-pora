# MPC Rounding Algorithm

## Definition

The **MPC rounding algorithm** is a distributed algorithm for converting fractional solutions (e.g., from linear programming relaxations) into integral solutions in the Massive Parallel Computation (MPC) model. Specifically, it transforms a fractional clustering solution $y \in \mathbb{R}^P_{\geq 0}$ into an integral center set $C \subseteq P$ with $|C| \leq k$ centers, while maintaining approximation guarantees in a distributed memory setting.

**Key Properties:**
- Works for **general metrics** (not just Euclidean)
- Operates in the **MPC model** where computation is distributed across multiple machines with limited local memory $s$
- Achieves polylogarithmic round complexity $O(\log_s n)$
- Maintains approximation guarantees through metric-aware rounding

## Key Equations

**Approximation Quality (Euclidean):**
$$\text{cost}(C) \leq 2^{O(z^2)} \cdot \text{OPT}^{\text{cl}}_k$$
where $z$ is a tunable parameter controlling the approximation factor.

**Memory-Communication Tradeoffs:**

*High-dimension regime:*
$$\text{Total Memory} = 2^{O(\varepsilon d)} \cdot O(n^{1+\varepsilon} \cdot \text{poly}(d \log(n\Delta)))$$
with rounds: $O(\log_s n)$

*Low-dimension regime ($d = o(\log n / \log \log n)$):*
$$\text{Total Memory} = 2^{O(d \log d)} \cdot O(n \cdot \text{polylog}(n\Delta))$$

**Aspect Ratio and Distance Scaling:**
All points $P \subseteq \mathbb{R}^d$ have aspect ratio $\Delta$, defined as:
$$\Delta = \frac{\max_{p,q \in P} \text{dist}(p,q)}{\min_{p,q \in P} \text{dist}(p,q)}$$

## Physical Intuition / Derivation

### Why Rounding is Necessary

Linear programming relaxations of clustering problems (e.g., $k$-clustering) produce fractional assignments where points are partially assigned to multiple centers. The rounding algorithm must "commit" each point to actual centers while preserving solution quality.

### Core Strategy: Metric Ruling Sets

The algorithm operates in phases using **metric $(τ, α_R \cdot τ)$-ruling sets**:
- A ruling set is a sparsified subset of the point set
- Two parameters: inner radius $τ$ (balls are disjoint) and outer radius $α_R \cdot τ$ (covers all points)
- Metric-aware selection ensures the sparsification respects the distance structure

**Intuition:** By working with ruling sets at different scales, the algorithm hierarchically processes points:
1. Start with a coarse ruling set at large scale
2. Progressively refine to finer scales
3. At each level, perform greedy center selection

### Three Key Oracle Operations

The algorithm abstracts its main computational tasks into three operations:

**(O1) Metric Ruling Set Computation**
- Input: radius parameter $τ$ and subset $Q \subseteq P$
- Output: $(τ, α_R \cdot τ)$-ruling set $R$
- **Why needed:** Enables hierarchical greedy selection of centers independent of fractional values

**(O2) Range Query (Approximate Aggregation)**
- Computes weighted sums in annuli:
$$s_p \in \left[\sum_{q: \text{dist}(p,q) \leq τ} v_q, \sum_{q: \text{dist}(p,q) \leq \Gamma \cdot τ} v_q\right]$$
- **Why needed:** Evaluates fractional solution quality in metric neighborhoods; the $(1, \Gamma)$ slack accommodates distributed implementation without exact global communication

**(O3) Approximate Nearest Neighbor Search**
- Returns $\widehat{NN}_\Gamma(p, Q)$ with distance:
$$\text{dist}(p, \widehat{NN}_\Gamma(p, Q)) \leq \Gamma \cdot \text{dist}(p, Q)$$
- **Why needed:** Assigns points to centers in the distributed setting; approximation factor $\Gamma$ is tolerated by the outer radius parameter

### Two Complexity Tradeoffs Explained

**Tradeoff 1 (Theorem 5.1):** High-dimensional regime
- Uses memory $2^{O(\varepsilon d)}$ to achieve $(1+\varepsilon)$-approximation in dimension $d$
- Requires $s \geq 2^{\Omega(d)}$ per machine (exponential in $d$)
- Scalable for small $d$ or when we can pay exponential memory

**Tradeoff 2 (Theorem 5.2):** Low-dimension regime
- Reduces memory to $2^{O(d \log d)}$ (better for small $d$)
- Worsens approximation to $2^{O(z^2)}$-factor (controlled by parameter $z$)
- Fully scalable when $d = o(\log n / \log \log n)$

## Applications in Engineering

### Distributed Machine Learning

**Clustering at Scale:**
- Implements $k$-means and $k$-clustering on MapReduce/Spark clusters
- Converts LP-relaxation solutions into practical center locations
- Example: clustering sensor data across thousands of IoT devices

### Data Center Optimization

**Server Placement:**
- Minimizes latency by selecting $k$ data center locations to serve $n$ client points
- MPC rounding respects network distance metrics (not Euclidean)
- Handles dynamic point distribution across servers

### Facility Location

**Supply Chain Networks:**
- Selects $k$ warehouse locations to serve customer demand
- Metric can be road distance, transportation cost, or time
- Distributed computation handles massive point sets (suppliers/customers)

### Geographical Information Systems (GIS