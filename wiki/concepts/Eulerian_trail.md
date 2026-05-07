# Eulerian Trail

## Definition

An **Eulerian trail** is a walk in a graph that traverses every edge exactly once. More formally:

Given a graph $G = (V, E)$, an Eulerian trail is a sequence of vertices $v_0, v_1, \ldots, v_m$ where:
- Each consecutive pair $(v_i, v_{i+1})$ corresponds to a distinct edge in $E$
- Every edge in $E$ appears exactly once in this sequence
- The trail may be open (start and end vertices differ) or closed/cyclic (start equals end, also called an **Eulerian circuit** or **Eulerian cycle**)

An Eulerian trail exists in a connected graph if and only if:
- **For cyclic trails:** All vertices have even degree
- **For open trails:** Exactly two vertices have odd degree (these are the start and end points)

## Key Equations

**Degree condition for Eulerian trails:**

$$\text{degree}(v) \equiv 0 \pmod{2} \quad \forall v \in V \quad \Rightarrow \quad \text{Eulerian circuit exists}$$

$$\#\{v : \deg(v) \text{ is odd}\} = 2 \quad \Rightarrow \quad \text{Eulerian trail exists (open)}$$

**Computational complexity of enumeration:**

For enumerating all Eulerian trails, the time complexity using compressed state-tree representations is:

$$O(m + z_T)$$

where $m = |E|$ is the number of edges and $z_T$ is the output size (number of distinct Eulerian trails).

## Physical Intuition / Derivation

### Historical Context: The Seven Bridges Problem

The concept originates from Leonhard Euler's 1735 solution to the Seven Bridges of Königsberg problem. Residents wondered whether they could walk across all seven bridges exactly once. Euler abstracted the problem into graph theory: vertices represent land masses, edges represent bridges.

### Why Eulerian Trails Matter

Intuitively, an Eulerian trail represents an efficient traversal of a network where **every connection must be used exactly once**. This avoids redundant coverage—crucial in applications where:
- Repetition is costly (fuel in vehicle routing)
- Completeness is mandatory (circuit board testing)
- Verification requires full coverage (network inspection)

### Hierholzer's Algorithm

The standard algorithm to find *one* Eulerian trail runs in $O(m)$ time:

1. Start from any vertex with odd degree (or any vertex if all degrees are even)
2. Follow edges greedily, removing each edge after traversal
3. When stuck at a vertex with no outgoing edges, backtrack and insert the trail at that point
4. Continue recursively until all edges are consumed

This greedy-with-backtracking approach naturally avoids getting "trapped" in subgraphs because the degree condition guarantees an exit from any sub-component.

### Enumeration Challenge

Finding *all* Eulerian trails is fundamentally harder. A naive approach enumerates all trails individually, which can be exponential. Modern approaches use **state compression**: 

- **State tree:** Represents decision points where multiple continuations of a partial trail are possible
- **Branching states:** States where the prefix can be completed in multiple ways
- **Compression rules:** Collapse linear (non-branching) paths to reduce tree size from exponential to $O(m + z_T)$

**Compression Rule 1 (Forced edges):** If a vertex has exactly one outgoing edge, that edge must be used when entering the vertex. Contract such nodes with their neighbors.

**Compression Rule 2 (SCC-respecting):** If a vertex has one outgoing edge within its strongly connected component and one edge leaving it, the within-SCC edge must come first. This rule exploits graph structure to identify forced orderings.

## Applications in Engineering

### 1. **Route Planning & Vehicle Routing**
- **Problem:** A snow plow or street sweeper must traverse every street in a city exactly once to minimize travel time
- **Application:** Eulerian trail algorithms solve the "Chinese Postman Problem" (Eulerian trail with minimum repeats if no pure Eulerian trail exists)

### 2. **Printed Circuit Board (PCB) Testing**
- **Problem:** Automated test probes must visit every connection point on a circuit board
- **Application:** Enumerate valid probe paths that cover all connections without repeating, minimizing equipment stress and test time

### 3. **Network Topology Verification**
- **Problem:** Verify that every link in a network is functional by traversing each exactly once
- **Application:** Audit packet paths or optical link validation in telecommunications networks

### 4. **DNA Sequence Assembly**
- **Problem:** Reconstruct a DNA sequence from overlapping fragments (de Bruijn graphs)
- **Application:** Eulerian path algorithms efficiently assemble genomes by finding paths through overlap graphs

### 5. **Robotics & Motion Planning**
- **Problem:** Plan a robot arm's path through a manufacturing workspace that must inspect/interact with every fixture
- **Application:** Generate collision-free motions using Eulerian trails in configuration-space graphs

## Common Mistakes / Pitfalls

### 1. **Confusing "Connected" with "Eulerian"**
A connected graph may not have an Eulerian trail. Always check degree conditions first.

**Wrong:** "This graph is connected, so it has an Eulerian trail"  
**Right:** "This connected graph has an Eulerian trail iff it has 0 or 2 vertices of odd degree"

### 2. **Forgetting Directionality**
Degree conditions differ for directed graphs. In a directed graph, Eulerian trails require:
- **In-degree** = **out-degree** for all vertices (for cyclic trails)
- Exactly one vertex with out-degree exceeding in-degree by 1, and one with in-degree exceeding out-degree by 1 (for open trails)

### 3. **Not Accounting for Multiplicity**
Multiple edges between the same pair of vertices are allowed and must all be traversed. The algorithm doesn't ignore "redundant" edges.

### 4. **Assuming Unique Solutions**
Graphs often have many Eulerian trails (exponentially many). If uniqueness is required, additional constraints must be added.

### 5. **Inefficient