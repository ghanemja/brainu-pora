# Dynamic Programming on Tree Decomposition

## Definition

Dynamic programming on tree decomposition (DPTTD) is an algorithmic technique for solving graph problems by exploiting the *treewidth* structure of a graph. Given a tree decomposition of a graph $G$ with treewidth $t$, we recursively compute solutions by processing nodes in the decomposition tree, maintaining **state information** about how partial solutions interact across bag boundaries.

More formally: A tree decomposition of graph $G = (V, E)$ is a pair $(T, \mathcal{B})$ where:
- $T$ is a tree with nodes called **bags**
- $\mathcal{B} = \{B_i : i \in V(T)\}$ is a collection of subsets $B_i \subseteq V$

satisfying:
1. $\bigcup_{i \in V(T)} B_i = V$ (coverage)
2. For each edge $(u,v) \in E$, there exists a bag $B_i$ containing both $u$ and $v$
3. For each vertex $v$, the set of bags containing $v$ forms a connected subtree

The **treewidth** $\text{tw}(G)$ is the minimum $t$ such that a tree decomposition exists with all bags of size at most $t+1$.

## Key Equations

**Running time for a problem on bounded treewidth graphs:**

$$T(n, t) = 2^{\tilde{O}(t)} \cdot n^{O(1)}$$

where $\tilde{O}(\cdot)$ suppresses logarithmic factors.

**State space complexity:** If the local problem at each bag maintains states characterizing interactions with neighboring bags:

$$|\text{States per bag}| = 2^{\tilde{O}(t)}$$

**Subexponential algorithm existence (Nederlof's insight):** For problems with connected solutions $Z$ that are local to $G[Z]$:

$$T(n, k) = 2^{\tilde{O}(\sqrt{k})} \cdot n^{O(1)}$$

This is achieved by finding separators where the solution intersects in $\tilde{O}(\sqrt{k})$ vertices, leading to $2^{\tilde{O}(\sqrt{k})}$ possible intersection types.

## Physical Intuition / Derivation

### Why Tree Decomposition?

Graphs with small treewidth have a **recursive structure**: they can be decomposed into overlapping subgraphs that interact only through small boundaries. This mirrors many real-world networks (biological, social, planar) which have low treewidth.

### The DP Strategy

1. **Root the decomposition tree** at an arbitrary bag.

2. **Define states** at each bag $B_i$: These encode all "relevant information" needed to:
   - Solve the problem on the subtree rooted at $B_i$
   - Extend the solution upward to the parent bag

3. **Bottom-up recurrence:** Process leaves-to-root. For a bag $B_i$ with children $\text{child}_1, \ldots, \text{child}_m$:
   - Combine states from all children
   - Add constraints from vertices/edges in $B_i$ only
   - Eliminate internal vertices not in the parent bag

4. **Elimination (Join operation):**
   When combining two subtrees through bag $B_i$, vertices that appear only in $B_i$ (not in parent) are "summed out":
   
   $$\text{DP}[i] = \bigcup_{c \in \text{children}(i)} \text{DP}[c] \quad \text{(optimally merged)}$$

### Example: Longest Path

For finding longest path with state space $2^{|B_i|}$ configurations of endpoints within a bag:
- Each state tracks: "which vertices in $B_i$ are path endpoints in this partial solution?"
- Merging two subtrees: connect compatible endpoint configurations
- **Complexity:** $2^{O(t)} \cdot n$ time

### Why This Avoids Exponential Blowup

Instead of exploring all $2^n$ subsets, we only explore $2^t$ states per bag. Since there are $O(n)$ bags, total time is $2^{O(t)} \cdot n^{O(1)}$ rather than $2^n$.

## Applications in Engineering

### 1. **Compiler Optimization & Program Analysis**
- Control-flow graphs of typical programs have bounded treewidth
- DPTTD used to compute data-flow facts (live variables, reaching definitions) efficiently
- Eliminates quadratic-time iterative dataflow analysis for structured code

### 2. **VLSI Circuit Design**
- Netlist hypergraphs model interconnect structure
- Tree decomposition reveals hierarchical modularity
- DP algorithms optimize wire routing and timing closure on subgraphs

### 3. **Biological Network Analysis**
- Protein interaction networks, phylogenetic trees have low treewidth
- Identifying conserved motifs, clique detection via DPTTD
- Significantly faster than general algorithms on dense networks

### 4. **Constraint Satisfaction Problems (CSPs)**
- Tree decomposition of constraint graphs enables efficient constraint propagation
- Used in SAT/SMT solvers for structured instances
- Dynamic programming computes satisfying assignments efficiently

### 5. **Decoding & Channel Codes**
- Tanner graphs (bipartite graphs for LDPC/turbo codes) have small treewidth
- DPTTD provides efficient belief propagation decoder
- Polynomial time decoding for certain code families

### 6. **Natural Language Processing**
- Dependency parse trees have bounded treewidth
- Semantic role labeling via tree DP
- More efficient than general structured prediction

## Common Mistakes / Pitfalls

### 1. **Confusing Treewidth with Tree-structuredness**
**Mistake:** Assuming $\text{tw}(G) = 1$ means $G$ is a tree.  
**Reality:** $\text{tw}(G) = 1$ means $G$ is a *forest* (disjoint union of trees). A tree has $\text{tw} = 1$, but a cycle has $\