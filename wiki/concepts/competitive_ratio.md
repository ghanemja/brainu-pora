# competitive ratio

## Definition

The **competitive ratio** is a fundamental performance metric in online algorithms that measures how well an algorithm performs relative to the optimal offline algorithm on the same input sequence.

Formally, for an online algorithm ALG and an input instance $X$, the **competitive ratio** $\rho$ is defined as:

$$\rho = \frac{\text{Cost}(\text{ALG})}{\text{Cost}(\text{OPT})}$$

where:
- $\text{Cost}(\text{ALG})$ is the total cost incurred by the online algorithm
- $\text{Cost}(\text{OPT})$ is the cost of the optimal offline solution (which knows the entire input sequence in advance)

An algorithm is said to achieve **competitive ratio** $\rho$ if, for all possible input sequences, the ratio of its cost to the optimal cost is at most $\rho$.

### Context: Online Algorithms

The competitive ratio arises naturally in **online algorithmic problems** where decisions must be made without knowledge of future requests. Examples include:
- Caching/paging decisions
- Server maintenance scheduling
- Geometric online problems (e.g., point location in response to adversarially chosen requests)
- Finance and portfolio management

## Key Equations

For an algorithm ALG with cost accumulation across $n$ rounds:

$$\text{Cost}_{\text{ALG}}(X_1, X_2, \ldots, X_n) = \sum_{i=0}^{n-1} |P_i P_{i+1}|$$

where $P_i$ is the algorithm's response to request $X_i$.

The competitive ratio on a prefix of the input is:

$$\rho_i = \frac{\sum_{j=0}^{i-1} |P_j P_{j+1}|}{\text{OPT}(X_1, \ldots, X_i)}$$

### MaxHedge Algorithm Definition

For an algorithm designed to achieve a target competitive ratio $\rho$, the response at round $i$ is positioned such that:

$$|Z_{i-1}Z_i| = \rho(o_i - o_{i-1})$$

where:
- $Z_i$ is the algorithm's response point at round $i$
- $o_i = \text{OPT}(X_i)$ is the optimal cost for the first $i$ requests
- The new point $Z_i$ lies on the intersection of a halfline from $T_i$ and a circle of radius $\rho(o_i - o_{i-1})$ centered at $Z_{i-1}$

## Physical Intuition / Derivation

### Why Competitive Ratio Matters

The competitive ratio quantifies the **price of not knowing the future**. Key insights:

1. **Lower bound on ignorance**: No online algorithm can do better than some competitive ratio $\rho^*$ on adversarially chosen inputs. This ratio represents the fundamental hardness of the problem.

2. **Algorithm validation**: An algorithm that achieves competitive ratio $\rho$ provides a guarantee: "I am never more than $\rho$ times worse than the best possible solution."

3. **Problem difficulty comparison**: Problems with small achievable competitive ratios (e.g., $\rho = 2$) are "easier" than those requiring large ratios (e.g., $\rho = O(\log n)$).

### MaxHedge Intuition

The MaxHedge algorithm embodies a **maximal hedging strategy**:

- At each decision point, it prepares as aggressively as possible for the next request (moving towards the anticipated future direction)
- **Without violating the target competitive ratio constraint**: the movement is constrained so that the cumulative cost stays within ratio $\rho$ of optimal
- The geometric constraint ($|Z_{i-1}Z_i| = \rho(o_i - o_{i-1})$) ensures that the algorithm's **incremental cost at round $i$** matches exactly what a $\rho$-competitive solution would require
- If MaxHedge "fails" (the geometric constraint cannot be satisfied), it means no algorithm can achieve ratio $\rho$ on that input

### Optimality Claim

The claim that **the optimal online algorithm is MaxHedge with the smallest $\rho$ that succeeds** follows from:

1. **Inductively**, MaxHedge maintains exactly $\rho$-competitiveness on every prefix
2. **Greedily**, it maximizes hedging (movement toward future requests) subject to the ratio constraint
3. **Adversarially**, any deviation would either exceed ratio $\rho$ or fail to prepare adequately for worst-case inputs

## Applications in Engineering

### 1. **Cache Management & Memory Hierarchies**
Competitive ratio analysis determines how much larger a cache must be to approximate the performance of an omniscient cache manager. A competitive ratio of 2 means a practical cache need only be twice the size of an optimal cache.

### 2. **Load Balancing & Server Management**
In distributed systems, online algorithms must assign incoming jobs to servers without knowing future arrivals. The competitive ratio bounds how much load balancing degrades versus offline optimal assignment.

### 3. **Facility Location & Maintenance Scheduling**
When maintenance decisions must be made online (e.g., robot repositioning, vehicle routing), competitive ratio analysis quantifies the cost of not knowing future service requests.

### 4. **Algorithmic Robotics**
Robot navigation in unknown environments uses competitive ratio bounds to guarantee that online path-planning is within a factor $\rho$ of the best path an omniscient planner could find.

### 5. **Financial Algorithms**
Online trading algorithms are evaluated by their competitive ratio relative to the best-possible offline trades (where the investor knows all future prices).

### 6. **Network Routing**
Online routing protocols are analyzed by their competitive ratio: how much worse is online rerouting compared to routing with full network knowledge?

## Common Mistakes / Pitfalls

### 1. **Confusing Competitive Ratio with Approximation Ratio**
- **Mistake**: Treating $\rho$ as an approximation guarantee for a single input instance.
- **Reality**: $\rho$ is a **worst-case bound across all input sequences**. A single instance might be solved optimally ($\rho = 1$), while adversarial instances achieve $\r