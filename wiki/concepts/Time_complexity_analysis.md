# Time Complexity Analysis

## Definition

**Time complexity analysis** is the formal study of how the execution time (or number of elementary operations) of an algorithm scales with respect to input size, typically expressed using asymptotic notation. It provides a machine-independent, input-size-dependent characterization of algorithmic efficiency.

Unlike wall-clock execution time, time complexity focuses on the *order of growth* of operations, allowing meaningful comparison between algorithms independent of hardware, compiler, and implementation details.

### Notation

- **Big-O** $O(f(n))$: upper bound; algorithm takes *at most* $f(n)$ operations
- **Theta** $\Theta(f(n))$: tight bound; algorithm takes *approximately* $f(n)$ operations
- **Omega** $\Omega(f(n))$: lower bound; algorithm takes *at least* $f(n)$ operations

## Key Equations

**General form:** For algorithm $A$ with input size $n$,
$$T(n) = O(f(n))$$

where $T(n)$ represents the number of primitive operations executed.

**Common complexity classes (ordered by growth rate):**
$$O(1) \subset O(\log n) \subset O(n) \subset O(n \log n) \subset O(n^2) \subset O(2^n) \subset O(n!)$$

**Specific examples from sorting algorithms:**

| Algorithm | Best Case | Average Case | Worst Case | Space |
|-----------|-----------|--------------|-----------|-------|
| Quicksort | $O(n \log n)$ | $O(n \log n)$ | $O(n^2)$ | $O(\log n)$ |
| Mergesort | $O(n \log n)$ | $O(n \log n)$ | $O(n \log n)$ | $O(n)$ |
| Introsort | $O(n \log n)$ | $O(n \log n)$ | $O(n \log n)$ | $O(\log n)$ |
| Radix Sort (bitwise) | $O(nw)$ | $O(nw)$ | $O(nw)$ | $O(n)$ or $O(w)$ |

where $w$ is the word size (bit-depth) of the data type.

## Physical Intuition / Derivation

### Why Asymptotic Analysis Matters

Consider two algorithms:
- **Algorithm A**: $T_A(n) = 100n$ operations (linear)
- **Algorithm B**: $T_B(n) = n^2$ operations (quadratic)

For small $n$:
- $n = 10$: A uses 1,000 ops; B uses 100 ops (B is faster)
- $n = 100$: A uses 10,000 ops; B uses 10,000 ops (comparable)
- $n = 1,000$: A uses 100,000 ops; B uses 1,000,000 ops (A is 10× faster)
- $n = 10,000$: A uses 1,000,000 ops; B uses 100,000,000 ops (A is 100× faster)

As input size grows, the **scaling behavior dominates** any constant factors. This is why we say $100n \in O(n)$ and $n^2 \in O(n^2)$—the constants matter little asymptotically.

### The Gap Between Theory and Practice

The source material illustrates a critical insight: **asymptotic complexity does not guarantee real-world performance**.

Example: Quicksort vs. Introsort
- **Theoretical**: Quicksort has worst-case $O(n^2)$, average $O(n \log n)$
- **Practice**: Introsort (a hybrid) matches quicksort's typical speed but guarantees $O(n \log n)$ worst-case by switching to heapsort when recursion depth becomes excessive

**Why the divergence occurs:**
1. **Constant factors**: Introsort's overhead in switching algorithms can be hidden by a large constant $c$ where $T = c \cdot n \log n$
2. **Cache locality**: Algorithms with better memory access patterns run faster despite identical asymptotic complexity
3. **Compiler optimization**: Instruction-level parallelism and branch prediction favor certain algorithm structures
4. **Data-dependent behavior**: Pivot selection in quicksort affects average vs. worst-case behavior in practice

### Bitwise Operations and Hybrid Algorithms

The bitwise partitioning algorithm (bsort) from the source demonstrates $O(nw)$ complexity:

$$T_{\text{bsort}}(n) = O(nw)$$

where:
- $n$ = number of elements
- $w$ = word size (8 bits for `char`, 64 bits for `long long`)

This is **linear in both** $n$ and $w$. For shallow bit-depths (small $w$), this beats comparison-based $O(n \log n)$ algorithms because:
$$nw < n \log n \quad \text{when} \quad w < \log n$$

However, experimental results show that **bsort's constant factors** become unfavorable for deep bit-widths, demonstrating the theory-practice gap.

## Applications in Engineering

### 1. **Algorithm Selection and Optimization**

In real-time systems (embedded, robotics, autonomous vehicles), algorithm choice is critical:
- **Hard deadline**: Must choose guaranteed $O(n \log n)$ introsort over unpredictable $O(n^2)$ quicksort
- **Batch processing**: Bitwise radix sort ($O(nw)$) preferred for large integer datasets where $w$ is small

### 2. **Database Query Optimization**

Query planners choose sort/join strategies based on complexity:
- Small table with complex predicate? Use $O(n^2)$ nested-loop join
- Large table? Use $O(n \log n)$ merge-join or hash-join

### 3. **Network Protocol Design**

Buffer management in routers must handle variable packet arrivals:
- Packet classification: $O(n)$ linear scan for tiny tables vs. $O(\log n)$ tree for large tables
- Decision point determined by expected