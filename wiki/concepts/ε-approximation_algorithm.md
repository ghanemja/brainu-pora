# ε-approximation algorithm

## Definition

An **ε-approximation algorithm** is a polynomial-time algorithm that produces a solution guaranteed to be within a multiplicative factor of $(1 + \varepsilon)$ of the optimal solution for an optimization problem, where $\varepsilon > 0$ is a user-specified approximation parameter.

More formally, for a minimization problem with optimal solution value $OPT$, an ε-approximation algorithm computes a solution with value $SOL$ such that:

$$SOL \leq (1 + \varepsilon) \cdot OPT$$

For maximization problems, the inequality reverses:

$$SOL \geq \frac{1}{1 + \varepsilon} \cdot OPT$$

The algorithm's runtime may depend on $\varepsilon$—typically, smaller $\varepsilon$ values permit longer computation. This stands in contrast to fixed approximation algorithms, where the approximation ratio is a constant independent of the problem instance.

## Key Equations

**Approximation ratio definition (minimization):**
$$\rho = \frac{SOL}{OPT} \leq 1 + \varepsilon$$

**Relative error:**
$$\text{error} = \frac{SOL - OPT}{OPT} \leq \varepsilon$$

**Runtime dependency (typical FPTAS structure):**
$$T(n, \varepsilon) = \text{poly}\left(n, \frac{1}{\varepsilon}\right)$$

where $n$ is the input size. This polynomial dependence on $1/\varepsilon$ ensures tractability for reasonable precision requirements.

## Physical Intuition / Derivation

### Why ε-approximation matters

Consider a hard optimization problem (e.g., NP-hard) where finding the optimal solution requires exponential time. An ε-approximation algorithm trades solution quality for computational tractability:

- **For small $\varepsilon$** (say $\varepsilon = 0.01$): The algorithm guarantees a solution within 1% of optimal, but may require longer runtime
- **For large $\varepsilon$** (say $\varepsilon = 0.5$): The algorithm is faster but accepts solutions up to 50% worse than optimal

### Connection to the source material

In the LZ77 compression context presented in the source material, an ε-approximation algorithm for pre-editing with budget $k$ modifications would guarantee:

$$C_{LZ77}(w') + k \log |w| \leq (1 + \varepsilon) \cdot OPT$$

where $OPT$ is the minimum possible combined cost of compression plus edit storage over all $k$-edit variants of $w$.

### Key structural insight

The approximation ratio $(1 + \varepsilon)$ is **relative to the optimal**, not absolute. This relative guarantee becomes weaker as the problem scale increases, but it is:
- **Instance-dependent**: A good approximation on one instance may be poor on another at different scales
- **Precision-adaptive**: Users can adjust $\varepsilon$ based on problem constraints and tolerance

## Applications in Engineering

### 1. Computational Optimization
- **Integer linear programming (ILP)**: ε-approximation algorithms approximate hard integer programs (e.g., resource allocation, bin packing)
- **Scheduling**: Task scheduling on parallel machines with deadline constraints
- **Network design**: Minimum-cost network flow with capacity constraints

### 2. Data Compression & Information Theory
- **String pre-processing for compression**: As in the source material, pre-edit strings to improve LZ77/LZ78 compressibility while charging for edits
- **Lossy compression**: Quantization algorithms with bounded reconstruction error
- **Streaming algorithms**: Process unbounded data streams with bounded memory, guaranteeing approximate results

### 3. Machine Learning & Approximation
- **Clustering**: $k$-means clustering approximates optimal cluster assignments
- **Matrix factorization**: Low-rank SVD approximations with controlled spectral error
- **Neural network pruning**: Reduce model size while maintaining accuracy within $\varepsilon$ of full model

### 4. Operations Research
- **Vehicle routing**: Traveling salesman problem variants with $\varepsilon$-approximation guarantees
- **Facility location**: Approximate facility placement to minimize total cost
- **Auction mechanisms**: Design incentive-compatible auctions with bounded efficiency loss

### 5. Geometry & Graphics
- **Polygon simplification**: Reduce vertex count while keeping Hausdorff distance $\leq \varepsilon$
- **Point cloud decimation**: Select representative points with bounded distortion
- **Mesh approximation**: Simplify 3D models within geometric error bounds

## Common Mistakes / Pitfalls

### 1. Confusing approximation ratio with absolute error
**Mistake**: Treating $(1 + \varepsilon) \cdot OPT$ as an additive $+ \varepsilon$ bound
**Correct**: The error scales with the problem—larger optimal solutions permit larger absolute gaps

### 2. Ignoring runtime dependency on $\varepsilon$
**Mistake**: Assuming ε-approximation algorithms always run in polynomial time
**Correct**: Runtime typically grows with $1/\varepsilon$ (or $1/\varepsilon^2$, etc.); very small $\varepsilon$ may be impractical

### 3. Missing that approximation is relative to unknown $OPT$
**Mistake**: Concluding that $SOL \leq (1+\varepsilon) \cdot OPT$ means the algorithm is "close to optimal"
**Correct**: Without knowing $OPT$, the absolute gap is unknown; the guarantee is *relative* and *worst-case*

### 4. Assuming better approximation ratio always means better algorithm
**Mistake**: Choosing an algorithm with ratio $(1 + \varepsilon/2)$ without considering runtime
**Correct**: Compare **frontiers**: algorithm A might give $(1.1, \text{fast})$ while B gives $(1.01, \text{very slow})$; problem context determines the right choice

### 5. Overlooking FPTAS vs. PTAS distinctions
**Mistake**: Treating "fully polynomial-time approximation scheme" (FPTAS) and "polynomial-time approximation scheme" (PTAS) as equivalent
**