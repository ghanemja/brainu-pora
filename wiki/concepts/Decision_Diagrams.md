# Decision Diagrams

## Definition

A **Decision Diagram (DD)** is a directed acyclic layered graph representation for discrete optimization problems. Each root-to-terminal path in the graph encodes a candidate solution to the problem. Formally:

- **Graph Structure**: A DD is a DAG $G = (V, A)$ organized into layers $L_0, L_1, \ldots, L_n$
- **Nodes**: Represent states in the decision space at each decision stage
- **Arcs**: Encode transitions (decisions) between states, typically labeled with decision values
- **Root and Terminal**: Unique source node (in $L_0$) and sink node (in $L_n$)
- **Path Semantics**: Each root-to-terminal path represents a feasible or candidate solution

### Two Primary Variants

1. **Restricted DD**: A heuristic that aggressively merges states to maintain small width $w$, producing a greedy-like feasible solution
2. **Relaxed DD**: A relaxation that retains more states (larger $w$) to compute valid combinatorial bounds on the optimal value

## Key Equations

### Complexity of DD Construction

**Standard (Explicit) Approach:**
- Restricted DD per-layer complexity: $O(w \log w)$
- Relaxed DD per-layer complexity: $O(w^2)$

where $w$ is the maximum width (number of nodes in any layer).

**Implicit DD Approach:**
- Both restricted and relaxed DD per-layer complexity: $O(w)$

This is **optimal** in the sense that:

$$\text{Optimal complexity} = \Omega(w)$$

because any framework must process $w$ states per layer and cannot do better while treating state-update and merge operations as black boxes.

### Value Propagation

For a relaxed DD computing an upper bound on a minimization problem:

$$v(n) = \min_{a \in \text{outgoing}(n)} \left\{ \text{cost}(a) + v(\text{target}(a)) \right\}$$

where $v(n)$ is the value (bound) at node $n$, and the bound at the root node provides a valid upper bound on the optimal objective.

## Physical Intuition / Derivation

### Why Decision Diagrams Matter

Standard Mixed-Integer Programming (MIP) solvers achieve their effectiveness through decades of theoretical and engineering refinement. Decision Diagrams, by contrast, represent a newer paradigm (rapid adoption since 2016) that has focused heavily on **algorithmic theory** but neglected **implementation complexity**.

The key insight is that many discrete optimization problems admit more compact dynamic programming (DP) formulations than MIP formulations. DDs provide a bridge: they are essentially *graphical representations of dynamic programs*.

### How Restricted DDs Work

Imagine solving a problem layer-by-layer, where at each layer you need to track all possible states. In an unrestricted DP, the number of states may grow exponentially. A restricted DD:

1. **Maintains width bound $w$**: At each layer, allow at most $w$ nodes
2. **Merges aggressively**: When states must be combined, merge them using problem-specific merge rules
3. **Produces greedy solution**: The resulting restricted DD yields a feasible solution (like a greedy heuristic)

**Intuition**: You trade optimality for tractability by intentionally forgetting information (through merging).

### How Relaxed DDs Work

A relaxed DD inverts this tradeoff:

1. **Maintains larger width**: Use a larger $w$ to retain more distinct states
2. **Relaxes merge rules**: Only merge states that are "safe" to merge without violating optimality
3. **Provides bounds**: The resulting DD yields a valid bound on the optimal value

**Intuition**: You retain more information to get tighter bounds, accepting higher construction cost.

### The Implicit Representation Breakthrough

Standard explicit DDs store all arcs $A$ in memory. For a layer with $w_i$ predecessor nodes and $w_{i+1}$ successor nodes, the number of arcs can be $O(w_i \cdot w_{i+1})$ in the worst case.

Implicit DDs observe that:
- Most problem instances have **structured arc sets** that can be **generated on-demand** rather than stored
- Rather than storing explicit arc lists, store only node states and use a **generative function** to compute successors when needed

This reduces memory and enables $O(w)$ layer construction by:
$$\text{Per-layer work} = O(w \text{ nodes}) \times O(1 \text{ average successors per node})$$

## Applications in Engineering

### Discrete Optimization Problems

1. **Subset Sum Problems**: Select items to reach target value; DDs compactly encode the DP structure
2. **Scheduling**: Machine scheduling, job sequencing; layers represent time steps
3. **Routing and Assignment**: Vehicle routing, assignment with side constraints
4. **Resource Allocation**: Knapsack variants, bin packing with additional constraints

### Integration with Solvers

- **Bounding in Branch-and-Bound**: Relaxed DDs provide bounds tighter than LP relaxations in some cases
- **Heuristic Generation**: Restricted DDs produce feasible solutions for warmstart
- **Hybrid Solvers**: Alternate between DD-based bounds and MIP techniques (as implemented in [[ImplicitDDs.jl]])

### Problem Classes

DDs excel on problems where:
- The optimal DP formulation has **polynomial width** (tractable state space)
- The MIP formulation is **large or weak** (loose LP bounds)
- Solutions have **sequential structure** (naturally layered)

Examples: structured scheduling, resource-constrained path problems, sequencing with precedence constraints.

## Common Mistakes / Pitfalls

### 1. Conflating Nodes and States

**Mistake**: Treating DD nodes as identical to DP states.

**Reality**: A DD node may represent multiple DP states (due to merging in restricted DDs) or may not exist if pruned. The DD is an *abstraction* of the DP.

### 2. Ignoring Implementation Cost

**Mistake**: Designing algorithms with theoretical optimal complexity but ignoring constant factors and memory layout.

**Reality**: As theory shows $O(w)$ is optimal, practical performance is determined by low-level engineering: