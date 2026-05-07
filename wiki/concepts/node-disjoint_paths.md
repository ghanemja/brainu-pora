# node-disjoint paths

## Definition

**Node-disjoint paths** (also called **internally-node-disjoint paths**) between two nodes $s$ and $t$ in a graph $G = (V, E)$ are multiple paths from $s$ to $t$ that share no common intermediate vertices. More precisely, if paths $P_1$ and $P_2$ are node-disjoint, then $P_1 \cap P_2 = \{s, t\}$—they may share the source and target but no other vertices.

A set of $k$ node-disjoint paths forms a **path witness** of width $k$ between the demand pair $(s, t)$.

### Formal Statement

For a graph $G$ and demand pair $(s, t)$, a collection of internally-node-disjoint $s \leadsto t$ paths $\{\pi_1, \pi_2, \ldots, \pi_k\}$ satisfies:
$$\pi_i \cap \pi_j = \{s, t\} \quad \forall i \neq j$$

## Key Equations

**Menger's Theorem (Vertex Version):** The maximum number of internally-node-disjoint paths from $s$ to $t$ equals the minimum cardinality of a vertex cut separating $s$ and $t$:

$$\max \{|\text{node-disjoint paths from } s \text{ to } t\}| = \min \{|X| : X \text{ separates } s, t\}$$

**Mass Function** (from MCMF analysis): For a collection of fractional weight functions $\{w_{s,t}\}$ indexed by demand pairs $(s,t) \in \mathcal{P}$:

$$\text{mass}(\{w_{s,t}\}) := \sum_{(s,t) \in \mathcal{P}} \sum_{v \in V \setminus X} w_{s,t}(v)$$

This measures the aggregate "thickness" of cuts across all demand pairs.

## Physical Intuition / Derivation

### Why Node-Disjoint Paths Matter

Node-disjoint paths represent redundancy in network connectivity. They answer the question: *"How many independent paths can route information from source to destination without interfering?"*

**Key insight from Menger's Theorem**: The width of the thinnest bottleneck (minimum cut) directly equals the number of completely independent routes available. This duality is fundamental:

- **Lower bound**: At least $k$ node-disjoint paths $\Rightarrow$ any cut must remove $\geq k$ nodes
- **Upper bound**: A cut of size $k$ immediately forbids more than $k$ completely independent paths

### Algorithmic Construction

The source material describes an algorithm that finds cuts by:

1. **Maintaining weight functions** $w_{s,t}(v)$ that assign capacities to each node $v$ relative to each demand pair
2. **Computing fractional min-cuts** to estimate node importance for separating $s$ and $t$
3. **Performing "random level cuts"**: sampling a threshold $d \in [0,1]$ and cutting nodes $v$ where the weighted distance from $s$ to $v$ crosses this threshold

This probabilistic approach leverages the continuous relaxation (minimum cost maximum flow, MCMF) to find integral solutions.

### Technical Refinement: Transitive Closure

A subtle point from the source material: when weight bounds are tight, the path witness may need to exist in the **transitive closure** $G \setminus X$ rather than $G \setminus X$ directly. This means:
- Paths may "skip" heavily-weighted intermediate nodes
- Weight bounds are relaxed by a $O(1)$ factor to compensate
- This preserves approximate path witnesses while maintaining balance in the algorithm's parameters

## Applications in Engineering

### Network Design & Reliability
- **Telecommunications**: Route $k$ edge-disjoint fiber paths for redundancy; node-disjoint generalizes to critical infrastructure (routers, switches)
- **Data center networks**: Design fault-tolerant routing where node failures (server/switch outage) don't disconnect demand pairs
- **Supply chain networks**: Identify minimum number of warehouse/hub closures that could disconnect sources from markets

### Graph Algorithms & Complexity
- **Flow networks**: Maximum flow algorithms implicitly construct node-disjoint paths via min-cut duality
- **Graph partitioning**: Cut-finding algorithms (as in the source material) use path witnesses to validate cut quality
- **Approximation algorithms**: Many routing and load-balancing problems reduce to finding node-disjoint paths

### Distributed Systems
- **Byzantine fault tolerance**: Requiring $f+1$ node-disjoint paths ensures message delivery survives $f$ adversarial nodes
- **Blockchain consensus**: Multi-path verification prevents single-point compromise

### Circuit Design
- **Signal routing**: Avoid signal crosstalk by ensuring critical paths don't share nodes (especially power/ground planes)
- **Chip partitioning**: Separate logic into regions with guaranteed node-disjoint signal paths

## Common Mistakes / Pitfalls

1. **Confusing node-disjoint with edge-disjoint**: Two edge-disjoint paths may share vertices. Node-disjoint is strictly stronger (except for $s$ and $t$).

2. **Applying Menger's theorem incorrectly**: The theorem gives an *equality*, not just an inequality. Students often forget that min-cut equals max node-disjoint paths—the duality is exact, not approximate.

3. **Ignoring the source/target loophole**: The definition permits $s$ and $t$ to appear in multiple paths. Paths are only disjoint on *intermediate* vertices.

4. **Forgetting computational hardness**: Finding truly maximum node-disjoint paths is **NP-hard** in general (though solvable in polynomial time for some restricted graph classes). Approximation algorithms like the one in the source material are necessary.

5. **Neglecting weight constraints in algorithms**: The source material shows that adding node weight upper bounds requires relaxation factors (e.g., by $O(1)$) and transitive closure tricks—naive applications fail.

6. **Assuming uniform node costs**: In practice, some nodes are more "expensive" to cut (e.g., critical routers); algorithms must