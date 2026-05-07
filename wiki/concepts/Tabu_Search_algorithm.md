# Tabu Search Algorithm

## Definition

**Tabu Search** is a metaheuristic optimization algorithm that explores the solution space of a combinatorial optimization problem by iteratively moving from one solution to neighboring solutions, while maintaining a **tabu list** (or **tabu tenure**) that prohibits recently visited solutions from being revisited within a specified number of iterations. This mechanism prevents the algorithm from cycling back to previously explored regions and helps escape local optima.

The algorithm is particularly effective for problems where:
- The solution space is discrete and large
- Exact algorithms are computationally prohibitive
- Local search alone gets trapped in local optima
- Domain-specific neighborhood structures are well-defined

## Key Equations

The fundamental update rule for Tabu Search at iteration $k$ is:

$$\mathbf{x}^{(k+1)} = \arg\min_{\mathbf{y} \in N(\mathbf{x}^{(k)}) \setminus T_k} f(\mathbf{y})$$

where:
- $\mathbf{x}^{(k)}$ = current solution at iteration $k$
- $N(\mathbf{x}^{(k)})$ = neighborhood of current solution (all feasible moves)
- $T_k$ = tabu list at iteration $k$ (set of forbidden moves/solutions)
- $f(\mathbf{y})$ = objective function value for candidate solution $\mathbf{y}$

**Aspiration Criterion** (override tabu restrictions):
$$\text{Allow move to } \mathbf{y} \text{ if } f(\mathbf{y}) < f(\mathbf{x}^*) \text{ and } \mathbf{y} \in T_k$$

where $\mathbf{x}^*$ is the best solution found so far.

The tabu list is updated by recording the **reverse move** that led to $\mathbf{x}^{(k)}$:
$$T_{k+1} = \left(T_k \setminus \{\text{moves older than tenure}\}\right) \cup \{\text{reverse of move to } \mathbf{x}^{(k+1)}\}$$

with tabu tenure typically set to $\tau \in [5, 20]$ iterations for small problems or $\tau \approx 0.05|N|$ for larger problems.

## Physical Intuition / Derivation

### The Problem with Greedy Local Search

Standard greedy local search converges quickly but gets trapped in local optima:

```
f(x)      ← Local optimum (stuck here)
  │        ╱╲
  │       ╱  ╲
  │      ╱    ╲
  │_____╱______╲_____ Global optimum (unreachable)
  └─────────────────x
```

### How Tabu Search Escapes

Tabu Search allows **uphill moves** (accepting worse solutions temporarily) to explore beyond local optima, but forbids **backtracking** to recently visited solutions:

1. **Memorization**: Store recent moves in the tabu list
2. **Forbidding**: Block moves that would undo recent progress
3. **Aspiration**: Override the tabu restriction if we find a better solution than the best known
4. **Diversification**: When stuck, restart from different initial solutions or increase neighborhood scope

**Why it works**: By preventing cycling, the algorithm is forced to explore new regions. The tabu tenure creates a time-varying penalty landscape that changes as iterations progress, allowing the same region to be revisited after enough iterations have passed.

## Applications in Engineering

### 1. **No-Wait Job Shop Scheduling** (cited source)
In Time-Sensitive Networking (TSN) scheduling on daisy-chain topologies, Tabu Search has been applied to compute no-wait schedules where streams cannot queue at switches. The algorithm explores permutations of stream routing to minimize maximum arrival time while respecting real-time constraints.

**Status**: Superseded by polynomial-time graph coloring approach for this specific problem, but demonstrates the method's effectiveness before problem-specific optimization.

### 2. **Vehicle Routing Problems (VRP)**
Optimize delivery routes minimizing distance or time. The neighborhood consists of moves like 2-opt swaps (reversing a segment of the route). The tabu list prevents immediate undoing of recent swaps.

### 3. **Facility Location and Layout Design**
Determine optimal placement of facilities to minimize total transportation/operation cost. Moves involve relocating facilities; tabu tenure prevents thrashing between adjacent configurations.

### 4. **Printed Circuit Board (PCB) Design**
Component placement and routing optimization. Neighborhoods include swapping component positions; tabu restrictions stabilize the layout evolution.

### 5. **Power Systems - Unit Commitment**
Scheduling power generation units to meet demand while minimizing cost. Moves turn units on/off; tabu lists prevent cycling through similar commitment schedules.

### 6. **Telecommunications - Network Design**
Optimize network topology, link allocation, and flow routing. Neighborhoods represent adding/removing/rerouting links.

## Common Mistakes / Pitfalls

### 1. **Tabu Tenure Too Short**
- **Problem**: Allows immediate cycling back to recently visited solutions
- **Fix**: Use empirical tuning or set $\tau \approx |N|/10$ to $|N|/5$ (neighborhood size-dependent)

### 2. **Tabu Tenure Too Long**
- **Problem**: Overly restricts the search; prevents revisiting beneficial regions even when they may have new local optima
- **Fix**: Implement **variable tabu tenure** that adapts dynamically: increase if no improvement, decrease if improvements found

### 3. **Ignoring the Aspiration Criterion**
- **Problem**: Never explores solutions better than current best, even if they're on the tabu list
- **Mistake**: Strictly enforcing the tabu list without exception
- **Fix**: Always allow a move if $f(\mathbf{y}) < f(\mathbf{x}^*)$

### 4. **Poor Neighborhood Definition**
- **Problem**: Neighborhood is too large (computationally infeasible) or too small (insufficient exploration)
- **Fix**: Domain-specific tuning; consider k-opt neighborhoods, ejection chains, or hierarchical neighborhoods

### 5