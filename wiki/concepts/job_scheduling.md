# Job Scheduling

## Definition

**Job scheduling** is the problem of determining an optimal ordering (permutation) of jobs on a single machine to optimize an objective function. In its most general form denoted $1|r_j, u_j|f$, we seek to schedule $n$ jobs $\{J_1, J_2, \ldots, J_n\}$ such that:

- Each job $j$ has a **processing time** $p_j$ (duration to complete)
- Each job $j$ may have a **release date** $r_j$ (earliest time it can start)
- Each job $j$ has a **utility function** $u_j(C_j)$ that depends on its completion time $C_j$
- We optimize an aggregate objective function $f$ over all job utilities

A **schedule** is a permutation $\pi = (\pi_1, \pi_2, \ldots, \pi_n)$ specifying the order in which jobs execute. The completion time of job $\pi_i$ in position $i$ is:

$$C_{\pi_i} = \sum_{k=1}^{i} p_{\pi_k}$$

The most common fairness objective is **maximize minimum utility**:

$$\text{maximize } u_{\min} = \min_{j \in J} u_j(C_j)$$

## Key Equations

### Utility Function Relationship

For a target utility level $u_T$, the equivalent **due date** for job $j$ is:

$$d_j^T = u_j^{-1}(u_T)$$

This transforms the utility maximization problem into a due-date feasibility problem: find the maximum $u_T$ such that there exists a schedule where all jobs meet their due dates (maximum lateness $\leq 0$).

### Completion Time Formula

For a schedule $\pi$ starting at time $t_0$ (or $t_0 = 0$ if no release dates):

$$C_j = t_0 + \sum_{i: \pi_i \text{ scheduled before } j} p_{\pi_i} + p_j$$

### Total Processing Time

$$P = \sum_{j=1}^{n} p_j$$

## Physical Intuition / Derivation

### The Core Challenge

Job scheduling balances a fundamental tension: **later jobs have later completion times**, which typically decreases their utility. When utility functions are non-increasing in completion time (common in real systems—users prefer faster service), scheduling a job earlier benefits that job but delays all subsequent jobs.

### MaxMinGreedy Algorithm

The provided algorithm builds schedules **backwards in time**:

1. Start with total slack time $T = \sum_j p_j$
2. Place jobs from position $n$ down to position 1
3. At each step, greedily select the job with **highest marginal utility** at the current time window
4. This is equivalent to: "which job loses the least utility by being pushed to this later position?"

**Why backwards?** By working backwards, we implicitly compute when each job finishes and can evaluate $u_j(C_j)$ correctly.

### Computational Complexity Results

**Without release dates** ($1|u_j|u_{\min}$): 
- MaxMinGreedy achieves optimal in $O(n^2)$ time (Theorem 2)
- This works because we can always rearrange jobs to satisfy non-increasing utilities

**With arbitrary release dates** ($1|r_j, u_j|u_{\min}$):
- **Strongly NP-hard** in the general case (Theorem 3)
- **Weakly NP-hard** even if only one job has $r_j > 0$ (Theorem 4)
- Weakly NP-hard admits pseudo-polynomial dynamic programming solution

The introduction of release dates breaks the greedy solution's optimality because the machine may be idle waiting for a released job, and decisions become interdependent.

## Applications in Engineering

### 1. **Manufacturing & Production Scheduling**
- Sequence operations on a CNC machine or assembly line
- Jobs = parts to manufacture; processing time = operation duration
- Utilities could model customer satisfaction (delivery deadline) or revenue (expedited orders worth more)

### 2. **Cloud Computing & Task Scheduling**
- Single-core processor or shared resource scheduling
- Jobs = computational tasks; $p_j$ = CPU time needed
- Utilities model fairness across users or service-level agreements (SLAs)

### 3. **Project Management**
- Schedule tasks on a critical path with non-linear penalties for delays
- Release dates model task dependencies
- Utility = penalty function for missing deadlines

### 4. **Emergency Room Triage**
- Schedule patient procedures on limited operating theaters
- Processing time = surgery duration
- Utility = clinical priority (non-increasing with wait time)
- Release dates = when patients arrive/stabilize

### 5. **Batch Job Scheduling in HPC**
- Allocate cycles in a supercomputer queue
- Jobs with different resource requirements and priorities
- Fairness objective ensures no user's job waits indefinitely

## Common Mistakes / Pitfalls

### 1. **Assuming Shortest-Job-First is Optimal**
❌ **Wrong**: Scheduling shorter jobs first maximizes fairness
✓ **Correct**: Only optimal if all utilities are identical. With heterogeneous non-increasing utilities, you need MaxMinGreedy or equivalent algorithm.

### 2. **Ignoring the Direction of Optimization**
❌ **Wrong**: Computing completion times from job 1 onward without considering utility direction
✓ **Correct**: Work backwards (as MaxMinGreedy does) to properly account for how pushing a job later affects its utility

### 3. **Confusing Weakly vs. Strongly NP-hard**
❌ **Wrong**: Release dates make the problem intractable with no approximation hope
✓ **Correct**: Weakly NP-hard = pseudo-polynomial DP exists (acceptable for moderate $P = \sum p_j$); strongly NP-hard = no such algorithm

### 4. **Forgetting the Non-Increasing Constraint**
- MaxMinGreedy optimality requires $u_j(C)$ to be **non-increasing** in $C$
- If utilities increase with completion time (e.g., "later is better"