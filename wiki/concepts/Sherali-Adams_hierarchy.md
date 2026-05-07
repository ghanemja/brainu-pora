# Sherali-Adams Hierarchy

## Definition

The **Sherali-Adams hierarchy** is a sequence of progressively tighter linear/semidefinite programming (SDP) relaxations of a combinatorial optimization problem. It is a systematic method for constructing convex relaxations of NP-hard problems by lifting the original problem into a higher-dimensional space.

Formally, given a 0-1 integer program (or more generally, a polynomial optimization problem), the $t$-th level of the Sherali-Adams hierarchy is obtained by:

1. **Introducing lifted variables**: For any subset $S \subseteq \{1, 2, \ldots, n\}$ with $|S| \leq t+1$, introduce variables $y_S$ intended to represent the joint assignment of variables indexed by $S$.

2. **Adding consistency constraints**: Enforce that marginalization is consistent—the probability/value assigned to subsets must be consistent with their supersets and subsets.

3. **Imposing semidefinite constraints**: Require a moment matrix (constructed from these lifted variables) to be positive semidefinite.

The $t$-th level can be formulated as an SDP with dimension $\binom{n}{t+1}$ variables. At $t = n-1$, the hierarchy recovers the original integer program exactly.

## Key Equations

**Original 0-1 integer program:**
$$\min \, \mathbf{c}^T \mathbf{x} \quad \text{s.t.} \quad A\mathbf{x} \leq \mathbf{b}, \, \mathbf{x} \in \{0,1\}^n$$

**Sherali-Adams $t$-level relaxation variables:**
For $S \subseteq [n]$ with $|S| \leq t+1$:
$$y_S \approx \prod_{i \in S} x_i \quad \text{(lifted variable)}$$

**Marginalization (consistency) constraints:**
$$y_S = \sum_{j \notin S} y_{S \cup \{j\}} \quad \text{(sum-to-one structure)}$$

**Positive semidefiniteness constraint:**
The moment matrix $M_t$ constructed from $\{y_S\}$ must satisfy:
$$M_t \succeq 0$$

**Hierarchy property:**
$$\text{OPT}_{t=0} \geq \text{OPT}_{t=1} \geq \cdots \geq \text{OPT}_{t=n-1} = \text{OPT}_{\text{exact}}$$

where $\text{OPT}_t$ is the optimal value of the $t$-th level relaxation.

## Physical Intuition / Derivation

### Building Intuition

Imagine trying to solve a hard combinatorial problem like maximum cut or vertex cover. The naive linear programming relaxation directly relaxes $\mathbf{x} \in \{0,1\}$ to $\mathbf{x} \in [0,1]$, but this is often too loose—the LP optimum may be far from the integer solution.

The Sherali-Adams hierarchy improves this by asking: *"What if we track not just individual variables $x_i$, but also their pairwise (or higher-order) joint distributions?"*

- **Level 0**: Only individual variables (standard LP relaxation)
- **Level 1**: Track pairs of variables; impose that $y_{\{i,j\}} \approx x_i x_j$
- **Level $t$**: Track all correlations up to $t+1$ variables

The **moment matrix** (PSD constraint) ensures that these lifted variables are "realizable"—i.e., they could plausibly arise from an actual 0-1 assignment. By requiring $M_t \succeq 0$, we enforce subtle consistency properties that eliminate many infeasible fractional solutions.

### Why It Works

At higher levels $t$, the lifted variables capture more structure about the correlations in the solution. The consistency constraints become increasingly restrictive. Eventually, at $t = n-1$, the only feasible solutions are the true integral solutions.

## Applications in Engineering

### 1. **Combinatorial Optimization**
- Maximum cut, graph coloring, vertex cover, and other NP-hard problems
- Provides approximation guarantees when exact solutions are intractable
- Used in chip design, circuit verification, and network optimization

### 2. **Low-Rank Matrix Approximation**
- **Entrywise low-rank approximation** (from source): Finding rank-$k$ matrices minimizing entrywise $\ell_p$ norm (p ≠ 2)
- Using Sherali-Adams hierarchy yields first polynomial-time approximation scheme for $p > 2$
- Applications: image compression, tensor decomposition, data analysis

### 3. **Quantum Information and Correlation Clustering**
- Matrix $p \rightarrow q$ norm approximation
- Related to small-set expansion and nonlocal games
- Additive approximation algorithms for $p < 2 < q$ regime

### 4. **Approximation Algorithms**
- General framework for designing approximation schemes when known techniques (sketching, column selection) fail
- Particularly useful for continuous optimization embedded in combinatorial structure

### 5. **Machine Learning & Statistics**
- Clustering and community detection
- Structured prediction with combinatorial constraints
- Lift-and-project techniques in algorithm design

## Common Mistakes / Pitfalls

1. **Confusing the hierarchy with LP relaxation**
   - Sherali-Adams is not just the standard LP relaxation; it includes higher-order constraints and PSD requirements
   - Requires SDP solving, not just LP

2. **Overestimating computational tractability**
   - While polynomial-time, the $t$-th level has $\binom{n}{t+1}$ variables
   - For moderate $t$ (e.g., $t=3$) on large $n$, the SDP can be computationally demanding
   - Not a practical algorithm for every problem despite theoretical guarantees

3. **Forgetting the hierarchy is not tight**
   - Sherali-Adams may require exponentially many levels to match the integrality gap exactly for some problems
   -