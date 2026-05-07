# Graph Eccentricity and Diameter Bounds

## Definition

**Graph Eccentricity** ($e(v)$) is the maximum distance from a vertex $v$ to any other vertex in graph $G$:

$$e(v) = \max_{u \in V} d(v, u)$$

where $d(v, u)$ is the shortest path distance between vertices $v$ and $u$.

**Graph Diameter** ($D$ or $d$) is the maximum eccentricity over all vertices:

$$D = \max_{v \in V} e(v) = \max_{u,v \in V} d(u, v)$$

**Radius** ($r$) is the minimum eccentricity:

$$r = \min_{v \in V} e(v)$$

These metrics characterize the "spread" or "depth" of a graph's structure and are fundamental parameters in analyzing algorithmic performance on networks.

## Key Equations

For any connected graph $G = (V, E)$:

$$r \leq e(v) \leq D \quad \forall v \in V$$

$$r \leq D \leq 2r$$

The **source eccentricity** $e(s)$ from a specific source node $s$ is often distinguished in distributed algorithms:

$$e(s) = \max_{u \in V} d(s, u)$$

### Termination Bounds in Amnesiac Flooding

For **bipartite graphs**:
$$T_{\text{termination}} = e(s)$$

For **non-bipartite graphs**:
$$e(s) \leq T_{\text{termination}} \leq e(s) + D + 1$$

For **multi-source scenarios** with source set $I$ (I-bipartite graphs):
$$T_{\text{termination}} = e(I) = \max_{v \in V} \min_{s \in I} d(s, v)$$

For **multiple-message flooding** with $k$ total messages in bipartite graphs:
$$T_{\text{termination}} = D \cdot (2^k - 1)$$

In non-bipartite graphs:
$$T_{\text{termination}} = (2D + 1) \cdot (2^k - 1)$$

## Physical Intuition / Derivation

### Why Eccentricity Matters

Consider a distributed system where information must propagate from a source node $s$ through the network via message passing. The **source eccentricity** $e(s)$ directly bounds how many rounds are needed in a synchronous setting for information to reach every vertex—it's simply the length of the longest shortest path from $s$.

### Diameter as Worst-Case Structure

The diameter $D$ captures the worst-case distance between *any* pair of nodes. If an algorithm must operate without knowing the source location, or must work for all sources simultaneously, the diameter becomes the relevant parameter. The relationship $r \leq D \leq 2r$ reveals that graphs cannot be arbitrarily "unbalanced"—a graph of radius $r$ cannot have diameter worse than twice that.

### Non-bipartite Overhead

The jump from $e(s)$ rounds (bipartite) to $e(s) + D + 1$ rounds (non-bipartite) in amnesiac flooding arises because non-bipartite graphs enable adversarial message oscillation. In bipartite graphs, the bipartite structure prevents cycles of odd length, constraining adversarial delay patterns. The $D + 1$ penalty accounts for the worst-case adversarial strategy exploiting these cycles.

### Multi-message Exponential Blowup

The factor $(2^k - 1)$ in multi-message scenarios reflects the exponential tree of possible message propagation patterns. Each message can independently explore worst-case paths, and the adversary can orchestrate conflicts to force repeated transmissions.

## Applications in Engineering

### 1. **Distributed Algorithms & Broadcast Protocols**
- **Amnesiac Flooding**: Determines termination time for gossip-based protocols without node memory
- Establishes lower bounds: any broadcast algorithm requires $\Omega(D)$ rounds
- Critical for consensus protocols in ad-hoc networks

### 2. **Network Topology Design**
- **Server placement**: Minimize maximum latency by selecting hubs with low eccentricity (radius vertices)
- **5G/6G deployment**: Eccentricity bounds inform base station placement for coverage guarantees
- **Data center networks**: Low-diameter topologies (e.g., BCube, FatTree) enable fast inter-server communication

### 3. **Wireless & Mobile Networks**
- **Delay-tolerant networks (DTN)**: Predict message propagation time in sparse networks
- **Sensor networks**: Plan relay chains with guaranteed end-to-end latency
- **Epidemic routing**: Bound infection time of routing updates

### 4. **Parallel Computing**
- **Distributed memory systems**: Synchronization barrier time proportional to diameter
- **AllReduce operations**: Tree-based reduction time scales with diameter of communication graph
- **Graph processing frameworks (Spark, Giraph)**: SuperStep duration determined by network diameter

### 5. **Social Networks & Disease Modeling**
- **Information diffusion**: Predict spread time of viral content (eccentricity $\approx$ "degrees of separation")
- **Epidemiology**: SIR model epidemic threshold related to graph spectral properties (connected to diameter)
- **Influence maximization**: Seed selection balanced between eccentricity and degree

### 6. **Control Systems**
- **Consensus control**: Time to consensus in multi-agent systems scales with diameter
- **Formation control**: Stability and convergence time depend on network connectivity (diameter)

## Common Mistakes / Pitfalls

### 1. **Confusing Eccentricity and Degree**
- **Error**: Thinking a high-degree hub has low eccentricity
- **Reality**: A star graph has diameter 2, but the center node has eccentricity 1 while leaves have eccentricity 2. Degree ≠ eccentricity.

### 2. **Assuming Bipartite Speedup Is Free**
- **Error**: Expecting bipartite graphs always terminate in $e(s)$ rounds
- **Reality**: This only holds