# vertex-capacitated setting

## Definition

The **vertex-capacitated setting** refers to a network flow problem variant where **capacity constraints are imposed on nodes (vertices) rather than (or in addition to) edges**. Each vertex $v$ has an associated capacity $c(v)$ that limits the total flow passing through that node.

More formally: In a directed graph $G = (V, E)$ with source $s$ and sink $t$, a feasible flow $f$ must satisfy:
- **Flow conservation** at intermediate nodes
- **Vertex capacity constraints**: the total flow through vertex $v$ cannot exceed $c(v)$

The vertex-capacitated setting is distinguished from the **edge-capacitated setting**, where only edges have capacity constraints.

### Related Parameter: Vertex Weight $W$

In the context of flow-cut gaps, a key parametrization is by **total vertex weight** $W$, defined as:
$$W = \sum_{v \in V} w(v)$$

where $w(v)$ is the fractional cut weight of vertex $v$. This parameter is argued to be more fundamental than the number of nodes $n$ because:
- It is invariant to addition of isolated nodes that do not affect connectivity
- It more accurately reflects instance hardness
- It enables problem simplifications unavailable when parametrizing by $n$

## Key Equations

### Flow-Cut Gap Bounds

For directed graphs with vertex capacities, the flow-cut gap (the ratio of maximum flow to minimum cut) can be bounded in terms of $W$:

$$\text{gap}_{\text{vertex}} \leq \tilde{O}(W^c)$$

for some constant $c$.

### Reduction: Vertex Weight to Node Count

**Theorem 3 (Folklore reduction)**: If the vertex flow-cut gap for $n$-node graphs is bounded by $\tilde{O}(W^c)$, then:

$$\text{gap}_{\text{vertex}} \leq \tilde{O}(n^{\frac{c}{1+c}})$$

This reduction uses a preprocessing technique: **cut all nodes of sufficiently high weight**, reducing the problem to bounded vertex weight.

### Simplification Theorem for Uncapacitated Uniform-Weight Instances

**Theorem 4 (Problem reduction)**: For the directed vertex flow-cut gap, bounding the special case of **uncapacitated graphs with uniform vertex weights** implies the same bound for **general graphs with arbitrary capacities and weights**:

$$\text{gap}_{\text{uniform, uncap}} \leq \tilde{O}(W^c) \implies \text{gap}_{\text{general}} \leq \tilde{O}(W^c)$$

This enables analysis on simplified instances without loss of generality—a property unique to $W$-parametrization in the vertex setting.

## Physical Intuition / Derivation

### Why Vertex Capacities Matter

In real networks, vertex (node) capacity constraints arise naturally:
- **Data centers**: routing capacity through a server's processing hardware
- **Transportation networks**: throughput capacity of an intersection or junction
- **Communication networks**: forwarding capacity of a router

The vertex-capacitated model is **strictly more general** than edge-capacitated models: vertex constraints can model bottlenecks that cannot be efficiently represented via edge constraints alone.

### Why Parametrize by $W$ Instead of $n$?

Traditional flow-cut analysis parametrizes by node count $n$, but this is problematic:

**Philosophical issue**: Adding isolated nodes (not affecting any source-sink paths) increases $n$ but not the problem's intrinsic difficulty. The parameter $W$ avoids this inflation.

**Technical advantage**: The reduction from general to uncapacitated/uniform-weight instances (Theorem 4) works *only* when parametrizing by $W$. When parametrizing by $n$, variable capacities and weights cannot be abstracted away—the problem structure changes fundamentally.

### Intuition for the $W$-to-$n$ Reduction

The folklore reduction works by observing that in any cut separating $s$ from $t$, nodes with very high weight "dominate" the cut cost. A preprocessing step removes these high-weight nodes by treating them as cut nodes. Remaining nodes have bounded total weight $W' \ll W$, reducing the problem to a smaller instance. This hierarchical removal technique is powerful but doesn't generalize to reverse parametrizations (obtaining $n$-bounds from $W$-bounds).

## Applications in Engineering

### Network Routing and Flow

- **Capacity planning**: Determining if a network can route demand $D$ when both nodes and links have capacity constraints
- **Flow-cut gap analysis**: Quantifying how well max-flow algorithms approximate minimum cuts in realistic networks
- **Approximation algorithms**: Using flow-cut bounds to prove approximation guarantees for routing and multicommodity flow problems

### Data Center Networking

- Modeling forwarding capacity of switches (vertex constraint) and link bandwidth (edge constraint)
- Assessing network reliability when bottlenecks exist at intermediate routing nodes

### VLSI and Circuit Design

- Gate/module capacity constraints in circuit routing
- Flow problems in netlist partitioning and placement algorithms

### Supply Chain and Logistics

- Warehouse/facility throughput limits (vertex capacity)
- Transportation link capacity (edge capacity)
- Bounds on feasible shipment volumes

## Common Mistakes / Pitfalls

1. **Confusing edge and vertex capacities**: Not recognizing that vertex constraints are fundamentally different; they cannot always be efficiently converted to edge constraints.

2. **Ignoring the role of $W$**: Attempting to analyze vertex-capacitated problems parametrized by $n$ when the instance structure naturally suggests $W$-parametrization, leading to weaker or inapplicable bounds.

3. **Assuming uniform reduction between settings**: Assuming that reductions proven for vertex-capacitated problems automatically apply to edge-capacitated settings (or vice versa). The vertex-to-edge reduction is folklore, but the converse is not known.

4. **Overlooking problem simplifications**: In vertex-capacitated settings, failing to apply Theorem 4 to simplify analysis to uncapacitated/uniform-weight cases, leading to unnecessarily complex arguments.

5. **Misinterpreting weight vs. count**: Treating weight parameters as equivalent to node count; they are fundamentally different for measuring problem difficulty in vertex-capacitated settings.

## See Also

- [[flow-cut gap]] –