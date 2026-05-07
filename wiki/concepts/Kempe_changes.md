# Kempe Changes

## Definition

A **Kempe change** is a local recoloring operation on a graph that systematically swaps colors within a connected component of a subgraph induced by two specific colors. Formally, given a proper $k$-coloring of a graph $G$ and two colors $a$ and $b$, the **$ab$-Kempe chain** is a maximal connected subgraph of $G$ containing only vertices colored $a$ or $b$. A Kempe change swaps all instances of color $a$ with color $b$ within this chain, preserving the properness of the coloring.

In the context of graph reducibility (particularly in planar graph four-coloring proofs), a coloring of a **ring** $R$ (the boundary of a configuration $Z$) is called **$i$-extendible** if the coloring can be extended to a full coloring of the entire configuration using at most $i$ Kempe changes applied to the external graph $G \setminus V(Z)$.

## Key Concepts

### Kempe Chain Structure

For a $k$-coloring $\phi: V(G) \to \{1, 2, \ldots, k\}$ and colors $a, b \in \{1, \ldots, k\}$, the $ab$-Kempe chain containing vertex $v$ is:

$$K_{ab}(v) = \text{connected component of } \{u \in V(G) : \phi(u) \in \{a,b\}\} \text{ containing } v$$

The Kempe swap operation $\text{KempeSwap}_{ab}(K_{ab}(v))$ recolors all vertices in $K_{ab}(v)$ by swapping their $a$ and $b$ colors:

$$\phi'(u) = \begin{cases} b & \text{if } \phi(u) = a \text{ and } u \in K_{ab}(v) \\ a & \text{if } \phi(u) = b \text{ and } u \in K_{ab}(v) \\ \phi(u) & \text{otherwise} \end{cases}$$

The result $\phi'$ remains a proper coloring.

### Reducibility via Kempe Changes

A configuration $Z$ with ring $R$ is **$C_i$-reducible** with respect to reducer $X$ if:

1. $X \subseteq E(Z) \setminus E(R)$ is a non-empty edge set
2. Contracting $X$ produces a loopless graph $\widehat{Z}/X$
3. Every valid 4-coloring of $R$ induced from a 4-coloring of $\widehat{Z}/X$ is $i$-extendible

The "$i$-extendible" condition means: by applying at most $i$ Kempe changes in the subgraph $G \setminus V(Z)$, the coloring of $R$ can be extended to a complete proper coloring of $Z$.

## Physical Intuition / Derivation

### Why Kempe Changes Work

The elegance of Kempe changes lies in their **local invertibility**: swapping colors $a$ and $b$ twice returns to the original coloring. This reversibility is crucial in proofs of four-color theorem via reducibility, where:

- Fixing a boundary coloring on ring $R$
- We need to show the interior can always be colored
- If a naive greedy coloring fails, a Kempe change in the exterior graph ($G \setminus V(Z)$) can "rearrange" the colors of $R$ into a state that *is* extendible

### Algorithmic Construction

The computational approach for checking $C_i$-reducibility follows an **iterative refinement** process:

**Round 0:** Identify which colorings of $R$ are **0-extendible** (directly extendible without any Kempe changes).

**Round $i$:** For each remaining unclassified coloring $\phi$ of $R$, search for an *improving Kempe change* — a swap in colors $a, b$ along the $ab$-chain in $G \setminus V(Z)$ that produces a $(i-1)$-extendible coloring.

**Key insight:** If for colors $a,b$ there exists an $ab$-Kempe chain from vertex $v_1$ to $v_j$ on the ring walk, there *cannot* simultaneously exist a $cd$-Kempe chain (for complementary colors $c,d$) connecting vertices in $\{v_2, \ldots, v_{j-1}\}$ to $\{v_{j+1}, \ldots, v_\ell\}$. This mutual exclusion constraint bounds the search space.

## Classical Examples

### Birkhoff Diamond (0-Reducible)
Two adjacent triangles with all four vertices of degree 5. Birkhoff [6] proved this configuration is **$D$-reducible** (0-extendible): any 4-coloring of the boundary can be extended without any Kempe changes.

### Franklin's Configuration (1-Reducible)
A degree-6 vertex surrounded by six degree-6 vertices. The reducer identifies all six degree-4 ring vertices into a single vertex. This configuration is **$C$-reducible** (1-extendible): any boundary coloring requires at most one Kempe change in the exterior.

## Applications in Engineering

### Graph Coloring in Scheduling
Kempe changes are used in **register allocation** compilers and **timetable scheduling**:
- Vertices = variables/events; colors = registers/time slots
- When initial greedy coloring fails, Kempe changes reassign registers locally to resolve conflicts without complete recoloring

### Network Frequency Assignment
In cellular networks with interference constraints:
- Frequency assignments ($k$-coloring) may require local adjustments
- Kempe changes allow swapping frequency pairs in a localized region without disrupting distant assignments

### VLSI Circuit Layout
Planar graph coloring for circuit design:
- Reducibility checks determine which subconfigurations can be locally optimized
- Kempe changes guide incremental improvement algorithms

## Common Mistakes / Pitfalls

1. **Assuming arbitrary color sw