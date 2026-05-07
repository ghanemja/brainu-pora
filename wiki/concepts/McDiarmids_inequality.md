# McDiarmid's Inequality

## Definition

McDiarmid's inequality is a concentration bound for functions of independent random variables, applicable when the function satisfies a **bounded differences** property. It states that if a random variable is determined by independent random inputs and changes by at most $c_i$ when any single input is perturbed, then the variable is highly concentrated around its expectation.

**Formal Statement:** Let $X_1, X_2, \ldots, X_n$ be independent random variables taking values in sets $\mathcal{X}_1, \mathcal{X}_2, \ldots, \mathcal{X}_n$, and let $f: \mathcal{X}_1 \times \cdots \times \mathcal{X}_n \to \mathbb{R}$. If there exist constants $c_1, c_2, \ldots, c_n \geq 0$ such that

$$\sup_{x_1, \ldots, x_n, x_i'} |f(x_1, \ldots, x_i, \ldots, x_n) - f(x_1, \ldots, x_i', \ldots, x_n)| \leq c_i$$

for all $i$ (the function is **Lipschitz** with respect to each variable), then for any $t > 0$:

$$\Pr[|f(X_1, \ldots, X_n) - \mathbb{E}[f(X_1, \ldots, X_n)]| \geq t] \leq 2\exp\left(-\frac{2t^2}{\sum_{i=1}^n c_i^2}\right)$$

## Key Equations

**McDiarmid's Inequality (main form):**
$$\boxed{\Pr[|X - \mathbb{E}[X]| \geq t] \leq 2\exp\left(-\frac{2t^2}{\sum_{i=1}^n c_i^2}\right)}$$

**Uniform bound (when $c_i = c$ for all $i$):**
$$\Pr[|X - \mathbb{E}[X]| \geq t] \leq 2\exp\left(-\frac{2t^2}{nc^2}\right)$$

**Application to graph problems:** In the source material, for edge-counting random variables $X_i$ depending on vertex labels:
$$\Pr[|X_i - \mathbb{E}[X_i]| > t] \leq 2\exp\left(-\frac{t^2}{\Delta(G') m'}\right)$$

where $\Delta(G')$ is maximum degree and $m'$ is edge count. This follows because changing one vertex label affects edges incident to that vertex (Lipschitz constant = degree).

## Physical Intuition / Derivation

### Why Does It Work?

McDiarmid's inequality exploits a key insight: **if the function is not too sensitive to changes in any single variable, then extreme deviations are exponentially unlikely.**

Think of it as a "smoothness" argument:
- If changing input $X_i$ can change the output by at most $c_i$, the function is "locally smooth"
- Global smoothness (bounded differences across all variables) prevents rare combinations of inputs from conspiring to create large deviations
- The denominator $\sum c_i^2$ reflects cumulative uncertainty: many small contributions add up

### From Bounded Differences to Concentration

The proof uses the **martingale method**:

1. Define a sequence of random variables: $Y_0 = \mathbb{E}[f]$ and $Y_i = \mathbb{E}[f | X_1, \ldots, X_i]$
2. Each step $Y_i - Y_{i-1}$ is a **martingale difference** bounded by $c_i$ (by bounded differences property)
3. Apply **Azuma's inequality** (or derive Chernoff-style bounds) to the martingale:
   $$\Pr[f - \mathbb{E}[f] \geq t] \leq \exp\left(-\frac{2t^2}{\sum c_i^2}\right)$$

### Graph Partitioning Example (from source)

In the parallel graph partitioning algorithm:
- $X_i$ = number of cut edges in piece $i$ (random over vertex label assignments)
- Changing one vertex's label affects only edges incident to that vertex
- Lipschitz constant = degree of that vertex
- Sum of squared Lipschitz constants = $\sum_v \deg^2(v) \leq \Delta \cdot m'$
- Therefore: $\Pr[X_i$ deviates by $t] \leq 2\exp(-t^2/(\Delta \cdot m'))$

## Applications in Engineering

### 1. **Parallel Graph Algorithms**
The source material applies McDiarmid's inequality to prove high-probability guarantees for:
- **Balanced graph partitioning**: ensuring cut edges are $O(m/k^2)$ with high probability
- **Bucket-based randomized algorithms**: showing bucket sizes concentrate around their mean
- **Culled partition construction**: proving that edge removal phases either halve edges or reach degree bounds

### 2. **Randomized Load Balancing**
- **Job assignment**: distribute $n$ jobs to $m$ machines; use McDiarmid to show load concentration
- **Hashing**: prove that hash collisions concentrate (collision count is Lipschitz in item labels)

### 3. **Machine Learning / Randomized Algorithms**
- **Generalization bounds**: if a loss function depends Lipschitz on many data point labels
- **Random sampling**: showing sample statistics concentrate around population statistics
- **Monte Carlo methods**: bounding deviation of stochastic approximations

### 4. **Network Design**
- **Routing algorithms**: distributing flows with concentration guarantees
- **Resource allocation**: proving utilization metrics stay near expected values with high probability

### 5. **Combinatorial Optimization**
- **Randomized rounding**: analyzing performance of probabilistic solutions
- **Greedy algorithms**: bounding deviation from expected cost across random input orderings