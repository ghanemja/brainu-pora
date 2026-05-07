# Hamiltonian Path

## Definition

A **Hamiltonian path** is a path in a graph that visits every vertex exactly once. In formal terms, given a graph $G = (V, E)$ where $|V| = n$, a Hamiltonian path is a sequence of vertices $(v_1, v_2, \ldots, v_n)$ such that:

1. All vertices in $V$ appear exactly once in the sequence
2. Consecutive vertices in the sequence are connected by edges: $(v_i, v_{i+1}) \in E$ for all $i \in \{1, 2, \ldots, n-1\}$

A **Hamiltonian cycle** (or circuit) additionally requires an edge between $v_n$ and $v_1$, closing the path into a loop.

### Related Graph Structure: Flip Graphs

In the context of combinatorial structures, a **flip graph** on a family of objects (e.g., ideals of a poset) is constructed where:
- Vertices represent distinct objects (ideals, antichains, etc.)
- Edges connect objects that differ by a small, well-defined modification (a "flip")

A Hamiltonian path in such a flip graph ensures an efficient enumeration where consecutive objects differ minimally, enabling what is called a **Gray code order**.

## Key Equations

For a graph $G = (V, E)$, a Hamiltonian path satisfies:

$$\text{Path} = (v_1, v_2, \ldots, v_n) \text{ where } (v_i, v_{i+1}) \in E \text{ and } |\{v_1, \ldots, v_n\}| = |V|$$

The **Gray code property** for enumeration states that consecutive objects in the enumeration sequence differ in at most $k$ elements:

$$\text{Hamming distance}(S_i, S_{i+1}) \leq k$$

where $S_i$ and $S_{i+1}$ represent the $i$-th and $(i+1)$-th visited objects.

## Physical Intuition / Derivation

### Why Hamiltonian Paths Matter in Enumeration

When enumerating a large family of combinatorial objects (e.g., all ideals of a partially ordered set), a naive approach visits them in arbitrary order. However, if we can arrange them along a **Hamiltonian path in the flip graph**, we gain:

1. **Minimal change between consecutive states**: Objects differing in only a few elements can be generated from one another via simple local modifications rather than reconstructing from scratch.

2. **Constant amortized delay**: The amortized time to enumerate the next object becomes constant, despite the total number of objects potentially being exponential.

### Construction via Recursive Decomposition

From the source material, Hamiltonian paths on flip graphs of poset ideals are constructed by:

- **Recursive partitioning**: Breaking the poset into smaller pieces via longest chain decomposition
- **Interleaving recursion**: Carefully ordering the recursive calls so that the resulting enumeration visits objects in a sequence where consecutive ideals differ in at most 2–3 elements
- **Potential analysis**: Using the "Pyramid condition" (mentioned in the paper) to prove that the amortized cost per visit is constant

## Applications in Engineering

### 1. **Combinatorial Optimization & Enumeration**
When enumerating all valid configurations of a system (e.g., all feasible production schedules, all valid network topologies), a Hamiltonian path in the configuration flip graph allows rapid enumeration with minimal state changes.

### 2. **VLSI Design & Logic Synthesis**
In the enumeration of all valid logic implementations or state assignments, Hamiltonian paths on flip graphs enable Gray code generation, reducing the number of signal transitions and minimizing switching noise.

### 3. **Scheduling & Constraint Satisfaction**
Enumerating all antichains of a partial order (representing conflict-free task sets) becomes tractable with Hamiltonian paths on the antichain flip graph—critical for parallel scheduling and resource allocation.

### 4. **Data Structure Enumeration**
Ranking and unranking combinatorial structures (lattice paths, binary trees, permutations) often relies on Gray codes derived from Hamiltonian paths, enabling O(1) amortized navigation.

### 5. **Robotics & Path Planning**
While not directly Hamiltonian path enumeration, the principle of visiting all configurations (waypoints, joint configurations) in a continuous, minimal-change sequence relates to Hamiltonian path concepts in configuration space.

## Common Mistakes / Pitfalls

### 1. **Confusing Existence with Computability**
A Hamiltonian path may exist in a flip graph, but computing it efficiently is not automatic. The source material notes that even when a Hamiltonian path exists on the flip graph of poset ideals (Pruesse & Ruskey result), it is **unknown whether such a path can be found with constant amortized delay**.

### 2. **Assuming All Graphs Have Hamiltonian Paths**
Hamiltonian path existence is NP-hard to determine in general graphs. Not every flip graph has a Hamiltonian path; existence must be proven separately for each class of objects.

### 3. **Conflating Hamiltonian Paths with Optimal Enumeration**
The existence of a Hamiltonian path does not guarantee the fastest enumeration algorithm. Trade-offs exist between:
- Minimizing object differences (Gray code order) vs. minimizing per-visit computation cost
- Achieving constant delay for all objects vs. constant *amortized* delay

### 4. **Overlooking Initialization Costs**
Algorithms like Algorithm 1.1 and 1.2 (in the source) have $O(n^2)$ initialization time and space. The constant-delay property applies to the *enumeration loop*, not the total runtime. For small $k$, initialization dominates.

### 5. **Misinterpreting "Loopless" Algorithms**
A "loopless" algorithm (mentioned in the source) does not mean "no loops." It means no unnecessary repeated computation within the per-iteration loop—each visited object is generated in $O(1)$ time without internal loops, enabling constant amortized delay.

## See Also

- [[Gray Code]]: A binary encoding where consecutive values differ in exactly one bit; generalizes to