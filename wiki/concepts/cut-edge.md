# cut-edge

## Definition

A **cut-edge** (also called a **bridge**) in an undirected graph is an edge whose removal increases the number of connected components. In the context of phylogenetic networks, a cut-edge is an edge $e = \{u, v\}$ that is not contained in any cycle.

More formally: An edge $e$ in graph $G$ is a cut-edge if and only if $e \notin E(C)$ for any cycle $C$ in $G$.

**In directed graphs (arcs):** When a cut-edge $e$ is directed in a partial orientation $U'$ of an undirected network $U$, it is called a **cut-arc** in $U'$.

## Key Equations

For an undirected graph $G = (V, E)$ with $c$ connected components:

$$|E_{\text{cut}}| = |V| - c$$

where $|E_{\text{cut}}|$ denotes the number of cut-edges. This follows because cut-edges form the edge set of a spanning forest.

**Characterization in q-cuttable networks:** A network $U$ is $q$-cuttable if every cycle contains a $q$-chain (a path of length $q$). Equivalently, by Observation 5, $U$ is $q$-cuttable if and only if deleting every edge from each maximal chain of length $\geq q$ results in a forest.

## Physical Intuition / Derivation

### Why Cut-edges Matter

Cut-edges are the "critical" edges of a network—they carry unique connectivity information. If you remove a cut-edge, certain nodes become unreachable from others. In phylogenetic networks, this translates directly to branch structure: cut-edges represent evolutionary events that uniquely define ancestral-descendant relationships.

### Relationship to Cycles

By definition, cut-edges never lie on cycles. Conversely, all edges *within* cycles are non-cut-edges (sometimes called **back-edges** or **cycle edges**). This dichotomy partitions the edge set:

$$E = E_{\text{cut}} \cup E_{\text{cycle}}$$

where $E_{\text{cut}} \cap E_{\text{cycle}} = \emptyset$.

### The 2-Cuttable Property

The key result (Proposition 7) states: **If a phylogenetic network is 2-cuttable, it admits a tree-child orientation.**

The intuition:
1. In a 2-cuttable network, every cycle contains a path of length $\geq 2$ with a distinguishable cut-edge nearby
2. By carefully removing edges from maximal chains (avoiding cut-edges), you can reduce the network to a spanning tree $T$
3. This tree structure allows a rooted orientation where each non-root vertex has either one parent (tree edge) or derives from a reticulation (multiple parents), but crucially, each reticulation node can be oriented to satisfy the "tree-child" property

## Applications in Engineering

### Phylogenetic Network Analysis
- **Evolutionary tree reconstruction:** Cut-edges identify the primary evolutionary backbone; non-cut-edges represent secondary reticulation events (hybridization, lateral gene transfer)
- **Computational verification:** Theorem 6 guarantees polynomial-time checking of whether a network is $q$-cuttable, enabling efficient validation of network topologies

### Network Reliability and Robustness
- **Critical infrastructure:** Cut-edges in communication or transportation networks are points of failure; their identification is essential for redundancy planning
- **Spanning tree construction:** Cut-edges form mandatory connections in any spanning tree, so they cannot be removed without disconnecting the graph

### Graph Decomposition
- **Modular analysis:** Networks can be decomposed at cut-edges into blocks (2-edge-connected components), simplifying analysis of network properties
- **Complexity reduction:** Algorithms can process cut-edges separately from more complex cycle structures

## Common Mistakes / Pitfalls

1. **Confusing cut-edges with cut-vertices (articulation points):** A cut-vertex is a vertex whose removal disconnects the graph. Cut-edges and cut-vertices are related but distinct concepts.

2. **Assuming all edges in a tree are cut-edges:** True—but the converse is false. A graph can have cut-edges without being a tree.

3. **Overlooking directionality:** In directed networks, orientation matters. An undirected cut-edge remains a cut-edge regardless of direction, but for acyclicity and tree-child constraints, the orientation of remaining edges in $S'$ must be carefully chosen (see Observation OB1 and OB2 in the proof of Proposition 7).

4. **Misinterpreting $q$-cuttability:** A network being 2-cuttable does NOT mean each edge can be removed; it means cycles have enough structure (chains of length $\geq 2$) that a spanning tree can be formed by strategic edge deletion.

5. **Assuming polynomial verification implies efficient construction:** While checking 2-cuttability is polynomial (Theorem 6), actually constructing the tree-child orientation requires additional algorithmic work beyond Observation 5.

## See Also

- [[cycle]] — The complement structure to cut-edges; cycles contain edges that are *not* cut-edges
- [[spanning tree]] — The result of removing edges strategically; all edges of a spanning tree are cut-edges in the subgraph
- [[2-edge-connected component]] — Maximal subgraphs containing no cut-edges
- [[tree-child orientation]] — The directed acyclic structure that 2-cuttable networks can achieve
- [[phylogenetic network]] — The evolutionary application context where cut-edge analysis proves most useful

## Sources

- Lecture excerpt on phylogenetic networks: Observations 5, Theorem 6, and Proposition 7 on $q$-cuttability and tree-child orientations
- Definitions of cut-edges in graph theory and their role in network decomposition
- Discussion of partial orientations and cut-arcs in directed network contexts