# Earth Mover's Distance (EMD)

## Definition

The **Earth Mover's Distance** (EMD), also called the **Wasserstein distance** or **optimal transport cost**, is a metric that quantifies the minimum cost required to transform one probability distribution into another by moving "mass" optimally.

Formally, given two probability distributions $p$ and $\hat{p}$ over a measurable space with a ground metric $d$, the EMD is:

$$\text{EMD}(\hat{p}, p) = \inf_{\gamma \in \Gamma(\hat{p}, p)} \mathbb{E}_{(x,y) \sim \gamma}[d(x, y)]$$

where $\Gamma(\hat{p}, p)$ is the set of all joint distributions (transport plans) with marginals $\hat{p}$ and $p$. The infimum is taken over all possible couplings of the two distributions, finding the plan that minimizes expected transportation cost.

### Discrete Case (Canonical Form)

When both distributions are discrete with support $\{a_1, \ldots, a_m\}$ and $\{b_1, \ldots, b_n\}$:

$$\text{EMD}(\hat{p}, p) = \min \sum_{i,j} \gamma_{ij} \cdot d(a_i, b_j)$$

subject to:
- $\sum_j \gamma_{ij} = \hat{p}(a_i)$ (marginal constraints on first distribution)
- $\sum_i \gamma_{ij} = p(b_j)$ (marginal constraints on second distribution)
- $\gamma_{ij} \geq 0$ (non-negativity)

This is a linear program solvable in polynomial time using optimal transport algorithms.

---

## Key Equations

### Relationship to Loss Bounds

In prediction problems with model misspecification, EMD characterizes robustness. A key result from the source material:

$$\text{Loss} = O\left(\min_{\text{policy}} \sqrt{b} \cdot \max(\text{EMD}(\hat{p}, p), 1)\right)$$

where $b$ is a problem-dependent parameter (e.g., buying horizon). This shows loss scales with the square root of the discrepancy between predicted $\hat{p}$ and true distribution $p$.

### Robustness Guarantee

With appropriate algorithmic truncation:

$$\text{Loss}_{\text{robust}} = O(b \log b)$$

independent of how poorly $\hat{p}$ approximates $p$, ensuring algorithms remain bounded even under severe distributional misspecification.

### Properties

- **Metric axioms**: EMD satisfies symmetry, non-negativity, identity of indiscernibles, and triangle inequality
- **Monge-Kantorovich duality**: 
$$\text{EMD}(\hat{p}, p) = \sup_{f: \|f\|_L \leq 1} \left|\mathbb{E}_{x \sim p}[f(x)] - \mathbb{E}_{y \sim \hat{p}}[f(y)]\right|$$
where $\|\cdot\|_L$ denotes Lipschitz constant.

---

## Physical Intuition / Derivation

### The "Earth Moving" Metaphor

Imagine two piles of dirt on a landscape: one pile has the shape of distribution $\hat{p}$, the other has the shape of distribution $p$. EMD is the minimum cost of earth-moving operations (transportation) needed to reshape the first pile to match the second exactly.

- **Transport plan** $\gamma(x,y)$: specifies how much mass moves from location $x$ to location $y$
- **Ground metric** $d(x,y)$: cost per unit mass for that movement
- The optimal plan minimizes total cost while respecting mass conservation

### Why This Matters for Algorithms

In the source context, $\hat{p}$ is a **predicted distribution** of future events (e.g., price evolution), while $p$ is the **true distribution**:

1. When $\text{EMD}(\hat{p}, p)$ is **small**: predictions are close to reality → algorithms designed for $\hat{p}$ remain near-optimal
2. When $\text{EMD}(\hat{p}, p)$ is **large**: predictions are far from reality → naive algorithms fail catastrophically, requiring robustness modifications (e.g., buying delay of $\sqrt{b}$ days)

The algorithm truncates decisions when probability mass concentrates in the tail, preventing commitment to low-probability events under the predicted distribution.

---

## Applications in Engineering

### 1. **Machine Learning & Domain Adaptation**
- Measuring distribution shift between training and test data
- Quantifying robustness of classifiers to dataset shift
- Optimal transport for generative model training (e.g., Wasserstein GANs)

### 2. **Supply Chain & Operations**
- Predicting demand distributions and hedging against forecast error
- Optimal inventory positioning when supplier locations change
- Cost of reconfiguring logistics networks

### 3. **Control Systems & Robotics**
- Trajectory planning under uncertainty in state distributions
- Measuring compatibility of control policies across different environments
- Distribution-robust control synthesis

### 4. **Finance & Portfolio Optimization**
- Model risk quantification: distance between assumed and true return distributions
- Robust portfolio construction insensitive to distributional misspecification
- Value-at-Risk under model uncertainty

### 5. **Online Algorithms & Prediction Markets**
- **Ski rental problem variant** (source): Buying decision (equipment rental vs. purchase) when future days-of-use follow predicted distribution $\hat{p}$
- Hedging strategies when market models diverge from reality
- Algorithm design that is both consistent (good when $\text{EMD}$ is small) and robust (bounded when $\text{EMD}$ is large)

---

## Common Mistakes / Pitfalls

### 1. **Confusing EMD with $L^2$ or $L^\infty$ distance**
EMD respects geometry: $\text{EMD}(\delta_0, \delta_\epsilon) = \epsilon$ (transportation cost), while $\|\delta_0