# Dynamic Programming

## Definition

**Dynamic Programming (DP)** is an algorithmic design paradigm for solving optimization problems by breaking them into overlapping subproblems, solving each subproblem exactly once, and storing results to avoid redundant computation. The approach relies on two key properties:

1. **Optimal Substructure**: An optimal solution to the problem contains optimal solutions to subproblems
2. **Overlapping Subproblems**: The same subproblems are solved repeatedly during naive recursion

The method systematically builds solutions bottom-up (tabulation) or top-down (memoization), trading space for time to achieve polynomial or pseudo-polynomial runtime improvements over exponential brute-force approaches.

## Key Equations

For a general DP formulation, the recurrence relation expresses the optimal value as a function of smaller subproblems:

$$\text{OPT}(s) = \min_{a \in \text{Actions}(s)} \left[ \text{Cost}(s, a) + \text{OPT}(s') \right]$$

where $s$ is the current state, $a$ is a decision, $s'$ is the resulting state, and $\text{Cost}(s, a)$ is the immediate cost.

The number of states often determines complexity. For the interval ordering problem cited above:
- **State Space Size**: $O(2^n)$ or $O(n^k)$ depending on problem structure
- **Time per State**: Varies based on transition enumeration
- **Total Runtime**: $(\text{# states}) \times (\text{transitions per state}) \times (\text{work per transition})$

**Memoization recurrence** (top-down):
$$f[s] = \begin{cases} \text{cached value} & \text{if } s \text{ computed} \\ \min_a[\text{Cost}(s,a) + f[s']] & \text{otherwise} \end{cases}$$

## Physical Intuition / Derivation

### Why Dynamic Programming Works

Consider ordering intervals to minimize exposure cost. A greedy choice of the next interval might seem optimal locally, but may prevent better orderings globally. However, we observe that:

1. **The optimal ordering has structure**: Once we decide which intervals are "covered" by previous choices, the order within that set doesn't matter if elements are indistinguishable
2. **We can parametrize subproblems by coverage state**: Instead of enumerating all $n!$ permutations, we track which intervals are already placed
3. **Subproblems overlap**: Computing the best way to place intervals $\{1,3,5\}$ appears as a subproblem in multiple larger orderings

### Building Intuition

**Without DP**: Trying all $2^n$ subsets and all orderings within each → $O(n! \cdot 2^n)$ time

**With DP**: Recognize that the *specific order within an indistinguishable group doesn't matter*. If elements have only $k$ types (e.g., two types in the calibration example: those with property $D_x(x_1) = D_x(x_2)$), we reduce the state space from $2^n$ to polynomial $O(n^k)$

The key insight from the source: type-sparse distributions allow restricting attention to **contiguous partitions**, reducing $O(2^n)$ states to $O(n^k)$ states, enabling polynomial-time algorithms.

$$\text{opt}(m_0, m_1) = \min_{\substack{1 \leq j_0 \leq m_0 \\ 1 \leq j_1 \leq m_1}} \left[ \text{Cost}_{\text{partition}}(j_0, j_1) + \text{opt}(j_0-1, j_1-1) \right]$$

## Applications in Engineering

### Computer Science & Algorithms
- **Shortest path problems** (Dijkstra as DP, Bellman-Ford equation)
- **Sequence alignment** (edit distance, Smith-Waterman in bioinformatics)
- **Knapsack problems** (resource allocation)
- **Interval scheduling** (weighted interval partitioning)

### Bioinformatics
- **Protein folding** (minimum energy configuration via DP)
- **DNA sequence matching** (as in the cited paper's motivation)
- **Multiple sequence alignment** (progressive alignment via DP recurrences)

### Operations Research
- **Production planning** (inventory management across time periods)
- **Vehicle routing** (traveling salesman variants)
- **Portfolio optimization** (asset allocation with constraints)

### Control & Systems
- **Model Predictive Control (MPC)**: DP formulates finite-horizon optimal control as a sequence of subproblems
- **Reinforcement Learning**: Bellman equations express value functions recursively

### Machine Learning
- **Viterbi algorithm** (Hidden Markov Models, decoding)
- **CYK parsing** (context-free grammar recognition)
- **Calibration problems** (as cited: finding type-sparse distributions via DP with $O(n^{2k})$ runtime)

## Common Mistakes / Pitfalls

1. **Forgetting base cases**: A DP without proper termination conditions produces infinite recursion or undefined values
   - *Fix*: Always explicitly define $\text{OPT}(\emptyset)$ or $\text{OPT}(0)$

2. **Overcounting or undercounting subproblems**: Mistakes in defining the state space lead to missing or duplicate computations
   - *Example*: In interval problems, confusing "which intervals to include" with "order of intervals" changes the state definition
   - *Fix*: Clearly specify what each state represents; verify it's sufficient to compute the answer

3. **Assuming optimal substructure without proof**: Not every optimization problem has this property (e.g., longest simple path in a graph doesn't)
   - *Fix*: Verify that $\text{OPT}(P) \subseteq \text{OPT}(\text{subproblems of } P)$

4. **Poor state representation**: Choosing a state space that's exponential when a polynomial one exists (like $2^n$ instead of $n^k$ for structured problems)
   -