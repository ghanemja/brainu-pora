# degree splitting

## Definition

**Degree splitting** is a fundamental problem in distributed graph algorithms where the edges incident to each vertex are partitioned into multiple groups such that the partition is as balanced as possible. More formally:

Given a graph $G = (V, E)$, a **degree split** is a partition of the edges incident to each vertex $v$ into $k$ groups such that:
- Each group has size between $\lfloor \deg(v)/k \rfloor$ and $\lceil \deg(v)/k \rceil$ (or as close as the constraint allows)
- The partition minimizes **discrepancy**: the maximum deviation from perfect balance

In the context of **balanced orientations** (a directed variant), we orient each edge such that for every vertex $v$, the in-degree and out-degree differ by at most $\varepsilon \cdot \deg(v)$.

### Formal Problem Statement

For a vertex $v$ with degree $\deg(v)$:
- **Undirected degree split**: Partition incident edges into groups $E_1, E_2, \ldots, E_k$ where $||E_i| - |E_j|| \leq 1$ for all $i,j$
- **Directed degree split (balanced orientation)**: Assign directions such that $|\text{in-degree}(v) - \text{out-degree}(v)| \leq \varepsilon \cdot \deg(v)$

## Key Equations

### Discrepancy Bound

For a balanced orientation, the discrepancy constraint is:
$$|d^{\text{in}}(v) - d^{\text{out}}(v)| \leq \varepsilon \cdot \deg(v) \quad \forall v \in V$$

where $d^{\text{in}}(v)$ and $d^{\text{out}}(v)$ are in-degree and out-degree respectively.

### Complexity Results

**Prior work** [GHK+20]:
$$T_{\text{old}} = O(\varepsilon^{-1} \cdot \log \varepsilon^{-1} \cdot (\log \log \varepsilon^{-1})^{1.71} \cdot \log n)$$

**Improved result** [Maus et al., current]:
$$T_{\text{new}} = O(\varepsilon^{-1} \cdot \log n)$$

where $n = |V|$ and $\varepsilon$ is the relative discrepancy parameter.

### Edge Coloring Application

Using degree splitting for $(3/2 + \varepsilon)\Delta$-edge coloring:
$$T_{\text{coloring}} = O(\varepsilon^{-1} \cdot \log^2 \Delta \cdot \log n + \varepsilon^{-2} \cdot \log n)$$

## Physical Intuition / Derivation

### Why Degree Splitting Matters

In distributed systems, edge orientation and degree partitioning arise naturally in load balancing and resource allocation:

1. **Communication Load Balance**: When edges represent communication channels, splitting degree evenly prevents bottlenecks at high-degree vertices
2. **Scheduling**: Partitioning incident edges helps schedule tasks with balanced work distribution
3. **Coloring as a Two-Step Process**: Edge coloring can be viewed as (1) split degree into two classes, (2) color each class independently

### Connection to Sinkless Orientations

The paper establishes a crucial connection to **hypergraph sinkless orientations**: a vertex with all in-edges (a "sink") must be avoided. The key insight is that:
- Sinkless orientations naturally produce balanced in/out-degrees
- By iteratively eliminating near-sinks, we achieve discrepancy $\varepsilon \cdot \deg(v)$

### Algorithm Sketch

The improved algorithm operates in phases:

1. **Phase**: For each vertex $v$, compute orientation of incident edges using local information from 2-hop neighborhood
2. **Imbalance Measurement**: Track vertices where $|d^{\text{in}}(v) - d^{\text{out}}(v)| > \varepsilon \cdot \deg(v)$ 
3. **Reorientation**: Use sinkless orientation gadget to reduce imbalance
4. **Repeat**: Continue until all vertices satisfy discrepancy bound

The key improvement over prior work is eliminating expensive logarithmic factors in $\varepsilon^{-1}$ through more efficient imbalance detection.

## Applications in Engineering

### 1. Distributed Edge Coloring

**Problem**: Color edges with minimum colors such that no two edges sharing a vertex have the same color.

**Application via Degree Splitting**:
- Split degree into balanced orientation (in-degree ≈ out-degree)
- Apply separate coloring algorithms to in-edges and out-edges
- Results in $(3/2 + \varepsilon)\Delta$-coloring for maximum degree $\Delta$

**Practical Use**: Resource scheduling in distributed networks.

### 2. Load Balancing in Parallel Systems

**Problem**: Distribute communication load evenly across routers/switches.

**Application**:
- Network topology is a graph; communication paths use edges
- Degree split ensures no router is overloaded by concentrated traffic from a high-degree vertex
- Enables efficient packet routing in data center networks

### 3. Task Scheduling

**Problem**: Schedule dependent tasks across processors with communication constraints.

**Application**:
- Tasks as vertices, dependencies as edges
- Degree split partitions task dependencies into balanced groups
- Each group executed in a phase, minimizing synchronization overhead

### 4. Distributed Graph Processing

**Problem**: Process large graphs in parallel systems (e.g., MapReduce, Spark GraphX).

**Application**:
- Degree splitting determines how vertex neighbors are partitioned
- Balances computation and communication per vertex
- Critical for achieving scalable speedup in distributed graph analytics

## Common Mistakes / Pitfalls

### 1. Confusing Undirected and Directed Splitting

**Mistake**: Treating edge color assignment as equivalent to orientation.

**Correction**: 
- **Directed**: Assign direction to each edge (orientation)
- **Undirected**: Partition edges into groups without orientation
- Undirected is strictly harder;