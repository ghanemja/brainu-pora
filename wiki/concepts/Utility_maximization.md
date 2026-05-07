# Utility Maximization

## Definition

**Utility maximization** is an optimization principle where a decision-maker (individual agent, system, or scheduler) selects actions or allocates resources to achieve the highest possible value of a utility function. In multi-agent contexts, utility maximization addresses the tension between individual agent satisfaction and system-level objectives through fairness or efficiency criteria.

Formally, given a set of $n$ agents with utility functions $U_i(x)$, utility maximization problems typically pursue one of two complementary objectives:

1. **Fair (minimax) approach**: Maximize the minimum utility
   $$\max_{x} \min_{i=1}^{n} U_i(x)$$

2. **Efficient (utilitarian) approach**: Maximize total utility
   $$\max_{x} \sum_{i=1}^{n} U_i(x)$$

In scheduling contexts, agent $i$ receives utility that depends on job completion time $C_i$, typically with utility **decreasing in completion time** (higher completion time yields lower satisfaction).

## Key Equations

### General Utility Maximization Framework

For an agent with job $i$ completing at time $C_i$:

$$U_i(C_i) = u_i - \alpha_i C_i$$

where $u_i$ is the baseline utility and $\alpha_i > 0$ is the disutility rate (opportunity cost per unit time).

**Fair scheduling objective** (maximin):
$$\text{Fair Solution} = \arg\max_{\text{schedule}} \min_{i \in \{1,\ldots,n\}} U_i(C_i(\text{schedule}))$$

**Efficient scheduling objective** (sum of utilities):
$$\text{Efficient Solution} = \arg\max_{\text{schedule}} \sum_{i=1}^{n} U_i(C_i(\text{schedule}))$$

### Complexity-Dependent Formulations

When utility functions can be adjusted within budget constraints:
$$\max_{u_i, \alpha_i} \min_{i} \{u_i - \alpha_i C_i\}$$
subject to: $\sum_i (u_i + \alpha_i) \leq B$ (budget constraint)

## Physical Intuition / Derivation

### Why Utility Depends on Completion Time

Consider a manufacturing or cloud computing scenario where each agent (customer, department, or application) has a time-sensitive job:
- **Direct cost of waiting**: Agents incur holding costs, opportunity costs, or SLA penalties proportional to how long their job waits
- **Time value of money**: Completing earlier allows the agent to monetize results sooner or avoid downstream bottlenecks
- **Competitive advantage**: In service systems, agents who complete earlier gain market advantage

Thus, utility naturally **decreases linearly with completion time**: $U_i(C_i) = \text{const} - \alpha_i C_i$.

### Fair vs. Efficient Trade-off

In multi-agent systems, these objectives often conflict:

| Objective | Optimizes for | Risk |
|-----------|---------------|------|
| **Fairness** (maximin) | Poorest-off agent | May sacrifice total system performance |
| **Efficiency** (utilitarian) | Total system benefit | Can leave some agents severely disadvantaged |

**Derivation intuition**: 
- Maximin scheduling prioritizes agents with highest disutility rates or longest jobs (to prevent anyone from suffering unbearably long waits)
- Sum-maximization may keep low-priority (low $\alpha_i$) agents waiting indefinitely while serving high-priority ones

### Scheduling Under Constraints

When jobs have **release dates** $r_i$ (earliest start) and **due dates** $d_i$ (target completion), the feasible region shrinks dramatically, making utility maximization NP-hard in the general case but tractable under structural assumptions (e.g., all jobs share identical processing times).

## Applications in Engineering

### 1. **Cloud Computing & Task Scheduling**
- Each user's job (VM, container, data pipeline) has an implicit utility function based on execution time
- Fair scheduling ensures no single user experiences extreme delays
- **Example**: Kubernetes scheduler balancing pod completion times across tenants

### 2. **Manufacturing & Job Shop Scheduling**
- Multiple customer orders, each with disutility proportional to tardiness
- Maximin fairness ensures no customer waits excessively longer than others
- **Example**: Semiconductor fab scheduling balancing across multiple product lines

### 3. **Transportation & Logistics**
- Delivery routes where each customer's utility decreases with delivery time
- Fair routing prevents certain regions from systematic long delays
- **Example**: Last-mile delivery scheduling in urban areas

### 4. **Network Resource Allocation**
- Competing flows with time-sensitive payloads (video streaming, financial transactions)
- Fairness ensures all flows achieve minimum throughput QoS
- **Example**: WFQ (Weighted Fair Queuing) in routers

### 5. **Healthcare Scheduling**
- Patient procedures with time-dependent utility (emergency vs. routine)
- Fair scheduling respects prioritization while avoiding indefinite waits
- **Example**: Operating room scheduling balancing urgent/routine surgeries

### 6. **Auction Design & Mechanism Design**
- Agents bid based on expected utility from winning
- Utility maximization informs pricing and allocation mechanisms
- **Example**: Spectrum auction design for communication networks

## Common Mistakes / Pitfalls

### 1. **Assuming Fairness ≡ Efficiency**
**Mistake**: Believing that fair solutions automatically maximize total utility.
- **Reality**: Maximin fairness often requires **sacrificing** total utility to avoid extreme disparities
- **Impact**: A fair schedule may have 10% lower total utility than the optimal efficient schedule

### 2. **Ignoring Computational Complexity**
**Mistake**: Treating all utility maximization variants as equally solvable.
- **Reality**: General scheduling with arbitrary release dates is **strong NP-hard** (no pseudo-polynomial algorithms), while restricted versions (uniform processing times, single release date) may be polynomial
- **Impact**: Cannot apply the same algorithm to all problem variants

### 3. **Linear Utility Assumptions**
**Mistake**: Assuming all agents have linear utility functions $U_i = \text{const} - \alpha_i C_i$.
- **Reality