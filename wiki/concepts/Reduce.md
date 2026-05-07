# Reduce

## Definition

**Reduce** is a fundamental parallel primitive that computes an aggregate value by applying an associative binary function $f$ across all elements of an array. Given an array $A = [a_1, a_2, \ldots, a_n]$ and an associative operator $f$, reduce produces:

$$\text{reduce}(A, f) = f(f(\cdots f(a_1, a_2), a_3) \cdots, a_n)$$

The key constraint is that $f$ must be **associative**, meaning $f(f(a, b), c) = f(a, f(b, c))$ for all valid inputs. This associativity enables parallel computation by allowing arbitrary grouping of subproblems.

### Complexity Characteristics

- **Work**: $O(n)$ where $n = |A|$ (assuming $f$ takes $O(1)$ time per operation)
- **Depth** (parallel time): $O(\log n)$
- **Span**: Logarithmic in array size due to parallel tree-structured evaluation

## Key Equations

**Sequential reduction** (baseline):
$$\text{result} = a_1 \oplus a_2 \oplus a_3 \oplus \cdots \oplus a_n$$

**Parallel tree reduction** (binary tree structure with $\log n$ levels):
$$\text{depth} = \lceil \log_2 n \rceil$$

**Work efficiency ratio**:
$$\text{Work}(n) = O(n) \quad \text{vs.} \quad \text{Depth}(n) = O(\log n)$$

This gives a **parallelism factor** of roughly $\frac{n}{\log n}$ available CPUs to achieve the speedup.

## Physical Intuition / Derivation

### Why Associativity Matters

In sequential computation, we must evaluate reductions strictly left-to-right: $((a_1 \oplus a_2) \oplus a_3) \oplus a_4$. This creates a **data dependency chain** of length $n$—each result depends on the previous one.

In parallel computation, associativity allows us to regroup:
$$((a_1 \oplus a_2) \oplus (a_3 \oplus a_4))$$

Now we can compute both $a_1 \oplus a_2$ and $a_3 \oplus a_4$ simultaneously, then combine results. This transforms a linear dependency chain into a **tree structure** with depth $\log n$.

### Tree Reduction Structure

For $n = 8$ elements:

**Level 0 (parallel):** $a_1 \oplus a_2$, $a_3 \oplus a_4$, $a_5 \oplus a_6$, $a_7 \oplus a_8$ → 4 results  
**Level 1 (parallel):** combine pairs → 2 results  
**Level 2 (parallel):** final combination → 1 result  

**Total depth:** $\log_2(8) = 3$ steps (optimal for 8 processors)

### Work Preservation

Despite parallelism, we still perform $n-1$ binary operations total—same as sequential reduction. We simply redistribute the operations across $\log n$ time steps instead of $n$ steps. This is why **work is $O(n)$** even with logarithmic depth.

## Applications in Engineering

### 1. **Data Aggregation (Databases & Analytics)**
- Sum, product, max, min over large datasets
- Computing running totals in data processing pipelines
- Histogram reduction in database query engines

### 2. **Linear Algebra & Scientific Computing**
- **Dot products**: $\vec{u} \cdot \vec{v} = \sum_{i=1}^{n} u_i v_i$ (reduce via multiplication + addition)
- **Matrix reductions**: Summing matrix elements, computing norms
- **Parallel linear solvers** that depend on global inner products

### 3. **Graphics & Computer Vision**
- Reducing color channels across image pixels
- Computing image statistics (mean luminance, histogram reduction)
- Parallel rendering: combining partial results from different processors

### 4. **Network & Systems**
- Aggregating telemetry data from distributed sensors
- Collective communication primitives in MPI (AllReduce)
- Load balancing: reducing task completion times

### 5. **Machine Learning**
- Gradient reduction in distributed training (averaging gradients across workers)
- Batch normalization statistics computation
- Decentralized optimization (parameter server reduction)

### 6. **Signal Processing**
- Computing signal energy: $E = \sum_{i=1}^{n} |x_i|^2$
- Parallel spectral analysis and FFT computation
- Beamforming weight reduction

## Common Mistakes / Pitfalls

### 1. **Assuming Commutativity**
Reduce requires only **associativity**, not commutativity. Subtraction is associative in grouping but non-commutative:
$$((a - b) - c) \neq (a - (b + c))$$ ✗

Floating-point addition is **neither** associative nor commutative in practice due to rounding:
$$(1.0 + \epsilon + (-1.0)) \neq (1.0 + (\epsilon + (-1.0)))$$

This can cause numerical instability in parallel reductions.

### 2. **Confusing Reduce with Scan**
- **Reduce**: single output (aggregation)
- **Scan**: produces all prefix values (more work but more information)

Trying to use reduce when scan is needed (or vice versa) is a common algorithmic error.

### 3. **Ignoring Identity Element Semantics**
A neutral/identity element $e$ satisfies $f(e, a) = f(a, e) = a$. Many parallel reduce implementations assume the identity element is the first array element, but this fails for empty arrays or when semantically incorrect.

### 4. **Assuming $O(\log n)$ Speedup is Always Achievable**
Achieving $O(\log n)$ depth requires **$O(n/\log n