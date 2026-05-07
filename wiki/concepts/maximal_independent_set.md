# Maximal Independent Set

## Definition

A **maximal independent set (MIS)** in an undirected graph $G = (V, E)$ is a subset $S \subseteq V$ of vertices such that:

1. **Independence**: No two vertices in $S$ are adjacent (i.e., for all $u, v \in S$ with $u \neq v$, $(u,v) \notin E$)
2. **Maximality**: $S$ is maximal, meaning no additional vertex from $V \setminus S$ can be added to $S$ while preserving independence

**Important distinction**: A maximal independent set is *not* necessarily a *maximum* independent set. A maximum independent set is one with the largest possible cardinality across all independent sets in the graph. A maximal independent set is merely locally maximal—it cannot be extended further, but other maximal independent sets in the same graph may have different sizes.

## Key Equations

For a graph $G = (V, E)$ with $|V| = n$ vertices and $|E| = m$ edges:

$$|MIS(G)| \geq \frac{n}{\Delta + 1}$$

where $\Delta$ is the maximum degree. This lower bound follows from a greedy argument: when selecting an independent set, adding a vertex $v$ eliminates at most $\Delta$ other vertices from consideration.

For a $d$-regular graph (all vertices have degree $d$):
$$\frac{n}{d+1} \leq |MIS(G)| \leq n - \frac{m}{d}$$

## Physical Intuition / Derivation

**Greedy Construction Intuition:**

Imagine placing non-attacking objects on a network where objects cannot occupy adjacent positions. A maximal independent set represents a configuration where:
- No two selected positions are neighbors
- We cannot fit any additional object without violating independence

**Why "Maximal" vs. "Maximum" Matters:**

Consider a path graph with 4 vertices: $1 - 2 - 3 - 4$
- $\{1, 3\}$ is an independent set (size 2) but *not maximal*—we can add vertex 4 to get $\{1, 3, 4\}$
- $\{1, 3, 4\}$ is a maximal independent set (cannot extend further)
- $\{1, 4\}$ is also a maximal independent set (size 2)
- The maximum independent set is $\{1, 3\}$ or $\{2, 4\}$ (size 2)

In this case, all maximal independent sets happen to be maximum, but this is not always true.

**Greedy Algorithm Derivation:**

The following greedy procedure produces *a* maximal independent set:

1. Initialize $S := \emptyset$
2. While $V \setminus S \neq \emptyset$:
   - Select any vertex $v \in V \setminus S$ (arbitrarily or via some rule)
   - Add $v$ to $S$
   - Remove $v$ and all neighbors of $v$ from future consideration
3. Return $S$

This terminates with a maximal independent set because any vertex not in $S$ was removed, meaning it is either:
- Selected into $S$, or
- Neighboring some vertex in $S$

**Luby's Parallel Algorithm** (referenced in source [21]) leverages randomization to compute MIS in parallel:
- Vertices select themselves with probability $1/(2\Delta)$ independently at random
- High-probability analysis shows expected logarithmic depth
- Derandomization techniques (source [22]) remove the randomness without asymptotic penalty

## Applications in Engineering

### 1. **Graph Coloring**
MIS is fundamental to distributed $(Δ+1)$-coloring algorithms (source [19]). A proper vertex coloring can be constructed recursively:
- Find an MIS in $G$
- Color those vertices with color 1
- Recursively color the remaining graph with colors $2, 3, \ldots, Δ+1$

### 2. **Distributed Algorithms**
In distributed computing, MIS algorithms run on low-power, networked devices:
- Nodes compute locally with only neighbor communication
- Used for leader election and distributed control protocols
- Luby's algorithm enables sublinear-depth parallel solutions

### 3. **Network Problems**
- **Wireless sensor networks**: MIS represents a maximal set of non-interfering transmitters
- **Load balancing**: Select a maximal set of independent tasks that can execute concurrently
- **k-core decomposition** (source [20]): Related iterative peeling algorithms use MIS-like independence constraints

### 4. **Graph Subproblem Reduction**
MIS algorithms appear in pipelines for:
- Clique counting and peeling (source [25])
- Butterfly computations (source [26])
- Hypergraph processing (source [27])

These use MIS to identify bottleneck substructures or partition work across processors.

## Common Mistakes / Pitfalls

1. **Confusing MIS with Maximum Independent Set**: Students often assume finding an MIS guarantees a largest independent set. In general graphs, this is NP-hard; MIS is only locally optimal.

2. **Greedy Doesn't Always Give the Largest MIS**: Different selection orders in the greedy algorithm yield different maximal sets with potentially different sizes.

3. **Overlooking Parallelism Constraints**: Luby's algorithm is randomized and parallel. Attempting deterministic sequential implementations misses its efficiency benefits.

4. **Degree Assumption Errors**: The bound $|MIS(G)| \geq n/(\Delta+1)$ requires knowing or computing maximum degree $\Delta$; forgetting this leads to loose or incorrect analysis.

5. **Initialization Neglect**: In distributed settings, assuming synchronized starts or shared state is unrealistic; robust MIS algorithms must handle asynchrony.

## See Also

- [[Graph Coloring]] – immediate application of MIS
- [[Distributed Algorithms]] – parallelization framework for MIS computation
- [[k-core Decomposition]] – related iterative graph reduction technique
- [[Maximum Independent Set]] – NP-hard optimization variant
- [[Greedy Algorithms]] – found