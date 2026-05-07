# PAC Learning

## Definition

**Probably Approximately Correct (PAC) learning** is a formal computational model for supervised learning that provides probabilistic guarantees on the quality of learned hypotheses.

An algorithm $\mathcal{A}$ is said to PAC-learn a hypothesis class $\mathcal{H}$ over domain $\mathcal{X}$ with label space $\{0,1\}$ if:

For all distributions $\mathcal{D}$ over $\mathcal{X} \times \{0,1\}$, all error parameters $\epsilon > 0$, and all confidence parameters $\delta \in (0,1)$, there exists a sample size $m(\epsilon, \delta, |\mathcal{H}|)$ such that:

$$\Pr_{S \sim \mathcal{D}^m}\left[\text{err}_\mathcal{D}(h_S) \leq \epsilon\right] \geq 1 - \delta$$

where $h_S$ is the hypothesis output by $\mathcal{A}$ on sample $S$ of size $m$, and $\text{err}_\mathcal{D}(h) = \Pr_{(x,y) \sim \mathcal{D}}[h(x) \neq y]$ is the true error.

The key requirement: the algorithm must be **probably** (with confidence $1-\delta$) **approximately** (within error $\epsilon$) **correct** (outputs a valid hypothesis).

## Key Equations

**Sample Complexity Bound:**
For a finite hypothesis class $\mathcal{H}$, the sample complexity is bounded by:

$$m(\epsilon, \delta) = O\left(\frac{1}{\epsilon}\left(\log|\mathcal{H}| + \log\frac{1}{\delta}\right)\right)$$

**Failure Probability Boosting:**
When composing PAC algorithms or amplifying success probability through independent trials, the multiplicative overhead in differential privacy is:

$$O\left(\log\frac{1}{\beta}\right) \text{ (multiplicative factor)}$$

while replicable composition achieves:

$$O\left(\frac{\log(1/\beta)}{\alpha}\right) \text{ (additive increase)}$$

where $\beta$ is the target failure probability and $\alpha$ is the replicability parameter.

**Generalization Error vs. Empirical Error:**
For a hypothesis $h \in \mathcal{H}$:

$$\text{err}_\mathcal{D}(h) \leq \text{err}_S(h) + O\left(\sqrt{\frac{\log|\mathcal{H}| + \log(1/\delta)}{m}}\right)$$

with probability at least $1-\delta$.

## Physical Intuition / Derivation

### Why PAC Learning Matters

PAC learning answers a fundamental question: **given finite data, how do we know our learned model generalizes to unseen data?** The framework replaces vague intuition ("the model looks good") with rigorous probabilistic guarantees.

### Building the Intuition

1. **Approximate** ($\epsilon$): We allow error up to $\epsilon$—we don't need a perfect hypothesis, just a reasonably good one.

2. **Probably** ($\delta$): In rare cases (probability $\delta$), our algorithm might fail. This is unavoidable with finite data. We control this failure rate explicitly.

3. **Correct**: The guarantee holds for *any* data distribution $\mathcal{D}$—the algorithm is distribution-free.

### Why Sample Complexity Grows as Stated

**Union bound argument:** Consider a finite hypothesis class $|\mathcal{H}| = N$.
- For a single hypothesis $h$, by Chernoff bounds, the probability that empirical error differs from true error by more than $\epsilon$ decreases exponentially in $m$.
- But we must succeed for *all* $N$ hypotheses simultaneously, requiring a union bound factor: $\Pr[\text{any of } N \text{ hypotheses fails}] \leq N \cdot 2^{-O(m\epsilon^2)}$
- Setting this $\leq \delta$ and solving for $m$ yields $m = O(\epsilon^{-1}(\log N + \log \delta^{-1}))$.

## Applications in Engineering

### Machine Learning & AI
- **Model selection**: Determines how much data is needed to learn a classifier with guaranteed error bounds, regardless of input distribution
- **Theoretical foundation**: Underpins modern supervised learning; justifies empirical risk minimization

### Statistical Query Learning
- PAC learning is tightly related to the statistical query (SQ) model, where algorithms only access empirical marginals
- Enables analysis of algorithms that are robust to data perturbations (relevant to privacy)

### Differential Privacy & Replicability
- **Privacy connection**: PAC-learnable classes under differential privacy have sample complexities that grow by only $\log(1/\delta)$ factors compared to basic PAC learning
- **Replicability**: Modern work shows that algorithms can be made *replicable* (stable outputs under resampling) with only additive overhead $O(\log(1/\beta)/\alpha)$ versus multiplicative $O(\log(1/\beta))$ in differential privacy

### Bandit Algorithms & Online Learning
- **Best-arm identification**: Identifies the best action with confidence $1-\delta$ while controlling sample complexity
- Uses PAC guarantees in adaptive settings with exploration-exploitation tradeoff

### Clustering & Unsupervised Learning
- PAC guarantees can be extended to clustering: outputs a clustering that is approximately correct with high probability

## Common Mistakes / Pitfalls

1. **Confusing err_D with err_S**: The *empirical* error (on training data) can be zero while the true error is large. PAC bounds always require sample complexity to relate empirical to true error.

2. **Ignoring the distribution-free nature**: PAC learning guarantees hold for *all* distributions, which is both powerful and restrictive—the bounds cannot depend on specific properties of $\mathcal{D}$.

3. **Sample complexity vs. failure probability**: The relationship is *logarithmic* in $1/\