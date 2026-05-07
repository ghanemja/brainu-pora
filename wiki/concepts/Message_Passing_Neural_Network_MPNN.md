# Message Passing Neural Network (MPNN)

## Definition

A **Message Passing Neural Network (MPNN)** is a class of graph neural networks that compute node embeddings through iterative rounds of local message exchange and aggregation across graph edges. At each layer, nodes aggregate information from their neighbors' embeddings, enabling the network to incorporate structural context and multi-hop dependencies.

Formally, an MPNN on a graph $G = (V, E)$ with node features $\mathbf{x}_v$ computes embeddings $\mathbf{h}_v^{(k)}$ at layer $k$ through:

$$\mathbf{m}_v^{(k)} = \text{AGGREGATE}^{(k)}\left(\left\{\text{MESSAGE}^{(k)}(\mathbf{h}_u^{(k-1)}, \mathbf{h}_v^{(k-1)}, e_{uv}) : u \in \mathcal{N}(v)\right\}\right)$$

$$\mathbf{h}_v^{(k)} = \text{UPDATE}^{(k)}(\mathbf{h}_v^{(k-1)}, \mathbf{m}_v^{(k)})$$

where:
- $\mathcal{N}(v)$ is the neighborhood of node $v$
- $\text{MESSAGE}$ computes messages from neighbors (parameterized by learnable functions)
- $\text{AGGREGATE}$ combines messages (e.g., sum, mean, max)
- $\text{UPDATE}$ incorporates aggregated messages into the node's embedding
- $e_{uv}$ denotes edge attributes (optional)

## Key Equations

### Standard Message Passing Update Rule
$$\mathbf{h}_v^{(k)} = \phi^{(k)}\left(\mathbf{h}_v^{(k-1)}, \bigoplus_{u \in \mathcal{N}(v)} \psi^{(k)}(\mathbf{h}_u^{(k-1)}, \mathbf{h}_v^{(k-1)})\right)$$

where $\phi$ and $\psi$ are learned functions and $\bigoplus$ is an aggregation operator (typically sum or mean).

### Multi-Head Attention Variant
$$\mathbf{h}_v^{(k)} = \text{CONCAT}\left(\alpha_{uv}^{(i)} \mathbf{W}^{(i)} \mathbf{h}_u^{(k-1)}\right)_{i=1}^{H}$$

where attention weights are:
$$\alpha_{uv}^{(i)} = \frac{\exp\left(\text{LeakyReLU}(\mathbf{a}^{(i)T}[\mathbf{W}^{(i)}\mathbf{h}_u^{(k-1)} \| \mathbf{W}^{(i)}\mathbf{h}_v^{(k-1)}])\right)}{\sum_{w \in \mathcal{N}(v)} \exp\left(\text{LeakyReLU}(\mathbf{a}^{(i)T}[\mathbf{W}^{(i)}\mathbf{h}_w^{(k-1)} \| \mathbf{W}^{(i)}\mathbf{h}_v^{(k-1)}])\right)}$$

### Reverse Message Passing (for bidirectional graphs)
For typed entity-attribute graphs with edge types, **reverse message passing** computes messages in both directions:
- Forward pass: entity → attribute
- Reverse pass: attribute → entity (aggregating fan-in profile)

This enables embedding $\mathbf{h}_v^{(k)}$ to capture not just local attributes but statistical properties of shared neighbors.

## Physical Intuition / Derivation

### Why Message Passing Works: Structural Context

**The core insight** is that node embeddings should depend on the broader graph structure, not just intrinsic attributes. Consider entity resolution:

1. **Naive approach (flat comparison):** Compare two entities $u$ and $v$ by independently extracting feature vectors, then computing pairwise similarity. This misses critical context.

2. **What's missing:** A phone number shared by $u$ and $v$ is strong evidence of co-reference if only two entities have it (high specificity), but is noise if thousands of entities share it (low specificity).

3. **MPNN solution:** Through message passing, nodes learn a representation that encodes **fan-in profiles** — the number of entities of each type connected to each attribute. After $k=2$ layers with reverse passing:
   - Layer 1 forward: each entity node receives its attributes
   - Layer 1 reverse: each attribute node aggregates statistics about its connecting entities
   - Layer 2 forward: each entity node receives back the fan-in profile of its attributes

This mechanism is captured by the aggregation operation:
$$\mathbf{m}_v^{(k)} = \bigoplus_{u \in \mathcal{N}(v)} \mathbf{h}_u^{(k-1)}$$

The aggregator (sum/mean) naturally encodes **how many** neighbors of each type are present—information a pairwise model cannot access.

### Expressivity Argument

A critical consequence: **if an MPNN architecture cannot compute the target function on a restricted domain (e.g., canonical-valued graphs), it cannot compute any reasonable generalization of that function on larger domains.** This establishes architectural requirements (e.g., reverse passing, ego IDs) as *necessary conditions* for learning, not merely helpful modifications.

## Applications in Engineering

### 1. **Entity Resolution & Record Linkage**
- Deduplicate customer records, publications, or organizational data
- Weight shared attributes by discriminative value (via fan-in profiles)
- Significantly outperform flat attribute-comparison baselines

### 2. **Knowledge Graph Completion**
- Predict missing links in knowledge graphs
- Nodes = entities/concepts; edges = relations
- Learn embeddings robust to incomplete information

### 3. **Molecular Property Prediction**
- Nodes = atoms; edges = chemical bonds
-