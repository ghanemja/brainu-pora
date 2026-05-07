# Kruskal's algorithm

## Definition

Kruskal's algorithm is a **greedy algorithm for computing the minimum spanning tree (MST)** of a weighted undirected graph. The algorithm constructs an MST by iteratively selecting edges in order of increasing weight, adding each edge to the tree if and only if it does not create a cycle.

**Formal statement:** Given a connected, weighted undirected graph $G = (V, E)$ with edge weights $w: E \to \mathbb{R}$, Kruskal's algorithm produces a set of edges $T \subseteq E$ such that:
- $T$ forms a spanning tree (connects all vertices with $|V|-1$ edges, no cycles)
- Total weight $\sum_{e \in T} w(e)$ is minimized
- $T$ is acyclic and contains exactly $|V| - 1$ edges

## Key Equations

**Correctness Property (Matroid Exchange Property):**
For any edge $e = (u,v)$ added by the algorithm at iteration $k$, with weight $w(e)$:
$$w(e) = \min\{w(e') : e' \text{ connects different components in forest } F_k\}$$

**Time Complexity:**
$$O(|E| \log |E| + |E| \cdot \alpha(|V|))$$

where $\alpha$ is the inverse Ackermann function (amortized cost of union-find operations), dominated by the edge sorting term: $O(|E| \log |E|)$ for comparison-based sorting.

**Space Complexity:** $O(|V| + |E|)$ for storing the graph and union-find data structure.

## Physical Intuition / Derivation

### Why Greedy Works

Kruskal's algorithm succeeds because the **minimum spanning tree problem satisfies the matroid property**—the greedy choice of the lightest edge that doesn't create a cycle always extends to an optimal solution.

**Intuitive argument:** Suppose the algorithm selects edge $e = (u,v)$ at some step, and imagine $e$ were *not* in some MST $T^*$. Then $T^* \cup \{e\}$ must contain a cycle. This cycle has another edge $e' = (x,y)$ also connecting the two components that would be joined by $e$. Since $e$ was selected by the algorithm, $w(e) \leq w(e')$. Swapping $e'$ for $e$ in $T^*$ yields an MST of equal or lower weight—contradiction.

### Algorithm Steps

1. **Sort edges** by weight: $w(e_1) \leq w(e_2) \leq \cdots \leq w(e_{|E|})$
2. **Initialize** forest $F$ with $|V|$ isolated vertices
3. **For each edge** $e_i = (u,v)$ in sorted order:
   - If $u$ and $v$ are in different connected components of $F$:
     - Add $e_i$ to $T$
     - Merge the components containing $u$ and $v$
4. **Return** $T$ (contains exactly $|V|-1$ edges)

The union-find (disjoint-set) data structure efficiently tests whether two vertices are in the same component and merges components.

## Applications in Engineering

### Network Design
- **Telecommunication networks:** Minimize cable length connecting cities while ensuring full connectivity
- **Power grids:** Design transmission networks with minimum material cost while serving all substations
- **Road networks:** Planning infrastructure connecting regions with minimum construction cost

### Circuit Design
- **VLSI routing:** Connect circuit components with minimum total wire length
- **PCB layout:** Route connections between components minimizing area and parasitic capacitance

### Clustering and Data Structure Compression
- **DAG-compressed graphs** (per source material): Kruskal's algorithm can be adapted to work directly on compressed graph representations, processing large graphs without full decompression
- **Hierarchical clustering:** Building minimum-weight dendrograms in agglomerative clustering

### Computer Networks
- **Network topology design:** Designing spanning trees for broadcast protocols (e.g., bridge spanning tree in switched Ethernet)
- **Redundancy optimization:** Selecting minimum-cost edges for network resilience

## Common Mistakes / Pitfalls

### 1. **Assuming it works on directed graphs**
Kruskal's algorithm requires **undirected graphs**. For directed graphs, the problem becomes finding a **minimum spanning arborescence** (directed MST), which requires Edmonds' algorithm—a more complex procedure.

### 2. **Forgetting edge sorting overhead**
Students sometimes claim $O(|E| \log |V|)$ complexity, ignoring that sorting dominates: $O(|E| \log |E|) \gg O(|E| \cdot \alpha(|V|))$. If edges are pre-sorted, the algorithm runs in nearly linear time.

### 3. **Misunderstanding the greedy choice**
The algorithm does *not* greedily choose edges incident to the current tree. It globally selects the lightest edge that avoids cycles—a subtle but critical distinction from Prim's algorithm.

### 4. **Union-find implementation errors**
Without **path compression and union by rank**, union-find operations degrade from nearly $O(1)$ to $O(\log |V|)$, increasing total complexity.

### 5. **Handling disconnected graphs**
If $G$ is not connected, the algorithm produces a **minimum spanning forest** (one tree per component). The problem statement typically requires connectivity.

### 6. **Numerical precision with real edge weights**
When weights involve floating-point numbers, tie-breaking in sorting can affect which MST is selected (though all have equal total weight). Use consistent comparison operators.

## See Also

- [[Prim's algorithm]] — Alternative MST algorithm with $O(|E| + |V| \log |V|)$ complexity
- [[Union-find (Disjoint-set union)]] — Data structure enabling efficient cycle detection
- [[Minimum spanning tree]] — Problem definition and optimality characterization
- [[Greedy algorithms]] — General technique; MST is canonical correctness example
- [[DAG compression]] — Application to compressed graph representations (source context)

## Sources

- Chudigiewit