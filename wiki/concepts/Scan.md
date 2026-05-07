# Scan

## Definition

A **scan** (also called a **parallel prefix sum** or **prefix scan**) is a fundamental parallel algorithm that computes the sequence of all prefix results of an array under an associative binary operator.

Formally, given:
- An array $A = [a_1, a_2, \ldots, a_n]$
- An associative binary operator $\oplus$

The scan produces the output array $B = [b_1, b_2, \ldots, b_n]$ where:

$$b_i = a_1 \oplus a_2 \oplus \cdots \oplus a_i$$

The operator $\oplus$ must be **associative** (though not necessarily commutative), meaning:
$$(x \oplus y) \oplus z = x \oplus (y \oplus z)$$

**Exclusive vs. Inclusive:**
- **Inclusive scan** (shown above): $b_i$ includes $a_i$
- **Exclusive scan**: $b_i = a_1 \oplus \cdots \oplus a_{i-1}$ (excludes $a_i$)

## Key Equations

### Work and Depth

For an array of size $n$ with an operator $\oplus$ taking $O(1)$ time:

$$\text{Work} = O(n)$$

$$\text{Depth} = O(\log n)$$

Where **work** is the total number of instructions and **depth** is the longest chain of data-dependent operations.

### Prefix Recurrence

The output satisfies the recurrence:
$$b_i = \begin{cases}
a_1 & \text{if } i = 1 \\
b_{i-1} \oplus a_i & \text{if } i > 1
\end{cases}$$

## Physical Intuition / Derivation

### Serial Algorithm
The naive sequential scan simply computes each prefix one at a time:

```
B[0] = A[0]
for i = 1 to n-1:
    B[i] = B[i-1] ⊕ A[i]
```

This takes $O(n)$ work and $O(n)$ depth—unsuitable for parallel hardware.

### Parallel Construction via Work-Efficient Scan

The parallel scan achieves $O(\log n)$ depth through a **two-phase** approach:

**Phase 1 (Up-sweep / Reduction):** Build a binary tree of partial results bottom-up, reducing depth by half at each level. This requires $O(n)$ work and $O(\log n)$ depth.

**Phase 2 (Down-sweep / Distribute):** Push accumulated results down the tree to compute all final prefixes, again using $O(\log n)$ depth.

### Why This Works

The key insight is that prefix computation has **optimal substructure**: once we know the prefix up to position $i$ and the reduction from $i+1$ to $j$, we can compute all prefixes in that range via distribution. By organizing computation in a tree structure, we exploit parallelism across independent subtrees while maintaining dependency chains of logarithmic length.

## Applications in Engineering

### 1. **Parallel Computing & GPU Programming**
- Core primitive in CUDA, OpenCL, and other parallel frameworks
- Used in stream compaction, stream processing, and data-parallel algorithms
- Essential for exploiting SIMD and many-core hardware

### 2. **Graphics Processing**
- Computing cumulative distributions in rendering
- Prefix sums for parallel ray tracing and photon mapping
- Efficient memory allocation on GPU

### 3. **Database Query Processing**
- Aggregation operations (SUM, COUNT, MAX) over sorted data
- Parallel query execution engines
- Distributed database joins and group-by operations

### 4. **Signal Processing**
- Computing cumulative energy or amplitude in signals
- Digital filter implementation via convolution with prefix structures
- Time-series analysis with running statistics

### 5. **Image Processing**
- Integral image computation for fast 2D region queries
- Parallel histogram computation and equalization
- Connected component labeling via parallel union-find

### 6. **Machine Learning**
- Efficient minibatch processing in distributed training
- Prefix-sum based histogram construction for decision trees
- Cumulative probability distributions in sampling

### 7. **Computational Geometry**
- Parallel sorting via radix sort (uses scan for digit bucketing)
- Prefix aggregation for 3D mesh processing
- Space partitioning structures (octrees, BVH construction)

## Common Mistakes / Pitfalls

### 1. **Assuming Commutativity**
Scans require associativity, **not** commutativity. Operators like subtraction or division will produce incorrect results even though they might appear to work in simple cases.

$$\text{WRONG: } (5 - 3) - 2 = (5 - 2) - 3$$

### 2. **Confusing Scan with Reduce**
- **Reduce**: single output (total of all elements)
- **Scan**: $n$ outputs (all prefix results)

Scan is strictly more powerful but costs more to compute.

### 3. **Not Accounting for Identity Elements**
In exclusive scan implementations, forgetting to pre-pend the identity element of $\oplus$ leads to off-by-one errors.

For example, with addition (identity = 0):
```
WRONG: exclusive_scan([1,2,3]) = [1,3,6]  // missing leading 0
RIGHT: exclusive_scan([1,2,3]) = [0,1,3]
```

### 4. **Underestimating Depth in Practice**
While theoretical depth is $O(\log n)$, constant factors and synchronization overhead in actual hardware can make naive implementations suboptimal. Work-efficient algorithms are essential.

### 5. **Ignoring Associativity at Scale**
Floating-point arithmetic is not associative: different evaluation orders give different results due to rounding error. This matters for reproducibility in scientific computing.

## See Also

- [[Reduce]] — Computing a single aggregate value (related but distinct)
- [[Partition]] — Reordering data via predicates (uses scan internally)
- [[Filter]] — Selecting elements (uses scan for efficient parallel implementation)