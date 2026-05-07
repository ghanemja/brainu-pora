# binary quicksort

## Definition

**Binary quicksort** is a non-comparison-based, divide-and-conquer sorting algorithm that partitions an array by examining individual bits of elements, starting from the most significant bit (MSB). Unlike comparison-based sorts, it achieves linear-time complexity relative to the word size of elements, making it particularly efficient for fixed-width data types.

The algorithm recursively splits an array into two subarrays based on whether each element has a 0 or 1 at a specific bit position, then applies the same process to the next less-significant bit in each subarray.

## Key Equations

**Bit mask for iteration $i$:**
$$m = 1 \ll (s - i)$$

where:
- $s$ = total number of bits per element (word size)
- $i$ = current iteration (where $1 \leq i \leq s$)
- $\ll$ = left-shift bitwise operator

**Partitioning invariants:**

For a subarray $a = [a_1, a_2, \ldots, a_n]$ partitioned at mask $m$:

$$\text{Partition 1: } a_i \land m \neq 0 \quad \forall a_i \in a_1$$
$$\text{Partition 2: } a_j \land m = 0 \quad \forall a_j \in a_2$$

where $\land$ is the bitwise AND operator.

**Complexity:**
- **Time:** $O(wn)$ where $w$ = word size, $n$ = number of elements
- **Space:** $O(w)$ auxiliary (in-place variant)

## Physical Intuition / Derivation

### Why Bit-Level Partitioning Works

Binary quicksort exploits the **radix property**: elements can be fully ordered by examining their bit representations sequentially from most to least significant. This avoids costly element comparisons.

**Step-by-step intuition:**

1. **MSB determines magnitude class:** At the highest bit position, elements naturally separate into two groups: those with that bit set and those without. For unsigned integers, this roughly splits the range $[0, 2^w)$ in half.

2. **Recursive refinement:** Within each subarray, the next bit refines the partition further. After $w$ iterations, elements are fully sorted because all bits have been examined.

3. **Example (4-bit unsigned):**
   ```
   Input: [5, 2, 9, 1, 14, 6]
   Binary: [0101, 0010, 1001, 0001, 1110, 0110]
   
   Bit 3 (MSB): Separate into [1001, 1110] and [0101, 0010, 0001, 0110]
   Bit 2:       Refine further...
   ... (continue for bits 1 and 0)
   Output: [1, 2, 5, 6, 9, 14]
   ```

### Why It's "Quicksort-Like"

Although it uses bitwise operations rather than comparisons, binary quicksort mirrors the structure of traditional quicksort:
- Both are divide-and-conquer algorithms
- Both partition around a "pivot" criterion (here: bit value instead of element magnitude)
- Both recursively sort partitions
- However, binary quicksort has *guaranteed* $O(wn)$ performance (no worst case), whereas comparison-based quicksort degrades to $O(n^2)$ with poor pivots

## Applications in Engineering

### 1. **In-Memory Database Indexes**
High-performance databases use binary quicksort variants for rapid integer and timestamp sorting when index rebuilds are needed, especially for time-series data with regular word sizes.

### 2. **Graphics Processing & GPGPU Computing**
Since the algorithm operates on fixed bit widths and uses only bitwise operations, it maps efficiently to SIMD instructions and GPU kernels for parallel sorting of vertex positions, pixel values, or particle attributes.

### 3. **Embedded Systems & Real-Time Applications**
For systems with strict time budgets (e.g., automotive control, robotics), the predictable $O(wn)$ performance—without worst-case degradation—is superior to comparison-based sorts.

### 4. **Floating-Point Data Sorting**
The paper extends binary quicksort to IEEE 754 floating-point numbers by transforming their bit representations into a comparable form (handling sign/exponent/mantissa), enabling efficient sorting of scientific and engineering datasets.

### 5. **Radix-Based Cryptographic Sorting**
In security applications requiring deterministic behavior and resistance to timing attacks, the non-adaptive bit-scanning approach provides constant-time performance characteristics independent of data values.

### 6. **Distributed/Parallel Sorting**
The bit-by-bit decomposition allows natural parallelization: different processors can handle different bit levels, or bit ranges can be distributed across machines.

## Common Mistakes / Pitfalls

### 1. **Assuming $O(wn)$ beats $O(n \log n)$ universally**
Binary quicksort is only faster than comparison sorts when $w \ll \log n$. For 64-bit integers and $n > 2^{64}$, the comparison-sort bound dominates. The constant factors in bitwise operations are smaller, but the asymptotic advantage is limited to small word sizes.

### 2. **Forgetting the $O(w)$ auxiliary space requirement**
While the algorithm can be made in-place, most implementations still require $O(w)$ working space (e.g., for recursion stack depth of $w$). This is often overlooked when comparing memory usage to true in-place sorts.

### 3. **Mishandling signed integers and floating-point**
The original binary quicksort works only on unsigned integers. Extensions for signed/floating-point require:
- **Signed integers:** Bit-flip the sign bit to convert two's-complement comparisons
- **Floating-point:** Reinterpret IEEE 754 representation and adjust sign/exponent encoding

Not applying these transformations correctly inverts or corrupts the sort order.

### 4. **Cache-unfriendly partitioning**
The bit-by-bit partitioning may access memory in non-sequential patterns, leading to cache misses.