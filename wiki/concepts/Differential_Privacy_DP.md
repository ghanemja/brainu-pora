# Differential Privacy (DP)

## Definition

**Differential Privacy** is a mathematical framework for quantifying and protecting the privacy of individuals in datasets by ensuring that the presence or absence of any single record has negligible effect on the output of an analysis.

Formally, a randomized algorithm $\mathcal{A}$ satisfies $(\varepsilon, \delta)$-differential privacy if for all pairs of neighboring datasets $D$ and $D'$ (differing in one record) and for all measurable sets $S$ in the output space:

$$\Pr[\mathcal{A}(D) \in S] \leq e^\varepsilon \cdot \Pr[\mathcal{A}(D') \in S] + \delta$$

**Parameters:**
- $\varepsilon$ (epsilon): **privacy budget** — controls the tightness of the constraint. Smaller $\varepsilon$ means stronger privacy. Typically $\varepsilon \in (0, 1)$ for meaningful privacy.
- $\delta$ (delta): **failure probability** — the probability the guarantee may not hold. Typically $\delta \ll 1/n$ where $n$ is dataset size.

### Local Differential Privacy (LDP)

In **local differential privacy**, each node/party independently sanitizes its own data before transmission, without trusting a central server. The definition extends to graphs: an algorithm is **locally node-differentially private (LNDP⋆)** if outputs remain indistinguishable when any single node's neighborhood in a graph changes.

## Key Equations

### Basic DP Guarantee
$$\Pr[\mathcal{A}(D) \in S] \leq e^\varepsilon \Pr[\mathcal{A}(D') \in S] + \delta$$

### Randomized Rounding (Blurry Degree Distribution)
$$R_s(x) = s \left\lfloor \frac{x}{s} \right\rfloor + \text{Bern}\left(\left\{\frac{x}{s}\right\}\right)$$

where $\{x/s\} = x/s - \lfloor x/s \rfloor$ is the fractional part. This rounds value $x$ to one of two nearest multiples of $s$, with probability proportional to distance.

### Composition (Sequential Queries)
If queries use budgets $\varepsilon_1, \varepsilon_2, \ldots, \varepsilon_k$:
$$\varepsilon_{\text{total}} = \sum_{i=1}^k \varepsilon_i \quad \text{(basic composition)}$$

## Physical Intuition / Derivation

### Why DP Matters

Imagine you're releasing statistics about a hospital dataset. An adversary observing the output could potentially infer whether a specific person was in the dataset by comparing two nearly-identical datasets. Differential privacy prevents this by:

1. **Adding noise calibrated to sensitivity**: Operations that change greatly when one record changes (high sensitivity) need more noise.

2. **Multiplicative indistinguishability**: The factor $e^\varepsilon$ bounds how much an adversary can learn. At $\varepsilon = 0$, outputs are identical regardless of whether any person's record exists.

3. **Composing gracefully under multiple queries**: You have a finite "privacy budget" that depletes with each query, preventing unlimited inference.

### Blurry Degree Distributions: Intuition

Direct degree statistics have **high sensitivity** in local DP: a single node's degree can shift by up to $n-1$. The blurry rounding $R_s(x)$ reduces this by:

- **Quantizing** degrees to multiples of $s$: a parameter chosen by the analyst
- **Spreading** contribution probabilistically across nearby quantization levels
- **Lowering effective sensitivity** from $\Theta(n)$ to $\Theta(s)$

This trades a small loss in granularity for dramatically better privacy-utility tradeoff when estimating aggregate statistics like degree distributions.

## Applications in Engineering

### 1. **Data Analytics and Reporting**
- **Census bureaus** use DP to release population statistics without risking individual re-identification
- **COVID-19 dashboards** that report aggregate case counts while protecting patient privacy
- **Salary surveys** that estimate average compensation while hiding individual salaries

### 2. **Machine Learning and Training**
- **Differentially private SGD**: train neural networks on sensitive data (healthcare, finance) with formal privacy guarantees
- **Federated learning**: devices train models locally, aggregate updates with DP noise added

### 3. **Graph and Network Analytics**
- **Social network analysis**: estimate clustering coefficients, degree distributions without revealing individual connections
- **Infrastructure networks**: analyze power grid vulnerabilities or traffic patterns while protecting sensitive facility locations
- **Epidemiology**: track disease spread on contact networks without exposing patient identities

### 4. **Database Systems**
- **SQL-like queries on sensitive databases** with DP compliance (e.g., Apple's differential privacy in iOS)
- **Location services** that aggregate user movements without tracking individuals

### 5. **Privacy-Preserving Auditing**
- **Fairness testing** in ML systems while protecting training data
- **Model evaluation** on sensitive benchmarks

## Common Mistakes / Pitfalls

### 1. **Confusing DP with Obscurity**
**Wrong**: "We encrypted/anonymized the data, so it's private."  
**Right**: Encryption only prevents one attack vector. De-anonymization and linkage attacks still possible. DP provides formal, composable guarantees against *any* adversary.

### 2. **Ignoring the Privacy Budget**
**Wrong**: Running 10,000 analyses, each with $\varepsilon = 0.1$, yields total $\varepsilon = 1000$.  
**Right**: Budget compounds through composition. Plan query sequences carefully and allocate sparingly.

### 3. **Misunderstanding $(\varepsilon, \delta)$ Parameters**
**Wrong**: "$\varepsilon = 0.1$ means I'm keeping 90% of my data private."  
**Right**: $\varepsilon$ is a multiplicative indistinguishability bound, not a percentage. $\delta$ is a failure probability, typically needs $\delta \ll 1/n$.

### 4