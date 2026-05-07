# Euler Tour Trees

## Definition

An **Euler tour tree** (ETT) is a dynamic data structure for maintaining connectivity information and performing dynamic tree operations on forest graphs. Specifically, it represents a forest (a collection of trees) in a way that supports:

- **Link** operation: connect two trees by adding an edge between them
- **Cut** operation: disconnect a tree into two components by removing an edge
- **Tree connectivity queries**: determine if two vertices are in the same connected component
- **Aggregate queries**: compute values (sums, minimums, etc.) over paths or subtrees

The key insight is that an Euler tour—a traversal that lists each edge twice (once in each direction) as it traverses the tree in depth-first order—can be represented as a circular sequence. By maintaining this sequence in a balanced data structure (typically a balanced binary search tree or splay tree), dynamic operations become efficient.

## Key Equations

For a forest with $n$ vertices and $m$ edges, an Euler tour tree achieves:

$$T_{\text{link}} = O(\log n), \quad T_{\text{cut}} = O(\log n), \quad T_{\text{query}} = O(\log n)$$

where all operations use balanced tree structures.

The Euler tour representation converts a tree $T = (V, E)$ with $|V| = n$ into a sequence of length $2|E| = 2(n-1) = 2n - 2$ by recording each edge traversal.

## Physical Intuition / Derivation

### Why Euler Tours?

Consider a forest as a collection of rooted trees. A straightforward approach to dynamic connectivity uses union-find, which answers reachability in near-constant amortized time but cannot efficiently handle edge deletions.

ETTs solve this by encoding tree structure into a linear sequence that can be split and concatenated:

1. **Euler tour construction**: Traverse each tree in DFS order, writing each directed edge $(u \to v)$ and $(v \to u)$ as encountered. This produces a circular sequence where:
   - Vertices appear multiple times (once per incident edge)
   - The sequence encodes the entire tree structure
   - Path information between vertices is localized

2. **Balanced representation**: Store the Euler tour in a balanced BST (e.g., splay tree) where:
   - Each node in the BST corresponds to one edge occurrence in the tour
   - Each tree vertex in the original forest maps to a contiguous interval in the BST
   - Tree structure queries reduce to interval queries on the BST

3. **Link operation**: To link trees $T_1$ and $T_2$ by adding edge $(u, v)$:
   - Insert the two directed edges $(u \to v)$ and $(v \to u)$ into the appropriate positions in the Euler tours
   - This merges two circular sequences into one

4. **Cut operation**: To cut edge $(u, v)$:
   - Remove the two directed edge records from the Euler tour
   - This splits one circular sequence into two

### Why $O(\log n)$ is Achievable

Because Euler tour positions are maintained in a balanced BST:
- Finding the interval for a vertex: $O(\log n)$
- Splitting/joining tours: $O(\log n)$ per rebalancing
- Path aggregate queries: $O(\log n)$ with augmented tree metadata

## Applications in Engineering

### 1. **Dynamic Connectivity in Networks**
Real-time network topology maintenance where links fail and are restored:
- Wireless networks with node mobility
- Data center network reconfiguration
- Telecommunication routing updates

### 2. **Parallel Graph Algorithms**
[[Parallel batch-dynamic k-core decomposition|[20]]] and related problems:
- Batch updates to graph structure
- Maintaining decompositions (k-core, degeneracy) under insertions/deletions
- Parallel peeling and clique counting operations

### 3. **Incremental Tree Algorithms**
- Maintaining minimum spanning trees in dynamic edge-weight scenarios
- Online connectivity certificates and 2-edge-connected components
- Hierarchical cluster maintenance

### 4. **Distributed Systems**
Consistency maintenance in replicated forest structures where:
- Nodes join and leave dynamically
- Quorum trees must be maintained efficiently

## Common Mistakes / Pitfalls

### 1. **Confusing with Union-Find**
**Mistake**: Assuming Euler tour trees are just a variant of union-find.  
**Reality**: ETTs explicitly support *edge deletion*, which union-find handles poorly (requires full rebuild). ETTs are ideal when deletions are frequent.

### 2. **Overlooking Euler Tour Representation Overhead**
**Mistake**: Not accounting for the $2n$ sequence length.  
**Reality**: Memory is $O(n)$ but constants matter; each tree vertex and edge has multiple records in the tour.

### 3. **Assuming All Path Queries are $O(\log n)$**
**Mistake**: Forgetting that only *aggregate* queries on paths/subtrees are supported efficiently.  
**Reality**: Arbitrary path operations require additional tree augmentation. Simple reachability queries need only $O(\log n)$, but computing (say) the sum of edge weights on a path requires careful augmentation.

### 4. **Incorrect Link/Cut Sequencing**
**Mistake**: Performing link/cut operations without updating Euler tour endpoints.  
**Reality**: The circular tour must be carefully re-spliced; off-by-one errors in interval positions are common.

### 5. **Parallelization Naiveté**
**Mistake**: Applying sequential ETT operations in parallel without synchronization.  
**Reality**: [[Batch-parallel Euler tour trees|[28]]] require careful batching of updates to avoid lock contention; not all operations can be parallelized trivially.

## See Also

- [[Splay Trees]]: The typical underlying balanced data structure for efficient amortized splicing
- [[Dynamic Connectivity]]: Broader problem class; ETTs are one solution among several (link-cut trees, dynamic 2-edge-connected components)
- [[Parallel Graph Algorithms]]: Applications in k-core decomposition and clique peeling
- [[Union-Find (Disjoint Set Union)]]: Related but less powerful for dynamic deletions
- [[Tree Decomposition]]: Hierarchical tree structures that ETTs help maintain dynamically

## Sources

- [28]