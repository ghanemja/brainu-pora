# Dynamic Graph Algorithms

## Definition

Dynamic graph algorithms are computational methods that efficiently maintain and query properties of graphs that change over time through edge/vertex insertions and deletions. Unlike static algorithms that assume the graph is fixed, dynamic algorithms must update their data structures and answer queries in real-time as the graph evolves.

A **fully dynamic algorithm** handles both insertions and deletions. A **semi-dynamic algorithm** handles only insertions (decremental) or only deletions (incremental). The key performance metric is the **amortized update time**—the average time per modification operation.

**Formal Problem Statement:**  
Maintain a graph $G = (V, E)$ supporting:
- $\texttt{Insert}(u, v)$: Add edge $(u,v)$ to $E$
- $\texttt{Delete}(u, v)$: Remove edge $(u,v)$ from $E$
- $\texttt{Query}(P)$: Answer queries about property $P$ (e.g., coloring, distance, connectivity)

such that each operation completes in $t_{\text{update}}$ time.

## Key Equations

### Johansson's Coloring Bound
For triangle-free graphs with maximum degree $\Delta$:
$$\chi(G) = O\left(\frac{\Delta}{\ln \Delta}\right)$$

This significantly improves the greedy upper bound of $\Delta + 1$ colors for general graphs.

### Amortized Analysis
If a sequence of $m$ updates takes total time $T$, the amortized time per update is:
$$t_{\text{amortized}} = \frac{T}{m}$$

### Potential Function Method
Define potential $\Phi$ such that actual cost $c_i$ and amortized cost $\hat{c}_i$ satisfy:
$$\hat{c}_i = c_i + \Delta \Phi_i$$
where $\Delta \Phi_i = \Phi_i - \Phi_{i-1}$.

## Physical Intuition / Derivation

### Why Dynamic Algorithms Matter

Static algorithms assume the entire graph is known upfront. In real systems—social networks, road networks, power grids—the graph structure constantly changes. Recomputing from scratch after each update is prohibitively expensive.

**Example Trade-off:**
- *Static approach*: Recompute coloring from scratch after each edge change. Cost: $O(n + m)$ per update.
- *Dynamic approach*: Incrementally recolor only affected regions. Cost: $\Delta^{o(1)} \log n$ per update (for the Johansson coloring problem).

### The Entropy Compression Technique

The entropy compression method (from the source material) is a proof technique that bounds the number of "recoloring configurations" the algorithm can reach. The intuition:

1. **Potential Measurement:** Assign each configuration a potential related to how "far" it is from a canonical state.
2. **Entropy Bound:** Count reachable configurations using information-theoretic arguments (bits needed to describe the state).
3. **Amortized Cost:** Charge the expensive recolorings to decreases in potential, amortizing their cost.

This technique is powerful because it separates the *analysis* of what happens (combinatorial argument) from the *implementation* (which recoloring rules apply).

### Randomization and High Probability

The algorithm is **randomized** and operates **with high probability (w.h.p.)**—meaning it succeeds with probability $1 - o(1/\text{poly}(n))$ against an **adaptive adversary** that observes previous coin flips and adjusts the adversarial updates accordingly. This is harder to achieve than against oblivious adversaries.

The $\Delta^{o(1)}$ factor (super-polynomial but sub-polynomial in $\Delta$) arises from tail bounds in the randomized analysis.

## Applications in Engineering

### 1. **Social Network Analysis**
Real-time friendship graphs change continuously. Dynamic algorithms maintain:
- Community structure and clustering coefficients
- Influence propagation and centrality measures
- Recommended friend lists without global recomputation

### 2. **Road Networks and Navigation**
GPS and routing systems operate on dynamic graphs:
- Edge weights change as traffic conditions fluctuate
- Maintain shortest paths / distance oracles (see CGMW references on planar graph distance oracles)
- Update routes in real-time for thousands of concurrent queries

### 3. **Network Routing and Topology**
Telecommunications networks:
- Maintain connectivity and spanning trees as links fail/recover
- Update multicast trees dynamically
- Ensure no color conflicts in wavelength assignment (graph coloring → spectrum allocation)

### 4. **Compiler Register Allocation**
Control flow graphs change during compilation:
- Maintain interference graph colorings for register assignment
- Insert spill code when new constraints arise
- Triangle-free graphs arise naturally in certain SSA-based IL representations

### 5. **Constraint Satisfaction and SAT Solving**
Implication graphs and conflict graphs grow/shrink:
- Maintain 2-SAT solutions under clause additions/removals
- Track conflict graph colorings for clause learning

## Common Mistakes / Pitfalls

### 1. **Confusing Amortized vs. Worst-Case Time**
A bound like $\Delta^{o(1)} \log n$ amortized does **not** mean every single update runs in that time—some updates may be much slower. Amortized bounds only guarantee the *average* over a sequence.

### 2. **Ignoring Adversarial Behavior**
"High probability against adaptive adversary" is much stronger than against oblivious adversaries. An adaptive adversary can cause unlucky coin flips to compound. Many naive randomized approaches fail here.

### 3. **Underestimating Hidden Constants**
The $\Delta^{o(1)}$ notation hides potentially large polynomial factors in $\log \log \Delta$ or $\log^* \Delta$. Real implementations may be slow for moderate $\Delta$.

### 4. **Applying Static Techniques Naively**
Simply running a static coloring algorithm on the perturbed graph is not truly dynamic. You lose the cumulative benefit of prior work. True dynamic algorithms must *reuse* prior data structures strategically.

### 5. **Forgetting the Problem Structure**
The dramatic improvement ($O(\Delta