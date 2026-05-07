# Online Matching Algorithm

## Definition

An **online matching algorithm** is an algorithmic framework for constructing maximum-weight matchings in graphs where edges arrive sequentially (or are processed in an order chosen by the algorithm) and matching decisions are irrevocable. Upon encountering an edge $e = (u, v)$, the algorithm observes its weight/value and must immediately decide whether to include it in the matching, subject to the constraint that each vertex can be matched at most once.

The **action-reward query-commit matching problem** generalizes this setting: for each edge $e$, the algorithm selects an action $a \in A_e$ (e.g., offering a payment level $\tau$ to a worker, or setting a threshold). The action succeeds (edge is added to matching) with probability $q_e(a)$, and yields expected reward $r_e(a)$ upon success. The algorithm has a **patience constraint**: each vertex can receive at most $k$ action offers.

The objective is to maximize expected total reward (or expected social welfare, or expected revenue, depending on problem variant).

---

## Key Equations

### Free-Order Prophet Matching

For an edge $e$ with weight $W_e \sim D_e$ and threshold action $a$ corresponding to threshold $\tau_e$:

$$q_e(a) = \mathbb{P}[W_e \geq \tau_e]$$

$$r_e(a) = \mathbb{E}[W_e \mid W_e \geq \tau_e]$$

### Sequential Pricing Problem

For an edge $e = (u, v)$ with payment offer $\tau \geq 0$:

**Acceptance probability:** $q_e(a) = p_{u,v}(\tau)$

**Revenue reward:** $r_e(a) = b_u - \tau$ (where $b_u$ is job value)

**Social welfare reward:** $r_e(a) = b_u - \mathbb{E}[C_{u,v} \mid C_{u,v} \leq \tau]$ (where $C_{u,v}$ is worker cost)

### Threshold Policy Optimality

For free-order prophet matching, an **optimal threshold policy** exists:
- Select threshold $\tau_e$ for each edge $e$ before processing
- Include edge $e$ in matching iff $W_e \geq \tau_e$
- Optimal thresholds lie in the support of $D_e$

---

## Physical Intuition / Derivation

### Why Online Matching Matters

Traditional matching algorithms assume full knowledge of the graph. In many real-world systems, edges (opportunities) arrive dynamically:

- **Job marketplace:** A job posting appears; a worker decides whether to apply at an offered wage
- **Dating/ridesharing:** Potential matches materialize sequentially
- **Network routing:** Links fail/appear over time

The algorithm **cannot defer decisions**—accepting edge $e$ blocks both $u$ and $v$ from future matches. This creates an inherent exploration-exploitation tradeoff: accept a good offer now, or wait for a potentially better match?

### Reduction to Action-Reward Framework

The framework unifies disparate problems by recognizing that:

1. **Uncertain outcomes:** Not all offered edges are accepted (stochastic matching)
2. **Decision parameterization:** The algorithm controls outcomes via actions (payment levels, thresholds)
3. **Tradeoff between success probability and reward:** Higher payments increase acceptance but lower revenue

**Example (Sequential Pricing):**
- Action: "offer payment $\tau$"
- Success probability: Worker accepts with probability $p_{u,v}(\tau)$ (typically increasing in $\tau$)
- Reward if successful: Platform gains $b_u - \tau$ (benefit minus cost)

The algorithm trades off:
- **High $\tau$:** Nearly certain match, but low profit margin
- **Low $\tau$:** High profit if accepted, but low acceptance probability

**Example (Free-Order Prophet Matching):**
- Action: "set threshold $\tau_e$"
- Success probability: Weight exceeds threshold, $\mathbb{P}[W_e \geq \tau_e]$
- Reward if successful: Conditional expectation $\mathbb{E}[W_e \mid W_e \geq \tau_e]$

**Optimality of Threshold Policies:** Consider why thresholds are optimal. For an edge $e$ at decision time, the algorithm knows:
- Its own future "flexibility" (remaining vertex capacity)
- The distribution of future edge weights

A threshold policy says: "Accept $e$ only if its weight justifies committing a vertex." This is optimal because the future looks statistically identical, and the commitment cost is the same regardless of when you pay it. Thus, comparing against a fixed threshold captures the optimal tradeoff.

### Patience Constraints

Each vertex $v$ can receive at most $k$ offers. This reflects real constraints:
- Workers have limited attention/bandwidth
- Servers have limited connection slots

Under patience constraints, the matching problem becomes harder (no longer a simple threshold suffices in general), but the action-reward framework still applies.

---

## Applications in Engineering

### 1. **Gig Economy Platforms (Uber, TaskRabbit, Upwork)**

**Problem:** Dynamically match workers to jobs, setting wages to balance:
- Worker acceptance rate (higher wages → higher acceptance)
- Platform profit margin (higher wages → lower profit)

**Application:**
- Each job $u$ arrives sequentially
- Platform queries available workers $v$ with payment offer $\tau$
- Worker accepts with known probability $p_{u,v}(\tau)$ (learned from historical data)
- Platform maximizes expected revenue $\sum \mathbb{E}[b_u - \tau]$ subject to worker patience constraints

**Outcome:** Online pricing algorithm that dynamically adjusts offers based on job values and worker availability.

---

### 2. **Ad Auctions & Real-Time Bidding**

**Problem:** Allocate ad slots to bidders arriving online, maximizing revenue or welfare.

**Application:**
- Ad slot $u$ appears; bidders $v$ submit bids drawn from known distributions
- Platform commits to bidder-slot pairing instantly
- Setting a reserve price $\tau$ is equivalent to an action: accept only bids $\geq \tau$
-