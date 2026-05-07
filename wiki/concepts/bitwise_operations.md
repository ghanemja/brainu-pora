# Bitwise Operations

## Definition

Bitwise operations are logical and arithmetic manipulations performed directly on the binary representations of integers at the level of individual bits. These operations work on one or more bit patterns or binary numerals to produce a result, typically without involving higher-level arithmetic or comparison operations.

The primary bitwise operators are:

- **AND** (`&`): Yields 1 only when both input bits are 1
- **OR** (`|`): Yields 1 when at least one input bit is 1
- **XOR** (`^`): Yields 1 when input bits differ
- **NOT** (`~`): Inverts all bits
- **Left Shift** (`<<`): Shifts bits left by $n$ positions, filling with zeros: $x \ll n = x \cdot 2^n$
- **Right Shift** (`>>`): Shifts bits right by $n$ positions (behavior depends on signedness)

## Key Equations

For a bit mask $m$ selecting a specific bit position:
$$m = 1 \ll (s - i)$$

where $s$ is the total word size (in bits) and $i$ is the bit position being examined (counting from MSB as $i=1$).

**Bit extraction:** To test if bit $i$ is set in value $x$:
$$\text{bit set} \iff (x \land m) \neq 0$$

**Bit manipulation time complexity:** Each bitwise operation executes in $O(1)$ time on fixed-width integers.

**Non-comparison sort complexity:** Algorithms exploiting bitwise operations achieve:
$$T(n) = O(w \cdot n)$$

where $w$ is the word size (number of bits) and $n$ is the number of elements.

## Physical Intuition / Derivation

### Why Bits Matter

Modern processors are fundamentally binary machines. While high-level comparison operations (`<`, `>`, `==`) are convenient for programmers, they ultimately require multiple CPU cycles and complex circuitry. Bitwise operations map directly to single CPU instructions, making them orders of magnitude faster for appropriate problems.

### Information-Theoretic Perspective

A comparison-based sort must distinguish between $n!$ possible orderings. Information theory dictates this requires at least $\log_2(n!) \approx n\log_2(n)$ comparisons. However, if we examine the data at the **bit level**, we gain direct access to the structure encoding that data. Each bit position becomes an independent partitioning criterion.

### Binary Quicksort Derivation

The core insight is to replace pairwise element comparison with **bit-by-bit partitioning**:

1. **Start with MSB:** Examine the highest-significance bit across all elements
2. **Partition:** Split the array into two groups:
   - $a_1$: elements with bit set (i.e., $a_i \land m \neq 0$)
   - $a_2$: elements with bit clear (i.e., $a_j \land m = 0$)
3. **Order groups:** Place group with 0-bits before 1-bits (for ascending sort), since numerically smaller values have leading zeros
4. **Recurse:** Apply the same process to each group with the next bit position

This avoids the $\Omega(n\log n)$ barrier because we're not comparing elements—we're examining fixed structural properties of the data representation.

### Handling Signed Integers and Floats

For two's-complement signed integers, the trick is recognizing that the sign bit (MSB) inverts the usual ordering: negative numbers have sign bit = 1 but are numerically smaller. A single XOR with the sign bit corrects this during partitioning.

For IEEE 754 floats, similar bit-level manipulation makes the exponent and mantissa sortable lexicographically when the sign bit is handled correctly.

## Applications in Engineering

### 1. **High-Performance Sorting**
Non-comparison sorts are deployed in databases and data warehouses when:
- Integers or fixed-point numbers dominate the dataset
- Word size is small ($w \ll \log n$)
- Memory bandwidth is the bottleneck (bitwise ops have superior cache efficiency)

### 2. **Embedded Systems**
Bitwise operations consume minimal power and execute in fixed time, critical for:
- Real-time systems with hard latency guarantees
- Resource-constrained IoT devices
- FPGA implementations (map directly to hardware gates)

### 3. **Graphics & Image Processing**
Pixel manipulation, color space conversions, and bitmask operations rely on bitwise operations for efficiency.

### 4. **Cryptography & Hashing**
Hash functions and cryptographic algorithms are fundamentally built on bitwise operations. They provide diffusion (output bits depend on all input bits) and confusion (nonlinear bit interactions).

### 5. **Network Programming**
IP address manipulation, subnet masking, and packet processing use bitwise masks extensively:
```
subnet_match = (ip_addr & subnet_mask) == network_address
```

### 6. **Hardware Design & VLSI**
Bitwise operations translate directly to logic gates, making bit-level algorithms preferable in hardware synthesis.

## Common Mistakes / Pitfalls

### 1. **Operator Precedence Confusion**
Bitwise operators have lower precedence than arithmetic operators in most languages:
```
// Wrong: x + 1 & 0xFF evaluates as (x+1) & 0xFF
// Correct:
mask = x & 0xFF; result = mask + 1;
```

### 2. **Assuming Bitwise = Always Faster**
Bitwise operations on variable-width data or when constant factors are large can be slower than optimized comparison sorts. Profile before optimizing.

### 3. **Sign Extension Errors**
Right-shifting signed integers may fill with sign bits (arithmetic shift) rather than zeros (logical shift). Behavior is compiler-dependent:
```c
// Dangerous for signed types
int x = -1;
int result = x >> 1;  // Undefined or -1 depending on implementation
```

### 4. **Forgetting Endianness**
Byte order matters when serializing bitwise results or working across architectures.

### 5. **Not Handling Edge Cases in Bit Sorting**
- Mixed positive/negative integers require special treatment
- Negative zero and NaN in floating