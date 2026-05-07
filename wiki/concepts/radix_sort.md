# Radix Sort

## Definition

**Radix sort** is a non-comparison-based sorting algorithm that arranges elements by processing their individual digits or bits, typically from the least significant to most significant position (or vice versa). Unlike comparison-based sorts that order elements by pairwise comparisons, radix sort exploits the positional notation of numbers to achieve linear-time complexity.

The algorithm is fundamentally based on the principle that the relative order of elements with identical radix values at position $i$ is preserved when processing position $i+1$ (a property called **stability**). This enables sorting without direct element comparison.

## Key Equations

**Time Complexity:**
$$T(n) = O(d \cdot n)$$
where $d$ is the number of digit positions (or bits) and $n$ is the number of elements.

**Space Complexity:**
$$S = O(n + k)$$
where $k$ is the radix (base) of the number system. For bit-level processing, $k = 2$.

**Word-size parameterization** (as in binary radix variants):
$$T(n) = O(w \cdot n)$$
where $w$ is the element word size in bits.

**Radix relationship:**
For base-$k$ radix sort on $w$-bit integers:
$$d = \lceil w / \log_2 k \rceil$$

## Physical Intuition / Derivation

### Core Principle: Positional Processing

Radix sort works because numerical values decompose into independent positional components. Consider sorting three 2-bit unsigned integers: $\{3, 1, 2\}$ in binary as $\{11, 01, 10\}$.

**Step 1 (process bit 0 - rightmost):**
- Bit 0 = 0: elements $\{10, 01\}$ → $\{2, 1\}$
- Bit 0 = 1: elements $\{11\}$ → $\{3\}$
- Result: $\{2, 1, 3\}$ (preserving relative order within groups)

**Step 2 (process bit 1):**
- Bit 1 = 0: elements $\{1\}$ → $\{1\}$
- Bit 1 = 1: elements $\{2, 3\}$ → $\{2, 3\}$
- Result: $\{1, 2, 3\}$ ✓

The key insight: once we've sorted by bit 0, processing bit 1 preserves that ordering because bit 1 is more significant. A **stable** auxiliary sort (e.g., counting sort for each bit position) maintains the invariant.

### Why Non-Comparison?

Radix sort avoids comparisons by distributing elements into **bins** based on bit/digit values. The bottleneck is **partitioning** (assigning elements to bins), not comparison, which can be done in linear time.

### Comparison to Binary Quicksort

The source material introduces **binary quicksort** and **bsort** as related divide-and-conquer variants that:
- Split arrays bit-by-bit from MSB (most significant bit)
- Partition elements into two subarrays: $a_1$ (bit is set) and $a_2$ (bit is unset)
- Use bitwise operations: $a_i \land m \neq 0$ vs. $a_i \land m = 0$ (where $m = 1 \ll (s-i)$ for bit position $i$)
- Operate **in-place** with only $O(w)$ auxiliary space, vs. radix sort's $O(n+k)$

This is a more memory-efficient variant suitable for hardware implementation.

## Applications in Engineering

### 1. **Sorting Large Integer Datasets**
- Database indexing and query optimization
- Sorting timestamps or IDs in time-series data
- Efficient when comparison cost is high (e.g., multi-word keys)

### 2. **Embedded Systems & FPGA Implementation**
- Minimal space overhead ($O(w)$ for in-place variants)
- Bitwise operations map directly to hardware gates
- Predictable latency for real-time sorting tasks

### 3. **Floating-Point Sorting**
- Handling IEEE 754 representations by reinterpreting bits as integers
- Critical in numerical libraries and GPU sort kernels
- Sign-bit manipulation required for signed magnitude representation

### 4. **Distributed Sorting (Big Data)**
- Histogram-based radix sort across multiple machines
- Each node processes different bit ranges independently
- Reduces communication overhead vs. comparison-based merge sorts

### 5. **Graphics & Vision Processing**
- Sorting pixel values or depth data for rasterization
- Counting sort (radix special case) for histogram computations
- Real-time constraints favor linear-time guarantees

### 6. **Cryptography**
- Sorting indices in SPN (Substitution-Permutation Network) operations
- Key schedule generation requiring deterministic bit permutations

## Common Mistakes / Pitfalls

### 1. **Assuming Radix Sort is Always Faster**
Radix sort's $O(wn)$ is only better than comparison sort's $O(n \log n)$ when $w < \log n$. For 64-bit integers on datasets $< 2^{64}$ elements, this rarely holds. Practical performance depends on cache locality and branch prediction.

### 2. **Forgetting Stability Requirement**
Non-stable implementations corrupt the sort order. Must use stable counting sort or equivalent at each digit position. In-place variants (binary quicksort) sacrifice full stability for memory efficiency.

### 3. **Incorrect Floating-Point Handling**
IEEE 754 bit representation requires special handling:
- Negative numbers have reversed bit ordering
- Sign bit must be flipped/processed separately
- Treating floats as integers directly produces wrong results

### 4. **Ignoring Radix Choice**
Choosing radix $k = 256$ (byte-wise) is faster than $k = 2$ (bit-wise) due to cache efficiency and fewer passes, but requires $O(256) = O(1)$ extra space per digit. Trade-offs matter in practice.

### 