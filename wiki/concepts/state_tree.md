# state tree

## Definition

A **state tree** is a rooted, directed tree data structure that compactly encodes all solutions to a graph enumeration problem by representing prefixes of solution paths. In the context of Eulerian trail enumeration, the uncompressed state tree $T_u$ of a directed graph $G = (V, E)$ is defined as:

- **Nodes (states)**: Each state $s$ in $T_u$ corresponds to a unique prefix $P_s$ of an Eulerian trail starting from a fixed source node $v_0$.
- **Edges (transitions)**: An edge exists from state $s_1$ to state $s_2$ in $T_u$ if $P_{s_1}$ is obtained by removing the last edge from $P_{s_2}$.
- **Leaves**: Each leaf node in $T_u$ corresponds to exactly one complete Eulerian trail in $G$.

The root of $T_u$ represents the empty prefix (starting at $v_0$ with no edges traversed).

## Key Equations

**Size of uncompressed state tree:**
$$|T_u| \in O(m \cdot z_T)$$

where $m = |E|$ (number of edges) and $z_T$ is the total number of distinct Eulerian trails in $G$.

**Compressed state tree complexity:**
$$|T_{\text{compressed}}| \in O(m + z_T)$$

**Enumeration time for subtree with $z$ leaves:**
$$\text{Time} \in O(m + z)$$

This near-linear dependency on the input size plus output size is achieved through path compression techniques.

## Physical Intuition / Derivation

### Why State Trees?

Consider the naive approach to enumerating all Eulerian trails: explicitly output each trail, requiring $\Omega(m \cdot z_T)$ time and space (since each trail has $m$ edges and there are $z_T$ trails). This is prohibitively expensive when $z_T$ is large.

A state tree avoids redundant work by observing that **many Eulerian trails share common prefixes**. Instead of independently computing each trail, we build a tree where:

1. Common prefix branches are represented once
2. The tree branches only at decision points (where multiple edge choices exist for continuing the trail)
3. Traversing from root to leaf implicitly reconstructs any complete trail

### Construction Intuition

The state tree is built recursively using a depth-first search (DFS) strategy:

1. Start at the root (empty prefix at $v_0$)
2. At each state $s$ with prefix $P_s$, extend $P_s$ by one edge using Hierholzer's algorithm
3. If multiple outgoing edges exist from the current node in $G$, the state tree branches
4. Continue until the prefix cannot be extended further (Eulerian trail is complete)

Each state represents a **choice point** in the space of all possible Eulerian trails. By organizing these choice points hierarchically, the tree avoids recomputing shared work.

### From Uncompressed to Compressed

The uncompressed tree has size $O(m \cdot z_T)$ because:
- It explicitly stores every prefix of every Eulerian trail
- In the worst case, prefixes are not shared effectively

**Compression** reduces this to $O(m + z_T)$ by:
- **Path compression**: Merging chains of states with branching factor 1 into single nodes
- **Implicit representation**: Storing only decision points and using on-the-fly edge exploration

## Applications in Engineering

### 1. **Network Routing & Circuit Design**
State trees enumerate all feasible paths through a network (e.g., Eulerian paths in a routing graph), enabling:
- Verification of all possible Hamiltonian decompositions
- Route enumeration for fault-tolerant network design
- Testing all possible circuit traversals in scan-path design

### 2. **Computational Biology**
DNA sequence assembly and genome reconstruction often require enumerating Eulerian trails in de Bruijn graphs:
- **de Bruijn graph**: Nodes represent $k$-mers; edges represent $(k+1)$-mers
- State trees enable efficient enumeration of all possible sequence reconstructions from fragmented reads
- Critical for handling sequencing ambiguities

### 3. **Logistics & Operations Research**
Vehicle routing problems with specific constraints (e.g., required edge traversals):
- State trees enumerate feasible delivery routes that traverse required streets/connections
- Enables optimization over the full solution space without explicit enumeration of exponentially many tours

### 4. **Formal Verification**
Model checking and symbolic execution:
- State trees represent all possible execution paths through a program or system
- Compressed representation enables checking safety properties across exponentially many behaviors efficiently

### 5. **Graph Isomorphism & Combinatorial Search**
Enumerating canonical forms or all matchings:
- State trees compactly represent solution space for backtracking algorithms
- Enables efficient branch-and-bound optimization

## Common Mistakes / Pitfalls

### 1. **Confusing Graph Nodes with Tree States**
**Mistake**: Using "node" to refer to both elements of $G$ and $T_u$.

**Correction**: Use precise terminology:
- **Nodes/edges** for the input graph $G$
- **States/transitions** for the tree $T_u$

### 2. **Assuming All Prefixes are Unique**
**Mistake**: Believing the uncompressed tree achieves $O(m + z_T)$ space without compression.

**Correction**: Uncompressed size is $O(m \cdot z_T)$. Compression is essential for near-linear complexity; it requires identifying and merging redundant branches.

### 3. **Missing the Role of Hierholzer's Algorithm**
**Mistake**: Treating state tree construction as a simple DFS without understanding edge selection.

**Correction**: Hierholzer's algorithm ensures that at each state, edge selection is **deterministic given a prefix**, enabling consistent state definitions. Different edge orderings yield different state trees but enumerate the same trails.

### 4. **Overlooking Source Node Constraints**
**Mistake**: Forgetting that the state tree is rooted at a **fixed source node** $v_0$.

**Correction**: For graphs with Eulerian cycles (no unique source), one must