# Sequential Decision-Making

## Definition

**Sequential decision-making** is the process of making a series of irrevocable choices over time, where:
- Information about options arrives progressively (often in random order)
- Each decision must be made immediately without knowledge of future arrivals
- Past rejected options cannot be reconsidered
- The goal is to optimize a global objective (e.g., selecting the best option, maximizing expected value)

This contrasts with batch decision-making, where all options are known upfront. Sequential decision-making is fundamental to **optimal stopping theory**—the mathematics of determining when to stop searching and act.

## Key Equations

### Classical Secretary Problem Success Probability

For $n$ interviewees, reject the first $k$ candidates and select the first one better than all of them:

$$P(\text{success}) = \frac{k}{n} \sum_{i=k}^{n-1} \frac{1}{i}$$

As $n \to \infty$, the optimal threshold is $k^* \approx \frac{n}{e}$, achieving success probability:

$$P^* \approx \frac{1}{e} \approx 0.368$$

### Odds Algorithm (General Optimal Strategy)

For a sequence with relative rank $r_i$ at position $i$, the optimal rule accepts if:

$$\frac{\text{probability of success if accept now}}{\text{probability of success if continue}} \geq 1$$

This leads to the **threshold rule**: 
- Reject initial candidates until reaching threshold position $k^*$
- Accept the first candidate exceeding the best seen so far

## Physical Intuition / Derivation

### Why the $1/e$ Threshold Emerges

The secretary problem embodies a fundamental exploration-exploitation tradeoff:

1. **Early rejection phase** ($i \leq k$): Gather information about the candidate pool's quality without committing. You learn the baseline ("best so far").

2. **Acceptance phase** ($i > k$): Stop exploring; accept the first candidate exceeding your learned baseline.

**Intuition for optimality:**
- If $k$ is too small: You commit too early with insufficient information about pool quality
- If $k$ is too large: You waste positions that could be used for accepting good candidates

The $1/e$ ratio emerges from balancing the probability that the global optimum appears in the acceptance phase ($\frac{n-k}{n}$) against the probability your threshold correctly identifies it ($\frac{k}{i}$ for candidate at position $i$).

In the limit, the integral formulation gives:
$$\max_{\alpha \in [0,1]} \alpha \int_{\alpha}^{1} \frac{dx}{x} = \max_{\alpha} \alpha \ln(1/\alpha) = \frac{1}{e} \text{ at } \alpha = 1/e$$

### Generalizations from Source Material

**Top-k variation**: Instead of selecting the best, accept any of the top $k$ candidates. This:
- Significantly increases success probability (e.g., top-3 selection $\approx 70\%$)
- Shifts optimal threshold earlier (more aggressive acceptance)
- Models realistic scenarios where candidates are "close in quality"

**Returning candidates**: When candidates may reappear with probability $p$:
- Additional observations refine ranking information
- Optimal threshold becomes adaptive—depends on $p$ and observation history
- More structure in the problem allows higher success rates

## Applications in Engineering

### 1. **Real-Time Resource Allocation**
- **Job scheduling**: Accept or reject incoming tasks for processor assignment knowing limited queue capacity
- **Network packet routing**: Forward or drop packets with incomplete destination information

### 2. **Sensor and Data Fusion**
- **Sequential hypothesis testing**: Accept/reject a hypothesis based on streaming sensor data
- **Fault detection**: Decide when to trigger alarms based on partial system observations

### 3. **Online Optimization**
- **Price setting in auctions**: Set bid thresholds when buyer valuations arrive sequentially
- **Cache replacement policies**: Evict cache lines based on limited future access information

### 4. **Robotics and Control**
- **Motion planning**: Commit to actions in dynamic environments with partial observability
- **Grasp selection**: Robot must decide when to execute grasp before target shifts

### 5. **Supply Chain and Operations**
- **Inventory acceptance**: Accept/reject incoming batches before inspecting entire shipment
- **Supplier selection**: Choose vendor based on limited past performance and incomplete future contracts

## Common Mistakes / Pitfalls

### 1. **Assuming Equal Information at All Positions**
**Error**: Treating the first and last candidates identically in strategy design.  
**Reality**: Candidate $i$ carries different information value. Late candidates have high "acceptance bar" because few remain.

### 2. **Greedy Selection Without Threshold Learning**
**Error**: Accepting the first "good-looking" candidate without establishing baseline.  
**Reality**: Optimal strategy *requires* a learning phase. Premature acceptance forfeits information gain.

### 3. **Confusing "Best" with "Good Enough"**
**Error**: Assuming the goal is always to find the global optimum.  
**Reality**: Many practical settings care about top-$k$ (e.g., hiring two scientists, not necessarily THE best). Success probability changes dramatically.

### 4. **Ignoring Discount Rates**
**Error**: Treating all future candidates as equally valuable.  
**Reality**: In time-critical applications (time-to-decision cost), waiting has a cost. Threshold shifts earlier.

### 5. **Misapplying Classical Results to Small $n$**
**Error**: Using $k \approx n/e$ for $n=5$ interviewees.  
**Reality**: Asymptotic formula is poor for small $n$. Must compute exact threshold numerically.

## See Also

- [[Optimal Stopping Theory]] — General framework for deciding when to stop search/wait
- [[Dynamic Programming]] — Computational backbone for solving sequential decision problems
- [[Markov Decision Processes]] — Extension to multi-stage decisions with state transitions
- [[Bandit Algorithms]] — Exploration-exploitation in sequential sampling contexts
- [[Online Learning]] — Sequential decision-making under partial feedback

## Sources

- Agrawal, S. & Saxena, S. (2026). "