# Adhesion Size

## Definition

**Adhesion size** is a graph-theoretic parameter that measures the maximum number of vertices shared between adjacent bags in a tree decomposition.

Formally, given a tree decomposition $\mathcal{T} = (T, \mathcal{B})$ of a graph $G$, where:
- $T$ is a tree with nodes representing bags
- $\mathcal{B}(v)$ denotes the bag (set of vertices) at node $v \in V(T)$

The **adhesion** of an edge $(u,v) \in E(T)$ connecting two adjacent bags is defined as:

$$\text{adhesion}(u,v) = |\mathcal{B}(u) \cap \mathcal{B}(v)|$$

The **adhesion size** of the entire decomposition is:

$$\text{adhesionSize}(\mathcal{T}) = \max_{(u,v) \in E(T)} |\mathcal{B}(u) \cap \mathcal{B}(v)|$$

## Key Equations

For a tree decomposition $\mathcal{T} = (T, \mathcal{B})$ of graph $G$:

**Adhesion bound vs. minor containment:**
If a graph $G$ has a tree decomposition with adhesion size $a$, then $G$ cannot contain a complete graph $K_n$ as a minor where $n > a + 1$ (assuming sufficient bag size).

**Relationship to treewidth:**
If a tree decomposition has treewidth $w$ (maximum bag size $w+1$) and adhesion size $a$, then:
$$a \leq w + 1$$

## Physical Intuition / Derivation

### Why Adhesion Matters

Tree decompositions break a complex graph into overlapping pieces (bags) arranged in a tree structure. The adhesion size quantifies how "tightly coupled" adjacent pieces are:

- **Small adhesion** ($a \ll w$): Bags are loosely connected; removing the intersection vertices would separate the graph into many components. This indicates the tree decomposition is *efficient* at decoupling the graph.

- **Large adhesion** ($a \approx w$): Bags overlap significantly; many vertices must be shared for connectivity. The decomposition provides less structural separation.

### Intuition from the Source Material

The excerpt demonstrates this principle: a tree decomposition with **bag size 6 and adhesion size 2** can constrain which minors appear in the graph. The key insight is:

If two disjoint vertex sets $X$ and $Y$ must remain connected via paths in $G$, then every bag on the unique tree path $P$ between them must be "hit" by these paths. If $|P|$ is long, the cumulative intersection sizes must account for the branching structure—limiting how many disjoint connections can exist.

Specifically, if three sets $R_1, R_2, R_3$ all need to reach two separated sets $L_i$ and $L_j$, they collectively require adhesions of size $\geq 4$ along the path—contradicting an adhesion limit of 2.

## Applications in Engineering

### 1. **Algorithm Design and Parameterized Complexity**
- Tree decompositions with controlled adhesion size enable dynamic programming algorithms on graphs with restricted structure
- Networks with small adhesion admit efficient routing and flow algorithms
- Used in VLSI design: small adhesion corresponds to few inter-layer connections

### 2. **Graph Minor Theory & Structural Graph Theory**
- Bounding adhesion is used to prove that certain graph families exclude specific minors (e.g., planar graphs exclude $K_5$ and $K_{3,3}$)
- Helps classify graph sparsity and design algorithms accordingly

### 3. **Network Reliability & Modularity**
- In communication networks, adhesion size relates to **network robustness**: small adhesion means few critical junction points
- Modules with small adhesion can be analyzed independently, reducing verification complexity

### 4. **Chordal Graph Recognition**
- Chordal graphs admit tree decompositions where adhesion equals treewidth (tight bound)
- Applied in compiler optimization and sparse matrix ordering

### 5. **Distributed Computing**
- Low-adhesion decompositions reduce inter-module message passing and synchronization overhead
- Enables partition-aware scheduling in distributed graph processing systems

## Common Mistakes / Pitfalls

### 1. **Confusing Adhesion with Bag Size**
**Mistake:** Treating adhesion size and treewidth interchangeably.

**Correction:** A decomposition with bag size $w+1$ can have adhesion anywhere from 1 to $w+1$. Small adhesion requires *extra* structure—not all decompositions achieve it.

### 2. **Assuming Minimal Adhesion is Always Better**
**Mistake:** Designing decompositions exclusively to minimize adhesion, ignoring bag size.

**Correction:** There's a tradeoff. Very small adhesion may force large bags. The relevant metric depends on the application (e.g., DP table size depends on bag size, not adhesion).

### 3. **Overlooking the Path Connectivity Requirement**
**Mistake:** Forgetting that small adhesion only constrains minors when the decomposition respects connectivity structure.

**Correction:** The adhesion argument works because graph connectedness forces the tree of bags to connect—this is a non-trivial property (Helly property for trees).

### 4. **Misapplying Minor Exclusion Bounds**
**Mistake:** Concluding that small adhesion alone excludes a minor, without considering bag size.

**Correction:** Both parameters matter. A graph with adhesion 2 but bag size 100 can still contain large minors. The constraint comes from the *combination* of structure and intersection sizes.

## See Also

- [[Treewidth]] — maximum bag size minus 1; principal measure of tree decomposition quality
- [[Tree Decomposition]] — the overarching framework defining adhesion
- [[Graph Minor]] — the structures that adhesion size helps exclude or constrain
- [[Graph Sparsity]] — structural property related to bounded treewidth and adhesion
- [[Dynamic Programming on Graphs]] — algorithms that exploit small adhesion for efficiency

## Sources

- Excerpt from pages 47 of graph decomposition analysis