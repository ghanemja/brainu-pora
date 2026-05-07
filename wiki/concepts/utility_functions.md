# Utility Functions

## Definition

A **utility function** $u_j$ quantifies the value or benefit derived from executing a task or job $j$ in a scheduling or optimization context. In engineering scheduling problems, utility functions map job-specific attributes (such as completion time, cost, or quality metrics) to a scalar utility value that represents preference or satisfaction.

**Formal characterization:**
- A utility function $u_j$ is typically a function of the completion time $C_j$ of job $j$
- In the canonical form: $u_j = b_j - a_j C_j$ where:
  - $b_j$ = base utility or intrinsic value of job $j$
  - $a_j$ = cost coefficient (penalty per unit completion time)
  - $C_j$ = completion time of job $j$
- A utility function is **non-increasing** if its value monotonically decreases with later completion times (i.e., $\frac{du_j}{dC_j} \leq 0$)

The general framework assumes utility functions are **continuous** and can be evaluated in constant time.

## Key Equations

**Linear utility model (most common):**
$$u_j = b_j - a_j C_j$$

**Aggregate utility objectives:**

Minimize worst-case utility (bottleneck objective):
$$f = u_{\min} = \min_j u_j$$

Maximize total utility (sum objective):
$$f = \sum_j u_j$$

**Example parameterizations:**
- Fixed base value: $u_j = \tilde{b}_j - a_j C_j$ (where $\tilde{b}_j$ is parameter)
- Fixed penalty rate: $u_j = b_j - \tilde{a}_j C_j$ (where $\tilde{a}_j$ is parameter)
- Both fixed: $u_j = \tilde{b}_j - \tilde{a}_j C_j$

## Physical Intuition / Derivation

**Why utility functions matter:**

In real-world scheduling, not all jobs contribute equally to system objectives. A utility function captures the trade-off between:
1. **Intrinsic value** ($b_j$): How important is this job? Does it generate revenue, ensure safety, or deliver customer value?
2. **Time sensitivity** ($a_j$): How much does lateness degrade value? A perishable product loses value rapidly; a batch processing task may be time-insensitive.

**Motivating example:**
Consider scheduling urgent medical procedures and routine maintenance:
- Urgent surgery: high $b_j$, high $a_j$ (loses value quickly if delayed)
- Equipment maintenance: lower $b_j$, lower $a_j$ (flexible deadline)

The utility function allows expressing this heterogeneity in a unified mathematical framework.

**Why non-increasing?**

Non-increasing utility functions reflect reality: delaying a job's completion cannot improve its value. This constraint is fundamental to making scheduling problems well-posed.

**Aggregation objectives:**

- **Minimizing $u_{\min}$** (bottleneck/max-min fairness): Ensures the worst-off job achieves acceptable utility. Useful for fairness-critical systems.
- **Maximizing $\sum u_j$** (utilitarian): Optimizes total system utility. Computationally harder but yields higher aggregate value.

## Applications in Engineering

### 1. **Scheduling and Resource Allocation**
- **Job shop scheduling**: Assign jobs to machines while maximizing user satisfaction or ensuring minimum service levels
- **Single-machine scheduling**: Order tasks to optimize utility-based objectives rather than classical metrics (makespan, tardiness)

### 2. **Cloud Computing & Task Scheduling**
- Assign computational tasks with varying priorities and time-sensitivity to servers
- Ensure SLA (Service Level Agreement) compliance by maintaining minimum utility thresholds

### 3. **Supply Chain & Manufacturing**
- Schedule production runs for products with different profit margins ($b_j$) and demand urgency ($a_j$)
- Balance high-margin, time-sensitive orders against routine batch production

### 4. **Maintenance Planning**
- Prioritize equipment maintenance tasks based on operational risk (high $b_j$) and degradation rate (high $a_j$)
- Optimize resource allocation for preventive vs. corrective maintenance

### 5. **Telecommunications & Network Scheduling**
- Schedule packet transmission with variable service priorities and deadline penalties
- Ensure quality-of-service (QoS) guarantees through utility-constrained scheduling

### 6. **Project Management**
- Weight project tasks by strategic importance ($b_j$) and schedule sensitivity ($a_j$)
- Allocate limited resources to maximize overall project value delivery

## Common Mistakes / Pitfalls

### 1. **Confusing utility with cost/time**
Students often treat utility as a minimization objective (like lateness). Remember: utility is typically *maximized*; higher utility = better outcome. The linear form $u_j = b_j - a_j C_j$ is a *benefit minus cost* structure, not a pure cost.

### 2. **Assuming all parameters are simultaneously variable**
The source material distinguishes between:
- **General problem**: All $b_j$ and $a_j$ are decision variables or parameters to optimize
- **Fixed parameters**: Some values are given ($\tilde{b}_j$, $\tilde{a}_j$). Not all variants are well-posed (e.g., the note on Problem 1 that $1|\sigma_{\text{SYS}} = \sigma_T, u_j = \tilde{b}_j - a_j C_j | \sum \tilde{b}_j$ is "not meaningful")

This distinction is critical: fixing certain parameters may eliminate degrees of freedom, making the problem trivial or infeasible.

### 3. **Ignoring continuity assumptions**
The algorithms assume utility functions can be evaluated in constant time and are continuous. Discrete utility functions require different algorithmic approaches (e.g., dynamic programming instead of greedy methods).

### 4. **Misapplying aggregation objectives**
- $u_{\min}$ (bottleneck) is computationally *easier* (often polynomial) but may waste total utility by over-protecting the worst job
- $\sum u_j$ (sum) is computationally *harder* (often