# Binary Search

## Definition

**Binary search** is a divide-and-conquer algorithm for locating a target value within a **sorted sequence** by repeatedly dividing the search space in half. Given a sorted array or list, binary search eliminates half of the remaining candidates with each comparison, achieving logarithmic time complexity.

**Formal definition:** Given a sorted sequence $\mathbf{a} = [a_1, a_2, \ldots, a_n]$ where $a_i \leq a_{i+1}$, and a target value $x$, binary search returns an index $i$ such that $a_i = x$ (if $x$ exists), or indicates that $x$ is not present.

## Key Equations

**Time Complexity:**
$$T(n) = O(\log n)$$

where $n$ is the size of the search space. Each iteration reduces the search space by a factor of 2:
$$n \to \frac{n}{2} \to \frac{n}{4} \to \cdots \to 1$$

Maximum number of iterations:
$$k = \lceil \log_2 n \rceil$$

**Space Complexity:**
- Iterative implementation: $O(1)$ (constant extra space)
- Recursive implementation: $O(\log n)$ (call stack depth)

## Physical Intuition / Derivation

### Why Binary Search Works

Imagine searching for a name in a phone book. Rather than reading sequentially from page 1, you open to the middle:
- If your target comes alphabetically *before* the middle, discard everything after
- If your target comes *after*, discard everything before
- Repeat on the remaining half

Each comparison eliminates **half** the remaining candidates. After $k$ comparisons, you've narrowed down from $n$ possibilities to $n/2^k$. Setting $n/2^k = 1$ and solving:
$$2^k = n \implies k = \log_2 n$$

### Precondition: Sorted Data

Binary search **requires** the input sequence to be sorted. This is crucial: the algorithm exploits the ordering to eliminate regions of the search space without examining them. On unsorted data, binary search gives incorrect results.

### Algorithm Pseudocode

```
function binarySearch(array, target):
    left = 0
    right = length(array) - 1
    
    while left ≤ right:
        mid = floor((left + right) / 2)
        
        if array[mid] == target:
            return mid
        else if array[mid] < target:
            left = mid + 1          // target in right half
        else:
            right = mid - 1         // target in left half
    
    return NOT_FOUND
```

## Applications in Engineering

### 1. **Database Query Optimization**
- **B-trees and indexed databases** use binary search principles to locate records in sorted key spaces in $O(\log n)$ time rather than $O(n)$ linear scan.
- Example: Finding a customer record by ID in a million-record table.

### 2. **Software Verification & Debugging**
- **Regression testing**: Pinpointing which of 100 commits introduced a bug using binary search on the commit history. Each test eliminates half the candidates.
- Known as "**git bisect**" in version control systems.

### 3. **Range Queries in Graphs & Hypergraphs**
In the source material, binary search is used to verify membership conditions:
> "The condition $u \in N_{\leq\alpha}(v)$ can be verified in time $O(\log |V|)$ via binary search as $N_{\leq\alpha}(v)$ is sorted and has size at most $|V|$."

This enables efficient hypergraph motif enumeration by quickly checking neighbor relationships.

### 4. **Numerical Root Finding**
- **Bisection method** for solving $f(x) = 0$: If $f$ is continuous and $f(a) \cdot f(b) < 0$, repeatedly bisect the interval $[a,b]$ to converge to the root.

### 5. **Parameter Tuning in ML/Signal Processing**
- **Threshold detection**: Finding the optimal threshold value in a sorted confidence score array.
- **Hyperparameter search**: Binary search on learning rates or regularization strengths (useful when response is unimodal).

### 6. **Distributed Systems**
- Locating data shards or partitions in distributed key-value stores using binary search on sorted shard boundaries.

## Common Mistakes / Pitfalls

### 1. **Forgetting to Sort**
**Mistake:** Applying binary search to unsorted data.
```python
# WRONG: array is not sorted
arr = [5, 1, 9, 3, 7]
binarySearch(arr, 9)  # May return incorrect result
```
**Fix:** Sort first, or ensure invariant is maintained.

### 2. **Off-by-One Errors**
**Mistake:** Incorrect boundary conditions.
```python
# WRONG: mid = (left + right) / 2 can overflow for large integers
mid = (left + right) // 2

# CORRECT: avoids overflow
mid = left + (right - left) // 2
```

### 3. **Exclusive vs. Inclusive Bounds**
Mixing `left < right` with `left ≤ right` causes infinite loops or missed values.

```python
# CORRECT loop condition: left ≤ right ensures all elements checked
while left <= right:
    mid = left + (right - left) // 2
    if array[mid] == target:
        return mid
    elif array[mid] < target:
        left = mid + 1
    else:
        right = mid - 1
```

### 4. **Assuming Uniqueness**
If duplicates exist, basic binary search finds *a* match, not necessarily the first or last. Use variants for finding leftmost/rightmost occurrence.

### 5. **Performance Assumptions on "Almost Sorted" Data**
Binary search **requires strict sorting**. Near-sorted data still requires full sort preprocessing; no "partial credit" for near-linear orderings.

## See Also

- [[Divide-and-Conquer Algorithms]] – paradigm