# Contrastive Reasons

## Definition

**Contrastive reasons** are minimal subsets of input features that, when modified or perturbed, alter a model's prediction. Formally, given a machine learning model $f$ and an input instance $\mathbf{x}$, a contrastive reason is a subset $S \subseteq \{1, 2, \ldots, n\}$ of feature indices such that:

$$f(\mathbf{x}) \neq f(\mathbf{x}')$$

where $\mathbf{x}'$ is obtained by modifying the features in $S$ from their original values in $\mathbf{x}$.

In contrast to **sufficient reasons** (which explain *why* a prediction is made), contrastive reasons explain *what would need to change* to obtain a different prediction. They answer the question: "What features, if different, would have led to a different outcome?"

A **minimal contrastive reason** is one where no proper subset has this property, making it a fundamental unit of explanation for counterfactual-style reasoning.

## Key Equations

The computational characterization of contrastive reasons can be expressed through a unified **value function** framework:

$$V_{\text{contrastive}}(S) = \min_{\mathbf{x}' : x'_i = x_i \text{ for } i \notin S} \mathbb{1}[f(\mathbf{x}) \neq f(\mathbf{x}')]$$

A subset $S$ is a contrastive reason if $V_{\text{contrastive}}(S) = 1$.

The **minimal contrastive reason** is the solution to:

$$\min_{S \subseteq [n]} |S| \quad \text{subject to} \quad V_{\text{contrastive}}(S) = 1$$

In the probabilistic setting, this generalizes to:

$$V(S) = \Pr[f(\mathbf{X}) \neq f(\mathbf{X}[S \leftarrow \mathbf{x}])]$$

where $\mathbf{X}[S \leftarrow \mathbf{x}]$ denotes replacing features in $S$ with their values from $\mathbf{x}$, and $\mathbf{X}$ is drawn from some reference distribution.

## Physical Intuition / Derivation

### Intuitive Understanding

Imagine a loan approval system that denies your application. A **sufficient reason** would identify the specific features (e.g., "your debt-to-income ratio and credit score") that together *guaranteed* the denial. A **contrastive reason**, by contrast, identifies which features you would need to change to potentially flip the decision.

**Contrastive reasons directly model human counterfactual thinking**: "If I had reduced my debt load by $X, would I have been approved?" They are inherently actionable—they tell stakeholders what levers they can pull.

### Why the Distinction Matters Computationally

The paper reveals a counterintuitive distinction:

- **Local setting** (single instance): Computing contrastive reasons is NP-hard even for simple models. The reason is that there is no structure to exploit—you must search through exponentially many subsets without guarantees.

- **Global setting** (distribution over instances): The value function exhibits **monotonicity** and **submodularity/supermodularity** properties, enabling polynomial-time approximation algorithms with provable guarantees.

**Monotonicity**: If $S \subseteq T$, then changing more features is always at least as likely to alter the prediction:
$$V(S) \leq V(T)$$

**Submodularity**: The marginal gain from adding a feature decreases as you add more features:
$$V(S \cup \{i\}) - V(S) \geq V(T \cup \{i\}) - V(T) \quad \text{for } S \subseteq T$$

These properties—absent in the local case—enable the greedy algorithm to achieve a $(1 - 1/e)$-approximation for minimizing explanation size.

## Applications in Engineering

### Machine Learning Explainability
- **Model debugging**: Identify which input features, if perturbed, would flip misclassifications
- **Robustness analysis**: Find minimal adversarial perturbations as a formal measure of model brittleness
- **Counterfactual fairness**: Determine what changes would be required to alter discriminatory predictions

### Autonomous Systems
- **Decision justification**: In autonomous vehicles, explain: "To avoid collision, sensor reading $X$ must differ from current state"
- **Safety certification**: Identify which sensor modalities are critical for safe operation

### Finance & Risk Management
- **Stress testing**: Determine minimal market condition changes that would trigger risk thresholds
- **Regulatory compliance**: Explain what business parameter changes would satisfy regulatory constraints

### Fault Diagnosis
- **Root cause analysis**: Identify which measurements, if different, would indicate a different failure mode
- **Preventive maintenance**: Determine threshold changes needed to avoid equipment failure

## Common Mistakes / Pitfalls

1. **Confusing with sufficient reasons**: Students often mix up "what caused this prediction" (sufficient) with "what would change it" (contrastive). These are dual but distinct concepts.

2. **Neglecting the distribution dependence**: In the probabilistic setting, contrastive reasons depend critically on the reference distribution. Changing the distribution can change which reasons are minimal—this is a feature, not a bug.

3. **Assuming local hardness invalidates practical use**: While local computation is NP-hard, this doesn't mean all instances are hard. NP-hardness is worst-case; heuristics and approximations often work well in practice.

4. **Oversimplifying to binary features**: The framework applies equally to continuous features with appropriate distance metrics, but this complexity is often overlooked in implementations.

5. **Ignoring actionability constraints**: Not all features can be modified in practice (e.g., age, protected characteristics). The framework must be constrained to actionable features for real applications.

6. **Missing the local/global distinction**: Assuming that because global computation is tractable, local computation (which practitioners care most about) is also tractable. These are fundamentally different problems.

## See Also

- [[Sufficient Reasons]] — Dual explanation type; identifies features that guarantee a prediction rather than