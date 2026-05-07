# Floating-Point Representation

## Definition

Floating-point representation is a standardized method for encoding real numbers in binary form within digital systems. A floating-point number is decomposed into three components:

$$\text{Value} = (-1)^s \times m \times 2^p$$

where:
- **Sign bit** ($s \in \{0, 1\}$): determines whether the number is positive ($s=0$) or negative ($s=1$)
- **Mantissa** ($m$): the fractional coefficient (also called the significand), normalized such that $1 \leq m < 2$ in standard form
- **Exponent** ($p$): the power of 2 that scales the mantissa

This representation enables computers to store a wide range of magnitudes (from very small to very large numbers) in a fixed-size storage unit (typically 32 or 64 bits) by trading off between precision and range.

## Key Equations

**Standard floating-point form:**
$$x = (-1)^s \cdot (1.m_1m_2m_3\ldots) \cdot 2^{p}$$

where $m_1m_2m_3\ldots$ are the fractional bits of the mantissa.

**Hierarchical numerical ordering** (from most to least significant):
$$\text{Sign} \gg \text{Exponent} \gg \text{Mantissa}$$

This ordering reflects the mathematical fact that the numerical value is determined *first* by sign (negative vs. non-negative), *second* by the magnitude's scale (exponent), and *third* by fine-grained precision (mantissa).

**IEEE 754 double precision (64-bit):**
$$\text{Layout: } [1\text{ sign bit}] [11\text{ exponent bits}] [52\text{ mantissa bits}]$$

## Physical Intuition / Derivation

### Why Three Components?

Computers must encode real numbers efficiently. Simply using fixed-point arithmetic (e.g., 32 bits for integer part + 32 bits for fractional part) would limit the dynamic range—you cannot simultaneously represent $10^{-9}$ and $10^9$ with reasonable precision.

Floating-point elegantly solves this by separating **scale** (exponent) from **precision** (mantissa):

- The **exponent** controls the decimal point position, enabling coverage of an enormous dynamic range
- The **mantissa** provides the significant digits at whatever scale the exponent sets
- The **sign** handles the fundamental distinction: negative vs. non-negative

### Example

Consider representing $-2.0$ and $0.5$ in floating-point:

$$-2.0 = (-1)^1 \times 1.0 \times 2^1$$
- Sign: negative
- Mantissa: $1.0_2$ (binary)
- Exponent: $1$

$$0.5 = (-1)^0 \times 1.0 \times 2^{-1}$$
- Sign: positive
- Mantissa: $1.0_2$
- Exponent: $-1$

Despite identical mantissas, they differ by orders of magnitude because of their exponents. Yet both fit in the same number of bits.

### Hierarchical Sorting Principle

When comparing two floating-point numbers for correctness (e.g., in a sorting algorithm), the comparison must respect the hierarchical structure:

1. **Compare signs first**: All negative numbers are smaller than all non-negative numbers
2. **If signs match, compare exponents**: A number with larger exponent (in the same sign) has larger magnitude
3. **If signs and exponents match, compare mantissas**: The mantissa determines fine-grained ordering

This hierarchy is *necessary*: any other sorting order (exponent before sign, or mantissa before exponent) fails to produce globally monotonic ordering. For instance, if mantissa were the primary key, the number $-2.0$ (mantissa $= 0x10$) could incorrectly sort after $0.5$ (mantissa $= 0x01$), violating numerical ordering.

## Applications in Engineering

### 1. **Scientific Computing & Simulation**
Floating-point enables accurate representation of physical quantities spanning extreme ranges: atomic-scale phenomena ($10^{-30}$ m) and cosmological distances ($10^{26}$ m) in the same calculation.

### 2. **Signal Processing & Digital Control**
Audio signals, sensor measurements, and feedback control systems rely on floating-point arithmetic for dynamic range. A single fixed-point representation cannot simultaneously capture both loud transients and quiet ambient noise.

### 3. **Machine Learning**
Neural network weights, activations, and loss functions span many orders of magnitude during training. Modern accelerators (GPUs, TPUs) use mixed-precision floating-point (e.g., FP16 for efficiency, FP32 for stability) to balance speed and numerical accuracy.

### 4. **Computer Graphics & CAD**
3D rendering and geometric computations require representing coordinates from sub-pixel precision (10⁻³) to world-scale distances (10⁶ units) within the same model. Floating-point is essential.

### 5. **Embedded Systems & Real-Time Applications**
Although integer arithmetic is sometimes preferred for speed, floating-point libraries are used when dynamic range is critical—e.g., power systems, structural health monitoring, aerospace guidance.

### 6. **Sorting and Database Indexing**
The hierarchical structure of floating-point representation allows efficient in-place sorting algorithms (radix sort). Understanding the bit-level structure enables optimizations that leverage the sign-exponent-mantissa hierarchy.

## Common Mistakes / Pitfalls

### 1. **Assuming Floating-Point is Continuous**
Floating-point numbers are *discrete*. There is no representable number between adjacent floats; the "gap" between consecutive values grows exponentially with the exponent. This causes rounding errors in iterative calculations.

### 2. **Misunderstanding Exponent Ordering for Negative Numbers**
When sorting floats bitwise, the exponent comparison direction must **reverse** for negative numbers. A more negative exponent (e.g., $2^{-5}$) represents a *larger* magnitude (farther from zero) for negative numbers, so it should sort *first* in ascending order. Neglecting this produces incorrect orderings.

###