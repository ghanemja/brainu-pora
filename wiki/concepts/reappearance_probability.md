# reappearance probability

## Definition

**Reappearance probability** (denoted $p$) is the fixed probability that a candidate or entity who was previously observed and rejected in a sequential decision process will appear again in a future round of observation. In the context of optimal stopping problems, it extends classical models (like the secretary problem) by allowing rejected candidates a second chance to be selected.

Formally: if an interviewee is rejected at their first appearance, they reappear independently with probability $p \in [0,1]$ at a later point in the sequence. The decision-maker observes both first and subsequent appearances and must decide whether to accept or reject at each encounter.

## Key Equations

For the **returning secretary problem with reappearance probability $p$**:

The optimal decision rule depends on whether the current candidate represents:
1. A new candidate (first appearance)
2. A returning candidate (second appearance with probability $p$)

Let $V(k, b, S)$ denote the value function representing the maximum probability of selecting the best candidate when:
- $k$ candidates have been processed
- $b$ is the best rank observed so far  
- $S$ is the set of candidates still expected to reappear

The **threshold strategy** characterizes the optimal policy:
$$\text{Accept if } \text{rank}(c) < \text{threshold}(k, p)$$

where the threshold depends on:
$$\text{threshold}(k, p) = f(k/N, p)$$

For the classical secretary problem ($p = 0$, no reappearance), the cutoff is:
$$k^* \approx \frac{N}{e}$$

With reappearance probability $p > 0$, the threshold shifts earlier because rejected candidates may return, providing additional decision opportunities.

## Physical Intuition / Derivation

### Why Reappearance Changes the Optimal Strategy

In the **classical secretary problem**, once you reject a candidate, they're gone forever. This creates pressure to accept candidates earlier than you might prefer—you trade off the risk of seeing someone worse against the certainty that better candidates may never return.

**Introducing reappearance probability $p$** fundamentally changes this calculus:

1. **Option value increases**: A rejected candidate at rank $r$ is not permanently lost; with probability $p$, they return and can be selected later.

2. **Information accumulation**: Each reappearance provides confirmation. A candidate who reappears is still ranked exactly as before, but now you've seen more of the competitive field, making relative comparison more confident.

3. **Threshold migration**: With higher $p$, you can afford to be more selective early on because:
   - Strong candidates are more likely to reappear (they haven't been accepted, but the problem is symmetric)
   - Weak early candidates are less likely to appear again—or if they do, you've seen better options by then

**Intuitive trade-off**:
- As $p \to 0$ (reappearance unlikely), threshold approaches classical solution at $n/e$
- As $p \to 1$ (reappearance nearly certain), threshold moves earlier and the problem approaches a full-information setting

### Derivation Sketch

The optimal policy follows from dynamic programming:

$$V_k = \max \begin{cases} 
\text{Accept candidate} & \rightarrow \text{utility} = 1 \text{ if best} \\
\text{Reject candidate} & \rightarrow \text{utility} = pV_{k+1} + (1-p)V_{k+1}' 
\end{cases}$$

where:
- Rejecting yields expected value from remaining candidates
- With probability $p$, the rejected candidate returns
- With probability $(1-p)$, they don't return, shifting the effective pool

The **comparative statics** show:
$$\frac{\partial \text{threshold}}{\partial p} < 0$$

Higher reappearance probability shifts the optimal cutoff **downward** (accept later).

## Applications in Engineering

### 1. **Hiring and Talent Acquisition**
- Candidates can interview again if not initially selected; reappearance probability models likelihood they stay in the applicant pool
- Used to optimize which candidate round to extend offers, balancing risk of losing top talent against gathering more information

### 2. **Dynamic Procurement and Vendor Selection**
- Suppliers may resubmit bids or renegotiate contracts with probability $p$
- Engineering procurement teams use this to decide whether to accept a supplier now or wait for better terms if they reappear

### 3. **Online Matching and Real-Time Auctions**
- Buyers in dynamic matching markets (cloud resource allocation, ad exchanges) need to decide whether to match with a current provider
- Reappearance probability models how often providers return to the marketplace
- Optimal cutoff thresholds reduce computational burden in high-frequency matching

### 4. **Sensor and Target Selection**
- In surveillance/robotics, a target (object of interest) may leave the sensor field and reappear with probability $p$
- Decision algorithms must choose whether to "commit" to tracking a current target or wait for the next one
- Reappearance probability informs resource allocation policies

### 5. **Portfolio and Asset Selection**
- Financial engineers use variants to model acquisition of volatile assets that may "re-enter" an acceptable trading range
- Optimal stopping with reappearance helps determine when to enter/exit positions

## Common Mistakes / Pitfalls

1. **Assuming $p$ is endogenous**: Reappearance probability is treated as exogenous and fixed. In reality, $p$ may depend on how "well" you rejected a candidate (harsh rejection vs. polite deferral), violating the model assumptions.

2. **Confusing reappearance with replacement**: A reappearing candidate has the same rank; they are not drawn from a new distribution. Students sometimes incorrectly apply Bayesian updating as if reappearance provides new information about candidate quality.

3. **Ignoring cutoff direction**: Counterintuitively, higher reappearance probability moves the optimal threshold **earlier** (lower rank cutoff), not later. The intuition that "more chances means be more selective" is backward here.

4. **Applying classical analysis uncritically**: The classical secretary problem's solution ($n/e$ cutoff) is not robust to reappearance. Using the classical threshold with $p > 0$ will significantly subopt