# Union Bound

## Definition

The **union bound** (also called **Boole's inequality**) is a fundamental principle in probability theory that upper-bounds the probability of a union of events by the sum of their individual probabilities.

For any finite or countable collection of events $E_1, E_2, \ldots, E_n$:

$$\Pr\left[\bigcup_{i=1}^{n} E_i\right] \leq \sum_{i=1}^{n} \Pr[E_i]$$

## Key Equations

**Basic form (finite events):**
$$\Pr\left[\bigcup_{i=1}^{n} E_i\right] \leq \sum_{i=1}^{n} \Pr[E_i]$$

**Intuition for two events:**
$$\Pr[A \cup B] = \Pr[A] + \Pr[B] - \Pr[A \cap B] \leq \Pr[A] + \Pr[B]$$

The inequality becomes an equality only when all events are mutually exclusive (disjoint).

**Application to $n$ identical events** (common case):
If $\Pr[E_i] = p$ for all $i$, then:
$$\Pr\left[\bigcup_{i=1}^{n} E_i\right] \leq np$$

## Physical Intuition / Derivation

### Why it works

The union bound avoids the complexity of computing intersections. Consider two events:
- The true probability of their union is $\Pr[A \cup B] = \Pr[A] + \Pr[B] - \Pr[A \cap B]$
- Since $\Pr[A \cap B] \geq 0$, we have $\Pr[A \cup B] \leq \Pr[A] + \Pr[B]$

For $n$ events, we repeatedly apply this reasoning: each new event can contribute at most its own probability to the union (since it might overlap completely with previous events).

### Why it's useful

The union bound is **not tight** (usually quite loose), but it has two critical advantages:

1. **Simplicity**: No need to compute complex intersection probabilities
2. **Composability**: Easily combines independent failure modes

This makes it invaluable for analyzing systems with many potential failure points.

### Illustrative Example

Suppose we want to guarantee that **none** of $n$ bad events occurs:
$$\Pr[\text{no bad event}] = \Pr\left[\bigcap_{i=1}^{n} \overline{E_i}\right] = 1 - \Pr\left[\bigcup_{i=1}^{n} E_i\right] \geq 1 - \sum_{i=1}^{n} \Pr[E_i]$$

If each event has probability $p_i \leq \frac{c}{n^2}$, then $\sum p_i \leq \frac{c}{n}$, and with high probability (whp) none occur.

## Applications in Engineering

### 1. **Algorithm Design & Analysis**

The union bound is essential for proving algorithms work with high probability (whp). In the source material's parallel semisort algorithm:

- **Underallocation failures**: For each of $n$ keys and $B \leq n$ buckets, individual failure probability is $n^{-c}$
- **Union bound application**: Total failure probability $\leq n \cdot n^{-c} + n \cdot n^{-c} = O(n^{1-c})$
- This allows guaranteeing structural properties across all elements simultaneously

### 2. **Hash Table Collision Analysis**

When hashing $m$ records into $K \cdot m$ slots with 2-universal hashing (from source):
$$\Pr[\text{collision}] \leq \binom{m}{2} \cdot \frac{1}{K \cdot m} \leq \frac{m^2}{2Km}$$

Applying union bound over $B$ buckets confirms all buckets satisfy collision requirements.

### 3. **Concentration Bounds & Deviation Guarantees**

Combined with Chernoff bounds (as in the source), union bound enables:
- Proving Chernoff concentration holds for **all** variables simultaneously
- Example: $\Pr[\exists x : \hat{W} \leq \mu(x) - t] \leq n \cdot \Pr[\hat{W}_x \leq \mu(x) - t] \leq n \cdot \exp(-t^2/2\mu)$

### 4. **Network & Reliability Engineering**

- **Component failures**: If a system has $n$ independent components, each with failure probability $p$, probability that **at least one** fails: $\Pr[\text{failure}] \leq np$ (for small $p$)
- **Packet loss**: Probability that **any** of $n$ packets is dropped in transmission

### 5. **Machine Learning & Model Selection**

- **Multiple hypothesis testing**: If testing $n$ models, union bound controls type-I error across all tests
- **Generalization bounds**: Probability that **any** of $n$ classifiers overfits can be bounded via union

## Common Mistakes / Pitfalls

### 1. **Assuming the bound is tight**
The union bound is often very loose! If $n=100$ and each $\Pr[E_i] = 0.01$, union bound gives $\Pr[\bigcup E_i] \leq 1$, which is vacuous. The actual probability could be much smaller.

**Fix**: Use tighter bounds (Chernoff, Chebychev, etc.) when events have special structure, then apply union bound only over truly independent failure modes.

### 2. **Over-counting independent events**
Union bound is most effective when events are truly independent and few. Applying it carelessly to dependent events or massive numbers of events can make bounds useless.

**Example**: If each $\Pr[E_i] = n^{-c}$ and $n$ is very large, $\sum \Pr[E_i]