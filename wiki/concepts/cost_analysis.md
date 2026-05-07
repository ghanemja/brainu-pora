# Cost Analysis

## Definition

Cost analysis is the systematic decomposition and quantification of expenses associated with a system, process, or solution, with the goal of understanding the trade-offs between solution quality and computational/resource expenditure. In optimization contexts, cost analysis examines how alternative configurations, partitions, or allocations affect the total objective function value.

Formally, a **cost function** $C(\mathcal{P})$ assigns a numerical value to a candidate solution $\mathcal{P}$ (such as a partition or allocation), where lower costs indicate better feasibility or efficiency. Cost analysis involves:

1. **Identifying cost contributors**: Which variables, constraints, or structural choices drive the objective?
2. **Quantifying trade-offs**: How sensitive is total cost to changes in parameters or structure?
3. **Establishing bounds**: What are achievable lower and upper bounds on cost?
4. **Proving optimality**: Can we show that certain solutions are optimal or near-optimal?

## Key Equations

For a partition $\mathcal{X} = \{X_1, X_2, \ldots, X_m\}$, the aggregate cost is:

$$C(\mathcal{X}) = \sum_{i=1}^{m} c(X_i)$$

where $c(X_i)$ is the cost of part $i$, which may depend on:
- **Discrete parameters**: element counts, signatures (e.g., number of type-$x$, type-$x'$, type-$x''$ elements)
- **Continuous parameters**: real-valued weights, sums $\sum_{j \in X_i} \varepsilon_j$

**Rounding bounds**: If elements are rounded from fine values to coarse bins (size $\Delta$), the perturbation to cost is bounded:

$$|C(\mathcal{X}_{\text{exact}}) - C(\mathcal{X}_{\text{rounded}})| \leq \frac{1}{\text{poly}(k)}$$

**Sub-optimality gap**: For irregular (non-canonical) structures, a guaranteed cost penalty emerges:

$$C(\text{irregular}) \geq C(\text{optimal}) + \Omega\left(\frac{1}{k^2}\right)$$

This gap must dominate rounding errors to enable rigorous analysis.

## Physical Intuition / Derivation

### Why Cost Analysis Matters

Consider partitioning a set of objects with heterogeneous properties. A naive enumeration of all partitions is exponential, making exhaustive cost comparison infeasible. Cost analysis provides two complementary insights:

1. **Structural reduction**: By showing that only *regular* (canonical) partitions can be optimal, we reduce the search space dramatically. In the source material, partitions with signatures $(t, 2t, 0)$ or $(t, 0, 2t)$ are "special"—they have provable optimality properties.

2. **Univariate reduction**: Once we restrict to regular partitions, cost becomes a function of fewer variables. For instance, after merging parts in a regular partition down to exactly two parts, cost reduces to a univariate function of the sum of $\varepsilon_i$ values in one part. Elementary calculus then determines the optimum.

### Why Irregular Partitions Are Suboptimal

In the example context:

- **Many part types** with arbitrary signatures lead to a cost function depending on many discrete and continuous variables simultaneously—difficult to analyze globally.
- **Signature constraints** (e.g., $(t, 2t, 0)$) impose balance conditions that reduce degrees of freedom. Any deviation (irregular signature) incurs a penalty.
- **Case analysis** exhaustively shows that the $\Omega(1/k^2)$ sub-optimality gap for irregular partitions is large enough to survive the $1/\text{poly}(k)$ rounding error, ensuring the rounding approximation is valid.

### Step-by-Step Analysis Template

1. **Round** continuous parameters to discrete bins (introducing $O(1/\text{poly}(k))$ error).
2. **Show** that irregular partitions cost $\geq \text{OPT} + \Omega(1/k^2)$ via exhaustive case analysis.
3. **Merge** regular parts to force a canonical form (2-part partition with signatures $(k, 2k, 0)$ and $(k, 0, 2k)$).
4. **Reduce** to univariate optimization: cost as a function of $\sum \varepsilon_i$ in the first part.
5. **Solve**: Use calculus to find the minimum cost configuration and verify it matches the problem instance.

## Applications in Engineering

### 1. **Supply Chain & Logistics**
- **Partitioning shipments** into transport routes with different costs (fuel, labor, vehicle depreciation).
- Cost analysis determines whether consolidating shipments (fewer parts, larger batches) or splitting them (more parts, faster delivery) minimizes total expense.

### 2. **Manufacturing & Process Design**
- **Production scheduling**: Partition jobs into batches, where each batch incurs setup costs plus per-unit processing costs.
- Cost analysis reveals whether small frequent runs or large infrequent runs minimize $C = \sum (\text{setup} + \text{batch size} \times \text{unit cost})$.

### 3. **Data Structure & Algorithm Design**
- **Memory allocation**: Partition data into cache-resident chunks vs. off-chip storage.
- Cost = access latency + data movement overhead. Analysis determines optimal partition granularity.

### 4. **Network & Resource Allocation**
- **Data center clustering**: Partition servers into groups; cost includes inter-group communication overhead.
- Cost analysis quantifies the trade-off between load balancing (fine partitions) and communication efficiency (coarse partitions).

### 5. **Calibration & Statistical Learning**
- **Empirical convergence**: In the source material, $\widehat{D}$ (empirical distribution) converges to true $D$ at rate $O(|X|/\varepsilon^2)$ samples.
- Cost analysis shows that achieving calibration distance $\leq 1/(36k)$ with high probability requires $O(1/\varepsilon^3)$ samples—three orders rather than two, due to the additional univariate optimization dimension.

## Common Mistakes / Pitfalls

### 