# Priority Queue

## Definition

A **priority queue** is an abstract data structure that maintains a collection of elements, each associated with a priority value, and supports the following core operations:

- **Insert(element, priority)**: Add an element with a given priority to the queue
- **ExtractMax()** (or ExtractMin()): Remove and return the element with the highest (or lowest) priority
- **Peek()**: View the highest-priority element without removing it
- **Update(element, new_priority)**: Modify the priority of an existing element

Unlike a standard queue (FIFO), elements are retrieved not in insertion order but in order of their priority. The priority value determines the ordering: higher priority elements are dequeued first in a max-heap variant, lower priorities in a min-heap variant.

## Key Equations

For a priority queue implemented as a balanced binary heap with $n$ elements:

$$
\text{Time Complexity} = \begin{cases}
O(\log n) & \text{Insert, Extract, Update} \\
O(1) & \text{Peek} \\
O(n \log n) & \text{Sort via repeated extraction}
\end{cases}
$$

For the **logarithmic method** decomposition mentioned in the source (partitioning into buckets $B_i$ of size $2^i$):

$$
\text{Total insertion time after } n \text{ insertions} = O(n \log n \log \log n)
$$

where each element participates in at most $O(\log n)$ merge operations across the $O(\log n)$ bucket levels.

## Physical Intuition / Derivation

### Why Priority Queues Matter

Consider a hospital emergency room. Patients arrive continuously (insertions), but they must be treated in order of medical urgency (priority), not arrival time. A standard queue would treat them FIFO, which is wrong. A priority queue naturally models this: critical patients have high priority and move to the front.

### Heap-Based Implementation

The most common implementation uses a **binary heap**, a nearly-complete binary tree where:
- **Max-heap property**: Each parent node has priority ≥ its children
- **Min-heap property**: Each parent node has priority ≤ its children

This tree structure ensures that:
1. The highest-priority element sits at the root (accessible in $O(1)$)
2. Insertions maintain heap property via "bubbling up" in $O(\log n)$ comparisons
3. Extractions restore the heap by moving the last element to the root and "sifting down"

The logarithm arises because a tree with $n$ nodes has height $\approx \log_2 n$, and these operations traverse at most the height.

### Application in Geometric Algorithms (from source)

In the convex hull context, a priority queue per x-coordinate stores all collinear points sorted by y-coordinate. Only the maximum-y point is retained for the algorithm proper. When a higher-y point arrives, it displaces the old maximum:

```
x-coordinate ──> Priority Queue (by y-value)
    x₁        ──> [(y₅, p₅), (y₃, p₃), (y₁, p₁)]  ──> Extract max: p₅
    x₂        ──> [(y₈, p₈), (y₂, p₂)]              ──> Extract max: p₈
```

This preprocessing handles the "general position" assumption violation elegantly.

## Applications in Engineering

### 1. **Operating System Scheduling**
Process schedulers (e.g., Linux CFS) use priority queues to determine which thread/process runs next, weighted by priority and fairness metrics.

### 2. **Network Routing & Packet Processing**
Routers maintain packet queues prioritized by Quality-of-Service (QoS) levels, ensuring critical traffic (VoIP, video) is processed before bulk data.

### 3. **Computational Geometry & Graphics**
- **Convex hull algorithms**: Partition points by x-coordinate using priority queues (as in the source material)
- **Sweep line algorithms**: Maintain events (line intersections, endpoint encounters) in priority-ordered queues keyed by x-coordinate
- **Ray tracing**: Intersections sorted by distance from viewpoint

### 4. **Dijkstra's & A* Pathfinding**
Priority queues store frontier nodes weighted by distance-to-source (Dijkstra) or estimated cost-to-goal (A*). Extract the lowest-cost node each iteration—infeasible without efficient priority selection.

### 5. **Event-Driven Simulation**
Physics engines, discrete event simulators (queueing networks, epidemiology models) process events in timestamp order. Event happens at smallest timestamp → extract it from priority queue.

### 6. **Data Compression & Huffman Coding**
Build Huffman trees by repeatedly extracting the two lowest-frequency symbols, encoding them, and re-inserting. Requires efficient min-extraction.

### 7. **Load Balancing**
Distributed systems assign tasks to servers with lowest current load (priority = negative load, or inverted). Priority queue tracks server status.

## Common Mistakes / Pitfalls

### 1. **Confusing Heap Property with Global Sorting**
A max-heap does **not** keep all elements in sorted order; only the root is guaranteed maximum. Extracting all elements gives a sorted sequence, but the heap itself is only partially ordered.

**Wrong assumption**: All elements are sorted in the heap.
**Correct**: Only parent ≥ children relationships hold.

### 2. **Forgetting Log Factor in Analysis**
Beginners sometimes state "insert is O(1)" or ignore the $\log n$ overhead when inserting many elements.

**Example mistake**: Thinking a priority queue takes $O(n)$ total time for $n$ insertions.
**Correct**: It takes $O(n \log n)$ total time.

### 3. **Ignoring Update Cost**
Some applications require updating a priority value mid-operation (e.g., Dijkstra's relaxation step). A naive implementation extracts the old element and re-inserts (costly). Efficient implementations use decrease-key/increase-key ($O(\log n)$), sometimes requiring a hash table index mapping elements to heap positions.

### 4. **Choosing Wrong Variant for Problem**
Min-heap vs. max