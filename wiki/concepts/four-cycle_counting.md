# Four-Cycle Counting

## Definition

**Four-cycle counting** is the problem of estimating or detecting the number of four-cycles (i.e., simple cycles of length 4) present in a large undirected graph, particularly in the **streaming model** where the graph is too large to store in memory and edges arrive sequentially in arbitrary order.

A four-cycle is a subgraph consisting of four distinct vertices $\{v_1, v_2, v_3, v_4\}$ connected by edges forming a cycle: $(v_1, v_2), (v_2, v_3), (v_3, v_4), (v_4, v_1)$. The counting problem asks: given a graph stream with edge count $m$ and true four-cycle count $T$, compute a $(1 + \epsilon)$-approximation of $T$ using sublinear space and a limited number of passes over the data.

This is a special case of the broader **subgraph motif counting** problem in graph streaming.

## Key Equations

**Space Complexity Bounds:**

The near-optimal algorithm achieves space complexity of:
$$\tilde{O}\left(\frac{m}{\sqrt{T}}\right)$$

where:
- $m$ = number of edges in the graph
- $T$ = true number of four-cycles
- $\tilde{O}$ denotes the big-O notation with logarithmic factors suppressed

This improves upon the previous best result by Vorotnikova:
$$\tilde{O}\left(\frac{m}{T^{1/3}}\right)$$

and **matches** the multi-pass lower bound established by McGregor and Vorotnikova:
$$\Omega\left(\frac{m}{\sqrt{T}}\right)$$

**Approximation Guarantee:**

The algorithm outputs estimate $\hat{T}$ satisfying:
$$\hat{T} = (1 \pm \epsilon) T$$

with high probability, where $\epsilon$ is a user-specified error parameter.

**Pass Complexity:**

The algorithm requires:
$$\text{Passes} = 3$$

## Physical Intuition / Derivation

### Why Four-Cycle Counting Is Hard

Counting four-cycles is fundamentally more challenging than triangle counting because:

1. **Longer dependency chains**: A four-cycle requires tracking paths of length 3, creating more complex correlations between edges compared to triangles (which need only length-2 paths).

2. **Adaptive sampling requirements**: In streaming, you cannot store the entire graph. The challenge is deciding which edges to sample or which information to maintain without exceeding space bounds.

3. **Edge ordering**: Edges arrive in arbitrary (adversarial) order. A four-cycle might be "broken up" across the stream, requiring careful bookkeeping.

### Intuition Behind Space-Cycle Tradeoff

The space bound $\tilde{O}(m/\sqrt{T})$ reveals an important phenomenon:

- **When $T$ is small** (few four-cycles): The space requirement is approximately $\tilde{O}(m)$, nearly linear in edges. This makes intuitive sense—if cycles are rare, you need to track more edge information to reliably detect them.

- **When $T$ is large** (dense four-cycles): The space requirement shrinks as $\tilde{O}(m/\sqrt{T})$. When the graph is "cycle-rich," sampling is more efficient because random edge subsets are likely to contain four-cycle instances.

This is analogous to **importance sampling**: rare events require larger sample sizes; common events need smaller samples for reliable estimation.

### Why 3 Passes?

The multi-pass model allows the algorithm to:
1. **Pass 1**: Gather global statistics about edge distributions and degree information
2. **Pass 2**: Perform targeted sampling or filtering based on pass 1 insights
3. **Pass 3**: Verify and count structures found in pass 2 passes

A single pass cannot achieve these tradeoffs because you see each edge only once and cannot adaptively refine your sampling strategy.

## Applications in Engineering

### Network Analysis & Social Media
- **Community structure detection**: Four-cycles often represent cliques or near-cliques in social networks; counting them reveals densely connected communities
- **Recommendation systems**: Four-cycle patterns indicate users who share common interests through mutual connections
- **Fraud detection**: Suspicious cliques or coordinated behavior in transaction networks often manifest as elevated four-cycle counts

### Biological Networks
- **Protein interaction networks**: Four-cycles represent feedback loops or feedforward motifs with regulatory significance
- **Gene networks**: Counting specific motifs helps identify functional modules and biological pathways
- **Systems biology**: Four-cycle abundance correlates with network robustness and dynamic behavior

### Database & Information Systems
- **Knowledge graph analysis**: Pattern matching on knowledge graphs requires efficient subgraph counting
- **Query optimization**: Understanding subgraph frequencies improves index structures and join planning
- **Graph compression**: Motif-aware compression exploits common four-cycle patterns

### Internet & Web Graphs
- **Hyperlink analysis**: Four-cycles in web graphs reveal topical clustering and topological anomalies
- **Online collaboration networks**: Wikipedia, GitHub, and similar platforms use motif counting for quality assessment

### Cybersecurity
- **Network anomaly detection**: Abnormal four-cycle densities may indicate botnet activity, DDoS coordination, or intrusion patterns
- **Graph fingerprinting**: Motif signatures enable rapid network classification and threat profiling

## Common Mistakes / Pitfalls

### 1. **Confusing Induced vs. Non-Induced Subgraphs**
**Mistake**: Counting only "chordless" four-cycles (induced subgraphs with no additional edges between the four vertices).

**Correction**: The algorithm counts all four-cycles regardless of additional edges. An induced four-cycle is a special case; general counting includes graphs where the four vertices have additional interconnections.

### 2. **Assuming Single-Pass Efficiency**
**Mistake**: Expecting the streaming algorithm to work in a single pass with the same space bounds.

**Correction**: Single-pass lower bounds are strictly worse. Multi-pass is essential for achieving near-optimal bounds. Trade-off: multiple passes over stored data vs. sublinear space per pass.

### 3. **Overlooking Adversarial Edge Ordering**
**Mistake**: Designing algorithms assuming edges arrive in a