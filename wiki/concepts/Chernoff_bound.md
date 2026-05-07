# Chernoff Bound

## Definition

The **Chernoff bound** is a concentration inequality that provides exponentially decreasing tail bounds on the probability that a sum of independent random variables deviates significantly from its expectation. It is one of the strongest and most widely used tools in probabilistic analysis of algorithms and systems.

Formally, for a sum $W = \sum_{i=1}^n X_i$ of independent random variables with $\mathbb{E}[W] = \mu$, the Chernoff bound provides:

- **Upper tail bound**: For any $t > 0$,
$$\Pr[W \geq \mu + t] \leq e^{-\Omega(t^2/\mu)}$$

- **Lower tail bound**: For any $0 < t < \mu$,
$$\Pr[W \leq \mu - t] \leq e^{-\Omega(t^2/\mu)}$$

These bounds decay **exponentially** in $t^2$, making them far tighter than Chebyshev-type bounds (which decay polynomially).

## Key Equations

### Standard Form (Lower Tail)
For $\hat{W} \leq \mu - t$ where $\hat{W}$ is the observed sum and $\mu$ is the expected value:

$$\Pr[\hat{W} \leq \mu - t] \leq \exp\left(-\frac{t^2}{2\mu}\right)$$

### Parametric Form (Union Bound Application)
When applied over $n$ independent events with failure probability $n^{-c}$ each:

$$\Pr[\text{any event fails}] \leq n \cdot n^{-c} = n^{1-c}$$

This scales as $n^{1-c}$, which remains sub-polynomial for $c > 1$.

### Weighted Sum Concentration (Theorem 2.3 reference)
For a weighted sum $W = \sum_{b} m_b X_b$ where $X_b$ are independent geometric random variables:

$$\Pr\left[\sum_b m_b X_b \geq (1+\delta) \mathbb{E}\left[\sum_b m_b X_b\right]\right] \leq \exp\left(-\Omega\left(\frac{\delta^2 \sum m_b^2}{\sum m_b}\right)\right)$$

## Physical Intuition / Derivation

### Why Exponential Decay?

The Chernoff bound's power comes from the **moment generating function (MGF) method**. Rather than bounding $\Pr[W \geq \mu + t]$ directly, we use:

$$\Pr[W \geq \mu + t] = \Pr[e^{\lambda W} \geq e^{\lambda(\mu + t)}] \leq \frac{\mathbb{E}[e^{\lambda W}]}{e^{\lambda(\mu + t)}}$$

by **Markov's inequality**. For independent random variables, $\mathbb{E}[e^{\lambda W}] = \prod_i \mathbb{E}[e^{\lambda X_i}]$, which can be bounded using properties of exponential functions. Optimizing over $\lambda$ yields the exponential decay.

### Why It Matters in Practice

Consider allocating buckets in a hash table:
- Naive bound (Chebyshev): $\Pr[|bucket\ size - \mu| > t] \leq O(1/t^2)$ — needs $t = \Theta(\sqrt{n})$ for sub-constant failure probability
- Chernoff bound: $\Pr[|bucket\ size - \mu| > t] \leq e^{-\Omega(t^2/\mu)}$ — needs only $t = O(\log n)$ for $n^{-c}$ failure probability

This is the difference between $\Theta(\sqrt{n})$ and $\Theta(\log n)$ buckets—orders of magnitude in practice.

### Union Bound Scaling

In the parallel semisort application (source material), we apply Chernoff to:
- Each of $n$ keys independently: failure probability $n^{-c}$ each → total failure $O(n^{1-c})$
- Each of $B \leq n$ buckets independently: failure probability $n^{-c}$ each → total failure $O(n^{1-c})$

The key insight: **exponential decay in the exponent allows union bounds to remain strong** when the number of events is polynomial in problem size.

## Applications in Engineering

### 1. **Algorithm Analysis & Randomized Data Structures**
- **Hash table load balancing**: Proving that with high probability, no bucket receives more than $O(\log n)$ items when $n$ items hash uniformly
- **Parallel sorting & semisorting**: Controlling the maximum work performed by any processor in parallel sorting networks (as in Algorithm 1 of the source)
- **Randomized quicksort**: Bounding the probability of poor pivot choices leading to $O(n^2)$ behavior

### 2. **Network & Distributed Systems**
- **Load balancing**: Ensuring no server receives significantly more than its fair share of requests when jobs are randomly routed
- **Packet collision analysis**: Bounding collision probability in random access networks (CSMA/CD, Ethernet)
- **Distributed consensus**: Analyzing Byzantine fault tolerance when adversaries control a random subset of nodes

### 3. **Machine Learning & Sampling**
- **Estimator variance bounds**: Proving that sample means concentrate around true means with high probability
- **Importance sampling**: Controlling variance in Monte Carlo estimation when sample weights are random
- **Reservoir sampling**: Analyzing failure probability of maintaining a uniform random sample

### 4. **Systems & Resource Allocation**
- **Memory allocation**: Guaranteeing that pre-allocated buffers are sufficient with high probability (as in Lemma 3.3)
- **Bandwidth provisioning**: Ensuring network links remain uncongested when demand is random
- **Job scheduling**: Bounding queue lengths in stochastic job arrival systems

### 5. **Cryptography & Security**
- **Collision probability bounds**: Proving cryptographic hash functions