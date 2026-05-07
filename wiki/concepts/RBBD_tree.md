# RBBD Tree

## Definition

The **RBBD tree** (Relational Balanced Box Decomposition tree) is a randomized variant of the classical BBD tree data structure, specifically designed to operate efficiently on relational data without materializing expensive join operations.

**Formal Characterization:**
- An RBBD tree is a spatial decomposition structure that hierarchically partitions a geometric space derived from a relational join query
- Unlike traditional BBD trees that require full data materialization, RBBD trees enable **on-the-fly expansion** through lazy evaluation
- Only necessary tree nodes are constructed during algorithm execution, using efficient sampling and counting techniques over the underlying relational joins

**Key Distinction:** While a standard BBD tree assumes direct access to a point set in $\mathbb{R}^d$, an RBBD tree operates on data logically defined by a join query $Q$ over tables $T_1, T_2, \ldots, T_k$, where the join result set may be exponentially larger than input table sizes.

## Key Equations

**Join Output Size Bound:**
$$|Q(T_1, \ldots, T_k)| \leq \prod_{i=1}^{k} |T_i|$$

The join result can be polynomially (or even exponentially) larger than constituent tables, motivating the need to avoid full materialization.

**Relational k-center Problem:**
Given join result $P = Q(T_1, \ldots, T_k) \subseteq \mathbb{R}^d$, find $k$ centers $C = \{c_1, \ldots, c_k\}$ minimizing:
$$\text{cost}(C) = \max_{p \in P} \min_{c \in C} \|p - c\|_2$$

The RBBD tree approach achieves $(2+\epsilon)$-approximation in $O(n \log n - kn \log k)$ time instead of $O(nk)$ for naive approaches, where $n = |P|$.

**Tree Expansion via Sampling:**
The probability of reaching a leaf at depth $d$ in an RBBD tree is determined by adaptive sampling rates:
$$p_{\text{expand}}(\text{node}) = \min\left(1, \frac{c \cdot \log(1/\delta)}{|S_{\text{node}}|}\right)$$

where $S_{\text{node}}$ is the estimated count of points in that region, obtained via relational cardinality estimation.

## Physical Intuition / Derivation

### The Core Problem
Clustering and optimization algorithms often rely on geometric data structures to achieve sublinear or near-linear time complexity. BBD trees are powerful for this purpose in the standard setting. However, when data lives in a relational database, **you cannot afford to compute the full join** $|T_1 \bowtie T_2 \bowtie \cdots \bowtie T_k|$ upfront—it may have terabytes of output.

### Why Naive Materialization Fails
Consider a database with three normalized tables:
- `Users` (1 million rows)
- `Purchases` (100 million rows)
- `Products` (1 million rows)

A three-way join could theoretically produce $10^6 \times 10^8 \times 10^6$ rows. Computing a k-means clustering on this materialized join is infeasible.

### The RBBD Tree Solution
The key insight is **lazy evaluation with probabilistic expansion:**

1. **Partition Space Hierarchically**: Divide $\mathbb{R}^d$ into axis-aligned boxes recursively, following the BBD tree structure.

2. **Count, Don't Materialize**: For any box region $B$, estimate $|P \cap B|$ by executing a relational query with filtering predicates. Modern databases can answer such cardinality questions without full materialization.

3. **Adaptive Expansion**: Expand tree nodes selectively. Only decompose a box further if:
   - It contains enough points to warrant recursion (determined by probabilistic thresholds)
   - The algorithm actually queries that region

4. **On-the-Fly Sampling**: When the algorithm needs to sample points from a region $B$, use stratified sampling over the join to obtain representative samples without materializing all $|P \cap B|$ points.

**Derivation Intuition:**
$$\underbrace{\text{Standard BBD}}_{\text{full structure}} \rightarrow \underbrace{\text{RBBD}}_{\text{sample, count, expand}} = \text{sublinear access to relational joins}$$

This transforms a $\Omega(n)$ materialization cost into $O(\log n + \text{query overhead})$ per node expansion in expectation.

## Applications in Engineering

### 1. **Database-Native Machine Learning**
Direct application of clustering algorithms on relational data without ETL (extract-transform-load) pipelines:
- k-means clustering on SQL joins reduces runtime by factor of $k$ compared to post-materialization approaches
- Integration with databases like PostgreSQL, Spark SQL, Presto

### 2. **Data Warehouse Analytics**
Efficient clustering of fact tables normalized across multiple dimension tables:
- Customer segmentation from denormalized schemas
- Anomaly detection in event logs across related tables

### 3. **Spatial Indexing in Geo-Databases**
When location data is partitioned across multiple relational tables:
- k-center facility location problems
- Geospatial clustering without full materialization

### 4. **Approximate Query Processing**
Enables fast approximate answers to optimization queries:
- Interactive clustering dashboards that respond in seconds rather than minutes
- Streaming relational data processing where materialization is impossible

### 5. **Scientific Databases**
Biology, physics simulations where experimental data is normalized across experiment metadata and measurement tables:
- Clustering high-dimensional scientific point clouds
- k-median analysis of structured experimental results

## Common Mistakes / Pitfalls

### ❌ **Mistake 1: Confusing with Standard BBD Trees**
Students often assume RBBD trees require the same construction time as BBD trees. The key difference is:
- **BBD**: $O(n \log n)$ preprocessing on materialized point set
- **RBBD**: $O(\log n + \text{I/O})$