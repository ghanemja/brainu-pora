# Greedy Approximation Algorithm

## Definition

A **greedy approximation algorithm** is a polynomial-time algorithm that iteratively makes locally optimal choices to construct a solution to an optimization problem, with a provably bounded worst-case ratio between the greedy solution and the optimal solution.

Formally, for a maximization problem, a greedy algorithm has an **approximation ratio** (or **approximation factor**) of $\alpha \in (0,1]$ if:

$$\text{OPT} \leq \frac{1}{\alpha} \cdot \text{ALG}$$

where $\text{OPT}$ is the optimal solution value and $\text{ALG}$ is the greedy algorithm's solution value. Similarly, for minimization, $\text{ALG} \leq \alpha \cdot \text{OPT}$.

The algorithm constructs a solution by repeatedly selecting the element that maximizes immediate gain (for maximization) or minimizes immediate cost (for minimization), without reconsidering previous choices.

## Key Equations

### Approximation Ratio

For a maximization problem with optimal value $f^*$ and greedy algorithm value $f_{\text{greedy}}$:

$$\rho = \frac{f^*}{f_{\text{greedy}}}$$

This ratio $\rho$ is the **approximation factor**—a value close to 1 indicates strong performance.

### Submodular Function Property

Many greedy analyses rely on submodular functions, where marginal gains diminish:

$$f(S \cup \{e\}) - f(S) \geq f(T \cup \{e\}) - f(T) \quad \text{for } S \subseteq T$$

### Greedy Marginal Gain Selection

At iteration $i$, select element $e_i$ maximizing:

$$e_i = \arg\max_{e \notin S_{i-1}} \left[ f(S_{i-1} \cup \{e\}) - f(S_{i-1}) \right]$$

---

## Physical Intuition / Derivation

### Why Greedy Works (Sometimes)

Greedy algorithms are attractive because they:

1. **Run in polynomial time**: Each iteration examines remaining candidates and selects one, typically in $\mathcal{O}(n^2)$ or better.
2. **Make intuitive decisions**: Select the "best next step" without complex lookahead.

However, greedy is **not optimal** in general. The approximation ratio quantifies how much quality is sacrificed for speed.

### Submodular Greedy Analysis

When optimizing a monotone submodular function under a cardinality constraint (select $k$ items), the **greedy algorithm achieves a $(1 - 1/e)$-approximation** ($\approx 0.632$):

$$f_{\text{greedy}} \geq \left(1 - \frac{1}{e}\right) f^*$$

**Intuition**: Submodularity ensures that even as the greedy set $S$ grows, each new element still contributes substantially. The factor $(1-1/e)$ emerges from summing a geometric series in the proof.

### Why Approximation Ratios Matter

- A $0.4$-approximation algorithm guarantees the solution is at least $40\%$ as good as optimal.
- For NP-hard problems, this is often the best we can do in polynomial time (unless $\text{P} = \text{NP}$).
- Different problem structures yield different ratios: submodular valuations often achieve constant factors; some problems admit PTAS; others have hardness barriers.

---

## Applications in Engineering

### 1. Resource Allocation

**Max-Min Fairness**: Allocate items (resources, tasks, bandwidth) to multiple agents to maximize the minimum satisfaction.

- **Example** (from source): Allocate computational jobs to servers where each server has identical submodular satisfaction functions. Greedy achieves $0.4$-approximation.
- **Engineering relevance**: Load balancing in cloud systems, fair task distribution in parallel computing.

### 2. Network Design & Centrality

**Group Closeness Centrality Maximization**: Select a $k$-node subset to minimize average distance to all other nodes, improving network resilience.

- **Example** (from source): Place $k$ relay stations to maximize coverage. Greedy provides a $1/5$-approximation.
- **Engineering relevance**: Sensor network deployment, facility location, emergency response infrastructure.

### 3. Facility Location & Coverage

**Set Cover & Dominating Set Problems**: Select facilities to cover maximum demand with minimum resources.

- Greedy achieves $\ln(n)$-approximation for weighted set cover.
- **Applications**: Hospital placement, cell tower siting, sensor deployment.

### 4. Submodular Optimization in ML

**Feature Selection, Data Summarization**: Greedily select representative samples or informative features.

- **Example**: Summarize large datasets by selecting diverse, representative elements.
- Greedy is within $(1-1/e)$ of optimal for monotone submodular objectives.

### 5. Matroid-Constrained Allocation

**Combinatorial Auctions & Matching**: Allocate items under independence constraints (e.g., knapsack, partition constraints).

- **Example** (from source): Allocate under $k$ matroid constraints with $\mathcal{O}(k)$-approximation.
- **Engineering**: Procurement optimization, vehicle routing under fleet constraints.

---

## Common Mistakes / Pitfalls

### 1. Assuming Greedy is Always Optimal
**Error**: Applying greedy without checking if the problem structure supports it.

**Reality**: Greedy is optimal only for specific problems (e.g., Dijkstra, MST, interval scheduling). For many NP-hard problems, it can be arbitrarily bad.

**Example**: Greedy graph coloring can use $n$ colors when 2 suffice (bipartite graph).

### 2. Confusing Approximation Ratio Direction
**Error**: Stating "greedy is a $0.4$-approximation" to mean the solution is 40% worse.

**Reality**: For maximization, $0.4$-approximation means greedy ≥ $0