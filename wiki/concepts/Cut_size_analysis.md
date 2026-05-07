# Cut size analysis

## Definition

**Cut size analysis** is a probabilistic technique for bounding the expected size of edge cuts (or node separators) in graph partitioning algorithms, particularly in the context of multicommodity flow approximation and demand routing.

More formally: given a graph $G = (V, E)$ and a sequence of demand pairs $(s_i, t_i)$, cut size analysis measures how many edges (or nodes) must be removed to disconnect a pair of nodes $(u, v)$ after applying cuts corresponding to randomly selected demand pairs. The analysis tracks the **persistence** of connectivity—how many rounds of the algorithm a given edge pair remains connected before being severed by some cut.

In advanced variants (like triangle analysis), the focus extends from pairwise connectivity $(\text{vdist}(u, v))$ to triple-wise connectivity structures, examining when three-node relationships lie between multiple demand pairs simultaneously.

## Key Equations

### Basic Distance Metric
$$\text{vdist}(u, v) = \text{minimum number of nodes in any path from } u \text{ to } v$$

### Persistence Bound (Gupta-style analysis)
For a node $v$ between demand pair $(s, t)$:
$$\mathbb{E}[\text{rounds } v \text{ is cut}] = O\left(\frac{n}{L}\right)$$

where $L$ is a distance threshold (typically $L = \Omega(\log n)$ or problem-dependent).

### Separation Probability
If node $u$ satisfies $\text{vdist}(u, v) \geq \Omega(L)$, then:
$$\mathbb{P}[\text{pair } (u,v) \text{ separated in round } r] \geq \Omega(L^{-1})$$

### Triangle-Based Improvement
With triangle structures, certain close pairs $(u, v)$ with $\text{vdist}(u, v) = \text{poly}(L)$ appear between $\Omega(nL^{\beta})$ demand pairs (vs. $\Omega(n)$ for far pairs), yielding:
$$\mathbb{E}[\text{rounds until separation}] = O\left(\frac{1}{L^{\beta}}\right)$$

## Physical Intuition / Derivation

### Gupta's Original Approach: "Far-Apart Pairs"

The core insight is **statistical amortization**:

1. **Observation**: If nodes $u$ and $v$ are far apart (distance $\geq \Omega(L)$), then roughly $\Omega(L)$ nodes lie on any path between them.

2. **Consequence**: When we solve a routing problem for demand pair $(s, t)$ and cut the graph to separate $s$ from $t$, if $v$ lies between $s$ and $t$, we must disconnect approximately $\Omega(L)$ node-pairs near $v$ from their reachable partners.

3. **Amortization**: Since there are $O(n^2)$ possible node pairs but only $n$ possible "intermediate nodes," each pair $(u, v)$ can be "between" only $O(n/L)$ demand pairs in expectation before being cut.

**Mathematical intuition**: The cut creates a "frontier" of disconnected pairs. The larger the distance between $u$ and $v$, the more likely they both lie across this frontier, but also the more "expensive" they are to separate (requiring many edge removals), so they're cut sooner.

### Triangle Analysis: "Mixed-Distance Triples"

The improvement introduces **triple-wise structures**:

1. **New phenomenon**: Instead of only considering far pairs like $(u, v)$ with $\text{vdist}(u, v) = \Omega(L)$, we identify *triangles* $(u, v, w)$ where:
   - Some pairs are far (e.g., $\text{vdist}(u, w) \geq \Omega(L)$)
   - Some pairs are close (e.g., $\text{vdist}(u, v) = O(L)$)
   - The triangle structure forces certain close pairs to appear in many demand pairs

2. **Coupling argument**: Either:
   - **Case A**: Triangle structures exist $\Rightarrow$ certain far pairs appear in $\Omega(nL^{\beta})$ demand pairs (exponentially more), or
   - **Case B**: No strong triangles $\Rightarrow$ there exist close pairs appearing in $\Omega(nL^{\beta})$ demand pairs (impossible without structure).

3. **Key advantage**: Close pairs, though individually "weak" (less likely cut per demand), are selected far more often, dominating the expected separation time.

### Close-Pair Separation: The Technical Subtlety

Unlike Gupta's analysis (which is independent of demand ordering), triangle analysis requires:
$$\mathbb{P}_{\text{cut}, \text{pair}}[\text{separation}] = \mathbb{E}_{\text{demand}}[\mathbb{P}_{\text{cut}}[\text{disconnect } (u,v) \mid (s,t)]]$$

The randomness comes from **both** the cut algorithm (which edges are removed) and the choice of which demand pair to solve (adversarial ordering is no longer valid).

## Applications in Engineering

### 1. **Approximation Algorithms for Routing**
- Cut size analysis bounds the stretch factor in multicommodity flow approximation.
- Critical for analyzing **oblivious routing** schemes that must handle unknown demand patterns.
- Example: Achieving $O(\log n)$ approximation for minimum-congestion routing on arbitrary graphs.

### 2. **Network Design & Load Balancing**
- Determines how much "over-capacity" is needed in networks with dynamic, unknown traffic patterns.
- Used in data center network design to provision Ethernet fabrics (e.g., spine-leaf architectures).

### 3. **VLSI Circuit Partitioning**
- Bounds the number of "cut" wires between circuit blocks during hierarchical partitioning.
- Guides placement algorithms to minimize inter-block communication.

### 4. **Machine Learning: Graph Neural Networks**
- Informs sampling strategies for mini-batch partitioning of large graphs.
- Helps analyze message-