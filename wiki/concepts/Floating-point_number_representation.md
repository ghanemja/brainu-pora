# Floating-point number representation

## Definition

A **floating-point number** is a standardized binary encoding scheme for representing real numbers in digital computers. It decomposes a number into three components:

1. **Sign bit** ($s$): 1 bit indicating positive (0) or negative (1)
2. **Exponent** ($e$): $w_e$ bits encoding the scale/magnitude
3. **Mantissa** (or significand, $m$): $w_m$ bits encoding the significant digits

The total bit-width is:
$$\text{sizeof}(x) = w_m + w_e + 1$$

The number is reconstructed as:
$$x = (-1)^s \times 2^{e - \text{bias}} \times (1.m)_2$$

where $(1.m)_2$ is the mantissa interpreted as a binary fraction with an implicit leading 1, and the exponent is offset by a bias constant (typically $2^{w_e-1} - 1$).

## Key Equations

**General floating-point value:**
$$x = (-1)^s \times 2^{(e - \text{bias})} \times 1.m$$

**Bit-width relationship:**
$$\text{sizeof}(x) = \underbrace{1}_{\text{sign}} + \underbrace{w_e}_{\text{exponent}} + \underbrace{w_m}_{\text{mantissa}}$$

**Lexicographical bit ordering (MSB → LSB):**
$$\text{bits ordered as: } [s \mid e_{w_e-1} \cdots e_0 \mid m_{w_m-1} \cdots m_0]$$

**Numerical comparison property:**
Two floating-point values can be ordered by comparing their bit representations *lexicographically* (bit-by-bit from MSB), provided the sign bit is handled separately for negatives.

## Physical Intuition / Derivation

### Why Three Components?

Real numbers span vastly different scales—from $10^{-308}$ to $10^{308}$. A fixed-point representation (like decimal integers) would require impractical bit-widths. Instead, floating-point separates:

- **Mantissa**: Captures *precision* (the significant digits)
- **Exponent**: Captures *scale* (the magnitude/range)
- **Sign**: Handles polarity

This mirrors scientific notation: $3.14159 \times 10^{-5}$ encodes the mantissa (3.14159), exponent (−5), and sign independently.

### Lexicographical Ordering

A key insight is that floating-point bit-strings *almost* obey lexicographical (bitwise) ordering when interpreted as unsigned integers. This works because:

1. **Sign bit is MSB**: Negative numbers have sign=1; positive have sign=0. Lexicographically, 0 < 1, so positives come first.
2. **Exponent is next**: Larger exponents (higher bit patterns) represent larger magnitudes within the same sign.
3. **Mantissa is LSB**: For fixed sign and exponent, larger mantissas yield larger values.

**Exception for negatives:** The lexicographical order reverses for negative numbers (represented in sign-magnitude form in IEEE 754). Sorting negatives requires reversing the comparison direction.

## Applications in Engineering

### 1. **Scientific Computing & Simulation**
   - Solving differential equations (CFD, heat transfer)
   - Numerical integration with adaptive step-sizing
   - Matrix computations in FEA (finite element analysis)

### 2. **Signal Processing**
   - Digital filters (IIR, FIR)
   - Fourier transforms and spectral analysis
   - Audio/image codec implementation

### 3. **Machine Learning**
   - Neural network training (backpropagation uses floating-point arithmetic)
   - Model inference on edge devices (FP16, BF16 reduced precision)

### 4. **Graphics & Rendering**
   - 3D transformations and perspective projection
   - Lighting calculations
   - GPU computations (native FP32/FP64 support)

### 5. **Embedded Systems**
   - Sensor fusion and Kalman filtering
   - Control systems (PID loops)
   - Real-time financial computations

### 6. **Efficient Sorting**
   - The source material demonstrates that floating-point values can be sorted efficiently using bit-level operations (radix sort on exponent, then mantissa), exploiting lexicographical ordering properties.

## Common Mistakes / Pitfalls

### 1. **Assuming Associativity and Distributivity Hold**
   ```
   (a + b) + c ≠ a + (b + c)  [floating-point rounding errors]
   a × (b + c) ≠ a×b + a×c
   ```
   Rearranging operations changes the order of rounding, producing different results.

### 2. **Comparing with Equality (`==`)**
   ```python
   if x == 0.1:  # WRONG: 0.1 is inexact in binary
       ...
   
   if abs(x - 0.1) < 1e-9:  # Correct: epsilon-based comparison
       ...
   ```

### 3. **Catastrophic Cancellation**
   Subtracting nearly-equal values loses precision:
   $$c = \sqrt{a^2 + b^2} - a \quad \text{(for small } b\text{)}$$
   Should be rewritten as: $c = \frac{b^2}{a + \sqrt{a^2 + b^2}}$

### 4. **Misunderstanding Precision vs. Accuracy**
   - **Precision**: bit-width of mantissa (how many digits stored)
   - **Accuracy**: how close to true value (affected by rounding, truncation, algorithm stability)
   - High precision ≠ high accuracy if accumulated errors are large

### 5. **Ignoring Sign Bit in Bitwise Sorting**
   Treating floating-point as unsigned integers breaks ordering for negatives. Must separate sign bit and reverse comparison for negative partition (as shown in the source algorithm).

### 6. **Forgetting