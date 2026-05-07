# degree sequences

## Definition

A **degree sequence** is an ordered or unordered list of the degrees (number of connections) of all vertices in a graph. For an undirected graph $G = (V, E)$ with $n$ vertices, the degree sequence is typically written as $d_1, d_2, \ldots, d_n$ where $d_i$ denotes the degree of vertex $i$.

More formally:
- **Degree** of vertex $v$: $\deg(v) = |\{u \in V : (v,u) \in E\}|$
- **Degree sequence**: the multiset $\{\deg(v_1), \deg(v_2), \ldots, \deg(v_n)\}$

For directed graphs, we distinguish:
- **In-degree**: $d^{in}_i$ = number of edges pointing toward vertex $i$
- **Out-degree**: $d^{out}_i$ = number of edges leaving vertex $i$

For bipartite graphs with vertex sets $U$ and $V$, we specify sequences for each partition separately.

## Key Equations

**Handshaking Lemma** (undirected graphs):
$$\sum_{i=1}^{n} d_i = 2|E|$$

The sum of all degrees equals twice the number of edges, since each edge contributes to exactly two vertices.

**Directed graph constraint**:
$$\sum_{i=1}^{n} d^{in}_i = \sum_{i=1}^{n} d^{out}_i = |E|$$

**Graphicality condition** (Erdős–Gallai theorem for undirected simple graphs):
A non-increasing sequence $(d_1, d_2, \ldots, d_n)$ with $d_1 \geq d_2 \geq \cdots \geq d_n \geq 0$ is graphical (realizable as a degree sequence) if and only if:
1. $\sum_i d_i$ is even
2. For each $k \in \{1, 2, \ldots, n\}$:
$$\sum_{i=1}^{k} d_i \leq k(k-1) + \sum_{i=k+1}^{n} \min(d_i, k)$$

**Bipartite graph feasibility** (necessary condition):
For bipartite graph with partitions $U = \{u_1, \ldots, u_m\}$ and $V = \{v_1, \ldots, v_n\}$ with degree sequences $(a_1, \ldots, a_m)$ and $(b_1, \ldots, b_n)$:
$$\sum_{i=1}^{m} a_i = \sum_{j=1}^{n} b_j$$

## Physical Intuition / Derivation

**Why degree sequences matter:**

The degree sequence encodes the *local connectivity* structure of a network—it answers "how many connections does each entity have?" This is often the only information available in practice due to privacy constraints, measurement limitations, or data availability. For instance:
- In financial networks, regulators may know the number of counterparties each institution has, but not the identities or transaction amounts
- In supply chains, firms may disclose connection counts without revealing partners
- In biological networks, degree information may be easier to measure than complete topology

**Graphicality and realizability:**

Not every sequence of numbers can arise as a degree sequence. The Erdős–Gallai theorem provides a constructive test: a sequence is "graphical" (realizable) if it satisfies the handshaking lemma *and* passes a local connectivity check. Intuitively, the second condition prevents over-concentration of high-degree vertices that would create impossible local structures.

**Sequential construction intuition:**

When building a graph sequentially (connecting vertices one by one), at each step we must verify that remaining vertices can still achieve their target degrees. This is a feasibility verification problem: after partially constructing the graph, is it still possible to complete it consistently with the prescribed degree sequence? The sequential interval method identifies *admissible ranges* for the number of new connections that preserve feasibility.

## Applications in Engineering

### Financial Systemic Risk
Network structure fundamentally shapes how shocks propagate through financial systems. Given only partial information (e.g., number of counterparties per institution), degree sequence-based graph generation allows:
- Monte Carlo sampling of plausible network structures
- Risk assessment under model uncertainty
- Stress testing across all degree-sequence-consistent topologies
- Identification of vulnerable network architectures

### Supply Chain Resilience
Production disruptions can cascade through interconnected supply networks. Applications include:
- Characterizing supplier networks when full connection data is proprietary
- Evaluating propagation of production bottlenecks across feasible topologies
- Designing inventory and diversification strategies robust to degree-sequence-compatible disruptions

### Network Inference
Given degree-only information (often the only public data), graph generation enables:
- Statistical characterization of missing network details
- Enumeration of all feasible network structures
- Uniform random sampling for unbiased inference
- Hypothesis testing on network properties

### Distributed Computing and Communications
Degree-constrained network design problems arise in:
- Routing protocol design (node degree limits)
- Peer-to-peer network construction
- Load balancing across networks with prescribed nodal capacities

### Biological and Social Networks
- Protein interaction networks (degree known from high-throughput screening, topology uncertain)
- Social networks (total connections known, specific ties unknown)
- Epidemic modeling on networks with known degree distributions

## Common Mistakes / Pitfalls

1. **Assuming all sequences are realizable**: Not every list of positive integers forms a valid degree sequence. Always verify graphicality before assuming a network can be constructed.

2. **Confusing directed and undirected degrees**: In directed graphs, in-degree and out-degree are distinct. A vertex can have high out-degree but low in-degree (source-like behavior).

3. **Ignoring symmetry constraints in undirected graphs**: When adding an edge between vertices $i$ and $j$ in an undirected graph, both degrees must increase simultaneously. Sequential methods must account for this dependency.

4. **Forgetting the factor of 2 in handshaking lemma**: The sum of degrees is $2|E|$, not $