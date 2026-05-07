# edge-weighted matching

## Definition

An **edge-weighted matching** is a subset of edges in a graph where:
- No two edges share a common vertex (the matching property)
- Each edge carries an associated weight or value $w(e) \in \mathbb{R}$
- The objective is typically to maximize (or minimize) the total weight

More formally, for a graph $G = (V, E)$ with edge weights $w: E \to \mathbb{R}$, a matching $M \subseteq E$ is edge-weighted if it is a valid matching and the goal is to find:

$$M^* = \arg\max_{M \text{ matching}} \sum_{e \in M} w(e)$$

This generalizes the unweighted matching problem (where $w(e) = 1$ for all $e$) and appears in diverse settings: maximum weight bipartite matching, auction design, online allocation problems, and stochastic matching under uncertainty.

## Key Equations

### Maximum Weight Matching Formulation

For bipartite graphs $G = (X \cup Y, E)$ with weights $w_{ij}$ on edge $(i,j)$:

$$\text{maximize} \quad \sum_{(i,j) \in E} w_{ij} x_{ij}$$

$$\text{subject to} \quad \sum_{j: (i,j) \in E} x_{ij} \leq 1 \quad \forall i \in X$$

$$\sum_{i: (i,j) \in E} x_{ij} \leq 1 \quad \forall j \in Y$$

$$x_{ij} \in \{0, 1\}$$

The linear programming relaxation (setting $x_{ij} \in [0,1]$) defines the **matching polytope**.

### Competitive Ratio for Online Matching

For online algorithms with arrival constraints, the competitive ratio $\rho$ is defined as:

$$\rho = \inf_{\text{ALG}} \sup_{I} \frac{\text{OPT}(I)}{\text{ALG}(I)}$$

where the infimum is over all online algorithms and the supremum is over all possible instances.

### Contention Resolution Schemes (CRS)

For a matching problem with random-order arrival or stochastic selection, a CRS achieves selection probability vector $y$ satisfying:

$$\mathbb{E}[\text{weight of selected edges}] \geq \alpha \cdot \text{LP relaxation value}$$

where $\alpha$ is the **resolution parameter** (typically $\alpha \in (0,1)$).

## Physical Intuition / Derivation

### Why Edge Weights Matter

In unweighted matching, all edges are equally desirable. However, real systems have heterogeneous value:
- In **online hiring**, applicants have different skill values
- In **online advertising**, ad slots have different values to bidders
- In **stochastic bipartite matching**, edge weights represent expected utility

### The Tension: Greedy Fails

The greedy algorithm (repeatedly pick the heaviest available edge) fails even on simple instances:

**Example**: Consider edges: $(1,a) \to 3$, $(1,b) \to 2$, $(2,a) \to 2$, $(2,b) \to 1$

- Greedy picks $(1,a) \to 3$, then $(2,b) \to 1$. Total: $4$
- Optimal picks $(1,b) \to 2$ and $(2,a) \to 2$. Total: $4$ (tie here, but greedy can be arbitrarily suboptimal)

The issue: committing to a heavy edge may block multiple medium-weight edges.

### Online and Stochastic Variants

When edges arrive in random order or selection probabilities are learned online, we cannot solve the problem offline. Key insights:

1. **Contention Resolution Schemes** [LS18, MMG23]: Instead of making binary decisions immediately, maintain fractional probabilities that can be "rounded" to respect matching constraints while preserving value.

2. **Prophet Inequalities**: Bound the value gap between optimal adaptive offline policies and simple online policies, using distributional information about arriving edges [LS18].

3. **Vertex vs. Edge Arrivals** [MM24]: Performance degrades differently when vertices arrive (revealing all incident edges) versus edges arriving one-by-one.

## Applications in Engineering

### 1. **Gig Economy & Labor Markets** [PRSW24, PGR19]
Matching workers to jobs under uncertainty about future arrivals. Weights represent productivity or profit. Online contention resolution schemes achieve $\geq 0.5$ fraction of offline optimum.

### 2. **Auction Design & Ad Allocation**
Match bidders to items maximizing revenue. Edge weights = bid values. Approximation algorithms guarantee competitive outcomes despite strategic behavior.

### 3. **Bipartite Scheduling** [Jan03]
Assign tasks to machines where edge weight = job value. Fractional relaxations and rounding techniques (via separation) produce near-optimal schedules.

### 4. **Sparse Random Graph Matching** [KS81]
Analysis of maximum weight matchings in random graphs relevant to wireless networks and peer-to-peer systems where connectivity is probabilistic.

### 5. **Stochastic Matching Under Uncertainty** [GKS19, HSWZ25]
Real-time matching where edge weights or existence are revealed as edges arrive. Algorithms must decide online whether to accept an edge before seeing future options.

## Common Mistakes / Pitfalls

### 1. **Confusing LP Relaxation with Integer Solution**
The LP relaxation (allowing $x_{ij} \in [0,1]$) is always $\geq$ the integer optimum. Don't assume a fractional solution rounds to the same value without error analysis.

### 2. **Greedy Achieves $1/2$ Approximation (Sometimes)**
While greedy fails badly in worst-case, it achieves $1/2$-approximation for general graphs. But for bipartite matching with adversarial edge weights, it can achieve worse ratios; context matters.

### 3. **Online vs. Offline Complexity**
Polynomial-time optimal algorithms exist offline (Hungarian algorithm, $