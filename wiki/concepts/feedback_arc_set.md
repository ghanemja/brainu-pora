# Feedback Arc Set

## Definition

A **feedback arc set (FAS)** of a directed graph $G = (V, E)$ is a subset of edges $F \subseteq E$ whose removal makes the graph acyclic (a DAG). Equivalently, $F$ is a set of edges whose reversal renders the graph acyclic.

The **minimum feedback arc set problem** seeks to find the smallest such subset:
$$\text{FAS}_{\min}(G) = \arg\min_{F \subseteq E} |F| \text{ such that } G \setminus F \text{ is acyclic}$$

**Related definition**: A feedback vertex set removes vertices instead of edges to break all cycles, but FAS operates on edges.

## Key Equations

For a directed graph $G = (V, E)$:

**Characterization**: A directed graph is acyclic if and only if it admits a topological ordering $\sigma: V \to \{1, 2, \ldots, |V|\}$ such that for all edges $(u, v) \in E$: $\sigma(u) < \sigma(v)$.

Equivalently, FAS can be minimized via:
$$\text{FAS}_{\min} = \min_{\sigma} \left| \{ (u,v) \in E : \sigma(u) > \sigma(v) \} \right|$$

This formulation shows FAS as counting **backward edges** with respect to a vertex ordering.

## Physical Intuition / Derivation

### Why FAS Matters

Cycles in directed graphs represent circular dependencies:
- In task scheduling: impossible circular prerequisites
- In control systems: unresolvable feedback loops
- In constraint satisfaction: inherent contradictions

### Building Intuition

Consider a directed graph with a cycle $v_1 \to v_2 \to \cdots \to v_k \to v_1$. No topological ordering exists because:
- If $v_i$ must come before $v_{i+1}$ (by edge direction)
- And $v_k$ must come before $v_1$ (by the cycle)
- We cannot linearly order vertices respecting all constraints

An FAS *breaks* the cycle by removing at least one edge. The minimum FAS uses fewest removals.

### Connection to Permutation Match Puzzles

In the source material, the constraint graph is constructed where:
- Vertices represent ordering constraints (ascending/descending labels)
- Edges encode conflicts between constraints
- A cycle indicates **unsolvable constraints**

The authors prove: *a permutation match puzzle is solvable if and only if its constraint graph is acyclic*, making FAS computation essential for determining minimum repairs (label flips).

## Applications in Engineering

### 1. **Scheduling and Project Management**
- Detect circular task dependencies
- Minimum rescheduling: which precedence constraints to relax?
- Example: breaking circular precedence in construction projects

### 2. **VLSI Circuit Design**
- Identify problematic feedback loops in circuit topology
- Determine minimum feedback channels to buffer or pipeline
- Static timing analysis with cycles

### 3. **Control Systems**
- Detect unresolvable feedback loops in block diagrams
- Identify which feedback connections must be broken for stabilization
- System causality analysis

### 4. **Compiler Optimization**
- Detect cyclic dependencies in instruction scheduling
- Find minimum edges to break for dependency analysis
- Loop unrolling and software pipelining

### 5. **Machine Learning & Constraint Satisfaction**
- Boolean constraint solving with circular implications
- Identifying minimal constraint relaxations
- Permutation matrix completion problems (as in source material)

### 6. **Network Design**
- Routing protocol deadlock detection
- Finding minimum virtual channels to prevent circular wait
- Network flow with cyclic dependencies

## Computational Complexity

The minimum feedback arc set problem is **NP-hard** in general directed graphs [Karp, 1972]. 

Key hardness results:
- **NP-complete** for general graphs
- **APX-hard**: no constant-factor approximation exists (unless P=NP)
- **FPT** with respect to FAS size: solvable in $O(2^k \cdot \text{poly}(n))$ for FAS size $k$

The source material uses FAS reduction to prove NP-completeness of the generalized permutation match puzzle problem.

## Special Cases & Algorithms

### Approximation
- **Greedy tournament approach**: $\frac{1}{4}$-approximation via random vertex ordering
- **Deterministic greedy**: iteratively remove vertex with maximum in-degree minus out-degree

### Fixed-Parameter Tractable
- Bounded search tree techniques when FAS size is small
- Iterative compression: if $|F|$ is bounded, feasible for moderate sizes

### Polynomial Cases
- Tournaments (complete directed graphs): can be solved in polynomial time via topological ordering methods

## Common Mistakes / Pitfalls

1. **Confusing FAS with FVS**: Feedback Vertex Set removes vertices (harder problem in general); FAS removes edges. Different complexity profiles.

2. **Assuming greedy optimality**: Greedy edge removal can produce suboptimal FAS. The problem requires global optimization.

3. **Cycles vs. feedback**: Not all edges in cycles need removal—only enough edges to break all cycles. Minimum FAS is subtle.

4. **Confusing acyclicity with solvability**: A DAG is necessary but not sufficient for all applications (e.g., reachability, strong solutions). Check problem-specific requirements.

5. **Overlooking approximation gaps**: For large instances, $\frac{1}{4}$-approximations may far exceed actual minimums for special graph classes.

6. **Topology ordering confusion**: Existence of a topological ordering is equivalent to acyclicity, but FAS seeks an optimal *cut*, not just any DAG.

## See Also

- [[Topological Sort]] — ordering algorithm for DAGs; used to compute backward edges
- [[Strongly Connected Components]] — identifying cycles via Tarjan/Kosaraju algorithms
- [[Directed Acyclic Graph]] — target property after FAS removal
- [[NP-Completeness]] — theoretical hardness framework; FAS is canonical NP-complete reduction
- [[Constraint Satisfaction Problems]] — application domain; FAS identifies unsolvable constraints