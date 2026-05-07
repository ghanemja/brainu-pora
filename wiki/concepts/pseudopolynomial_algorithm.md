# pseudopolynomial algorithm

## Definition

A **pseudopolynomial algorithm** is a deterministic algorithm whose time complexity is polynomial in both the **numeric magnitude** of the input values and the **size** of the input representation (number of variables, edges, vertices, etc.), but may be exponential in the bit-length of those values.

Formally, for a problem with input size $n$ (structural parameters like number of vertices or edges) and numeric parameter $W$ (maximum absolute value of weights/costs), a pseudopolynomial algorithm runs in time:

$$T(n, W) = \text{poly}(n, W)$$

This contrasts with:
- **Polynomial algorithms**: $T(n, \log W)$ — treat integers as atomic
- **Fully polynomial algorithms**: $T(n, \log(n/\epsilon))$ — polynomial even in logarithm of numeric values

## Key Equations

For a problem instance with:
- $n$ = number of structural elements (vertices, variables, constraints)
- $m$ = number of edges or constraints
- $W$ = maximum absolute numeric value in the input

**Pseudopolynomial complexity bounds** (examples from mean-payoff games):
$$T_{\text{pseudopoly}} = O(nmW \log W) \quad \text{(value iteration)}$$
$$T_{\text{pseudopoly}} = O(m^2 n^2 \log W) \quad \text{(GKK algorithm)}$$

Compare to:
$$T_{\text{polynomial}} = O(n^3) \quad \text{(would not depend on } W\text{)}$$
$$T_{\text{fully-poly}} = O(n^3 \log(1/\epsilon)) \quad \text{(approximation algorithms)}$$

## Physical Intuition / Derivation

### Why Pseudopolynomial Matters

Consider solving a game or optimization problem where edge weights range from $-W$ to $+W$. An algorithm might:

1. **Maintain potential values** on vertices that can accumulate to magnitude $O(nW)$ in the worst case
2. **Iterate until convergence**, with each iteration taking $O(m)$ time
3. **Converge in** $O(nW)$ iterations (the algorithm "makes progress" by $O(1)$ units per iteration across a range of $O(nW)$)

Total: $O(m \cdot nW) = O(mnW)$ — pseudopolynomial.

### The Catch: Unary vs. Binary Encoding

If $W = 2^k$ (represented with $k$ bits in **binary**), then:
$$\text{Pseudopoly time} = O(mnW) = O(mn2^k)$$

This is **exponential in the bit-length** $k$! However, if weights are given in **unary** (a string of $W$ ones), the encoding size itself is $W$, so the algorithm is polynomial in the actual input size.

### Why Algorithms Take This Form

Many graph/game problems use:
- **Potential functions** or **value iteration**: maintain numeric estimates on vertices
- **Relaxation/propagation**: refine estimates until stability
- Convergence proof shows: "value improves by ≥1 per iteration, and range is $\leq nW$"

This naturally yields $O(nW)$ iterations × $O(m)$ work per iteration.

## Applications in Engineering

### 1. **Game Theory & Verification**
Mean-payoff games (source material) model:
- Robot motion planning with long-run average cost minimization
- Network protocol verification: determine if a policy achieves average-case performance $\geq$ threshold
- Software synthesis: compute strategies to guarantee mean-payoff objectives

### 2. **Scheduling & Resource Allocation**
- **Project scheduling with costs**: minimize average cost per unit time; pseudopolynomial algorithms apply when job durations/costs are moderate integers
- **Power management**: compute policies for long-run average energy consumption

### 3. **Shortest/Longest Path Variants**
- **Bottleneck path problems**: find path minimizing maximum edge weight
- **0-1 Knapsack**, **subset sum**: classic pseudopolynomial via dynamic programming (DP depends on capacity $W$, not bit-length)
- Example: Knapsack with capacity $C$ runs in $O(nC)$ time — pseudopolynomial

### 4. **Financial & Operations**
- **Portfolio rebalancing**: average long-run return; weight limits in basis points (integers)
- **Inventory management**: average cost over planning horizon with discrete demands $W$

### 5. **Control & Automata**
- **Weighted automata minimization**: compute reachability with accumulated numeric weights
- **Markov Decision Processes (MDPs)** with long-run average reward

## Common Mistakes / Pitfalls

### 1. **Confusing "pseudopolynomial" with "polynomial"**
- ❌ "The algorithm is polynomial in $n$" → true but misleading; it's **exponential in $W$**
- ✓ State: "Pseudopolynomial: $O(mnW)$" to be precise

### 2. **Ignoring the binary representation issue**
- ❌ Assuming $W$ is "small" without justification
- ✓ Check: is $W$ unary-encoded in the problem, or binary? If binary with many bits, the algorithm may be intractable
- Example: Factoring uses weights up to $2^{256}$; a pseudopolynomial algorithm would be hopeless

### 3. **Misapplying pseudopolynomial algorithms to strongly NP-hard problems**
- ❌ Attempting pseudopolynomial DP on a problem that is NP-hard even with unary weights
- ✓ Pseudopolynomial algorithms **do not exist** for strongly NP-hard problems (unless P=NP)
- Counter-example: **Partition problem** is strongly NP-hard; no pseudopolynomial algorithm known

### 4. **Forgetting logarithmic factors**
- Many modern pseudopolynomial bounds include $\log W$ or $\log(nW)$ factors
- $O(nmW)$ vs. $O(nmW \log W)$ can matter in practice for large