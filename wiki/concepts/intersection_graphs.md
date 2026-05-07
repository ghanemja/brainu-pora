# intersection graphs

## Definition

An **intersection graph** is a graph $G = (V, E)$ where:
- Each vertex $v \in V$ corresponds to a geometric object (set, region, disk, etc.)
- Two vertices $u$ and $v$ are connected by an edge if and only if their corresponding objects intersect

More formally, given a collection of objects $\mathcal{O} = \{O_1, O_2, \ldots, O_n\}$ in some geometric space, the intersection graph $G(\mathcal{O})$ has:
- Vertex set: $V = \{v_1, v_2, \ldots, v_n\}$ (one per object)
- Edge set: $(v_i, v_j) \in E \iff O_i \cap O_j \neq \emptyset$

**Specialized cases:**
- **Unit disk graphs**: Objects are disks of identical radius $r$ in $\mathbb{R}^2$
- **Interval graphs**: Objects are intervals on the real line
- **Chordal graphs**: Intersection graphs of subtrees of a tree
- **Fat objects with cell partition**: Objects that are "similarly sized" with bounded aspect ratio, partitioned into regions

## Key Equations

**Clique size bound in cell partitions:**
For an intersection graph $G \in I_\alpha$ with cell partition $\mathcal{P}$, if each clique $C \in \mathcal{P}$ has maximum size $|C| \leq \ell$, then for integer $k$, vertices can be decomposed into $k$ sets $X_1, \ldots, X_k$ such that:

$$\sum_{i=1}^k |X_i| = O(|\mathcal{P}| \cdot \ell)$$

and the resulting contracted graphs satisfy:
$$\text{tw}(G/X_i) = O(k\ell)$$

where $\text{tw}$ denotes treewidth.

**Lipschitz embedding condition:**
A mapping $f: V(G) \to V(H)$ is $c$-Lipschitz if:

$$\frac{1}{c} \cdot \text{dist}_G(x,y) \leq \text{dist}_H(f(x), f(y)) \leq c \cdot \text{dist}_G(x,y)$$

for all pairs of vertices $x, y$.

## Physical Intuition / Derivation

### Why Intersection Graphs?

Many real-world problems naturally encode relationships as geometric overlaps:
- **Network design**: Nodes represent service regions; edges connect overlapping coverage areas
- **Scheduling**: Tasks represented as time intervals; conflicts arise when intervals intersect
- **Sensor networks**: Sensors have detection ranges; communication edges connect overlapping ranges

### Why Cliques Matter

In an intersection graph, a **clique** (complete subgraph) corresponds to a set of objects that mutually intersect. For objects embedded in Euclidean space with bounded aspect ratio, Helly's theorem and packing arguments bound the maximum clique size, making the problem tractable.

### The Contraction Decomposition Strategy

The excerpt describes a sophisticated algorithmic approach:

1. **Start with intersection graph $G$**: Vertices are fat objects, edges represent intersection
2. **Construct dual structure $G_\mathcal{P}$**: Each clique in the partition becomes a vertex
3. **Embed into planar graph $H$**: Use Lipschitz embedding to preserve both distance structure and contraction properties
4. **Apply contraction decomposition**: Find sets $X_i$ whose contraction yields bounded treewidth
5. **Lift back to original graph**: Each contracted region in $H$ maps to a clique-union in $G$

The **delicate balance** in choosing $H$:
- Too many edges → contracting a small set doesn't correspond to small contraction in $G$
- Too few edges → small treewidth in $H$ doesn't guarantee small treewidth in $G$ after lifting

Lipschitz embeddings preserve this balance by maintaining distance structure with controlled distortion factor $c$.

## Applications in Engineering

### 1. **Computational Geometry & CAD**
- Detecting part interference in mechanical assemblies
- Collision detection in robotics and animation
- Spatial data indexing and range queries

### 2. **Network Design & Optimization**
- Wireless sensor network coverage optimization
- Facility location with overlapping service regions
- Approximation algorithms for Steiner trees on intersection graphs

### 3. **Scheduling & Resource Allocation**
- Interval scheduling (intersection graphs of time intervals)
- Graph coloring for task scheduling with resource conflicts
- Register allocation in compilers

### 4. **Bioinformatics**
- Protein interaction networks (modeled as geometric intersections)
- DNA sequence alignment visualization
- Phylogenetic tree construction

### 5. **VLSI & Circuit Design**
- Wire routing with overlap avoidance
- Gate placement and floorplanning
- Signal integrity analysis

## Common Mistakes / Pitfalls

1. **Assuming all graphs are intersection graphs**: Not every abstract graph is realizable as an intersection graph of geometric objects. Realizability is a strong structural constraint.

2. **Confusing cliques with maximal cliques**: A clique in an intersection graph is any set of mutually intersecting objects; a *maximal* clique is one that cannot be extended. Cell partitions exploit maximal clique structure.

3. **Underestimating aspect ratio dependence**: When objects are not "similarly sized" or have large aspect ratios, theoretical bounds degrade rapidly. The $O(k\ell)$ treewidth depends critically on object homogeneity.

4. **Ignoring embedding quality**: A $c$-Lipschitz embedding with large constant $c$ may preserve distances but still distort contraction effects. The constant $c$ directly affects algorithmic complexity.

5. **Treating unit disk graphs as general case**: While unit disk graphs are well-studied, many theoretical results (contraction decompositions, planar spanners) don't extend directly to arbitrary fat objects without careful re-derivation.

6. **Forgetting the role of cell partitions**: The partition $\mathcal{P}$ is not arbitrary—it induces structure that makes the contraction decomposition possible.