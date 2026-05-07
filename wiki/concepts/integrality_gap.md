# Integrality Gap

## Definition

The **integrality gap** of an optimization problem is the worst-case ratio between the optimal value of a linear programming (LP) relaxation and the optimal value of the original integer programming (IP) formulation.

Formally, for a minimization problem:

$$\text{Integrality Gap} = \max_{\text{instances}} \frac{\text{OPT}_{\text{LP}}}{\text{OPT}_{\text{IP}}}$$

For a maximization problem, this ratio is inverted. The integrality gap quantifies how much information is lost when relaxing integer constraints to continuous variables—it bounds the approximation ratio achievable via LP-based algorithms for that problem.

**Key characteristics:**
- Always $\geq 1$ for minimization (LP relaxation provides a lower bound on IP optimum)
- A small integrality gap indicates the LP relaxation is "tight" and likely yields good approximations
- A large integrality gap signals fundamental difficulty; no LP-based algorithm can achieve better than this approximation ratio

## Key Equations

For a minimization integer program:
$$\text{OPT}_{\text{IP}} \geq \text{OPT}_{\text{LP}}$$

Thus the integrality gap satisfies:
$$\text{IG} = \frac{\text{OPT}_{\text{LP}}}{\text{OPT}_{\text{IP}}} \leq 1 \text{ (if we flip the ratio)}$$

More commonly stated as:
$$\text{OPT}_{\text{IP}} \leq \text{IG} \cdot \text{OPT}_{\text{LP}}$$

For geometric stabbing problems (e.g., rectangle stabbing), if $k^*$ is the optimal number of lines and $k_{\text{LP}}$ is the LP relaxation bound:
$$\text{IG} = \sup \frac{k^*}{k_{\text{LP}}}$$

## Physical Intuition / Derivation

### Why the Gap Exists

When we relax an IP to an LP, we allow fractional solutions. For example, in a set cover problem, the LP might assign 0.5 to multiple sets, covering each element fractionally. The IP must use only integer sets, requiring discrete commitments that may be wasteful.

**Simple example:** Consider covering 3 elements with sets $\{A = \{1,2\}, B = \{2,3\}, C = \{1,3\}\}$, each costing 1.
- **IP optimum:** Use any 2 sets (cost = 2)
- **LP optimum:** Assign weight 0.5 to each set (cost = 1.5)
- **Integrality gap:** $2/1.5 = 4/3$

### Building Intuition

The integrality gap measures the "cost of discreteness." Large gaps occur when:

1. **Fractional solutions exploit problem structure unavailable to integral solutions** — e.g., overlapping sets can be "split" fractionally in ways that have no discrete counterpart
2. **The feasible region of the LP relaxation has many fractional vertices** — more distance from the integral vertices
3. **Rounding fractional solutions causes cascading violations** — fixing one variable breaks constraints elsewhere

### Derivation via LP Duality

The integrality gap can be analyzed using LP duality. If the LP has a large optimal value (loose relaxation), the dual LP will have a corresponding large value, indicating weak dual certificates—fewer structural constraints preventing fractional solutions.

## Applications in Engineering

### 1. **Approximation Algorithm Design**

The integrality gap is the fundamental limit for LP-based approximation algorithms. If IG = $c$, then:
- Any rounding algorithm based on that LP formulation has approximation ratio $\geq c$
- Designing better approximations requires either a better LP formulation or non-LP techniques

**Example applications:**
- [[Vehicle Routing Problem]]: Large integrality gaps motivate cutting-plane methods and branch-and-cut algorithms
- [[Facility Location]]: LP relaxations with IG $\approx 1.463$ guide algorithm design

### 2. **Rectangle Stabbing & Geometric Optimization**

In stabbing problems (covering geometric objects with minimum lines/points):
- LP relaxations provide lower bounds on the stabbing number
- Integrality gap determines how many more stabbing elements are needed in the worst case
- Applications: VLSI layout verification, computational geometry algorithms (e.g., [1], [6], [8])

### 3. **Resource Allocation & Scheduling**

In bin packing, job scheduling, and resource allocation:
- The integrality gap reveals the efficiency loss from rounding fractional allocations
- Guides design of online algorithms with competitive ratios matching known gaps

### 4. **Network Design**

In Steiner tree, network flow, and routing problems:
- IG informs bounds on the cost of discrete network topologies vs. continuous relaxations
- Critical for evaluating heuristic solutions in telecommunications and grid design

### 5. **Parameterized Complexity**

In fixed-parameter tractable (FPT) problems, integrality gaps interact with parameterization:
- A high IG can signal hardness even for parameterized approximation
- Used to prove lower bounds on approximation-parameterized algorithms (e.g., [4], [10])

## Common Mistakes / Pitfalls

### 1. **Confusing Direction for Maximization vs. Minimization**

❌ **Mistake:** Applying the minimization formula to a maximization problem.
$$\text{Correct for max:} \quad \text{IG} = \frac{\text{OPT}_{\text{IP}}}{\text{OPT}_{\text{LP}}} \quad (\text{always} \leq 1)$$
Better phrased as: LP is *at most* IG fraction of IP optimum.

### 2. **Assuming IG Applies to All Relaxations**

❌ **Mistake:** An integrality gap for one LP formulation applies to all formulations.
✅ **Correct:** Different LP relaxations have different gaps. Strengthening constraints (cutting planes, valid inequalities) reduces the gap for that formulation.

### 3. **Conflating IG with