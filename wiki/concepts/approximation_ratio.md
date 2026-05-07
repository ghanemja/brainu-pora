# approximation ratio

## Definition

An **approximation ratio** (or **approximation factor**) is a measure of how close an approximate solution is to the optimal solution for a computational problem. For a minimization problem, the approximation ratio $\rho$ of an algorithm $A$ is defined as:

$$\rho = \frac{\text{Cost}(A)}{\text{Cost}(\text{OPT})}$$

where $\text{Cost}(A)$ is the objective value produced by algorithm $A$ and $\text{Cost}(\text{OPT})$ is the optimal objective value. For a maximization problem, the definition is reversed:

$$\rho = \frac{\text{Cost}(\text{OPT})}{\text{Cost}(A)}$$

An algorithm with approximation ratio $\rho$ is called a **$\rho$-approximation algorithm**. The ratio is always $\geq 1$, with $\rho = 1$ meaning the algorithm is optimal.

## Key Equations

**Minimization problem:**
$$\rho_{\min} = \max_{\text{all instances}} \frac{\text{Cost}(A)}{\text{OPT}}$$

**Maximization problem:**
$$\rho_{\max} = \max_{\text{all instances}} \frac{\text{OPT}}{\text{Cost}(A)}$$

**Relative error:**
$$\text{Error} = \rho - 1 = \frac{\text{Cost}(A) - \text{OPT}}{\text{OPT}}$$

A $(1 + \epsilon)$-approximation achieves a relative error of at most $\epsilon$.

## Physical Intuition / Derivation

### Why Approximation Ratios Matter

Many important problems in engineering (routing, clustering, scheduling) are NP-hard, meaning finding the truly optimal solution is computationally infeasible for large instances. Rather than accepting either slow exponential algorithms or heuristics with no quality guarantees, we seek *guaranteed approximate solutions*.

The approximation ratio provides a **worst-case guarantee**: it bounds how far from optimal the algorithm's solution can be *on any input*.

### Example: Correlation Clustering

Consider the correlation clustering problem (from the source material). The task is to partition graph vertices to minimize disagreements:
- Cut edges connecting vertices in the same cluster (false positives)
- Non-edges between vertices in different clusters (false negatives)

The classic **pivot algorithm** (Ailon, Charikar, Newman) achieves a 3-approximation: for any input graph, it produces a clustering whose cost is at most 3 times the optimal cost. The source material shows this can be improved to 2.9991 by removing "good clusters" before each pivot step.

### Deriving Approximation Ratios

Proofs typically proceed by:

1. **Upper bound**: Show that algorithm $A$ always produces a solution with cost $\leq \rho \cdot \text{OPT}$
   - This requires analyzing the algorithm's worst-case behavior across all possible inputs
   
2. **Lower bound (tightness)**: Construct a specific instance where the algorithm achieves cost exactly $\rho \cdot \text{OPT}$
   - This shows the ratio cannot be improved without changing the algorithm
   - The source material notes that existing lower bounds for the pivot algorithm rely on "very good clusters, e.g., a complete graph minus a matching"

## Applications in Engineering

### Algorithm Design & Optimization
- **Vehicle routing**: Approximation algorithms for Traveling Salesman Problem (TSP) route vehicles within known factors of optimal distance
- **Network design**: Facility location and Steiner tree algorithms guarantee network costs within constant factors of optimum
- **Job scheduling**: Algorithms schedule tasks on machines while bounding makespan (total completion time) relative to optimal

### Machine Learning & Data Mining
- **Clustering**: Correlation clustering and k-means approximation ratios guide algorithm selection for data partitioning
- **Feature selection**: Greedy algorithms for submodular maximization achieve $(1 - 1/e)$-approximation, used in active learning and sensor placement

### Operations Research
- **Integer linear programming**: LP relaxation with rounding provides approximation guarantees when optimal integer solutions are hard to find
- **Bin packing**: Online algorithms for resource allocation guarantee waste within logarithmic factors of optimal

### Hardware/Resource Allocation
- **Cache replacement**: Approximation ratios characterize competitive performance of online caching algorithms
- **Power management**: Online algorithms for frequency scaling achieve polylogarithmic approximation ratios

## Common Mistakes / Pitfalls

### 1. **Confusing Approximation with Average-Case Performance**
   - An $\rho$-approximation is a *worst-case* guarantee
   - The algorithm may perform much better (closer to optimal) on typical instances
   - The source material shows empirically that the improved pivot algorithm performs "remarkably" well on synthetic datasets, beating the theoretical 2.9991 ratio

### 2. **Misinterpreting Ratio Direction**
   - Students often swap minimization and maximization definitions
   - For minimization: $\rho \geq 1$ (algorithm's cost $\geq$ optimal)
   - For maximization: $\rho \geq 1$ (algorithm's value $\leq$ optimal)

### 3. **Assuming Better Approximation Always Means Better Algorithm**
   - A 2.5-approximation is not always preferable to a 3-approximation if it:
     - Has higher time complexity ($O(n^3)$ vs. $O(n)$)
     - Has larger constant factors hidden in big-O notation
     - Performs worse on real-world instances
   - The source material's pivot algorithm remains influential despite the 3-approximation ratio because of its $O(n \log n)$ simplicity

### 4. **Overlooking Tightness**
   - A ratio is only meaningful if tight (lower bounds exist)
   - Proving an upper bound of 10 is less valuable if instances show the algorithm only ever exceeds optimal by 2×
   - The source material explicitly addresses this: moving from factor 3 to 2.9991 requires removing good clusters

### 5. **Neglecting Instance-Specific Factors**
   - Approximation ratios apply to *worst cases*
   -