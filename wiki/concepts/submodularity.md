# Submodularity

## Definition

A set function $f: 2^V \to \mathbb{R}$ is **submodular** if it satisfies the *diminishing returns property*:

$$f(S \cup \{e\}) - f(S) \geq f(T \cup \{e\}) - f(T) \quad \forall S \subseteq T \subseteq V, \, e \notin T$$

Equivalently, for any two sets $S, T \subseteq V$:

$$f(S) + f(T) \geq f(S \cup T) + f(S \cap T)$$

**Intuition**: The marginal gain (or "value") of adding an element $e$ to a set decreases as the set grows larger. Adding a feature to an already-rich set yields less benefit than adding it to a sparse set.

A function is **supermodular** if the inequality reverses (increasing returns), and **modular** (or additive) if equality holds.

## Key Equations

### Diminishing Returns Formulation
$$\Delta_f(e \mid S) := f(S \cup \{e\}) - f(S) \text{ is non-increasing in } S$$

For submodular $f$: if $S \subseteq T$, then $\Delta_f(e \mid S) \geq \Delta_f(e \mid T)$.

### Greedy Approximation Guarantee
When maximizing a monotone submodular function via greedy selection (iteratively choosing the element with highest marginal gain), the approximation ratio is:

$$\text{OPT} \leq \frac{e}{e-1} \cdot \text{GREEDY} \approx 1.618 \times \text{GREEDY}$$

### Lovász Extension
For a submodular function $f$ on the ground set $V$, the Lovász extension $\bar{f}: [0,1]^{|V|} \to \mathbb{R}$ is defined as:

$$\bar{f}(\mathbf{x}) = \mathbb{E}_{u \sim [0,1]}[f(S_u(\mathbf{x}))]$$

where $S_u(\mathbf{x}) = \{i : x_i \geq u\}$. The Lovász extension is concave and minimizable in polynomial time via convex optimization.

## Physical Intuition / Derivation

### Why Diminishing Returns?

Consider adding sensors to a monitoring system:
- Adding the **1st sensor** provides maximal information gain (nothing before)
- Adding the **2nd sensor** provides less gain (correlated with 1st)
- Adding the **100th sensor** provides minimal gain (most correlation already captured)

This is *submodularity*: each new element contributes less marginal value as the set grows.

### Connection to Information Theory

In machine learning explanations, if $f(S)$ represents "how well features $S$ predict the target," submodularity arises naturally:
- Features are often redundant or correlated
- Adding features to an explanatory set with high predictive power yields diminishing improvements
- This contrasts with feature *interactions* (supermodular), where sets unlock disproportionate value only when combined

### Why It Matters for Complexity

From the source paper: global value functions in ML explanation problems exhibit **submodularity**, which implies:
1. **Greedy algorithms have approximation guarantees** (not just heuristics)
2. **Convex relaxations work**: The Lovász extension can be minimized via convex optimization in polynomial time
3. **Local vs. Global dichotomy**: Local explanations lack submodularity/monotonicity, making them NP-hard; global ones have these properties, enabling polynomial-time computation

## Applications in Engineering

### 1. Feature Selection & Interpretability
- **Problem**: Select a minimal subset of input features that preserves prediction accuracy
- **Application**: If the loss function is submodular in feature sets, greedy selection yields $(1 - 1/e)$-optimal solutions with polynomial runtime
- **Example**: Document summarization, sensor placement

### 2. Machine Learning Model Explanations
- **Sufficient reasons**: Find minimal feature subsets $S$ such that $f(S) \geq \theta$ (a threshold confidence)
- **Contrastive reasons**: Identify feature changes needed to flip a prediction
- **Guarantee**: When the value function is monotone submodular, these can be computed in polynomial time globally, enabling efficient explainability for neural networks and tree ensembles

### 3. Combinatorial Optimization
- **Influence maximization**: Maximize social spread in networks (submodular objective)
- **Budget-constrained placement**: Allocate limited resources (sensors, cameras, maintenance crews) to maximize coverage
- **Approach**: Use greedy algorithms with proven $(1 - 1/e)$ approximation

### 4. Distributed & Federated Learning
- Data/model utility functions in selection often exhibit submodularity
- Enables efficient subset selection without evaluating all combinations

### 5. Network & Infrastructure Design
- Redundancy placement, fault tolerance: marginal benefit of adding a redundant path decreases as network connectivity grows
- Cost-benefit tradeoffs in engineering projects

## Common Mistakes / Pitfalls

### 1. **Confusing Submodularity with Concavity**
- **Mistake**: Assuming a submodular function is concave (or vice versa)
- **Clarification**: Submodularity is a discrete property (on set lattices); concavity is continuous. However, the Lovász extension *bridges* them—it's the unique concave extension of a submodular function

### 2. **Greedy Optimality**
- **Mistake**: Treating greedy selection as optimal for submodular maximization
- **Truth**: Greedy gives $(1 - 1/e) \approx 0.632$ approximation; exact optimization is NP-hard in general. The approximation ratio is *tight*

### 3. **Ignoring the Monotonicity Requirement**
- **Mistake**: Applying greedy guarantees to non-monotone submodular functions
- **Requirement**: Greedy $(1 - 1/e)$ approximation holds *only