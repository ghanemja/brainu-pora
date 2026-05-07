# Minimum Spanning Trees

## Definition

A **minimum spanning tree (MST)** of a weighted undirected graph $G = (V, E, w)$ is a subset of edges $T \subseteq E$ that satisfies:

1. **Acyclic**: $T$ contains no cycles
2. **Connected**: $T$ spans all vertices in $V$ (forms a tree)
3. **Minimal weight**: The sum $w(T) = \sum_{e \in T} w(e)$ is minimized among all spanning trees

Formally, an MST is a spanning tree $T$ such that for any other spanning tree $T'$:
$$w(T) \leq w(T')$$

**Key observation**: A connected graph with $n$ vertices has an MST with exactly $n-1$ edges. If the graph is disconnected, we compute a **minimum spanning forest** (one MST per connected component).

## Key Equations

**Total Weight of MST**:
$$w(T^*) = \sum_{e \in T^*} w(e)$$

where $T^*$ denotes an optimal (minimum-weight) spanning tree.

**Cycle Property** (optimality condition):
For any cycle $C$ in $G$, the maximum-weight edge in $C$ cannot be in any MST (except when it has non-unique weight).

**Cut Property** (used in greedy algorithms):
For any cut $(S, V \setminus S)$ of the graph, the minimum-weight edge crossing the cut belongs to some MST.

## Physical Intuition / Derivation

### Why MSTs Matter

Imagine connecting $n$ cities with roads of varying construction costs. You want minimal total cost while ensuring all cities remain connected. An MST solves this exactly.

### Greedy Optimality

The key insight is that MST algorithms exploit the **cut property**: locally choosing the cheapest way to extend a partial tree always leads to a globally optimal solution. This works because:

1. **No negative cycles exist** (weights are non-negative in most applications)
2. **Local minimality compounds**: adding the cheapest edge to connect a new region never forces us to remove a cheaper edge later
3. **Exchange argument**: if a greedy choice is not in an MST $T^*$, we can always swap an edge in $T^*$ for our choice without increasing total weight

This is formalized through the **matroid** structure underlying MST problems.

## Applications in Engineering

### 1. **Network Design**
- **Telecommunications**: Minimum-cost fiber optic backbone connecting cities
- **Power distribution**: Optimal placement of transmission lines connecting substations
- **Water/gas pipelines**: Least-cost network topology

### 2. **Computer Networks**
- **Spanning tree protocol (STP)**: Prevents loops in Ethernet switches by computing an MST of the switch topology
- **Ad-hoc networking**: Routing trees in wireless sensor networks minimize energy consumption
- **DAG-compressed graphs**: Modern work (cited sources) shows MST computation can be accelerated on compressed graph representations

### 3. **Clustering & Data Analysis**
- **Single-linkage hierarchical clustering**: MST guides cluster formation in agglomerative clustering
- **Outlier detection**: Edges with unusually high weight in an MST identify anomalies

### 4. **Civil Engineering**
- **Road network planning**: Minimum-cost connected infrastructure
- **Structural analysis**: Truss design optimization

### 5. **Manufacturing**
- **Circuit design**: Routing connections on PCBs with minimal wire length
- **Supply chain networks**: Minimum-cost logistics networks

## Algorithms

### Kruskal's Algorithm
**Greedy by edge weight**:
1. Sort all edges by weight (ascending)
2. Iterate through edges; add each edge if it doesn't create a cycle
3. Stop when $n-1$ edges are selected

**Complexity**: $O(|E| \log |E| + |E| \alpha(|V|))$ where $\alpha$ is the inverse Ackermann function (near-constant)

**Key tool**: Union-Find (disjoint set union) data structure for cycle detection

### Prim's Algorithm
**Greedy by vertex addition**:
1. Start with an arbitrary vertex
2. Repeatedly add the minimum-weight edge from the current tree to an outside vertex
3. Stop when all vertices are included

**Complexity**: $O(|E| + |V| \log |V|)$ with binary heap, or $O(|V|^2)$ with adjacency matrix

### Borůvka's Algorithm
Works by repeatedly contracting minimum-weight edges in each component; efficient for **parallel computation** and **graph compression** scenarios.

## Common Mistakes / Pitfalls

1. **Assuming uniqueness**: MSTs are not necessarily unique when multiple edges have the same weight. Different algorithms may produce different MSTs with equal total weight.

2. **Confusing with shortest paths**: MST minimizes *total* edge weight over a spanning tree, not distance between specific vertices. Dijkstra's algorithm solves the latter.

3. **Ignoring disconnected graphs**: If $G$ is disconnected, no spanning tree exists—compute a minimum spanning *forest* instead.

4. **Negative weights**: Classical algorithms (Kruskal, Prim) assume non-negative weights. Negative edge weights require careful handling or may indicate the problem should use other approaches (e.g., negative-weight cycles break MST definitions).

5. **Graph compression pitfall**: When using compressed representations (e.g., DAG compressions), naively decompressing before running MST algorithms defeats the compression purpose. Adapted algorithms are needed (as shown in the cited paper).

6. **Greedy failure on other problems**: The cut property works *only* for MSTs. Greedy approaches fail for minimum-weight Hamiltonian cycles, traveling salesman problems, etc.

## See Also

- [[Spanning Tree|Spanning Trees]] — foundational concept; MST is an optimized variant
- [[Kruskal's Algorithm]] — primary MST construction algorithm
- [[Prim's Algorithm]] — alternative greedy MST algorithm  
- [[Union-Find Data Structure]] — enables efficient cycle detection in Kruskal's algorithm
- [[Graph Compression]] — modern techniques for working with MSTs on compressed representations
- [[Shortest Path Algorithms]] — related but distinct graph optimization problems

## Sources

- *On the Complexity of