# s-t paths

## Definition

An **s-t path** (or source-target path) is a sequence of vertices $\pi = (v_0, v_1, \ldots, v_k)$ in a directed graph $G = (V, E)$ where:
- $v_0 = s$ (source vertex)
- $v_k = t$ (target/sink vertex)
- $(v_i, v_{i+1}) \in E$ for all $i = 0, 1, \ldots, k-1$ (consecutive vertices are connected by edges)

The notation $s \rightsquigarrow t$ denotes the existence of at least one path from $s$ to $t$.

**Interior vertices** of an s-t path are all vertices except the endpoints: $\{v_1, v_2, \ldots, v_{k-1}\}$.

## Key Equations

### Vertex Distance (Weighted)

For a vertex-weighted graph with weight function $w: V \to \mathbb{R}^+$, the **weighted vertex distance** is:

$$\text{vdist}_w(s, t) = \min_{\pi: s \rightsquigarrow t} \sum_{v \in \text{interior}(\pi)} w(v)$$

where the sum includes only interior vertices of path $\pi$, **excluding the endpoints $s$ and $t$ themselves**.

### Vertex Distance (Unweighted)

When all vertices have uniform weight $w(v) = 1$:

$$\text{vdist}_G(s, t) = \min_{\pi: s \rightsquigarrow t} |\text{interior}(\pi)|$$

This equals the length of the shortest path minus 1 (excluding endpoints).

### Vertex Cut Bound

For a set $X \subseteq V$ that is a **vertex cut** for all pairs $(s,t)$ with $\text{vdist}_w(s,t) \geq 1$:

$$|X| \leq \tilde{O}\left(\langle\text{cost}, w\rangle \cdot \min\left\{n^{1/3}, w(V)^{1/2}\right\}\right)$$

where $w(V) = \sum_{v \in V} w(v)$ and $\langle\text{cost}, w\rangle = \sum_{v \in V} \text{cost}(v) \cdot w(v)$.

## Physical Intuition / Derivation

### Why Exclude Endpoints?

The definition excludes $s$ and $t$ from the distance calculation because:
1. **Flow-cut duality context**: In network flow problems, we want to find minimum vertex sets that separate source from sink; the source and sink themselves are trivial separators.
2. **Non-triviality**: A cut must contain at least one *interior* vertex to actually sever all paths, making $s$ and $t$ irrelevant to separation cost.

### Distance as Minimum Interior Cost

The weighted vertex distance captures the **least expensive interior obstruction** needed to block all s-t paths:
- If $\text{vdist}_w(s, t) = D$, then every path from $s$ to $t$ has interior weight $\geq D$
- Conversely, some path has interior weight exactly $D$
- This is the vertex-weighted analogue of edge-weighted shortest paths, but measuring path quality by interior vertices only

### Vertex Cuts and Separation

A vertex cut $X$ for pairs $(s, t)$ with $\text{vdist}_w(s, t) \geq 1$ means:
- For every such pair, **every** path $s \rightsquigarrow t$ contains at least one vertex from $X$ in its interior
- This guarantees separation: removing $X$ disconnects all sufficiently-far pairs
- The bound $|X| \leq \tilde{O}(w(V)^{1/2})$ shows we can achieve cuts using only $O(\sqrt{w(V)})$ total weight

## Applications in Engineering

### Network Design & Resilience
- **Graph partitioning**: Identify critical vertices whose removal disconnects distant components
- **Fault tolerance**: Design redundant paths by understanding minimum vertex separations
- **Network reliability**: Compute vertex connectivity and minimum cuts for robustness analysis

### Routing & Load Balancing
- **Multi-commodity flow**: Balance traffic across disjoint paths, where disjointness is measured by interior vertices
- **Traffic engineering**: Route around congested vertices by computing path diversity

### VLSI & Circuit Design
- **Gate-level analysis**: Vertices represent logic gates; s-t paths model signal propagation
- **Critical paths**: Identify interior gates (not input/output) on timing-critical paths
- **Partitioning**: Split circuits into manageable regions while bounding vertex boundaries

### Distributed Systems
- **Byzantine fault tolerance**: Find minimum sets of vertices that must be healthy to maintain connectivity
- **Consensus protocols**: Analyze message paths in distributed algorithms
- **Network protocols**: Ensure alternate paths exist through intermediate nodes only

## Common Mistakes / Pitfalls

### ❌ Confusing s-t paths with shortest paths
**Error**: Assuming shortest s-t path has minimal interior weight.
**Correction**: The shortest path (fewest edges) may have expensive interior vertices. Use Dijkstra on vertex weights, not edge count.

### ❌ Including endpoints in distance
**Error**: Computing $\text{vdist}(s, t) = $ sum of all vertices on shortest path.
**Correction**: Exclude $s$ and $t$; they are endpoints and don't contribute to the distance metric. Interior only: $\sum_{v \in \text{interior}(\pi)} w(v)$.

### ❌ Confusing vertex cuts with edge cuts
**Error**: Computing minimum edge cut and expecting it to bound vertex cut size.
**Correction**: These are fundamentally different: vertex cuts separate by removing vertices; edge cuts by removing edges. A vertex $v$ corresponds to removing all incident edges, but vertex cut bounds don't directly translate to edge cut bounds.

### ❌ Assuming zero-weight vertices don't matter
**Error**: Ignoring vertices with $w(v) = 0$ because they "don't contribute