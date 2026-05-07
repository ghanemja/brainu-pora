# Dynamic Programming Algorithm

## Definition

Dynamic programming (DP) is an algorithmic paradigm for solving optimization problems by breaking them into overlapping subproblems, solving each subproblem exactly once, and storing their solutions to avoid redundant computation. The approach applies when a problem exhibits **optimal substructure** (an optimal solution can be constructed from optimal solutions to subproblems) and **overlapping subproblems** (the same subproblems appear multiple times in the recursion tree).

More formally, a DP algorithm:
1. **Decomposes** the original problem into a sequence of interdependent decisions
2. **Memoizes** (stores) solutions to subproblems indexed by their state
3. **Builds up** solutions bottom-up (tabulation) or top-down (memoization) via recurrence relations

## Key Equations

**Bellman Recurrence Relation** (generic form):
$$V(s) = \max_{a \in A(s)} \left\{ R(s,a) + \gamma \sum_{s'} P(s'|s,a) \cdot V(s') \right\}$$

where:
- $V(s)$ = value/cost of state $s$
- $a$ = decision/action taken in state $s$
- $R(s,a)$ = immediate reward/cost
- $P(s'|s,a)$ = transition probability to state $s'$
- $\gamma$ = discount factor

**Cost of Partition** (from calibration example):
$$\text{cost}_{D,f}(P) = \sum_{i=1}^{k} \sum_{x \in X_i} D_x(x) \cdot |f(x) - \mu_D(X_i)|$$

This represents the sum of weighted deviations for each partition element, which DP can minimize by exploring partition candidates.

**DP Table Recurrence** (contiguous partitions):
$$\text{OPT}[i] = \min_{j < i} \left\{ \text{OPT}[j] + \text{cost}(X_{j+1}^i) \right\}$$

where $\text{OPT}[i]$ is the minimum cost to partition elements $1$ through $i$, and $X_{j+1}^i$ is the interval from $j+1$ to $i$.

## Physical Intuition / Derivation

### Why Substructure Matters

Consider partitioning a domain $X = \{x_1, \ldots, x_n\}$ to minimize calibration distance. A naive approach would enumerate all $B_n$ (Bell number) partitions—exponential. Instead, observe:

> **Key Insight:** If the optimal partition of $X$ uses a boundary between $x_j$ and $x_{j+1}$, then the partition restricted to $\{x_1, \ldots, x_j\}$ must be optimal for that subset.

This is optimal substructure. It means we can build the solution incrementally:
- Solve for subsets $\{x_1\}, \{x_1, x_2\}, \ldots, \{x_1, \ldots, x_n\}$
- For each prefix, try all possible last partition elements
- Combine known-optimal solutions to subproblems

### The Contiguity Constraint

From the source material: the NP-hardness of partitioning under monotonicity constraints is resolved efficiently when **each subgroup must form a contiguous interval**. Why?

- Without contiguity: you must consider which non-adjacent elements group together → exponential choice space
- With contiguity: you only choose where to place partition boundaries → polynomial number of candidates

A DP table with $n$ rows (one per element) and $O(n)$ states per row gives **$O(n^2)$ or $O(n^3)$ complexity**, depending on cost computation.

### Memoization Pattern

```
function solve(state):
    if state in memo:
        return memo[state]
    
    if state is base case:
        return base_value
    
    result = min/max over choices of:
        immediate_cost + solve(next_state)
    
    memo[state] = result
    return result
```

This transforms exponential recursion $T(n) = 2^n$ into polynomial $T(n) = O(n^k)$ by caching.

## Applications in Engineering

### 1. **Optimization & Operations Research**
- **Knapsack problems**: packing items with weight/value constraints
- **Production scheduling**: minimizing makespan or inventory costs
- **Resource allocation**: distributing limited resources across time periods

### 2. **Machine Learning & Calibration**
- **Model calibration** (as in the source): partitioning predictor outputs to match empirical frequencies
- **Isotonic regression**: fitting monotonic functions with DP under monotonicity constraints
- **Decision tree learning**: selecting splits to minimize impurity

### 3. **Network & Control Systems**
- **Shortest path problems**: Dijkstra, Floyd-Warshall (DP variants)
- **Model predictive control**: multi-stage optimization with receding horizon
- **Optimal control**: value iteration in Markov decision processes

### 4. **Computational Biology**
- **Sequence alignment**: edit distance (Levenshtein), Smith-Waterman
- **Protein folding**: energy minimization over conformational states

### 5. **Signal Processing & Data Science**
- **Time series segmentation**: partitioning signals into homogeneous regions
- **Sparse approximation**: selecting basis elements to minimize reconstruction error

### 6. **Compilers & Formal Verification**
- **Parsing**: bottom-up DP parsing for context-free grammars
- **Register allocation**: assigning variables to registers with minimal spills

## Common Mistakes / Pitfalls

### 1. **Failing to Verify Optimal Substructure**
A problem may have overlapping subproblems but lack optimal substructure (e.g., finding the **longest simple path** in a graph). Applying DP leads to incorrect results.
- **Check:** Can you prove that an optimal solution uses only optimal subsolutions?

### 2. **State Space Too Large**
Choosing a state