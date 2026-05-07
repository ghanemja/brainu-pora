# Knapsack Problem

## Definition

The **knapsack problem** is a combinatorial optimization problem in which one must select a subset $S$ from a finite set of items, each with an associated weight (or cost) and value, to maximize total value subject to a total weight constraint. Formally:

$$\max_{S \subseteq I} \sum_{i \in S} v_i \quad \text{subject to} \quad \sum_{i \in S} w_i \leq W$$

where:
- $I = \{1, 2, \ldots, n\}$ is the set of items
- $v_i$ is the value of item $i$
- $w_i$ is the weight of item $i$
- $W$ is the knapsack capacity

**Key variants:**
- **0/1 Knapsack**: each item selected at most once (binary decision)
- **Unbounded Knapsack**: items can be selected multiple times
- **Fractional Knapsack**: items can be selected partially
- **Multidimensional (Multi-constraint) Knapsack**: multiple weight constraints simultaneously

## Key Equations

**Dynamic Programming Formulation (0/1 Knapsack):**

Let $DP[i][w]$ denote the maximum value using items $1, \ldots, i$ with capacity $w$:

$$DP[i][w] = \max\begin{cases} DP[i-1][w] & \text{(skip item } i\text{)} \\ DP[i-1][w-w_i] + v_i & \text{(include item } i\text{)} \end{cases}$$

with base case $DP[0][w] = 0$ for all $w$.

**Optimality Condition (Fractional Case):**

For the fractional knapsack with items ordered by value-to-weight ratio $\rho_i = v_i/w_i$:

$$\text{Optimal solution includes items in decreasing order of } \rho_i$$

**Lagrange Relaxation (Interdiction Context):**

When introducing Lagrange multiplier $\lambda$ for capacity constraint, reweighted costs become:

$$w_\lambda(e) = \min\{w(e), \lambda c(e)\}$$

This reformulation allows decomposition of complex constrained problems into simpler subproblems.

## Physical Intuition / Derivation

### Why the Knapsack Problem Matters

Imagine a hiker with a backpack of fixed capacity who must choose which items to bring. Each item has weight and utility; the goal is to maximize utility without exceeding capacity. This simple scenario encapsulates a broad class of resource allocation problems.

### Complexity and Tractability

- The 0/1 knapsack is **NP-hard** in the strong sense (no pseudo-polynomial algorithm exists for all instances)
- However, it is **NP-hard in the weak sense** when pseudo-polynomial: dynamic programming solves it in $O(nW)$ time
- This distinction is crucial: practical instances with moderate $W$ are often solvable, but scaling $W$ exponentially makes them intractable

### Why Dynamic Programming Works

The DP approach exploits **optimal substructure**: if $S^*$ is an optimal selection for capacity $W$, then $S^* \setminus \{i\}$ is optimal for capacity $W - w_i$. This allows building solutions incrementally:

1. Fill a table where entry $(i, w)$ records the best value achievable using items $1, \ldots, i$ with capacity exactly $w$
2. Each entry depends only on entries from the previous row, reducing space complexity to $O(W)$
3. The recurrence expresses the choice: include item $i$ (if it fits) or exclude it

### Connection to Lagrangian Duality

In the interdiction context cited, the knapsack arises as a subproblem: after eliminating an interdiction budget constraint via Lagrange duality, one obtains a reweighted knapsack-like problem. At optimal $\lambda^*$, solving this reweighted problem and enumerating its approximate solutions yields witness information for the original interdicted problem.

## Applications in Engineering

### 1. **Resource Allocation and Scheduling**
- Assigning tasks or jobs to processors with memory/power constraints
- Portfolio optimization: selecting investments to maximize expected return within budget
- Cutting stock problems: minimizing waste when cutting material to required lengths

### 2. **Network and Wireless Systems**
- **Connectivity Interdiction**: selecting network edges to delete (given limited budget) to minimally degrade connectivity. The reweighted knapsack subproblem is central to FPTAS approximation algorithms
- Spectrum allocation: assigning frequency bands to base stations within power budgets
- Sensor placement: selecting sensors to monitor with energy constraints

### 3. **Supply Chain and Manufacturing**
- Vehicle loading: maximizing cargo value while respecting weight/volume limits
- Inventory management: selecting items to stock given shelf space or capital constraints
- Machine scheduling with precedence constraints and limited resources

### 4. **Operations Research**
- Capital budgeting: selecting projects to fund within a fixed budget to maximize return
- Warehouse management: packing orders to minimize shipping cost or container count

### 5. **Algorithmic Development**
- Benchmarking approximation and exact algorithms
- Testing decision diagram methods (as in implicit DD solver implementations)
- Prototyping for larger combinatorial optimization problems

## Common Mistakes / Pitfalls

### 1. **Confusing Polynomial and Pseudo-polynomial**
Many practitioners incorrectly believe $O(nW)$ DP is "polynomial" in general. It is polynomial *only in the size of the weight*; if $W$ is encoded in binary, the input size is $\log W$, making the algorithm exponential. **Never forget**: complexity must be stated relative to input encoding.

### 2. **Greedy Fails for 0/1 Knapsack**
The greedy approach—selecting items in order of value-to-weight ratio—is *optimal only for the fractional knapsack*. For 0/1, it can miss the optimal by an arbitrary factor. Example:
   - Capacity $W = 10$, items: $(w=6, v=30), (w=5, v=25