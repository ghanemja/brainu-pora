# acyclic tournament

## Definition

An **acyclic tournament** is a directed graph on a finite vertex set where:

1. **Tournament property**: For every pair of distinct vertices $u, v$, there is exactly one directed edge between them (either $u \to v$ or $v \to u$, but not both and not neither).
2. **Acyclicity**: The graph contains no directed cycles.

Equivalently, an acyclic tournament is a **transitive tournament**—a tournament whose edge relation defines a total order on the vertices. This can be verified by the property that if $u \to v$ and $v \to w$, then $u \to w$.

## Key Equations

For an acyclic tournament $T$ on $n$ vertices:

**Number of edges:**
$$|E(T)| = \binom{n}{2} = \frac{n(n-1)}{2}$$

**Transitive property (characterization):**
$$u \to v \land v \to w \implies u \to w$$

**Feedback Vertex Set bound:** For an arbitrary directed graph $G$ with feedback vertex set of size $k$, removing those $k$ vertices yields an acyclic subgraph. Conversely, any acyclic tournament is a feedback vertex set solution of size 0 for itself.

## Physical Intuition / Derivation

### From Permutations to Tournament Structure

An acyclic tournament naturally arises from **total orders**: given a permutation $\pi \in S_n$, we can define a tournament by placing an edge $i \to j$ whenever $\pi(i) < \pi(j)$ in the ordering. This tournament is acyclic because the ordering is transitive.

### Why Acyclicity Matters

In constraint-satisfaction problems (such as permutation matching puzzles), a cycle in a constraint graph indicates a logical inconsistency:
- Vertices represent choice variables
- Edges represent constraints between pairs
- A cycle means constraints form a circular dependency with no valid assignment

Thus, **acyclic tournaments correspond to consistent, satisfiable constraint systems** where a linear ordering of variables exists.

### Structural Consequence

Every acyclic tournament on $n$ vertices admits a **topological ordering**: a linear ordering $v_1, v_2, \ldots, v_n$ such that $v_i \to v_j$ whenever $i < j$. This is the unique ordering (up to symmetry) consistent with the acyclic tournament structure.

## Applications in Engineering

### 1. **Scheduling and Project Management**
- Tasks as vertices; precedence constraints as edges
- Acyclic tournaments model total-order task dependencies
- The topological ordering gives a valid execution sequence

### 2. **Database Transaction Ordering**
- Transactions as vertices; data dependencies as edges
- Acyclic tournaments ensure serializable execution schedules
- Cycles would indicate deadlock-prone dependency patterns

### 3. **Compiler and Static Analysis**
- Symbol resolution and dependency graphs in module systems
- Acyclic imports guarantee no circular dependencies
- Function call graphs: acyclic tournaments identify call orderings

### 4. **Constraint Satisfaction Problems (CSPs)**
- Permutation matching puzzles (the original motivation)
- Grid-structured constraint graphs with acyclic row/column tournaments
- Solvability directly tied to global acyclicity

### 5. **Sorting Networks and Comparator Logic**
- Each comparator induces a constraint; chains of comparators form tournaments
- Acyclicity guarantees the network correctly sorts all inputs

## Common Mistakes / Pitfalls

### 1. **Confusing "Tournament" with "General Directed Graph"**
- A tournament is *complete* (every pair of vertices has exactly one directed edge)
- Not all acyclic directed graphs are tournaments
- **Pitfall:** Assuming sparsity; acyclic tournaments have $\Theta(n^2)$ edges

### 2. **Assuming Topological Ordering is Unique**
- While every acyclic tournament admits a topological ordering, the tournament structure itself is unique
- However, different labelings of vertices yield different edge directions
- **Pitfall:** Not recognizing that transitive tournaments represent the "most constrained" acyclic structure

### 3. **Misidentifying Acyclicity**
- Checking acyclicity naively requires cycle-detection algorithms (DFS-based)
- In a tournament, acyclicity is *stronger* than general acyclic graphs
- **Pitfall:** Overlooking that transitivity provides powerful structural guarantees

### 4. **Grid Acyclification Complexity Confusion**
- Grid Acyclification (restricted to grid graphs with acyclic row/column tournaments) is NP-complete
- This does NOT mean recognizing acyclic tournaments is hard (it's trivial—check transitivity)
- **Pitfall:** Conflating the hardness of the global optimization problem with local verification

### 5. **Ignoring the "Each Pair Must Have an Edge" Requirement**
- Missing edges break the tournament property
- **Pitfall:** Treating partial orders as tournaments without verifying completeness

## See Also

- [[topological sorting]] — algorithmic method to order acyclic DAGs
- [[Feedback Vertex Set problem]] — NP-complete problem of removing minimum vertices to break all cycles
- [[transitive reduction]] — computing minimal equivalent acyclic representation
- [[constraint satisfaction problem]] — CSPs where acyclic tournaments model solvability
- [[permutation]] — generating acyclic tournaments from total orders

## Sources

- **Grid Acyclification Problem and NP-Completeness Reduction** (Gajjar & Misra): Analysis of acyclic tournament structure in grid graphs, construction of NP-complete variant via reduction from Feedback Vertex Set
- **Permutation Matching Puzzles**: Connection between constraint graph acyclicity and satisfiability of permutation-based puzzles
- **Tournament Theory** (classical): Foundational graph-theoretic characterization of tournaments and transitive tournaments