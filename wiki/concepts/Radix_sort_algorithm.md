# Radix Sort Algorithm

## Definition

**Radix sort** is a non-comparative integer sorting algorithm that processes elements by examining their individual digits (or bits) in a systematic fashion, typically from least significant to most significant (LSD) or vice versa. Unlike comparison-based algorithms such as quicksort or mergesort, radix sort distributes elements into buckets based on digit/bit values and reconstructs the sorted array by concatenating buckets in order.

The algorithm is classified as a **linear time sorting algorithm** because its execution time depends on the number of elements $n$ and the number of digit positions $w$ (or word size), rather than on relative comparisons between elements.

## Key Equations

**Time Complexity:**
$$T(n) = O(n \cdot w)$$

where:
- $n$ = number of elements to sort
- $w$ = word size (number of bits/digits per element)

For fixed word sizes (e.g., 32-bit or 64-bit integers), this reduces to $O(n)$.

**Space Complexity:**
$$S(n) = O(n + k)$$

where $k$ is the radix (typically $k = 2$ for binary radix sort, or $k = 256$ for byte-wise radix sort).

**Number of passes required:**
$$\text{passes} = \lceil w / \log_2(k) \rceil$$

For binary radix sort ($k=2$): $\text{passes} = w$  
For byte-wise radix sort ($k=256$): $\text{passes} = \lceil w/8 \rceil$

## Physical Intuition / Derivation

### Why Radix Sort Escapes Comparison Lower Bounds

Comparison-based sorting algorithms face a fundamental lower bound: any algorithm that sorts by comparing pairs of elements requires at least $\Omega(n \log n)$ comparisons in the worst case. This derives from information theory—there are $n!$ possible orderings, so $\log_2(n!)$ bits of information must be extracted.

Radix sort **bypasses this constraint** by not relying on comparisons. Instead, it extracts information directly from element structure (their binary or decimal representations). Each pass examines one radix position across all elements, using **counting sort** as a subroutine.

### How It Works: Bit-by-Bit Processing

Consider sorting 32-bit integers with binary radix sort:

1. **Pass 1:** Partition elements into two buckets based on bit 0 (LSB)
   - Bucket 0: elements with bit 0 = 0
   - Bucket 1: elements with bit 0 = 1
   - Maintain relative order (stable sort)

2. **Pass 2:** Re-partition the result based on bit 1
3. **Continue for all 32 passes**

After $w$ passes, elements are fully sorted because the most significant bits dominate the ordering.

**Why stability matters:** At each pass, equal elements (in terms of the current bit) must retain their relative order from the previous pass. This ensures that earlier (less significant) bit decisions are preserved.

### The Role of Word Size $w$

The parameter $w$ directly determines total work. If elements have large bit-widths (e.g., 64-bit doubles), more passes are required:

$$\text{Work} = n \cdot w \text{ bit operations}$$

This is why radix sort performs better on **narrow data types** (char: 8 bits) than wide ones, but maintains linear scaling in all cases.

## Applications in Engineering

### 1. **High-Performance Sorting Systems**

Modern libraries implement **hybrid radix sorts** that switch between radix and comparison-based methods:
- **ska_sort:** Optimized radix sort for integer types
- **Spreadsort:** Hybrid algorithm using radix + quicksort
- **Introsort:** Comparison-based with introspection (fallback from quicksort to heapsort)

From the source material, ska_sort achieves $O(n \cdot w)$ time and is benchmarked against introsort ($O(n \log n)$) in real systems.

### 2. **Database Indexing and Data Processing**

Radix sort is used in:
- Sorting large datasets by timestamp or ID (8–64 bit keys)
- Building B-tree indexes in databases
- Bucket-based partitioning in parallel query execution

### 3. **Graphics and Scientific Computing**

- Sorting particles by spatial coordinates (3D rendering, N-body simulations)
- Histogram-based algorithms (e.g., median filtering) in image processing
- Sorting rays or primitives in ray-tracing pipelines

### 4. **Network Packet Processing**

Router/switch firmware uses radix sort for:
- Sorting by destination IP (32-bit addresses)
- Priority queue management
- Load-balanced packet routing

## Common Mistakes / Pitfalls

### 1. **Assuming $O(n)$ Always Beats $O(n \log n)$**

The constant factors hidden in the asymptotic notation are **crucial**:
- Radix sort requires $n \cdot w$ bit-level operations
- Quicksort requires $n \log_2 n$ comparisons (each comparison is fast)

For small $w$ (e.g., $w = 8$), radix sort wins decisively. For very large $w$ (e.g., $w = 64$ on 64-bit doubles), the advantage narrows or reverses due to:
- Cache behavior (radix sort makes $w$ passes through memory)
- Instruction-level parallelism (quicksort comparisons vectorize better)

From the source: *"when the bit-depth is shallow, bsort consistently outperforms introsort, but when it is deep, its relative performance decreases."*

### 2. **Forgetting the Stability Requirement**

Many optimizations break stability. A **non-stable radix sort** may fail to maintain relative order of equal keys, corrupting the sort result. Always use counting sort (or stable partitioning) in subroutines.

### 3. **Ignoring Architectural Overheads**

The source material emphasizes:
> "architectural overheads and compiler limitations can significantly hinder real-world efficiency"

Cache misses, branch misprediction, and poor