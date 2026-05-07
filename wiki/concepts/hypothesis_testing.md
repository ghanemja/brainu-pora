# Hypothesis Testing

## Definition

Hypothesis testing is a statistical method for making decisions about the validity of a claim (hypothesis) regarding a population parameter or distribution, based on sample data. Formally, it involves:

- **Null hypothesis** ($H_0$): A baseline assumption, typically representing "no effect" or "no difference"
- **Alternative hypothesis** ($H_1$): The claim we seek evidence for
- **Test statistic**: A function of the data whose distribution is known under $H_0$
- **Decision rule**: A threshold (critical region) that determines whether to reject $H_0$

The outcome is binary: either **reject** $H_0$ (with statistical confidence) or **fail to reject** $H_0$ (insufficient evidence).

## Key Equations

### Error Probabilities

$$\alpha = \Pr[\text{reject } H_0 \mid H_0 \text{ true}]$$
**Type I error**: False positive rate (significance level)

$$\beta = \Pr[\text{fail to reject } H_0 \mid H_1 \text{ true}]$$
**Type II error**: False negative rate

$$\text{Power} = 1 - \beta$$
Probability of correctly detecting a true effect

### Sample Complexity for Binary Testing

For a valid hypothesis test to distinguish between two hypotheses with error probabilities $\alpha$ and $\beta$:

$$n_{\text{samples}} \geq \frac{\log(1/\min\{\alpha, \beta\})}{\text{KL divergence between hypotheses}}$$

### Replicability-Aware Testing

From the source material, the sample complexity of a $\rho$-replicable algorithm is:

$$n_{\text{new}}(\rho, \alpha, \beta) = n_{\text{replic}}\left(\frac{\rho}{4}, \frac{\alpha}{2}, \frac{\rho}{4}\right) + n_{\text{tester}}\left(\frac{\alpha}{2}, \min\{\rho, \beta\}/4\right) + n_{\text{non-replic}}\left(\alpha, \frac{\beta}{2}\right)$$

where the algorithm runs a replicable sub-routine, validates its output with a tester, and falls back to a non-replicable algorithm if needed.

### Mismatch and Failure Probabilities

In adversarial settings with fixed random seed $r$:

$$\rho(r) = \Pr_{r,S,S'}\left[\exists i \in [k]: y_i \neq y'_i \mid r\right]$$
Probability that two runs produce different outputs

$$\beta(r) = \Pr_{r,S}\left[\exists i \in [k]: y_i \notin G_{\theta_i} \mid r\right]$$
Probability that any output is invalid

## Physical Intuition / Derivation

### The Trade-off Between Confidence and Sample Size

Hypothesis testing balances two competing goals:
- **Reducing false positives** ($\alpha$ small) requires stronger evidence against $H_0$
- **Reducing false negatives** ($\beta$ small) requires distinguishing $H_1$ from $H_0$ reliably

These demands pull in opposite directions. As you tighten one threshold, you need exponentially more samples to maintain performance on the other. This is fundamental to statistical inference.

### Why Replicability Matters in Testing

The source material addresses **replicable hypothesis testing**: when two independent runs with the same random seed must produce identical outputs. This is crucial because:

1. **Reproducibility crisis**: Many published results fail to replicate with fresh data
2. **Adversarial robustness**: An adversary can exploit slight differences between runs
3. **Algorithmic compliance**: Regulations may require decisions to be reproducible

The key insight is that enforcing replicability ($\rho$ small) *increases* sample complexity. The algorithm must validate its output using a tester before committing, adding overhead. The fixed-$r$ lower bound (Claim 4) shows that forcing agreement across runs requires $\Omega(\rho^{-1})$ additional samples in the worst case.

### Why Adversarial Samples Matter

In the source setting, an adversary presents test data $T$ but withholds the true parameter $\theta_i$. The algorithm must:
- Maintain agreement between two runs (replicability constraint)
- Correctly classify samples (validity: $A(T, S, H_{i-1}; r) \in G_\theta$)

The union bound over $k$ rounds gives exponential failure probability unless controlled carefully.

## Applications in Engineering

### 1. Quality Control & Manufacturing

**Semiconductor testing**: Hypothesis test whether a batch meets specification limits for defect rate.
- $H_0$: Defect rate $p \leq p_0$ (acceptable)
- $H_1$: Defect rate $p > p_0$ (reject batch)
- Sample complexity determines inspection costs vs. risk of shipping defective parts

### 2. Machine Learning Model Validation

**A/B testing in recommendation systems**: Test whether algorithm variant A outperforms baseline B.
- Sample size formula ensures statistical power to detect meaningful differences
- Replicability ensures consistent user experience across devices/servers
- Type I error controls false innovation claims

### 3. Signal Processing & Communications

**Spectrum sensing (cognitive radio)**: Detect whether a frequency band is occupied.
- $H_0$: Noise only
- $H_1$: Signal + noise
- Error probabilities constrain miss detection (missed spectrum access) vs. false alarm

### 4. Biomedical Device Testing

**Equivalence testing for medical devices**: Verify that a new design performs comparably to gold standard.
- Requires two-sided test with symmetric error bounds
- Regulatory requirements (FDA) mandate specific $\alpha, \beta$ levels
- Sample size calculations directly impact clinical trial cost

### 5. Software Verification

**Automated testing under randomness**: Confirm that a probabilistic algorithm (e.g., randomized sorting) meets correctness guarantees.
- Replicable testing (from source) ensures test suites are reproducible
- Fallback to non-replicable method only when necessary
- Balances confidence in correctness against test execution time

## Common Mistakes / Pitfalls