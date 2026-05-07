# edge contraction

## Definition

**Edge contraction** is a graph transformation operation that removes a node $v$ and its unique outgoing neighbor $u$ by merging them into a single node. Formally, given a directed graph $G = (V, E)$ and a node $v \in V$ with exactly one outgoing multi-edge to neighbor $u$, edge contraction:

1. Creates a new node $w$ to replace both $v$ and $u$
2. Redirects all incoming edges to $v$ to point to $w$
3. Redirects all outgoing edges from $u$ to originate from $w$
4. Removes the edge $(v, u)$

The result is a simplified graph $G' = (V', E')$ where $|V'| = |V| - 1$.

In the context of **multigraphs** (graphs with multiple edges between the same pair of nodes), edge contraction must account for edge multiplicities and preserve the multiplicity information during the merge.

## Key Equations

For a state $s$ in a graph exploration algorithm, let $G_s'$ denote the remaining graph after processing state $s$.

**Contraction condition:**
$$\text{contract}(v, u) \iff |\text{out-edges}(v)| = 1 \text{ and } \text{out-neighbor}(v) = u$$

**Multiplicity preservation in multigraphs:**
$$m_{w \to x} = \begin{cases} m_{v \to x} & \text{if } x \neq u \\ m_{v \to u} + m_{u \to x} & \text{if } x = u \text{ (self-loop)} \end{cases}$$

where $m_{a \to b}$ denotes the multiplicity of edges from node $a$ to node $b$.

## Physical Intuition / Derivation

### Why Contract?

Edge contraction serves as a **compression rule** in graph exploration algorithms. Consider traversing a graph when at node $v$ there is only one possible outgoing transition to $u$—this transition is **forced** and adds no branching complexity. By contracting $v$ and $u$:

- **Reduces state space:** Eliminates trivial forced transitions that don't represent genuine decision points
- **Simplifies analysis:** The compressed graph maintains essential structure while removing deterministic paths
- **Enables efficient algorithms:** Allows state-tree explorations (like Eulerian path algorithms) to skip over linear chains of deterministic steps

### Building Intuition with an Example

Consider a simple directed graph:
- Node $v$ with single outgoing edge to $u$
- Node $u$ with outgoing edges to $x$ and $y$

Before contraction: Any path through $v$ must pass through the forced edge to $u$.

After contraction: We merge $v$ and $u$ into node $w$, with direct edges $w \to x$ and $w \to y$. This preserves all reachability but eliminates the unnecessary intermediate step.

### Multigraph Subtlety

In multigraphs, Lemma 7.3 establishes that **crossing edges have multiplicity one**. This is crucial: when contracting in a multigraph, non-crossing edges may have multiplicity $> 1$, but this doesn't prevent contraction—we simply preserve all multiplicities through the merge.

## Applications in Engineering

### 1. **Network Routing & Optimization**
In telecommunications and road networks, edge contraction eliminates intermediate routing nodes that have only one outgoing link, simplifying routing tables and reducing computational overhead in path-finding algorithms.

### 2. **Circuit Analysis & Netlist Simplification**
In VLSI and electronic circuit design, contraction can merge buffer chains or intermediate nodes that serve no logical branching purpose, reducing circuit complexity for analysis and synthesis.

### 3. **Compiler Optimization**
In control-flow graph (CFG) analysis, basic blocks with no conditional branching can be contracted, simplifying program analysis and enabling more efficient code generation.

### 4. **Graph Algorithms & Shortest Paths**
Preprocessing graphs via contraction reduces graph size before running algorithms like Dijkstra's or Floyd-Warshall, improving runtime while preserving distances.

### 5. **State-Space Exploration**
In model checking and formal verification, contracting forced transitions reduces the state explosion problem, making exhaustive exploration computationally feasible.

## Common Mistakes / Pitfalls

### 1. **Forgetting to Preserve Multiplicities**
**Mistake:** When contracting multi-edges, treating multiple edges as a single edge.
**Correction:** Sum multiplicities correctly. If $v$ has a multi-edge of multiplicity 2 to $u$, and $u$ has a multi-edge of multiplicity 3 to $w$, the contracted edge from $w$ should combine both pieces of information appropriately.

### 2. **Losing Crossing Information**
**Mistake:** Contracting edges without verifying they are non-crossing (in Eulerian path contexts).
**Correction:** Only contract edges that cannot be identified as crossings in the current graph state. Lemma 7.3 guarantees crossings have multiplicity 1, so contracting higher-multiplicity edges is safe.

### 3. **Breaking Self-Loop Conditions**
**Mistake:** Contracting nodes with self-loops without considering Multigraph Compression Rule 2.
**Correction:** Self-loops should only be removed in specific cases—when the node has exactly one other incoming and outgoing edge, and the self-loop's starting point won't be revisited.

### 4. **Creating Consecutive Forced Transitions**
**Mistake:** Failing to apply compression rules exhaustively, leaving chains of forced transitions.
**Correction:** Apply both compression rules recursively until no more reductions are possible. Lemma 7.5 ensures this prevents forced-transition chains.

### 5. **Assuming Contraction is Lossless for All Properties**
**Mistake:** Using contraction without verifying that the graph property of interest is preserved.
**Correction:** Contraction preserves reachability and path existence, but may not preserve all metrics (e.g., maximum independent sets). Verify applicability to your problem.

## See Also

- [[Eulerian path]] – Path traversal algorithms where forced transitions arise
- [[Multigraph]] – Graph structures with multiple edges, requiring special