# δ-sufficient reason

## Definition

A **δ-sufficient reason** is a subset of input features $S \subseteq \{1, 2, \ldots, n\}$ that, when fixed to their values in a reference instance $x$, determines the output of a function $f$ with high probability—at least $\delta$—regardless of how other features vary.

More precisely:
- **Local δ-sufficient reason**: A subset $S$ is a local δ-sufficient reason for instance $x$ if varying features outside $S$ while keeping features in $S$ fixed at $x_S$ preserves the prediction with probability $\geq \delta$.
- **Global δ-sufficient reason**: A subset $S$ is a global δ-sufficient reason if, when averaging the local sufficiency condition over all instances drawn from the data distribution $D$, the expectation remains $\geq \delta$.

The concept quantifies *how much* a feature subset explains a model's prediction under distributional uncertainty, bridging deterministic explanations with probabilistic reasoning.

## Key Equations

**Local δ-sufficient reason:**
$$\Pr_{z \sim D}(f(z) = f(x) \mid z_S = x_S) \geq \delta \quad (6)$$

**Global δ-sufficient reason:**
$$\mathbb{E}_{x \sim D}\left[\Pr_{z \sim D}(f(z) = f(x) \mid z_S = x_S)\right] \geq \delta \quad (6')$$

where:
- $f$ is the model/function being explained
- $x$ is a reference instance
- $S$ is a subset of feature indices
- $z_S$ denotes features in $S$ taking values from $x_S$
- $D$ is the data distribution
- $\delta \in [0, 1]$ is the sufficiency threshold

**Related contrastive form** (for comparison):
$$\mathbb{E}_{x \sim D}\left[\Pr_{z \sim D}(f(z) \neq f(x) \mid z_{\bar{S}} = x_{\bar{S}})\right] \geq \delta \quad (8)$$

This flips the logic: features in $\bar{S}$ (the complement) are fixed, and we measure the probability of prediction *change*.

## Physical Intuition / Derivation

### Building Understanding

Consider a credit scoring model $f$ that predicts loan approval. A δ-sufficient reason answers: *"Which features, if known, make the decision robust to uncertainty in other features?"*

**Local perspective**: Given applicant $x$ with income = $80k$, does fixing "income" and "credit_score" make the decision stable? We sample alternative values for age, employment_history, etc., and measure how often the approval decision remains the same. If this frequency is $\geq \delta = 0.85$, then $S = \{\text{income, credit\_score}\}$ is a local δ-sufficient reason for $x$.

**Global perspective**: The above is noisy—one applicant might have stable decisions while another doesn't. So we average: take the local sufficiency probability for every applicant in the training distribution, then compute the mean. If the mean is $\geq \delta$, the feature subset is globally sufficient.

### Why This Matters

1. **Robustness**: δ-sufficient reasons guarantee that the explanation holds under distributional variation, not just for a single point.

2. **Minimality trade-off**: Smaller feature subsets are preferred (simpler explanations), but they may only achieve lower δ. The framework quantifies this trade-off via **subset-minimal** and **cardinally-minimal** explanations (Definition 1 in source material).

3. **Connection to monotonicity**: Global δ-sufficient reasons induce monotone non-decreasing value functions $v^g_{\text{suff}}(S)$, which ensures greedy algorithms (like Algorithm 1) converge to subset-minimal explanations (Proposition 5).

## Applications in Engineering

### Machine Learning Explainability
- **Model debugging**: Identify minimal feature sets that drive predictions, helping engineers detect spurious correlations or data leakage.
- **Audit compliance**: Provide probabilistic certificates that certain features (e.g., race, gender) are *not* δ-sufficient for high-stakes decisions.

### Safety-Critical Systems
- **Autonomous vehicles**: Determine which sensor inputs (lidar, camera, radar) are δ-sufficient for lane-keeping decisions.
- **Medical diagnosis**: Verify that explanations for treatment recommendations are robust across patient populations, not artifacts of specific subgroups.

### Feature Selection & Compression
- **Data acquisition**: In high-cost sensing environments (industrial IoT, remote sensing), select minimal feature subsets achieving δ-sufficiency, reducing instrumentation costs.
- **Model compression**: Identify redundant features that can be removed without losing explanatory power beyond threshold δ.

### Fairness & Bias Mitigation
- **Causal inference**: Detect if protected attributes remain δ-sufficient for decisions after debiasing interventions.
- **Disparate impact analysis**: Show that outcomes are robust to demographic features with high δ across all population groups.

## Common Mistakes / Pitfalls

1. **Confusing local and global**: A feature subset may be locally sufficient for some instances but fail globally. Conversely, global sufficiency does not guarantee local sufficiency for every individual—use the appropriate notion for your problem.

2. **Ignoring distributional dependence**: δ-sufficiency is relative to distribution $D$. If training and deployment distributions differ, guarantees evaporate. Always validate on the target distribution.

3. **Over-interpreting threshold δ**: Achieving δ=0.6 does not mean the explanation is "bad"—it depends on the cost of misclassification. Lower δ with smaller feature sets may be preferable to high δ with large sets. Define δ based on acceptable decision uncertainty, not empirical performance.

4. **Assuming sufficiency implies causation**: $S$ being δ-sufficient means fixing $S$ stabilizes predictions, but does *not* prove $S$ causes changes in $f(x)$. This is a statistical association under a specific conditioning scheme, not causation. Use causal frameworks if causal claims are required.

5. **Greedy algorithm convergence**: Local suff