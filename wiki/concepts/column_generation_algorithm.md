# Column Generation Algorithm

## Definition

**Column generation** is an iterative algorithm for solving large-scale linear programs (LPs) by working with a restricted subset of variables (columns) rather than the complete formulation. The algorithm alternates between:

1. **Restricted Master Problem (RMP)**: Solves the LP using only a subset of columns
2. **Pricing Subproblem**: Identifies new columns with negative reduced cost that improve the current solution

The algorithm terminates when no such improving columns exist, yielding an optimal solution to the original (full) LP.

**Formal Statement**: Given an LP in standard form:
$$\max \mathbf{c}^T \mathbf{x} \quad \text{s.t.} \quad A\mathbf{x} = \mathbf{b}, \quad \mathbf{x} \geq 0$$

where $A$ has exponentially many columns, column generation solves:
$$\text{RMP:} \quad \max \mathbf{c}^T_{J} \mathbf{x}_{J} \quad \text{s.t.} \quad A_{J}\mathbf{x}_{J} = \mathbf{b}, \quad \mathbf{x}_{J} \geq 0$$

with $J \subseteq \{1, 2, \ldots, n\}$ initially small. At each iteration, the **pricing subproblem** solves:
$$\text{Pricing:} \quad \min_{\mathbf{a}} \left( c_{\mathbf{a}} - \boldsymbol{\pi}^T \mathbf{a} \right)$$

where $\boldsymbol{\pi}$ is the dual vector from the RMP. If the minimum is negative, a new improving column is added.

## Key Equations

### Reduced Cost Criterion

A column $\mathbf{a}$ is added to the RMP if its **reduced cost** is negative:
$$\bar{c}_{\mathbf{a}} = c_{\mathbf{a}} - \boldsymbol{\pi}^T \mathbf{a} < 0$$

where $\boldsymbol{\pi}$ are dual optimal values from the current RMP.

### Optimality Condition

The RMP solution is optimal for the full LP when:
$$\min_{\mathbf{a}} \left( c_{\mathbf{a}} - \boldsymbol{\pi}^T \mathbf{a} \right) \geq 0$$

i.e., no column with negative reduced cost exists.

### Convergence Rate

For well-structured problems, column generation often achieves much tighter bounds than the LP relaxation with all columns, particularly when:
$$|J| \ll \binom{|V|}{k} \text{ (exponential column space)}$$

## Physical Intuition / Derivation

### Why Column Generation Works

Traditional LP solvers (simplex, interior-point) scale poorly when the constraint matrix has exponentially many columns. Column generation exploits **sparsity**: most columns will never be used in an optimal solution, so we generate only those needed.

**Analogy**: Imagine a warehouse with exponentially many product types. Rather than pricing all products upfront, we identify which products customers demand most (pricing subproblem), add them to inventory (RMP), and repeat until no profitable products remain.

### The Duality Connection

At iteration $t$:
- The RMP yields primal solution $\mathbf{x}^{(t)}$ and dual solution $\boldsymbol{\pi}^{(t)}$
- The **dual bound** is $\boldsymbol{\pi}^{(t)T} \mathbf{b}$
- The pricing subproblem must find the *most attractive* column under current prices $\boldsymbol{\pi}^{(t)}$

If no attractive column exists (all reduced costs $\geq 0$), strong duality guarantees optimality.

### Exponential-Size Formulation Example

The source material demonstrates this for the **co-3-plex problem**:

A co-$k$-plex is a subset $S \subseteq V$ such that the induced subgraph $G[S]$ has maximum degree $k-1$. The source reduces finding a maximum co-3-plex to a stable set problem in an auxiliary graph $A(G)$ of exponential size.

The LP formulation:
$$\max \sum_{\mathbf{s} \in \text{paths/triangles}} w(\mathbf{s}) x_{\mathbf{s}} \quad \text{s.t.} \quad \text{covering constraints}$$

has exponentially many variables (one per feasible co-3-plex substructure), but the **pricing subproblem** reduces to finding a **maximum vertex and edge weighted induced path**, solvable in polynomial time.

## Applications in Engineering

### 1. **Cutting Stock & Bin Packing**
Column generation solves the **cutting stock problem**: minimize waste when cutting material into demanded sizes. Each column represents a cutting pattern; the pricing subproblem is a knapsack problem.

### 2. **Vehicle Routing & Crew Scheduling**
Routes (columns) are generated dynamically. The pricing subproblem finds profitable new routes given current dual values. This enables solving instances with thousands of customers.

### 3. **Network Design & Telecommunications**
Find minimum-cost multiflow routing. Columns are paths; pricing identifies congestion-aware routes via shortest path subproblems.

### 4. **Graph Optimization Problems**
As in the source: finding maximum cliques, independent sets, or structured subgraphs (co-$k$-plexes) when the direct IP is intractable.

### 5. **Machine Learning & Combinatorial Optimization**
Column generation + branch-and-bound (**branch-and-price**) solves hard integer programs in set cover, facility location, and structured prediction.

## Common Mistakes / Pitfalls

### 1. **Assuming the Pricing Subproblem is Easier**
Column generation only works if the pricing subproblem is significantly faster than solving the full LP. If pricing is NP-hard, the speedup vanishes. ⚠️ *The