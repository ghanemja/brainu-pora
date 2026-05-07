# FPT (Fixed-Parameter Tractable)

## Definition

**Fixed-Parameter Tractability (FPT)** is a computational complexity concept that characterizes problems solvable in polynomial time when restricted to a secondary parameter in addition to the input size.

Formally, a decision problem parameterized by $k$ is **FPT** if there exists an algorithm that solves it in time:

$$f(k) \cdot |I|^{O(1)}$$

where:
- $f(k)$ is an arbitrary computable function depending only on parameter $k$
- $|I|$ is the input size
- The polynomial degree is constant and independent of $k$

**Contrast with classical NP-hardness**: A problem may be NP-hard in general but still FPT for small values of a relevant parameter. This separates "hard" complexity that comes from the parameter versus hardness inherent to the problem itself.

### Parameter Selection

The choice of parameter is crucial. For Rectangle Stabbing (the motivating example), the parameter $k = |L^*|$ represents the size of the optimal solution. A problem is tractable with respect to this parameter if we can find or approximate a solution in time $f(k) \cdot \text{poly}(n)$.

---

## Key Equations

### Running Time Characterization

For an FPT algorithm with parameter $k$ and input size $n = |I|$:

$$T(n, k) = f(k) \cdot n^{O(1)}$$

**Example**: The Rectangle Stabbing parameterized approximation algorithm runs in time:
$$k^{O(k)} \cdot (|L| \cdot |R|)^{O(1)}$$

This is FPT in $k$ because the exponential dependence ($k^{O(k)}$) is isolated to the parameter, not the input size.

### Approximation Ratio in Parameterized Setting

For parameterized approximation, we seek algorithms returning solution of size at most $\alpha k$ while running in $f(k) \cdot \text{poly}(n)$ time:

$$\text{Solution size} \leq \alpha \cdot k_{\text{opt}}$$

where $\alpha > 1$ is the approximation ratio and $k_{\text{opt}}$ is the optimal parameter value.

---

## Physical Intuition / Derivation

### Why Parameter Matters

Classical complexity theory treats all input aspects symmetrically. A problem with $n$ variables that is NP-hard appears equally hard whether:
- $n = 100$ with many "hard" variables, or  
- $n = 10000$ with only $k = 5$ variables involved in the actual hardness

**Parameterized complexity separates these cases**: FPT isolates the hardness to a specific structural parameter $k$, allowing exponential blowup in $f(k)$ while keeping the polynomial part constant.

### Intuition via Rectangle Stabbing

Given rectangles $R$ and lines $L$, finding minimum stabbing set is NP-hard. But if we know $k_{\text{opt}} \leq 5$:

- Brute force: try all $\binom{|L|}{k}$ subsets → time $O(|L|^k \cdot |R|)$ (exponential in both)
- Parameterized approach: exploit structure, compute in time $f(5) \cdot \text{poly}(|L|, |R|)$ with $f(5)$ being a constant

The source material shows an FPT algorithm running in $k^{O(k)} \cdot (|L||R|)^{O(1)}$ time that achieves a $7k/4$ approximation.

### W[1]-hardness as FPT's Negative Counterpart

Just as some problems are NP-complete (unlikely polynomial solution), some are **W[1]-hard** (unlikely FPT solution). The source shows:

$$\text{Rectangle Stabbing} \notin \text{FPT} \text{ (unless FPT} = \text{W[1])}$$

meaning no $f(k) \cdot n^{O(1)}$ algorithm exists for exact solution, even though polynomial 2-approximations exist.

---

## Applications in Engineering

### 1. **Computational Geometry & Sensor Networks**

The Optimal Discretization problem (generalized by Rectangle Stabbing) applies to:
- **Fault-tolerant sensor networks**: Partition 2D space with minimum axis-parallel lines to separate sensor regions
- **Discretization in machine learning**: Divide feature space to separate different classes with minimal boundaries

### 2. **VLSI & Circuit Design**

Rectangle stabbing models **pin routing** and **layer assignment**:
- Minimize horizontal/vertical layers (lines) needed to connect rectangular routing regions
- FPT algorithms enable exact solutions when optimal layer count is small

### 3. **Computational Biology**

Parameterized approximation algorithms for geometric covering problems aid in:
- **DNA sequence alignment**: Model as stabbing problems over score matrices
- **Protein structure prediction**: Discretize 3D space around molecular structures

### 4. **Resource Allocation & Scheduling**

When scheduling tasks on machines, geometric interpretations lead to stabbing problems:
- Tasks as rectangles in (time, resource-type) space
- Lines represent machine allocations
- FPT algorithms provide solutions when optimal allocation count is bounded

---

## Common Mistakes / Pitfalls

### 1. **Confusing FPT with Polynomial-Time**

❌ **Wrong**: "FPT means the algorithm is polynomial time"

✓ **Right**: "FPT means polynomial in $n$ for **fixed** $k$. For varying $k$, time can be exponential in $k$."

Example: $2^k \cdot n^2$ is FPT; $2^n$ is not.

### 2. **Ignoring the Parameter Choice**

❌ **Wrong**: "Rectangle Stabbing is FPT" (without specifying parameter)

✓ **Right**: "Rectangle Stabbing is FPT in $k = |L^*|$ with approximation ratio $7/4$; it is W[1]-hard for exact solutions."

### 3. **Misinterpreting Approximation