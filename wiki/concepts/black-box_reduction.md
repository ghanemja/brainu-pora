# black-box reduction

## Definition

A **black-box reduction** is a compositional framework that allows solving a complex problem by treating simpler subproblems as modular, interchangeable components without requiring knowledge of their internal implementation. In the context of replicability and multi-instance learning, a black-box reduction takes an algorithm $\mathcal{A}$ that solves a single instance of problem $T$ and directly composes it to solve $k$ independent (or nearly independent) instances, achieving favorable sample complexity scaling.

Formally, given:
- $k$ independent problem instances $T_1, T_2, \ldots, T_k$
- A $\rho$-replicable algorithm for single instances with sample complexity $n$

A black-box reduction produces a $\rho$-replicable algorithm for all $k$ instances **without requiring redesign of the base algorithm**, achieving sample complexity scaling that is nearly linear in $k$ rather than quadratic.

The key property: the composition mechanism treats each $T_i$ as a "black box," requiring only the interface/guarantees of the single-instance solution, not its internal details.

## Key Equations

**Non-adaptive composition (Theorem 1, informal):**
$$m_{\text{non-adaptive}}(k) = \tilde{O}(nk)$$

where $m(k)$ is total sample complexity for solving $k$ instances, $n$ is single-instance complexity, and $\tilde{O}$ hides logarithmic factors.

**Adaptive composition lower bound (Theorem 3, informal):**
$$m_{\text{adaptive}}(k) = \Omega(nk^2)$$

This establishes the **quadratic separation** between composition strategies:
$$\frac{m_{\text{adaptive}}(k)}{m_{\text{non-adaptive}}(k)} = \Omega(k)$$

## Physical Intuition / Derivation

### Why Black-Box Composition Matters

In problems involving $k$ independent tasks, the naive approach is to run $k$ separate algorithms sequentially or in parallel. If each task requires fresh randomness and samples, and there is no structured way to share information across tasks, one might expect:

$$m_{\text{naive}}(k) = k \cdot n$$

However, if the algorithm must satisfy **replicability**—producing the same output given the same input seed—naive composition can fail:

**The Adaptive Trap:** If later problems depend on outputs of earlier ones (adaptive setting), an adversary can craft a sequence where each decision point branches in ways that force redundant sample consumption. The algorithm must maintain independent replicability at each round, preventing global information sharing that would ordinarily amortize cost.

### How Black-Box Reduction Avoids Quadratic Blowup

The key insight is to **separate the composition strategy from individual algorithm design**:

1. **Modular interface:** Each algorithm $\mathcal{A}_i$ only needs to expose: "given fresh samples from distribution $D_i$, solve problem $T_i$ replicably."

2. **Joint randomness:** The compositor allocates a *shared random seed* across all instances, ensuring that if the same instance is queried twice (same input distribution, same prior outputs), it produces identical results—while different instances naturally get different randomness.

3. **Non-adaptive scheduling:** Since problems are independent, the compositor can determine all $k$ problem specifications upfront, rather than adapting dynamically. This breaks the adversarial feedback loop that forces quadratic cost.

**Intuitive analogy:** 
- **Adaptive composition** = a teacher responding to student questions in real-time, forced to re-explain concepts if a student asks about an earlier topic again (waste).
- **Black-box reduction** = distributing a fixed exam with multiple problems upfront; the grader can use a single answer key across all problems (amortization).

### Why Adaptive Composition Requires $\Omega(nk^2)$

The lower bound (Theorem 3) shows that in an adaptive game:
- An adversary poses $k$ problems sequentially
- Each problem $T_i$ can depend on outputs $y_1, \ldots, y_{i-1}$
- The adversary can force **revisiting earlier distributions**

A replicable algorithm, once it commits to outputting $y_i$ for problem $T_i$ with a given seed, must produce the same $y_i$ if the algorithm's randomness and input are repeated. An adaptive adversary can exploit this by:
- Querying round $i$ with state $s_i$
- Later querying round $j$ (where $j > i$) with a state that forces the algorithm to implicitly recompute round $i$
- Forcing $O(nk)$ samples per round in worst case

This gives $\Omega(nk^2)$ total complexity.

## Applications in Engineering

### 1. Replicable Machine Learning

**Multi-task learning with consistency requirements:**
- Run $k$ independent classification or estimation tasks
- Guarantee that rerunning the entire pipeline with the same random seed produces identical predictions
- **Application:** Regulatory compliance (financial predictions, medical diagnostics) where results must be reproducible and auditable

**Example:** Best-arm identification across $k$ parallel bandits
- Use black-box reduction to solve $k$ independent best-arm problems
- Achieves $\tilde{O}(nk)$ samples (nearly linear in $k$)
- Prior "naive" joint exponential mechanism required $\Omega(nk^2)$

### 2. Distributed Algorithm Design

**Composable subroutines in distributed systems:**
- Build complex distributed protocols by black-box composition of simpler replicable algorithms
- No need to redesign lower-level modules when scaling to more instances
- **Application:** Distributed consensus, replicated state machines (Raft, Paxos variants)

### 3. Differential Privacy & Sensitive Data

**Formal privacy composition theorems:**
- Black-box reductions connect to composition theorems in differential privacy
- Correlated sampling via shared seed maintains privacy budget sublinearly in $k$
- **Application:** Federated learning with formal privacy guarantees across $k$ rounds or $k$ data holders

### 4. Experimental Design & A/B Testing

**Multi-arm bandits at scale:**
- Conduct $k$ parallel A/B tests with replicability guarantees
- Use black-box