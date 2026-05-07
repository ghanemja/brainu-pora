# Memory complexity O(log n)

## Definition

**Memory complexity $O(\log n)$** describes an algorithm or protocol whose memory requirement grows logarithmically with the input size $n$. In distributed systems and network algorithms, this typically refers to the maximum memory any single processor/node must maintain during execution.

Formally, an algorithm has memory complexity $O(\log n)$ if there exists a constant $c$ such that the memory required by any node is bounded by:

$$M(n) \leq c \cdot \log n$$

for all sufficiently large $n$.

In the context of **fragment-based MST/MSF algorithms** (particularly the GKP phase), logarithmic memory arises because:
- Fragments are hierarchically merged in phases
- The fragment hierarchy has depth $O(\log n)$
- Each node need only maintain state for fragments at its current level and immediate neighbors

## Key Equations

For fragment-merging algorithms operating in $k$ phases:

$$\text{Memory per node} = O(k) = O(\log n)$$

where the number of phases $k$ satisfies:
$$n_0 \to n_1 \to \cdots \to n_k$$

with each phase reducing the fragment count by a constant factor (e.g., $n_{i+1} \geq 2 \cdot n_i$ in size, or equivalently $\text{fragments}_{i+1} \leq \text{fragments}_i / 2$).

Depth of hierarchy:
$$k = \lceil \log_2 n \rceil = O(\log n)$$

## Physical Intuition / Derivation

### Why Hierarchical Merging Produces $O(\log n)$ Memory

Consider a bottom-up fragment merging process:

1. **Initial state**: $n$ nodes, each is its own fragment
2. **Phase 1**: Fragments merge in pairs or small groups → fragment count drops by constant factor
3. **Phase $i$**: Current fragment count $\approx n / 2^i$
4. **Termination**: After $k = \log n$ phases, one fragment (the MST) remains

**Key insight**: Each node only needs to remember:
- Its current fragment identifier
- Pointers to parent/child fragments in the hierarchy  
- Edges crossing fragment boundaries
- A constant amount of communication state per level

Since there are $O(\log n)$ levels in this hierarchy, total memory is $O(\log n)$ per node.

### Example: The GKP Phase

In Claim 2.1, the GKP phase maintains three message types:
1. Parent → children (broadcast within fragment)
2. Parent → one child (unicast)
3. Child → parent (upward aggregation)

This tree-like communication pattern naturally fits in $O(\log n)$ memory because:
- Tree depth = $O(\log n)$ for balanced fragment structures
- Each node stores only its position in the tree
- Aggregation replies flow bottom-up in a single pass

## Applications in Engineering

### 1. **Distributed MST Algorithms**
- Lenzen's phase and GKP phase use $O(\log n)$ memory per processor
- Critical for large-scale distributed systems where memory is limited
- Enables MST computation on networks with millions of nodes

### 2. **Sensor Networks & IoT**
- Wireless sensor networks require minimal per-node storage
- $O(\log n)$ memory allows nodes to remain active longer (lower power)
- Applicable to Minimum Spanning Forest construction for network topology

### 3. **Parallel & GPU Computing**
- Each thread/core maintains $O(\log n)$ state during tree reduction operations
- Relevant for prefix sums, scan operations, and hierarchical aggregations
- Allows massive parallelism on thousands of cores with bounded shared memory

### 4. **Hierarchical Clustering**
- Clustering algorithms using bottom-up merging (like single-linkage) use $O(\log n)$ memory
- Each node remembers only its position in the cluster hierarchy

### 5. **Network Routing Protocols**
- Link-state protocols that build spanning trees can use logarithmic memory
- Base fragment approach (Claim 2.2) partitions network into regions, reducing routing table size

## Common Mistakes / Pitfalls

| Mistake | Correction |
|---------|-----------|
| **Confusing total vs. per-node memory** | $O(\log n)$ applies *per node*, not total system memory. Total is $O(n \log n)$. |
| **Assuming $O(\log n)$ is "always small"** | For $n = 2^{30}$ (1 billion nodes), $\log n \approx 30$ units—still substantial. Context matters. |
| **Forgetting constant factors** | $O(\log n)$ hides significant constants. Practical algorithms may have $100 \log n$ or $1000 \log n$ memory. |
| **Mixing with time complexity** | Memory and time complexity are independent. An algorithm can be $O(\log n)$ memory but $O(n^2)$ time. |
| **Assuming balancedness automatically** | Achieving $O(\log n)$ memory requires *careful algorithm design*. Naïve merging may create unbalanced trees with $O(n)$ depth. |

## See Also

- [[Minimum Spanning Tree (MST)]] – foundational problem where this complexity appears
- [[Borůvka's Algorithm]] – fragment-merging approach underlying these results
- [[Distributed Graph Algorithms]] – algorithms designed for networked settings
- [[Time-Message Trade-offs in Distributed Computing]] – balancing complexity metrics
- [[Fragment-based Graph Processing]] – general framework for hierarchical decomposition

## Sources

- **[16]** Deterministic time- and message-efficient MST algorithm with logarithmic memory bounds
- **[24]** GKP phase (Claim 2.1): message types and memory complexity analysis
- **[41]** Lenzen's phase optimization for balanced fragment growth
- **[47]** Randomized precursor to deterministic message-efficient algorithms
- **Appendix A.2.2** (source material): Detailed proof of GKP phase $O(\log n)$ memory
- **Appendix A.2.3** (source material): Memory-efficient implementation of Lenzen