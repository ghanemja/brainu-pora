# Binomial distribution

## Definition

The **binomial distribution** with parameters $n \in \mathbb{N}$ and $p \in [0,1]$, denoted $\text{Bin}(n,p)$, is the probability distribution of the sum of $n$ independent and identically distributed (i.i.d.) [[Bernoulli distribution]] random variables, each with parameter $p$.

Formally, if $x_1, x_2, \ldots, x_n \stackrel{\text{iid}}{\sim} \text{Ber}(p)$, then:
$$Z = \sum_{i=1}^{n} x_i \sim \text{Bin}(n,p)$$

The random variable $Z$ represents the count of successes in $n$ independent trials, where each trial succeeds with probability $p$.

## Key Equations

**Probability mass function (PMF):**
$$P(Z = k) = \binom{n}{k} p^k (1-p)^{n-k}, \quad k \in \{0, 1, \ldots, n\}$$

**Mean (expected value):**
$$\mathbb{E}[Z] = np$$

**Variance:**
$$\text{Var}(Z) = np(1-p)$$

**Cumulative tail probability (via [[Chernoff bound]]):**

For $Z \sim \text{Bin}(n,p)$ with mean $\mu = np$:
$$\Pr[Z \geq (1+\Delta)\mu] \leq \exp\left(\frac{-\Delta^2 \mu}{2+\Delta}\right)$$

**Sample complexity bound:** To ensure that with probability at least $1-\delta$ we have $Z \leq n((1+\alpha)p + \varepsilon)$ for parameters $\alpha, \varepsilon \in [0,1]$:
$$n = O\left(\frac{\log(1/\delta)}{\varepsilon(\alpha + \varepsilon)}\right)$$

## Physical Intuition / Derivation

### Building the Distribution

The binomial distribution arises naturally from repeating a simple binary experiment:

1. **Base experiment:** A single trial with two outcomes—success (probability $p$) or failure (probability $1-p$). This is modeled by the [[Bernoulli distribution]].

2. **Repetition:** Perform this trial $n$ times independently. We count how many successes occur.

3. **Aggregation:** The total count of successes follows $\text{Bin}(n,p)$.

### Why the PMF has this form

For exactly $k$ successes in $n$ trials:
- We need $k$ successes (each contributing probability $p$) and $(n-k)$ failures (each contributing $1-p$): probability $p^k(1-p)^{n-k}$
- There are $\binom{n}{k}$ ways to arrange which $k$ trials succeed
- Total: $\binom{n}{k}p^k(1-p)^{n-k}$

### Concentration and Tail Bounds

The [[Chernoff bound]] tells us that binomial random variables concentrate tightly around their mean $np$. For large $n$, the probability of observing significant deviations decays exponentially—this is crucial for engineering reliability and sample complexity arguments in learning theory.

## Applications in Engineering

### 1. Quality Control and Manufacturing
- **Acceptance sampling:** Testing a batch of products where each item either meets specification (success, probability $p$) or fails. The count of defects follows $\text{Bin}(n, p_{\text{defect}})$. Use binomial tail bounds to set batch acceptance criteria.

### 2. Wireless Communications
- **Bit error rates:** When transmitting $n$ bits over a noisy channel, the number of bit errors follows approximately $\text{Bin}(n, p_{\text{error}})$. Chernoff bounds determine required coding overhead to achieve target error rates.

### 3. Reliability Engineering
- **System failures:** A system with $n$ independent components, each failing with probability $1-p$, has a failure count distributed as $\text{Bin}(n, 1-p)$. Predict probability that more than $k$ components fail.

### 4. Machine Learning and Statistical Learning Theory
- **PAC learning (Probably Approximately Correct):** When training on $n$ i.i.d. samples, the number of misclassified examples is binomially distributed. Sample complexity calculations (see [[Chernoff bound]] application) determine how many training examples are needed to guarantee low error with high confidence.
- **Empirical risk minimization:** Use concentration inequalities for binomial tails to prove generalization bounds.

### 5. Network Packet Loss
- **Transmission reliability:** In networks, each transmitted packet is received with probability $p$. The number of received packets from $n$ transmissions is $\text{Bin}(n,p)$.

## Common Mistakes / Pitfalls

1. **Confusing with Poisson:** Students often use Poisson approximation carelessly. The Poisson approximation $\text{Bin}(n,p) \approx \text{Poisson}(np)$ is valid only when $n$ is large and $p$ is small (so $np$ is moderate). For moderate $p$, binomial is distinctly non-Poissonian.

2. **Forgetting independence:** The binomial formula requires that the $n$ trials be truly independent. Correlated trials (e.g., sampling without replacement from a small population) follow the [[hypergeometric distribution]], not binomial.

3. **Misapplying tail bounds:** The [[Chernoff bound]] provides an *upper bound* on tail probabilities. The actual probability may be much smaller—bounds are often loose for practical parameters. Also, $\Delta > 0$ bounds the *upper* tail; separate bounds exist for lower tails.

4. **Neglecting variance:** When $np(1-p)$ is large, standard deviation $\sqrt{np(1-p)}$ is significant. Designs assuming the mean exactly occurs without accounting for variance lead to unreliability.

5. **Sample size underest