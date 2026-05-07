# Recursive Formula

## Definition

A **recursive formula** is a mathematical relation that defines a sequence, function, or probability by expressing each term (or value) as a function of one or more preceding terms. In the context of optimal stopping problems and dynamic programming, a recursive formula establishes a backward-induction relationship where the solution at state $k$ depends on solutions at states $k+1, k+2, \ldots, n$.

Formally, if $P(k)$ denotes the probability of success when applying an optimal strategy starting at position $k$, a recursive formula takes the form:

$$P(k) = f(k, P(k+1), P(k+2), \ldots, P(n))$$

where $f$ is determined by the problem structure, with a **base case** $P(n)$ (or $P(0)$) providing the termination condition.

## Key Equations

### General Form
For threshold-based strategies in secretary-type problems, the recursive probability is:

$$P(k) = \frac{1}{n-k+1} \cdot \max\left(c_k, \sum_{i=k}^{n} P(i+1) \cdot \mathbb{1}[\text{accept at } i]\right)$$

where $c_k$ is the immediate payoff (or success probability) for accepting the candidate at position $k$.

### Concrete Example: Classical Secretary Problem with Threshold $k$
If we observe the first $k-1$ candidates without selecting, then select the first candidate better than all previous ones:

$$P(k) = \begin{cases}
\text{Base case: } P(n+1) = 0 \\
\text{Recursive step: } P(k) = \frac{1}{n-k+1} + \frac{n-k}{n-k+1} \cdot P(k+1)
\end{cases}$$

### Returning Secretary Problem
When each candidate reappears with probability $p$:

$$P(k) = \frac{1}{n-k+1} \cdot [1 + (1-p) \cdot P(k+1)] + \frac{n-k}{n-k+1} \cdot P(k+1)$$

This accounts for the possibility that a rejected candidate returns.

### Top-3 Selection Variant
For selecting a candidate in the top 3:

$$P_{\text{top-3}}(k) = \text{Pr}[\text{rank} \leq 3 \mid \text{threshold } k] + (1-\text{acceptance rate}) \cdot P_{\text{top-3}}(k+1)$$

## Physical Intuition / Derivation

### Why Recursive Formulas Work

Recursive formulas exploit the **principle of optimality**: the optimal decision at any stage depends only on the optimal decisions for remaining future stages, not on how we arrived at the current state. This is a cornerstone of dynamic programming.

**Backward Induction Intuition:**

1. **Start from the end**: At position $n$ (the last candidate), we either accept them or fail. Thus $P(n)$ is a boundary condition.

2. **Work backward**: At position $k$, we face a choice:
   - **Accept the current candidate** → success with some probability (depending on their rank)
   - **Reject and continue** → move to position $k+1$ with success probability $P(k+1)$

3. **Optimal decision**: Choose the action maximizing expected success:
   $$P(k) = \max(\text{accept payoff}, \text{reject payoff}) = \max(\text{payoff}_k, P(k+1))$$

### Derivation for Secretary Problem

For a threshold strategy accepting the first candidate after position $k$ who is better than all previous:

- **Probability current candidate is best among those seen so far**: $\frac{1}{n-k+1}$ (uniform over $k$ candidates)
- **Expected success by rejecting**: $P(k+1)$ (defer decision to next candidate)

Therefore:
$$P(k) = \underbrace{\frac{1}{n-k+1}}_{\text{accept}} + \underbrace{\frac{n-k}{n-k+1} \cdot P(k+1)}_{\text{reject}}$$

The weighted average reflects that with probability $\frac{1}{n-k+1}$ we accept (and succeed if this is the best), and with probability $\frac{n-k}{n-k+1}$ we reject and continue.

## Applications in Engineering

### 1. **Online Decision Making & Control**
- **Resource allocation** in cloud computing: Deciding when to accept a job submission given uncertain future job quality
- **Sensor scheduling**: Choosing when to query a sensor given streaming data with unknown future information

### 2. **Auction & Matching Algorithms**
- **Online hiring systems**: Secretary problem variants determine optimal interview-to-hire thresholds
- **Ad placement**: Deciding which advertiser to accept in real-time bidding with limited lookhead

### 3. **Signal Processing & Change Detection**
- **Sequential hypothesis testing**: Recursive formulas compute optimal stopping rules for detecting anomalies
- **Predictive maintenance**: Determining when to replace equipment given degradation signals

### 4. **Operations Research**
- **Inventory management**: Reorder point policies derived via recursive dynamic programming
- **Scheduling**: Job shop scheduling with real-time arrivals

### 5. **Financial Engineering**
- **Option pricing**: American option valuations computed recursively (binomial models)
- **Optimal stopping for asset sales**: Deciding when to sell given uncertain future prices

## Common Mistakes / Pitfalls

### 1. **Forgetting the Base Case**
**Error**: Deriving a beautiful recursive relation but not specifying $P(n)$ or $P(\infty)$.
- **Fix**: Always explicitly state boundary conditions. In secretary problems: $P(n+1) = 0$ (no candidates remain).

### 2. **Confusing Forward and Backward Recursion**
**Error**: Writing $P(k) = f(P(k-1))$ when the problem naturally decouples backward in time.
- **Fix**: Use the Markov property: future decisions don't affect past. Always recur