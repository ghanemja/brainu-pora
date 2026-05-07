# Fall Achromatic Number

## Definition

The **fall achromatic number** of a graph $G$, denoted $\psi_f(G)$, is the maximum number of colours $k$ in a proper $k$-colouring of $G$ such that **every colour class consists entirely of b-chromatic vertices**.

A vertex $v$ in a proper colouring is **b-chromatic** if it is adjacent to at least one vertex of every other colour in the colouring. In other words, a b-chromatic vertex "witnesses" the presence of all other colour classes through its neighbourhood.

The fall achromatic number represents the most restrictive variant in the b-chromatic framework:
- **Fall Achromatic:** All vertices in every colour class are b-chromatic
- **Tight b-Chromatic:** Exactly one b-chromatic vertex per colour class
- **Fall Chromatic:** At least one b-chromatic vertex per colour class
- **b-Chromatic:** Standard proper colouring (no b-chromatic requirement)

## Key Equations

For a proper $k$-colouring $c: V(G) \to \{1, 2, \ldots, k\}$, let $C_i = c^{-1}(i)$ denote the colour class of colour $i$.

A colouring is **fall achromatic** if and only if:

$$\forall i \in \{1, 2, \ldots, k\}, \quad \forall v \in C_i: \left|\{c(u) : u \in N(v)\}\right| = k - 1$$

where $N(v)$ denotes the neighbourhood of $v$.

The fall achromatic number satisfies:

$$\psi_f(G) = \max\{k : \exists \text{ a fall achromatic } k\text{-colouring of } G\}$$

### Relationship to Other Parameters

$$\chi(G) \leq \psi_f(G) \leq \psi(G) \leq \psi_b(G)$$

where:
- $\chi(G)$ = chromatic number
- $\psi_f(G)$ = fall achromatic number
- $\psi(G)$ = achromatic number
- $\psi_b(G)$ = b-chromatic number

## Physical Intuition / Derivation

### Motivation from Standard Colouring

Classical graph colouring minimizes the number of colours needed while respecting the adjacency constraint. The fall achromatic number inverts this perspective: **maximize the number of colours while imposing a stronger structural constraint on the colouring**.

### The b-Chromatic Requirement

For a vertex to be b-chromatic, it must be "maximally connected to the colour structure":

- It has the same colour as other vertices in its class
- It reaches all other colour classes directly through its neighbours
- This implies the vertex is in some sense a "representative" of its colour class

### Why Fall Achromatic is Restrictive

The requirement that **all** vertices in a colour class be b-chromatic is very strong:

1. **Degree constraint:** If colour class $C_i$ has size $|C_i| \geq 2$, every vertex in $C_i$ must have degree at least $k-1$ (to touch all other $k-1$ colour classes)

2. **Global structure:** The induced subgraph on vertices of different colours must form a dense bipartite-like structure between colour classes

3. **Example:** In a complete graph $K_n$, every vertex has degree $n-1$, and any proper $n$-colouring (where each vertex gets a unique colour) trivially satisfies the fall achromatic property since each colour class has size 1. Thus $\psi_f(K_n) = n$.

## Applications in Engineering

### Network Design and Reliability

**Sensor Networks:** Assign sensor nodes to $k$ groups (colours) such that each sensor in a group can communicate with representatives from all other groups. The fall achromatic number represents the maximum number of independent functional groups achievable under this communication constraint.

**Data Center Network Topology:** Partition servers into service classes where every server must maintain connectivity to all service classes. Fall achromatic colourings ensure fault tolerance and load balancing across the network hierarchy.

### Resource Allocation

**Register Allocation in Compilers:** In instruction scheduling, colour vertices (variables/instructions) to minimize register pressure while maximizing the number of distinct resource classes, subject to all allocated registers in a class being "fully utilized" (touching all other resource classes).

**Frequency Spectrum Management:** Assign radio frequencies to transmitters grouped by transmission class, ensuring each transmitter in a class reaches all other frequency classes for inter-channel coordination.

### Graph Clustering and Classification

**H-Free Graph Analysis:** The source paper establishes that the computational complexity of computing $\psi_f(G)$ is entirely determined by forbidden induced subgraph $H$. This provides a unified classification framework for which graph families admit efficient algorithms:
- **Polynomial-time solvable** for certain H-free families
- **NP-complete** for general graphs containing specific forbidden structures

## Common Mistakes / Pitfalls

### 1. Confusing with Achromatic Number

Students often conflate the fall achromatic number with the classical **achromatic number** $\psi(G)$. Key difference:

- **Achromatic:** At least one b-chromatic vertex per colour class
- **Fall achromatic:** All vertices in each colour class are b-chromatic

This makes $\psi_f(G) \leq \psi(G)$.

### 2. Misunderstanding Single-Vertex Colour Classes

A colour class with a single vertex $\{v\}$ **vacuously satisfies** the fall achromatic condition if $v$ is b-chromatic (which requires it to reach all other $k-1$ colour classes). This is not trivial—$v$ must have degree exactly $k-1$.

### 3. Overestimating the Parameter

The fall achromatic number is typically much smaller than the chromatic number for sparse graphs. For example, $\psi_f(P_n) = 3$ for paths (only achievable with specific colorations), while $\chi(P_n) = 2$ or