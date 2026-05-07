# Bit Manipulation (Sign Bit, Exponent Bits, Mantissa Bits)

## Definition

Bit manipulation of floating-point numbers involves direct interpretation and processing of the three constituent bitfields in IEEE 754 standard floating-point representations:

- **Sign Bit**: A single bit (position $w-1$) that encodes the sign of the number. Sign = 0 represents positive; Sign = 1 represents negative.
- **Exponent Bits**: Typically 8 bits (in 32-bit floats) or 11 bits (in 64-bit doubles) that encode the magnitude scale, stored with a bias offset to allow representation of both very large and very small numbers.
- **Mantissa (Significand) Bits**: The remaining bits (23 in 32-bit, 52 in 64-bit) that encode the fractional precision of the number, representing the digits after the implicit leading 1 in normalized form.

In bit manipulation, these fields are accessed and processed at the raw binary level rather than through floating-point arithmetic, enabling bitwise sorting, comparison, and transformation algorithms that respect floating-point ordering semantics.

## Key Equations

A floating-point number is composed as:

$$\text{Value} = (-1)^{\text{sign}} \times 2^{\text{exponent} - \text{bias}} \times (1.\text{mantissa})_2$$

where bias is typically 127 for 32-bit floats and 1023 for 64-bit doubles.

The IEEE 754 bit layout (32-bit example):
$$\text{bits} = [\underbrace{\text{sign}}_1][\underbrace{\text{exponent}}_8][\underbrace{\text{mantissa}}_23]$$

For bitwise comparison to preserve numerical ordering, a **monotonic transformation** via bit reinterpretation must respect:
$$\text{bit\_pattern}_1 < \text{bit\_pattern}_2 \iff \text{value}_1 < \text{value}_2$$

This holds for non-negative numbers directly, but requires sign-bit inversion and magnitude inversion for negative numbers to maintain total order.

## Physical Intuition / Derivation

### Why Bit Manipulation Works for Floating-Point Sorting

The key insight is that **IEEE 754 encodes floating-point numbers such that their bit patterns, when interpreted as unsigned integers, preserve magnitude ordering for non-negative values**.

Consider two positive normalized floats with bit patterns $B_1$ and $B_2$:
- If they have different exponents, the one with the larger exponent bits is numerically larger (assuming equal signs and positive).
- If exponents are equal, the one with larger mantissa bits is numerically larger.

This lexicographic ordering of fields (sign → exponent → mantissa) mirrors the numerical ordering, allowing direct bitwise comparison without floating-point arithmetic.

### Special Value Handling

The approach naturally handles IEEE 754 special values:

**Positive Infinity ($+\infty$)**
- Representation: sign = 0, exponent = all 1s, mantissa = all 0s
- Bitwise: `0 11111111 00000000...`
- Behavior: Partitions into non-negative values with maximal exponent; ordered as largest value

**Negative Infinity ($-\infty$)**
- Representation: sign = 1, exponent = all 1s, mantissa = all 0s
- Bitwise: `1 11111111 00000000...`
- Behavior: Partitions into negative values with maximal exponent; ordered as smallest value

**Not-a-Number (NaN)**
- Representation: exponent = all 1s, mantissa ≠ all 0s (sign arbitrary)
- Bitwise: `[0 or 1] 11111111 [non-zero]`
- Behavior: Segregated at partition extremities; relative order determined by mantissa payload (signaling vs. quiet NaN)

**Positive Zero ($+0$) and Negative Zero ($-0$)**
- $+0$: sign = 0, exponent = 0, mantissa = 0 → `0 00000000 00000000...`
- $-0$: sign = 1, exponent = 0, mantissa = 0 → `1 00000000 00000000...`
- Behavior: $-0$ partitions into negatives at the boundary; $+0$ partitions into positives at the boundary
- Ordering preserved: $-0 < +0$ emerges naturally from bit comparison

### Example Trace

For $a = [1.75, 1.25, -2.5, -\infty]$ with 6-bit representation (1 sign, 3 exponent with bias 3, 2 mantissa):

| Value | Binary | Interpretation |
|-------|--------|---|
| 1.75  | `001111` | sign=0, exp=011, mant=11 → $2^{3-3} \times 1.75$ ✓ |
| 1.25  | `001101` | sign=0, exp=011, mant=01 → $2^{3-3} \times 1.25$ ✓ |
| -2.5  | `110001` | sign=1, exp=100, mant=01 → $-2^{4-3} \times 1.25$ ✓ |
| $-\infty$ | `111100` | sign=1, exp=111, mant=00 ✓ |

Bitwise radix sort by bit position (sign first, then exponent, then mantissa) correctly produces: $[-\infty, -2.5, 1.25, 1.75]$

## Applications in Engineering

### 1. High-Performance Sorting
Bitwise radix sort on floating-point arrays achieves $O(nw)$ time complexity where $w$ is word size (constant ~64 bits), avoiding comparison-based sort overhead and floating-point exceptions.

**Example**: Sorting sensor data streams, GPU-accelerated physics simulations, database indexing of real-valued records.

### 2. GPU Compute Kernels
Bit manipulation avoids branching (slow on GPUs) and enables vectorized operations on floating-