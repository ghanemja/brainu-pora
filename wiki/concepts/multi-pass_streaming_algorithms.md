# multi-pass streaming algorithms

## Definition

A **multi-pass streaming algorithm** is a computational algorithm that processes an input sequence (or constraint instance) **multiple times** in a fixed sequential order, with the constraint that the algorithm maintains limited working memory (space) at any point in time.

In the context of **streaming constraint satisfaction problems (CSPs)**, a $p$-pass algorithm:
- Receives constraints of an instance sequentially
- Makes exactly $p$ complete passes over the input in a predetermined order
- Maintains memory bounded by some function of the input size
- Aims to compute or approximate a solution (e.g., maximum fraction of satisfiable constraints)

**Formal Model:**
Given a CSP instance $I = (V, C)$ with $|V| = n$ variables and $|C| = m$ constraints, a $p$-pass streaming algorithm:
1. Reads constraints $C_1, C_2, \ldots, C_m$ sequentially
2. May maintain state/sketch of size $S(n, p)$ bits
3. Repeats this process for $p$ passes
4. Outputs an assignment or approximate solution

## Key Equations

### Approximation Ratio vs. Space Trade-off

For a CSP family $F$ with LP-based threshold $\alpha_{\text{LP}}$:

$$\text{Approximation Ratio} = \alpha_{\text{LP}} - \varepsilon \implies S(n, p) = O(\text{polylog } n)$$

$$\text{Approximation Ratio} = \alpha_{\text{LP}} + \varepsilon \implies S(n, p) = \Omega\left(\frac{\sqrt{n}}{p}\right)$$

This represents the fundamental **space-approximation frontier**.

### General Lower Bound (Few Passes)

For $p = o(\log n)$:

$$S(n, p) = \Omega\left(n \cdot 2^{-O_\varepsilon(p)}\right)$$

This exponential decay in passes reflects the power of multiple sequential readings.

### Max-Cut on Bounded-Degree Instances

For certain CSPs (e.g., max-cut), achieving approximation better than $1/2 + \varepsilon$ requires:

$$S(n, p) = \Omega_\varepsilon(\sqrt{n})$$

independent of the number of passes (in the single-pass regime).

## Physical Intuition / Derivation

### Why Multiple Passes Help

Think of a streaming CSP as reading a long list of constraints one-by-one with limited scratch paper:

- **Single pass ($p=1$):** You see each constraint once. To approximate the solution, you must decide immediately whether to tentatively satisfy it, storing minimal state about decisions made.
  
- **Multiple passes ($p>1$):** You revisit the constraints, refining your solution. After pass 1, you have approximate knowledge of which variables appear frequently or in conflicting constraints. In pass 2, you can make better-informed decisions.

### The Information-Theoretic Bottleneck

The space lower bounds arise from an **information-theoretic argument:**

1. The input has $m$ constraints, but you have only $S$ bits of memory
2. After $p$ passes, you can distinguish between roughly $2^{S \cdot p}$ different "states" of the problem
3. Different constraint orderings may force the same memory configuration to produce different decisions
4. To approximate to within $\alpha_{\text{LP}} + \varepsilon$, you need to distinguish between sufficiently different problem instances
5. This requires $S \cdot p \gtrsim \log(\text{number of hard instances})$, which scales with $\sqrt{n}$

### Connection to Linear Programming

The constant $\alpha_{\text{LP}}$ is defined by the **basic linear program relaxation** of the CSP:

$$\max_{x \in [0,1]^{|V|}} \sum_{i=1}^{m} \mathbb{E}_{a \sim \text{constraint}_i}[f_i(a)]$$

Key insight: Polylogarithmic-space, constant-pass algorithms **cannot exceed** $\alpha_{\text{LP}}$—they hit a computational barrier even with unlimited passes and memory, unless $P=NP$.

## Applications in Engineering

### 1. **Distributed Data Processing**
- **MapReduce / Spark frameworks:** Multiple passes correspond to multiple stages of computation
- Trade-off between communication rounds (passes) and node memory (space)
- Optimal number of passes determined by space-approximation frontier

### 2. **Network Monitoring & Analytics**
- Constraint satisfaction arises in flow assignment, load balancing, link scheduling
- Streaming CSP algorithms process arriving network packets/events
- Multiple passes = multiple epochs of network observation
- Memory ↔ approximation quality determines sampling rate for QoS monitoring

### 3. **Approximate Database Query Processing**
- Constraints model join predicates, filter conditions
- Multi-pass streaming processes records sequentially
- Limited buffer memory (in DBMS) constrains approximation ratio of query results

### 4. **SAT/MaxSAT Solvers with Limited Memory**
- Streaming CSPs formalize approximate solving under memory constraints
- Multiple passes enable refinement of variable assignments
- Used in embedded systems, IoT, and hardware-accelerated solvers

### 5. **Signal Processing & Compressed Sensing**
- Streaming over time-series sensor data
- Each pass = processing new blocks of measurements
- Space-bounded sketches maintain compressed representation of signal

## Common Mistakes / Pitfalls

### 1. **Confusing $p$ passes with $p$ copies of memory**
   - **Wrong:** "With $p$ passes and memory $S$, I have $p \cdot S$ total memory."
   - **Right:** You have $S$ memory at each point in time, reused across passes. Total time×space product is $O(pS)$, not additive.

### 2. **Assuming more passes always help arbitrarily**
   - The improvement from extra passes follows $1/p$ scaling: doubling passes only gains $\sqrt{2}\times$ in space
   - Eventually hits problem-dependent barriers (e.g., $\alpha_{\text{LP}}$ threshold)
   - Not all problems benefit equally from more passes