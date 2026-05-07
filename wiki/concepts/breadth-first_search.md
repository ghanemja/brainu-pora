# Breadth-First Search

## Definition

**Breadth-first search (BFS)** is a fundamental graph traversal algorithm that explores vertices of a graph in layers based on their distance from a source vertex. Starting from a designated source, BFS visits all vertices at distance $k$ before visiting any vertex at distance $k+1$.

Formally, given a graph $G = (V, E)$ and a source vertex $s \in V$, BFS computes:
- The set of all vertices reachable from $s$
- The shortest path distance $d(s, v)$ from $s$ to each reachable vertex $v$
- A **BFS tree** (or **level structure**) that encodes these shortest paths

BFS operates by maintaining a **frontier**: a set of vertices whose neighbors have not yet been explored. It processes vertices in first-in-first-out (FIFO) order.

## Key Equations

**Distance definition:** For a source vertex $s$ and vertex $v$ reachable from $s$,
$$d(s, v) = \min\{|P| : P \text{ is a path from } s \text{ to } v\}$$
where $|P|$ denotes the number of edges in path $P$.

**BFS layer structure:** Partition reachable vertices into levels:
$$L_k = \{v \in V : d(s, v) = k\}$$
The BFS tree spans from $L_0 = \{s\}$ through all non-empty layers.

**Time complexity:**
$$T(V, E) = O(|V| + |E|)$$
Each vertex is enqueued and dequeued once; each edge is examined once.

**Space complexity:**
$$S(V, E) = O(|V|)$$
For the queue and distance array.

## Physical Intuition / Derivation

BFS can be understood as a **wavefront expansion** from the source:

1. **Layer 0:** Start with the source vertex $s$.

2. **Layer construction:** For each layer $L_k$, identify all neighbors of vertices in $L_k$ that have not yet been visited. These form layer $L_{k+1}$.

3. **Invariant:** When we begin processing layer $L_k$, we have discovered all vertices at distance $\leq k$, and all edges from $L_k$ lead either within the layer or to unvisited vertices (which must be in $L_{k+1}$).

4. **FIFO ordering:** The queue enforces that we exhaust one layer completely before moving to the next. This is the key difference from depth-first search, which uses a stack (LIFO).

**Why shortest paths?** In an unweighted graph, the first time we reach a vertex is via a shortest path. If we reached $v$ after exploring $k$ edges, any other path to $v$ must use at least $k$ edges (by the triangle inequality in graphs).

## Applications in Engineering

### Network and Connectivity Analysis
- **Component discovery:** Finding all nodes reachable from a given network node
- **Social network analysis:** Computing degrees of separation, identifying connected communities
- **Network reachability:** Determining which servers are accessible from a given host

### Robot Navigation and Path Planning
- **Multi-step planning:** Finding minimum-action paths in discrete environments
- **Sensor network deployment:** Determining coverage frontiers and expansion priorities
- **Autonomous exploration:** Systematically exploring unknown environments level-by-level

### Graph Compression Algorithms
As noted in the source material, BFS adapts naturally to **compressed graph representations** (e.g., DAG compressions). The algorithm can operate directly on compressed vertex clusters without decompressing, maintaining runtime proportional to compressed size—critical for billion-edge industrial graphs.

### Circuit and Logic Design
- **Topological layer assignment:** Partitioning logic gates by depth for pipelining
- **Signal propagation analysis:** Computing gate depths and timing slack

### Data Structure Validation
- **Tree/DAG verification:** Checking acyclicity and computing depth metrics
- **Dependency resolution:** Ordering tasks respecting DAG constraints

## Common Mistakes / Pitfalls

1. **Forgetting to mark visited vertices:** Revisiting the same vertex leads to infinite loops in cyclic graphs and $O(\infty)$ or exponential time.

2. **Using BFS on weighted graphs:** BFS gives shortest paths only by *edge count*, not by weight. Use **Dijkstra's algorithm** instead.

3. **Assuming bidirectional equivalence:** In directed graphs, reachability is not symmetric. Compute forward BFS from source and backward BFS from target separately if needed.

4. **Queue vs. stack confusion:** Accidentally using a stack (depth-first) yields correct exploration but loses the layer-by-layer property and shortest-path guarantee.

5. **Mishandling disconnected components:** BFS only explores vertices reachable from the source. To explore the entire graph, run BFS from an unvisited vertex after each BFS completes.

6. **Compressed graph pitfall:** When working on compressed graphs (as in DAG compressions), naively decompressing destroys efficiency. The algorithm must respect cluster boundaries and work on the compressed representation.

## Pseudocode Reference

```
BFS(G, s):
  queue ← empty queue
  visited[s] ← true
  distance[s] ← 0
  enqueue(queue, s)
  
  while queue is not empty:
    u ← dequeue(queue)
    for each neighbor v of u in G:
      if not visited[v]:
        visited[v] ← true
        distance[v] ← distance[u] + 1
        parent[v] ← u
        enqueue(queue, v)
```

## See Also

- [[Depth-First Search]] — alternative graph traversal; explores deeply before breadth
- [[Dijkstra's Algorithm]] — extends BFS to weighted graphs via priority queue
- [[Graph Compression]] — DAG/tree compressions enabling BFS on compact representations
- [[Shortest Path Problem]] — theoretical foundation; BFS solves unweighted case optimally
- [[Connected Components]] — application of BFS/DFS to partition graphs

## Sources

- Chudigiewitsch, F., Tantau, T., & Winkler, F. (2026). "On the Complexity of Fundamental Problems for DAG-