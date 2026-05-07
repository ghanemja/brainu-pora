# Min Cuts

## Definition

A **min cut** (minimum cut) is a partition of the vertices of a graph $G = (V, E)$ into two disjoint sets $S$ and $T = V \setminus S$ that minimizes the total weight of edges crossing the partition boundary.

More formally, given a directed graph $G = (V, E)$ with edge weights $w_e \geq 0$, a cut separating source $s$ from sink $t$ is a subset $X \subseteq V$ such that $s \in X$ and $t \notin X$. The **capacity** of this cut is:

$$\text{cap}(X) = \sum_{(u,v) \in E: u \in X, v \notin X} w(u,v)$$

The **minimum cut** for a pair $(s,t)$ is the cut $X^*$ that minimizes this capacity.

### Vertex-Weighted Min Cuts

In **vertex-weighted** variants (as discussed in the source material), each node $v$ has an associated weight $w(v)$. A vertex cut separates $s$ and $t$ by removing a set of vertices $X$ from the graph. The cost is:

$$\text{cost}(X) = \sum_{v \in X \setminus \{s\}} w(v)$$

This is equivalent to the edge-weighted problem on an expanded graph where each vertex $v$ is replaced by an edge of weight $w(v)$.

## Key Equations

**Max-Flow Min-Cut Theorem** (classical):
$$\text{min cut capacity} = \text{max flow value}$$

**Fractional Min Cut**: A fractional weight assignment $w'_{s,t}$ is a minimum fractional $(s,t)$-cut if it solves:
$$w'_{s,t} = \arg\min_{w} \sum_{v \in V} w(v) \quad \text{subject to: } w \text{ separates } s \text{ from } t$$

This can be computed via linear programming and satisfies the dual of the maximum flow LP.

**Mass Function** (from Algorithm 2):
$$\text{mass}(\{w_{s,t}\}) := \sum_{(s,t) \in P} \sum_{v \in V \setminus X} w_{s,t}(v)$$

The mass function aggregates weights across all demand pairs and measures progress toward a valid cut.

## Physical Intuition / Derivation

Min cuts arise naturally when asking: *"What is the minimum capacity I must remove to disconnect source from sink?"*

### Why This Matters

1. **Bottleneck Analysis**: In flow networks (pipes, traffic, data), the min cut identifies the system's capacity bottleneck.

2. **Duality with Flows**: By max-flow min-cut, computing maximum flow also reveals the minimum cut capacity.

3. **Vertex vs. Edge Weights**: Vertex weights model node failures or processing costs (routers, servers), while edge weights model link capacity or distance.

### Algorithmic Approach (From Source Material)

The **VertexCut algorithm** incrementally constructs a vertex cut $X$ through:

1. **Weighted Distance Sampling**: For each demand pair $(s,t)$, maintain vertex weights $w_{s,t}(v)$ representing the "thickness" of each node along paths from $s$ to $t$.

2. **Epoch-Based Refinement**: When the aggregated mass across all pairs decreases significantly (by factor $\log n$), increase the epoch parameter and refine the weight bounds.

3. **Random Level Cuts**: Sample a threshold $d$ uniformly from $[0,1]$ and cut all nodes $v$ whose "distance interval" $[\text{vdist}_{s,t}(s,v), \text{vdist}_{s,t}(s,v) + w_{s,t}(v))$ contains $d$.

**Key Insight**: The random sampling ensures that paths from $s$ to $t$ are likely to hit the cut, while the epoch-based weight updates ensure the cut respects all demand pairs approximately simultaneously.

## Applications in Engineering

### Network Design & Reliability
- **Telecommunications**: Identify critical links whose failure disconnects networks; plan redundancy accordingly.
- **Power Grids**: Find minimum transmission line removals that isolate substations.

### Computer Networks
- **Data Center Topology**: Compute bisection bandwidth—the min cut that partitions servers into equal-sized groups. Critical for cluster scheduling.
- **SDN Routing**: Min cuts inform traffic engineering and bottleneck detection.

### Machine Learning & Clustering
- **Graph Clustering**: Use min cut to partition graphs while minimizing inter-cluster edges (normalized cut objectives).
- **Image Segmentation**: Treat pixels as nodes; min cuts identify object boundaries by minimizing edge weights across regions.

### VLSI & Chip Design
- **Circuit Partitioning**: Minimize wires crossing chip partitions to reduce interconnect delay and power.

### Logistics & Supply Chain
- **Network Flow Optimization**: Min cuts identify capacity constraints in supply networks (warehouses, shipping routes).

## Common Mistakes / Pitfalls

1. **Confusing Min Cut with Shortest Path**: The min cut is a *partition*, not a path. A minimum cut may remove many nodes simultaneously, not a single cheapest edge/node.

2. **Assuming Uniqueness**: Min cuts are rarely unique. Many different partitions can achieve the same minimum capacity. The algorithm returns one valid cut, not "the" cut.

3. **Ignoring Edge Direction**: In directed graphs, $(u,v)$ and $(v,u)$ are different edges. A cut separating $s \to t$ need not separate $t \to s$.

4. **Vertex vs. Edge Weights**: Forgetting that vertex weights require graph expansion (splitting each vertex into in/out edges). A vertex-weighted problem is not directly solved by applying edge-weighted min-cut algorithms.

5. **Weight Upper Bounds**: In the source algorithm, relaxing node weight bounds to $\tilde{O}(1/L)$ (rather than fixed weights) is crucial. Overly heavy nodes prevent the MCMF (Min-Cost Max-Flow) theorem from applying directly—this required introducing paths in the transitive closure.

6. **Assuming Paths Remain in $G