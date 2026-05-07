# Graph Reconstruction

## Definition

**Graph reconstruction** is the problem of determining the unknown edge set $E$ of a connected graph $G = (V, E)$ given:
- The visible vertex set $V$ (known)
- An oracle that answers **shortest path distance queries**: for any two vertices $u, v \in V$, the oracle returns $\text{dist}_G(u, v)$ (the length of the shortest path between $u$ and $v$)

The goal is to identify all edges with the minimum number of oracle queries. The reconstruction is complete when the query answers uniquely determine $E$.

### Query Model Specifics

A **shortest path (SP) distance query** takes two vertices $(u, v)$ as input and returns:
$$d(u, v) = \begin{cases} 
\text{minimum number of edges on any } u\text{-}v\text{ path} & \text{if path exists} \\
\infty & \text{if } u \text{ and } v \text{ are disconnected}
\end{cases}$$

This is an unweighted distance model; the graph is assumed to be unweighted and connected.

## Key Equations

### Trivial Upper Bound
Any graph can be reconstructed with:
$$Q_{\text{trivial}} = \binom{n}{2} = \frac{n(n-1)}{2}$$
queries by testing all vertex pairs for direct adjacency. An edge $(u,v)$ exists if and only if $d(u, v) = 1$.

### Bounded Degree, Bounded Treelength Result
For connected graphs with bounded degree $\Delta$ and bounded treelength $\text{tl}$:
$$Q_{\text{optimal}} = O_{\Delta, \text{tl}}(n \log n)$$

This improves over the previous best randomized algorithm:
$$Q_{\text{previous}} = \tilde{O}_\Delta(n^{3/2})$$

where $\tilde{O}$ notation hides polylogarithmic factors.

### Lower Bound
For bounded chordality graphs (a subclass of bounded treelength graphs):
$$Q_{\text{lower}} = \Omega(n \log n)$$

Thus the result is **asymptotically tight** for this graph class.

## Physical Intuition / Derivation

### Why the Problem is Hard

The naive approach—querying all pairs—costs $\Theta(n^2)$. However, we can do better by exploiting **structural properties** of the graph:

1. **For trees**: Even though trees have only $n-1$ edges, reconstructing them requires $\Omega(n^2)$ queries in the worst case (unbounded degree). This is because the distance between two distant leaves can only be verified by explicit distance queries.

2. **For bounded degree graphs**: Since each vertex has at most $\Delta$ neighbors, there are only $O(\Delta n)$ edges total. The challenge is identifying which vertex pairs are adjacent without querying all $\binom{n}{2}$ pairs.

3. **For bounded treelength graphs**: The key insight is that graphs with small **treelength** have a "tree-like" decomposition that limits structural complexity. This allows algorithms to:
   - Use a **BFS-based exploration** that prioritizes querying nearby vertices
   - Prune the search space using distance oracle properties
   - Reconstruct the edge set in nearly-linear complexity

### Algorithm Sketch

A reconstruction algorithm for bounded degree, bounded treelength graphs typically:

1. **Initialize** with vertices from a frontier (e.g., visited during BFS from an arbitrary root)
2. **For each vertex $v$**: Query distances from $v$ to all other vertices
3. **Identify edges**: An edge $(u, v)$ exists if $d(u, v) = 1$ AND no "shortcut" path of length $< 1$ exists (which is impossible, but we verify using triangle inequality and previously discovered edges)
4. **Optimize using structure**: Skip queries for vertex pairs that are provably non-adjacent based on their treelength decomposition

The $O(n \log n)$ bound arises because:
- We must query $\Omega(n \log n)$ pairs due to the lower bound
- The algorithm's careful use of tree decompositions achieves this bound
- Each query is processed in $O(1)$ time

## Applications in Engineering

### 1. **Internet Topology Reconstruction**
- **Problem**: Map the structure of routers and links in large networks (e.g., BGP topology) without direct access to routing tables
- **Solution**: Use ping-based distance estimates (hop counts) as shortest path oracle responses
- **Benefit**: Reconstruct backbone topology with $O(n \log n)$ measurements instead of all-pairs measurements

### 2. **Evolutionary/Phylogenetic Tree Reconstruction**
- **Problem**: Determine evolutionary relationships (edges) between species given only pairwise evolutionary distances
- **Application**: Distance matrices in bioinformatics (e.g., UPGMA, neighbor-joining algorithms)
- **Relevance**: Bounded treelength assumption models realistic evolutionary branching patterns

### 3. **Network Diagnostics**
- **Problem**: Identify faulty links in a network by querying latency between endpoint pairs
- **Benefit**: Minimal latency probes required to pinpoint issues

### 4. **Social Network Analysis**
- **Problem**: Reconstruct hidden social networks using shortest path/distance information (e.g., "degrees of separation")
- **Constraint**: Respect privacy by minimizing pairwise distance queries

### 5. **Sensor Network Topology**
- **Problem**: Determine connectivity in wireless sensor networks using distance/timing measurements
- **Practical Advantage**: Reduce energy cost of topology discovery

## Common Mistakes / Pitfalls

### 1. **Confusing Edge Existence with Distance Equality**
**Error**: Assuming $(u, v) \in E \iff d(u, v) = 1$

**Why it fails**: This is actually **correct** for unweighted graphs, but students often forget to verify it holds before assuming an edge.

**Correct approach**: Always verify $d(u, v) = 1$ is necessary **and sufficient** (it is, for unweighted connected graphs).

### 2. **Ignoring the Role of Graph Structure**