# internally-node-disjoint paths

## Definition

Two or more paths in a directed graph $G = (V, E)$ between nodes $s$ and $t$ are **internally-node-disjoint** if they share no common intermediate vertices. Formally, paths $P_1, P_2, \ldots, P_k$ from $s$ to $t$ are internally-node-disjoint if for any two distinct paths $P_i$ and $P_j$, their vertex sets satisfy:

$$V(P_i) \cap V(P_j) = \{s, t\}$$

That is, the paths may only intersect at the source $s$ and target $t$, but cannot share any other nodes. This is weaker than **edge-disjoint** paths (which cannot share edges) and **vertex-disjoint** paths (which cannot share any vertices at all, including endpoints).

The **maximum number of internally-node-disjoint paths** between $s$ and $t$ is bounded by the minimum vertex cut separating them—a consequence of the **Menger's Theorem** for vertices.

## Key Equations

**Menger's Theorem (Vertex Version):**
$$\text{max # internally-node-disjoint } (s,t)\text{-paths} = \text{min vertex cut separating } s \text{ and } t$$

For a fractional (weighted) variant as used in the source material:

$$w'_{s,t} = \text{minimum fractional } (s,t)\text{-cut}$$

where node weights are constrained:
- Nodes in $X$: weight $= 1$
- Nodes in $G \setminus X$: weight $\leq \frac{4^{\text{epoch}}}{L}$

The **mass function** aggregates weights across all demand pairs:
$$\text{mass}(\{w_{s,t}\}) := \sum_{(s,t) \in P} \sum_{v \in V \setminus X} w_{s,t}(v)$$

## Physical Intuition / Derivation

### Why internally-node-disjoint paths matter

Consider a communication network where:
- Each node can process one message at a time
- We need multiple independent routes from source $s$ to sink $t$
- These routes must not compete for node resources (though they may share edges)

Internally-node-disjoint paths formalize this: if $k$ such paths exist, then $k$ units of flow can be routed simultaneously without any intermediate node becoming a bottleneck.

### Connection to min-cuts

By Menger's Theorem, the maximum number of internally-node-disjoint paths equals the minimum cardinality of a **vertex cut**—a set $X \subset V$ whose removal disconnects $s$ from $t$. This duality is fundamental:

- **Lower bound (paths):** If $k$ internally-node-disjoint paths exist, any cut must contain $\geq k$ nodes
- **Upper bound (cuts):** If a cut of size $\geq k$ exists, $> k-1$ node-disjoint paths cannot exist

### Fractional relaxation (source material context)

The source material uses a **fractional min-cut** variant where:
1. Each node $v$ carries a weight $w_{s,t}(v)$ instead of unit cost
2. A fractional cut is a weight distribution such that every $(s,t)$-path has total weight $\geq 1$
3. The goal is to minimize total weight assigned

This relaxation allows:
- Smoother algorithmic analysis (avoiding integrality gaps)
- Application of linear programming techniques
- Recovery of integral path witnesses via the **Min-Cost Max-Flow (MCMF) Theorem**

### The transitive closure subtlety

The source mentions paths must exist in the **transitive closure** $G \setminus X$ rather than $G \setminus X$ directly. This means:
- Direct edges in $G \setminus X$ are respected
- Paths can be "composed" through reachability, allowing algorithmic flexibility
- Requires relaxing weight bounds by $O(1)$ factor to recover witnesses

## Applications in Engineering

### 1. Network Routing & Resilience
- **Multipath routing** in data center networks: Internally-node-disjoint paths ensure that a single node failure doesn't eliminate all alternative routes
- **SRLG-disjoint paths** (Shared Risk Link Group): Generalization avoiding single points of failure

### 2. Power Grid Reliability
- Locating critical nodes whose failure would disconnect generators from loads
- Assessing grid robustness: minimum node cuts indicate vulnerability

### 3. Transportation Networks
- Analyzing vulnerability of hub-and-spoke systems
- Finding critical road/rail intersections whose closure isolates regions

### 4. Chip Design & VLSI
- Routing multiple independent signal paths on PCBs to avoid crosstalk
- Identifying critical via/node placements in multilayer circuits

### 5. Distributed Systems
- Byzantine fault tolerance: ensuring disjoint communication paths so that no single faulty node can block consensus
- Message authentication paths in peer-to-peer networks

## Common Mistakes / Pitfalls

### 1. Confusing with edge-disjoint paths
**Mistake:** Treating internally-node-disjoint paths as synonymous with edge-disjoint.
- Two internally-node-disjoint paths may share edges
- Edge-disjoint is a **stronger** condition
- Different min-cut theorems apply; edge-disjoint uses edge cuts, not vertex cuts

### 2. Forgetting the endpoints are shared
**Mistake:** Assuming internally-node-disjoint paths share *no* vertices.
- Definition explicitly allows shared source $s$ and sink $t$
- Only intermediate nodes must be distinct
- Three node-disjoint paths from $A$ to $B$ still converge at $B$

### 3. Applying Menger's Theorem incorrectly
**Mistake:** Computing maximum paths without properly accounting for vertex capacities.
- Menger's Theorem requires treating nodes as bottlenecks (via node splitting: $v \to (v_{in}, v_{out})$ with capacity-1 edge)
- In fractional variants, must weight nodes appropriately

### 4. Overg