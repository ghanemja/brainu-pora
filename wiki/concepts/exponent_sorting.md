# Exponent Sorting

## Definition

**Exponent sorting** is the second-level sorting operation in the hierarchical radix-sort algorithm for floating-point numbers (bsortFloat). It partitions elements that share the same sign into finer-grained sub-partitions based on their exponent values, maintaining numerical correctness through **sign-dependent sort direction**.

Formally, for a floating-point number represented as:
$$x = s \cdot p \cdot m$$

where $s$ is the sign bit, $p$ is the exponent, and $m$ is the mantissa, exponent sorting operates on the $p$ component after initial partitioning by $s$.

**Key property:** The sort direction for exponents must be **reversed for negative numbers** relative to positive numbers to preserve numerical ordering.

---

## Key Equations

For a set of floating-point values with identical sign $s$, the correct ordering relationship depends on the sign:

**Positive numbers ($s = +1$):**
$$\text{If } p_1 < p_2 \text{ then } x_1 < x_2 \text{ (ascending order: sort exponents ascending)}$$

**Negative numbers ($s = -1$):**
$$\text{If } p_1 < p_2 \text{ then } |x_1| > |x_2| \text{ (ascending order: sort exponents descending)}$$

The magnitude ordering for negative numbers inverts because the exponent determines absolute magnitude, which must be negated:
$$x_{\text{neg}} = -10^{p} \cdot m$$

---

## Physical Intuition / Derivation

### Why Exponent Sorting is Necessary

Floating-point numbers encode magnitude in two components: the **exponent** (which determines the order of magnitude) and the **mantissa** (which refines within that magnitude). The exponent is the coarse-grained determinant of size.

Consider three numbers:
- $x = -2.0$ (represented as $-1 \cdot 2^0 \cdot 2^0$)
- $y = 0.0$ (represented as $+1 \cdot 0^2 \cdot 2^0$)
- $z = 0.5$ (represented as $+1 \cdot 1^2 \cdot 2^{-1}$)

**Counterexample without proper exponent sorting:** If mantissa were sorted first, you'd get $\{0.0, 0.5, -2.0\}$ (incorrect). If exponent were sorted first without respecting sign, you'd get $\{0.5, 0.0, -2.0\}$ (still incorrect).

### Sign-Dependent Sort Direction

The inversion of sort direction for negative exponents stems from the **negation operator** in the floating-point representation:

$$x_{\text{pos}} = 10^{p} \cdot m \quad \Rightarrow \quad \text{larger } p \text{ means larger } x$$

$$x_{\text{neg}} = -10^{p} \cdot m \quad \Rightarrow \quad \text{larger } p \text{ means smaller (more negative) } x$$

**Example:**
- $10^2 = 100 > 10^1 = 10$ ✓ (ascending exponents → ascending values)
- $-10^2 = -100 < -10^1 = -10$ ✓ (ascending exponents → **descending** values)

Therefore, to maintain global ascending order while sorting exponents, negatives must be sorted **in reverse** of positives.

---

## Hierarchical Sorting Order (Theorem 2)

The **necessity proof** establishes that the correct radix-sort hierarchy for floating-point values is:

$$\text{Sign} \to \text{Exponent} \to \text{Mantissa}$$

**Proof sketch by contradiction:**
- If exponent were primary: $\{-2.0, 0.5, 0.0\}$ fails (exponents $0, -1, 0$ don't preserve order across sign boundary)
- If mantissa were primary: $\{0.0, 0.5, -2.0\}$ fails (mantissas $0, 1, 10$ place negative last)
- Only sign-first partitioning creates sub-partitions where exponent and mantissa comparisons remain locally valid

---

## Applications in Engineering

### 1. **High-Performance Sorting Algorithms**
   - GPU/parallel sorting of large floating-point datasets (scientific computing, signal processing)
   - Avoiding branch prediction penalties from floating-point comparisons on hardware with limited FPU capability

### 2. **Scientific Data Processing**
   - Sorting simulation outputs (CFD, FEM results) with mixed positive/negative values
   - Organizing sensor data across multiple orders of magnitude

### 3. **Database Systems**
   - Indexing floating-point columns in scientific databases
   - Radix-based B-tree implementations for IEEE 754 numbers

### 4. **Graphics & Game Engines**
   - Depth-sorting transparent objects (often negative Z-values) for correct rendering order
   - Sorting point-light contributions by distance-based exponent

### 5. **Machine Learning**
   - Sorting activation values or loss terms during training
   - Radix-sort variants for efficient histogram computation in tree-building algorithms

---

## Common Mistakes / Pitfalls

### ❌ Mistake 1: Using Unsigned Integer Comparison Directly
**Problem:** Treating floating-point bit representations as unsigned integers breaks for negative numbers.
```
-2.0 (binary: 11000000000...0) > 0.5 (binary: 00111111000...)  // Wrong!
```
**Solution:** Apply sign-dependent transformation before bitwise comparison.

### ❌ Mistake 2: Forgetting Sign-Dependent Sort Direction
**Problem:** Sorting all exponents ascending, even for negative sub-partition.
```
Input (negative partition):  [-10.0, -1.0, -0.1]  (exponents: 1, 0, -1)
Sorted ascending by exponent: [-0.1, -1.0, -10.0]  // Wrong order!
```