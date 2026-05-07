# Partition-Based Sorting

## Definition

**Partition-based sorting** is an algorithmic paradigm that recursively or iteratively divides an input dataset into disjoint subsets (partitions) based on a discriminating property, then sorts within or across these partitions. The most common instantiation is **radix-like bitwise partitioning**, where elements are segregated by individual bit positions—typically from most-significant to least-significant (or vice versa)—and partitions are recursively subdivided until fully sorted.

In the context of floating-point numbers, partition-based sorting exploits the IEEE 754 bit representation (sign, exponent, mantissa) to correctly order values including special cases (±∞, NaN, ±0) through sequential bitwise partitioning without explicit comparison operations.

## Key Equations

**Time Complexity:**
$$T(n, w) = O(nw)$$

where $n$ is the number of elements and $w$ is the word size in bits. Each of the $w$ bit positions requires one linear-time partitioning pass through all $n$ elements.

**Partition Index Mapping:**
For a given bit position $b$ and element $a_i$, the partition assignment is determined by:
$$\text{partition}(a_i, b) = \begin{cases} 0 & \text{if bit } b \text{ of } a_i = 0 \\ 1 & \text{if bit } b \text{ of } a_i = 1 \end{cases}$$

**IEEE 754 Monotonicity Preservation:**
Adding a constant offset is a **monotonic transformation**, which preserves numerical ordering:
$$a_i < a_j \implies f(a_i) < f(a_j) \quad \text{(for monotonic } f\text{)}$$

This property enables reinterpretation of IEEE 754 bitstrings as unsigned integers while maintaining sort order after appropriate sign-bit transformations.

## Physical Intuition / Derivation

### Why Bitwise Partitioning Works

Traditional comparison-based sorting (quicksort, mergesort) requires $\Omega(n \log n)$ comparisons. Partition-based bitwise sorting achieves linear $O(nw)$ time by **eschewing comparisons entirely** and instead using the bit structure itself as the organizing principle.

**Mechanism:**
1. Process bits in priority order (sign → exponent → mantissa for floats)
2. For each bit position $b$, partition the current set into two groups: elements with bit $b = 0$ and bit $b = 1$
3. Elements are placed in order such that all 0-bit elements come before 1-bit elements
4. After processing all $w$ bits, the array is sorted

**Why this preserves order:** A number with a higher-significance bit set will always sort ahead of numbers differing only in lower-significance bits, regardless of their absolute magnitudes. This is the fundamental property of positional number systems.

### Floating-Point Special Cases

IEEE 754 encodes special values in ways that seem contradictory to unsigned integer ordering:
- **Sign bit = 1** typically represents negative numbers
- **All exponent bits set** represents ±∞ or NaN
- **Positive zero (0x00...)** vs. **negative zero (0x80...)** must satisfy $-0 < +0$

**Solution:** Partition-based sorting handles these by:
1. **Partitioning by sign first:** Negative numbers (sign = 1) go to one half, positive to the other
2. **Conditional bit inversion for negative partition:** Within negative numbers, a secondary sort inverts bit interpretation so that more negative values (larger bitstrings) are correctly placed earlier
3. **Special partition placement:** ±∞ and NaN occupy boundary partitions with well-defined positions

For example, $-\infty$ (bits: 1111...0) occupies the partition of negative numbers with all exponent bits set, guaranteeing all finite numbers satisfy $a_i > -\infty$.

## Applications in Engineering

### 1. **GPU and Hardware Accelerators**
- Bitwise partitioning maps efficiently to SIMD and parallel architectures (no data-dependent branching)
- Used in CUDA-based sorting for massive datasets (millions of elements)
- No irregular memory access patterns, enabling cache-efficient execution

### 2. **Numerical Computing and Scientific Simulation**
- Sorting floating-point datasets while preserving IEEE 754 semantics (essential in physics/chemistry simulations)
- Handling datasets containing infinities and NaN gracefully without additional conditional logic
- Time-critical applications (e.g., real-time financial modeling, signal processing)

### 3. **Database Systems**
- Index construction for floating-point columns in database engines
- Sorting sensor data or measurement arrays with guaranteed $O(nw)$ worst-case performance
- Predictable latency for embedded database systems

### 4. **Machine Learning**
- Sorting feature vectors by individual bit dimensions (feature quantization preprocessing)
- Efficient binning and histogram construction for gradient-boosted trees

### 5. **Cryptography and Security**
- Sorting cryptographic keys or hash values without timing attacks (constant per-bit work)
- No comparison branches that could leak timing information

## Common Mistakes / Pitfalls

### 1. **Assuming Comparison-Free Sorting is Always Faster**
Partition-based sorting excels when $w$ is small (e.g., 32–64 bits for standard floats). For very short arrays ($n < 10$) or large word sizes, comparison-based methods may be faster in practice due to better cache locality and lower constants.

### 2. **Forgetting Bit-Inversion for Negative Numbers**
A naive bitwise sort on two's-complement or IEEE 754 negative numbers will produce *reversed* order. The algorithm must conditionally invert bits within the negative partition to correct this.

### 3. **Mishandling NaN**
NaN is not totally ordered under IEEE 754 semantics: $\text{NaN} \not< x$ and $\text{NaN} \not> x$ for any $x$. Partition-based sorting may place NaN values at array extremities based on mantissa payload, but *relative order of multiple NaN values is not guaranteed*. Applications requiring strict reproducibility must post-process NaN elements.

### 4. **