# Polynomial-Time Algorithms

## Definition

A **polynomial-time algorithm** is an algorithm whose worst-case runtime is bounded by a polynomial function of the input size $n$. Formally, an algorithm runs in polynomial time if its time complexity $T(n) = O(n^k)$ for some constant $k \geq 1$.

More precisely: an algorithm is polynomial-time if there exist constants $c > 0$ and $k \geq 1$ such that for all inputs of size $n$, the algorithm terminates in at most $c \cdot n^k$ elementary computational steps.

**Computational significance**: Polynomial-time algorithms are considered *tractable* or *efficiently solvable* in computational complexity theory. This contrasts with exponential-time algorithms ($O(2^n)$, $O(n!)$), which become infeasible even for moderate input sizes.

## Key Equations

### Complexity Classes

**Polynomial time is formally defined as:**
$$T(n) = O(n^k) \text{ for some constant } k \geq 1$$

**P (Polynomial)** is the complexity class:
$$\mathcal{P} = \{L : L \text{ is decidable in polynomial time by a deterministic Turing machine}\}$$

**Pseudopolynomial time** (weaker notion): 
$$T(n, v_{\max}) = O(p(n, v_{\max}))$$
where $v_{\max}$ is the magnitude of the largest input value. This is polynomial in both $n$ and the numeric value of inputs, useful for problems with bounded integer parameters.

### Binary Search Efficiency Example
Given bounds $u$ and $\bar{u}$ on an optimal solution value, binary search iterations scale as:
$$\text{Iterations} = O(\log(\bar{u} - u)) \text{ per unit precision}$$

## Physical Intuition / Derivation

### Why Polynomial Time Matters

Consider solving a scheduling problem on a single machine:
- A brute-force algorithm checking all $n!$ job orderings is exponential: even $n=10$ requires $\sim 3.6$ million evaluations
- A polynomial-time algorithm with $O(n^2)$ complexity processes $n=1000$ in roughly 1 million steps

**Tractability threshold**: Practical engineering systems require algorithms that scale smoothly with problem size. Polynomial time is the theoretical boundary separating "solvable in reasonable time" from "infeasible even for modest inputs."

### Why Complexity Varies Across Problem Variants

From the source material, notice that **the same problem structure yields different complexity depending on constraints**:

- **1|$u_j$|$f$**: Polynomial when $f = u_{\min}$ (minimize worst utility), but **strongly NP-hard** when $f = \sum u_j$ (maximize total utility)
  
- **1|$r_j, u_j = b_j - a_j C_j$|$f$**: Adding release dates $r_j$ makes the problem strongly NP-hard *even for* $f = u_{\min}$

**Insight**: A single additional constraint (release dates) can shift a problem from tractable to intractable. This reflects an fundamental phase transition in problem structure.

### Solution Approaches for Polynomial Cases

The source material describes a **general solution approach using binary search**:
1. Establish lower bound $\underline{u}$ and upper bound $\bar{u}$ on optimal utility value
2. Binary search over the feasible range $[\underline{u}, \bar{u}]$
3. For each midpoint candidate, verify feasibility in polynomial time
4. Total complexity: $O(\log(\bar{u}/\underline{u}) \cdot T_{\text{feasibility}})$

This demonstrates that polynomial-time algorithms often involve:
- **Greedy approaches** (problem 1|$p_j = 1, r_j, u_j$|$f$: polynomial assignment)
- **Dynamic programming** (implicit in feasibility checks)
- **Search with oracle** (binary search + polynomial verification)

## Applications in Engineering

### Scheduling and Resource Allocation
The source material focuses on **single-machine scheduling problems** ($1|\cdots|f$):
- **Job sequencing with deadlines**: Polynomial algorithms exist for minimizing minimum utility $u_{\min}$ under linear utility functions
- **Release dates and processing times**: Critical in manufacturing and cloud computing; polynomial solutions exist for special cases (identical processing times $p_j = p$)
- **Multi-objective optimization**: Balancing total utility $\sum u_j$ vs. fairness metric $u_{\min}$ requires different algorithmic approaches

### Network Design and Routing
- Shortest-path algorithms (Dijkstra, Bellman-Ford) are polynomial-time and foundational to telecom and logistics
- Minimum spanning tree (Kruskal, Prim) run in $O(n^2)$ to $O(n \log n)$

### Compiler Optimization
Register allocation, instruction scheduling, and dead-code elimination employ polynomial-time heuristics and exact algorithms

### Approximation of Hard Problems
When NP-hard problems arise (e.g., 1|$\sum U_j \leq k, u_j = b_j - a_j C_j$|$f$ is strongly NP-hard per Theorem 13), engineers often:
- Use polynomial-time approximation schemes (PTAS)
- Apply greedy polynomial heuristics with known approximation ratios
- Leverage integer linear programming with polynomial relaxations (LP bounds)

## Common Mistakes / Pitfalls

### 1. **Conflating "Polynomial" with "Fast in Practice"**
An algorithm with $T(n) = 100n^{10}$ is polynomial but utterly impractical. Polynomial time is a theoretical threshold, not a practical speed guarantee. Always check leading constants and exponents.

### 2. **Assuming All Variations of a Problem Have the Same Complexity**
**Critical lesson from the source**: Adding constraints like release dates $r_j$ or changing the objective function can shift complexity classes:
- 1|$u_j = b_j - a_j C_j$|$\sum u_j$ is **polynomial** (Smith, 1956)
- 1|$r_j, u