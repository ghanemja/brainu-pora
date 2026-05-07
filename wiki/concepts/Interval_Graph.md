# Interval Graph

## Definition

An **interval graph** is an undirected graph $G = (V, E)$ where each vertex $v \in V$ can be mapped to an interval $I_v = [a_v, b_v]$ on the real line such that two vertices $u$ and $v$ are adjacent (connected by an edge) if and only if their corresponding intervals overlap:

$$(u, v) \in E \iff I_u \cap I_v \neq \emptyset$$

In other words, an interval graph is the intersection graph of a set of intervals on the real line. The mapping from vertices to intervals is called an **interval representation** of the graph.

**Key Property**: A graph is an interval graph if and only if it is a **chordal graph** that contains no asteroidal triple (ATP)—a structural characterization that enables efficient algorithmic exploitation.

## Key Equations

**Interval Overlap Condition**:
$$I_u \cap I_v \neq \emptyset \iff \max(a_u, a_v) < \min(b_u, b_v)$$

**Clique Size in Interval Graphs**: For any interval graph $G$, the size of the maximum clique equals the chromatic number (a rare property):
$$\omega(G) = \chi(G)$$

where $\omega(G)$ is the clique number and $\chi(G)$ is the chromatic number.

**Greedy Coloring Optimality**: The greedy coloring algorithm applied to intervals sorted by left endpoint produces an optimal coloring in $O(n \log n)$ time, where $n = |V|$.

## Physical Intuition / Derivation

### Why Interval Graphs Matter

Interval graphs naturally model **temporal and spatial scheduling constraints**. Consider a set of jobs or tasks, each occupying a time interval on a timeline:

- **Temporal interpretation**: If vertex $u$ represents a task occupying time interval $[a_u, b_u]$, then two tasks conflict (require different resources) if their time windows overlap.
- **Resource allocation**: Finding the minimum number of resources (colors) needed is equivalent to finding $\chi(G)$, which for interval graphs equals the maximum number of overlapping intervals at any point in time.

### Example Construction

Suppose we have three tasks:
- Task A: $[0, 5)$
- Task B: $[3, 8)$  
- Task C: $[7, 10)$

The interval graph has edges: $(A, B)$ since $[0,5) \cap [3,8) \neq \emptyset$, and no edge $(A,C)$ or $(B,C)$ since their intervals don't overlap. The graph requires 2 colors (A and B conflict; C is independent).

### Algorithmic Foundation

The power of interval graphs lies in their **total order structure**: sorting intervals by left endpoint imposes a natural ordering that respects the conflict relationship. This is why greedy algorithms achieve optimality—we process intervals left-to-right and assign the smallest available color to each.

In contrast, general graphs lack this structure, making the graph coloring problem NP-hard.

## Applications in Engineering

### 1. **Time-Sensitive Network (TSN) Scheduling**
In the referenced paper, interval graphs model no-wait scheduling on daisy-chain topologies. Each data stream occupies a time window (interval) on the network, and overlapping intervals represent conflicts requiring different time slots. The polynomial-time solvability of interval graph coloring enables optimal scheduling for thousands of streams in industrial automation and in-vehicle communication systems.

### 2. **Job Shop and Process Scheduling**
Manufacturing systems use interval graphs to represent:
- Machine allocation (each job is an interval; overlapping jobs need different machines)
- Assembly line sequencing (temporal dependencies modeled as interval conflicts)
- Resource leveling in construction projects

### 3. **Register Allocation in Compilers**
Variables' live ranges (intervals during which they must be stored) form an interval graph. Finding the minimum number of CPU registers needed is the interval graph coloring problem, solved optimally in polynomial time.

### 4. **Bandwidth Allocation in Communication Networks**
Flows or connections occupy time-frequency intervals; overlapping allocations must use different channels or time slots. Spectrum allocation and wavelength assignment in optical networks leverage interval graph structure.

### 5. **Classroom/Exam Scheduling**
Courses or exams occupy time slots (intervals), and conflicting schedules must use different rooms or time periods.

## Common Mistakes / Pitfalls

### 1. **Confusing Interval Graphs with General Chordal Graphs**
Not all chordal graphs are interval graphs. A chordal graph is an interval graph if and only if it is **claw-free and contains no asteroidal triple**. Students sometimes assume efficient algorithms for chordal graphs apply to general graphs.

### 2. **Applying Greedy Coloring Without Interval Ordering**
The greedy algorithm achieves optimality only when vertices (intervals) are processed in **sorted order by left endpoint**. Arbitrary ordering can produce suboptimal colorings. Always verify the underlying problem admits an interval representation.

### 3. **Assuming Optimal Coloring = Minimum Number of Resources**
For interval graphs, yes—$\chi(G) = \omega(G)$. But this equality does **not** hold for general graphs. The maximum clique size provides only a lower bound.

### 4. **Overlooking Problem Reformulation**
The key insight in the TSN paper is recognizing that the no-wait scheduling problem **can be recast** as interval graph coloring with restricted color sets. Many scheduling problems are solvable if you identify the underlying interval graph structure; the challenge is the reformulation, not the algorithm.

### 5. **Ignoring Representation Construction**
An abstract graph must be verified to admit an interval representation before assuming interval graph properties. Recognition algorithms (e.g., using PQ-trees) exist but require careful implementation.

## See Also

- [[Graph Coloring Problem]] — The foundational problem of assigning colors to vertices such that no two adjacent vertices share a color
- [[Chordal Graph]] — A superclass of interval graphs with important structural properties
- [[Daisy-Chain Topology]] — Network architecture where interval graph scheduling is applied for TSN
- [[Time-Sensitive Networking (TSN)]] — Real-time deterministic communication framework exploiting polynomial-time interval scheduling