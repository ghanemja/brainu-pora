# MaxMinGreedy Algorithm

## Definition

MaxMinGreedy is a greedy scheduling algorithm for single-machine job sequencing problems that optimizes a *fairness* objective. Specifically, it solves the problem $1|u_j|\umin$ (single machine, utility-based objective, maximize minimum utility) by constructing a schedule backward in time, greedily selecting at each step the job with the highest utility at the current completion time.

**Formal Problem Statement:**
Given a set of $n$ jobs $\{J_1, \ldots, J_n\}$ with:
- Processing times $p_j > 0$ for each job $j$
- Non-increasing utility functions $u_j(C_j)$ where $C_j$ is the completion time of job $j$

The goal is to find a permutation (schedule) $\pi$ that maximizes the minimum utility achieved by any job:
$$\max_{\pi} \min_{j \in J} u_j(C_j^\pi)$$

## Algorithm Description

**Input:** Job set $J$, processing times $\{p_j\}$, utility functions $\{u_j\}$

**Output:** Permutation $\pi = (\pi_1, \ldots, \pi_n)$ representing job sequence

**Pseudocode:**

```
T := Σ_j p_j                          // Total processing time
for i = n downto 1 do
    k := arg max{u_j(T) : j ∈ J}      // Job with highest utility at time T
    π_i := k                           // Schedule job k at position i
    T := T - p_k                       // Decrease available time
    J := J \ {k}                       // Remove scheduled job
end for
```

**Key Insight:** The algorithm works *backward* from the makespan. At each step, it assigns the job that maximizes utility at the current "effective completion time," implicitly ensuring the minimum utility is as large as possible.

## Key Equations

**Completion Time Relationship:**
If job $j$ is scheduled at position $i$ in the sequence, its completion time is:
$$C_j = \sum_{k \in \text{jobs scheduled at positions} \leq i} p_k$$

**Optimality Criterion (Theorem 2):**
For any non-increasing utility functions $u_j(C_j)$, MaxMinGreedy is optimal for problem $1|u_j|u_{\min}$ with time complexity $O(n^2)$.

**Implicit Binary Search Connection:**
The algorithm implicitly solves: "What is the maximum utility threshold $u^*$ such that all jobs can achieve utility $\geq u^*$?"

This is equivalent to finding:
$$u^* = \max\{u_T : \text{there exists a feasible schedule where } C_j \leq d_j^T \text{ for all } j\}$$

where $d_j^T = u_j^{-1}(u_T)$ are the "due dates" corresponding to utility threshold $u_T$.

## Physical Intuition / Derivation

### Why Backward Construction?

Consider the optimization goal: maximize the *minimum* utility. This is a **max-min** fairness problem. The backward construction has an elegant interpretation:

1. **Exchange Argument:** Suppose jobs are scheduled in some order. If we swap adjacent jobs $i$ and $j$ (where $i$ is processed before $j$), job $i$'s completion time *decreases* while job $j$'s increases. Since utilities are non-increasing in completion time:
   - $u_i$ increases (completes earlier → higher utility)
   - $u_j$ decreases (completes later → lower utility)

2. **Fairness Principle:** To maximize the minimum, we should prioritize jobs that would otherwise suffer the most. Jobs scheduled last (with earliest completion times) are naturally favored. By working backward, we greedily assign the "rightmost" position to jobs that benefit most.

3. **Greedy Selection:** At each step, if we haven't scheduled jobs, the remaining jobs will complete at time $T$ (the sum of unscheduled job durations). The job with highest utility at time $T$ should be scheduled now—delaying it would only hurt it more (since utility is non-increasing).

### Why Non-Increasing Utilities?

The non-increasing assumption is critical: it ensures that completing a job earlier is always better or equal. This aligns with intuitive fairness: shorter completion times should yield higher satisfaction/utility across all jobs.

## Applications in Engineering

### 1. **Workflow Scheduling with QoS Constraints**
In cloud computing and distributed systems, jobs have quality-of-service (QoS) targets represented as utility functions. MaxMinGreedy ensures fair resource allocation where the worst-off job achieves maximum possible utility.

### 2. **Manufacturing & Job Shop Scheduling**
Single-machine environments (e.g., CNC machine tool centers) process jobs with customer satisfaction metrics inversely tied to completion time. MaxMinGreedy optimizes worst-case customer satisfaction.

### 3. **Real-Time Systems**
Scheduling periodic or aperiodic real-time tasks where utility degrades with deadline miss (e.g., $u_j(C_j) = \max(0, 1 - (C_j - d_j)/d_j)$). Backward scheduling maximizes the minimum hard-real-time satisfaction.

### 4. **Fair Resource Allocation (Data Centers)**
MapReduce and Spark clusters use fairness scheduling to prevent task starvation. MaxMinGreedy principles underpin fair-share schedulers minimizing the slowest job's completion time relative to its utility target.

### 5. **Energy & Power Systems**
In microgrid dispatch problems, jobs represent loads with time-dependent penalties. Backward scheduling with utility = -(delay cost) minimizes maximum delay penalty.

## Key Theorems & Complexity Results

### **Theorem 1 (Optimality - No Release Dates)**
If all jobs are available from time 0 and $u_j$ are non-increasing functions of completion time $C_j$, then MaxMinGreedy computes an optimal solution to $1|u_j|u_{\min}$ in $O(n^2)$ time.

**Proof Sketch:** Any swap of adjacent jobs in the