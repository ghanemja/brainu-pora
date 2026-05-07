# edge-disjoint paths

## Definition

Two or more paths in a graph are **edge-disjoint** if they share no edges in common. More formally:

**Paths $P_1, P_2, \ldots, P_k$ in a graph $G = (V, E)$ are edge-disjoint if:**
$$E(P_i) \cap E(P_j) = \emptyset \quad \text{for all } i \neq j$$

where $E(P_i)$ denotes the set of edges in path $P_i$.

**Key distinction:** Edge-disjoint paths may share *vertices*, but cannot share *edges*. This contrasts with vertex-disjoint paths, which share neither vertices nor edges (except endpoints).

## Key Equations

### Menger's Edge Connectivity Theorem
The maximum number of edge-disjoint paths between two vertices $s$ and $t$ equals the minimum edge cut separating $s$ from $t$:

$$\max\{\text{edge-disjoint paths } s \text{ to } t\} = \min\{\text{edges in cut separating } s \text{ from } t\}$$

### Path Concatenation Property
If paths $P_1$ (from $a$ to $b$) and $P_2$ (from $b$ to $c$) are edge-disjoint, their concatenation $P_1 \circ P_2$ is a valid path from $a$ to $c$ that is edge-disjoint from any path edge-disjoint from both $P_1$ and $P_2$.

## Physical Intuition / Derivation

### Why Edge-Disjointness Matters

Consider a communication network where data must flow between two nodes. If you route two messages along edge-disjoint paths:

1. **Redundancy:** If any single edge fails, both messages can still reach their destination (one survives the failure)
2. **Capacity:** You effectively double bandwidth by avoiding congestion on shared edges
3. **Robustness:** The network is resilient to single-edge failures

This is fundamentally different from vertex-disjoint paths (stronger requirement) which offer even greater isolation but are harder to construct.

### Constructive Example

In a simple network:
```
    x -------- p₁ -------- y
    |                      |
    |         q            |
    |         |            |
    w -------- p₂ -------- z
```

Two edge-disjoint paths might exist between $(x, y)$ and $(w, z)$:
- $P_1$: x → p₁ → y (horizontal top path)
- $P_2$: w → p₂ → z (horizontal bottom path)

These paths share no edges but may intersect at vertices. A third edge-disjoint path from an internal vertex of $P_1$ (e.g., $p_1$) to an internal vertex of $P_2$ (e.g., $p_2$) through $q$ provides further connectivity.

### Connection to Network Reliability

The existence of $k$ edge-disjoint paths between critical nodes is a standard measure of network reliability. By Menger's theorem, this equals the minimum number of edges whose removal would disconnect the two nodes.

## Applications in Engineering

### 1. **Network Design & Telecommunications**
- **Routing protocols:** Ensure messages can reach destinations even if some links fail
- **QoS guarantees:** Allocate multiple edge-disjoint paths for critical data streams
- **Optical networks:** Route wavelengths on different fiber paths to avoid correlated failures

### 2. **VLSI Circuit Layout**
- **Wire routing:** Design chip interconnects using edge-disjoint paths to minimize cross-talk and electromagnetic interference
- **Power distribution:** Ensure multiple edge-disjoint power delivery paths to reduce voltage drop and power loss

### 3. **Transportation Networks**
- **Traffic engineering:** Design alternate routes that don't share critical road segments
- **Railway systems:** Ensure trains can reroute if a track segment fails
- **Pipeline networks:** Oil/gas routing with redundancy through independent pipes

### 4. **Phylogenetic Tree Embedding** *(from source context)*
- **Unrooted tree containment:** Determine whether a phylogenetic tree can be embedded in a network structure by verifying edge-disjoint path properties in entangled networks
- **Evolutionary network analysis:** Validate whether conflicting evolutionary signals can coexist in a single network model

### 5. **Fault Tolerance in Distributed Systems**
- **Message passing:** Send critical messages via multiple edge-disjoint routes
- **Byzantine resilience:** Achieve agreement even if some communication channels fail
- **Database replication:** Distribute copies across networks with multiple independent paths

## Common Mistakes / Pitfalls

### 1. **Confusing with Vertex-Disjoint Paths**
**Error:** Assuming edge-disjoint paths must also be vertex-disjoint.

**Reality:** Edge-disjoint paths can share internal vertices. If you need stronger isolation, explicitly require vertex-disjoint paths.

**Example:** In a graph $1 - 2 - 3 - 4$, paths $1 - 2 - 3$ and $2 - 4$ share vertex 2 but are edge-disjoint.

### 2. **Overlooking Endpoint Sharing**
**Error:** Thinking edge-disjoint paths cannot share any vertices at all.

**Reality:** Edge-disjoint paths routinely share source and destination (and may share intermediate vertices).

### 3. **Misapplying Menger's Theorem**
**Error:** Claiming the maximum number of edge-disjoint paths is $k$ without verifying the minimum cut is $k$.

**Reality:** Menger's theorem provides an equality—you must compute both the maximum flow and minimum cut to confirm.

### 4. **Ignoring Direction in Directed Graphs**
**Error:** Treating directed and undirected edge-disjoint paths identically.

**Reality:** In directed graphs, path direction matters; an edge can only be traversed once in the specified direction.

### 5. **Assuming Greedy Algorithms Succeed**
**Error:** Greedily routing one path, then another, guarantees finding all possible edge-disjoint paths.

**Reality:**