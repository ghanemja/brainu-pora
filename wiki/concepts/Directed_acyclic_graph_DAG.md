# Directed Acyclic Graph (DAG)

## Definition

A **Directed Acyclic Graph (DAG)** is a finite directed graph $G = (V, E)$ containing no directed cycles. Formally:
- $V$ is a set of vertices (nodes)
- $E \subseteq V \times V$ is a set of directed edges
- For all vertices $v \in V$, there exists no path $v \to v_1 \to v_2 \to \cdots \to v$ (no cycle)

**Partial order interpretation**: A DAG encodes a partial order relation on its vertex set. An edge $u \to v$ means "$u$ precedes $v$" in the ordering, but not all pairs of vertices need be comparable.

**Total extensions**: A **topological sort** of a DAG is a total ordering of $V$ consistent with the partial order—i.e., whenever $u \to v$ exists, $u$ appears before $v$ in the ordering. The number of such extensions is denoted $e(G)$.

## Key Equations

**Topological ordering property**:
For a DAG $G = (V, E)$ with $|V| = n$ vertices and $|E| = m$ edges, any valid topological sort $\sigma$ satisfies:
$$\forall (u,v) \in E: \sigma(u) < \sigma(v)$$

**Information-theoretic lower bound** (for sorting under partial information):
Any comparison-based algorithm to find a total extension must make at least
$$\log_2 e(G)$$
comparisons in the worst case, since there are $e(G)$ possible valid orderings.

**Logarithmic extension bound**:
The number of linear extensions is bounded by:
$$e(G) \leq n! \quad \text{(trivial)}$$
More usefully: $e(G)$ can range from 1 (fully ordered) to $n!$ (independent vertices).

## Physical Intuition / Derivation

### Why DAGs Matter

Consider a project with tasks and dependencies:
- **Vertices** = individual tasks
- **Edges** = precedence constraints (task $u$ must complete before task $v$)
- **Acyclicity** = projects must be feasible (no circular dependencies)

A topological sort is a valid **schedule**: an ordering of tasks respecting all dependencies.

### Partial Information and Sorting

In the "sorting under partial information" problem:
1. You are given a **partial order** (a DAG representing known comparisons)
2. You must determine a **total order** (which total extension is the "true" sorted order)
3. You can make additional **comparisons** to disambiguate between consistent total extensions

**Why $\log e(G)$ matters**: If $e(G)$ distinct total extensions are compatible with the DAG, information theory guarantees you need $\geq \log_2 e(G)$ comparisons to identify which one (in bits). The DAG "narrows down" the search space from $n!$ possibilities to $e(G)$ possibilities.

### Preprocessing Tradeoff

The source material reveals a fundamental **preprocessing-query tradeoff**:
- **Naive approach**: Do no preprocessing ($O(1)$ prep), then $O(n \log n)$ sorting time
- **Intermediate approaches**: $O(n^{2.5})$ preprocessing → $O(\log e(G) + n)$ sorting time  
- **Optimal approach** (this paper): $O(m)$ preprocessing → $O(\log e(G))$ sorting time

The key insight is that preprocessing the DAG structure enables **extremely fast queries** by encoding the partial order efficiently.

## Applications in Engineering

### 1. **Project Management / Critical Path Analysis**
- Represent task dependencies as a DAG
- Use topological sort to identify feasible schedules
- Preprocessing computes slack times; queries answer "can task $x$ run before task $y$?"

### 2. **Compiler Optimization**
- Data-flow dependencies in instruction scheduling form a DAG
- Topological sort determines valid execution orders
- DAG preprocessing enables fast instruction reordering queries

### 3. **Database Query Execution**
- A query execution plan is a DAG of operators (join, filter, scan)
- Edges represent data-flow dependencies
- Preprocessing optimizes operator placement; topological sort defines execution order

### 4. **Version Control Systems (Git)**
- Commits and their parent relationships form a DAG
- Topological sort defines the logical history
- Efficient DAG preprocessing enables fast merge/rebase operations

### 5. **Hardware Verification / Logic Synthesis**
- Circuit logic is a DAG (combinational logic has no cycles without registers)
- Partial order reflects signal dependencies
- Preprocessing enables fast timing analysis and constraint propagation

### 6. **Machine Learning / Computation Graphs**
- TensorFlow/PyTorch represent computations as DAGs
- Forward/backward passes are topological traversals
- Efficient DAG processing is critical for training performance

## Common Mistakes / Pitfalls

### ❌ Confusing "partial order" with "DAG"
**Mistake**: Thinking every partial order can be represented as a DAG.
**Reality**: A DAG *is* the transitive reduction of a partial order. Not all edges are explicit; only the minimal transitive covering is needed.

### ❌ Assuming all topological sorts are equally likely
**Mistake**: Thinking if $e(G) = k$, each sort is uniform probability $1/k$.
**Reality**: The distribution of topological sorts depends on the DAG structure. Bottlenecks (vertices with high in-degree) make certain orderings more "constrained."

### ❌ Confusing $\log e(G)$ with $\log n$
**Mistake**: Using generic $O(\log n)$ bounds for sorting under partial information.
**Reality**: $e(G)$ can be exponentially smaller than $n!$, making $\log e(G) \ll n \log n$ possible. This is the whole point of preprocessing.

### ❌ Assuming preprocessing is "free"
**Mistake**: Believing that preprocessing has no practical cost.
**Reality**: $O(m)$ preprocessing is optimal but still linear in the graph size. For massive DAGs, preprocessing dominates total time