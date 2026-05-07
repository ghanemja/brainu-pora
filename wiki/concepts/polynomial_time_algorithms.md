# Polynomial Time Algorithms

## Definition

A **polynomial time algorithm** is a computational procedure that solves a decision or optimization problem in a number of steps bounded by a polynomial function of the input size. Formally, an algorithm runs in polynomial time if there exist constants $c$ and $k$ such that for any input of size $n$, the algorithm terminates in at most $cn^k$ elementary operations.

An algorithm is said to be in the complexity class **P** (polynomial time) if it can solve a decision problem correctly in polynomial time. This is distinguished from **NP** problems, which can be *verified* in polynomial time but may not be solvable in polynomial time.

### Formal Notation

For an algorithm $A$ with input size $n$:
$$T(n) = O(n^k) \text{ for some constant } k \geq 1$$

where $T(n)$ denotes the worst-case number of steps (time complexity).

## Key Equations

**Polynomial Complexity Classes:**
$$
\begin{align}
\text{Linear:} \quad &T(n) = O(n) \\
\text{Quadratic:} \quad &T(n) = O(n^2) \\
\text{Cubic:} \quad &T(n) = O(n^3) \\
\text{Polylogarithmic:} \quad &T(n) = O(n \log n)
\end{align}
$$

**Verification vs. Solving:**
$$
P \subseteq NP$$

where $P$ is the class of problems solvable in polynomial time, and $NP$ is the class of problems verifiable in polynomial time.

## Physical Intuition / Derivation

The concept of polynomial time captures a fundamental engineering principle: **feasibility in practice**. 

### Why Polynomial Time Matters

1. **Scalability**: An algorithm with $T(n) = n^2$ can process $n = 10^6$ items in $10^{12}$ operations, which modern computers achieve in seconds to minutes. By contrast, exponential algorithms like $T(n) = 2^n$ become intractable for $n > 40$.

2. **Resource-Bounded Rationality**: In fair division problems (such as the school redistricting example), we need algorithms that scale with the number of students $n$ and groups $g$. The paper demonstrates that a 1-relaxed envy-free allocation exists and **can be found in polynomial time**—meaning even for large school districts with thousands of students, a fair solution is computationally achievable.

3. **Hardness Hierarchy**: The polynomial hierarchy exists because:
   - Some problems are easy (polynomial, like sorting)
   - Some are hard to solve but easy to verify (NP-complete, like subset sum)
   - Some may be fundamentally harder (NP-hard)

### From Fair Division to Algorithm Design

In the school redistricting context, the authors show:
- **Proportional allocations**: solvable in polynomial time when $g$ is constant (result by Procaccia et al.)
- **Envy-free allocations for $g \geq 3$**: may require super-polynomial resources
- **1-relaxed envy-freeness for $g = 2$**: exists *and* findable in polynomial time

This progression illustrates why problem **relaxation** is a key engineering technique—making a problem slightly easier (allowing capacity violations of ≤1 per school) transforms it from potentially intractable to polynomial-time solvable.

## Applications in Engineering

### 1. **Fair Resource Allocation**
- School redistricting, voting district boundaries, hospital bed assignments
- Requires polynomial-time verification of fairness guarantees

### 2. **Operations Research & Scheduling**
- Job scheduling, facility location, load balancing
- Must handle thousands of items/constraints; exponential algorithms are unusable

### 3. **Network Design**
- Routing algorithms (shortest path: Dijkstra $O(n^2)$)
- Maximum flow algorithms (polynomial, not exponential)

### 4. **Machine Learning & AI**
- Training algorithms (gradient descent, though not always polynomial in practice)
- Constructive proofs must yield efficient implementations

### 5. **Cryptography**
- Public-key systems assume certain problems are hard (not in P)
- Security relies on the $P \neq NP$ conjecture

### 6. **Compiler Design**
- Register allocation, code optimization require polynomial-time heuristics
- Full optimization is often NP-hard; approximations use polynomial algorithms

## Common Mistakes / Pitfalls

### 1. **Confusing "Polynomial" with "Fast"**
A $O(n^{10})$ algorithm is polynomial but often too slow for practical use. Conversely, $O(2^{0.01n})$ is exponential but faster for small $n$.

### 2. **Ignoring Hidden Constants**
An $O(n^2)$ algorithm with constant $10^6$ is worse than an $O(n^3)$ algorithm with constant $1$ for typical input sizes. Big-O notation hides coefficients.

### 3. **Assuming "Solvable in Polynomial Time" = "Practical Solution"**
Even polynomial algorithms can be impractical. A $O(n^4)$ algorithm requires $10^{24}$ operations for $n = 10^6$—still infeasible without approximation.

### 4. **Misapplying NP-Completeness**
- Proving a problem is NP-complete does NOT mean it's hard in practice for small instances
- Approximation algorithms and heuristics often solve NP-hard problems efficiently
- The school redistricting paper shows: relax envy-freeness → polynomial time becomes possible

### 5. **Forgetting Input Representation**
Polynomial time depends on the *encoding* of input. For example, if a number is represented in binary vs. unary, the running time analysis changes dramatically (leading to pseudo-polynomial vs. strongly polynomial distinctions).

### 6. **Overlooking Space Complexity**
An algorithm may run in polynomial time but require exponential space—equally prohibitive in engineering contexts.

## See Also

- [[Computational Complexity Theory]] — formal framework for analyzing algorithm time/space bounds
- [[NP-Completeness]] — characterizes problems likely not solvable in