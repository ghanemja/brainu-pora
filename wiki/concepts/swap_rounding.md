# Swap Rounding

## Definition

**Swap rounding** is a randomized rounding technique used in combinatorial optimization to convert fractional solutions (elements of a polytope) into integral solutions while maintaining strong concentration guarantees. It operates by iteratively:

1. Solving the fractional relaxation to obtain a fractional point in a polytope
2. Identifying a subset of fractional elements with bounded maximum density
3. Rounding this subset to an integral solution (coloring)
4. Removing the rounded elements and recursing on the remaining fractional elements

The key property is that it guarantees **tight concentration**—the fractional density drops reliably at each step by approximately a $(1-\varepsilon)$ factor, enabling controlled approximation and decomposition algorithms.

## Key Equations

For a matroid $M = (U, \mathcal{I})$ with rank function $r : 2^U \to \mathbb{Z}_+$:

**Matroid Polytope:**
$$P(M) = \left\{x \in \mathbb{R}^U_+ : x(S) \leq r(S) \text{ for all } S \subseteq U\right\}$$

**Edmonds' Condition (Chromatic Number):**
$$\chi(M) = \max_{S \subseteq U} \left\lceil \frac{|S|}{r(S)} \right\rceil$$

**Fractional Feasibility:**
For any $q \geq \chi(M)$, the uniform fractional point satisfies:
$$\frac{\mathbf{1}}{q} \in P(M)$$

where $\mathbf{1}$ is the all-ones vector and $\chi(M)$ is the matroid's coloring number.

**k-Matroid Intersection:**
Given $k$ matroids $M_1, \ldots, M_k$ over ground set $U$, the intersection independence system is:
$$\mathcal{I}_{\text{int}} = \bigcap_{i \in [k]} \mathcal{I}_i$$

## Physical Intuition / Derivation

### Motivation

The swap rounding framework addresses a fundamental problem: given a fractional feasible solution (e.g., $x = \frac{\mathbf{1}}{q}$ in a matroid polytope), how do we systematically convert it to an integral solution while controlling the approximation quality?

### The Peeling Algorithm

**Core Idea:** Rather than rounding all elements at once, swap rounding uses a **layer-by-layer peeling strategy**:

1. **Solve Fractional Relaxation:** Compute a fractional solution $x^*$ in polytope $P(M)$ (or intersection polytope for multiple matroids)

2. **Identify Dense Subset:** Find a subset $R \subseteq U$ of elements with bounded maximum density. This is feasible because:
   - By Edmonds' condition, density $\frac{|S|}{r(S)} \leq \chi(M)$ for all $S$
   - Elements can be grouped into color classes $R_1, \ldots, R_k$ where each class is independent

3. **Round and Peel:** 
   - Color all elements in $R_i$ the same color (commit to an independent set)
   - Remove colored elements from consideration
   - Recurse on uncolored elements $U \setminus R$

4. **Concentration Guarantee:** The fractional density of remaining elements decreases reliably because the matroid structure guarantees that each maximal independent set covers a constant fraction of remaining mass.

### Why Tight Concentration Matters

Tight concentration means that at each iteration $t$, the **remaining fractional mass** shrinks predictably:
$$\text{remaining density} \approx (1-\varepsilon) \cdot \text{previous density}$$

This ensures the algorithm terminates in $O(\log n)$ iterations with polylogarithmic approximation factors—far better than naive round-and-cut approaches.

## Applications in Engineering

### 1. **Resource Allocation & Scheduling**
- **Network Design:** Decomposing fractional edge allocations in multi-commodity flow problems into integral routing tables
- **Wireless Scheduling:** Converting fractional spectrum allocations (fractional matchings in interference graphs) into realizable integer schedules across time slots

### 2. **Matroid-Based Optimization**
- **Processor Task Assignment:** Partitioning tasks among multiple processors where independence constraints represent processor capabilities
- **Dependency Resolution:** Software package management systems use matroid intersection to respect compatibility constraints while minimizing install complexity

### 3. **Combinatorial Approximation Algorithms**
- **Submodular Maximization:** Approximating optimal solutions when optimizing submodular objectives subject to matroid constraints
- **Machine Learning:** Feature selection under cardinality and diversity constraints (e.g., selecting diverse training examples)

### 4. **Supply Chain & Logistics**
- **Inventory Routing:** Decomposing fractional delivery routes into feasible integer routes respecting vehicle capacity and time window constraints

## Common Mistakes / Pitfalls

### 1. **Assuming Arbitrary Polytopes Work**
- **Error:** Applying swap rounding to general integer programs
- **Reality:** Requires special structure (matroids, polymatroids, or submodular functions) where tight concentration can be guaranteed
- **Fix:** Verify Edmonds' condition or stronger geometric properties before applying

### 2. **Confusing Chromatic Number with Approximation Ratio**
- **Error:** Thinking $\chi(M) = q$ means the algorithm achieves $q$-approximation
- **Reality:** $\chi(M)$ is the minimum number of colors needed; the approximation ratio depends on the specific objective and constraints
- **Fix:** Analyze the objective function loss separately from the decomposition quality

### 3. **Neglecting Residual Elements**
- **Error:** Ignoring fractional elements that don't fit into identified color classes
- **Reality:** Swap rounding peels iteratively; must account for all remaining mass through recursion
- **Fix:** Track total fractional mass and ensure concentration bounds apply to remaining mass, not just identified dense subsets

### 4. **Misapplying to Non-Loopless Matroids**
- **Error:** Using