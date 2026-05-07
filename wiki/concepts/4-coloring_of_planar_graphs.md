# 4-coloring of planar graphs

## Definition

The **4-coloring problem for planar graphs** asks whether every planar graph can be properly colored using at most 4 colors, such that no two adjacent vertices share the same color.

**Formal Statement (Four Color Theorem):** Every planar graph $G = (V, E)$ admits a proper vertex coloring $c: V \to \{1, 2, 3, 4\}$ where for all edges $(u,v) \in E$, we have $c(u) \neq c(v)$.

A **planar graph** is a graph that can be drawn on a plane without edge crossings. By Euler's formula, such graphs satisfy $|E| \leq 3|V| - 6$, making them sparse.

**Key Related Terms:**
- **Proper coloring:** A vertex coloring where adjacent vertices have different colors
- **D-reducible configuration:** A subgraph structure that cannot appear in a minimal counterexample to the Four Color Theorem (FCT)
- **Minimal counterexample:** A graph requiring 5 or more colors, but every proper subgraph requires ≤4 colors
- **Kempe chain:** A connected subgraph of alternating colors used in inductive recoloring arguments
- **Obstructing cycle:** A cycle structure that prevents certain coloring patterns and cannot exist in a minimal counterexample

## Key Equations

**Chromatic number bound for planar graphs:**
$$\chi(G) \leq 4 \text{ for all planar graphs } G$$

**Vertex-edge relationship (Euler's formula for connected planar graphs):**
$$|V| - |E| + |F| = 2$$

where $|F|$ is the number of faces. This implies:
$$|E| \leq 3|V| - 6$$

**Time complexity of modern 4-coloring algorithms:**
$$T(n) = O(n \log n)$$

where $n = |V|$ is the number of vertices. The authors discuss achieving $O(n \log n)$ performance through strategic use of $D$-reducible configurations (numbering >8,200 in their approach).

**Parallel complexity lower bound:**
$$T_{\text{parallel}} = \Omega(n) \text{ rounds (local model)}$$

This shows that Kempe chain operations cannot be efficiently parallelized.

## Physical Intuition / Derivation

### Why Planar Graphs Matter

Planar graphs model real-world networks: circuit layouts, road maps, geographic regions, and printed circuit boards. Unlike general graphs (which may require unbounded colors), planar graphs have intrinsic geometric constraints that limit chromatic number.

### The Proof Strategy: Reducibility

The proof of the FCT (Appel-Haken, 1976 onwards) uses **proof by contradiction**:

1. **Assume** a minimal counterexample exists: a planar graph $G$ requiring 5 colors, but every proper subgraph requires ≤4 colors.

2. **Unavoidable set:** Any planar graph must contain at least one configuration from a finite "unavoidable set." Early proofs used 1,482 configurations (Appel-Haken); modern proofs use >8,200 **D-reducible configurations**.

3. **Reducibility:** For each configuration in the unavoidable set, show that if it appears in a graph, that graph **cannot** be a minimal counterexample. This is done via:
   - Removing the configuration
   - 4-coloring the resulting smaller graph (by inductive hypothesis)
   - Recoloring/patching the configuration back in using Kempe chains

4. **Conclusion:** Since every unavoidable configuration is reducible, no minimal counterexample can exist. Therefore, all planar graphs are 4-colorable.

### Why D-reducibility?

**D-reducibility** is a restricted form of reducibility that:
- Applies only to specific vertex neighborhoods (discharging rules)
- Allows more configurations to qualify as reducible
- Enables linear-time enumeration of a sufficient set
- Makes computer verification tractable

The authors use >8,200 D-reducible configurations to guarantee a **linear number** of configurations appear in any planar graph, enabling the $O(n \log n)$ algorithm.

## Applications in Engineering

### 1. **VLSI and Circuit Design**
- **Printed Circuit Board (PCB) routing:** Planar subgraphs model trace layouts; 4-coloring assigns frequency bands or routing layers to avoid electromagnetic interference
- **Layer assignment:** Different metal layers in semiconductor fabrication can be represented as colors in a planar embedding

### 2. **Register Allocation in Compilers**
- **Interference graphs** in register assignment are often planar or near-planar
- **4-coloring** assigns variables to 4 available CPU registers, minimizing memory spills
- Reduces code size and improves execution speed

### 3. **Frequency Assignment**
- **Cellular networks:** Assign frequency bands to cell towers (vertices) such that adjacent towers use different frequencies
- Planar or nearly-planar topologies arise in geographic coverage maps
- Guarantees interference-free communication

### 4. **Map Coloring and Geographic Information Systems (GIS)**
- **Political boundaries:** Color regions such that adjacent regions have different colors
- **Land use planning:** Assign compatible uses (colors) to adjacent regions

### 5. **Scheduling and Timetabling**
- **Graph-based scheduling:** Vertices = tasks/events; edges = conflicts
- Planar structure arises in spatial or hierarchical scheduling problems
- 4-coloring finds valid time slots or room assignments

### 6. **Network Design and Topology**
- **Planar network embeddings:** Determine crossing-free layouts of distributed systems
- **4-coloring** supports domain partitioning, load balancing, or resource allocation

## Common Mistakes / Pitfalls

### 1. **Confusing 4-colorability with non-planarity**
- **Mistake:** Assuming any graph requiring >4 colors must be non-planar
- **Reality:** All planar graphs are 4-colorable, but the converse is not true. Some non-planar graphs are 4-colorable; others require 5+ colors (e.g., $K_5$, $K_{3