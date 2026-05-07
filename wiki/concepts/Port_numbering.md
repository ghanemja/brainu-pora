# Port numbering

## Definition

**Port numbering** is a structural mechanism in message-passing neural networks (MPNNs) that assigns unique identifiers to edges based on their **incoming** or **outgoing** endpoints, enabling the network to distinguish between parallel edges in multigraphs and count distinct sources of information.

Formally, for a multigraph $G = (V, E)$ with multiple edge types $\tau \in T$:

- An **incoming port number** for an edge $e = (u, v)$ of type $\tau$ is an integer label assigned to $e$ such that:
  - **(i)** All parallel edges from the same source $u$ to sink $v$ share the same incoming port
  - **(ii)** Edges arriving at $v$ from *distinct* predecessors receive *distinct* incoming port numbers

This provides a canonical way to track message multiplicity and source identity without explicit simplicity constraints.

## Key Equations

Consider an attribute node $a$ receiving messages from multiple entities via edges of type $\tau$. Let $M^{\text{in}}_{\tau,p}(a)$ denote the set of messages from entities connected to $a$ via type-$\tau$ edges with incoming port $p$.

**Message aggregation with port numbering:**
$$\text{agg}_\tau(a) = \bigoplus_{p \in P(\tau)} \bigoplus_{m \in M^{\text{in}}_{\tau,p}(a)} m$$

where $P(\tau)$ is the set of distinct ports for edge type $\tau$, and $\bigoplus$ denotes permutation-invariant aggregation (e.g., sum, mean, max).

**Distinct source counting:**
The number of distinct entity predecessors of type $\sigma$ becomes:
$$|\text{Pred}_\sigma(a)| = |\{p : M^{\text{in}}_{\sigma,p}(a) \neq \emptyset\}|$$

Port numbering allows this count to be computed even when entities send *multiple parallel edges*.

## Physical Intuition / Derivation

### Why Port Numbering is Necessary

On **simple graphs** (at most one edge between any two nodes), message multiplicity at a receiver directly equals the number of distinct senders. However, on **multigraphs**, parallel edges inflate multiplicity without indicating additional sources:

$$\text{Raw multiplicity} \neq |\text{Distinct sources}|$$

Port numbering solves this by creating a **canonical grouping** of parallel edges. Instead of the aggregation function seeing three identical-source messages as potentially three different sources, port numbering acts as a **structural fingerprint**:

- Messages from entity $u$ → $a$ all carry port $p_u$
- Messages from entity $v$ → $a$ all carry port $p_v$  
- Distinct ports → distinct sources, regardless of edge count

### Role Relative to Simplicity

Port numbering is the **minimal relaxation** when moving from simple to multigraph assumptions:

| Assumption | Simple Graph | Multigraph |
|-----------|-----------|-----------|
| Max edges $(u,v)$ per type | 1 | $\infty$ |
| Source counting method | Raw multiplicity | **Incoming port numbers** |
| Information required | Edge presence | Port assignment + edge labels |

This is analogous to restoring structure lost by generalizing the graph class.

## Applications in Engineering

### 1. **Record Linkage & Entity Resolution**
Detecting duplicate entities in databases with multiple matching attributes. Port numbering allows neural networks to count *distinct* attributes without overcounting when entries have redundant typed references.

### 2. **Knowledge Graph Completion**
In knowledge graphs with parallel edges (e.g., multiple "authored-by" relationships of different metadata types), port numbering enables precise source disambiguation when aggregating neighborhood information.

### 3. **Bipartite Graph Analysis**
In entity-attribute bipartite graphs (common in recommendation systems, schema inference):
- Entities and attributes are separate node types
- Port numbering disambiguates when one entity connects to one attribute via multiple typed edges
- Essential for detecting $K_{2,r}$ patterns (two entities sharing $r$ distinct typed attributes)

### 4. **Message-Passing Graph Neural Networks**
Architectures like R-GCN variants and typed-GNNs use port numbering to:
- Separate aggregation channels per edge type and predecessor
- Compute statistics over distinct neighbors (e.g., in heterogeneous graphs)
- Support reverse message passing for entity-to-attribute communication

### 5. **Multi-Modal Learning**
When nodes have multiple types of incoming connections (e.g., visual, textual, relational), port numbering prevents conflation of parallel modalities.

## Common Mistakes / Pitfalls

### Mistake 1: Confusing Port Numbers with Edge Labels
**Error:** Treating port numbers as learned edge features or attention weights.  
**Correction:** Port numbers are *structural identifiers* assigned deterministically before learning, not learnable parameters. They enable the network to *use* multiplicities meaningfully, but are not themselves optimized.

### Mistake 2: Using Outgoing Instead of Incoming Ports
**Error:** Assigning unique IDs based on which edges a sender *produces*.  
**Correction:** Incoming ports matter for counting distinct sources at a receiver. The proof of Theorem 5 uses only incoming ports; outgoing ports are unnecessary and do not enable the same disambiguation.

### Mistake 3: Assuming Port Numbering Solves All Multigraph Problems
**Error:** Thinking port numbering alone is sufficient for any multigraph learning task.  
**Correction:** Port numbering addresses *source disambiguation*. For harder tasks (e.g., $K_{2,r}$ detection with $r \geq 2$), additional mechanisms like **ego IDs** or **structural features** are necessary. Port numbering is tight only for specific predicates (e.g., $K_{2,1}$).

### Mistake 4: Forgetting the Depth Cost
**Error:** Expecting that adding port numbering reduces the required network depth.  
**Correction:** Theorem 5 shows that two layers are *necessary* for $\text{Dup}$ detection even with port numbering. The information-flow constraint (entities must learn fan-in statistics of attributes) still requires aggregation at intermediate layers. Port numbering enables