# Rooted Tree Structure

## Definition

A **rooted tree structure** is a connected acyclic graph with a designated root vertex, used to represent hierarchical relationships and enable efficient distributed algorithms. In the context of distributed systems, a rooted tree $T = (V, E)$ consists of:

- A set of vertices $V$ representing processors or network nodes
- A set of directed edges $E$ where each edge $(u, v)$ connects parent $u$ to child $v$
- A distinguished root vertex $r \in V$
- A parent-child relationship: every non-root vertex $v$ has exactly one parent, and a vertex $u$ can have zero or more children

**Key property for distributed representation:** For every edge $e = (u, v)$ where $u$ is the parent and $v$ is the child, the child $v$ must know about the edge. This asymmetric knowledge requirement allows compact memory representation while maintaining algorithmic capability.

## Key Equations

**Memory complexity for compact tree storage:**
$$\text{Space}(T) = O(\log n) \text{ bits per vertex}$$

where $n = |V|$ is the total number of vertices.

**Algorithm complexity for distributed rooted tree operations:**
$$\begin{align}
\text{Time Complexity} &= O(D)\\
\text{Message Complexity} &= O(n)\\
\text{Local Memory Complexity} &= O(\log n)
\end{align}$$

where $D$ is the diameter (height) of the tree.

## Physical Intuition / Derivation

### Why Asymmetric Edge Knowledge Works

In traditional distributed representations, each vertex $v$ must maintain the full adjacency list of all incident edges $E'_v$. However, for tree algorithms, we only need sufficient information to coordinate data flow:

- **For broadcast** (root to leaves): The root initiates, and each vertex sends received messages only to children. Children don't need to know they have children; they only need to know their parent.
  
- **For convergecast** (leaves to root): Each child must send aggregated results to its parent. Thus the child must know the parent-child edge.

This is why requiring knowledge at the child suffices: the parent will learn about the edge when the child sends data through it initially (via a request message).

### Storage Breakdown

Each vertex needs to store:
1. **Parent pointer**: $O(\log n)$ bits to identify its parent
2. **Child count**: $O(\log n)$ bits to track children (needed for convergecast termination)
3. **Backtrace pointer** (optional): $O(\log n)$ bits to retrace paths for source identification

This totals $O(\log n)$ bits per vertex, giving $O(n \log n)$ total distributed memory—far more efficient than centralizing the tree structure.

## Applications in Engineering

### 1. **Distributed Computing & Consensus Algorithms**
Rooted trees form the backbone of:
- **Leader election algorithms** (e.g., GHS algorithm mentioned in sources) where a spanning tree is computed to organize distributed processors
- **Fault-tolerant systems**: Tree-structured heartbeat protocols for failure detection
- **MapReduce and data-parallel frameworks**: Tree-based aggregation stages

### 2. **Network Routing**
- **Broadcast trees** (spanning trees) for multicast routing in ad-hoc and sensor networks
- **Minimum spanning tree (MST) computation** for optimal cost routing
- **Reverse path forwarding**: Each node knows its parent in the routing tree, enabling loop-free forwarding

### 3. **Hierarchical Sensor Networks**
- **Data aggregation**: In wireless sensor networks (WSNs), convergecast aggregates measurements (min, max, sum) from all sensors to a root sink node with $O(D)$ latency
- **Energy efficiency**: Directed parent-child links minimize redundant transmissions

### 4. **Parallel Computing**
- **Tree-based reduction operations**: Combining results from parallel tasks via tree structure (e.g., sum, product of distributed values)
- **Barrier synchronization**: Rooted trees coordinate phase transitions across processors

### 5. **Network Protocol Design**
- **Spanning tree protocols** (IEEE 802.1D): Prevents loops in bridged networks
- **Cluster formation**: In mobile ad-hoc networks, tree topologies organize nodes into a hierarchy

## Common Mistakes / Pitfalls

### 1. **Confusing symmetric vs. asymmetric edge knowledge**
❌ **Wrong**: "Every vertex must know all incident edges"  
✓ **Correct**: "In a rooted tree, each child must know its parent edge; parents learn about children dynamically"

### 2. **Forgetting the diameter complexity bound**
❌ **Wrong**: Assuming broadcast/convergecast takes $O(n)$ rounds  
✓ **Correct**: Time is $O(D)$ where $D$ is the tree height/diameter

### 3. **Overestimating memory needs**
❌ **Wrong**: Storing full adjacency lists requires $O(n)$ bits per vertex  
✓ **Correct**: In a tree, only $O(\log n)$ bits suffice (parent ID + child count)

### 4. **Ignoring the request buffering mechanism**
❌ **Wrong**: Each broadcast requires resending requests every round  
✓ **Correct**: Requests are buffered as edge state, reducing redundant messages

### 5. **Misunderstanding convergecast termination**
❌ **Wrong**: "A parent receives aggregated results in any order and stops when convenient"  
✓ **Correct**: "A parent maintains a count of received child messages and aggregates only when count equals number of children"

## See Also

- [[Spanning Tree|Spanning Trees]] — The fundamental graph structure from which rooted trees are derived
- [[Broadcast Algorithm|Broadcast Algorithms]] — Root-to-all message dissemination using rooted tree structure
- [[Convergecast Algorithm|Convergecast/Aggregation]] — Leaf-to-root data collection along tree edges
- [[Distributed Graph Algorithms]] — GHS and GKP algorithms that construct and use rooted trees
- [[Message Complexity|Message and Time Complexity]] — Analysis framework for rooted tree algorithms

## Sources

- Distributed algorithms lecture notes, Section A.1-A.2 (Broadcast and converge