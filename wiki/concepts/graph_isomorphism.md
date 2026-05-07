# Graph Isomorphism

## Definition

**Graph isomorphism** is a structure-preserving bijection between the vertex sets of two graphs. Two graphs $G_1 = (V_1, E_1)$ and $G_2 = (V_2, E_2)$ are **isomorphic** if there exists a bijection $\phi: V_1 \to V_2$ such that:

$$\forall u, v \in V_1: \quad (u, v) \in E_1 \iff (\phi(u), \phi(v)) \in E_2$$

When such a bijection exists, we write $G_1 \cong G_2$. 

The bijection $\phi$ is called an **isomorphism** or **graph homomorphism** when it preserves adjacency relationships. For vertex pairs $(v_Z, v_R) \in V(Z) \times V(G(R))$ corresponding under an isomorphism, all structural properties (degree, neighborhood structure, cycles, etc.) must correspond exactly.

### Structural Invariants

Isomorphic graphs must share all **graph invariants**:
- Number of vertices: $|V_1| = |V_2|$
- Number of edges: $|E_1| = |E_2|$
- Degree sequence (sorted vertex degrees)
- Girth (length of shortest cycle)
- Diameter and radius
- Chromatic number
- Spectral properties (eigenvalues of adjacency matrix)

## Key Equations

**Necessary conditions for isomorphism** — if $G_1 \cong G_2$, then:

$$\sum_{v \in V_1} \deg(v) = \sum_{v \in V_2} \deg(v) = 2|E|$$

**Adjacency matrix correspondence** — under isomorphism $\phi$, the permuted adjacency matrix $A_2 = P A_1 P^T$ where $P$ is the permutation matrix corresponding to $\phi$.

**Degree constraint in rule matching** (from source context) — a configuration $Z$ obeys a rule $R$ if $Z \cong G(R)$ **and** every vertex correspondence satisfies:

$$\forall (v_Z, v_R) \text{ corresponding under } \phi: \quad \delta_R^-(v_R) \leq d(v_Z) \leq \delta_R^+(v_R)$$

This couples graph structure with degree-interval constraints.

## Physical Intuition / Derivation

### Why Isomorphism Matters

Graph isomorphism captures the notion of **"same shape, different labels."** Consider two circuit networks with identical topology but different component labeling—they are isomorphic. From an engineering perspective:

1. **Relabeling irrelevance**: The actual names of vertices (component IDs, geographic labels) don't matter for functional behavior; only connectivity does.

2. **Canonical form reduction**: Recognizing when two graphs are isomorphic lets us reduce problem instances and avoid redundant computation.

3. **Configuration matching**: In the discharging rules context, we need to detect whether a subgraph in a larger graph matches a *pattern* (the rule template). This requires testing isomorphism to the rule's near-triangulation $G(R)$.

### Computational Challenge

Testing whether $G_1 \cong G_2$ is **not known to be in P or NP-complete**—it sits in a complexity class of its own (Graph Isomorphism, GI). For general graphs:
- Brute-force: $O(n! \cdot \text{poly}(n))$ — prohibitively expensive
- Practical heuristics use invariant filtering to prune the search space

### Application in Discharging Rules

In the source material, rule matching proceeds as:
1. Identify a candidate edge $(s,t)$ in graph $G$
2. Extract the local configuration $Z$ around this edge
3. Test if $Z \cong G(R)$ for rule $R$ 
4. **If isomorphic**, verify that degree constraints are satisfied: $\delta_R^-(v_R) \leq d(v_Z) \leq \delta_R^+(v_R)$
5. Apply charge transfer (send $r(R)$ units from $s$ to $t$)

The isomorphism must preserve the **directed semantics**: the arrow direction on edge $s(R)t(R)$ in the rule determines which vertex is the "tail" (source of charge) and "head" (receiver).

## Applications in Engineering

### 1. **Circuit Design & Network Topology**
- Detect equivalent circuit topologies despite different component labels
- Simplify circuit analysis by recognizing isomorphic subcircuits
- Verify that two netlists implement the same logical structure

### 2. **Software Architecture**
- Identify refactored code sections with identical control-flow graphs
- Detect code clones (isomorphic Abstract Syntax Trees)
- Graph-based malware detection: recognize similar call graphs

### 3. **Graph Coloring & Resource Allocation**
- Verify that two constraint satisfaction problems are equivalent (same chromatic number, same degree sequence)
- Network scheduling: ensure isomorphic problems yield isomorphic solutions

### 4. **Combinatorial Optimization & Proof Theory**
- **Discharging method** (Four Color Theorem context): Prove properties hold for *all* graphs satisfying certain invariants by matching against a finite rule set. Graph isomorphism allows matching local patterns in an arbitrary triangulation against canonicalized rule templates.
- Configuration testing in planar graph theory

### 5. **Bioinformatics**
- Protein interaction networks: identify isomorphic network motifs
- Chemical compound comparison: canonicalize molecular structures as graphs

### 6. **Machine Learning on Graphs**
- Graph neural networks use isomorphism-aware embeddings (Weisfeiler-Lehman test as lower bound on GNN expressiveness)
- Graph classification requires identifying when learned patterns are structurally equivalent across inputs

## Common Mistakes / Pitfalls

### 1. **Confusing Isomorphism with Equality**
❌ *Incorrect*: "$G_1 \cong G_2$" means the graphs are the same object  
✓ *Correct*: