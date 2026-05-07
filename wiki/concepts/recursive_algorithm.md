# Recursive Algorithm

## Definition

A **recursive algorithm** is a computational procedure that solves a problem by having a function call itself on smaller or simpler instances of the same problem, until reaching one or more **base cases** that can be solved directly without further recursion.

Formally, a recursive algorithm consists of:

1. **Base case(s)**: One or more conditions where the function returns a value without making a recursive call
2. **Recursive case(s)**: One or more conditions where the function calls itself with modified arguments that move toward the base case
3. **Progress guarantee**: Each recursive call must make measurable progress toward the base case to ensure termination

In the context of game theory and combinatorial optimization (e.g., mean-payoff games), a recursive algorithm structures the solution by decomposing complex game states into simpler subproblems, solving those recursively, and combining results symmetrically across all problem components.

## Key Equations

For a recursively-defined function $f$:

$$f(n) = \begin{cases}
\text{base\_value} & \text{if } n \in \text{BASE\_CASES} \\
g(f(h_1(n)), f(h_2(n)), \ldots) & \text{otherwise}
\end{cases}$$

where:
- $h_i(n)$ represents transformations of the input that reduce problem size or complexity
- $g$ is the combination function merging recursive results

**Recurrence relation for complexity** (example):
$$T(n) = aT(n/b) + f(n)$$

where $a$ is the branching factor and $b$ is the problem reduction factor.

## Physical Intuition / Derivation

### Why Recursion Works

Recursion leverages the principle of **structural decomposition**: many complex systems exhibit self-similar structure at different scales. A recursive algorithm exploits this by:

1. **Identifying the recursive structure**: The problem can be decomposed into subproblems of the same type
2. **Defining the base case**: The smallest possible instance can be solved directly
3. **Trusting the recursion**: Once you verify the base case and recursive case logic are correct, you can trust the algorithm works for all valid inputs

### Example: Mean-Payoff Game Context

In mean-payoff games, a symmetric recursive algorithm decomposes the game graph by:

- **Recursive decomposition**: Partition vertices into subsets based on game value
- **Symmetric treatment**: Apply identical logic to both players (Min/Max)
- **Convergence**: Iterate until game values stabilize, with each recursion reducing the uncertainty about vertex values
- **Base case**: A single-vertex game has trivial solution

This is more elegant than explicit energy tracking because the recursive structure naturally encodes the information flow.

## Applications in Engineering

### 1. **Software Engineering & Algorithm Design**
- **Tree/graph traversal**: Depth-first search (DFS), tree searches, parsing
- **Divide-and-conquer algorithms**: Merge sort, quicksort, binary search
- **Dynamic programming**: Fibonacci sequences, shortest paths (Bellman equations)

### 2. **Game Theory & AI**
- **Minimax search**: Game trees in chess/Go engines (Alpha-Beta pruning)
- **Mean-payoff game solving**: Distributed control and synthesis
- **Reactive system verification**: Model checking via recursive state exploration

### 3. **Compiler Design**
- **Recursive descent parsing**: Building abstract syntax trees (ASTs)
- **Expression evaluation**: Parsing arithmetic/logical expressions with operator precedence

### 4. **Control Systems**
- **Hierarchical control**: Decomposing control objectives into recursive subtasks
- **State machine design**: Nested state machines with recursive call structures

### 5. **Network & Distributed Systems**
- **Distributed consensus algorithms**: Recursive message passing
- **Fault tolerance**: Recursive recovery protocols with backoff

## Common Mistakes / Pitfalls

### 1. **Missing or Incorrect Base Case**
```
❌ Bad: No base case → infinite recursion → stack overflow
✓ Good: Always verify base case is reachable and returns correct value
```

### 2. **Infinite Recursion Without Progress**
```
❌ Bad: f(n) calls f(n) (no reduction)
✓ Good: Ensure each call has strictly smaller argument (by well-founded order)
```

### 3. **Exponential Blowup from Redundant Computation**
- **Problem**: Naive recursive Fibonacci computes $f(5)$ multiple times
- **Solution**: Use memoization (cache results) or convert to iterative DP

### 4. **Stack Overflow on Deep Recursion**
- **Problem**: Large recursion depth exhausts call stack
- **Solution**: 
  - Use tail-call optimization (TCO)
  - Convert to iterative approach
  - Increase stack size (platform-dependent)

### 5. **Asymmetric Treatment in Symmetric Algorithms**
- **In context of game theory**: Treating Min and Max differently breaks optimality proofs
- **Solution**: Verify recursive structure applies identically to all players/components

### 6. **Misunderstanding Termination**
- Many recursive algorithms on infinite structures (e.g., mean-payoff games on infinite plays) require **abstract termination** via progress metrics, not literal program termination
- Verify convergence formally; don't assume it

## See Also

- [[Divide and Conquer]] — Algorithmic paradigm using recursive decomposition
- [[Dynamic Programming]] — Recursive optimization via memoization
- [[Game Theory]] — Mathematical frameworks for multi-agent decision problems
- [[Depth-First Search]] — Classic recursive graph traversal
- [[Fixed-Point Iteration]] — Iterative recursive methods for solving equations

## Sources

- Ohlmann, P. (2024). "A symmetric recursive algorithm for mean-payoff games." *CNRS, Laboratoire d'Informatique et des Systèmes (LIS)*
- Ehrenfeucht & Mycielski (1979). "Positional strategies for mean-payoff games"
- Zwick & Paterson (1996). "The complexity of mean-payoff games" — established NP ∩ coNP membership and pseudopolynomial algorithms
- Brim et al. (2011). "Value iteration algorithm" for mean-payoff games — $O(nm