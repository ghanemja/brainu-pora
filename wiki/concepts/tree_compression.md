# Tree Compression

## Definition

**Tree compression** is a graph data structure technique for storing dense graphs efficiently by organizing vertex clusters into a tree-like hierarchy. Formally, a tree compression of a graph $\mathbf{G} = (\mathbf{V}, \mathbf{E})$ is a triple $D = (V, A, E)$ where:

- $(V, A)$ is a **rooted tree** (a special case of a directed acyclic graph) whose leaf nodes are exactly the vertices in $V \subseteq \mathbf{V}$
- Each node $v \in V$ in the tree represents a **cluster** $C_D(v) \subseteq \mathbf{V}$, typically defined as the set of original vertices contained in the subtree rooted at $v$
- $E \subseteq V \times V$ is a set of **compression edges** that encode the edges of the original graph: for each edge $(\mathbf{u}, \mathbf{v}) \in \mathbf{E}$ where $\mathbf{u} \in C(u)$ and $\mathbf{v} \in C(v)$, there exists a compression edge $(u, v) \in E$

The tree structure imposes a hierarchical constraint where clusters form a tree-like nesting relationship, making tree compressions particularly suitable for graphs with natural hierarchical structure (e.g., social networks, biological systems, organizational structures).

## Key Equations

### Compression Ratio

The **compression ratio** measures how effectively a tree compression reduces the original graph:

$$\text{Compression Ratio} = \frac{|E| + |V|}{|\mathbf{E}| + |\mathbf{V}|}$$

where $|E|$ and $|V|$ represent the size of the compressed representation, and $|\mathbf{E}|$ and $|\mathbf{V}|$ represent the original graph size.

### Cluster Definition (Hierarchy-based)

For a tree compression where $v \in V$ is a node, the cluster is recursively defined:

$$C(v) = \begin{cases} 
\{\mathbf{v}\} & \text{if } v \text{ is a leaf} \\
\bigcup_{c \in \text{children}(v)} C(c) & \text{if } v \text{ is internal}
\end{cases}$$

## Physical Intuition / Derivation

Tree compression exploits the observation that real-world graphs often exhibit **hierarchical structure**: vertices naturally group into clusters, clusters group into larger meta-clusters, and so forth. Rather than storing all $O(|\mathbf{V}|^2)$ possible edges, we store:

1. A **tree skeleton** that captures the hierarchical organization ($O(|\mathbf{V}|)$ nodes and edges)
2. **Inter-cluster edges** that connect distinct clusters ($O(|E|)$ edges, typically much smaller than $|\mathbf{E}|$ for dense graphs)

### Building Intuition with an Example

Consider a road network with cities organized by region → state → nation:
- **Original graph**: Every city connected to every nearby city (dense edge set)
- **Tree compression**: Organize cities into regional clusters, states into regional super-clusters, etc.
- **Compression edges**: Rather than store all city-to-city connections, store region-to-region and state-to-state connections
- **Retrieval**: To find if city A connects to city B, traverse the tree to find their lowest common ancestor and check compression edges

### Why Trees (Not General DAGs)?

Trees enforce a **unique path to the root** for each cluster, which guarantees:
- Unambiguous hierarchical membership
- Linear reconstruction time (no need to check multiple paths)
- Straightforward dynamic updates when edges/vertices change

This constraint makes trees simpler and more efficient than general DAG compressions for many practical scenarios, though the research material notes that general DAG compressions can achieve better compression ratios in specific cases.

## Applications in Engineering

### Computer Networks
- **Subnetting and hierarchical routing**: Organize IP addresses/routers into tree-structured clusters (similar to tree compression), reducing routing table sizes
- **Network monitoring**: Compress traffic flow graphs between data centers, regions, and individual servers

### Social Network Analysis
- **Community detection**: Organize users into hierarchical communities (friend groups → neighborhoods → regions) and compress inter-community edges
- **Privacy-preserving analytics**: Release compressed graphs instead of full social networks, protecting individual relationships while preserving macro-scale statistics

### Biological Networks
- **Protein interaction networks**: Organize proteins into functional modules (proteins → complexes → pathways) and store only inter-module interactions
- **Metabolic pathway compression**: Store pathways hierarchically to reduce storage and speed up pathway analysis

### VLSI Circuit Design
- **Hierarchical netlist compression**: Modern chips have millions of gates organized into hierarchical modules; tree compression reduces netlist size for verification and simulation
- **Timing analysis**: Propagate timing constraints through compressed module hierarchy rather than gate-by-gate analysis

### Data Indexing and Databases
- **XML/JSON document compression**: Compress document trees with cross-references (compression edges) between distant nodes
- **Knowledge graphs**: Organize entities hierarchically and compress relationships between entity clusters

## Common Mistakes / Pitfalls

### 1. **Assuming Trees Are Always Better Than General Graphs**
Students often think tree compressions are optimal. However, the source material proves that **DAG compressions (which allow multiple paths) can achieve better compression ratios**. Trees trade optimality for simplicity and computational efficiency.

### 2. **Confusing Clusters with Connected Components**
A cluster $C(v)$ is *not* necessarily a connected subgraph of the original graph—it's defined topologically by the tree hierarchy. Many algorithms require explicitly checking which original vertices are in a cluster.

### 3. **Overlooking Dynamic Update Costs**
When edges are added/deleted, the optimal tree compression may change completely. Incrementally updating the tree can be expensive. Students should not assume that tree compressions remain small or efficient under frequent updates.

### 4. **Forgetting to Check Compression Edges**
When answering queries like "does an edge exist between vertex $\mathbf{u}$ and $\mathbf{v}$?", you must:
   - Find the clusters $C(u)$