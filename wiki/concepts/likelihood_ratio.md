# Likelihood Ratio

## Definition

The **likelihood ratio** is a comparative measure of the probability of observing data under two competing hypotheses or distributions. Formally, for a distribution $\nu$ relative to a reference distribution $U$ (often uniform), the likelihood ratio at a point $x$ is:

$$\frac{d\nu}{dU}(x) = \frac{\Pr[X = x \mid \nu]}{\Pr[X = x \mid U]}$$

This ratio quantifies how much more (or less) probable the observation $x$ is under $\nu$ compared to the reference distribution $U$. When $\nu$ is absolutely continuous with respect to $U$, this is the **Radon-Nikodym derivative**—the density of $\nu$ with respect to $U$.

In the context of probabilistic sampling procedures, the likelihood ratio measures how well a sampler approximates the target distribution. A bounded likelihood ratio indicates that no outcome is disproportionately favored or suppressed relative to the ideal distribution.

## Key Equations

**Basic form (discrete case):**
$$\frac{d\nu}{dU_m}(x) = \frac{\Pr_{y \sim \mu}[\text{Samp}(x) = y] \cdot \Pr_{r \sim D}[\text{InvSamp}(\text{Samp}(x), r) = x]}{\Pr_{z \sim U}[\text{Samp}(z) = \text{Samp}(x)] \cdot \Pr_{z \sim U}[z = x \mid \text{Samp}(x) = \text{Samp}(z)]}$$

**Bounded likelihood ratio condition:**
$$\frac{d\nu}{dU_m}(x) \leq C \quad \text{for all } x \in \{\pm 1\}^m$$

where $C$ is a constant (often denoted $C_{\text{Samp}}$ or $C_{\text{inv}}$ for different components).

**Decomposition into independent components:**
$$\frac{d\nu}{dU}(x) = \frac{\text{Ratio}_1}{\text{Ratio}_2} \leq C_1 \cdot C_2$$

where component ratios are bounded independently.

## Physical Intuition / Derivation

### Why Likelihood Ratios Matter

Imagine building a procedure to sample from a complex target distribution $\nu$ by:
1. Drawing a seed uniformly at random
2. Processing it through a sampler to produce output

The likelihood ratio answers: *"For any outcome $x$, how much more likely is it than in a truly uniform distribution?"*

A ratio close to 1 everywhere means your sampler faithfully reproduces the target. A ratio that explodes at some points means your procedure is "biased"—certain outcomes are over-represented relative to the true distribution.

### Derivation Strategy (from the source)

The source material uses a **decomposition strategy**:

1. **Forward mapping**: A sampler $\text{Samp}$ maps a uniform seed to a sample from $\mu$
2. **Inverse mapping**: An inverter $\text{InvSamp}$ recovers the original seed from a sample

For any output $x$:
- The probability of obtaining $x$ depends on whether seeds map to it via $\text{Samp}$
- The likelihood ratio factors into:
  - **Sampling distortion**: How much does $\text{Samp}$ skew the uniform distribution?
  - **Inversion distortion**: How much does inverting back introduce bias?

Each factor is bounded ($C_{\text{Samp}}$, $C_{\text{inv}}$), so their product is also bounded.

### Low-Degree Polynomial Insight

A key technical requirement: the inverter must have **low-degree polynomial representation** in the sample. This ensures:
- The composition of a degree-$k$ function (the target computation) with a degree-$t$ function (the inverter) yields a degree-$kt$ function
- Degree bounds provide leverage for proving distributional properties via polynomial methods

## Applications in Engineering

### 1. **Cryptography & Pseudorandom Generation**
- Likelihood ratios quantify how close a pseudorandom generator output is to uniform
- Bounded ratios guarantee security properties against statistical tests
- Used in analyzing seed extractors and randomness amplification

### 2. **Sampling-Based Inference (Statistics/ML)**
- **Importance sampling**: likelihood ratios weight samples to correct for biased samplers
- **Acceptance-rejection sampling**: ratios determine acceptance probabilities
- **Markov Chain Monte Carlo**: ensures detailed balance via likelihood ratio tests

### 3. **Communication Systems**
- **Likelihood ratio decoding**: Optimal decoders for error-correcting codes compute log-likelihood ratios of received symbols
- Ratio guides decision thresholds in noisy channels

### 4. **Distributed Systems & Sampling Complexity**
- Analyze local iterative samplers: likelihood ratios bound how much locality constraints distort the output distribution
- Applications to combinatorial optimization (e.g., random hypergraph colorings)

### 5. **Hypothesis Testing**
- **Neyman-Pearson Lemma**: likelihood ratio is the optimal test statistic
- Engineering decision systems often use log-likelihood ratios as decision metrics

## Common Mistakes / Pitfalls

1. **Confusing with posterior odds**: The likelihood ratio is $P(x|\nu)/P(x|U)$, not a Bayesian posterior. Don't mix up with $P(\nu|x)/P(U|x)$.

2. **Assuming unbounded ratios are "fine"**: An unbounded or very large ratio indicates poor approximation quality. Even constant factors matter in applications requiring high confidence.

3. **Ignoring support conditions**: If $\nu$ has restricted support, the likelihood ratio may be zero or undefined outside that support. The source material emphasizes this subtlety.

4. **Multiplicative vs. additive errors**: Likelihood ratios multiply. A ratio of 1.1 on each of $n$ independent steps yields $(1.1)^n$, which can be large. Use log-likelihood (additive) for analysis.

5. **Forgetting the reference measure**: The likelihood ratio *always* depends