# Monotone Functions

## Definition

A **monotone function** $g: [n]^k \to \mathbb{R}^k$ is a function where the output respects a partial order on the input domain. More precisely, for inputs $x, y \in [n]^k$:

$$x \preceq y \implies g(x) \preceq g(y)$$

where $\preceq$ denotes coordinate-wise partial order (each coordinate of $g(x)$ is less than or equal to the corresponding coordinate of $g(y)$).

### Monotone Partial Information (PI) Functions

A **monotone PI function** $p$ is a partial specification of a monotone function, where each coordinate $p(x)_i$ for point $x \in [n]^k$ and index $i \in [k]$ may take values in:
- **Definite values**: $\{-1, 0, +1\}$ (fully specified)
- **Indefinite values**: $\{\geq, \leq\}$ (constrained but not fully determined)

A function $g$ is **consistent** with a monotone PI function $p$ if:
- Whenever $p(x)_i \in \{-1, 0, +1\}$, we have $g(x)_i = p(x)_i$
- Whenever $p(x)_i = \geq$, we have $g(x)_i \in \{0, +1\}$
- Whenever $p(x)_i = \leq$, we have $g(x)_i \in \{-1, 0\}$

### Candidate Sets

For a monotone PI function $p$, a set $S \subseteq [n]^k$ is a **candidate set** $\text{Cand}(p)$ if:

$$\forall \text{ monotone functions } g \text{ consistent with } p, \exists x \in S: g(x) \succcurlyeq 0^{k+1} \text{ or } g(x) \preccurlyeq 0^{k+1}$$

In other words, every monotone function agreeing with the partial information $p$ must have at least one **fixed point** or **zero crossing** within $S$.

## Key Equations

**Tarski's Fixed Point Theorem** (continuous version):
$$\text{If } g: \mathbb{R}^k \to \mathbb{R}^k \text{ is monotone and continuous, then } \exists x: g(x) = x$$

**Discrete analog (Tarski*)**: For discrete monotone functions $g: [n]^k \to [n]^k$, a solution exists satisfying:
$$g(x) \geq x \text{ or } g(x) \leq x$$

**Query Complexity Target**: An algorithm achieving Objectives 1 and 2 yields:
$$Q(n,k) = O(k \log n)$$

where $Q(n,k)$ is the number of queries needed to find a fixed point.

## Physical Intuition / Derivation

### Why Monotone Functions Matter

Monotone functions naturally model systems where **increasing inputs cannot decrease outputs**. Examples include:
- Economic equilibrium models (price increase → supply increase)
- Network flows (capacity increase → throughput increase)
- Potential energy landscapes (displacement respects energy ordering)

### The Candidate Set Approach

The key insight is that **partial information about a function constrains where solutions must exist**:

1. **Start** with trivial candidate set $S_0 = [n]^k$ (all possible points)
2. **Query** a strategic point $q$ to refine the PI function
3. **Update** to PI function $p'$ incorporating the query result
4. **Shrink** candidate set to $S_1$ such that $|S_1| \leq (1-\alpha)|S_0|$
5. **Repeat** until candidate set contains a provable fixed point

### The Paradox

Simply taking $S = [n]^k$ trivially satisfies the definition but provides no algorithmic advantage. Conversely, the theoretically *smallest* candidate set is hard to construct and reason about. **Safe PI functions** resolve this by providing candidate sets that are:
- **Structurally simple** (efficiently computable)
- **Sufficiently small** (non-trivial reduction per iteration)

## Applications in Engineering

### 1. **Algorithmic Game Theory**
Finding Nash equilibria in games corresponds to finding fixed points of monotone best-response functions. The candidate set framework provides query-efficient algorithms for computing equilibria.

### 2. **Supply Chain Optimization**
Monotone functions model inventory and demand relationships. Candidate sets identify feasible regions where equilibrium pricing exists without exhaustive search.

### 3. **Electrical Network Analysis**
Power flow in grids exhibits monotone properties (higher voltage increases reactive power). Candidate sets localize feasible operating points.

### 4. **Machine Learning / Optimization**
Monotone neural networks constrain outputs to preserve input ordering—useful for ranking, preference learning, and constrained optimization. Identifying candidate solution regions reduces search cost.

### 5. **Control Theory**
Monotone dynamical systems (e.g., compartmental models) have stable equilibria. Candidate sets bound the basin of attraction without simulation.

## Common Mistakes / Pitfalls

### Mistake 1: Confusing Global vs. Coordinate-wise Monotonicity
**Wrong**: Thinking $f(x) \leq f(y)$ (scalar comparison) implies monotone function.
**Right**: Require $f(x) \preceq f(y)$ **coordinate-wise**. A function can be non-monotone globally but monotone in each coordinate separately.

### Mistake 2: Assuming Candidate Sets Are Unique
The definition allows multiple valid candidate sets $S_1, S_2$ for the same PI function $p$. The algorithm must construct a *specific* candidate set with guaranteed shrinkage properties—not just any set satisfying the definition.

### Mistake 3: Forgetting Consistency Constraints
The partial information $p$ imposes **implicit constraints** on possible extensions. A naive algorithm may query points that immediately contradict the monotonicity requirement, wasting queries