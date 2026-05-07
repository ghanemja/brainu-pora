# PTAS (Polynomial-Time Approximation Scheme)

## Definition

A **Polynomial-Time Approximation Scheme (PTAS)** is a family of approximation algorithms for an optimization problem where, for any fixed error tolerance $\varepsilon > 0$, there exists a polynomial-time algorithm that computes a solution guaranteed to be within a factor of $(1 + \varepsilon)$ of the optimal value.

More formally, a PTAS for a minimization problem is an algorithm $A_\varepsilon$ such that:
- **Input:** An instance $I$ and error parameter $\varepsilon > 0$
- **Output:** A feasible solution with objective value $\text{OPT}(I) \leq A_\varepsilon(I) \leq (1 + \varepsilon) \cdot \text{OPT}(I)$
- **Runtime:** $\text{poly}(|I|, 1/\varepsilon)$ — polynomial in instance size and the inverse of the error tolerance

### Related Terms

- **EPTAS (Efficient PTAS):** Runtime is $f(1/\varepsilon) \cdot \text{poly}(|I|)$ where $f$ is any computable function. The dependence on $1/\varepsilon$ is separated from instance size.
- **APX (Constant-Factor Approximation):** A weaker notion where the approximation ratio is a fixed constant independent of $\varepsilon$.
- **FPTAS (Fully Polynomial-Time Approximation Scheme):** Runtime is $\text{poly}(|I|, 1/\varepsilon)$ (stronger requirement than PTAS for pseudo-polynomial problems).

## Key Equations

For a minimization problem with optimal value $\text{OPT}(I)$ and approximation algorithm output $A_\varepsilon(I)$:

$$A_\varepsilon(I) \leq (1 + \varepsilon) \cdot \text{OPT}(I)$$

The **approximation ratio** is:
$$\rho = \frac{A_\varepsilon(I)}{\text{OPT}(I)} \leq 1 + \varepsilon$$

For maximization problems, the relationship reverses:
$$A_\varepsilon(I) \geq \frac{\text{OPT}(I)}{1 + \varepsilon}$$

The algorithm runtime satisfies:
$$T(|I|, \varepsilon) \in O\left(\text{poly}(|I|) \cdot \text{poly}(1/\varepsilon)\right)$$

## Physical Intuition / Derivation

### Why PTAS Matters

PTAS represents a **sweet spot** in approximation complexity:

1. **Better than constant-factor:** Unlike APX algorithms (which give fixed ratios like 1.5), PTAS lets you trade computation time for arbitrarily small error. Want error $< 0.1\%$? Run with $\varepsilon = 0.001$.

2. **Practical realizability:** Unlike exact algorithms for NP-hard problems, PTAS algorithms actually run in polynomial time for any fixed $\varepsilon$—making them genuinely executable, not merely theoretical.

3. **The $\text{poly}(1/\varepsilon)$ cost:** The price of this flexibility is that runtime grows with $1/\varepsilon$. When $\varepsilon = 0.01$, you're running an algorithm that's $\text{poly}(100)$ slower than the base case. For small $\varepsilon$, this can become prohibitive.

### Skeletal Algorithm Pattern (from source context)

The PTAS methodology often proceeds via:

1. **Spanner/Skeleton Construction:** Build a reduced subgraph $G'$ of size $\text{poly}(1/\varepsilon) \cdot \text{OPT}$ that preserves approximate distances.

2. **Shortest-Path Rerouting:** Ensure that any path taking shortcuts outside the skeleton can be rerouted within it with at most $(1+\varepsilon)$ length increase.

3. **Iterative Refinement:** Extend a boundary cycle $C$ by adding "shortcut" paths $P$ where the detour through $C$ exceeds $(1+\varepsilon)$ times the shortcut length. Each addition:
   - Increases skeleton size polynomially in $1/\varepsilon$
   - Eliminates profitable shortcuts

This technique is central to PTASs for geometric problems like **Subset TSP** and **Steiner Tree** on planar graphs and intersection graphs.

## Applications in Engineering

### Combinatorial Optimization

- **Steiner Tree Problem:** PTAS exists for planar graphs (Klein [68], extended to intersection graphs in the source material). Steiner trees are fundamental in VLSI routing, where exact solutions are intractable for large instances.
  
- **Traveling Salesman Problem (Subset TSP):** The source material references EPTAS for Subset TSP on geometric intersection graphs—crucial for vehicle routing and logistics when terminal subsets are constrained.

- **Facility Location:** PTAS algorithms allow practical approximation of warehouse/server placement problems where small optimality gaps are worth the computational cost.

### Geometric Computing

- **Polygon Intersection Graphs:** PTAS techniques apply to routing and packing problems on intersection graphs of fat objects (connected objects with bounded aspect ratio), common in motion planning and computational geometry.

- **Planar Graph Optimization:** Many infrastructure networks (road networks, circuit layouts) are planar or nearly planar, making PTAS algorithms especially valuable.

### Practical Engineering Workflow

**Trade-off analysis:** Engineers select $\varepsilon$ based on acceptable error versus time constraints:
$$\varepsilon = 0.05 \rightarrow \approx 5\% \text{ suboptimality, faster}$$
$$\varepsilon = 0.001 \rightarrow \approx 0.1\% \text{ suboptimality, slower}$$

## Common Mistakes / Pitfalls

1. **Confusing PTAS with "always fast":** PTAS is polynomial for *fixed* $\varepsilon$. For tiny $\varepsilon$