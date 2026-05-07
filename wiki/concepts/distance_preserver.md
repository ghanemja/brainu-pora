# distance preserver

## Definition

A **distance preserver** is a subgraph $H$ of a graph $G = (V, E)$ that preserves shortest-path distances between a designated set of vertices $S \subseteq V$ (called *terminals*).

Formally, for all pairs of vertices $u, v \in S$:
$$d_H(u, v) = d_G(u, v)$$

where $d_X(u,v)$ denotes the shortest-path distance in graph $X$.

### Variants

**Subsetwise Distance Preserver (SDP):** Preserves distances between *all pairs* of terminals in $S$.

**Pairwise Distance Preserver (PDP):** Preserves distances only for a specified subset of terminal pairs, given as input.

A distance preserver is **minimal** if no proper subgraph preserves the same distances. It is **minimum** if it has the fewest edges among all distance preservers.

## Key Equations

### Distance Preservation Constraint
$$\text{For all } u, v \in S: \quad d_H(u, v) = d_G(u, v)$$

### Optimization Objective
$$\text{minimize} \quad |E(H)| \quad \text{subject to distance preservation}$$

### Trivial Bounds
- **Upper bound:** $|E(H)| \leq |E(G)|$ (the full graph preserves all distances)
- **Lower bound for SDP:** At least $|S| - 1$ edges are required (connectivity requirement)
- **Observation:** If preserving all pairwise distances in $G$, then $H = G$ (no compression possible)

## Physical Intuition / Derivation

### Why Distance Preservers Matter

Distance preservers address a fundamental trade-off in graph processing:

**The Core Tension:** A shortest-path tree between $|S|$ terminals requires only $O(|S|)$ edges but may detour significantly for non-terminal pairs. A distance preserver guarantees exact distance preservation while minimizing edges.

### Intuitive Construction

Consider a simple example: a graph with terminals $S = \{s_1, s_2, s_3\}$ and shortest paths:
- $s_1 \to s_2$: path of length 3 via edges $e_1, e_2, e_3$
- $s_2 \to s_3$: path of length 2 via edges $e_4, e_5$  
- $s_1 \to s_3$: path of length 4 via edges $e_1, e_2, e_4, e_5$

A distance preserver must include at least $\{e_1, e_2, e_3, e_4, e_5\}$ to maintain all three pairwise distances. Any single-edge removal breaks at least one shortest path.

### Why It's Hard

The problem is computationally challenging because:

1. **Subgraph selection is combinatorial:** For large graphs, checking all $2^{|E|}$ subgraphs is infeasible
2. **Dependencies are global:** Removing one edge can invalidate multiple distance constraints simultaneously
3. **Greedy approaches fail:** Including the "most important" edges first doesn't guarantee minimality
4. **Graph structure matters:** Regular structures (grids, trees) have vastly different complexities than arbitrary graphs

## Applications in Engineering

### 1. **Distributed Computing & Networks**
- **Routing protocols:** Preserve distances only between critical node pairs to reduce routing table size
- **Network monitoring:** Create minimal subgraphs that capture essential connectivity constraints
- **Fault tolerance:** Identify critical edges whose failure would break distance preservation

### 2. **Computational Geometry**
- **Proximity graphs:** Construct sparse representations of point sets while preserving distances between query points
- **Mesh processing:** Simplify geometric graphs while preserving geodesic distances for specific regions of interest

### 3. **Transportation & Logistics**
- **Road network optimization:** Identify minimal essential roads connecting critical hubs (terminals = distribution centers)
- **Transit planning:** Design minimal transfer networks preserving travel times between major stations

### 4. **Algorithm Acceleration**
- **Preprocessing for shortest-path queries:** Replace full graph with distance preserver for reduced memory/query time
- **Approximate distance oracles:** Use distance preservers as foundation for faster distance approximation

### 5. **Graph Compression & Storage**
- **Network visualization:** Create sparse but distance-faithful graph representations for visual exploration
- **Indexing:** Build compact graph summaries for massive dynamic networks

## Common Mistakes / Pitfalls

### 1. **Confusing with Shortest-Path Tree**
**Error:** Assuming a single shortest-path tree from a root terminal suffices.

**Why it fails:** A tree rooted at $s$ preserves distances from $s$ to all terminals, but not distances *between other terminals*. For SDP on $S = \{s, t_1, t_2, \ldots\}$, distances $d(t_i, t_j)$ are often not preserved.

**Correct approach:** Consider distance preservation as a system of constraints, not a tree-based structure.

### 2. **Greedy Edge Selection**
**Error:** Iteratively adding edges that "fix the most violations" leads to minimal solutions.

**Why it fails:** Local greedy choices create dependencies that force expensive global subgraph choices later.

**Correct approach:** Use parameterized algorithms (bounded search trees, dynamic programming on treewidth) for exact solutions on restricted graph classes.

### 3. **Ignoring Problem Variant Differences**
**Error:** Treating PDP and SDP as equivalent.

**Why it fails:** The two variants have radically different complexities! SDP is FPT when parameterized by vertex cover; PDP is NP-hard even on vertex cover 3 graphs.

**Correct approach:** Choose algorithm and complexity analysis specific to your variant.

### 4. **Assuming General Hardness on All Graphs**
**Error:** Concluding that distance preservers are intractable everywhere because they're NP-hard on grid subgraphs.

**Why it fails:** Full grids and tree-structured graphs admit FPT solutions; hardness is instance/structure-dependent.

**Correct approach:** Analyze the graph class; exploit structure (low treewidth,