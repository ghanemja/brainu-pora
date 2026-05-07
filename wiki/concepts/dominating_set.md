# Dominating Set

## Definition

A **dominating set** is a subset $D$ of vertices in a graph $G = (V, E)$ such that every vertex not in $D$ is adjacent to at least one vertex in $D$. Formally:

$$D \subseteq V \text{ is dominating if } \forall v \in V \setminus D, \exists u \in D : (u,v) \in E$$

Equivalently, the dominating set property requires that the closed neighborhood $N[D] = D \cup \bigcup_{v \in D} N(v)$ equals the entire vertex set $V$, where $N(v)$ denotes the open neighborhood of $v$.

### Variants

- **Minimum dominating set**: A dominating set of smallest cardinality; the **domination number** $\gamma(G)$ is its size
- **Approximately dominating set**: A relaxation where the domination condition is satisfied approximately (e.g., most vertices are dominated)
- **Total dominating set**: Every vertex (including those in $D$) must have a neighbor in $D$

## Key Equations

**Domination condition:**
$$N[D] = V \quad \Leftrightarrow \quad D \text{ is dominating}$$

**Domination number bounds:**
$$\gamma(G) \geq \frac{|V|}{\Delta(G) + 1}$$
where $\Delta(G)$ is the maximum degree.

**Trivial bounds:**
$$1 \leq \gamma(G) \leq |V|$$

## Physical Intuition / Derivation

### Motivation from Graph Coverage

Imagine positioning monitoring stations (vertices in $D$) throughout a network. A dominating set ensures that every location either has a station or is within communication distance of one. This models:

- **Wireless networks**: Base stations must cover all devices
- **Facility location**: Service centers positioned to reach all customers
- **Surveillance**: Cameras positioned to observe all critical areas

### Why This Matters

The dominating set is minimal in a structural sense—you cannot remove any vertex without violating the domination property. However, finding the *minimum* dominating set is **NP-hard** for general graphs, making it a canonical hard optimization problem in computer science.

### Building Intuition

Consider a graph where vertices represent voters and edges represent preference comparisons:

- A **dominating set of candidates** ensures that every non-selected candidate loses a pairwise comparison to at least one selected candidate
- This connects to the **Condorcet principle** in voting theory: every "outside" alternative is "beaten" by some member of the chosen set
- This motivates the notion of a **Condorcet-winning set**, which is a dominating set in the pairwise preference graph

## Applications in Engineering

### 1. **Wireless Sensor Networks**
Determining minimum base station coverage where each uncovered node must be adjacent to a covered node. Minimizing $|D|$ reduces infrastructure cost.

### 2. **Distributed Systems & Consensus**
Selecting a minimum set of reference nodes such that every other node can communicate with or verify state through the dominating set, ensuring network consensus.

### 3. **Social Choice & Voting**
Identifying a dominating set of candidates in the pairwise preference tournament ensures selection of candidates that collectively defeat all alternatives. Central to analyzing **Condorcet dimensions** in voting systems.

### 4. **Supply Chain & Facility Location**
Determining minimum locations for warehouses, distribution centers, or service points such that all demand nodes are within service radius of at least one facility.

### 5. **Power Grid & Critical Infrastructure**
Identifying minimum number of monitoring points (PMUs—phasor measurement units) to observe all nodes in an electrical grid directly or through one hop.

### 6. **Approximation Algorithms**
Since exact solutions are intractable, greedy approximations (selecting vertices with highest undominated neighbors first) achieve $O(\log n)$ approximation ratio—used in real network optimization.

## Common Mistakes / Pitfalls

### 1. **Confusing with Independent Set**
**Error**: Thinking dominating set $D$ requires vertices in $D$ to be non-adjacent.

**Correction**: Vertices in $D$ can be arbitrarily connected to each other. The constraint is only on vertices *outside* $D$.

### 2. **Overlooking Triviality**
**Error**: Assuming a dominating set always exists or is unique.

**Correction**: Dominating sets always exist (the entire vertex set $V$ trivially dominates), but minimum dominating sets are rare and hard to compute.

### 3. **Misapplying to Directed Graphs**
**Error**: Applying undirected domination definitions to directed graphs without care.

**Correction**: In directed graphs, must specify whether edges must point *into* $D$ (in-dominating) or *out of* $D$ (out-dominating), or both.

### 4. **NP-Hardness Pessimism**
**Error**: Concluding that dominating sets cannot be computed in reasonable time.

**Correction**: NP-hardness applies to *exact minimum* domination; practical approximations, heuristics, and parameterized algorithms work well on instances of moderate size.

### 5. **Forgetting Vertex Self-Domination**
**Error**: Thinking vertices in $D$ must be dominated by other vertices in $D$.

**Correction**: By definition, every vertex in $D$ dominates itself (via the closed neighborhood $N[D]$), so any vertex can be in $D$.

## See Also

- [[Condorcet Principle]]: Voting theory concept where dominating sets represent winning coalitions
- [[Vertex Cover]]: Related NP-hard graph problem; dual concept in some contexts
- [[Independent Set]]: Contrasting optimization problem on graphs
- [[Graph Coloring]]: Another classic NP-hard graph problem with connections to domination on specific graph classes
- [[Approximation Algorithms]]: Techniques for computing near-optimal dominating sets in polynomial time

## Sources

- Charikar et al. [2026]: Approximately dominating sets and their existence properties
- Gärdenfors [1975]: Popularity concept in two-sided matching (cited as foundational for relaxations of standard solution concepts)
- General reference: Domination in graphs appears as a classical topic in extrem