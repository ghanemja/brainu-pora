# EPTAS (Efficient Polynomial-Time Approximation Scheme)

## Definition

An **Efficient Polynomial-Time Approximation Scheme (EPTAS)** is an algorithm that produces a $(1+\varepsilon)$-approximate solution to an optimization problem in time:

$$T(n, \varepsilon) = f(\varepsilon) \cdot \text{poly}(n)$$

where:
- $n$ is the input size
- $\varepsilon > 0$ is the approximation parameter (error tolerance)
- $f(\varepsilon)$ is a computable function depending *only* on $\varepsilon$ (not on $n$)
- The dependence on $1/\varepsilon$ is *single-exponential* or better (e.g., $2^{\text{poly}(1/\varepsilon)}$)

The key distinction from [[PTAS|Polynomial-Time Approximation Scheme]] is the *efficiency*: EPTAS requires the exponential blowup in $1/\varepsilon$ to be polynomial rather than superpolynomial.

### Formal Approximation Guarantee

For a minimization problem with optimal value $\text{OPT}(I)$ and approximate solution value $A(I)$:

$$A(I) \leq (1 + \varepsilon) \cdot \text{OPT}(I)$$

holds for any instance $I$ and any $\varepsilon > 0$.

---

## Key Equations

### Time Complexity Classes

**PTAS (weaker):**
$$T(n, \varepsilon) = n^{f(1/\varepsilon)}$$

Example: $T(n, \varepsilon) = n^{1/\varepsilon^2}$ — **superpolynomial in $n$ for fixed $\varepsilon$**

**EPTAS (stronger):**
$$T(n, \varepsilon) = 2^{\text{poly}(1/\varepsilon)} \cdot n^c$$

Example: $T(n, \varepsilon) = 2^{O(1/\varepsilon^2)} \cdot n^3$ — **polynomial in $n$, fixed exponent**

### Example: Planar Steiner Tree

From the source material, the EPTAS for planar Steiner Tree achieves:

$$T(n, \varepsilon) = 2^{\text{poly}(1/\varepsilon)} \cdot n^{O(1)}$$

This improves the earlier bound of $2^{2^{\text{poly}(1/\varepsilon)}} \cdot n^{O(1)}$.

---

## Physical Intuition / Derivation

### Why EPTAS Matters

In practical optimization, we often face a tension:
- **Smaller $\varepsilon$** (better approximation) requires more computation
- **Larger $n$** (bigger problem) should scale gracefully

**PTAS allows** $T \sim n^{1/\varepsilon^2}$: even with just 100 vertices ($n=100$), setting $\varepsilon=0.1$ gives $n^{100}$ time—**infeasible**.

**EPTAS allows** $T \sim 2^{1/\varepsilon^2} \cdot n^3$: with $n=100, \varepsilon=0.1$, we get $2^{100} \cdot 10^6$ operations, which is still large but the **polynomial** scaling in $n$ means the algorithm remains viable for problem-specific preprocessing and small instances.

### Structural Insights: The Spanner Approach

The source material reveals the key technique: **spanner construction**. For Geometric Subset TSP on intersection graphs:

1. **Spanner Property**: Reduce instance $(G, T)$ to a smaller induced subgraph $G' \subseteq G$ such that:
   - $|V(G')| \leq O_{\beta,\delta}(1/\varepsilon^{10}) \cdot \text{OPT}$
   - $\text{cost}(G', T) \leq (1+\varepsilon) \text{cost}(G, T)$
   
2. **Solve on Reduced Instance**: The small spanner can be solved exactly (or approximately) in $2^{|V(G')|}$ time, achieving EPTAS overall.

This is the **key insight**: by controlling the problem size as a function of $\varepsilon$ alone, we isolate the exponential dependence.

---

## Applications in Engineering

### 1. **Computational Geometry & GIS**
- **Facility location** in unit disk intersection graphs (wireless sensor networks, cell tower placement)
- **Steiner tree problems** on road networks approximated by geometric graphs
- Guaranteed near-optimal solutions with controllable runtime for real-world instances

### 2. **Network Design**
- **Subset TSP** for routing with terminal subsets (delivery networks, evacuation routes)
- Spanner-based preprocessing reduces networks from millions to thousands of vertices
- Example: optimizing delivery routes in urban logistics

### 3. **Approximation Algorithms in Practice**
- When **exact optimization is NP-hard** but we can afford $\varepsilon=0.1$ (10% approximation)
- **Trade-off parameter**: user specifies error tolerance; algorithm runs accordingly
- Superior to PTAS when $n$ is large (e.g., $n > 10^6$)

### 4. **Geometric Intersection Problems**
- **Unit disk graphs** model wireless communication range constraints
- Fat polygon collections model real geometric objects (imperfect circles, irregular shapes)
- EPTAS results extend to "similarly-sized" objects where size ratios are bounded

---

## Common Mistakes / Pitfalls

### 1. **Confusing EPTAS with PTAS**
**Wrong**: "Both EPTAS and PTAS are polynomial; EPTAS is just a newer name."

**Correct**: 
- PTAS: $T(n,\varepsilon) = n^{1/\varepsilon^2}$ is polynomial *per instance* but has **variable exponent**
-