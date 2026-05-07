# Rank Invariant

## Definition

The **rank invariant** is a fundamental algebraic invariant for multiparameter persistence modules that quantifies the "persistence" of topological features across a pair of parameter values. 

For a multiparameter persistence module $V$ (a family of vector spaces $\{V_\alpha\}_{\alpha \in \mathbb{R}^d}$ with linear maps $V_\alpha \to V_\beta$ for $\alpha \leq \beta$), the rank invariant is a function:

$$\text{rank}_V: \{(\alpha, \beta) \in \mathbb{R}^d \times \mathbb{R}^d : \alpha \leq \beta\} \to \mathbb{N}$$

defined by:
$$\text{rank}_V(\alpha, \beta) = \text{rank}(V_\alpha \to V_\beta)$$

That is, $\text{rank}_V(\alpha, \beta)$ is the rank (dimension of the image) of the structure map from the vector space at parameter value $\alpha$ to the vector space at parameter value $\beta$.

### Intuition

A feature that "persists" from $\alpha$ to $\beta$ corresponds to a linearly independent element in the image of the map $V_\alpha \to V_\beta$. The rank counts how many independent features remain present across this parameter interval.

## Key Equations

For parameters $\alpha \leq \beta \leq \gamma$ in the partial order on $\mathbb{R}^d$:

**Functoriality (Composition Property):**
$$\text{rank}_V(\alpha, \gamma) \leq \min(\text{rank}_V(\alpha, \beta), \text{rank}_V(\beta, \gamma))$$

**Monotonicity:**
If $\alpha_1 \leq \alpha_2$ and $\beta_1 \leq \beta_2$, then:
$$\text{rank}_V(\alpha_1, \beta_2) \geq \text{rank}_V(\alpha_2, \beta_1)$$

**Rank-Nullity on the Interval:**
$$\text{rank}_V(\alpha, \beta) = \dim(V_\alpha) - \text{nullity}(V_\alpha \to V_\beta)$$

where nullity is the dimension of the kernel of the inclusion map.

## Physical Intuition / Derivation

### Why the Rank Invariant Matters

In one-parameter persistence (the classical setting), the decomposition theorem gives a complete and interpretable description: every persistence module decomposes into intervals. This makes visualization and interpretation straightforward.

In multiparameter settings ($d \geq 2$), **no such decomposition theorem exists**—modules are fundamentally more complex and don't decompose nicely. The rank invariant provides a computable summary that:

1. **Captures persistence structure**: It counts how many "persistent" features cross between any two parameter regions.
2. **Is computable**: Unlike the full decomposition (which may not exist), the rank function can be computed directly from the module's representation.
3. **Is stable**: The rank invariant is robust to small perturbations of the input data, with controlled interleaving distance.

### Construction from Filtration Data

In practical applications, a multiparameter persistence module arises from a filtered simplicial complex or point cloud:
- Parameters $\alpha \in \mathbb{R}^d$ index different "filter levels"
- $V_\alpha = H_*(K_{\leq \alpha})$ is the homology of the complex up to filter value $\alpha$
- Structure maps arise from inclusion of subcomplexes

The rank invariant then counts independent $k$-dimensional holes that are "born" by filter level $\alpha$ and "survive" to filter level $\beta$.

## Applications in Engineering

### Data Analysis and Machine Learning
- **Topological data analysis (TDA)**: The rank invariant vectorizes the module into a feature vector suitable for downstream ML pipelines, avoiding the interpretability burden of full decomposition.
- **Biomedical data**: Multiparameter persistence has been applied to cell morphology data, gene expression networks, and protein structure analysis [source material references applications in biology].

### Stability and Robustness
- The rank invariant admits a controlled **erosion distance** that is stable with respect to the interleaving distance on persistence modules.
- This stability is crucial when data is noisy: small perturbations of input yield small changes in the rank invariant.

### Computational Topology
- Computing rank invariants is polynomial-time in the dimension of the module (via straightforward evaluation).
- Forms the basis for more refined invariants like the **Skyscraper Invariant**, which filters the rank invariant by restricting to "persistent-over-small-volume" features.

### Signal Processing and Filtering
- In multifiltered signal processing, the rank invariant can summarize how many frequency components, spatial modes, or temporal features persist across parameter ranges.

## Common Mistakes / Pitfalls

### 1. **Confusing Rank with Cardinality of Decomposition**
A common error is assuming that $\text{rank}_V(\alpha, \beta)$ equals the number of indecomposable summands that "live" between $\alpha$ and $\beta$. This is **only true in one parameter**. In multiple parameters, the module may not decompose, and rank is instead a direct count of linear dependencies.

### 2. **Assuming the Rank Invariant Determines the Module**
The rank invariant is **not complete**—it does not uniquely determine a module up to isomorphism. Different modules can share the same rank invariant. (The Skyscraper Invariant is strictly stronger.)

### 3. **Misinterpreting Monotonicity**
The monotonicity property does not mean $\text{rank}_V(\alpha, \beta)$ is decreasing in $\beta$. Rather, it is monotonic with respect to the partial order: expanding the parameter region in both coordinates preserves the inequality.

### 4. **Ignoring Parameter Geometry**
In multiparameter modules, which pairs $(\alpha, \beta)$ are "most relevant" depends on the geometry of the data and the scientific question. Naively evaluating rank at all pairs can miss important structure.

### 5. **Computational Complexity**