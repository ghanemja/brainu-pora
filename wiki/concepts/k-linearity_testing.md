# k-linearity testing

## Definition

**k-linearity testing** is a property testing problem where, given query access to a function $f: \mathbb{R}^n \to \mathbb{R}$, the goal is to efficiently distinguish between two cases:

1. **Accept case**: $f$ is a $k$-linear function (a linear combination of at most $k$ variables)
2. **Reject case**: $f$ is $\epsilon$-far from all $k$-linear functions

A function is **$k$-linear** if it can be expressed as:
$$f(x) = c_0 + \sum_{i \in S} c_i x_i$$
where $|S| \leq k$ and $c_0, c_i \in \mathbb{R}$ are constants.

**Distance metric**: The proximity is measured in the $L^1$ metric under the Standard Gaussian distribution $\mathcal{N}(0, I_n)$ over the domain $\mathbb{R}^n$. A function is $\epsilon$-far from $k$-linear if:
$$\min_{g \text{ is } k\text{-linear}} \mathbb{E}_{x \sim \mathcal{N}(0,I_n)}[|f(x) - g(x)|] \geq \epsilon$$

**Query model**: The tester has approximate query access—it can query the function at points and receive values subject to noise or approximation.

## Key Equations

### Query Complexity Bounds

For $k$-linearity testing over $\mathbb{R}^n$ with parameter $\epsilon$, the known bounds are:

**Upper bound (tester complexity)**:
$$\text{Query complexity} = O\left(\frac{k}{\epsilon}\right)$$

**Lower bound (information-theoretic)**:
$$\text{Query complexity} = \Omega(k)$$

### Linearity Test via Gaussian Sampling

A natural tester checks the $L^1$ distance from linearity by:
$$\text{Dist}(f, \text{LIN}_k) = \mathbb{E}_{x \sim \mathcal{N}(0,I_n)}\left[\min_{\ell \text{ is } k\text{-linear}} |f(x) - \ell(x)|\right]$$

### Connection to Polynomial Testing

k-linearity is a special case of testing $k$-sparse polynomials where degree $d = 1$.

## Physical Intuition / Derivation

### Why Gaussians?

The Standard Gaussian distribution is chosen as the natural measure because:
- It is **scale-invariant** under rotations (orthogonal transformations)
- It provides a **canonical** probability measure on $\mathbb{R}^n$
- It makes the $L^1$ distance well-defined and computationally tractable
- It reflects real-world scenarios where data is often approximately normally distributed

### Why k-linearity Matters

In practice, many high-dimensional phenomena are approximately governed by only a few dominant variables. For example:
- In machine learning, feature selection identifies the $k$ most important features
- In scientific computation, dominant modes often capture system behavior
- Linearity is the simplest meaningful structure beyond constant functions

### Testing Strategy Intuition

A tester must:
1. **Sample** points $x_1, \ldots, x_m$ from $\mathcal{N}(0, I_n)$
2. **Query** $f$ at these points to get $f(x_i)$
3. **Fit** the best $k$-linear function to the samples
4. **Verify** that the residual error is small (accept) or large (reject)

The key insight: if $f$ is actually $k$-linear, fitting a $k$-dimensional subspace via least squares will capture it. If $f$ is far from $k$-linear, the residual will be large with high probability.

### Lower Bound Intuition

An adversary can construct a function that:
- Agrees with a $k$-linear function on a sparse set of points
- Deviates in directions orthogonal to the $k$-dimensional subspace
- Requires $\Omega(k)$ queries to distinguish from true $k$-linearity

This follows from information-theoretic arguments: there are $\binom{n}{k}$ possible supports for a $k$-linear function, requiring $\log \binom{n}{k} = \Theta(k \log n)$ bits of information, which translates to $\Omega(k)$ queries in the worst case.

## Applications in Engineering

### 1. **Machine Learning & Feature Selection**
- Testing whether a learned model depends on only $k$ features
- Validating sparse linear regression models
- Detecting overfitting when feature count exceeds true dimensionality

### 2. **Signal Processing**
- Testing if a signal is approximately spanned by $k$ basis vectors
- Compressive sensing: verify that signal reconstruction is valid under $k$-linearity assumption
- Dimensionality reduction validation

### 3. **Control Systems**
- Verifying that a high-dimensional system's input-output relationship is dominated by $k$ linear modes
- Reduced-order model validation: test if full system can be approximated by $k$-linear submodel

### 4. **Sensor Network Analysis**
- In distributed sensor arrays, test if measurements are approximately $k$-linear in environmental parameters
- Detect sensor failures or anomalies that violate linearity assumption

### 5. **Power Systems**
- Testing if power flow relationships remain approximately linear in operating regimes
- Contingency analysis: verify $k$-linear approximations of system dynamics

### 6. **Data Quality Assurance**
- Validate that high-dimensional datasets satisfy expected sparse linear structure
- Early detection of data corruption or anomalies

## Common Mistakes / Pitfalls

### 1. **Confusing k-linearity with k-sparsity**
- **Mistake**: Treating "at most $k$ nonzero coefficients" the same as "at most $k$ variables involved"
- **Clarification**: A $k$-linear function has exactly $k$ variables with nonzero coefficients in the representation $c_0 + \sum_{