# Shortest Paths Algorithms

## Definition

A **shortest path algorithm** is a computational procedure that finds a minimum-cost path between two vertices in a weighted directed or undirected graph. For a source vertex $s$ and target vertex $t$, the algorithm determines the path $P = (v_0 = s, v_1, \ldots, v_k = t)$ that minimizes the total edge weight:

$$\text{cost}(P) = \sum_{i=0}^{k-1} w(v_i, v_{i+1})$$

where $w(u,v)$ denotes the weight of the edge from $u$ to $v$.

### Variants

- **Single-source shortest paths**: Compute shortest paths from one source $s$ to all other vertices
- **All-pairs shortest paths**: Compute shortest paths between all pairs of vertices
- **Weighted vs. unweighted graphs**: Weights can be non-negative or allow negative values (but not negative cycles in well-defined problems)
- **Single-target**: Equivalent to single-source in undirected graphs; requires reverse graph traversal in directed graphs

---

## Key Equations

### Distance Definition
The shortest path distance from $s$ to $t$ is:
$$d(s,t) = \min_{P: s \rightsquirc t} \sum_{(u,v) \in P} w(u,v)$$

### Bellman-Ford Recurrence
For dynamic programming, distances are updated iteratively:
$$d_i(v) = \min\left(d_{i-1}(v), \min_{(u,v) \in E} d_{i-1}(u) + w(u,v)\right)$$

where $d_i(v)$ is the shortest path distance to $v$ using at most $i$ edges.

### Triangle Inequality (Metric Property)
In non-negative edge weights, shortest path distances satisfy:
$$d(s,t) \leq d(s,u) + d(u,t) \quad \forall u$$

This is a key property for algorithm correctness and approximation analysis.

### Time Complexity Bounds
- **Dijkstra (non-negative weights, single-source)**: $O((V + E) \log V)$ with binary heap
- **Bellman-Ford (negative weights, single-source)**: $O(VE)$
- **Floyd-Warshall (all-pairs)**: $O(V^3)$
- **Recent advances (negative weights, near-linear)**: $O(E \cdot \text{poly}(\log V))$ [3], [5]

---

## Physical Intuition / Derivation

### Why Greedy Works for Non-Negative Weights

Dijkstra's algorithm relies on a **greedy selection principle**: once we've determined the shortest path to vertex $v$, no future relaxation can improve it if all edge weights are non-negative.

**Intuition**: Imagine spreading a wavefront from source $s$ at uniform speed. The first vertex a wavefront reaches is guaranteed to be reached via the shortest path, because:
1. Any alternative path would require traveling through a vertex already visited
2. All subsequent edges add positive cost, so cannot improve the path

Mathematically, if vertex $v$ is selected (smallest $d[v]$) before vertex $u$, then:
$$d[v] \leq d[u]$$

Any path from $v$ to $u$ via intermediate vertices $w$ has cost $\geq d[v] + w(v,w) \geq d[v]$, maintaining the invariant.

### Why Negative Weights Require More Care

With negative edge weights, the greedy assumption breaks. A longer path via a negative edge might ultimately be shorter:

$$d[v] \text{ (current)} > d[u] + w(u,v) \text{ (via negative edge)}$$

**Bellman-Ford Solution**: Iteratively relax all edges $|V|-1$ times. Each iteration improves distances by considering all possible one-edge extensions:

$$\text{For iteration } i = 1 \text{ to } |V|-1:$$
$$\quad \text{For each edge } (u,v) \in E:$$
$$\quad\quad d[v] \leftarrow \min(d[v], d[u] + w(u,v))$$

After $|V|-1$ iterations, negative cycles (if any) are detectable by attempting one more relaxation that succeeds.

---

## Applications in Engineering

### 1. **Navigation and Routing**
- **GPS/Route planning**: Finding fastest/shortest routes in road networks (Google Maps, Waze)
- **Network routing protocols** (OSPF): Routers compute shortest paths to forward packets efficiently
- **Time-dependent routing**: Extensions for time-varying edge weights (rush hour traffic)

### 2. **Telecommunication Networks**
- **Cable/fiber routing**: Minimizing physical cable length between network nodes
- **Delay optimization**: Finding low-latency paths in packet-switched networks
- **Quality-of-service (QoS)**: Multi-metric shortest paths balancing bandwidth, jitter, and latency

### 3. **Supply Chain & Logistics**
- **Vehicle routing problems**: Computing cost-minimal delivery routes
- **Warehouse network optimization**: Shortest paths for inter-warehouse material flow
- **Inventory routing**: Time-weighted shortest paths accounting for holding costs

### 4. **Robotics & Autonomous Systems**
- **Path planning**: Shortest collision-free paths in configuration spaces (RRTs, Dijkstra in discretized state spaces)
- **Trajectory optimization**: Energy-minimal paths under kinematic constraints
- **Multi-robot coordination**: Shortest paths in conflict-avoidance graphs

### 5. **Electrical Engineering & Circuit Analysis**
- **Power grid optimization**: Minimum-loss power flow paths
- **VLSI routing**: Shortest interconnects in chip design (Steiner tree approximations)
- **Signal routing**: Minimum-delay wire routing in PCB layout

### 6. **Computational Biology**
- **Sequence alignment**: Edit-distance shortest paths (dynamic programming analog)
- **Protein folding**: Shortest paths in conformational energy landscapes
- **Phylogenetic tree construction**: Metric-based tree distances

---

## Common Mistakes / Pitfalls