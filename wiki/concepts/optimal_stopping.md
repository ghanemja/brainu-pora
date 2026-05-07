# Optimal Stopping

## Definition

**Optimal stopping** is a decision problem in stochastic control theory where an agent must decide whether to continue observing a stochastic process or stop and receive a payoff based on the current state. The goal is to maximize expected payoff by choosing the optimal stopping time.

Formally: given a stochastic process $\{X_t\}_{t=0}^{\infty}$ and a reward function $R(X_t)$, find the stopping time $\tau^*$ that maximizes:

$$\mathbb{E}[R(X_{\tau})]$$

subject to the constraint that the stopping decision at time $t$ depends only on information available up to time $t$ (non-anticipative property).

## Key Equations

### Value Function
The **dynamic programming equation** characterizes optimal stopping:

$$V(x_t) = \max\left\{ R(x_t), \mathbb{E}[V(x_{t+1}) \mid x_t] \right\}$$

where $V(x_t)$ is the value of being in state $x_t$ at time $t$.

### Optimal Policy
An optimal policy follows a **threshold rule**: define the optimal value function recursively as

$$V_n(x) = \max\left\{ R(x), \mathbb{E}[V_{n-1}(X_{t+1}) \mid X_t = x] \right\}$$

with boundary condition $V_0(x) = R(x)$.

### Secretary Problem Special Case
For the classical secretary problem with $n$ candidates arriving uniformly at random:
- **Optimal cutoff rule**: reject the first $\frac{n}{e}$ candidates (approximately)
- **Success probability**: $P(\text{select best}) = \frac{1}{e} \approx 0.368$ for large $n$

The **odds algorithm** (Bruss, 1997) states: continue until you see a candidate better than all previous ones, but only if the *odds* of finding a better one later justify stopping.

## Physical Intuition / Derivation

### The Trade-off
Optimal stopping reflects a fundamental trade-off:
- **Exploitation vs. Exploration**: Do we take the best offer seen so far, or continue searching for something better?
- **Information vs. Regret**: Each additional observation provides information but carries the risk of missing a good option that appeared earlier.

### Why Threshold Rules Are Optimal
Consider the secretary problem. At observation $k$, you know:
1. The relative ranking of all candidates seen (you know if candidate $k$ is the best so far)
2. How many candidates remain ($n - k$)
3. The probability that a better candidate appears in the remaining pool

A **threshold rule** (reject the first $t^*$ candidates, then accept the next one better than all previous) is optimal because:

$$V(k) = \begin{cases}
\text{"Wait longer" value} & \text{if } k < t^* \\
\text{Current offer value} & \text{if } k \geq t^* \text{ and candidate is best so far}
\end{cases}$$

The threshold $t^*$ is chosen where the continuation value equals the stopping value. For the classical secretary problem:

$$P(\text{success} \mid \text{stop at position } k) = \frac{t^*}{n} \cdot P(\text{best candidate is after position } k)$$

Setting this equal across all positions and solving yields $t^* = \frac{n}{e}$.

### Intuition for $1/e$ Result
- If you reject too few ($t^* < n/e$), you're likely to reject the best candidate
- If you reject too many ($t^* > n/e$), you're forced to accept an inferior candidate
- The exponential distribution of arrival times leads naturally to the factor $1/e \approx 0.368$

## Applications in Engineering

### 1. **Portfolio Optimization & Investment**
- Deciding when to sell an asset given uncertain future prices
- Optimal liquidation timing in financial markets
- Choosing between accepting a job offer or continuing to interview

### 2. **Real-Time Scheduling**
- Job scheduling in manufacturing: accept a job or wait for a better one
- Network routing: route a packet now or wait for a lower-latency path
- Power management: process a task or wait for lower power costs

### 3. **Quality Control & Inspection**
- When to stop inspecting a batch and release the product
- Reliability testing: when is the system sufficiently tested?
- Acceptance sampling in manufacturing

### 4. **Search & Detection**
- Optimal search time for a target in signal processing
- Sensor networks: when to stop collecting samples and make a decision
- Anomaly detection: threshold for declaring an anomaly detected

### 5. **Online Algorithms**
- Online ad placement: accept a user or wait for higher-value ads
- Cache replacement policies: evict now or wait
- Caching strategies in memory hierarchies

### 6. **Robotics & Control**
- Grasp planning: when to attempt a grasp vs. continue planning
- Path planning: commit to a route or gather more sensor data
- Drone battery management: return home now or continue mission?

## Common Mistakes / Pitfalls

### 1. **Ignoring Information Structure**
❌ **Wrong**: Assuming you can always know the global best without seeing it  
✓ **Right**: Only the relative ordering of observed items is known; future items are uncertain

### 2. **Applying Classical Solution to Non-Classical Problems**
❌ **Wrong**: Using $n/e$ cutoff when candidates can reappear (returning secretary) or success means "top 3" instead of "best 1"  
✓ **Right**: Reprove the threshold rule for your specific reward structure (see source material variations)

### 3. **Confusing Optimal with Greedy**
❌ **Wrong**: "Always take the next candidate better than the current best"  
✓ **Right**: Optimal stopping requires knowing the cutoff point; greedy is often suboptimal

### 4. **Neglecting Boundary Effects**
❌ **Wrong**: Applying large-$n$ approximations to small problem sizes  
✓ **Right**: Use dynamic programming for exact solutions on small