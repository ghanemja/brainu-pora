# H-free graphs

## Definition

An **H-free graph** is a graph $G$ that does not contain $H$ as an induced subgraph. Equivalently, $G$ is $H$-free if there is no subset of vertices in $G$ whose induced subgraph is isomorphic to $H$.

### Formal Definition
Let $G = (V, E)$ be a graph and $H$ be a fixed graph. Then $G$ is **$H$-free** if and only if:
$$\text{No induced subgraph of } G \text{ is isomorphic to } H$$

This is denoted as $G \in \text{Free}(H)$, where $\text{Free}(H)$ is the class of all $H$-free graphs.

### Key Distinction
- **Induced subgraph**: A subgraph obtained by selecting a subset $S \subseteq V$ and including all edges of $G$ between vertices in $S$
- **Subgraph** (general): May omit edges between selected vertices
- $H$-freeness is defined on *induced* subgraphs, making the constraint structural and strong

## Key Equations

### Computational Complexity Framework
For a problem $\mathcal{P}$ and graph class $\mathcal{C} = \text{Free}(H)$:

$$\text{Complexity}(\mathcal{P}, \text{Free}(H)) \in \begin{cases} 
\text{P} & \text{(polynomial-time solvable)} \\
\text{NP-complete} & \text{(intractable)} \\
\text{XP} & \text{(fixed-parameter tractable in some parameter)}
\end{cases}$$

### Characterization by Forbidden Induced Subgraph
A graph class $\mathcal{G}$ can be characterized as:
$$\mathcal{G} = \text{Free}(\mathcal{H}) = \bigcap_{H \in \mathcal{H}} \text{Free}(H)$$

where $\mathcal{H}$ is a set of forbidden induced subgraphs.

## Physical Intuition / Derivation

### Why Induced Subgraphs Matter

The restriction to *induced* subgraphs is fundamental because:

1. **Structural constraint**: Forbidding $H$ as an induced subgraph forbids not just the edge pattern of $H$, but also all relationships *between* those vertices. This is far more restrictive than just forbidding $H$ as a subgraph.

2. **Graph classes with structure**: Many natural graph classes are naturally $H$-free:
   - **Triangle-free graphs**: $\text{Free}(K_3)$ (bipartite graphs have no odd cycles, so no triangles)
   - **Claw-free graphs**: $\text{Free}(K_{1,3})$ (important in matching theory)
   - **$P_4$-free graphs** (cographs): No induced path of length 4
   - **Chordal graphs**: $\text{Free}(P_4, C_k \text{ for } k \geq 4)$ (every cycle has a chord)

3. **Complexity reduction**: Forbidding structure can make hard problems tractable. A problem that is NP-hard on general graphs may become polynomial-time solvable on $H$-free graphs for certain $H$.

### Example Construction
Consider $K_{1,3}$ (star with 3 leaves):
$$K_{1,3} = \text{(central vertex connected to 3 independent vertices)}$$

A graph $G$ is $K_{1,3}$-free if no vertex has 3 or more non-adjacent vertices among its neighbors. This is a strong structural constraint.

## Applications in Engineering

### 1. **Algorithms & Computational Complexity**
- **Parameterized complexity**: Study of problems on $H$-free graphs reveals which structural restrictions make intractable problems solvable
- **Approximation algorithms**: Better approximation ratios achievable on restricted graph classes
- **Heuristics design**: Exploit $H$-free structure for more efficient search algorithms

### 2. **Coloring Problems** (as in source material)
- **b-Chromatic Number**: Finding minimum colors such that each color class has a b-chromatic vertex (adjacent to all other colors)
- **Fall Chromatic Number**: Each color class has exactly one b-chromatic vertex
- **Complexity result**: These are NP-complete on general graphs but become polynomial-time solvable on specific $H$-free graph classes

### 3. **Network Design**
- **Conflict resolution**: Forbidden subgraph structure models incompatibility constraints
- **Wireless networks**: Ensuring no interference patterns (forbidden configurations) exist
- **Scheduling**: Graph coloring with structural constraints from $H$-freeness

### 4. **Constraint Satisfaction**
- **CSP formulations**: Forbidden induced subgraphs encode incompatible variable assignments
- **Boolean satisfiability**: Clause interaction graphs that avoid certain substructures

### 5. **Combinatorial Optimization**
- **Matching & independence**: Problems on $H$-free graphs often admit better algorithms (e.g., maximum matching in claw-free graphs)
- **Vertex cover, dominating set**: Complexity often decreases on forbidden subgraph classes

## Common Mistakes / Pitfalls

### 1. **Confusing Induced vs. Non-induced Subgraphs**
**Mistake**: "A graph is triangle-free if it has no $K_3$ edges"
**Correction**: $K_3$-freeness means no three vertices all connected pairwise (induced subgraph). A graph with edges $\{a-b, b-c, a-c\}$ is never $K_3$-free; a path $P_3$ (three vertices $a-b-c$ with only edges $a-b, b-c$) *is* $K_3$-free.

### 2. **Assuming NP-hardness Persists Universally**
**Mistake**: "If problem $\mathcal{P}$ is NP-hard on general graphs, it's NP-hard on $H$-