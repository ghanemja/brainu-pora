# Randomized algorithm

## Definition

A **randomized algorithm** is a computational procedure that incorporates random choices (via coin tosses, random sampling, or probabilistic selection) during execution. Unlike deterministic algorithms that follow a fixed sequence of steps, randomized algorithms may produce different outputs or execution paths on identical inputs.

Formally, a randomized algorithm $\mathcal{A}$ maps an input instance $I$ to a probability distribution over possible outputs and/or execution traces. The algorithm's performance is characterized by:

- **Expected runtime**: $\mathbb{E}_r[\text{time}(I, r)]$ where $r$ denotes the random choices
- **Expected cost**: $\mathbb{E}_r[\text{cost}(\mathcal{A}(I, r))]$ for optimization problems
- **Success probability**: $\Pr_r[\text{solution}(I, r) \text{ is valid}]$

Randomized algorithms are particularly powerful for **certification problems** (verifying properties of a system by probing/testing elements) and **optimization problems** where random sampling reduces computational burden below deterministic lower bounds.

## Key Equations

### Randomized Probe Selection (Epoch-based)

For the matroid-SBFC problem, Algorithm 1 employs epoch-based probabilistic probing:

$$\text{Pr}[\text{probe element } e \text{ in epoch } \sigma] = \min\left(1, \alpha \sum_{t \leq 2^{\sigma}} x_{e,t}\right)$$

where:
- $x_{e,t}$ is a fractional solution from an LP relaxation
- $\alpha = 4\log n$ is a concentration parameter
- Epochs $\sigma \in \{1, \ldots, \lceil\log_2 n\rceil\}$ enable multi-stage refinement

### Expected Cost Bound

**Lemma 3**: The randomized algorithm achieves expected probing cost:

$$\mathbb{E}[\text{probes}] \leq O(\log n) \cdot \text{cost}(x^*)$$

where $x^*$ is an optimal (or near-optimal) solution to the LP relaxation. This $O(\log n)$ multiplicative factor is fundamental—no deterministic algorithm can do better for worst-case instances.

### Concentration via Second-Moment Method

For random permutations $\pi$ on $[N]$ with a "large" fixed set $T \subseteq [N]$ where $|T| \geq N/2$:

$$\Pr\left(\exists \ell \in T : \varphi(\ell) = \pi(\ell)\right) \geq \frac{1}{4}$$

This ensures that randomization yields useful solutions with bounded probability.

## Physical Intuition / Derivation

### Why Randomization Helps

**Deterministic certification is hard**: To certify that $n$ elements contain a basis of rank $k$, a deterministic adversary can force probing of nearly all elements before confirmation. Randomization breaks this adversarial structure.

**Epoch-based exploration**:
1. **Epoch 1** ($\sigma=1$): Probe each element with probability $\propto x_{e,1}$ (elements most likely active in low time horizons)
2. **Epoch 2** ($\sigma=2$): Probe remaining elements with probability $\propto x_{e,2}$ (elements likely active longer term)
3. **Repeat**: Double the time window each epoch

This **multi-scale strategy** ensures:
- High-probability elements get checked early (low expected cost)
- Low-probability elements are checked with lower probability overall
- Geometric growth of epochs means only $O(\log n)$ rounds needed

### The LP Relaxation Foundation

Rather than solving the discrete combinatorial problem directly (NP-hard in general), we:

1. **Solve LP**: Minimize $\sum_e u_e$ subject to matroid basis constraints (polynomial time via ellipsoid method or interior-point algorithms)
2. **Round probabilistically**: Use LP values $x_{e,t}$ to guide random probe selection
3. **Amplify success**: Run algorithm with concentration parameter $\alpha = 4\log n$ to ensure with high probability a basis is found

The $O(\log n)$ gap between randomized and LP-optimal reflects **integrality gap** inherent to the problem's combinatorial structure.

## Applications in Engineering

### 1. **Network Certification**
- **Spanning tree verification**: Test network links to confirm a connected spanning tree exists
- **Graph matroid**: $M = (U, I)$ where $I$ = acyclic subsets; probing = checking link status
- **Use case**: Minimal spanning tree health monitoring without full network audit

### 2. **Supply Chain / Inventory Systems**
- **k-of-n certification**: Verify that at least $k$ of $n$ suppliers are active/reliable
- **Partition matroid**: Different suppliers grouped by region; need coverage from each region
- **Benefit**: Adaptive testing strategy reduces inspection cost by factor of $\log n$

### 3. **Matrix Rank / Linear Algebra Testing**
- **Matroid-based verification**: Confirm a matrix has rank $k$ by probing entries randomly
- **Graphic matroid specialization**: Test edge connectivity without examining every edge
- **Engineering use**: Structural analysis, finite-element model verification

### 4. **Sensor Networks**
- **Distributed sensing**: Activate sensors probabilistically to cover redundant measurements
- **Cost efficiency**: Randomized scheduling saves power while maintaining confidence in coverage
- **Adaptive strategies**: Updated greedy algorithm selects next sensor based on observations so far

### 5. **Software Testing / Coverage**
- **Test case selection**: Randomly prioritize tests using failure probability estimates
- **Quality assurance**: Achieve high code coverage with fewer tests via informed randomization
- **Defect prediction**: Balance detection cost against false-positive rates

## Common Mistakes / Pitfalls

### 1. **Confusing Expected vs. High-Probability Bounds**
- **Mistake**: Assuming expected cost $\mathbb{E}[\text{cost}] = O(\log n) \cdot OPT$ means every run uses $O(\log n) \cdot OPT$ probes
- **Reality**: Some runs may require significantly more