# Online Algorithm

## Definition

An **online algorithm** is a computational procedure that must make irrevocable decisions in response to sequential input requests, without knowledge of future requests. Unlike offline algorithms that have complete input information before making decisions, online algorithms operate under uncertainty and must optimize their response at each stage.

### Formal Characterization

For a sequence of requests $X = \{X_1, X_2, \ldots, X_n\}$ arriving sequentially, an online algorithm $\text{ALG}$ must:

1. Process request $X_i$ without knowledge of $X_j$ for all $j > i$
2. Generate a response (decision) $Z_i$ immediately upon receiving $X_i$
3. Incur a cost that cannot be undone or revised

The **competitive ratio** $\rho$ measures how well an online algorithm performs relative to the optimal offline solution:

$$\rho = \frac{\text{Cost}_{\text{ALG}}(X)}{\text{OPT}(X)}$$

An online algorithm is $\rho$-competitive if this ratio is bounded by $\rho$ for all possible input sequences.

## Key Equations

### Competitive Ratio Definition

For an arbitrary algorithm $\text{ALG}$ responding to requests with costs $c_i$:

$$c_i = \text{ALG}(X_i; \alpha) = \sum_{j=0}^{i-1} |P_j P_{j+1}|$$

where $P_j$ is the algorithm's response to request $X_j$.

### MaxHedge Algorithm Response

The MaxHedge algorithm with parameter $\rho$ places its response $Z_i$ such that:

$$|Z_{i-1} Z_i| = \rho(o_i - o_{i-1})$$

where $o_i = \text{OPT}(X_i; \alpha)$ is the optimal offline cost for the first $i$ requests.

### Optimal Cost Structure (Example)

For certain geometric request sequences:

$$o_i = \sqrt{s^2 - 4s + (1+s)^2\sin^2(\alpha)}$$

This represents the cumulative optimal cost, which grows predictably with the sequence length.

## Physical Intuition / Derivation

### Why Online Problems Are Hard

Online algorithms face a fundamental dilemma: **early decisions constrain future options**. Consider a geometric setting where:
- Requests arrive as points $X_i$ in some space
- The algorithm must position responses $Z_i$ 
- Cost accumulates with distance traveled: $\sum |Z_{i-1}Z_i|$

The algorithm cannot know whether the next request will return to the previous side of a boundary (favoring hedging) or continue forward (favoring commitment).

### MaxHedge: Maximal Hedging Strategy

MaxHedge embodies a principle of **balanced preparation**: it allocates movement budget $\rho(o_i - o_{i-1})$ at each step such that:

1. **Commits forward** to maintain competitiveness with offline optimal
2. **Hedges laterally** (moving along the direction $\vec{T_i T_{i+1}}$) to prepare for adversarial next requests
3. **Uses geometric intersection** to ensure the movement lies on a halfline (feasible region) while respecting the budget

The algorithm succeeds if a feasible point $Z_i$ exists on both:
- The halfline $\overrightarrow{T_i T_{i+1}}$ (path constraints)
- A circle of radius $\rho(o_i - o_{i-1})$ centered at $Z_{i-1}$ (budget constraint)

If they don't intersect, the algorithm **fails**, meaning no $\rho$-competitive solution exists.

### Optimality Claim

**Theorem (Implicit):** The optimal competitive ratio for a request sequence $X$ is the minimum $\rho$ for which MaxHedge succeeds on $X$.

This works because MaxHedge maximally prepares for adversarial continuations while respecting a fixed competitive ratio budget—no algorithm can do better without violating the ratio constraint.

## Applications in Engineering

### 1. **Online Scheduling & Resource Allocation**
- Job scheduling on parallel machines without knowing future arrivals
- Cloud computing: allocating servers to requests without demand forecasting
- **Competitive ratio analysis** guides SLA design (e.g., $O(\log n)$-competitive scheduling)

### 2. **Navigation & Robotics**
- Robot path planning with adversarial target sequences
- Real-time obstacle avoidance where future obstacles unknown
- **Geometric online algorithms** (like MaxHedge) model spatial commitment vs. preparation tradeoffs

### 3. **Network Routing**
- Packet routing in dynamic networks (requests = packet arrivals)
- Without global network state, routers must decide packet forwarding online
- Competitive ratio bounds inform congestion guarantees

### 4. **Financial Trading & Caching**
- Online stock trading: decide buy/sell without future price information
- Cache replacement policies: evict pages without knowing future accesses
- **Adversarial analysis** reveals worst-case performance

### 5. **Paging & Memory Management**
- Classic application: demand paging in virtual memory
- LRU cache is $k$-competitive for $k$ cache pages
- Competitive ratio analysis predicts performance without statistical assumptions

## Common Mistakes / Pitfalls

### 1. **Confusing Online with Real-Time**
**Mistake:** Thinking online algorithms are about speed/latency.  
**Correction:** Online refers to *information availability*, not execution speed. An online algorithm can be slow; what matters is that decisions are irrevocable given incomplete information.

### 2. **Assuming Competitive Ratio = Approximation Ratio**
**Mistake:** Using $\rho$ as an approximation factor for a single instance.  
**Correction:** Competitive ratio is a *worst-case guarantee* over all possible adversarial sequences. A single instance may be solved near-optimally.

### 3. **Misidentifying When MaxHedge Fails**
**Mistake:** Thinking MaxHedge always finds a feasible response.  
**Correction:** Failure occurs when the halfline and circle don't intersect—this proves no $\rho$-