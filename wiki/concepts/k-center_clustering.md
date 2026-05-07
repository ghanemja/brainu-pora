# k-center clustering

## Definition

**k-center clustering** is a clustering problem where the goal is to partition a point set $P$ into $k$ clusters by selecting $k$ center points such that the maximum distance from any point to its nearest center is minimized.

Formally, given a point set $P$ and an integer $k$, find a set of $k$ centers $C = \{c_1, c_2, \ldots, c_k\}$ that minimizes the **clustering radius**:

$$r(C) = \max_{p \in P} \min_{c \in C} d(p, c)$$

where $d(p, c)$ denotes the distance between point $p$ and center $c$.

The **approximation ratio** $\alpha$ of a solution $C$ relative to the optimal solution $C^*$ is:

$$\alpha = \frac{r(C)}{r(C^*)}$$

### Dynamic Setting Extensions

In **dynamic k-center clustering**, the point set $P$ undergoes adversarial updates:

- **Fully dynamic**: Both insertions and deletions of points
- **Incremental**: Only insertions
- **Decremental**: Only deletions

Two adversarial models are distinguished:
- **Oblivious adversary**: The entire update sequence is fixed before the algorithm executes; cannot adapt based on algorithm outputs
- **Adaptive adversary**: Can observe algorithm outputs and internal randomized decisions; represents the strongest guarantees

## Key Equations

**Clustering radius (minimax objective):**
$$r(C) = \max_{p \in P} \min_{c \in C} d(p, c)$$

**Approximation ratio:**
$$\alpha = \frac{\text{radius of algorithm's solution}}{\text{radius of optimal solution}}$$

**Recourse (consistency metric):**
$$\text{Recourse} = |C_{\text{old}} \triangle C_{\text{new}}|$$

where $\triangle$ denotes symmetric difference; measures the number of center changes after a single update.

**Update time complexity:** $T_{\text{update}}$ — time required to process one adversarial point insertion or deletion.

## Physical Intuition / Derivation

The k-center problem arises naturally in scenarios where you need to cover a spatial region with a limited number of facilities:

**Covering interpretation**: Imagine placing $k$ emergency response stations (fire departments, hospitals) to minimize the worst-case response distance to any location in a city. The clustering radius $r(C)$ is the maximum distance any civilian must travel to reach the nearest station.

**Why the minimax objective?** Unlike k-means (which minimizes average squared distance), k-center optimizes the **worst case**. This is critical when:
- Coverage guarantees matter (e.g., all customers must be served within SLA)
- Fairness is important (no point should be neglected)
- One outlier's poor service is catastrophic

**Approximation hardness**: The greedy algorithm that repeatedly adds the point furthest from existing centers achieves a **2-approximation** — provably optimal, since achieving better than 2 is NP-hard under standard assumptions.

**Recourse and consistency**: In dynamic settings, recomputing centers from scratch after each update is computationally expensive and causes instability (e.g., delivery routes constantly change). The **recourse** metric quantifies algorithmic stability: fewer changes to $C$ means less disruption to downstream systems while maintaining quality approximations.

## Applications in Engineering

### Facility Location & Logistics
- **Server placement**: Position data centers to minimize maximum latency to any user
- **Distribution networks**: Place warehouses to cover geographic regions with bounded delivery times
- **Emergency services**: Station ambulances/fire trucks to ensure response time SLAs

### Machine Learning & Data Analysis
- **Outlier-robust clustering**: Unlike k-means, insensitive to extreme outliers
- **Diverse model selection**: Choose $k$ representative samples maximizing coverage of data space
- **Coreset construction**: Compress large datasets while preserving worst-case distances

### Real-time Systems
- **Sensor network design**: Place sensors to monitor maximum coverage with bounded gaps
- **Mobile robotics**: Plan waypoints ensuring no area of interest is too far from patrol routes
- **Network design**: Place replicas in distributed systems with bounded access time

### Consistent Clustering Applications
- **Online recommendation systems**: Cluster users while minimizing disruption to model serving
- **Dynamic resource allocation**: Adjust resource centers (e.g., cloud instances) without constant reassignment
- **Streaming data**: Maintain centers for evolving datasets with guaranteed stability between updates

## Common Mistakes / Pitfalls

### 1. **Confusing k-center with k-means**
Students often conflate the two because both use $k$ clusters. Key difference:
- **k-center**: Minimizes maximum distance (minimax); sensitive to problem structure; 2-approximable
- **k-means**: Minimizes sum of squared distances (average); more sensitive to outliers; NP-hard to approximate well

### 2. **Ignoring the approximation factor**
Claiming an algorithm "solves" k-center when it only achieves $\alpha$-approximation. In dynamic settings, approximation ratios compound—a $\alpha$-approximation maintained dynamically may grow with the number of updates.

### 3. **Neglecting recourse in dynamic algorithms**
A dynamic algorithm with good update time but $\Theta(k)$ recourse per update is impractical. True consistency requires both:
- Small approximation ratio
- Small recourse (ideally $O(1)$ or $O(\log k)$ per update)

### 4. **Assuming oblivious adversary suffices**
Many textbooks study only oblivious adversaries. However:
- Adaptive adversaries are strictly stronger and reveal true worst-case behavior
- Real deployments face adaptive adversaries (adversarial ML, network attacks)
- Algorithms robust to adaptive adversaries are more trustworthy black-boxes

### 5. **Overlooking metric space assumptions**
k-center algorithms assume the distance function $d$ satisfies the metric axioms (symmetry, triangle inequality, identity of indiscernibles). Violations invalidate approximation guarantees.

## See Also

- [[k-means clustering]] — Alternative clustering objective minimizing average distance; see [Concept: k-means clustering]
- [[Approximation algorithms]] — General framework for measuring solution