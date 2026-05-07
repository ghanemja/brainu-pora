# Secretary Problem

## Definition

The **secretary problem** (also called the **optimal stopping problem** or **marriage problem**) is a decision theory problem in which a decision-maker must select one item from a sequence of $N$ distinct items arriving in random order, with the following constraints:

- Items arrive **sequentially** in uniformly random order
- The decision-maker can **rank any subset of items observed so far** (i.e., determine the best among those seen)
- After observing each item, a decision to **accept or reject must be made immediately and irreversibly**
- The goal is to **maximize the probability of selecting the single best item** (rank 1)
- The decision-maker has **no information about future items**

The problem models realistic scenarios where:
- Job candidates must be hired or rejected during interviews
- One-time decisions have uncertain future consequences
- You cannot revisit previous options

---

## Key Equations

### Optimal Strategy (Classical Problem)

The **optimal threshold rule** is:

$$\text{Reject the first } k^* \text{ candidates, then select the first candidate better than all previous}$$

where the optimal cutoff is approximately:

$$k^* \approx \frac{N}{e}$$

where $e \approx 2.71828$ is Euler's number.

### Success Probability

The maximum probability of selecting the best candidate using the optimal strategy is:

$$P(\text{success}) \approx \frac{1}{e} \approx 0.368$$

This remarkably depends only on $N$ asymptotically, not on its actual value.

### Exact Formula (Finite $N$)

For $N$ candidates with cutoff at position $k$:

$$P(\text{success} \mid k) = \frac{k}{N} \sum_{i=k}^{N-1} \frac{1}{i}$$

The optimal $k^*$ satisfies:

$$\sum_{i=k^*}^{N-1} \frac{1}{i} \approx 1$$

---

## Physical Intuition / Derivation

### Why is $1/e$ Special?

The problem creates a **fundamental trade-off**:

- **Reject too few candidates:** You accept an early mediocre candidate and miss better ones later
- **Reject too many candidates:** You gather good information but run out of candidates to accept

Consider rejecting the first $k$ candidates as a **learning phase**. After position $k$:
- You know the maximum value $M_k$ in the first $k$ candidates
- You select the first candidate better than $M_k$

The success probability depends on two independent events:
1. **The best candidate appears after position $k$:** probability $\frac{N-k}{N}$
2. **The first candidate better than $M_k$ is actually the best:** probability $\approx \frac{k}{N}$ (the best must be among the first $k$ to set the threshold)

Thus:
$$P(\text{success}) \approx \frac{k}{N} \cdot \frac{N-k}{N}$$

Optimizing over $k$ by setting $\frac{d}{dk}\left[\frac{k(N-k)}{N^2}\right] = 0$ gives $k = N/2$ for continuous relaxation. However, the discrete problem with rank comparisons yields $k^* \approx N/e$.

### The Odds Algorithm Intuition

The optimal policy can be viewed through **odds**: the ratio of candidates remaining to candidates already evaluated. The decision rule becomes: *accept a candidate if the odds ratio favors accepting her over continuing the search*.

---

## Applications in Engineering

### 1. **Hiring and Recruitment**
- Determining interview cutoff points before making final offers
- Balancing exploration (interviewing) vs. exploitation (hiring early)
- Applies when candidates cannot be reconsidered (burn bridges, market moves)

### 2. **Real-time Scheduling and Resource Allocation**
- Online scheduling: accept a job request or defer (cannot go back)
- Server load balancing: accept or reject incoming requests
- Network routing: commit to a path before seeing future packets

### 3. **Sensor Networks and Data Streaming**
- Online anomaly detection: decide in real-time if data point is anomalous
- Cache replacement: deciding which items to evict from limited memory
- Load shedding: accepting/rejecting data streams under computational constraints

### 4. **Auctions and Trading**
- Sequential bidding: when to place an offer in online auctions
- Trading decisions: sell an asset now or wait for better prices (with incomplete information)

### 5. **Search and Exploration Problems**
- Web search: how many results to review before committing to a choice
- Experimental design: how many pilot experiments before committing to a design
- Portfolio selection: sample alternatives before investment

### 6. **Robotics and Autonomous Systems**
- Target selection in vision: commit to tracking one object among many candidates
- Path planning: irreversible navigation decisions

---

## Variations and Extensions

### Returning Secretary Problem
**Modification:** Each candidate may reappear with fixed probability $p$. An accepted candidate may be seen again, and the decision-maker can update their acceptance.

**Key insight:** Reappearances reduce optimal rejection phase length $k^*$, since gathering information from repeated appearances improves performance.

### Top-$m$ Secretary Problem  
**Modification:** Success means selecting *any one of the top $m$* candidates (not just rank 1).

**Key results:**
- Success probability increases dramatically (e.g., selecting top 3 gives $\approx 52\%$ success vs. $37\%$ for top 1)
- Optimal threshold shifts **earlier** because the success criterion is relaxed
- Models realistic scenarios where "good enough" outperforms waiting for perfection

### $K$-Choice Secretary Problem
- **Modification:** Select $k$ candidates out of $N$
- Requires balancing diversity and quality

### Knapsack Secretary Problem
- **Modification:** Each candidate has a value and weight; maximize total value under weight constraint
- Introduces combinatorial optimization

---

## Common Mistakes / Pitfalls

### 1. **Assuming the Optimal Threshold is Deterministic**
- Students often think the optimal strategy is a fixed number (e.g., "always reject the first