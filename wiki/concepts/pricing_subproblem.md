# Pricing Subproblem

## Definition

The **pricing subproblem** is the core optimization task solved repeatedly within a column generation algorithm. It determines which new variables (columns) should enter the basis by identifying the variable with the most negative reduced cost.

Formally, in the restricted master problem (RMP):

$$\text{minimize } \mathbf{c}^T \mathbf{x}$$
$$\text{subject to } A\mathbf{x} = \mathbf{b}, \quad \mathbf{x} \geq 0$$

Given dual variables $\boldsymbol{\pi}$ from the current RMP solution, the pricing subproblem solves:

$$\text{maximize } \bar{c} = \text{objective value} - \boldsymbol{\pi}^T A_{\text{new}}$$

where $A_{\text{new}}$ represents a new column. A column with $\bar{c} > 0$ (negative reduced cost in minimization) indicates improvement and should be added to the RMP.

### In the Context of Co-k-Plex Optimization

The source material demonstrates a concrete application: when solving the maximum weighted co-k-plex problem via column generation, the pricing subproblem reduces to **finding a maximum vertex and edge weighted induced path in polynomial time** on chordal graphs. This is remarkable because it proves that column generation itself runs in polynomial time for this NP-hard problem class.

## Key Equations

**Reduced Cost Calculation:**
$$\bar{c}_j = c_j - \boldsymbol{\pi}^T A_j$$

where:
- $c_j$ is the original objective coefficient of column $j$
- $A_j$ is the constraint matrix column $j$
- $\boldsymbol{\pi}$ are the dual variables (shadow prices) from the current RMP

**Optimality Condition:**
$$\text{Stop if } \max_j \bar{c}_j \leq 0 \quad \text{(minimization)}$$

Otherwise, the column with maximum reduced cost enters the basis.

**Column Generation Scheme:**
$$\text{RMP solution} \xrightarrow{\text{extract } \boldsymbol{\pi}} \text{Pricing Subproblem} \xrightarrow{\text{find new column}} \text{Update RMP}$$

## Physical Intuition / Derivation

### The Motivation

Traditional LP formulations for combinatorial problems often have exponentially many variables (columns). Explicitly enumerating all columns is computationally infeasible. Column generation avoids this by:

1. **Starting small:** Initialize with a subset of "obvious" columns
2. **Smart expansion:** Only add columns that provably improve the solution
3. **Pricing oracle:** Use dual information to guide which columns to generate

### How the Pricing Subproblem Guides Search

The dual variables $\boldsymbol{\pi}$ reflect the "shadow prices"—how much each constraint would relax if given one unit of slack. When solving the pricing subproblem, we're asking:

> *Which variable, when added to the basis, gives the most improvement per unit cost?*

In the co-k-plex example:
- The RMP formulates co-k-plexes as a stable set problem in an auxiliary graph
- The dual variables encode the value of including certain vertices/edges
- The pricing subproblem becomes: "Find the highest-value induced path" (weighted by dual info)
- Since induced path finding is polynomial on chordal graphs, the entire column generation loop is polynomial

### Why This Matters

If the pricing subproblem is **hard to solve**, column generation becomes impractical. If it's **polynomial**, column generation can be a practical solution to otherwise intractable problems.

## Applications in Engineering

### 1. **Integer Programming & Combinatorial Optimization**
   - Vehicle routing problems (VRP): pricing subproblem finds optimal vehicle routes
   - Cutting stock problems: pricing finds patterns that minimize waste
   - Set partitioning: used in airline crew scheduling

### 2. **Network Design & Operations Research**
   - Telecommunications: finding optimal paths under capacity constraints
   - Supply chain: generating delivery routes with resource constraints
   - Network flow: generating paths with minimum cost

### 3. **Machine Learning & Large-Scale Optimization**
   - Structured prediction: pricing generates candidate predictions
   - Kernel methods: implicit column generation in dual space
   - Distributed optimization: each node solves local pricing subproblems

### 4. **Graph Algorithms (from source material)**
   - Finding maximum dense subgraphs (co-k-plexes) in networks
   - Identifying cliques or near-cliques in biological/social networks
   - Community detection where induced path structure is informative

## Common Mistakes / Pitfalls

### 1. **Forgetting the Dual Connection**
**Mistake:** Treating the pricing subproblem as a standalone optimization task, losing sight that it *must* use dual variables $\boldsymbol{\pi}$ from the RMP.

**Correction:** The pricing subproblem is inherently coupled to the RMP solution. Neglecting this breaks optimality convergence.

### 2. **Assuming Any Feasible Solution Suffices**
**Mistake:** Solving the pricing subproblem approximately or heuristically.

**Correction:** For optimality of column generation, you must find the *true maximum* reduced cost (or prove none exists). Approximate solutions can cause premature termination with suboptimal solutions.

### 3. **Ignoring Complexity of the Pricing Subproblem**
**Mistake:** Assuming that because column generation is elegant, the pricing subproblem will be easy.

**Correction:** Column generation is only practical if the pricing subproblem is efficiently solvable. The source material's insight—that pricing for co-k-plexes is a polynomial induced path problem—is a *major theoretical result precisely because pricing is often hard*.

### 4. **Not Recognizing Problem Structure**
**Mistake:** Applying generic column generation without exploiting special structure (e.g., chordal graph properties).

**Correction:** The source shows that *graph class matters*: induced paths are polynomial on chordal graphs but may be intractable on general graphs. Recognize your problem's underlying structure.

### 5. **Cycling and Degeneracy**