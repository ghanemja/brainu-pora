# Competitive Ratio Analysis

## Definition

**Competitive ratio analysis** is a theoretical framework for evaluating the performance of online algorithms by comparing their objective value against an optimal offline algorithm operating on the same input instance.

Formally, for a minimization problem, an online algorithm $\mathcal{A}$ is said to be **$c$-competitive** if there exists a constant $k$ such that for all input sequences $\sigma$:

$$\text{Cost}(\mathcal{A}, \sigma) \leq c \cdot \text{Cost}(\text{OPT}, \sigma) + k$$

where:
- $\text{Cost}(\mathcal{A}, \sigma)$ = cost incurred by algorithm $\mathcal{A}$ on input $\sigma$
- $\text{Cost}(\text{OPT}, \sigma)$ = cost incurred by an optimal offline algorithm with complete knowledge of $\sigma$
- $c \geq 1$ is the **competitive ratio** (smaller is better)
- $k$ is an additive constant (often $k=0$, termed **strictly $c$-competitive**)

The competitive ratio quantifies the worst-case performance degradation due to lack of future information.

## Key Equations

### Basic Competitive Ratio Definition
$$\text{CR}(\mathcal{A}) = \inf\{c : \text{Cost}(\mathcal{A}, \sigma) \leq c \cdot \text{Cost}(\text{OPT}, \sigma) + k \text{ for all } \sigma\}$$

### Lower Bound on Competitive Ratio
For many online problems, lower bounds are established via adversarial analysis:
$$\text{CR}_{\text{lower}} = \inf_{\mathcal{A}} \sup_{\sigma} \frac{\text{Cost}(\mathcal{A}, \sigma)}{\text{Cost}(\text{OPT}, \sigma)}$$

### Parameterized Competitive Ratio (α-clairvoyant example)
When algorithms depend on a parameter $\alpha \in [0,1]$ controlling information revelation:
$$\text{CR}(\alpha) = O\left(\frac{1}{1-\alpha}\right), \quad \text{for } 0 \leq \alpha < 1$$

This shows how competitive ratio degrades gracefully as clairvoyance decreases (as $\alpha \to 1$, ratio $\to \infty$).

### Randomized Competitive Ratio
For randomized algorithms $\mathcal{R}$:
$$\text{CR}_{\text{rand}}(\mathcal{R}) = \inf\{c : \mathbb{E}[\text{Cost}(\mathcal{R}, \sigma)] \leq c \cdot \text{Cost}(\text{OPT}, \sigma) + k\}$$

## Physical Intuition / Derivation

### Why Competitive Ratio Matters

Consider a scheduling problem where an online scheduler must decide job priorities without knowing future job lengths. Unlike an offline algorithm (which sees all jobs upfront and can optimize globally), the online algorithm makes irrevocable decisions with incomplete information.

The competitive ratio captures: *"In the worst case, how much worse does my online algorithm perform than an all-knowing adversary?"*

### Intuition Through Delayed-Clairvoyant Scheduling Example

The α-clairvoyant model illustrates the framework elegantly:

1. **α = 0 (Full Clairvoyance):** The scheduler learns job length immediately upon arrival. The shortest-remaining-processing-time (SRPT) rule is optimal with $\text{CR} = 1$.

2. **0 < α < 1 (Partial Information):** After processing an $\alpha$-fraction of a job, its full length becomes known. The algorithm has limited but growing information. Analysis shows:
   $$\text{CR}(\alpha) = O\left(\frac{1}{1-\alpha}\right)$$
   
   **Why this dependence?** As $\alpha$ increases (delaying information), the algorithm accumulates longer jobs in the queue with high uncertainty, forcing suboptimal scheduling decisions. The factor $(1-\alpha)^{-1}$ captures the "information deficit."

3. **α = 1 (Non-Clairvoyant):** Job length only revealed at completion. No constant competitive ratio exists—the adversary can construct instances where online algorithms perform arbitrarily poorly relative to OPT.

### Proof Strategy: Borrow Graph Analysis

The source material uses a "borrow graph" technique:
- Model the algorithm's decisions as a directed graph where edges represent resource dependencies
- Show that the online algorithm's cost is bounded by (worst-case) graph structure scaled by some constant
- Derive competitive ratio by bounding the maximum cost ratio over all possible graphs

## Applications in Engineering

### 1. **Operating System Scheduling**
- Real OSs estimate job (process/task) runtime via profiling
- Competitive ratio analysis validates scheduling heuristics (e.g., multilevel feedback queues)
- Determines performance guarantees under worst-case workloads

### 2. **Cloud Computing / Data Center Management**
- VM placement and resource allocation under uncertain job durations
- Batch job scheduling minimizes total turnaround time
- α-clairvoyant model matches cloud profiling practices (job runtime predictions improve as tasks execute)

### 3. **Network Routing and Packet Scheduling**
- Packet arrival patterns are uncertain; routing decisions must be made online
- Competitive ratio bounds QoS degradation vs. offline algorithms with global network knowledge
- Applications in software-defined networks (SDN) and edge computing

### 4. **Caching and Memory Management**
- Page replacement policies (LRU, etc.) compared to offline optimal via competitive analysis
- Bounds on cache miss rates inform memory hierarchy design
- Extends to modern problems like content delivery networks

### 5. **Supply Chain / Inventory Management**
- Demand forecasting parallels job length prediction
- Competitive ratio quantifies cost penalty from demand uncertainty
- Guides safety stock levels and order policies

### 6. **Auction and Pricing Algorithms**
- Online auctions lack future bid information
- Competitive ratio determines pricing strategy performance bounds
- Example: Secretary problem with competitive ratio ≈ 1/e

## Common Mistakes / Pitfalls