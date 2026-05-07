# fixed-parameter tractability

## Definition

**Fixed-parameter tractability (FPT)** is a computational complexity framework for analyzing the solvability of problems that are generally NP-hard, but become tractable when certain problem-specific parameters are treated as independent variables.

A decision problem with input size $n$ and parameter $k$ is in **FPT** if it admits an algorithm with runtime:

$$T(n, k) = f(k) \cdot n^{O(1)}$$

where $f(k)$ is a computable function depending only on $k$ (possibly exponential), and the polynomial exponent is a constant independent of both $n$ and $k$.

### Broader Complexity Hierarchy

For a problem parameterized by $k$:
- **FPT** (Fixed-Parameter Tractable): $f(k) \cdot \text{poly}(n)$ algorithm exists
- **XP** (Slice-Wise Polynomial): $n^{f(k)}$ algorithm exists (polynomial in $n$, but exponent depends on $k$)
- **para-NP-complete**: NP-hard even for fixed $k$
- **W[1]-hard**: unlikely to be in FPT (parameterized analogue of NP-hardness)

---

## Key Equations

### FPT Runtime Bound
$$T(n,k) = f(k) \cdot \text{poly}(n) = f(k) \cdot n^c$$
where $c$ is a constant and $f(k)$ is arbitrary (often exponential).

### Example: Short Secluded Path Problem
For an undirected graph $G = (V, E)$ with $|V| = n$, $|E| = m$, vertices $s, t \in V$, and parameters $k$ (path length) and $l$ (maximum neighbors):

**Problem:** Determine if there exists an $s$-$t$ path of length $\leq k$ such that the path vertices have $\leq l$ neighbors outside the path.

The problem is:
- **W[1]-hard** when parameterized by $k$ alone or cliquewidth
- **para-NP-complete** when parameterized by $l$ alone
- **FPT** when parameterized by $k + l$ or treewidth

---

## Physical Intuition / Derivation

### Why Parameters Matter

Consider a NP-hard problem on $n$ vertices. A brute-force algorithm checking all $2^n$ possibilities is infeasible for large $n$. However, many real-world instances have a **natural small parameter** $k \ll n$:

- **Shortest path length** in a network (even if finding the absolute shortest is hard)
- **Number of "forbidden" resources** in a constrained environment
- **Tree decomposition width** (structural parameter of the graph)

### The Core Insight

Rather than asking "can we solve this in $\text{poly}(n)$?", FPT asks:

> **Can we solve this efficiently by isolating hardness into a single parameter?**

If yes, then for small $k$, the problem becomes practical even if $n$ is large.

### Example: Parameterization in Secluded Paths

The **Short Secluded Path problem** on a graph:
- Naive approach: try all $O(n^k)$ paths of length $k$ and check seclusion $\Rightarrow$ intractable
- **FPT approach (parameterized by $k+l$)**: Use dynamic programming that explores only "promising" paths while tracking neighbors, with state space bounded by $2^{k+l}$

---

## Applications in Engineering

### 1. **Network Security & Routing**
   - **Secure communication channels**: Find transmission paths that minimize exposure to potential eavesdropping nodes
   - **Time complexity**: With $k$ = path length and $l$ = exposure threshold, FPT algorithms allow real-time routing decisions even on large networks
   - **Concrete example**: An organization routing classified data through a network needs a path that passes through $\leq l$ "untrusted" relay points while keeping path length reasonable

### 2. **Robotics & Motion Planning**
   - **Obstacle-aware pathfinding**: Find trajectories that minimize interaction with sensor-rich regions (noise sources, potential collision zones)
   - **Parameter**: $k$ = trajectory length, $l$ = max "risky zone" contacts
   - **Advantage**: Unlike Dijkstra (which optimizes only distance), FPT algorithms can simultaneously optimize path length AND environmental interaction

### 3. **Transportation & Logistics**
   - **Convoy routing**: Military/commercial convoys need routes avoiding maximum $l$ hostile regions while staying within distance $k$
   - **Pandemic routing**: During disease outbreaks, find delivery routes minimizing contact with affected areas
   - **Computational model**: FPT algorithm makes real-time route planning feasible for large city graphs

### 4. **Power Grid & Infrastructure**
   - **Critical path protection**: Identify transmission lines connecting substations with minimal exposure to geological hazard zones
   - **Parameter**: $l$ = number of vulnerable segments; $k$ = maximum detour distance
   - **Benefit**: Guarantees polynomial-time solutions when these parameters are naturally small

### 5. **VLSI & Chip Design**
   - **Wire routing in circuit layouts**: Route signals through regions minimizing interference (cross-talk)
   - **Structural parameter**: treewidth of the routing grid $\Rightarrow$ FPT solutions for complex layouts
   - **Impact**: Enables exact optimization where heuristics previously dominated

---

## Common Mistakes / Pitfalls

### 1. **Confusing XP with FPT**
   - ❌ "An $n^{k}$ algorithm is fixed-parameter tractable"
   - ✓ An $n^k$ algorithm is **XP**, not FPT
   - **Issue**: For $k = 10$ and $n = 1000$, $n^k = 10^{30}$ is infeasible; but $2^k \cdot n = 10^9$ (FPT) is tractable

### 2. **Ignoring Parameter Choice**
   - ❌ "This problem is FPT, so it's