# Hasse diagram

## Definition

A **Hasse diagram** is a directed acyclic graph (DAG) that visualizes the partial order of a poset (partially ordered set) by representing elements as vertices and drawing a directed edge from $a$ to $b$ if $a < b$ and there is no $c$ with $a < c < b$ (i.e., the relation is immediate/covering).

In the context of topological complexes and computational topology, the Hasse diagram of a simplicial or cell complex $Y$ represents the **face lattice**: vertices correspond to cells (simplices) of all dimensions, and edges encode the inclusion relation between cells. The **width** (or **treewidth**) of a Hasse diagram measures the maximum complexity of the partial order structure.

### Formal characterization

For a complex $Y$:
- Each cell/simplex is a node in the Hasse diagram
- An edge $\sigma \to \tau$ exists if $\sigma \subsetneq \tau$ and $\dim(\tau) = \dim(\sigma) + 1$ (immediate covering)
- The **treewidth** of the Hasse diagram bounds the "tree-like" structure of this poset: a tree decomposition of width $k$ means the partial order can be decomposed into overlapping bags of size $\leq k+1$ arranged in a tree structure

## Key Equations

**Treewidth preservation under gadget construction:**

If a directed graph $D$ has treewidth $k$, then a complex $Y$ built from $D$ using the Width-Preserving Strategy (WiPS) satisfies:

$$\text{tw}(\text{Hasse}(Y)) \leq c \cdot k + c'$$

where $c, c'$ are fixed constants independent of $D$ and $|Y|$ remains polynomial in $|D|$.

**Complexity scaling (optimal):**

For Optimal Morse Matching (OMM) on Hasse diagrams of treewidth $k$:

$$T(n, k) = 2^{\Theta(k \log k)} \cdot n^{O(1)}$$

This bound is tight under the Exponential Time Hypothesis (ETH).

## Physical Intuition / Derivation

### Why Hasse diagrams matter

The Hasse diagram encodes the **combinatorial skeleton** of a topological space. Instead of storing every geometric coordinate, it captures the incidence structure: which faces belong to which higher-dimensional cells. This is crucial for:

- Computing topological invariants (homology, Morse theory)
- Analyzing algorithmic complexity of operations on the complex
- Understanding how simplicial/cell complexes can be efficiently decomposed

### The treewidth bottleneck

A naive construction—globally gluing vertex gadgets to a base digraph $D$—can produce an exponentially wide Hasse diagram even when $D$ itself has small treewidth (width $k$). This happens because:

1. **Long-range interactions**: handles and fuses from distant parts of $D$ can intertwine
2. **Loss of locality**: merging gadgets globally creates unavoidable ordering dependencies across many cells

**Solution: Width-Preserving Strategy (WiPS)**

WiPS builds the complex **incrementally** along a nice tree decomposition of $D$:

- For each bag $X_t$ in the tree decomposition, maintain a **partial complex** $Y_t$
- Only expose a bounded interface (constant-size set of boundary circles) to avoid cross-contamination
- Operations per bag:
  - **Introduce-vertex**: attach fresh gadget $F(v) \cup L(v)$
  - **Introduce-edge**: add single pinching handle between locks
  - **Forget-vertex**: cap boundary components
  - **Join**: merge child gadgets via constant-size local updates (pair-of-pants on lock side, cylinder attachment on fuse side)

This ensures each bag "sees" only $O(k)$ cells, so the global Hasse diagram maintains treewidth $\leq ck + c'$.

### Key insight

By processing the digraph $D$ via its tree decomposition and only introducing constant-size simplicial pieces at each step, the treewidth of the resulting Hasse diagram scales linearly with $k$ rather than exponentially.

## Applications in Engineering

### 1. **Computational Topology & Persistent Homology**
- Hasse diagrams structure cell complexes for efficient homology computation
- Treewidth bounds enable algorithms for computing topological features on sparse/treelike domains

### 2. **Optimal Morse Matching**
- Critical for reducing the number of cells in a complex while preserving topology
- Applications: mesh simplification, shape analysis, computational cohomology
- ETH-tight bounds guarantee algorithmic optimality for bounded-treewidth inputs

### 3. **Graph Embeddings & Erasability Problems**
- 2D erasability (deciding if a 2-complex is contractible) reduces to Directed Feedback Vertex Set (DFVS) on the underlying digraph
- Hasse diagram treewidth propagation ensures hardness results transfer from DFVS to topological problems

### 4. **Mesh Compression & Data Structures**
- Sparse representations of simplicial complexes use Hasse diagrams to avoid storing redundant face information
- Treewidth bounds guarantee polynomial-size encoding for structured domains

### 5. **Theoretical Computer Science (Parameterized Complexity)**
- Hasse diagram width is a key parameter for designing FPT (Fixed-Parameter Tractable) algorithms
- Enables 2D tiling problems, constraint satisfaction on structured inputs

## Common Mistakes / Pitfalls

### 1. **Confusing Hasse diagram with the complex itself**
- The complex $Y$ is a topological space; the Hasse diagram is a *data structure* representing its face lattice
- Treewidth of the diagram ≠ geometric dimension of the space

### 2. **Assuming treewidth of $D$ equals treewidth of Hasse$(Y)$**
- Naive gadget gluing can blow up the diagram's treewidth exponentially
- WiPS construction is required to *preserve* treewidth (up to constants)

### 3. **Forgetting boundary interfaces in WiPS**
- Each bag must maintain a bounded "interface" of exposed cycles
- Failing to cap or merge