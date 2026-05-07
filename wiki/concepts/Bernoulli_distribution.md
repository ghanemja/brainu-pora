# Bernoulli distribution

## Definition

The **Bernoulli distribution** with parameter $p \in [0,1]$, denoted $\text{Ber}(p)$, is a discrete probability distribution that models a single trial with two possible outcomes:
- Takes the value **1** with probability $p$ (success)
- Takes the value **0** with probability $1-p$ (failure)

Formally, for a random variable $X \sim \text{Ber}(p)$:

$$P(X = k) = \begin{cases} p & \text{if } k = 1 \\ 1-p & \text{if } k = 0 \end{cases}$$

The parameter $p$ is called the **success probability** or **Bernoulli parameter**.

## Key Equations

**Mean (Expected Value):**
$$E[X] = p$$

**Variance:**
$$\text{Var}(X) = p(1-p)$$

**Probability Mass Function (PMF):**
$$P(X = k) = p^k(1-p)^{1-k}, \quad k \in \{0,1\}$$

**Moment Generating Function:**
$$M_X(t) = E[e^{tX}] = (1-p) + pe^t$$

## Physical Intuition / Derivation

The Bernoulli distribution is the fundamental building block for modeling **binary outcomes** in a single trial. Think of it as answering: *"What is the probability of success in one experiment?"*

**Intuitive Examples:**
- Coin flip: $p = 0.5$ (fair coin)
- Product defect: $p = 0.02$ (2% failure rate)
- Network packet loss: $p = 0.01$ (1% loss probability)
- System availability: $p = 0.99$ (99% uptime)

**Why these properties make sense:**
- The mean $E[X] = p$ reflects that if you repeat the trial many times, the fraction of 1's approaches $p$
- The variance $p(1-p)$ is maximized when $p = 0.5$ (maximum uncertainty about the outcome) and minimized at the extremes ($p = 0$ or $p = 1$, where the outcome is certain)
- The distribution is fundamental because **any complex random experiment involving independent binary trials can be decomposed into Bernoulli components**

## Applications in Engineering

### 1. **Reliability and Quality Control**
- Modeling whether a component passes inspection ($p =$ pass rate)
- Predicting defects in manufacturing: if $p = 0.05$, then 5% of items are defective
- Calculating failure probability of a single component in a system

### 2. **Communication Systems**
- **Bit error probability**: In digital communications, $X \sim \text{Ber}(p_e)$ where $p_e$ is the bit error rate (BER)
- **Channel modeling**: Each transmitted bit has probability $p_e$ of being corrupted
- Used to analyze signal-to-noise ratio (SNR) effects

### 3. **Network and Systems Engineering**
- **Packet loss modeling**: Whether a packet is lost ($p =$ loss probability)
- **Server availability**: Whether a server is up or down ($p =$ uptime probability)
- **Connection state**: Link up/down status in network topology

### 4. **Machine Learning and Classification**
- **Binary classification labels**: Instances are labeled as class 0 or 1
- **PAC learning bounds** (as in source material): Analyzing sample complexity when each labeled example follows a Bernoulli-like distribution
- **Hypothesis testing**: Whether a classifier's prediction matches the true label

### 5. **Sensor and IoT Applications**
- **Binary sensor readings**: Motion detector on/off, door open/closed
- **Threshold crossing**: Whether a measurement exceeds a threshold ($X = 1$ if threshold exceeded)

## Relationship to Other Distributions

### Binomial Distribution
If $X_1, X_2, \ldots, X_n$ are $n$ **independent** $\text{Ber}(p)$ random variables, then their sum follows a **Binomial distribution**:

$$Y = \sum_{i=1}^{n} X_i \sim \text{Bin}(n, p)$$

The source material explicitly defines this relationship: Binomial is the sum of i.i.d. Bernoulli trials.

### Rademacher Distribution
The Rademacher distribution with mean $\mu$ (from the source) takes values $\{+1, -1\}$ with probabilities $\frac{1+\mu}{2}$ and $\frac{1-\mu}{2}$. This is a **shifted and scaled Bernoulli**: if $X \sim \text{Ber}(p)$, then $2X - 1 \sim \text{Rad}(2p-1)$.

## Common Mistakes / Pitfalls

### 1. **Confusing Bernoulli with Binomial**
- **Mistake**: Using Binomial formulas for a single trial
- **Correction**: Bernoulli models exactly one trial ($n=1$). Use Binomial for multiple trials.

### 2. **Parameter Range Confusion**
- **Mistake**: Using $p > 1$ or $p < 0$
- **Correction**: Always ensure $p \in [0,1]$. Values outside this range are invalid probabilities.

### 3. **Independence Assumption**
- **Mistake**: Applying Bernoulli analysis to correlated trials
- **Correction**: Bernoulli assumes each trial is independent. Real systems (e.g., packet losses in congested networks) may be correlated.

### 4. **Misidentifying the Random Variable**
- **Mistake**: Treating the outcome as continuous or having more than 2 values
- **Correction**: A true Bernoulli random variable takes **exactly two values**: 0 and 1 (or equivalently, success/failure).

### 5. **Overlooking Bias in Estimation**
- **Mistake**: Using the sample mean $\hat{p} = \frac{\text{# successes}}{n}$ without