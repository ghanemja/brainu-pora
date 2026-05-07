# binary search algorithm

## Definition

A **binary search algorithm** is a divide-and-conquer search technique that efficiently locates a target value within a **sorted dataset** by repeatedly dividing the search space in half. The algorithm maintains a search interval $[L, R]$ and compares the target with the midpoint element, eliminating half the remaining candidates in each iteration.

In its classical form, binary search operates on a **linearly ordered structure** (typically an array or list) and returns the position of a target element or indicates its absence.

### Formal Specification

Given:
- A **sorted sequence** $A = [a_0, a_1, \ldots, a_{n-1}]$ where $a_i \leq a_{i+1}$
- A **target value** $x$

The algorithm maintains invariants:
- All elements in $A[0 \ldots L-1]$ are $< x$
- All elements in $A[R+1 \ldots n-1]$ are $> x$
- The answer (if it exists) lies in $A[L \ldots R]$

## Key Equations

**Time Complexity:**
$$T(n) = O(\log n)$$

This logarithmic complexity arises because the search space halves with each comparison, requiring at most $\lceil \log_2 n \rceil$ iterations.

**Number of iterations to reduce $n$ elements to 1:**
$$k = \lceil \log_2 n \rceil$$

**Midpoint calculation (guards against overflow):**
$$m = L + \lfloor (R - L) / 2 \rfloor$$

**Search space reduction:**
$$|S_{i+1}| = \frac{|S_i|}{2}$$

where $S_i$ denotes the search interval at iteration $i$.

## Physical Intuition / Derivation

### Why Binary Search Works

Binary search exploits the **sorted structure** of the dataset. Consider searching a phonebook:
- Rather than scanning every name sequentially (linear search, $O(n)$), you open to the middle
- If the target name comes alphabetically after the midpoint, eliminate the first half
- Repeat on the remaining half

Each step **halves** the problem size, leading to exponential reduction.

### Why Not Linear?

**Linear search** examines elements sequentially: $1, 2, 3, \ldots, n$
- Worst case: $O(n)$ comparisons
- Average case: $O(n/2) = O(n)$ comparisons
- No exploitation of order structure

**Binary search** jumps to the middle:
- Worst case: $O(\log n)$ comparisons
- Best case: $O(1)$ (found at first midpoint)
- Exponentially faster for large $n$

### The Correctness Argument

The algorithm maintains the **loop invariant**: "if $x$ exists in $A$, it is in $A[L \ldots R]$."

1. **Initialization:** $L = 0, R = n-1$ includes the entire array → invariant holds
2. **Maintenance:** At each step:
   - Compute $m = \lfloor (L+R)/2 \rfloor$
   - If $A[m] = x$, found it
   - If $A[m] < x$, set $L = m+1$ (eliminate left half, invariant holds)
   - If $A[m] > x$, set $R = m-1$ (eliminate right half, invariant holds)
3. **Termination:** When $L > R$, the invariant guarantees that $x$ is not in $A$

### Application to Broader Structures

The source material demonstrates binary search applied in **graph reconstruction contexts**, where the algorithm is used to:
- Navigate a **layering tree** $T$ in a graph $G$
- Perform a "binary search type algorithm" in $T_k$ (subtree of first $k$ layers)
- Couple binary search with exhaustive search within layers to minimize shortest path queries

This shows binary search generalizes beyond linear arrays to **tree and graph structures** when traversing hierarchical decompositions.

## Applications in Engineering

### 1. **Database Systems**
- **B-trees and B+ trees:** Binary search on sorted keys in database indices enables $O(\log n)$ lookups in datasets with billions of records
- Example: Finding a specific record by primary key in a relational database

### 2. **Signal Processing & Control**
- **Frequency sweep algorithms:** Binary search to find resonant frequencies in systems
- **Root-finding methods:** Bisection method (a binary search variant) for solving $f(x) = 0$

### 3. **Networking & Distributed Systems**
- **Graph reconstruction** (as in source material): Determining graph structure from shortest-path queries using binary search on layering trees
- **Load balancing:** Binary search to find optimal partition points in distributed datasets

### 4. **Hardware Design**
- **Memory hierarchies:** Binary search used in cache coherence protocols
- **FPGA routing:** Finding paths in interconnect networks

### 5. **Machine Learning**
- **Hyperparameter tuning:** Binary search over learning rates or regularization parameters
- **Model selection:** Identifying decision boundaries in classification problems

### 6. **Computational Geometry**
- **Spatial queries:** Binary search on sorted coordinates for range searching in 2D/3D spaces
- **Collision detection:** Finding intersection points using binary search on parameterized curves

## Common Mistakes / Pitfalls

### 1. **Forgetting to Check if Data is Sorted**
❌ **Error:** Applying binary search to unsorted arrays
```
A = [3, 1, 4, 1, 5, 9, 2, 6]  // NOT sorted!
// Binary search will fail unpredictably
```
✓ **Correct:** Always verify $a_i \leq a_{i+1}$ or sort first

### 2. **Off-by-One Errors in Index Calculation**
❌ **Common mistake:**
```
m = (L + R) / 2  // Integer overflow risk in some languages
```
✓ **Correct:**
```
m = L + (R - L) / 2  // Avoids overflow, equivalent