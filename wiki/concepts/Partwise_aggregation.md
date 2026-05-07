# Partwise Aggregation

## Definition

**Partwise aggregation** is a distributed algorithmic technique for computing aggregate functions (such as summation, minimum, maximum, or other associative operations) over a network partitioned into disjoint subsets, where each partition independently computes a local aggregate and these local results are then combined hierarchically.

In the context of distributed computing on networks, partwise aggregation decomposes a global aggregation problem into:
1. **Local aggregation phase**: Each partition $P_i$ of the network computes an aggregate over its members
2. **Inter-partition aggregation phase**: Local results from partitions are combined to produce the global result

The key advantage is that partwise aggregation enables **memory-efficient** distributed algorithms by allowing vertices to discard information after their partition-level computation completes, rather than maintaining global state.

## Key Equations

For a set of values $\{v_1, v_2, \ldots, v_n\}$ distributed across a network partitioned into $k$ disjoint subsets $P_1, P_2, \ldots, P_k$:

**Local aggregation:**
$$a_i = \bigoplus_{v_j \in P_i} v_j$$

where $\bigoplus$ denotes an associative aggregate operator (e.g., $\min$, $\max$, $+$).

**Global result:**
$$A = \bigoplus_{i=1}^{k} a_i$$

**Time complexity for partwise aggregation** (general form):
$$T_{\text{total}} = T_{\text{local}} + T_{\text{combine}} = O(D_P) + O(D_{\text{inter}})$$

where $D_P$ is the diameter within partitions and $D_{\text{inter}}$ is the effective diameter of the inter-partition aggregation tree.

## Physical Intuition / Derivation

### Why Partwise Aggregation Matters

Standard distributed aggregation algorithms require each vertex to maintain information about the entire global state, leading to **$\Omega(n \log n)$ memory** per vertex in many cases.

**Partwise aggregation breaks this bottleneck** through a hierarchical, multi-phase approach:

1. **Phase 1 (Local Aggregation)**: Within each partition $P_i$, vertices collaboratively compute $a_i$. This requires only local communication and memory proportional to partition size.

2. **Phase 2 (Partition Cleanup)**: Vertices can now discard partition-internal data. Only the partition representative (or a small set) needs to retain $a_i$.

3. **Phase 3 (Inter-partition Aggregation)**: A much smaller problem—combining $k$ partition results—is solved hierarchically. This incurs minimal memory overhead.

### Memory Efficiency Gain

- **Naive aggregation**: Each vertex stores information about all $n$ vertices → $\Omega(n \log n)$ bits per vertex
- **Partwise aggregation**: Each vertex stores information about $O(n/k)$ local neighbors plus $O(\log k)$ inter-partition routing state → $O\left(\frac{n}{k} + \log k\right)$ bits per vertex

For $k = \Theta(\sqrt{n})$ partitions, memory per vertex drops to **$O(\sqrt{n})$**, a substantial improvement.

## Applications in Engineering

### 1. Distributed Minimum Spanning Tree (MST)

The primary application highlighted in the source material. Partwise aggregation yields an algorithm that is simultaneously:
- **Time-optimal**: $O(D + \sqrt{n} \log^* n)$ rounds
- **Message-optimal**: $O(m + n^{3/2})$ messages  
- **Memory-optimal**: $O(\log n)$ bits per vertex

This addresses the real deployment challenge: prior algorithms sacrificed one optimality dimension for the others.

### 2. Wireless Sensor Networks

In large-scale sensor deployments, memory on each node is severely constrained. Partwise aggregation enables:
- Computing network-wide statistics (min/max temperature, average humidity) without centralizing all data
- Reducing energy consumption by limiting storage overhead
- Graceful degradation as nodes fail (local partitions remain functional)

### 3. Distributed Machine Learning

Federated learning systems use partwise aggregation to:
- Train models on local data partitions (e.g., data from geographic regions)
- Aggregate local model updates rather than raw data
- Preserve privacy while combining global insights

### 4. Peer-to-Peer (P2P) Networks

Computing aggregate metrics (total files, network capacity, active peers) over decentralized networks without centralizing state.

### 5. Data Center Networks

Aggregating telemetry from thousands of servers, where memory constraints on network switches or aggregation points necessitate hierarchical combination of metrics.

## Common Mistakes / Pitfalls

### 1. **Assuming All Aggregation Operations Are Partwise-Compatible**

Not all functions decompose cleanly. Partwise aggregation requires operators to be **associative and commutative**:
$$\text{INCORRECT}: \text{Computing medians or percentiles via partwise aggregation}$$
$$\text{CORRECT}: \min, \max, \sum, \text{ bitwise-AND, bitwise-OR}$$

Quantiles and order statistics are *not* partwise-aggregable without additional state.

### 2. **Neglecting Inter-Partition Overhead**

The inter-partition aggregation phase can become a bottleneck if partitions are not sized carefully. Simply creating many small partitions increases $D_{\text{inter}}$ and defeats the purpose.

**Correct approach**: Balance partition size so that $D_P \approx D_{\text{inter}}$, giving overall complexity $O(D + \sqrt{n} \log^* n)$ rather than $O(n)$.

### 3. **Ignoring Load Balancing**

If partitions have vastly different sizes, vertices in large partitions still face $\Omega(n \log n)$ memory. Partitions should be roughly equal, achieved via graph partitioning algorithms (e.g., spectral partitioning, recursive bisection).

### 4. **Conflating with Simple Hierarchical Aggregation**

A simple tree-based aggregation (e.g., balanced binary tree) is *not*