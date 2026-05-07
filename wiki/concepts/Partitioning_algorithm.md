# Partitioning Algorithm

## Definition

A **partitioning algorithm** is a divide-and-conquer subroutine that reorganizes array elements into disjoint subsets (partitions) based on a specific criterion, without necessarily fully sorting within each partition. The algorithm guarantees that all elements satisfying a condition precede all elements that do not.

Formally, given an array $a$ and a predicate $P(x)$, partitioning rearranges $a$ such that:
$$a[0..k-1] \text{ satisfy } P \quad \text{and} \quad a[k..n-1] \text{ do not satisfy } P$$

where $k$ is the partition index determined by the algorithm.

**Key property**: The relative order of elements *within* each partition may be preserved (stable) or destroyed (unstable), depending on implementation.

---

## Key Equations

For a **single-bit partitioning pass** (as in radix-based sorting):

$$\text{Position of element } x = \begin{cases} 
\text{next available in 0-group} & \text{if bit}_i(x) = 0 \\
\text{next available in 1-group} & \text{if bit}_i(x) = 1
\end{cases}$$

where $\text{bit}_i(x)$ denotes the $i$-th bit of element $x$.

**Floating-point bit decomposition**:
$$\text{sizeof}(x) = \text{sizeof}(\text{mantissa}) + \text{sizeof}(\text{exponent}) + 1$$

The "+1" accounts for the sign bit, typically the most significant bit.

---

## Physical Intuition / Derivation

### Single-Pass Partitioning (Bit-Based)

Imagine you have a collection of items, each labeled with a binary feature (bit). To partition by this feature:

1. **Scan left-to-right**, maintaining two "slots":
   - A slot in the left (0-group) where items with bit=0 should go
   - A slot in the right (1-group) where items with bit=1 should go

2. **Place each element** into its corresponding group while preserving the order of appearance *within* groups

3. **Result**: A clear boundary separates the two groups

### Multi-Level Partitioning (Inductive Argument)

For problems requiring partitioning across multiple bits (e.g., sorting floating-point numbers):

- **Base case** ($k=1$): One pass partitions by the 1st bit correctly
- **Inductive step** ($k \to k+1$): If the array is correctly partitioned by $k$ bits into independent sub-partitions, apply the partitioning algorithm to each sub-partition using the $(k+1)$-th bit
  - Each sub-partition processes independently
  - Elements with identical $k$-bit prefixes stay together
  - The new bit refines each group further

**Why this works**: After $p$ passes (where $p = $ word size), every element is uniquely distinguished by its full bit pattern, achieving complete sorting.

### Application Example: Floating-Point Sorting

`bsortFloat` partitions in three stages:

1. **Sign bit** (most significant): Separates negative from non-negative
2. **Exponent bits**: Partitions by magnitude range
3. **Mantissa bits** (least significant): Refines within same-magnitude groups

Each stage is a partitioning operation, guaranteeing correctness through induction.

---

## Applications in Engineering

### 1. **Sorting Algorithms**
- **Radix sort**: Core operation; partitions by each digit/bit position sequentially
- **Quicksort**: Partitions around a pivot value
- **Floating-point sorting**: Multi-stage partitioning respects IEEE 754 bit layout

### 2. **Database Query Processing**
- Partitioning large datasets by key ranges before merging or filtering
- Enables parallel processing (each partition processed independently)

### 3. **Parallel & Distributed Computing**
- **MapReduce**: Partitioning input data across nodes
- **GPU computing**: Partitioning workloads for load balancing
- Reduces data movement within memory hierarchy

### 4. **Signal Processing & Data Analysis**
- Separating signals by frequency band (filter bank partitioning)
- Clustering: Partitioning data by feature values as preprocessing

### 5. **Hardware & Networking**
- **Network packet routing**: Partitioning packets by destination IP range
- **Cache optimization**: Partitioning memory access patterns
- **VLSI design**: Partitioning circuit components for placement/routing

---

## Common Mistakes / Pitfalls

### 1. **Forgetting Stability**
- Assuming relative order within partitions is preserved when it isn't
- **Fix**: Document whether your partitioning is stable or unstable; use explicit indices if order matters

### 2. **Incorrect Inductive Hypothesis**
- Claiming correctness without verifying that partitions remain independent after each pass
- **Fix**: Explicitly state what property holds after step $k$ and verify it extends to step $k+1$

### 3. **Bit-Order Confusion**
- Processing least significant bits first (wrong for lexicographic sorting)
- **Fix**: Always sort most-significant bits first for correct numerical/lexicographic order

### 4. **Off-by-One Partition Boundary**
- Elements equal to pivot placed inconsistently across calls
- **Fix**: Establish clear convention: elements $\leq$ pivot go left, $>$ pivot go right (or opposite)

### 5. **Ignoring Special Values**
- For floating-point: NaN, $\pm\infty$, and $-0$ don't follow standard bit-ordering rules
- **Fix**: Handle sign-flipping for negative exponents or preprocess special values

### 6. **Performance Assumption**
- Assuming $O(n)$ partitioning always beats $O(n \log n)$ comparison sorts
- **Fix**: Consider input size, cache behavior, and constant factors; partitioning excels on large uniform datasets

---

## See Also

- [[Radix Sort]]: Multi-stage partitioning algorithm achieving $O(nk)$ sorting
- [[Quicksort]]: Pivot-based partit