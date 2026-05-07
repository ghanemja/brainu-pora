# polynomial-time approximation scheme (PTAS)

## Definition

A **polynomial-time approximation scheme (PTAS)** is an algorithm that, given an optimization problem instance and an error parameter $\varepsilon > 0$, produces a solution with objective value within a factor of $(1 + \varepsilon)$ of optimal in time polynomial in the instance size $n$ (but potentially exponential in $1/\varepsilon$).

Formally, a PTAS for a minimization problem is an algorithm $\mathcal{A}$ such that:
- **Input:** instance $I$ and error bound $\varepsilon > 0$
- **Output:** solution with value $\text{OPT}(I) \leq A(I, \varepsilon) \leq (1+\varepsilon) \cdot \text{OPT}(I)$
- **Runtime:** $\text{poly}(|I|) \cdot f(1/\varepsilon)$ for some computable function $f$

The key distinction is that runtime must be polynomial in instance size for any fixed $\varepsilon$, though it can be arbitrarily bad (even super-exponential) as $\varepsilon \to 0$.

### Relationship to other approximation classes

| Class | Runtime | Approximation Factor |
|-------|---------|----------------------|
| **PTAS** | $\text{poly}(n) \cdot f(1/\varepsilon)$ | $(1+\varepsilon)$-factor |
| **FPTAS** | $\text{poly}(n, 1/\varepsilon)$ | $(1+\varepsilon)$-factor |
| **APX** | $\text{poly}(n)$ | constant factor (e.g., $O(1)$) |

**FPTAS** (Fully PTAS) is strictly stronger—it requires the algorithm to be polynomial in both $n$ and $1/\varepsilon$, making it practical for small $\varepsilon$.

## Key Equations

For a minimization problem with optimal value $\text{OPT}$:

$$\text{OPT} \leq A(I, \varepsilon) \leq (1+\varepsilon) \cdot \text{OPT}$$

Equivalently, the **approximation ratio** satisfies:

$$\rho(\varepsilon) = \frac{A(I,\varepsilon)}{\text{OPT}(I)} \leq 1 + \varepsilon$$

**Runtime complexity:**
$$T(n, \varepsilon) = \text{poly}(n) \cdot \text{exp}(O(1/\varepsilon^k))$$

for some polynomial in $n$ and some constant $k$ (problem-dependent). Common forms include $|X|^{O(1/\varepsilon)}$ or $2^{O(1/\varepsilon^2)}$.

## Physical Intuition / Derivation

### Why PTAS matters

PTAS occupies a "sweet spot" in approximation theory:

1. **Better than constant-factor approximation:** While APX algorithms guarantee a fixed approximation ratio regardless of effort, PTAS lets you *improve* the approximation ratio arbitrarily by accepting longer runtime.

2. **Computationally realistic for moderate $\varepsilon$:** If you only need 1% error ($\varepsilon = 0.01$), the algorithm may run in reasonable time even if $\varepsilon \to 0$ causes explosion.

3. **Not always efficient:** Unlike FPTAS (which avoids exponential dependence on $1/\varepsilon$), a PTAS can have runtimes like $\text{poly}(n) \cdot 2^{1/\varepsilon}$, making it impractical for very small errors.

### Common derivation strategy: dynamic programming with discretization

Many PTAS algorithms use a **rounding and DP** approach:

1. **Scale the input** by factor $\Delta = \varepsilon \cdot \text{OPT}/k$ for some constant $k$
2. **Round** all problem parameters to multiples of $\Delta$ (losing at most $\varepsilon \cdot \text{OPT}$ in error)
3. **Apply DP** with state space polynomial in the rounded instance size
4. **Unround** the solution

This reduces the state space from $\text{poly}(n, M)$ (where $M$ is max value) to $\text{poly}(n/\varepsilon)$, yielding runtime $\text{poly}(n) \cdot \text{poly}(1/\varepsilon)$.

### Example from source material

The calibration distance computation achieves:
- **Noiseless, uniform distribution:** exact in $O(|X|^4)$ time
- **Uniform distribution:** PTAS in $|X|^{O(1/\varepsilon)}$ time
- **General case:** PTAS in $(|X|/\varepsilon)^{O(1/\varepsilon)}$ time

The exponent depends inversely on $\varepsilon$, showing the characteristic PTAS trade-off.

## Applications in Engineering

### 1. **Knapsack Problem**
The classic 0/1 knapsack admits an FPTAS via dynamic programming with value-scaling. For any $\varepsilon > 0$, compute optimal solution for rounded values in time $\text{poly}(n, 1/\varepsilon)$.

### 2. **Bin Packing & Resource Allocation**
Approximating minimum number of bins (or machines) for packing jobs. PTAS algorithms enable quality-vs-runtime trade-offs in industrial scheduling.

### 3. **Geometric Problems**
- **Euclidean TSP:** PTAS exists in 2D (and higher dimensions) via geometric divide-and-conquer and DP
- **Facility location:** Approximating cost of placing warehouses/factories to minimize total distance

### 4. **Calibration in Machine Learning** (from source)
Computing distance from calibration for predictions: approximate the minimum $\ell_\infty$ error of a predictor in $(|X|