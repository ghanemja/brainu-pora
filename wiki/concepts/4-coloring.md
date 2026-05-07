# 4-Coloring

## Definition

A **4-coloring** is an assignment of one of four colors to each vertex of a graph such that no two adjacent vertices receive the same color. In the context of the Four Color Theorem and reducibility theory, a 4-coloring of a graph $G$ is called **$i$-extendible** with respect to a subgraph configuration $Z$ if any 4-coloring of the ring $R$ (the boundary of $Z$) can be extended to a valid 4-coloring of the entire configuration $Z$ using at most $i$ **Kempe changes**—local recoloring operations that swap colors along alternating paths.

A configuration $Z$ (with exterior ring $R$) is said to be **$C_i$-reducible** with respect to a reducer edge-set $X \subseteq E(Z) \setminus E(R)$ if every 4-coloring of $R$ that arises from some 4-coloring of the contracted graph $Z/X$ is $i$-extendible. A configuration with $i = 0$ is called **$D$-reducible** (directly reducible), and with $i = 1$ is called **$C$-reducible** (Kempe-reducible).

## Key Equations

**Kempe Chain Definition:**
If $\{a, b\}$ and $\{c, d\}$ are pairs of complementary colors in a partial coloring, an **$ab$-Kempe chain** is a maximal alternating path where consecutive vertices alternate between colors $a$ and $b$.

**Extendibility Criterion:**
A coloring of ring $R$ is $i$-extendible to configuration $Z$ if there exist at most $i$ Kempe changes applied to the exterior graph $G \setminus V(Z)$ such that the resulting coloring of $R$ admits a valid extension into $Z$.

**Notation:**
- $Z/X$ = graph obtained by contracting all edges in $X$
- $|R|$ = number of vertices on the boundary ring
- Number of possible 4-colorings of $R$ ≈ $3^{|R|-1}$ (accounting for symmetry)

## Physical Intuition / Derivation

### Why 4-Coloring Matters

The 4-coloring problem originates from graph coloring, where the goal is to assign minimal colors to vertices such that adjacent vertices differ in color. The **Four Color Theorem** states that every planar graph is 4-colorable, a result proven (infamously) using extensive computer verification.

### Reducibility Strategy

Rather than verifying 4-colorability globally, reducibility theory breaks the problem into manageable pieces:

1. **Identify a problematic configuration** $Z$ (e.g., a dense subgraph with high-degree vertices)
2. **Extract the boundary ring** $R$ — the interface between $Z$ and the rest of the graph
3. **Contract internal edges** via reducer $X$ to simplify analysis
4. **Verify extendibility computationally**: for each of the ~$3^{|R|-1}$ possible 4-colorings of $R$, confirm that it extends into $Z$

### Kempe Changes

A **Kempe change** is the key operation allowing color reorganization without violating coloring constraints. If two color classes $a$ and $b$ are present in a neighborhood, swapping them along a Kempe chain alters the coloring locally. The bound $i$ quantifies how many such swaps are needed before a coloring of $R$ can propagate into $Z$.

## Applications in Engineering

While 4-coloring is fundamentally a discrete mathematics concept, it has surprising practical applications:

### Network Design
- **Frequency assignment in wireless networks**: Assign frequencies (analogous to colors) to base stations such that adjacent stations don't interfere. A planar network layout is 4-colorable, guaranteeing at most 4 frequencies suffice.

### Scheduling & Resource Allocation
- **Exam timetabling**: Assign time slots (colors) to exams such that students don't have conflicting exams. Graph structure encodes conflicts; 4-coloring gives efficient schedules.

### VLSI & Chip Design
- **Register allocation**: Assign hardware registers to variables in compiled code. The interference graph is 4-colorable, minimizing spills to memory.

### Map Coloring (Historical)
- **Cartographic coloring**: Original motivation; 4 colors suffice for any political map so that adjacent regions have distinct colors.

### Verification & Testing
- **Configuration testing**: Reducibility checks verify that complex circuit configurations are 4-colorable by testing boundary conditions, reducing overall verification cost.

## Common Mistakes / Pitfalls

1. **Confusing "extendibility" with "validity"**: A coloring of $R$ that is $i$-extendible does *not* immediately extend to $Z$; it requires $i$ Kempe changes in $G \setminus V(Z)$ first.

2. **Ignoring the reducer constraint**: The reducer $X$ must not create loops in $Z/X$. Blindly contracting edges can destroy the structure needed for Kempe arguments.

3. **Underestimating search space**: Computing $3^{|R|-1}$ colorings grows exponentially. For $|R| = 30$, this is ~$2 \times 10^{14}$ cases—computationally prohibitive without pruning strategies.

4. **Assuming local reducibility is compositional**: If $Z_1$ is $C_1$-reducible and $Z_2$ is $C_1$-reducible, their union is *not* automatically $C_1$-reducible. Interaction effects between configurations complicate composition.

5. **Missing obstructing cycles**: When contracting edges in $X$, ensure no obstructing cycle in $G$ with all vertices in $Z$ creates unexpected loops. This constraint is subtle and often overlooked.

6. **Kempe chain behavior in bounded regions**: In a finite configuration $Z$, a Kempe chain may "wrap around" in unexpected ways. The ring topology $R$ must be carefully tracked to avoid logical errors.

## See Also

- [[Graph Coloring]] — General vertex coloring framework
- [[Kempe Chain]] — Fundamental tool for color reorganization