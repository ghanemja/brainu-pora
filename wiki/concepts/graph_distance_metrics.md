# Graph Distance Metrics

## Definition

Graph distance metrics quantify the shortest-path distance between vertices or sets of vertices in a graph. In the context of planar graph decomposition, **boundary distance** measures how far a vertex is from the boundary (periphery) of a decomposed region.

Formally, for a vertex $v$ in a subgraph $G|R$ (induced subgraph on region $R$):

$$\text{dist}_{R}(v, S) = \text{length of shortest path from } v \text{ to set } S \text{ in } G|R$$

A vertex $v$ is **boundary-distant** (relative to region $R$) if:

$$\text{dist}_{R}(v, V(\text{South}(R) \cup \text{North}(R))) > \lambda$$

where $\lambda = 1/\varepsilon^{7.5}$ is a distance threshold, and South$(R)$ and North$(R)$ denote the southern and northern boundary vertices of region $R$.

## Key Equations

**Distance from vertex to boundary set:**
$$d(v, \partial R) = \min_{u \in \partial R} \text{dist}_R(v, u)$$

**Monotonicity under graph expansion:**
If $R' \subset R$ and $v \in V(R')$ with $S \subseteq V(R')$:
$$\text{dist}_{R'}(v, S) \leq \text{dist}_{R}(v, S)$$

This inequality is fundamental: distances can only decrease or stay the same when restricting to a subgraph.

**Bridge decomposition cost bound (Lemma 9.4):**
$$\sum_{i=1}^{t-1} \text{length}(e_{P_i}) = O\left(t\right) = O\left(\frac{|\text{South}(R)|}{\sqrt{\lambda}}\right) = O(\varepsilon^2 |\text{South}(R)|)$$

## Physical Intuition / Derivation

### Why Distance Metrics Matter in Decomposition

When decomposing a planar region into smaller subregions using "bridges" (separating paths), a key goal is to identify which regions actually need to be separated. Two consecutive regions $R'$ and $R''$ can be **merged** without loss of information if neither contains a vertex that is truly "interior" (far from boundaries).

The intuition:
- A **boundary-distant vertex** is one that is "deep" within a region, far from edges where it might interact with adjacent regions
- If a vertex $v$ has distance $> \lambda$ to the boundary, then $v$ is sufficiently isolated that it cannot "see" across a bridge path of length $O(\lambda)$
- Therefore, removing the bridge doesn't change connectivity properties of sufficiently interior vertices

### The Greedy Bridge Construction

The algorithm constructs bridges greedily from west to east:
1. Start with an initial trivial bridge $P_1$ at vertex $v$
2. For each subsequent bridge $P_{i+1}$, find the first vertex on the southern boundary whose objects are **disjoint** from previous bridges
3. This ensures bridges don't overlap and form a well-defined ordering

The distance threshold $\lambda = 1/\varepsilon^{7.5}$ (where $\varepsilon$ is some decomposition parameter) is chosen large enough that:
$$\lambda > 10 \quad \text{(neighborhood radius of bridge starting points)}$$

This ensures vertices within the bridge neighborhood cannot be boundary-distant in the merged region.

### Why $O(t) = O(\varepsilon^2 |\text{South}(R)|)$

Among $t$ regions, at least $\lfloor t/2 \rfloor$ must contain boundary-distant vertices (property **Bdg2**). Each such region requires "expensive" bridges that intersect eastern or western bridge objects (property **Bdg1**). Since bridges are disjoint and limited by the southern boundary size, the total bridge cost scales as $O(\varepsilon^2 |\text{South}(R)|)$.

## Applications in Engineering

### 1. **Planar Embedding & VLSI Layout**
Distance metrics guide the decomposition of circuit regions. Vertices (gates/components) far from region boundaries can be processed independently, reducing cross-region communication delays.

### 2. **Mesh Generation & Finite Element Analysis**
In computational geometry, boundary distance determines when a mesh region is "well-shaped." Vertices near boundaries need special treatment (refinement, boundary conditions), while interior vertices ($d > \lambda$) can use uniform approximation.

### 3. **Routing & Network Design**
Graph distance metrics compute hop counts in network routing. Critical paths must be identified early; boundary-distant nodes can use standard routing, while boundary-proximal nodes need careful handling to minimize congestion.

### 4. **Shortest Path Algorithms**
Graph distance metrics are fundamental to Dijkstra, Bellman-Ford, and A* algorithms. The monotonicity property (distances decrease on subgraphs) justifies pruning strategies in hierarchical routing.

### 5. **Clustering & Community Detection**
Vertices with small mutual distances form tight clusters. Distance-based clustering (k-means on metric space, single-linkage clustering) relies on well-defined graph metrics.

## Common Mistakes / Pitfalls

### ❌ **Mistake 1: Confusing graph distance with Euclidean distance**
Graph distance $\text{dist}_G(u, v)$ counts edges in the shortest path, *not* geometric distance in the plane. A planar graph with short Euclidean distances can have large graph distances if edges are sparse.

**Correct approach:** Always specify the graph and metric clearly. For planar regions, distinguish between $\text{dist}_R$ (in subgraph) and $\text{dist}_{R'}$ (in super-region).

### ❌ **Mistake 2: Assuming distance preservation across graph union**
Students often believe $\text{dist}_R(u,v) = \text{dist}_{R \cup R'}(u,v)$. **This is false!** Distances can decrease when adding new edges.

**Correct approach:** Use the monotonicity inequality: distances are non-increasing when going to larger graphs.

### 