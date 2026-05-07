# PTAS (Polynomial Time Approximation Scheme)

## Definition

A **Polynomial Time Approximation Scheme (PTAS)** is a family of approximation algorithms for an optimization problem that, for any fixed error tolerance $\varepsilon > 0$, produces a $(1+\varepsilon)$-approximation in time polynomial in the input size $n$, though the polynomial's degree may depend on $\varepsilon$.

Formally, for a minimization problem with optimal solution value $\text{OPT}$, a PTAS algorithm $A_\varepsilon$ computes a solution $s$ satisfying:

$$\text{cost}(s) \leq (1+\varepsilon) \cdot \text{OPT}$$

in time $\text{poly}(n) \cdot f(\varepsilon)$, where $f(\varepsilon)$ is some function (potentially exponential in $1/\varepsilon$).

**Related concept:** An **FPTAS** (Fully Polynomial Time Approximation Scheme) strengthens this to time $\text{poly}(n, 1/\varepsilon)$, making it practical even for small $\varepsilon$.

## Key Equations

For a minimization problem with PTAS guarantee:

$$A_\varepsilon(\text{input}) \leq (1 + \varepsilon) \cdot \text{OPT}$$

**Approximation ratio:**
$$\rho = 1 + \varepsilon$$

**Time complexity:**
$$T(n, \varepsilon) = O(n^{p(1/\varepsilon)})$$

where $p(\cdot)$ is a polynomial function of $1/\varepsilon$ (often appearing as $O(n^{1/\varepsilon})$ or $O(n^{1/\varepsilon^2})$ in geometric settings).

## Physical Intuition / Derivation

### Why PTAS Matters

Many NP-hard problems admit no constant-factor approximation (unless P=NP). A PTAS sidesteps this by allowing the approximation ratio to approach 1 arbitrarily closely—the tradeoff is computational cost that grows with precision demands.

### The Separator-Based Paradigm

The source material illustrates a powerful PTAS construction technique via **planar support graphs**:

1. **Support Graph Construction:** For a geometric problem (e.g., hitting set with balls), embed the objects into a planar graph where objects correspond to nodes.

2. **Planar Separator Exploitation:** Planar graphs admit $O(\sqrt{n})$-size separators (by the Planar Separator Theorem). This means we can recursively partition the problem into smaller subproblems.

3. **Local Search with Separation:** An $O_\varepsilon(1)$-swap local search algorithm becomes a $(1+\varepsilon)$-approximation when analyzed on a planar support, since:
   - The separator bounds the interaction between problem regions
   - Swapping bounded-size subsets across separator boundaries explores a rich solution neighborhood
   - Polynomial recursion depth yields polynomial total time

### Example: Geometric Hitting Set

Given balls $\mathcal{R}$ in the plane and points $V$:
- Build a Voronoi partition of the plane with respect to ball centers
- This induces a planar dual graph
- Local search (swap up to $O(1/\varepsilon)$ points) finds a $(1+\varepsilon)$-approximate hitting set in $n^{O(1/\varepsilon)}$ time

## Applications in Engineering

### 1. **Computational Geometry & Spatial Problems**
- **Geometric hitting set / set cover**: Given regions and points, minimize points covering all regions
  - Used in sensor placement, facility location
  - PTAS via planar support graphs (as in source material)

- **Terrain guarding / Art Gallery variants**: Approximate minimum guard set
  - Robotics, surveillance system design

### 2. **Network Optimization**
- **Maximum independent set on geometric graphs**: Select non-overlapping objects (e.g., disk scheduling)
- **Dominating set in pseudodisk systems**: Minimize control/monitoring stations

### 3. **Approximation-Critical Applications**
- **VLSI routing**: Minimize wire congestion or connection cost where exact solutions are intractable
- **Manufacturing / supply chain**: Geometric facility location with PTAS guarantees enables certified near-optimal solutions at scale

### 4. **Practical Leverage**
Where exact algorithms take exponential time:
- PTAS allows choosing $\varepsilon$ pragmatically: $\varepsilon = 0.1$ (10% tolerance) may yield $n^{20}$ runtime; acceptable if $n$ is small or $\varepsilon = 0.5$ reduces exponent acceptably

## Common Mistakes / Pitfalls

### 1. **Confusing PTAS with Constant-Factor Approximation**
- **Error:** Thinking PTAS guarantees polynomial time for *all* $\varepsilon$
- **Correct:** Time is polynomial for *fixed* $\varepsilon$; as $\varepsilon \to 0$, runtime grows (potentially exponentially in $1/\varepsilon$)

### 2. **Overlooking the Role of Problem Structure**
- **Error:** Assuming PTAS exists for arbitrary NP-hard problems
- **Correct:** PTAS constructions exploit geometric, planar, or other structural properties (bounded VC dimension, planarity, etc.)
  - A problem may be NP-hard but lack these structures, making PTAS unlikely

### 3. **Ignoring the Exponential Dependence**
- **Error:** Implementing PTAS naively with small $\varepsilon$ without considering $f(\varepsilon)$ cost
- **Correct:** For $\varepsilon = 0.01$, the $n^{1/\varepsilon} = n^{100}$ factor may dominate even small instances

### 4. **Misunderstanding Planar Support Requirements**
- **Error:** Assuming any geometric problem admits a planar support
- **Correct:** The problem's structure must permit a planar graph embedding; counterexamples exist (e.g., arbitrary point-region