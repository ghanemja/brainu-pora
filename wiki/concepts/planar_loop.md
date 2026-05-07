# planar loop

## Definition

A **planar loop** is a closed curve in the plane formed by combining two directed paths in a planar graph along with a connecting edge that closes the cycle. Formally, given a planar embedding of a graph $G$:

- Let two upward paths $P_1$ and $P_2$ exist in a spanning subgraph $H \subseteq G$
- Let $e$ be a "closing edge" in $G$ connecting the terminal endpoints of $P_1$ and $P_2$, where $e \notin H$
- The **planar loop** $\xi_S$ is the Jordan curve formed by the planar drawing of $P_1$, $P_2$, and $e$ together

The loop $\xi_S$ divides the plane into two regions: an **interior** and an **exterior**. This is a direct consequence of the Jordan curve theorem applied to the graph-theoretic setting.

## Key Equations

The membership classification for vertices relative to a planar loop:

$$\text{Interior}(\xi_S) = \{v \in V(G) : v \text{ lies in bag of } T \text{ on component side 1 after removing } e\}$$

$$\text{Exterior}(\xi_S) = \{v \in V(G) : v \text{ lies in bag of } T \text{ on component side 2 after removing } e\}$$

where $(T, \beta)$ is a tree decomposition and $e \in E(T)$ is the adhesion edge inducing separator $S$.

## Physical Intuition / Derivation

### Construction from Tree Decomposition

The concept emerges naturally when decomposing planar graphs hierarchically. Consider:

1. **Start with a planar graph** $G$ embedded in the plane
2. **Build a spanning tree** $H$ that "respects" certain structural properties
3. **Identify separators**: When removing an edge $e$ from the tree decomposition tree $T$, we partition bags into two components
4. **Form the loop**: The separator $S$ is constructed from two upward paths in $H$ plus a closing edge from $G \setminus H$. Drawing these three components together creates a topological circle.

### Why This Matters

The planar loop serves as a **barrier** for detecting problematic vertex pairs:

- **Bad pairs** with respect to $\xi_S$ are those whose connecting links (shortest paths or paths in some metric) intersect the loop
- These bad pairs fall into two categories:
  - **Separated pairs**: endpoints lie on opposite sides of $\xi_S$
  - **Contaminating pairs**: the link uses an edge from $S$ that is excluded from some required subgraph

This classification enables algorithmic techniques to count and control problematic pairs in graph algorithms.

## Applications in Engineering

### 1. **Graph Routing & Network Design**
- Planar loop analysis helps identify critical separators in network topology
- Determines which terminal pairs require path routing that crosses specific regions
- Used in VLSI routing to detect design rule violations crossing predefined boundaries

### 2. **Planar Graph Decomposition Algorithms**
- Structural tool in treewidth and pathwidth decomposition of planar graphs
- Enables divide-and-conquer algorithms that recursively solve subproblems inside/outside loops
- Reduces solution space for NP-hard problems on planar graphs (e.g., [[Steiner tree]], [[maximum cut]])

### 3. **Mesh Generation & Computational Geometry**
- Defines connectivity constraints in constrained Delaunay triangulation
- Used to identify mesh refinement boundaries without violating planarity
- Ensures that mesh vertices respect topological separation requirements

### 4. **Constraint Satisfaction in Layout Design**
- Electronic circuit design uses planar loops to enforce non-crossing constraints
- PCB routing prevents cross-layer interference by respecting planar loop boundaries
- Identifies design rule violations in automated layout verification

## Common Mistakes / Pitfalls

### 1. **Confusing Loop with Cycle**
A planar loop is **not** merely a cycle in the graph—it is a **Jordan curve in the plane**. A cycle exists abstractly; a loop is a topological object with defined interior and exterior.

### 2. **Assuming All Graph Cycles Form Valid Loops**
Only cycles constructed deliberately from paths in a spanning tree + exterior closing edges reliably create the required loop properties. Arbitrary cycles may not partition bags correctly.

### 3. **Forgetting Non-Planarity When Generalizing**
The Jordan curve theorem and the resulting interior/exterior distinction fail for non-planar graphs. This technique is *fundamentally planar*.

### 4. **Misclassifying Bad Pair Types**
**Critical mistake**: A pair can be bad without being separated (if both endpoints are on the same side but the link still crosses $\xi_S$). Always check both separation *and* contamination conditions.

### 5. **Oversimplifying "Closing Edge"**
The closing edge must be in $G$ but **not** in the spanning tree $H$. Using an edge already in $H$ does not create a valid closing edge and breaks the construction.

## See Also

- [[tree decomposition|Tree Decomposition]] – hierarchical partition of graph bags
- [[planar graph]] – graphs embeddable in the plane without edge crossings
- [[Jordan curve theorem]] – topological foundation for interior/exterior distinction
- [[separator (graph theory)]] – vertex/edge sets whose removal disconnects components
- [[Steiner tree problem]] – application requiring control of terminal pair routing
- [[treewidth]] – graph width parameter that benefits from planar loop analysis

## Sources

- Lecture/paper excerpt on tree decomposition of planar graphs and separator-based analysis (Theorem 3.5 and Claims 5.9–5.10)
- Structural graph theory literature on planar decomposition and bad pair enumeration