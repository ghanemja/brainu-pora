# Bipartite Graph

## Definition

A **bipartite graph** is an undirected graph $G = (V, E)$ whose vertex set $V$ can be partitioned into two disjoint subsets $V_1$ and $V_2$ (where $V_1 \cup V_2 = V$ and $V_1 \cap V_2 = \emptyset$) such that every edge in $E$ connects a vertex in $V_1$ to a vertex in $V_2$. Equivalently, a bipartite graph is a graph that contains **no odd-length cycles**.

In formal notation:
$$G = (V_1 \cup V_2, E) \text{ where } E \subseteq V_1 \times V_2$$

A **complete bipartite graph** $K_{m,n}$ has $m$ vertices in $V_1$ and $n$ vertices in $V_2$, with every vertex in $V_1$ connected to every vertex in $V_2$, yielding $mn$ edges.

## Key Equations

**Bipartiteness Characterization (König's Theorem):**
A graph $G$ is bipartite if and only if it is **2-colorable**, meaning there exists a proper vertex coloring using exactly 2 colors:
$$\chi(G) = 2$$

**Cycle Condition:**
A connected graph $G$ is bipartite if and only if it contains no cycles of odd length. For any cycle in $G$:
$$\text{All cycles have even length} \iff G \text{ is bipartite}$$

**Maximum Matching in Bipartite Graphs (Hall's Theorem):**
For a bipartite graph with parts $V_1$ and $V_2$ where $|V_1| \leq |V_2|$, a perfect matching from $V_1$ to $V_2$ exists if and only if for every subset $S \subseteq V_1$:
$$|N(S)| \geq |S|$$
where $N(S)$ denotes the neighborhood (set of adjacent vertices) of $S$ in $V_2$.

## Physical Intuition / Derivation

The bipartite structure emerges naturally from **classification and relationship problems**:

1. **Two-Party Systems:** Consider a system with two fundamentally distinct types of entities. A bipartite structure implies entities of the same type never interact directly—only across types. For example:
   - Workers and Jobs: edges represent "worker capable of performing job"
   - Students and Courses: edges represent "student enrolled in course"

2. **Why No Odd Cycles?** Imagine trying to 2-color a graph by assigning alternating colors along any path. If you encounter an odd cycle, you return to your starting vertex with the *opposite* color—a contradiction. This geometric constraint is equivalent to the absence of odd cycles.

3. **Relation to Linear Systems:** The source material demonstrates bipartite graph detection in the context of **constraint satisfaction**: determining whether a subset of a graph's variables can satisfy a linear system (corresponding to a 2-coloring with values in a specific set). When edges represent linear constraints, a bipartite structure guarantees certain algebraic properties hold.

## Applications in Engineering

### 1. **Network Flow & Matching Problems**
- **Personnel Assignment:** Assign $n$ workers to $m$ tasks optimally using bipartite matching algorithms (Hungarian Algorithm, Hopcroft-Karp). Edges weight worker-task compatibility.
- **Resource Allocation:** In data centers, match computational tasks to available servers; in hospitals, match patients to medical procedures.

### 2. **Circuit Design & VLSI**
- **Standard Cell Placement:** Partition circuit components into two groups (e.g., logic gates and routing channels) where connections flow only between groups.
- **Checkerboard Coloring:** In integrated circuit design, use bipartite structure to ensure alternating placement of complementary circuit elements.

### 3. **Scheduling & Project Management**
- **Time-Machine Scheduling:** Partition tasks into two phases; edges represent precedence constraints across phases. Bipartite structure simplifies critical path analysis.
- **Shift Scheduling:** Match workers (one partition) to time slots (other partition) ensuring coverage constraints.

### 4. **Recommendation Systems**
- **User-Item Graphs:** Bipartite structure with users on one side and products/content on the other. Edges represent purchases, ratings, or interactions. Used in collaborative filtering.

### 5. **Document Analysis & Information Retrieval**
- **Term-Document Matrices:** Create bipartite graphs where one partition is terms (words) and the other is documents. Detect communities or optimize clustering.

### 6. **Distributed Computing & Load Balancing**
- **Server-Client Networks:** Partition into servers and clients; edges represent communication links. Bipartite structure enables efficient routing and load balancing algorithms.

### 7. **Cryptography & Constraint Satisfaction** (as per source material)
- **Min-CSP Problems:** When solving constraint satisfaction problems (e.g., Min-2-Lin over $\mathbb{Z}_4$), identifying bipartite subgraphs of constraints reduces problem complexity. Variables forming a bipartite subset can be satisfied with fewer constraint deletions.

## Common Mistakes / Pitfalls

1. **Confusing "2-colorable" with "2-partite":** All bipartite graphs are 2-colorable, but 2-coloring alone doesn't define bipartiteness without the *partition property*. A 2-coloring is a necessary and sufficient characterization, not a separate concept.

2. **Overlooking disconnected components:** A disconnected graph is bipartite if *each* connected component is bipartite. Checking only one component is insufficient.

3. **Assuming odd cycles are obvious:** In large graphs, non-obvious odd cycles can hide. Use BFS/DFS algorithms rather than visual inspection:
   ```
   A graph with a 5-cycle plus a 6-clique (source material example):
   5-cycle (odd) makes the component non-bipartite.
   The 6-clique alone is NOT bipartite (contains triangles).
   ```

4. **Misapplying matching theorems:** Hall's Theorem applies to **perfect matchings**. For maximum matchings in non-perfect scenarios, use König-Egervá