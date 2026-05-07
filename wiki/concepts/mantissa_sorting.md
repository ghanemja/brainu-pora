# Mantissa Sorting

## Definition

**Mantissa sorting** is the third and final pass in a three-stage radix-based sorting algorithm for IEEE 754 floating-point numbers. It operates on elements that have already been partitioned by sign and exponent, where all elements within a sub-partition share identical sign and exponent values.

In this final stage, elements are ordered by their fractional part (mantissa/significand) as if they were unsigned integers. Because sign and exponent are already equal within each partition, the mantissa directly determines the relative numerical ordering of elements.

## Key Equations

The complete three-pass sort hierarchy is formalized as:

$$\text{Sort order} = \text{Sign} \to \text{Exponent} \to \text{Mantissa}$$

For an IEEE 754 floating-point number representation:

$$x = (-1)^s \cdot 2^p \cdot (1.m)$$

where:
- $s$ ∈ {0, 1}: sign bit
- $p$ ∈ $\mathbb{Z}$: exponent (biased)
- $m$ ∈ $[0, 1)$: mantissa/significand bits

**Relative ordering constraint within a partition:**

Given elements with identical $(s, p)$ pairs, for ascending sort:
$$m_i < m_j \iff x_i < x_j$$

**Sort direction dependency on sign:**

- **Positive numbers** ($s=0$): mantissa sorted in **ascending** order
- **Negative numbers** ($s=1$): mantissa sorted in **descending** order

This is because for negative values, a larger mantissa produces a smaller (more negative) number:
$$-2^p \cdot (1.m_1) < -2^p \cdot (1.m_2) \text{ when } m_1 > m_2$$

## Physical Intuition / Derivation

### Why Three-Pass Hierarchical Sorting?

The hierarchical structure emerges from the nested dominance of floating-point components:

1. **Sign is primary** because it creates the fundamental numerical boundary: negative vs. non-negative. No refinement of exponent or mantissa can overcome a wrong sign.

2. **Exponent is secondary** because it determines magnitude order-of-magnitude. Within numbers of the same sign, the exponent establishes coarse ordering: $2^{10}$ is always larger than $2^{-5}$ (for positive numbers).

3. **Mantissa is tertiary** because it refines ordering within a single order-of-magnitude. For fixed sign and exponent, $1.0001_2 \times 2^p < 1.1111_2 \times 2^p$.

### Proof of Necessity (Theorem 2)

**Counterexample to alternative orderings:**

Consider sorting $[-2.0, 0.0, 0.5]$ in ascending order.

IEEE 754 representations:
- $x = -2.0$: $(s_x, p_x, m_x) = (1, 1, 0)$
- $y = 0.0$: $(s_y, p_y, m_y) = (0, 0, 0)$
- $z = 0.5$: $(s_z, p_z, m_z) = (0, -1, 0)$

**If mantissa is sorted first:** All three have mantissas of 0, leaving order undefined by the first pass. Subsequent passes cannot reliably establish global order.

**If exponent is sorted first:** We get partitions ordered by $p_z(-1) < p_{x,y}(0,1)$, placing $z$ before $x$ and $y$. But $z = 0.5 > -2.0 = x$, violating the ascending invariant.

**Only sign → exponent → mantissa works:** 
- First pass partitions: $\{x\}$ (negative), $\{y, z\}$ (non-negative)
- Second pass on exponent: Within non-negatives, $p_z = -1 < p_y = 0$
- Third pass on mantissa: All mantissas equal within subpartitions
- **Result:** $[-2.0, 0.5, 0.0]$ ✓

### Mantissa-as-Integer Equivalence

Within a fixed $(s, p)$ partition, comparing mantissas directly—treating them as unsigned integers—preserves numerical order because:

$$\text{If } m_i < m_j \text{ (as unsigned ints)}, \text{ then } (1 + m_i \times 2^{-b}) < (1 + m_j \times 2^{-b})$$

where $b$ is the bit-width of the mantissa. Scaling by the common exponent $2^p$ preserves this ordering.

## Applications in Engineering

### 1. **GPU-Accelerated Sorting**
Mantissa sorting is a key component of **bitonic sort** and **radix sort** implementations for floating-point data on GPUs. The three-pass structure naturally parallelizes across thousands of threads, each handling a sub-partition independently.

**Example:** NVIDIA CUDA libraries use mantissa-based ordering in high-performance scientific computing kernels for sorting particle positions, sensor readings, or simulation outputs.

### 2. **Machine Learning & Data Processing**
Sorting neural network weights, activation values, and gradient tensors requires correct floating-point ordering. Mantissa sorting enables efficient GPU-based sorting of large datasets without converting to fixed-point representations.

### 3. **Real-Time Systems & Sensor Data**
Embedded systems processing continuous streams of floating-point measurements (temperature, pressure, voltage) use mantissa sorting for online statistical analysis, percentile ranking, and anomaly detection where IEEE 754 compliance is critical.

### 4. **Scientific Computing & Numerical Simulation**
Finite-element solvers, climate models, and CFD systems must sort floating-point residuals, node coordinates, and timestep values while maintaining numerical precision. Mantissa sorting ensures correct ordering without accumulated rounding errors.

### 5. **Financial Computing**
Portfolio systems and derivative pricing engines require stable, accurate sorting of floating-point monetary values and risk metrics across many decimal scales (from cents to billions).

## Common