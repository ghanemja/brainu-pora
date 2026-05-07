# Tarski Fixed Point Theorem

## Definition

**Tarski's Fixed Point Theorem** states that every monotone function over a complete lattice has at least one fixed point.

Formally: Let $(L, \preceq)$ be a complete lattice and $f: L \to L$ a **monotone** (or order-preserving) function, meaning:
$$a \preceq b \implies f(a) \preceq f(b)$$

Then there exists at least one element $x^* \in L$ such that:
$$f(x^*) = x^*$$

Moreover, the set of all fixed points forms a complete lattice under the order $\preceq$.

### Key Terminology

- **Complete Lattice**: A partially ordered set where every subset has both a least upper bound (supremum) and greatest lower bound (infimum)
- **Monotone Function**: A function preserving the order relation
- **Least Fixed Point**: The smallest element satisfying $f(x) = x$, denoted $\mu f$
- **Greatest Fixed Point**: The largest element satisfying $f(x) = x$, denoted $\nu f$

## Key Equations

**Least Fixed Point Characterization:**
$$\mu f = \bigwedge \{x \in L : f(x) \preceq x\}$$

**Greatest Fixed Point Characterization:**
$$\nu f = \bigvee \{x \in L : x \preceq f(x)\}$$

**Iterative Computation (for $k$ iterations from bottom element $\bot$):**
$$f^0(\bot) = \bot, \quad f^{n+1}(\bot) = f(f^n(\bot))$$

For a finite lattice, the least fixed point is reached in at most $|L|$ iterations.

**Query Complexity (from source):** For finding a Tarski fixed point over $[n]^k$:
$$O(\log^{\lceil(k-1)/3\rceil+1} n) \text{ queries}$$

## Physical Intuition / Derivation

### Why Fixed Points Must Exist

Consider the **ascending chain** starting from the bottom element $\bot$ of the lattice:
$$\bot \preceq f(\bot) \preceq f^2(\bot) \preceq f^3(\bot) \preceq \cdots$$

Because $f$ is monotone, each application preserves order. In a finite lattice, this chain must stabilize at some point $x^*$ where $f(x^*) = x^*$.

**Intuitive picture**: Think of $f$ as a transformation that "respects" ordering. If you start at the smallest element and keep applying the transformation, you climb monotonically through the lattice. Since the lattice is finite (or has well-founded structure), you must eventually reach a resting point.

### Graphical Intuition

In a 1D setting where $L = \{1, 2, \ldots, n\}$ with standard ordering:
- A monotone function $f$ has its graph as a non-decreasing curve
- Any such curve must intersect the diagonal line $y = x$ at least once
- Each intersection is a fixed point

For higher dimensions, the monotonicity ensures sufficient structure that fixed points cannot be avoided.

## Applications in Engineering

### 1. **Verification & Model Checking**
- Computing the largest (or smallest) set of states satisfying a temporal logic property
- **μ-calculus model checking**: Properties are expressed as fixed points of monotone functions over state sets
- Finding reachable states in systems: Start from initial states, iteratively apply the transition relation until reaching a fixed point

### 2. **Game Theory & Equilibria**
- **Supermodular games**: Pure strategy Nash equilibria exist and correspond to fixed points of best-response dynamics
- Computing value functions in repeated games via value iteration (a fixed-point algorithm)
- **Parity games & mean-payoff games**: Finding winning regions reduces to computing Tarski fixed points

### 3. **Static Program Analysis**
- **Data flow analysis**: Computing invariants (e.g., reaching definitions, live variables) as fixed points of monotone transfer functions
- **Abstract interpretation**: Program semantics computed via fixed-point iteration over abstract domains
- Type inference in programming languages

### 4. **Financial Networks & Stability**
- **Financial contagion analysis**: Computing the set of solvent institutions as a fixed point of clearing functions
- Stability analysis in networks with interdependencies
- Determining which agents default given feedback effects

### 5. **Control Theory & Distributed Systems**
- **Consensus algorithms**: Fixed points correspond to consensus values in distributed protocols
- Convergence of iterative control systems
- Computing greatest invariant sets that guarantee safety properties

### 6. **Image Processing & Computer Vision**
- Morphological operations (dilation, erosion) and their fixed points
- Watershed segmentation using iterative refinement
- Texture analysis via iterative filtering

## Common Mistakes / Pitfalls

### 1. **Assuming Uniqueness**
A monotone function may have *many* fixed points. The theorem guarantees existence, not uniqueness. For uniqueness, additional conditions (e.g., strict monotonicity under certain constraints) are required.

### 2. **Forgetting the Monotonicity Requirement**
A function that is *not* monotone may have no fixed points. Example: $f(x) = 2 - x$ on $[0, 2]$ is antitone (order-reversing), and while it has a fixed point ($x=1$), this is *not* because of Tarski's theorem.

### 3. **Confusing Lattice Requirements**
Tarski's theorem requires a **complete lattice** (every subset has a supremum and infimum), not just a partial order. Finite lattices are always complete, but infinite ones may not be. For instance, the real numbers $\mathbb{R}$ with standard order is *not* a complete lattice.

### 4. **Misapplying Iteration**
- Starting iteration from the wrong element (use $\bot$ for least fixed point, $\top$ for greatest)
- Assuming iteration always converges in reasonable time (finite lattices guarantee convergence, but size matters for computational complexity)
- Confusing the number of iterations needed (can be exponential in