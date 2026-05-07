# Graph Neural Network Layers

## Definition

A **graph neural network (GNN) layer** is a computational unit that transforms node embeddings by aggregating information from neighboring nodes through message passing. Each layer performs three operations in sequence:

1. **Message construction**: Each node computes messages to send to its neighbors based on its current embedding and edge information
2. **Message aggregation**: Each node receives and aggregates messages from its neighbors using a permutation-invariant aggregation function (typically sum or max)
3. **Embedding update**: Each node combines its aggregated neighbor information with its own embedding to produce a new representation

Formally, a single GNN layer transforms embeddings $h^{(k)}$ to $h^{(k+1)}$ via:

$$h_u^{(k+1)} = \text{UPDATE}^{(k)}\left(h_u^{(k)}, \text{AGGREGATE}^{(k)}\left(\{h_v^{(k)} : v \in \mathcal{N}(u)\}\right)\right)$$

where $\mathcal{N}(u)$ denotes the neighborhood of node $u$.

In **message passing neural networks (MPNNs)**, this is decomposed explicitly:

$$m_u^{(k)} = \text{AGGREGATE}\left(\{\text{MESSAGE}^{(k)}(h_v^{(k)}, h_u^{(k)}, e_{v,u}) : v \in \mathcal{N}(u)\}\right)$$

$$h_u^{(k+1)} = \text{UPDATE}^{(k)}(h_u^{(k)}, m_u^{(k)})$$

where $e_{v,u}$ represents edge features and messages are multisets (unordered collections allowing duplicates) because node neighborhoods are unordered.

## Key Equations

### Standard Message Passing
$$h_u^{(k+1)} = \gamma^{(k)}\left(h_u^{(k)}, \text{AGG}^{(k)}\left(\left\{\phi^{(k)}(h_u^{(k)}, h_v^{(k)}) : v \in \mathcal{N}(u)\right\}\right)\right)$$

where:
- $\phi^{(k)}$ is the message function
- $\text{AGG}^{(k)}$ is an aggregation function (permutation-invariant)
- $\gamma^{(k)}$ is the update function

### Common Aggregation Functions
$$\text{SUM}: \text{AGG}(\mathcal{M}) = \sum_{m \in \mathcal{M}} m$$

$$\text{MEAN}: \text{AGG}(\mathcal{M}) = \frac{1}{|\mathcal{M}|}\sum_{m \in \mathcal{M}} m$$

$$\text{MAX}: \text{AGG}(\mathcal{M}) = \max_{m \in \mathcal{M}} m \text{ (elementwise)}$$

### Information Flow Depth
For a graph property that depends on nodes at distance $d$, the minimum layer depth required is $d$ layers, since information propagates exactly one hop per layer. This creates a **temporal causality constraint**: information from distance $d$ requires $d$ sequential layers to reach a target node.

## Physical Intuition / Derivation

### Why Multiset Messages Matter
Node neighborhoods are **unordered and allow multiple edges** (in multigraphs). Standard neural networks assume ordered inputs, but GNN messages form multisets. A permutation-invariant aggregation (like sum or max) ensures that:
$$\text{AGG}(\{m_1, m_2, m_3\}) = \text{AGG}(\{m_3, m_1, m_2\}) = \text{AGG}(\{m_1, m_1, m_2\})$$

This is essential because nodes have no inherent ordering of their neighbors.

### Information Flow as Temporal Progression
Each layer performs exactly one "hop" of information propagation:
- **Layer 1**: Each node learns about its direct neighbors ($1$-hop)
- **Layer 2**: Each node learns about neighbors' neighbors ($2$-hop)
- **Layer k**: Each node has integrated information from all nodes within $k$-hop distance

The source material demonstrates this through a concrete example: computing whether an ego node $u$ has overlap $\geq r$ with another node $v$ in a bipartite entity-attribute graph requires exactly **4 layers** because:

1. **Layer 1** (forward): Ego mark reaches attributes from the ego node
2. **Layer 2** (reverse): Ego-attribute membership reaches other entities; each entity computes local overlap count $o_v(v)$
3. **Layer 3** (forward): Overlap counts propagate back to attributes; each attribute computes $\max$ over overlaps
4. **Layer 4** (reverse): Aggregated maximum reaches the ego to decide the predicate

This exemplifies why **depth is minimized but non-negotiable**: the information-theoretic dependency structure of the graph requires this specific sequence of aggregations.

### Why Injective Multiset Encoding is Rarely Needed
Most GNN layers use elementary aggregations (sum, max, mean). The source material notes that even in demanding tasks, multiset injectivity (fully distinguishing all possible multisets) is invoked only occasionally. This is because:

- **Sum aggregation** works well when duplicate messages convey frequency information
- **Max aggregation** extracts the strongest signal regardless of multiplicities
- Only when distinguishing different **compositions** of identical multisets is injective encoding necessary

## Applications in Engineering

### 1. Molecular Chemistry
- **Prediction task**: Predict molecular properties (solubility, reactivity, binding affinity) from atomic structure
- **Graph structure**: Atoms as nodes, chemical bonds as edges
- **Layer role**: Each layer captures richer chemical neighborhood context; typically 3–5 layers sufficient because atomic influence is local
- **Practical use**: Drug discovery pipelines in pharmaceutical engineering

### 2. Traffic Network Analysis
- **Prediction task**: Predict travel time, congestion, or accident likelihood on road networks
- **Graph structure**: Intersections/road segments as nodes, traffic