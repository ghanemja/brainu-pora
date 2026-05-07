# Heap Data Structure

## Definition

A **heap** is a specialized tree-based data structure that satisfies the **heap property**: for every node in the tree, the value at that node is either greater than or equal to (max-heap) or less than or equal to (min-heap) the values at its children.

### Formal Definition (Binary Heap)

A binary heap is a **complete binary tree** where:
- **Structure property**: All levels are fully filled except possibly the last, which is filled left-to-right
- **Heap property**: 
  - **Max-heap**: $\text{Parent}(i) \geq \text{Child}(i)$ for all nodes $i$
  - **Min-heap**: $\text{Parent}(i) \leq \text{Child}(i)$ for all nodes $i$

In array representation with 1-based indexing:
- Left child of node $i$: index $2i$
- Right child of node $i$: index $2i+1$
- Parent of node $i$: index $\lfloor i/2 \rfloor$

### Generalized Heaps

The heap concept extends beyond binary heaps:
- **$d$-ary heap**: Each node has up to $d$ children
- **Fibonacci heap**: Lazy consolidation structure with amortized performance guarantees
- **Unified bound heaps**: Novel structures (as in the source material) optimizing performance across multiple operations

## Key Equations

### Time Complexity (Binary Heap)

$$
\begin{align}
T_{\text{insert}} &= O(\log n) \\
T_{\text{delete-min}} &= O(\log n) \\
T_{\text{heapify}} &= O(n) \\
T_{\text{build-heap}} &= O(n)
\end{align}
$$

where $n$ is the number of elements.

### $d$-ary Heap Trade-off

For a $d$-ary heap with $n$ elements:

$$
\begin{align}
T_{\text{insert}} &= O(\log_d n) \\
T_{\text{delete-min}} &= O(d \log_d n) \\
\text{Height} &= \Theta(\log_d n)
\end{align}
$$

### Heap Sort Complexity

$$T_{\text{heap-sort}} = O(n \log n)$$

Achieved via: build heap $O(n)$ + $n$ deletions $\times O(\log n)$ per deletion.

## Physical Intuition / Derivation

### Why Heaps Achieve $O(\log n)$ Operations

The heap exploits a **hierarchical comparison structure**:

1. **Binary search tree property generalization**: While BSTs maintain global order through pairwise comparisons, heaps maintain only **local order** (parent-child relationships). This reduces constraint overhead.

2. **Complete binary tree geometry**: The constraint that the tree be complete ensures:
   - Height is $\Theta(\log n)$ for any orientation (no skew)
   - All levels are balanced, enabling array representation without gaps

3. **Sift-up vs. Sift-down**:
   - **Sift-up** (insertion): Bubble new element up by comparing with parent, at most $\log n$ steps
   - **Sift-down** (deletion): Bubble root down by comparing with children, at most $\log n$ steps
   - Each operation follows a single path from leaf to root (or vice versa)

### Why Building a Heap is Linear

The classic result that `build-heap` is $O(n)$ (not $O(n \log n)$) follows from:

$$\sum_{i=1}^{n} \text{(cost to sift down node at level } i) = \sum_{i=0}^{\log n} \frac{n}{2^{i+1}} \cdot i = O(n)$$

The sum telescopes because the cost decreases geometrically with level height.

### Context: Sorting Under Partial Information

The source material introduces **unified bound heaps** as a refinement to standard heaps, optimizing for the specific problem of sorting under partial order constraints. These heaps enable:

- **Preprocessing**: Building an implicit partial order in $O(m)$ time
- **Query**: Extracting elements in sorted order with only $O(\log e(G))$ comparisons, where $e(G)$ is the number of linear extensions of the partial order $G$

This represents a fundamental advance: instead of worst-case $O(\log n!)$ comparisons needed classically, the algorithm adapts to the actual information entropy of the input.

## Applications in Engineering

### 1. **Priority Queues** (Operations Research, Scheduling)
- Task scheduling in operating systems (process priority queues)
- Event simulation: discrete event systems maintain next-event via min-heap
- Network routing (Dijkstra's algorithm for shortest paths uses binary heaps)

### 2. **Sorting and Sorting Networks**
- Heap sort for in-place sorting when space is critical
- Partial sorting: extract $k$ largest elements in $O(n + k \log n)$
- Sorting under partial information (source context): accelerate sorting when partial ordering is already known

### 3. **Load Balancing and Resource Allocation**
- Load-aware task distribution: maintain heap of server utilization
- Memory management: priority-based allocation policies
- Cache replacement: min-heap tracks least-recently-used blocks

### 4. **Graph Algorithms**
- **Dijkstra's shortest path**: $O((V + E) \log V)$ with binary heap
- **Prim's minimum spanning tree**: maintain candidate edges in min-heap
- **A\* search**: open set as priority queue ordered by heuristic cost

### 5. **Online Algorithms**
- **Median finding**: dual heaps (max-heap for left half, min-heap for right)
- **Top-$k$ elements**: maintain min-heap of size $k$
- **Streaming data**: approximate statistics via heap-based sketches

### 6. **Advanced Data Structures**
- **Fibonacci heaps** in theoretical computer science: amortized $O(1)$ decrease-key enables optimal MS