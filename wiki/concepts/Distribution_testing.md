# Distribution Testing

## Definition

**Distribution testing** is a subfield of property testing and statistical learning that studies the problem of determining whether an unknown probability distribution over a domain satisfies a specific property or belongs to a particular class, given access to independent samples from that distribution.

Formally, given:
- An unknown distribution $\mathcal{D}$ over domain $X$
- A property $\mathcal{P}$ (a set of distributions)
- Sample access to $\mathcal{D}$

A distribution testing algorithm must:
- **Accept** with high probability if $\mathcal{D} \in \mathcal{P}$
- **Reject** with high probability if $\mathcal{D}$ is $\epsilon$-far from $\mathcal{P}$ (in total variation distance or another metric)

The primary goal is to minimize the **sample complexity**—the number of samples required to solve the testing problem.

### Formal Distance Metric

Two distributions $\mathcal{D}_1$ and $\mathcal{D}_2$ are $\epsilon$-far in total variation distance if:
$$\mathrm{TV}(\mathcal{D}_1, \mathcal{D}_2) = \frac{1}{2}\sum_{x \in X} |\mathcal{D}_1(x) - \mathcal{D}_2(x)| > \epsilon$$

## Key Equations

### Sample Complexity Bounds

For many classical distribution testing problems, sample complexity follows the pattern:
$$n = \Theta\left(\frac{1}{\epsilon^2}\right) \text{ or } n = \Theta\left(\frac{\sqrt{|X|}}{\epsilon^2}\right)$$

depending on whether the domain is continuous or discrete and bounded.

### Typical Test Structure

A generic distribution test using the **chi-squared statistic** for goodness-of-fit:
$$\chi^2 = \sum_{i=1}^{k} \frac{(N_i - np_i)^2}{np_i}$$

where:
- $N_i$ = observed count in bin $i$
- $n$ = total samples
- $p_i$ = probability under null hypothesis
- Under the null, $\chi^2 \sim \chi^2_k$ approximately

## Physical Intuition / Derivation

### Why Distribution Testing Matters

In practice, we often have only sample access to data and need to verify fundamental assumptions:

1. **Data Validation**: Is our collected data consistent with expected distribution?
2. **Model Checking**: Does the observed sample support Gaussian vs. exponential assumptions?
3. **Anomaly Detection**: Is new data drawn from the same distribution as historical data?

### Sample Complexity Intuition

**Lower bounds** emerge from information-theoretic arguments:
- To distinguish between two distributions differing at single point with probability $\delta$, we need roughly $\Omega(1/\delta^2)$ samples (birthday paradox analogy)
- For domain size $|X|$, we need $\Omega(\sqrt{|X|})$ samples to distinguish arbitrary distributions at distance $\epsilon$ (since there are exponentially many possible distributions)

**Upper bounds** rely on concentration inequalities:
- **Chernoff bounds** control tail probability of sample counts
- **Union bounds** over discretized hypothesis space

### Key Insight: Replicability Connection

Recent advances (referenced in sources [DGK+25]) connect distribution testing to **replicability**—the requirement that an algorithm produces consistent outputs across independent runs with high probability. This is achieved through:
- Stability constraints on the testing procedure
- Privacy-preserving mechanisms that ensure robustness

## Applications in Engineering

### 1. **Quality Control & Manufacturing**
- Testing if production batch meets specification distributions
- Detecting equipment drift by comparing production distributions over time
- Sample complexity determines inspection batch size while controlling false positive/negative rates

### 2. **Network & System Monitoring**
- Detecting anomalies in packet inter-arrival time distributions
- Validating that system latency follows assumed exponential distribution
- Early warning systems for performance degradation

### 3. **Machine Learning Validation**
- **Covariate shift detection**: Testing if test data distribution matches training distribution [connects to [[Distributional Shift]]]
- **Model validation**: Ensuring generated samples from generative models match target distribution
- **Fairness auditing**: Testing if classifier decisions follow fair distributions across groups

### 4. **Signal Processing**
- Goodness-of-fit testing for noise assumptions (Gaussian white noise hypothesis)
- Detection of signal components in stochastic processes
- Spectrum analysis validation

### 5. **Drug Development & Clinical Trials**
- Safety testing: Does adverse event rate follow expected Poisson/binomial distribution?
- Adaptive trial design: Sequentially test if treatment effect magnitude matches distribution assumptions
- Sample size planning for required statistical power

### 6. **Replicable Machine Learning** [CMY23], [DGK+25]
- Building learning algorithms that remain stable under data perturbation
- Distribution-free testing procedures that work without parametric assumptions
- Combining differential privacy with distribution testing for robust learning systems

## Common Mistakes / Pitfalls

### 1. **Confusing Hypothesis Testing with Distribution Testing**
- **Mistake**: Assuming standard $t$-tests or $z$-tests directly apply
- **Reality**: Distribution testing is more general—it doesn't assume parametric families. Use nonparametric methods like Kolmogorov-Smirnov test for continuous distributions
- **Fix**: Use [[Nonparametric Statistics]] approaches; rely on empirical CDF convergence

### 2. **Ignoring Sample Complexity Scaling**
- **Mistake**: Using fixed sample sizes across different domain sizes
- **Reality**: Sample complexity often scales as $\Theta(\sqrt{|X|}/\epsilon^2)$—exponential domains require exponential samples to achieve constant $\epsilon$
- **Fix**: Understand hardness results; sometimes binning/discretization is necessary

### 3. **Multiple Testing Fallacy**
- **Mistake**: Running many distribution tests independently without correction
- **Reality**: False discovery rate accumulates across tests
- **Fix**: Apply Bonferroni or Benjamini-Hochberg corrections; use unified testing framework

### 4. **Neglecting Replicability**
- **Mistake