# High-probability (whp) linear-work algorithm

## Definition

A **high-probability linear-work algorithm** is a randomized algorithm that solves a computational problem in $O(m)$ work (where $m$ is the input size) with probability at least $1 - 1/\text{poly}(n)$, where $n$ is a problem-dependent parameter. The algorithm achieves linear work complexity *in expectation* while maintaining rigorous probabilistic guarantees.

More formally: an algorithm $\mathcal{A}$ is whp linear-work if:
- **Work bound**: $W(\mathcal{A}) = O(m)$ with probability at least $1 - n^{-c}$ for constant $c > 0$
- **Correctness**: The algorithm produces a correct solution with the same high probability

This contrasts with Las Vegas algorithms (which always correct but variable runtime) and Monte Carlo algorithms (which have variable correctness).

## Key Equations

For a random variable $X$ representing algorithm work, the method of bounded differences guarantees:

$$P(|X - \mathbb{E}[X]| \geq t) \leq 2\exp\left(-\frac{2t^2}{\sum_{i=1}^{n} c_i^2}\right)$$

where $c_i$ bounds the influence of the $i$-th random choice. Setting $t = \Theta(\sqrt{m \log n})$ yields whp concentration.

For balanced partitioning, if vertices are randomly assigned to $k = \text{polylog}(n)$ parts, the edge load in part $i$ satisfies whp:

$$|E(V_i)| = O\left(\frac{m}{k^2}\right) = O\left(\frac{m}{(\log n)^{2c}}\right)$$

## Physical Intuition / Derivation

### The Challenge: Derandomization

Work-efficient randomized algorithms often suffer from **load imbalance**: when a graph is partitioned randomly, dense subgraphs may concentrate in a single partition, requiring $\Omega(m)$ work even on average. To achieve linear work *with high probability*, we must:

1. **Identify bad structures**: High-degree vertices create concentration risk
2. **Remove them strategically**: Cull vertices with degree $> D_{\text{threshold}}$ into a small set $C$
3. **Apply randomization**: Partition the remaining "tame" graph where bounded differences guarantee balance
4. **Extend deterministically**: Handle the culled vertices $C$ exactly (feasible because $|C| \leq \text{polylog}(n)$)

### Culled Balanced Partition Strategy

The algorithm works in phases:

**Phase $t$:**
- Check if all degrees in remaining graph $G_t$ satisfy: $\max_v \deg(v) \leq D_t$
- If **yes**: Apply random partition into $k = \text{polylog}(n)$ parts. By bounded differences, each part has $O(m_t/k^2)$ edges whp
- If **no**: Remove all high-degree vertices (at most $\text{polylog}(n)$ per iteration). This halves edges: $m_{t+1} \leq m_t/2$

Since edges halve exponentially, at most $\log n$ iterations occur before the degree condition holds.

**Total culled**: $|C| = O(\log n \cdot \text{polylog}(n)) = O(\text{polylog}(n))$

### Why Linear Work Follows

After culling and partitioning:
- Each balanced piece has $O(m/\text{polylog}(n)^2)$ edges
- Solve recursively on $k$ pieces (work-inefficient subroutine, but small enough that sum is $O(m)$)
- Extend across cuts in $O(m)$ deterministically
- Process culled set in $O(\text{polylog}(n))$ time (negligible)

$$W_{\text{total}} = O(m) + \sum_{i=1}^{k} W_{\text{piece}_i} + O(\text{polylog}(n)) = O(m)$$

## Applications in Engineering

### 1. **Graph Coloring (Δ+1-vertex coloring)**
Distributed systems use vertex colorings to assign non-conflicting tasks. The whp algorithm achieves $O(m)$ total work:
- Palette sampling on balanced pieces (inefficient, but small pieces)
- Deterministic extender: scan cut edges once, compute residual colors for boundary vertices
- For vertex $v$ in piece $H_1$ cut by $H_0$:
$$|\text{residual palette}(v)| \geq \deg_{H_1}(v) + 1$$
guarantees a valid color exists.

### 2. **Distributed Edge Coloring**
Network scheduling: assign colors to edges so no vertex has two edges of the same color. The culled partition reduces the problem to small edge-balanced subgraphs solvable whp in linear work.

### 3. **Parallel Graph Algorithms**
Multicore systems with $p$ processors. Linear-work whp algorithms with $O(\log^c n)$ span (depth) run on PRAM in $O(m/p + \text{polylog}(n))$ time whp, achieving near-linear speedup.

### 4. **Sparse Matrix Factorization**
Nested dissection in sparse LU decomposition: culled partitions create a separator tree with $O(\text{polylog}(n))$-size separators, reducing fill-in whp.

### 5. **Load Balancing in Data Centers**
Partition tasks (vertices) across machines to balance load (edges = dependencies). Culling high-degree tasks before random assignment prevents bottlenecks.

## Common Mistakes / Pitfalls

### 1. **Confusing whp with "in expectation"**
$O(m)$ whp is stronger than $\mathbb{E}[W] = O(m)$. A single run succeeds with probability $1 - n^{-c}$, not just the average.

### 2. **Ignoring the polylog(n) overhead