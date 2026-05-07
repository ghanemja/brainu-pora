# Aggregation Logic in Graph Neural Networks

## Definition

**Aggregation logic** in Graph Neural Networks (GNNs) refers to the computational rules and mechanisms by which nodes integrate information from their neighbors during message passing. Specifically, it encompasses:

1. **How neighbor representations are combined** (e.g., summation, maximum, mean)
2. **The conditional dependencies** in aggregation operations (e.g., whether aggregation depends on node identity, relative ordering, or structural properties)
3. **The expressiveness constraints** imposed by different aggregation schemes—determining which graph properties and predicates can be distinguished

In the context of provable GNN expressiveness, aggregation logic defines the *sufficient weight configurations* that enable a GNN to compute specific graph predicates (such as entity duplication detection or graph isomorphism distinguishability).

## Key Equations

### Message Passing Framework

The standard Message Passing Neural Network (MPNN) update for node $v$ at layer $k$ is:

$$h_v^{(k+1)} = \text{UPDATE}\left(h_v^{(k)}, \text{AGGREGATE}\left(\{h_u^{(k)} : u \in \mathcal{N}(v)\}\right)\right)$$

where $\mathcal{N}(v)$ is the neighborhood of $v$.

### Common Aggregation Functions

**Summation aggregation:**
$$\text{AGG}_{\text{sum}} = \sum_{u \in \mathcal{N}(v)} h_u^{(k)}$$

**Mean aggregation:**
$$\text{AGG}_{\text{mean}} = \frac{1}{|\mathcal{N}(v)|} \sum_{u \in \mathcal{N}(v)} h_u^{(k)}$$

**Max aggregation (conditional):**
$$\text{AGG}_{\max} = \max_{u \in \mathcal{N}(v)} h_u^{(k)}$$

### Conditional Aggregation (Existential Sufficiency)

For predicates like entity duplication detection, sufficiency theorems assert the *existence* of weight configurations $\theta^*$ such that:

$$\exists \theta^* : \text{GNN}_{\theta^*}(G) = P(G)$$

where $P(G)$ is the target predicate. The proof constructs explicit aggregation logic such as:

$$\text{AGG}_{\text{cond}} = \max_{v \in S} h_v, \quad \text{where } S \subseteq \mathcal{N}(v) \text{ satisfies constraint } C$$

This represents **conditional maximum** operations—aggregating over constrained neighbor subsets.

## Physical Intuition / Derivation

### Why Aggregation Logic Matters

Graph neural networks operate under a **locality principle**: each node can only directly observe its immediate neighbors. Aggregation is the bottleneck where structural information gets compressed. Different aggregation schemes have fundamentally different "expressive power."

### Necessity vs. Sufficiency in GNN Design

The paper validates two complementary directions:

**Necessity (∀θ):** For certain graph pairs $G_1, G_2$, *every* weight configuration $\theta$ of a weak architecture (e.g., without ego-node identifiers) produces identical embeddings:

$$\forall \theta : \text{EMBED}_{\theta}(G_1) = \text{EMBED}_{\theta}(G_2)$$

This is proven structurally—the symmetric architecture has no degree-of-freedom to distinguish the graphs, regardless of weights. Random sampling across 100 weight initializations showing exactly zero $L_2$ distance confirms this structural invariant.

**Sufficiency (∃θ*):** For weaker architectures to compute a target predicate, we must *construct* the exact weight configuration. Consider entity duplication detection:

- A random MPNN initialization fails because it has no reason to implement the specific conditional aggregation logic required
- The *constructed* network with tailored weights implements, e.g., $\text{AGG} = \max_{v \in \text{candidates}} h_v$ where candidates are filtered via ego-node context
- This is entirely consistent: existence ≠ probability

### The Minimal Architecture Principle

Theorems 3, 5, 8, and 12 collectively establish that for each task-graph-class pair:

$$\text{Min-Architecture}(P, \mathcal{G}) = \{\text{AGG schemes and depth} : \exists \theta^* \text{ computing } P \text{ on } \mathcal{G}\}$$

This formalizes the intuition that different problems require different aggregation logic.

## Applications in Engineering

### 1. **Entity Resolution / Record Linkage**
- Detecting duplicate entities in knowledge graphs
- Aggregation logic must distinguish node identity from local degree patterns
- Ego-node identifiers + conditional max aggregation required for worst-case separation

### 2. **Graph Isomorphism / Structure Verification**
- Testing if two circuit topologies are equivalent
- Symmetric aggregation (sum/mean) insufficient for distinguishing $K_{2,1}$ from $K_{2,r}$
- Requires careful ordering or conditional aggregation

### 3. **Molecular Property Prediction**
- Different aggregation logics (e.g., attention-based vs. fixed) capture different chemical invariants
- Equivariance under atomic permutation requires sum aggregation; bond-order sensitivity may require max

### 4. **Social Network Analysis**
- Community detection: mean aggregation smooths community boundaries
- Influence prediction: max aggregation captures high-influence outliers
- Task-dependent choice of aggregation logic

### 5. **Typed Attribute-Entity Graphs (TEAGs)**
- Preliminary empirical results show weaker architectures can exploit statistical proxies (e.g., distinctive degree patterns) on random graphs
- Engineering insight: separation gaps are worst-case; average-case behavior depends on distribution

## Common Mistakes / Pitfalls

### 1. **Confusing Necessity with Sufficiency**
*Mistake:* Assuming that because no random weights work, the architecture is fundamentally incapable.

*Correction:* Sufficiency is existential—we must *construct* weights. Random initialization is not expected to land on the specific configuration. Necessity