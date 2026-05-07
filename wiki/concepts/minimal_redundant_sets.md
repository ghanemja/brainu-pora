# minimal redundant sets

## Definition

A **minimal redundant set** in a graph $G = (V, E)$ is a vertex subset $S \subseteq V$ such that:

1. **Redundancy condition**: Every vertex in $S$ is redundant with respect to $S$, meaning for each $v \in S$, there exists another vertex $u \in S$ such that the closed neighborhood satisfies $N[v] \subseteq N[u]$ (or vice versa).

2. **Minimality condition**: No proper subset of $S$ satisfies the redundancy condition.

In contrast to **maximal irredundant sets** (where vertices are pairwise non-redundant and the set is maximal under inclusion), minimal redundant sets represent the "most compressed" configurations where internal structure permits systematic vertex elimination without loss of coverage properties.

Formally: $S$ is minimal redundant if:
- For all $v \in S$: $\exists u \in S \setminus \{v\}$ such that $N[v] \subseteq N[u]$ or $N[u] \subseteq N[v]$
- $\forall S' \subsetneq S$: the redundancy condition fails for $S'$

## Key Equations

**Comparability relation** (foundation for redundancy):
$$\text{vertices } x, y \text{ are comparable} \iff N(x) \setminus \{y\} \subseteq N(y) \setminus \{x\} \text{ or } N(y) \setminus \{x\} \subseteq N(x) \setminus \{y\}$$

**Quasi-simple vertex**: A vertex $v$ is quasi-simple if all vertices in $N(v)$ are pairwise comparable with respect to each other.

**Closed neighborhood operator**:
$$N[v] = N(v) \cup \{v\}$$

**Trace of hypergraph** (for reduction to hypergraph domination):
$$H_S = (S, \{E \cap S \mid E \in E(H), E \cap S \neq \emptyset\})$$

## Physical Intuition / Derivation

### Why Study Minimal Redundant Sets?

Minimal redundant sets represent **structural degeneracies** in network and system topologies. The key insight is that within a network:

1. **Vertices have hierarchical influence**: The comparability relation captures when one vertex's neighborhood strictly contains another's. This models scenarios where one entity's reach encompasses another's.

2. **Redundancy = Structural Compression**: A set is redundant when its vertices can be partially ordered by neighborhood inclusion. This mirrors real systems where:
   - In sensor networks: sensors with overlapping coverage can be ordered by monitoring reach
   - In organizational charts: subordinate roles may have identical reporting structures
   - In biological networks: genes with overlapping function can be hierarchically arranged

3. **Minimality = Irreducibility**: The minimal condition ensures we've identified the **smallest irreducible subgraph** with this redundancy structure—removing any vertex breaks the property.

### Connection to Strongly Orderable Graphs

The source material emphasizes **quasi-simple elimination orderings** on strongly orderable graphs. The algorithm strategy is:

$$\text{If } v \text{ is quasi-simple in } G[\{v_1, \ldots, v_i\}], \text{ then the subproblem reduces to simpler classes}$$

This recursive structure means minimal redundant sets on strongly orderable graphs (which include chordal bipartite and strongly chordal graphs) decompose into tractable sub-instances through repeated identification of quasi-simple vertices.

## Applications in Engineering

### 1. **Sensor Network Optimization**
- **Problem**: Minimize deployed sensors while maintaining complete coverage
- **Application**: Identify minimal redundant sensor clusters where sensors have overlapping detection ranges. Remove all but one per cluster.
- **Metric**: Percentage reduction in sensor count while preserving event detection

### 2. **Data Center Redundancy**
- **Problem**: Determine minimal sets of servers that can be powered down without service degradation
- **Application**: Servers with identical network accessibility and backup roles form minimal redundant sets
- **Benefit**: Energy savings through strategic consolidation

### 3. **Power Grid Resilience**
- **Problem**: Identify critical vs. redundant substations
- **Application**: Substations serving identical load profiles form minimal redundant sets; candidates for strategic hardening or removal
- **Safety**: Prevents over-engineering while maintaining fault tolerance

### 4. **Computational Hypergraph Analysis**
- **Problem**: Compress hypergraph representations (e.g., satisfiability formulas, knowledge bases)
- **Application**: The closed-neighborhood hypergraph $\mathcal{N}(G)$ construction allows translating graph-theoretic redundancy into hyperedge redundancy via transposed hypergraphs and incidence graphs
- **Implementation**: Red-blue domination algorithms on incidence bipartite graphs $B(H)$ solve redundancy problems in linear/quasi-polynomial time on appropriate graph classes

### 5. **System Safety Analysis**
- **Problem**: Identify minimal failure modes with equivalent consequences
- **Application**: Components whose failure manifests identically (same downstream effects) form minimal redundant sets; prioritize protection for the non-redundant elements

## Common Mistakes / Pitfalls

### 1. **Confusing Minimal Redundant with Maximal Irredundant**
❌ **Wrong**: "A minimal redundant set maximizes irredundant vertices"  
✓ **Correct**: Minimal redundant sets have *every* vertex redundant (opposite property). Maximize size of irredundant sets separately.

### 2. **Assuming Comparability is Symmetric**
❌ **Wrong**: "If $x$ comparable to $y$, then $y$ comparable to $x$ in the same direction"  
✓ **Correct**: Comparability is symmetric (either direction suffices), but the inclusion relation is directional: $N(x) \subseteq N(y)$ is not equivalent to $N(y) \subseteq N(x)$.

### 3. **Misapplying Quasi-Simplicity Locally**
❌ **Wrong**: "A quasi-simple vertex remains quasi-simple after induced subgraph extraction"  
✓