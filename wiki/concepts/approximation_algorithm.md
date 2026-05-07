# Approximation Algorithm

## Definition

An **approximation algorithm** is a polynomial-time algorithm that solves an optimization problem by producing a solution whose cost is guaranteed to be within a provable factor of the optimal solution. For a minimization problem, an algorithm is said to be a $c$-approximation algorithm (or have approximation ratio $c$) if:

$$\text{Cost}(\text{ALG}) \leq c \cdot \text{OPT}$$

where $c \geq 1$ is the approximation factor, ALG denotes the solution produced by the algorithm, and OPT is the cost of an optimal solution.

For maximization problems, the relationship is inverted: $\text{ALG} \geq \frac{1}{c} \cdot \text{OPT}$.

**Key distinction from exact algorithms:** Approximation algorithms are designed for intractable problems (typically NP-hard) where finding optimal solutions is computationally infeasible. They trade solution quality for computational tractability.

## Key Equations

For a **minimization problem** with approximation ratio $\alpha$:
$$\text{ALG}(I) \leq \alpha \cdot \text{OPT}(I) \quad \forall \text{ instances } I$$

For a **maximization problem** with approximation ratio $\alpha \geq 1$:
$$\text{ALG}(I) \geq \frac{1}{\alpha} \cdot \text{OPT}(I) \quad \forall \text{ instances } I$$

A **Fully Polynomial-Time Randomized Approximation Scheme (FPRAS)** achieves:
$$\text{Cost}(\text{ALG}) \leq (1+\varepsilon) \cdot \text{OPT}$$
in time polynomial in both the input size $n$ and $\frac{1}{\varepsilon}$:
$$T(n, \varepsilon) = \text{poly}\left(n, \frac{1}{\varepsilon}\right)$$

## Physical Intuition / Derivation

### Why Approximation Matters

Many real-world optimization problems—from network design to resource allocation—are computationally hard. Rather than spending exponential time computing exact solutions, approximation algorithms acknowledge this barrier and instead focus on guaranteeing a solution *close enough* to optimal in polynomial time.

### Constructive vs. Non-Constructive Gaps

A fundamental challenge in algorithmic design is the **constructive-nonconstructive gap**: existence proofs (often via probabilistic or algebraic methods) may guarantee solutions without providing efficient algorithms to find them. The source material illustrates this by:

1. Proving via combinatorial arguments that a coloring exists with specific properties (non-constructive)
2. Developing an LP-relaxation and rounding technique to *construct* such a coloring algorithmically (constructive)

### LP-Rounding Strategy

A powerful framework for approximation involves:

1. **Formulate** the discrete problem as an integer linear program (ILP)
2. **Relax** the integrality constraints to obtain an LP with fractional solutions
3. **Solve** the LP efficiently (polynomial time)
4. **Round** the fractional solution back to an integer solution while controlling the factor loss

The approximation ratio often follows from:
$$\text{Cost}(\text{rounded}) \leq \alpha \cdot \text{Cost}(\text{LP relaxation}) \leq \alpha \cdot \text{OPT}$$

since $\text{Cost}(\text{LP relaxation}) \leq \text{OPT}$ for a minimization problem.

### Example from Source Material

For **$k$-matroid-intersection coloring**:
- The problem is NP-hard in general
- Prior work achieved an $O(k \log n)$-approximation via reduction to set cover
- The new approach using LP-rounding achieves a $k(k-1)$-approximation
- For fixed $k$, this is the **first constant-factor approximation**

## Applications in Engineering

### 1. Network and Resource Optimization
- **Load balancing** across servers: approximate min-makespan scheduling
- **Network routing**: approximating min-cost flows subject to multiple capacity constraints
- **Spectrum allocation**: assigning frequency bands to transmitters under interference constraints

### 2. Combinatorial Optimization Problems

| Problem | Approximation Algorithm | Ratio |
|---------|------------------------|----|
| Vertex Cover | Greedy/LP-rounding | $2$ |
| Set Cover | Greedy (ln $n$) | $O(\log n)$ |
| Traveling Salesman (metric) | Christofides | $1.5$ |
| Max Cut | SDP-based | $0.878$ |

### 3. Matroid-Based Applications
- **Matroid intersection coloring** (from source): scheduling tasks under multiple resource constraints
- **Basis selection**: selecting diverse feature sets with rank constraints in machine learning
- **Graphic matroid problems**: routing and spanning tree optimizations

### 4. Practical Engineering Use Cases
- **VLSI design**: wire routing under multiple constraint hierarchies
- **Facility location**: balancing distance to customers against setup costs
- **Inventory management**: selecting SKUs subject to storage and demand constraints

## Common Mistakes / Pitfalls

### 1. Confusing Approximation Ratio Direction
**Mistake:** Stating a 2-approximation algorithm as "achieves 50% of optimal" (incorrect for minimization).
**Correct:** A 2-approximation for minimization achieves at most *twice* the optimal cost.

### 2. Assuming Approximation Guarantees are Tight
An algorithm with a $c$-approximation *worst-case* guarantee may perform much better on average. The guarantee provides a *ceiling*, not a typical bound.

### 3. Ignoring Constant Factors in Running Time
The statement "polynomial time" can hide large constant factors. A $\text{poly}(n, 1/\varepsilon)$ FPRAS might have running time $n^{10} / \varepsilon^5$—impractical despite being theoretically polynomial.

### 4. Failing to Verify Feasibility
An approximate *solution* must satisfy all constraints; only the *objective value* is approximate. Violating