# Calibration Distance

## Definition

**Calibration distance** is a formal measure of miscalibration for probabilistic predictors, defined as the minimum $\ell^1$ distance (weighted by the marginal distribution) between a given predictor and any perfectly calibrated predictor.

For a predictor $\hat{p}: \mathcal{X} \to [0,1]$ and data distribution $\mathcal{D}$, the calibration distance is:

$$d_{\text{cal}}(\hat{p}, \mathcal{D}) = \min_{\tilde{p} \text{ calibrated}} \mathbb{E}_{x \sim \mathcal{D}_{\mathcal{X}}}[|\hat{p}(x) - \tilde{p}(x)|]$$

where $\mathcal{D}_{\mathcal{X}}$ is the marginal distribution over features $\mathcal{X}$, and $\tilde{p}$ is calibrated if for all $\alpha \in [0,1]$:

$$\mathbb{P}(Y=1 \mid \hat{p}(X)=\alpha) = \alpha$$

A predictor is **perfectly calibrated** when $d_{\text{cal}}(\hat{p}, \mathcal{D}) = 0$.

## Key Equations

**Calibration condition** (perfect calibration):
$$\forall \alpha \in [0,1]: \quad \mathbb{P}(Y=1 \mid \hat{p}(X)=\alpha) = \alpha$$

**Empirical calibration distance** (from $n$ samples):
$$\hat{d}_{\text{cal}}^{(n)} = \text{min distance to calibrated predictor using samples}$$

**Sample complexity bound** (from source):
$$\Theta\left(\frac{1}{\varepsilon^3}\right) \text{ samples sufficient and necessary for } |\hat{d}_{\text{cal}}^{(n)} - d_{\text{cal}}| \leq \varepsilon$$

**Computational complexity:**
- **Tractable case** (uniform marginal + noiseless labels): polynomial time
- **General case**: NP-hard; approximation possible via polynomial-time approximation scheme (PTAS)

## Physical Intuition / Derivation

### Motivation: Why Calibration Matters

Consider a weather forecaster predicting 90% rain on 100 days, with rain occurring on only 50 days. The predictor is **miscalibrated**: when it says "90% chance," the actual frequency is 50%, not 90%. This creates a trust problem—a decision-maker using this forecast for planning (e.g., scheduling events) will make systematically poor choices.

Perfect calibration ensures that predictive probabilities match empirical frequencies—a necessary condition for trustworthy probabilistic forecasting and reliable downstream decision-making.

### Why Distance to Calibration?

Rather than asking "how miscalibrated is this predictor?", we ask **"how far must we move the predictor to make it calibrated?"** This reformulation:

1. **Provides a universal metric**: independent of which specific calibration measure (ECE, MCE, etc.) one prefers
2. **Respects the geometry of prediction space**: the $\ell^1$ distance is natural for probability predictions
3. **Weights by the data distribution**: only "important" regions (high-probability feature values) count

### Construction: How to Find the Closest Calibrated Predictor

The calibration distance is found by solving an optimization problem:
- Start with predictor $\hat{p}$
- Search over all calibrated predictors $\tilde{p}$
- Find the one minimizing $\mathbb{E}[|\hat{p}(X) - \tilde{p}(X)|]$

For **noiseless labels** (deterministic ground truth given $X$) and **uniform marginal**, this can be solved efficiently by:
- Grouping predictions into quantile buckets
- Isotonically recalibrating within each bucket
- Achieving exact computation in polynomial time (improving prior $O(1/\sqrt{|\mathcal{X}|})$ approximation)

For **general case** (noisy labels, non-uniform marginals), the problem becomes NP-hard; solutions use sparsification techniques to reduce the search space.

## Applications in Engineering

### 1. **Trustworthy Machine Learning**
- **Medical AI**: Calibrated confidence scores are critical for clinical decision support. A model claiming 95% disease presence should be correct ~95% of the time.
- **Autonomous vehicles**: Uncertainty quantification must be calibrated so that collision avoidance logic can trust confidence thresholds.

### 2. **Probabilistic Forecasting**
- **Weather prediction**: Forecasters are evaluated partly on calibration—forecast probabilities should match observed frequencies.
- **Financial risk models**: Calibrated tail-risk probabilities are essential for reserve requirements and hedging decisions.

### 3. **Fairness and Accountability**
- **Loan approval systems**: If a lender's model predicts 30% default risk for protected groups with higher frequency than 30%, this miscalibration may constitute unfair discrimination.
- **Recidivism prediction**: Calibration ensures predicted re-offense rates match true rates for different demographics.

### 4. **Active Learning / Selective Prediction**
- **Bandit algorithms**: Calibrated uncertainty enables principled exploration-exploitation tradeoffs.
- **Reject option**: A classifier can reliably use the rule "reject high-uncertainty predictions" only if uncertainties are calibrated.

### 5. **Ensemble Methods**
- Calibration distance guides the combination of multiple models: predictors with better calibration distance should be weighted higher.

## Common Mistakes / Pitfalls

### 1. **Confusing Calibration with Accuracy**
**Mistake**: A model with 95% accuracy must be well-calibrated.
**Reality**: A model that predicts 0.5 for all inputs can be 50% accurate but terrible on calibration distance. Calibration and accuracy are orthogonal properties.

### 2. **Ignoring Distribution Weights**
**Mistake**: Computing calibration distance using uniform weighting over prediction values, ignoring $\mathcal{D}_{\mathcal