# distributed algorithm

## Definition

A **distributed algorithm** is a computational procedure executed simultaneously and independently across multiple processes or nodes in a network, where:

- Each node has only **local knowledge** (its own state, neighbors' IDs, local parameters)
- Nodes communicate through **synchronous or asynchronous message passing** over fixed time rounds
- No central controller or global state exists
- Computation must **terminate** with correct results despite partial information

In formal terms, a distributed algorithm solves a problem on a graph $G = (V, E)$ where each vertex $v \in V$ executes the same local algorithm that reads only local inputs and neighbor messages, producing local outputs that collectively satisfy the global problem specification.

### The CONGEST Model

The standard **CONGEST** (CONgestion + GESTure) model constrains distributed algorithms with:
- Each vertex can send **one $O(\log n)$-bit message per neighbor per round**
- Vertices know their own unique ID and neighbor IDs (initially)
- Communication is **synchronous** (lockstep rounds)
- Total runtime measured in **rounds** (network diameter lower bound)

## Key Equations

**Hop-diameter complexity bound:**
$$T_{\text{rounds}} = \tilde{O}(D)$$

where $D$ is the hop-diameter (maximum shortest-path distance in the network) and $\tilde{O}$ hides logarithmic factors.

**Weight balance constraint (for separator algorithms):**
$$w(v) \leq \frac{1}{12} \sum_{u \in V} w(u), \quad \forall v \in V$$

ensures no single vertex dominates the partition.

**Message complexity per round:**
$$M_{\text{per-round}} = O(n \log n) \text{ bits total}$$
(each of $n$ vertices sends $O(\log n)$ bits to each neighbor)

## Physical Intuition / Derivation

### Why Distributed Algorithms Matter

Traditional centralized algorithms require a single processor to know the entire graph structure—infeasible for:
- **Sensor networks** with thousands of nodes
- **Peer-to-peer systems** without central servers
- **Large-scale systems** where data collection is expensive or impossible

Distributed algorithms impose **locality constraints**: each node decides based only on its neighborhood, forcing algorithms to exploit network structure rather than global knowledge.

### Information Propagation Speed

A fundamental insight: **information spreads at one hop per round**. To compute anything involving distant nodes, an algorithm must pay at least $\Omega(D)$ rounds where $D$ is the network diameter.

Example: Computing a **spanning tree** via BFS from root $r$:
1. Round 1: $r$ broadcasts to neighbors
2. Round 2: Neighbors relay to their unvisited neighbors
3. Round $D$: Furthest nodes receive first message
4. Result: $\Omega(D)$ lower bound on any spanning tree algorithm

### The Weight-to-Face Transfer Mechanism

The source material introduces a simple but elegant idea:
- **Problem**: Assigning vertex weights to faces risks **overcounting** (multiple faces per vertex)
- **Solution**: Each vertex transfers its weight to **exactly one arbitrary face** it belongs to
- **Effect**: Each unit of weight counted exactly once, enabling clean balance guarantees

This is a **derandomization** technique—replacing randomized load balancing with deterministic but arbitrary choice.

## Applications in Engineering

### 1. **Distributed Graph Algorithms**
- **Shortest paths**: Computing distances in $\tilde{O}(D)$ rounds via synchronous flooding
- **Spanning trees**: BFS or DFS trees for network backbone construction
- **Graph coloring**: Vertex colorings for scheduling without conflicts (e.g., radio channel assignment)

### 2. **Network Topology Management**
- **Planar graph separators**: Partitioning networks into balanced components (road networks, circuit layouts)
- **Load balancing**: Distributing computation/storage across nodes via cuts
- **Hierarchical decomposition**: Recursively partitioning for multi-level control

### 3. **Concrete Engineering Problems**
- **Maximum flow / minimum cut** on road networks (traffic routing)
- **Depth-first search** for network connectivity/cycle detection
- **Global minimum-cut** in directed networks (fault tolerance)
- **Reachability queries** in communication networks

### 4. **Wireless & Mobile Networks**
- **Localization**: Distributed position estimation using neighbor distances
- **Consensus algorithms**: Nodes agreeing on a value (e.g., timestamp synchronization)
- **Routing protocol** initialization (OSPF, ISIS) uses distributed tree construction

## Common Mistakes / Pitfalls

### 1. **Ignoring the Diameter Lower Bound**
❌ **Mistake**: Designing an algorithm expected to run in $O(\log n)$ rounds on arbitrary graphs  
✓ **Reality**: Any algorithm touching distant parts of graph needs $\Omega(D)$ rounds; $D$ can be $\Theta(n)$ for paths

### 2. **Assuming Nodes Know Global Information**
❌ **Mistake**: Using a greedy strategy that requires "knowing the globally optimal choice"  
✓ **Fix**: Algorithms must use only local information or explicitly propagate decisions with $O(D)$ cost

### 3. **Forgetting Synchronization Overhead**
❌ **Mistake**: Neglecting that asynchronous algorithms require additional complexity for clock synchronization  
✓ **Reality**: Synchronous CONGEST model is idealized; real systems need Byzantine-robust variants or time-stamping

### 4. **Miscounting in Weight/Load Assignment**
❌ **Mistake**: Assigning same vertex weight to multiple domains (double-counting)  
✓ **Fix**: As in source material—each entity claims to exactly one "owner" deterministically

### 5. **Assuming Messages Are Free**
❌ **Mistake**: Designing with $O(n^2)$ total message complexity  
✓ **Reality**: CONGEST model constrains $O(n \log n)$ per round; total messages scale as $O(n D \log n)$ for $O(D)$-round algorithms

## See Also

- [[spanning tree]] — fundamental structure computed distributedly in $O(D)$ rounds
- [[planar graph]] — restricted graph class enabling balanced separators
- [[