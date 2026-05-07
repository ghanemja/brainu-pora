# Filter

## Definition

A **filter** is a parallel algorithm primitive that takes an array $A$ and a predicate (boolean function) $P$ as input, and produces a new array containing exactly those elements $a \in A$ for which $P(a)$ evaluates to true, **preserving the original relative order** of the selected elements.

Formally, given an array $A = [a_1, a_2, \ldots, a_n]$ and predicate $P: A \to \{\text{true}, \text{false}\}$, the filter operation produces:
$$\text{Filter}(A, P) = [a_{i_1}, a_{i_2}, \ldots, a_{i_k}]$$
where $i_1 < i_2 < \cdots < i_k$ are all indices such that $P(a_{i_j}) = \text{true}$.

### Key Properties

- **Order preservation**: The filtered elements maintain their relative positions from the original array
- **Deterministic size**: The output size $k$ is determined by the number of elements satisfying $P$
- **Non-reordering**: Differs from [[partition]], which only requires grouping of elements, not order preservation

## Key Equations

### Complexity Bounds

**Work complexity**: $O(|A|)$ 
- Each element is examined exactly once, with constant work per element

**Depth complexity**: $O(\log |A|)$
- Achieved through parallel prefix sum (scan) operations

### Implementation via Scan

The standard implementation uses [[scan]] operations:

1. **Mark phase**: Create a binary array $M$ where $M[i] = 1$ if $P(a_i)$ is true, else $0$
2. **Scan phase**: Compute exclusive prefix sum $S = \text{ExclusiveScan}(M, +)$
   - $S[i]$ gives the count of selected elements before position $i$
3. **Gather phase**: Output element $a_i$ to position $S[i]$ if $M[i] = 1$

If $m = S[n-1] + M[n-1]$ is the total selected count, this produces the filtered array of size $m$.

## Physical Intuition / Derivation

### Sequential Perspective
In sequential algorithms, filtering is trivial: iterate through the array once, keeping elements that satisfy $P$. However, this is inherently sequential due to the variable output size.

### Parallel Challenge
The key difficulty in parallelization is **not knowing output positions a priori**. Consider filtering $[1, 2, 3, 4, 5]$ with $P(x) = (x \text{ is even})$. Element $3$ doesn't know it should go to position $2$ in the output without knowing how many elements *before* it were selected.

### Solution via Prefix Sums
The scan-based approach solves this by:
1. **Computing position offsets in parallel**: The prefix sum $S$ efficiently tells every element its output position
2. **Enabling parallel output writes**: Once positions are known, all elements can write their output simultaneously with no conflicts
3. **Maintaining order through inclusive accounting**: The prefix sum structure inherently preserves relative order

This transforms a seemingly sequential problem into one with logarithmic depth.

## Applications in Engineering

### 1. **Database Query Processing**
Filtering datasets based on conditions (e.g., "SELECT * WHERE salary > 50000") is fundamental. GPU-accelerated databases use parallel filters to process millions of records efficiently.

### 2. **Graphics and Image Processing**
- Removing invalid pixels or polygons (e.g., backface culling in 3D rendering)
- Extracting image regions satisfying intensity criteria
- Particle system culling based on visibility or lifecycle predicates

### 3. **Machine Learning Data Pipelines**
- Preprocessing: removing outliers, filtering by feature ranges
- Batch construction: selecting relevant training samples based on difficulty scores
- Inference: filtering detection results by confidence thresholds

### 4. **Signal Processing**
- Windowing operations: extracting signal segments meeting energy thresholds
- Anomaly detection: filtering time-series data to identify outliers
- Feature extraction: selecting significant frequency components

### 5. **Parallel Simulation**
- Particle filtering: removing particles below importance thresholds
- Agent-based modeling: selecting active agents by state predicates
- Mesh processing: removing degenerate or low-quality elements

### 6. **Network Packet Processing**
- Firewall rules: filtering packets by IP, port, protocol
- Traffic analysis: selecting packets of interest for inspection
- Load balancing: routing packets based on header criteria

## Common Mistakes / Pitfalls

### 1. **Confusing Filter with Partition**
**Mistake**: Thinking filter and partition are equivalent because both select elements.
**Reality**: Filter preserves order and produces a compact output; partition reorders elements into two groups. Use partition when you need two output streams but don't care about relative ordering within each.

### 2. **Underestimating Output Size Variability**
**Mistake**: Assuming average-case output sizes without accounting for worst cases.
**Reality**: If $P$ is very selective (e.g., only 0.1% of elements pass), most output space is wasted. Conversely, if $P$ is very permissive, memory requirements spike. Consider dynamic [[allocation]] strategies.

### 3. **Naïve Implementation with Load Imbalance**
**Mistake**: Assigning threads to contiguous input chunks without coordinating output positions.
**Reality**: This causes serialization bottlenecks. Always use a global scan-based position calculation to enable truly parallel writes.

### 4. **Order Preservation Overhead**
**Mistake**: Assuming order-preserving filter has the same cost as unordered filtering.
**Reality**: The prefix sum required for order preservation adds significant overhead. If order is irrelevant, use partition instead.

### 5. **Cache Inefficiency**
**Mistake**: Ignoring memory access patterns when gathering scattered outputs.
**Reality**: Parallel gathers based on computed positions can cause cache misses. Consider blocked/chunked variants if locality matters.

## See Also

- [[Partition]] — Related primitive that groups elements without order preservation
- [[Scan]] — Fundamental parallel primitive used to implement filters
- [[Reduce]] — Complementary primitive for aggregate computations