# fully dynamic algorithm

## Definition

A **fully dynamic algorithm** is an algorithm that efficiently maintains a computational solution (data structure) subject to both **insertions and deletions** of elements, while supporting queries on the current state. Unlike semi-dynamic algorithms (which support only insertions) or static algorithms (which require complete recomputation for any change), fully dynamic algorithms must handle arbitrary element modifications with minimal recomputation.

### Characteristics:
- **Online operation**: updates and queries are interleaved in arbitrary order
- **Amortized complexity**: typically analyzed using amortized time per operation
- **Decomposability**: often requires clever decomposition strategies to avoid full recomputation
- **Data structure-dependent**: complexity depends on the problem structure and query types

---

## Key Equations

For a fully dynamic algorithm maintaining a dataset of size $n$:

$$T_{\text{update}} = O(f(n)) \quad \text{(amortized per insertion/deletion)}$$

$$T_{\text{query}} = O(g(n)) \quad \text{(per query)}$$

**Example from convex hull maintenance:**

$$T_{\text{update}} = O(\log n \log \log n) \quad \text{(amortized)}$$

$$T_{\text{query}} = O(\log^2 n)$$

The **amortized cost** distributes expensive rebuilding operations across multiple cheaper insertions:

$$\text{Amortized cost} = \frac{\text{Total cost of } k \text{ operations}}{k}$$

---

## Physical Intuition / Derivation

### The Core Challenge

Maintaining geometric properties (like convex hulls) dynamically presents a fundamental tension:

1. **Naive approach**: Rebuild the entire structure after each update
   - Simple and reliable
   - Cost: $O(n \log n)$ per update
   - Infeasible for update-heavy workloads

2. **Logarithmic decomposition method**: Break the problem into smaller pieces
   - Maintain multiple data structures of exponentially increasing sizes
   - Only rebuild structures that are "full" (reach capacity)
   - Insertions update small structures (cheap); deletions are harder (see deletion-only structures below)

### Logarithmic Method Intuition

Think of inserting elements into **buckets of exponential sizes** (like digits in logarithmic base):

- Bucket 0: $2^0 = 1$ element
- Bucket 1: $2^1 = 2$ elements  
- Bucket 2: $2^2 = 4$ elements
- Bucket $i$: $2^i$ elements

When a bucket overflows (reaches capacity), combine it with the next bucket. This is analogous to **carrying** in addition. The total work spreads across $O(\log n)$ buckets, and rebuilding an overflowing bucket costs only its size, amortizing to $O(\log n)$ per insertion.

### Handling Deletions

**Deletions are fundamentally harder** than insertions in geometric problems:
- Inserting a point is **monotonic**: the convex hull can only expand or stay the same
- Deleting a point requires **recomputation**: the hull might shrink and change arbitrarily

**Solution**: Use a **deletion-only convex hull data structure** combined with lazy deletion:
- Mark elements as deleted without physically removing them
- Periodically rebuild affected structures when deletions accumulate
- Maintain deletion counts alongside data structures

---

## Applications in Engineering

### 1. **Spatial Data Analysis and GIS**
- Tracking boundaries of moving object clusters (vehicles, wildlife populations)
- Real-time environmental monitoring with changing sensor networks
- Urban planning with evolving building footprints

### 2. **Computational Geometry and CAD**
- Collision detection in robotics with dynamic obstacles
- Shape approximation in computational design
- Visibility polygon maintenance

### 3. **Computational Finance**
- Maintaining Pareto frontiers in portfolio optimization as assets are added/removed
- Risk boundary computation for evolving asset portfolios
- Support vector machine training with online data streams

### 4. **Machine Learning and Data Mining**
- Outlier detection in streaming data (convex hull separates inliers from outliers)
- Support vector machines with incremental learning
- One-class classification with evolving training sets

### 5. **Robotics and Path Planning**
- Maintaining obstacles as dynamic objects enter/exit the workspace
- Computing free space boundaries for navigation

### 6. **Graphics and Visualization**
- Point-location queries for convex hull containment testing
- Mesh generation with evolving vertex sets

---

## Common Mistakes / Pitfalls

### 1. **Confusing Amortized and Worst-Case Costs**
**Mistake**: Assuming amortized $O(\log n \log \log n)$ means every operation takes that time.

**Reality**: Some operations may be expensive (full rebuilds), others cheap (simple updates). The average over many operations equals the amortized bound.

**Fix**: Understand that amortized analysis hides variance—worst-case per-operation complexity may be higher.

### 2. **Ignoring Deletion Complexity**
**Mistake**: Treating deletions like "backwards insertions."

**Reality**: Deletions don't have the monotonicity property. A deletion-only structure *cannot* support insertions efficiently.

**Fix**: Use separate strategies for insertions (logarithmic decomposition) and deletions (specialized data structures or lazy deletion).

### 3. **Overlooking Point-Location Query Decomposability**
**Mistake**: Assuming that if a problem is solvable dynamically, queries like "is point $p$ inside the convex hull?" are easy.

**Reality**: Point-location queries on decomposed structures are **non-decomposable**—you cannot answer queries on individual pieces and combine results easily.

**Fix**: Implement queries that search across all active data structures and combine results carefully.

### 4. **Numerical Robustness Issues**
**Mistake**: Using exact arithmetic assumptions in floating-point implementations.

**Reality**: Geometric predicates (orientation tests) accumulate rounding errors. Rebuilding operations at boundaries are particularly sensitive.

**Fix**: Use adaptive precision arithmetic or exact predicate libraries; validate implementations against synthetic and real-world datasets.

### 5. **Not Profiling Workload Characteristics**
**Mistake**: Choosing a fully dynamic algorithm without considering the update-to-