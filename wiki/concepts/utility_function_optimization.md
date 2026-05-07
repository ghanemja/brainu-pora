# Utility Function Optimization

## Definition

**Utility function optimization** is the process of finding scheduling or allocation decisions that maximize a measure of satisfaction or benefit, typically represented as a scalar utility function that quantifies agent preferences over outcomes.

In the context of multi-agent scheduling, utility function optimization addresses the problem where:
- Each agent $i$ has a utility function $u_i(C_i)$ that depends on their job completion time $C_i$
- Utilities are **time-dependent**: they decrease as completion time increases (agent dissatisfaction grows with delay)
- The goal is to find a schedule that optimizes a system-level objective derived from individual utilities

### Formal Problem Statement

Given $n$ jobs assigned to $n$ self-interested agents on a single machine:
- Job $i$ has processing time $p_i$
- Agent $i$ has utility function $u_i(C_i)$ where $C_i$ is completion time
- Typical form: $u_i(C_i) = a_i - b_i \cdot C_i$ (linear, decreasing in $C_i$)

**Optimization objectives:**
1. **Maximin fairness**: $\max_{\text{schedule}} \min_i u_i(C_i)$ — maximize the worst-off agent's utility
2. **Utilitarian efficiency**: $\max_{\text{schedule}} \sum_i u_i(C_i)$ — maximize total system utility

## Key Equations

### Linear Utility Functions
$$u_i(C_i) = a_i - b_i \cdot C_i$$

where:
- $a_i$ = utility intercept (maximum possible utility for agent $i$)
- $b_i$ = utility slope (rate of utility decrease per unit time)
- $b_i > 0$ ensures utility decreases with completion time

### Schedule Completion Times
For a given permutation $\pi$ of jobs:
$$C_{\pi(j)} = \sum_{k=1}^{j} p_{\pi(k)}$$

The completion time of job in position $j$ equals cumulative processing time up to position $j$.

### Fairness Objective (Maximin)
$$\text{OPT}_{\text{fair}} = \max_{\pi} \min_{i \in [n]} \left(a_i - b_i \sum_{k=1}^{j_i} p_{\pi(k)}\right)$$

where $j_i$ is the position of agent $i$'s job in schedule $\pi$.

### Efficiency Objective (Utilitarian)
$$\text{OPT}_{\text{eff}} = \max_{\pi} \sum_{i=1}^{n} \left(a_i - b_i \sum_{k=1}^{j_i} p_{\pi(k)}\right)$$

## Physical Intuition / Derivation

### Why Utility Decreases with Completion Time

Consider a delivery service scheduling system:
- Agent $i$ wants their package delivered as early as possible
- Each unit of delay reduces satisfaction: waiting costs accumulate
- Linear utility captures: "my satisfaction decreases by $b_i$ units per hour of delay"
- The intercept $a_i$ represents baseline satisfaction if served immediately

### The Fairness vs. Efficiency Tension

**Maximin fairness** prioritizes protecting the worst-off agent:
- Schedule tends to prioritize "impatient" agents (high $b_i$) early
- May sacrifice total system utility to ensure no agent is extremely unhappy
- Egalitarian approach: "nobody should suffer unnecessarily"

**Utilitarian efficiency** maximizes aggregate satisfaction:
- May tolerate one agent's significant dissatisfaction if overall utility increases
- Implies: agent with low $b_i$ (patient) should wait longer than agent with high $b_i$ (impatient)
- Natural alignment with "weighted shortest job first" in many cases

### Binary Search for Maximin Solution

To find maximum minimum utility $\lambda^*$:

1. **Binary search over** $\lambda \in [0, \max_i a_i]$
2. **For each candidate** $\lambda$: Check if schedule exists where $u_i(C_i) \geq \lambda$ for all $i$
3. **Constraint transformation**: $a_i - b_i C_i \geq \lambda$ becomes $C_i \leq \frac{a_i - \lambda}{b_i}$
4. **Feasibility check**: Can we order jobs respecting deadline $D_i = \frac{a_i - \lambda}{b_i}$ for each agent?

This reduces to a **scheduling problem with deadlines** (polynomial solvable in many variants).

## Applications in Engineering

### 1. Cloud Computing & Batch Job Scheduling
- Heterogeneous users with different patience levels for computation completion
- Cloud provider maximizes fairness: all users experience acceptable response times
- Trade-off: Serve impatient users (high $b_i$) first vs. efficiency (balance load)

### 2. Manufacturing & Production Scheduling
- Multiple production orders from different clients
- Client $i$ has penalty cost proportional to delay: $u_i = \text{contract value} - \text{delay penalty}$
- Optimize schedule to maintain fairness across clients (no client excessively delayed)

### 3. Healthcare Operations
- Patients arrive with different urgency levels (parameterized by $b_i$)
- Operating room scheduling optimizes both fairness (no patient waits unreasonably) and efficiency
- Emergency patients have high $b_i$; elective procedures have lower $b_i$

### 4. Auction & Mechanism Design
- Bidders (agents) have time-sensitive valuations
- Utility functions encode: how much value decreases if their request is fulfilled later
- Auctioneer chooses allocation order to maximize fairness or total revenue

### 5. Transportation & Logistics
- Delivery routes for multiple customers
- Each customer's utility decreases with delivery delay
- Real-world: Amazon, UPS optimize for fairness (no customer wildly delayed) + efficiency

## Common Mistakes / Pitfalls

### 1. **Confusing Maximin with Minimax**
- **Maximin**: $\max \min u_