# High probability bounds

## Definition

A **high probability bound** is a probabilistic guarantee that an event occurs with probability at least $1 - \frac{1}{n^C}$, where $n$ is a problem size parameter and $C$ is an arbitrary positive constant that can be made arbitrarily large through careful choice of problem-dependent constants.

Formally, a random event $\mathcal{E}$ occurs **with high probability (w.h.p.)** if:
$$\Pr[\mathcal{E}] \geq 1 - \frac{1}{n^C}$$

The term "with high probability" is a standard shorthand in algorithm analysis and probabilistic methods, meaning the failure probability vanishes faster than any polynomial in the problem size as $n \to \infty$.

## Key Equations

### High Probability Event Definition
$$\Pr[\text{event holds}] \geq 1 - \frac{1}{n^C}, \quad C \text{ arbitrarily large}$$

### Failure Probability
$$\Pr[\text{event fails}] \leq \frac{1}{n^C}$$

### Typical Application (from source material)
For path survival probability under random deletion with threshold $i \geq C \frac{\ln n |P|}{\text{val}(u,v)}$:
$$\Pr[\text{path } u \leadsto v \text{ survives in } G \setminus X] \leq n^{-C}$$

## Physical Intuition / Derivation

### Why High Probability Matters

High probability bounds are fundamental in the analysis of randomized algorithms because they provide **asymptotic guarantees that hold for all sufficiently large problem instances**. Unlike simple probabilistic bounds, w.h.p. statements mean:

1. **Failure is vanishingly rare**: As $n$ grows, even tiny failure probabilities become astronomically unlikely. For example, $n^{-10}$ becomes negligible at $n = 10^6$.

2. **Constant can be amplified**: The beauty of w.h.p. bounds is that by increasing hidden constants (through repeated trials, better analysis, or refined algorithms), you can make the failure probability as small as you need—the dependence on $n$ remains polynomial.

3. **Union bound compatibility**: When you have many events that each hold w.h.p., you can often union-bound over them while maintaining a w.h.p. guarantee on their conjunction. If you have $\text{poly}(n)$ events, each failing with probability $\le n^{-C}$ where $C$ is large enough, then with high probability *all* events succeed.

### Building a High Probability Argument

A typical derivation involves:

1. **Identify the failure event**: What could go wrong? (e.g., a path gets deleted)
2. **Bound its probability**: Show failure probability $\le n^{-C}$ for some $C$
3. **Union over all relevant cases**: If there are $\text{poly}(n)$ cases (e.g., $|P|$ pairs, $n^3$ paths), union bound gives:
$$\Pr[\text{any case fails}] \leq |P| \cdot n^{-C'} \leq \text{poly}(n) \cdot n^{-C'} = n^{-C}$$
for appropriately chosen $C' > C + \log n$.

4. **Adjust constants**: The implicit constant in $\tilde{O}$ or $\tilde{\Omega}$ notation absorbs the necessary tweaks to maintain w.h.p.

## Applications in Engineering

### Network and Routing Algorithms
- **Path reliability**: Proving that critical communication paths survive random link failures w.h.p.
- **Load balancing**: Showing that randomized load distribution achieves near-optimal utilization w.h.p.
- **Flow decomposition**: In fractional flow problems (as in source material), guaranteeing bottleneck pairs exist with high probability for progress bounds.

### Randomized Data Structures
- **Hash tables**: Proving collision-free or collision-bounded performance w.h.p. under random hashing
- **Skip lists**: Demonstrating logarithmic search time w.h.p. despite randomized level assignments
- **Bloom filters**: Bounding false positive rates that vanish as filter size grows

### Distributed Computing
- **Consensus protocols**: Ensuring Byzantine agreement succeeds w.h.p. despite adversarial delays
- **Peer-to-peer systems**: Guaranteeing network connectivity and message delivery w.h.p. in highly dynamic networks
- **Parallel algorithms**: Analyzing work distribution when jobs are assigned randomly to processors

### Machine Learning and Sampling
- **Statistical learning**: Proving generalization bounds w.h.p. via concentration inequalities
- **Monte Carlo methods**: Showing algorithm output converges to true answer w.h.p. as sample size grows
- **Randomized sketching**: Guaranteeing dimensionality reduction preserves distances w.h.p.

### Graph Algorithms (as in source)
- **Cut decomposition**: Decomposing flow into paths; bounding round complexity w.h.p.
- **Fractional packing**: Finding high-value path pairs w.h.p. to charge against fractional solutions

## Common Mistakes / Pitfalls

### 1. Confusing "High Probability" with "Deterministic Guarantee"
**Error**: Treating w.h.p. bounds as absolute guarantees.  
**Reality**: There is a (vanishing) failure probability. For safety-critical applications, you may need derandomization.

### 2. Forgetting to Union Bound Over Cases
**Error**: Proving one event holds w.h.p., then claiming all poly$(n)$ cases hold w.h.p. without adjustment.  
**Reality**: You must either prove a single event w.h.p. that covers all cases, or union-bound carefully, increasing the constant $C$.

### 3. Misunderstanding the Role of $C$
**Error**: Treating $C$ as fixed; building an argument that breaks if $C$ is large.  
**Reality**: $C$ is a parameter under your control. By pushing constants high enough, you can make failure arbitrarily unlikely.

### 4. Sloppiness with Hidden Constants
**Error**: Using $\tilde