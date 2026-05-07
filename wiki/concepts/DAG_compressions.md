# DAG Compressions

## Definition

A **DAG compression** (Directed Acyclic Graph compression) is a graph compression scheme that represents a dense or complex graph $G = (V, E)$ through a hierarchical abstraction using three components:

$$\text{DAG compression of } G = (V, A, E)$$

where:
- **$V$** = set of **compression nodes** (abstract modules representing clusters of original vertices)
- **$A$** = set of **containment edges** forming a directed acyclic graph that defines the hierarchical nesting structure of modules
- **$E$** = set of **compressed edges** (edges between modules that represent groups of edges in the original graph)

The compression is valid when:
- The containment DAG $A$ defines a partial order on compression nodes
- Each compressed edge in $E$ represents one or more actual edges in the original graph
- The structure is lossless: the original graph can be exactly reconstructed

A key distinction from **tree compressions** is that containment relationships form a DAG rather than a tree, allowing **cross-hierarchy relationships** that tree structures cannot express. This relaxation enables more compact representations for certain graph families.

## Key Equations & Metrics

**Compression size** (total encoding cost):
$$\text{Cost} = |A| + |E|$$

where the trade-off between edges in the containment structure ($|A|$) and compressed representation edges ($|E|$) is central to optimization.

**Minimization problem** (NP-hard):
$$\text{min-dag-compression}: \text{Does } G \text{ admit compression } (V, A, E) \text{ with } |A| + |E| \leq k?$$

**Key complexity result**: It is **NP-hard** to decide whether a graph admits a DAG compression with $|E| \leq k$ (minimizing compression edges alone).

## Physical Intuition / Derivation

### Motivation: From Trees to DAGs

Tree compressions impose a strict hierarchical constraint: if two modules overlap, one must be completely contained within the other. This tree structure is provably insufficient for some graphs.

**Example**: The **rook graph** (vertices arranged as an $n \times n$ grid where row and column vertices are connected) has:
- A linear-size DAG compression
- **No known** linear-size tree compression

The intuition is that a rook graph has natural bipartite structure (rows and columns) that cross-cuts hierarchy. A DAG allows modules to participate in multiple containment relationships simultaneously, capturing this structure efficiently.

### Why DAG > Tree

When the containment structure must be a tree:
- Each module has at most one "parent"
- Vertices can only be organized along a single hierarchical dimension
- Some multi-dimensional groupings force redundant module expansion

When containment forms a DAG:
- Modules can have **multiple predecessors** in the partial order
- Allows orthogonal structural dimensions to coexist
- Reduces total encoding at the cost of more complex bookkeeping

## Applications in Engineering

### 1. **Graph Visualization & Knowledge Representation**
- **Power graphs** (predecessor concept) use similar module-based abstraction for visualizing dense networks
- DAG compressions provide compact visual hierarchies for network topology, software architecture diagrams, and dependency graphs
- Engineers can abstract complex interconnections into manageable levels of detail

### 2. **Minimum Spanning Tree Computation**
- DAG compressions enable **more efficient MST algorithms** (cited as Theorem 1.2 application)
- Useful in network design, circuit routing, and infrastructure planning where optimal spanning trees minimize total cost while maintaining connectivity

### 3. **Network & Software Architecture**
- Representing hierarchical systems where components have cross-cutting concerns
- Example: microservice architectures where services may belong to multiple logical layers/domains simultaneously
- Enables identification of redundant dependencies and structural optimization

### 4. **Data Compression in Knowledge Graphs**
- Compressing knowledge bases, ontologies, and semantic networks
- Reduces storage while maintaining queryability
- Applies to RDF graphs, property graphs in graph databases

### 5. **Circuit Design & Hierarchical Schematics**
- Compressing large circuit netlists where functional blocks may relate to multiple organizational hierarchies
- Supports design at multiple abstraction levels

## Common Mistakes / Pitfalls

### 1. **Confusing Optimization Objectives**
- **Mistake**: Assuming minimizing $|E|$ (compression edges) is equivalent to minimizing total cost $|A| + |E|$
- **Reality**: The source material emphasizes this is "not really the question"—encoding the containment structure $A$ is expensive. Minimizing edges at the cost of complex hierarchies may increase overall encoding
- **Lesson**: Always optimize the full encoding cost, not just one component

### 2. **Assuming DAG Compressions are Always Better**
- **Mistake**: Treating DAGs as a strict generalization that always improves upon trees
- **Reality**: DAG compressions have higher **computational overhead** (NP-hard optimization) and more complex bookkeeping. Tree compressions may be preferable when applicable
- **Lesson**: Use DAGs only when tree structure provably inadequate for your graph family

### 3. **Conflating Twin-Width with DAG-Compressibility**
- **Mistake**: Assuming graphs with bounded twin-width have linear-size DAG compressions (or vice versa)
- **Reality**: Bounded twin-width implies linear tree compression, but the rook graph has linear DAG compression *without* bounded twin-width
- **Lesson**: These are distinct structural properties; test each independently

### 4. **Underestimating NP-Hardness Implications**
- **Mistake**: Viewing NP-hardness of min-dag-compression as a minor computational hurdle
- **Reality**: Finding optimal DAG compressions requires approximation algorithms or heuristics in practice; no polynomial-time exact solution exists (unless P=NP)
- **Lesson**: Plan for heuristic/greedy approaches in engineering applications

### 5. **Ignoring Reconstruction Overhead**
- **Mistake**: Optimizing compression size without considering cost to **decompress** and reconstruct the original graph
- **Lesson**: In applications requiring frequent decompression, balance compression ratio against reconstruction time

## See Also

- [[Tree Compressions]]: Predecessor model with strict hierarchical (tree) containment constraints
-