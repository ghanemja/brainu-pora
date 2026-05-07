# Streaming Algorithms

## Definition

A **streaming algorithm** is a computational procedure that processes a sequential data stream in a single pass (or a small number of passes) while using **sublinear space** in the input size. Rather than storing the entire dataset, streaming algorithms maintain a compact data structure that allows them to answer queries or produce outputs with controlled approximation guarantees.

Formally, a streaming algorithm $\mathcal{A}$ processes a stream $s = (e_1, e_2, \ldots, e_n)$ of $n$ elements, using space $S(n) \ll n$ (typically $S(n) = \operatorname{polylog}(n)$ or $O(\sqrt{n})$), and produces answers with approximation ratio $\alpha$ such that:

$$\text{answer} \leq \alpha \cdot \text{optimal solution}$$

For problems requiring fault tolerance (e.g., handling up to $f$ edge deletions in graphs), the space complexity is often expressed as $\tilde{O}(n\sqrt{f})$, where $\tilde{O}$ suppresses polylogarithmic factors.

## Key Equations

### Space-Stretch Tradeoff
For fault-tolerant distance oracles in graphs:

$$\text{Space} = \tilde{O}(n\sqrt{f}) \text{ bits, with stretch } O(\log n \log \log n)$$

This bypasses the classical $\Omega(nf)$ lower bound for spanners.

### Query Approximation Guarantee
For distance queries under $f$ faults:

$$\text{dist}_{G-F}(u,v) \leq \hat{d} \leq \alpha(n) \cdot \text{dist}_{G-F}(u,v)$$

where $|F| \leq f$, $\alpha(n) = O(\log^3 n)$ for poly-time algorithms, and $\alpha(n) = O(\log n \log \log n)$ for existential results.

## Physical Intuition / Derivation

### Why Streaming Is Necessary

In many real-world scenarios, data arrives too fast to store completely:
- **Network monitoring**: Monitoring packet flows where storing all packets is infeasible
- **Sensor networks**: Continuous data from thousands of sensors
- **Graph dynamics**: Edge insertions/deletions in evolving networks

### The Core Tension

Streaming algorithms must resolve a fundamental tradeoff:

$$\text{Accuracy} \leftrightarrow \text{Space Efficiency} \leftrightarrow \text{Query Time}$$

Storing nothing (zero space) gives zero information. Storing everything (linear space) trivializes the problem. Streaming algorithms find the sweet spot by:

1. **Extracting structure** rather than storing raw data (e.g., using expander decomposition to identify low-cut regions in graphs)
2. **Using randomization** to amplify weak signals (sketching techniques, sampling)
3. **Maintaining invariants** that remain valid under data insertion/deletion

### Expander Decomposition Framework

The source material reveals that streaming oracles rely on **expander decomposition**: partitioning a graph into expander components. This is powerful because:

- Expanders have small diameter relative to their size, so distances within an expander are predictable
- Distances between expanders go through few cut edges, which can be stored compactly
- A $\log n \log \log n$ stretch factor emerges directly from naive expander diameter bounds

This decomposition is the "unifying principle" mentioned that bypasses the $n \cdot f$ barrier.

## Applications in Engineering

### 1. **Network Monitoring & Cybersecurity**
- **Anomaly detection**: Streaming algorithms track network statistics (entropy, cardinality) without storing all packets
- **DDoS mitigation**: Identify heavy hitters (frequent sources) in near-real-time using count-min sketches
- **Space complexity**: $\operatorname{polylog}(n)$ for networks with $n$ flows

### 2. **Distributed & Fault-Tolerant Systems**
- **Distance oracles**: Query shortest paths in graphs with edge failures using $\tilde{O}(n\sqrt{f})$ space instead of $\Omega(nf)$
- **Resilient routing**: Route around up to $f$ failed edges with logarithmic stretch penalty
- **Data center networks**: Compact routing tables that tolerate equipment failures

### 3. **Data Stream Mining**
- **Approximate aggregation**: COUNT, SUM, AVERAGE queries with provable error bounds
- **Sliding window statistics**: Monitor time-series metrics over recent windows
- **Graph streaming**: Approximate MST, connectivity, and matching in graphs with insertion/deletion streams

### 4. **Machine Learning on Edge Devices**
- **Lightweight models**: Process sensor data with minimal memory (IoT, embedded systems)
- **Continuous learning**: Update model statistics without storing training data
- **Federated learning**: Compress model updates for communication efficiency

### 5. **Database Query Processing**
- **Cardinality estimation**: DISTINCT COUNT using hyperloglog sketches
- **Join size prediction**: Estimate result sizes before materializing joins
- **Memory-constrained environments**: Process larger-than-RAM datasets in single pass

## Common Mistakes / Pitfalls

### 1. **Confusing "Sublinear" with "Constant"**
Streaming algorithms use $o(n)$ space, but this can still be $\sqrt{n}$ or $\operatorname{polylog}(n)$. The source material achieves $\tilde{O}(n\sqrt{f})$—still linear in $n$, but with a $\sqrt{f}$ factor that improves over spanners' $\Omega(nf)$ bound.

**Mistake**: Assuming streaming = small constant space. **Reality**: Often $\text{space} = O(\sqrt{n})$ or $O(n^{2/3})$.

### 2. **Ignoring the Stretch-Space Tradeoff**
The $O(\log n \log \log n)$ stretch in Theorem 1.1 is not arbitrary—it comes directly from expander diameter bounds.

**Mistake**: Expecting constant stretch with sublinear space for arbitrary graphs. **Reality**: Polylogarithmic stretch