# Recursive Algorithm Analysis

## Definition

**Recursive algorithm analysis** is a rigorous methodology for determining the time complexity, space complexity, and accuracy bounds of algorithms that solve problems by recursively reducing them to smaller subproblems of the same structure.

In the context of matrix operations and graph algorithms, recursive analysis involves:

1. **Problem decomposition**: Breaking a problem of size $n$ into subproblems of size $n/\sigma$ (or similar reduction factor)
2. **Recursion depth tracking**: Measuring how many levels of recursion occur before reaching base cases
3. **Work aggregation**: Summing computational costs across all recursive levels, including oracle calls and ancillary operations
4. **Parameter evolution**: Tracing how algorithm parameters (e.g., approximation tolerance $\varepsilon$) change across recursion levels

The analysis typically yields a **recurrence relation** of the form:
$$T(n) = \text{(work at current level)} + \sum_{i=1}^{k} T(\text{subproblem}_i)$$

which is then solved to determine overall complexity.

---

## Key Equations

### General Recurrence Template

For a recursive algorithm with branching factor $k$, reduction factor $\sigma$, and oracle cost $O_{\text{DAG}}$:

$$T(m, n, \varepsilon, h) \leq \tilde{O}\left(T\left(m, n, \varepsilon, \frac{h}{\lambda}\right)\right) + \sum_{i} \tilde{O}\left(T\left(m_i, \frac{n}{\sigma}, \left(1 - \frac{1}{\log n}\right)\varepsilon, \frac{n}{W}\right)\right) + O_{\text{DAG}}(O(\lambda wm))$$

where:
- $\lambda = \sigma = 2^{\log^{1-\delta} n}$ (reduction parameters)
- $\varepsilon$ is approximation tolerance (decays slowly to avoid over-recursion)
- $m_i$ sizes of subproblems at level $i$
- $\tilde{O}(\cdot)$ suppresses polylogarithmic factors

### Recursion Depth Bound

$$\text{Depth} \leq \log_\lambda n = \log_{2^{\log^{1-\delta}n}} n = \tilde{O}(1)$$

More precisely, depth = $O(\log^{1/(1-\delta)} n)$, which is quasi-linear in log space.

### Parameter Degradation

The approximation parameter decays by factor $(1 - 1/\log n)$ per level:

$$\varepsilon_{\ell} = \left(1 - \frac{1}{\log n}\right)^{\ell} \varepsilon_0 \geq \frac{\varepsilon_0}{2} \quad \text{for } \ell \leq O(\log^{\delta}n)$$

This **controlled degradation** ensures $\varepsilon$ remains within constant factors of its initial value despite deep recursion.

### Oracle Call Budget

Total oracle calls across all recursion levels:

$$\sum_{\ell=0}^{\text{depth}} \#\text{calls}_\ell = \tilde{O}(1)^{\log^\delta n} = \hat{O}(1)$$

Each oracle operates on graphs with $\hat{O}(wm)$ edges, giving total oracle overhead:

$$\tilde{O}(1)^{\log^\delta n} \cdot \lambda wm = \hat{O}(wm)$$

---

## Physical Intuition / Derivation

### Why Recursive Analysis Matters

Traditional algorithm analysis (e.g., worst-case counts) often misses crucial structure in modern algorithms. Recursive decomposition arises naturally when:

- **Hierarchical structure exists**: Matrix multiplication can decompose into smaller matrix products
- **Divide-and-conquer is optimal**: Breaking a large problem reduces fundamental bottlenecks (communication, conditioning, oracle complexity)
- **Parallelization is possible**: Independent recursive calls execute simultaneously

### Understanding the Recurrence

Consider dividing an $M \times K$ by $K \times N$ matrix product recursively:

$$\text{Problem size: } (M, K, N) \rightarrow (m_0, k_0, n_0) \text{ with } M = m_0 m^\ell, \, K = k_0 k^\ell, \, N = n_0 n^\ell$$

**Why this structure arises:**
- Each recursion level solves smaller problems (size scales by $m, k, n < 1$)
- Base case computes small products with algorithm $\beta$ directly
- Intermediate levels aggregate partial results using oracle calls (e.g., approximate SSSP on DAGs)

**Key insight—parameter tracking:**
The algorithm must maintain:
- **Approximation tolerance $\varepsilon$**: Degrades slightly per level to avoid exponential error accumulation
- **Recursion depth $h$**: Halves or decreases by factor $\lambda$ per level
- **Reduced problem sizes**: $n/\sigma$ (clustering size), edges $O(\lambda wm)$ (oracle input size)

### Why Depth Remains Polylog

With $\lambda = \sigma = 2^{\log^{1-\delta}n}$ (super-polynomial but subexponential):

$$\log_\lambda n = \frac{\log n}{\log \lambda} = \frac{\log n}{\log^{1-\delta}n} = \frac{1}{\log^{-\delta}n} = o(\log n)$$

This **quasi-linear depth** is crucial: it keeps total oracle calls manageable ($\hat{O}(1)$ invocations) despite deep recursion.

---

## Applications in Engineering

### 1. **High-Performance Linear Algebra**
- **Recursive matrix multiplication**: Strassen's algorithm and variants reduce asymptotic complexity for large dense matrices
- **Sparse matrix kernels**: Recursive blocking structure improves cache locality and parallelism
- **Accuracy certification**: Bound propagation through recursion levels guarantees final error