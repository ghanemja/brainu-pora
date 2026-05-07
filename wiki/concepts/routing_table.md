# routing table

## Definition

A **routing table** is a data structure maintained at each vertex in a distributed network that stores compact directional information for routing messages toward specific destinations. In the context of tree-based routing schemes (such as the TZ scheme), a routing table at vertex $v$ contains:

1. **Routing label information**: An indicator of which single edge to omit from the direct path to the tree root
2. **Subtree metadata**: An interval associated with the subtree rooted at $v$
3. **Vertex identifier**: A number uniquely identifying $v$ within the tree structure

The critical innovation is **size reduction through selective edge omission**: instead of storing the complete path of $O(D)$ edges from root to $v$ (where $D$ is tree depth), the routing table stores only $O(\log n)$ edges by omitting edges leading to sufficiently large subtrees.

## Key Equations

### Storage Complexity
$$\text{Label size} = O(\log^2 n) \text{ bits}$$
$$\text{Routing table size} = O(\log n) \text{ bits}$$

### Edge Omission Criterion
An edge $u \to v$ is omitted from the routing label of $v$ if:
$$|\text{subtree}(v)| \geq \frac{1}{2}|\text{subtree}(u)|$$

Each vertex has **at most one such omittable edge**, reducing the path representation exponentially.

### Setup Complexity (CONGEST Model)
$$\text{Time complexity} = O(D \log n)$$
$$\text{Message complexity} = O(n \log n)$$

## Physical Intuition / Derivation

### Why Omit Large Subtree Edges?

The key insight is that when routing in a tree, certain edges represent "heavy" (voluminous) branches. If you're at vertex $v$ and its subtree is already at least half the size of its parent $u$'s subtree, then the path segment $u \to v$ can be reconstructed during routing without explicit storage.

**The recursion works like this:**

1. Start with a path of $O(D)$ edges from root to $v$
2. Moving down the tree, whenever a subtree doubles in relative size, mark that edge for omission
3. Since subtree sizes can double at most $\log n$ times (going from 1 vertex to $n$ vertices), only $O(\log n)$ edges remain
4. The omitted edges can be found by a greedy downward search using the stored vertex numbers and subtree intervals

### Depth Separation in Communication

For distributed algorithms using routing tables, **depth separation** ensures no message congestion:
- Fragment $F_i$ performs its upcast communication at round $t = i + d(T) - d(v)$
- This staggered scheduling guarantees each vertex receives at most one message per fragment per round
- Vertices communicate about different fragments at different depths, eliminating contention

## Applications in Engineering

### 1. **Distributed Computing & Sensor Networks**
- Reduces memory overhead at resource-constrained nodes (edge devices, IoT sensors)
- Enables scalable convergecast/aggregation in sensor networks where all nodes report to a collection point
- Avoids message congestion in coordinated multi-fragment computations

### 2. **Telecommunication Networks**
- Compact routing tables for backbone routers handling $n \sim 10^6$ nodes
- Logarithmic label size allows fast lookup in hardware forwarding tables
- Particularly valuable in hierarchical network topologies

### 3. **Distributed Consensus & Agreement Protocols**
- Supports efficient leader election and information dissemination on tree topologies
- Used in consensus mechanisms requiring aggregation phases with bounded round complexity

### 4. **Mobile & Ad-Hoc Networks**
- Enables dynamic reconfiguration with minimal label updates
- Reduces control message overhead for topology maintenance

## Common Mistakes / Pitfalls

### ❌ Confusing Label Size with Routing Time
**Mistake**: Assuming $O(\log^2 n)$ label size means $O(\log^2 n)$ routing steps.
**Reality**: Labels are stored offline; routing to the root takes $O(\log n)$ hops, achieved by storing only $O(\log n)$ relevant edges.

### ❌ Missing the "At Most One" Constraint
**Mistake**: Thinking every edge on the root path can be omitted.
**Reality**: Each vertex has **exactly one** omittable edge (if any). Other edges must be retained because their subtrees don't meet the $\geq 1/2$ size threshold.

### ❌ Forgetting Metadata Overhead
**Mistake**: Believing routing tables contain only edge references.
**Reality**: The $O(\log n)$ bits budget includes vertex numbers and subtree interval information, which are essential for correct routing decisions.

### ❌ Assuming Symmetric Routing
**Mistake**: Using routing tables designed for root-directed routing (upcast) for arbitrary source-destination pairs.
**Reality**: TZ-scheme routing tables are optimized for directed paths toward a fixed root; general all-pairs routing requires different techniques.

### ❌ Ignoring Setup Costs
**Mistake**: Assuming the $O(\log n)$-bit tables appear for free.
**Reality**: Setup requires $O(D \log n)$ rounds and $O(n \log n)$ messages, which can dominate latency in dynamic networks.

## See Also

- [[tree decomposition]] – hierarchical structure underlying compact routing
- [[convergecast]] – upcast aggregation operation using routing tables in reverse
- [[compact routing scheme]] – general framework for distance-sensitive routing with sublinear state
- [[distributed algorithm]] – analysis framework (CONGEST model) for evaluating message/time complexity
- [[label assignment]] – technique for encoding routing information in vertex identifiers

## Sources

- Thorup & Zwick routing scheme analysis (referenced as [53] in source material)
- Formal analysis of TZ routing labels with $O(\log^2 n)$ bit complexity
- Convergecast cycle analysis with depth separation under CONGEST model communication constraints
- Communication cycle analysis in distributed computing with fragment-based aggregation