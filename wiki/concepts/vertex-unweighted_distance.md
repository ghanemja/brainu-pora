# vertex-unweighted distance

## Definition

**Vertex-unweighted distance** (denoted $\text{vdist}_G(s, t)$) is the length of the shortest path between nodes $s$ and $t$ in a directed graph $G = (V, E)$, where every vertex traversal contributes equally to the path length. In contrast to edge-weighted distances (where edges carry costs), vertex-unweighted distance counts the number of vertices visited along a path.

Formally, for nodes $s, t \in V$:
$$\text{vdist}_G(s, t) = \min_{\text{paths } \pi: s \rightsquigarrow t} |\text{vertices in } \pi|$$

More precisely, in the context of **vertex-weighted distances** (a generalization), each vertex $v$ carries an associated weight $w(v) \geq 0$, and the distance becomes:
$$\text{vdist}_{G,w}(s, t) = \min_{\text{paths } \pi: s \rightsquigarrow t} \sum_{v \in \pi} w(v)$$

When $w(v) = 1$ for all $v$, this reduces to standard unweighted vertex distance.

## Key Equations

### Mass Function

The **mass function** quantifies the total accumulated vertex weights across all demand pairs and remaining vertices:

$$\text{mass}(\{w_{s,t}\}) := \sum_{(s,t) \in P} \sum_{v \in V \setminus X} w_{s,t}(v)$$

where:
- $P$ is the set of demand pairs (node pairs requiring path separation)
- $X$ is the set of already-selected cut vertices
- $w_{s,t}(v)$ is the weight assigned to vertex $v$ for demand pair $(s,t)$

### Random Level Cut Sampling

For a uniformly sampled threshold $d \in [0,1]$, a vertex $v$ is added to cut set $X$ if:

$$d \in \left[\text{vdist}_{s,t}(s, v), \text{vdist}_{s,t}(s, v) + w_{s,t}(v)\right)$$

This creates a probabilistic separation between vertices based on their vertex-weighted distances from source $s$.

## Physical Intuition / Derivation

### Why Vertex-Weighted Distances Matter

Consider a network (road system, circuit, communication network) where we care about **how many critical nodes** we must traverse, not how many edges. For instance:
- In a power grid, routing through high-congestion substations is expensive
- In communication networks, each relay/node may have a propagation delay or processing cost
- In social networks, passing through many intermediaries (vertices) adds latency

The vertex-unweighted version ($w(v) = 1/L$ for all $v$) treats all nodes uniformly, providing a baseline; vertex-weighted generalizations allow fine-grained control.

### Algorithm Intuition (VertexCut)

The algorithm iteratively identifies a **cut** (separator set $X$) that disconnects all demand pairs $(s,t)$ with $\text{vdist}_G(s,t) \geq L$ by:

1. **Assigning weights** to vertices based on current fractional min-cut solutions
2. **Epoch progression**: When fractional cuts become much cheaper (mass decreases by $\log n$ factor), increase the weight bound and recompute—this ensures we make progress
3. **Random level cut**: Sample a threshold $d$ uniformly, then add all vertices "crossed" by this threshold (in the vertex-distance metric from $s$) to the cut

The key insight: a random level cut in the vertex-distance landscape naturally separates $s$ from nodes at distance $\geq L$, with high probability.

### Why Vertex-Weighted Paths in Transitive Closure?

The source material notes a technical subtlety: to apply Min-Cost Max-Flow (MCMF) with upper-bounded vertex weights, one must allow paths in the **transitive closure** $G^* \setminus X$ (shortest paths through removed vertices) rather than direct edges in $G \setminus X$. This relaxation:
- Permits recovery of approximate min-cut witnesses
- Requires relaxing weight upper bounds by $O(1)$ factor
- Introduces parameter-balancing constraints

## Applications in Engineering

### Network Design & Routing
- **Node-disjoint path computation**: Finding multiple paths through a network that share no intermediate nodes; critical for fault tolerance in telecommunications
- **VPN/overlay networks**: Ensuring traffic passes through the minimum number of intermediaries (servers, proxies)

### Circuit Design
- **Vertex routing in VLSI**: Minimizing the number of logic cells or gates traversed by critical signals
- **Heat dissipation**: Routing signals through fewer intermediate nodes reduces cumulative thermal loading

### Social Network Analysis
- **Information diffusion**: Computing the minimum number of "hops" (people) needed to propagate information
- **Influencer identification**: Finding nodes that lie on many shortest (vertex-unweighted) paths

### Transportation & Logistics
- **Truck routing**: Minimizing stops/intermediate points (warehouses, hubs) rather than pure distance
- **Disaster response**: Identifying critical junction nodes that must remain accessible

### Graph Partitioning for Distributed Computing
- **Load balancing**: Cutting a computation graph to minimize the number of process-node boundaries crossed

## Common Mistakes / Pitfalls

### 1. Confusing Vertex-Unweighted with Edge-Unweighted Distance
- **Mistake**: Using Dijkstra's shortest path algorithm directly on $G$ without marking vertex cost
- **Correct approach**: Convert to an edge-weighted graph where each vertex $v$ becomes two nodes ($v_{\text{in}}, v_{\text{out}}$) with edge $(v_{\text{in}} \to v_{\text{out}})$ carrying $w(v)$

### 2. Ignoring the Transitive Closure Requirement
- **Mistake**: Assuming all paths must use only direct edges in $G \setminus X$
- **Correct approach**: In theoretical analyses (like MCMF witnesses), paths can use shortcuts through removed vertices; this is captured