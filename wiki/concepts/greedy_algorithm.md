# Greedy Algorithm

## Definition

A **greedy algorithm** is a problem-solving approach that constructs a solution by making a sequence of locally optimal choices at each step, with the hope that these local optima will lead to a global optimum. At each decision point, the algorithm selects the option that appears best according to a predefined greedy criterion, without reconsidering or backtracking previous choices.

Formally, given a problem instance with a set of candidate elements $C$, a greedy algorithm maintains a solution set $S$ and iteratively adds elements to $S$ according to a selection function $f: C \to \mathbb{R}$ that ranks remaining candidates. The algorithm terminates when no further elements can be added or a stopping criterion is met.

## Key Equations

### Greedy Selection Criterion

At iteration $i$, the algorithm selects element $c^* \in C \setminus S$ satisfying:

$$c^* = \arg\max_{c \in C \setminus S} f(c)$$

where $f(c)$ is the greedy evaluation function that quantifies the local desirability of adding element $c$ to the current solution.

### Solution Construction

The iterative solution is:

$$S_i = S_{i-1} \cup \{c^*_i\}$$

with $S_0 = \emptyset$, where $c^*_i$ denotes the element selected at iteration $i$.

## Physical Intuition / Derivation

The greedy approach is motivated by intuitive decision-making: when facing sequential choices with uncertain global consequences, humans often choose the "best-looking" option immediately available.

**Why greedy can fail:** Consider scheduling jobs on a machine to minimize total completion time. A greedy strategy might process the shortest job first (Shortest Job First, SJF). For a single machine this is optimal, but when utility functions depend on completion time differently across agents (as in the source material), this myopic strategy may violate fairness: one agent with a slow job might suffer disproportionately.

**When greedy succeeds:** Greedy algorithms are guaranteed optimal when the problem exhibits:
1. **Optimal substructure**: An optimal solution contains optimal solutions to subproblems
2. **Greedy choice property**: A locally optimal choice leads toward a globally optimal solution

Classical examples where these hold:
- **Kruskal's algorithm** (minimum spanning tree): Selecting minimum-weight edges that don't create cycles
- **Dijkstra's algorithm** (shortest paths): Expanding from the closest unexplored vertex
- **Huffman coding**: Combining the two lowest-frequency nodes repeatedly

**In the scheduling context:** The source material proposes a "greedy-based alternative" to binary search for fair scheduling. This suggests applying greedy selection of job orderings to maximize the minimum utility—but such a greedy approach must be carefully designed and may only guarantee approximate solutions unless the problem structure allows.

## Applications in Engineering

### 1. **Scheduling and Sequencing**
- **Job scheduling**: SJF for minimizing average completion time (uniprocessor systems)
- **Machine scheduling**: Assigning jobs to machines with earliest-deadline-first (EDF) for deadline satisfaction
- **Multi-agent fairness**: Ordering jobs to maximize minimum agent satisfaction (source material context)

### 2. **Network Optimization**
- **Spanning trees**: Kruskal's and Prim's algorithms construct minimum-weight spanning trees greedily
- **Routing**: Greedy routing selects the next hop with best metric (distance, latency, cost)
- **Resource allocation**: Assigning bandwidth or memory to processes based on demand priority

### 3. **Facility Location and Clustering**
- **k-means initialization**: Selecting initial cluster centers greedily by distance
- **Sensor network deployment**: Placing sensors to maximize coverage with minimum cost

### 4. **Supply Chain and Logistics**
- **Vehicle routing**: Nearest neighbor heuristic for delivery routes
- **Inventory management**: Greedy reordering policies based on current stock levels

### 5. **Machine Learning**
- **Feature selection**: Incrementally adding features that most improve model performance
- **Decision trees**: Selecting splits that maximize information gain (ID3, C4.5 algorithms)

## Common Mistakes / Pitfalls

### 1. **Assuming Greedy Implies Optimal**
Many beginners implement greedy algorithms without verifying that the problem satisfies optimal substructure and the greedy choice property. Result: suboptimal or incorrect solutions.

**Example**: Greedy scheduling for *multiple* machines or with precedence constraints often fails. For fairness scheduling with time-dependent utilities, naive greedy job ordering may severely disadvantage slow jobs.

### 2. **Poor Choice of Greedy Criterion**
The selection function $f(c)$ is problem-dependent. Using the "obvious" criterion without justification often leads to poor results.

**Example**: In scheduling, "process longest jobs first" might seem natural to clear them, but it typically increases mean completion time compared to SJF.

### 3. **Ignoring Tie-breaking**
When multiple elements have equal $f(c)$ value, the order of selection can significantly impact final solution quality. This is often overlooked.

### 4. **No Approximation Analysis**
When greedy doesn't guarantee optimality, practitioners should quantify the approximation ratio:
$$\rho = \frac{\text{Greedy Solution}}{\text{Optimal Solution}}$$

Greedy algorithms for NP-hard problems (like bin packing, set cover, or fairness scheduling with release dates) deserve explicit approximation bounds.

### 5. **Confusing Greedy with Dynamic Programming**
Greedy constructs a solution sequentially with no reconsideration. Dynamic programming solves subproblems and recombines them. Don't conflate these paradigms.

---

## See Also

- [[Binary Search Algorithm]]: The source paper uses binary search on the minimum utility parameter as an alternative to greedy for fair scheduling
- [[Dynamic Programming]]: Contrasting approach that reconsidering decisions; appropriate when greedy fails
- [[Approximation Algorithm]]: Framework for analyzing greedy heuristics on NP-hard problems
- [[Scheduling Theory]]: Domain where greedy algorithms are extensively applied and analyzed
- [[Optimal Substructure]]: Structural property that permits greedy or DP approaches

---

## Sources

- Nicosia, G., Pacifici, A., & Pferschy, U.