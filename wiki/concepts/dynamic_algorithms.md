# Dynamic Algorithms

## Definition

**Dynamic algorithms** are algorithms designed to efficiently maintain solutions to computational problems as the input changes incrementally over time. Rather than recomputing solutions from scratch after each modification, dynamic algorithms update existing solutions by exploiting the structure of the problem and the locality of changes.

More formally, a dynamic algorithm maintains a data structure that supports:
- **Update operations**: Insert, delete, or modify elements in the input
- **Query operations**: Answer questions about the current state of the input

The goal is to minimize the time per update and query operation, typically trading off against preprocessing time and space complexity.

### Key Distinction from Related Concepts
- **Static algorithms**: Compute a fixed answer for a given input (no updates)
- **Online algorithms**: Process input sequentially without knowledge of future elements
- **Streaming algorithms**: Process data in a single pass with limited memory

Dynamic algorithms often combine elements of all three paradigms.

## Key Equations

### Amortized Analysis Framework

For a sequence of $n$ operations, the **amortized cost per operation** is:

$$\text{Amortized Cost} = \frac{\text{Total Time for } n \text{ operations}}{n}$$

### Competitiveness in Online Settings

For problems with dynamic components, the **competitive ratio** measures performance:

$$C = \max_{\text{input sequence}} \frac{\text{Cost of online algorithm}}{\text{Cost of optimal offline algorithm}}$$

### Update Time vs. Query Time Trade-off

A fundamental relationship in dynamic data structures:

$$(\text{Update Time}) \times (\text{Query Time}) = \Omega(\log n)$$

This lower bound appears in many problems (e.g., dynamic connectivity, dynamic range queries) and represents an inherent trade-off in the design space.

## Physical Intuition / Derivation

### The Core Challenge

Consider maintaining a solution to a problem where the input changes:

1. **Naive approach**: Recompute from scratch after each change
   - Time per update: $O(n)$ or worse
   - Problem: Wasteful—most of the problem structure remains unchanged

2. **Dynamic approach**: Exploit locality
   - A small change (insert/delete one element) affects only a localized part of the solution
   - Update only affected components incrementally
   - Time per update: ideally $o(n)$, often $\text{poly}(\log n)$

### Incremental Thinking

The key insight is **decomposing changes**:

$$\text{Solution}(\text{Input} \cup \{\text{new element}\}) = \text{Update}(\text{Solution}(\text{Input}), \text{new element})$$

The update function can be much faster than the original algorithm if designed carefully.

### Trade-offs in Design

Three main design dimensions:

| Dimension | Cost | Relationship |
|-----------|------|--------------|
| **Update Time** | $U$ | Faster updates → more preprocessing |
| **Query Time** | $Q$ | Faster queries → more storage |
| **Space** | $S$ | More space → faster operations |

Different applications require different balances. For instance:
- Real-time systems prioritize small $U$
- Database systems often prioritize small $Q$
- Memory-constrained systems minimize $S$

## Applications in Engineering

### Database Systems
- **B-trees and variants**: Dynamically maintain sorted order with $O(\log n)$ insertion/deletion/search
- **Range queries**: Answer "find all records where $a \leq x \leq b$" efficiently as data changes
- Used in SQL indexes, NoSQL systems

### Network Routing
- **Dynamic shortest paths**: Maintain shortest paths as edge weights or connectivity changes
- Real-time GPS navigation systems that update routes as traffic conditions change
- Network reconfiguration after link failures

### Clustering and Machine Learning
- **Dynamic k-clustering**: Maintain cluster assignments as data points are added/removed
- **Streaming clustering**: Incrementally update clusters in online learning scenarios
- Semi-supervised learning where labeled data arrives over time

### Computational Geometry
- **Convex hull maintenance**: Incrementally add/remove points while maintaining the convex hull boundary
- **Nearest neighbor queries**: Dynamic spatial data structures (KD-trees, R-trees)
- Collision detection in graphics engines

### Linear Algebra in Streaming Settings
- **Online matrix sketching**: Maintain low-rank approximations as rows/columns are added
- **Sliding window linear algebra**: Solutions in streaming and sliding window models
- Reduces memory footprint from $O(n^2)$ to $O(\text{poly}(\log n))$

### Competitive Analysis & Resource Allocation
- **k-server problems**: Dynamically allocate servers to requests arriving online
- **Cache replacement**: Decide which items to keep as new requests arrive
- Approximation algorithms for online scheduling and packing problems

## Common Mistakes / Pitfalls

### 1. **Confusing Amortized vs. Worst-Case Bounds**
- Amortized $O(\log n)$ per operation does **not** guarantee every single operation takes $O(\log n)$ time
- Some operations may take $O(n)$ time, with others very fast
- Mistake: Using amortized bounds for hard real-time systems requiring strict worst-case guarantees

### 2. **Ignoring Space Complexity**
- Dynamic algorithms often require auxiliary data structures (e.g., auxiliary trees, sketches, summaries)
- Total space can exceed original input size
- Mistake: Only optimizing time complexity while space grows exponentially

### 3. **Forgetting the Offline Baseline**
- In competitive analysis, the "optimal offline algorithm" can see future operations
- A $2$-competitive online algorithm is often quite good because it's half the cost of the all-knowing adversary
- Mistake: Dismissing algorithms as "suboptimal" without considering the offline lower bound

### 4. **Over-Engineering for Worst Case**
- Sometimes the average case (amortized analysis) is what matters in practice
- Making every operation $O(\log n)$ in worst case can add unnecessary constants
- Mistake: Implementing unnecessary complexity for theoretical guarantees not needed by application

### 5. **Not Considering Update Patterns**
- Different application domains have different update distributions
- Batch updates vs. single updates vs. adversarial updates
- Mistake: Choosing a data structure optimal for random updates when application sees sequential patterns

### 6. **Memory Hierarchy