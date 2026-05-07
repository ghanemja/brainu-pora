# Burning Number

## Definition

The **burning number** $b(G)$ of a graph $G$ is the minimum number of fires required to burn all vertices of the graph, where fires spread to adjacent unburned vertices in each subsequent time step.

More formally: In each round $t \geq 1$, a vertex can be **ignited** (set on fire). In round $t+1$, fire spreads from all currently burning vertices to all adjacent vertices that are not yet burned. The burning number $b(G)$ is the minimum cardinality of an initial ignition set such that all vertices are burned within some finite time horizon.

This metric is particularly relevant for **rooted graph products**, which model hierarchical network architectures where information dissemination is constrained through bottleneck vertices. The rooted product $G \circ H$ (with distinguished root $r_H \in V(H)$) is constructed by taking one copy of $G$ and, for each vertex $v \in V(G)$, attaching a copy of $H$ with $v$ identified to the root $r_H$. This creates a backbone-and-branches structure where inter-branch communication must pass through gateway vertices.

## Key Equations

**Bounding Theorem for Rooted Products:**
$$b(G \square H) \leq b(G \circ H) \leq b(G) + \text{ecc}(r_H)$$

where:
- $G \square H$ denotes the Cartesian product
- $\text{ecc}(r_H)$ is the **eccentricity** of the root (maximum distance from root to any vertex in $H$)

**Refined Bound for Center-Rooted Products:**
$$b(G \square H) \leq \min\{b(G \circ H), b(H \circ G)\} \leq \min\{b(G) + \text{rad}(H), b(H) + \text{rad}(G)\}$$

where $\text{rad}(G)$ is the radius (minimum eccentricity) of graph $G$.

**Comb Graph (Path-Based Rooted Product):**
$$C_{n,m} = P_n \circ P_m$$

where $P_n$ is the spine (backbone path) with $n$ vertices and $P_m$ are the teeth, yielding a graph with $nm$ total vertices. The burning number satisfies:
$$b(P_n \circ P_m) \leq b(P_n) + \text{rad}(P_m)$$

## Physical Intuition / Derivation

### Hierarchical Bottleneck Structure

Unlike symmetric product architectures (Cartesian or strong products) where information spreads in parallel across multiple pathways, rooted products enforce a **strict hierarchical constraint**: each local subnetwork (copy of $H$) connects to the global backbone (graph $G$) through exactly one gateway vertex.

This models real-world systems with:
- **Chain-of-command structures** (military, administrative hierarchies)
- **Hub-and-spoke networks** (airlines, supply chains)
- **Clustered communication systems** (sensor networks with cluster heads)

### Why the Bound Works

The proof of Theorem 1 proceeds via a two-phase strategy:

1. **Phase 1 (Backbone):** Ignite $b(G)$ vertices optimally on the backbone graph $G$ using a minimal burning sequence.

2. **Phase 2 (Propagation to Branches):** Wait $\text{ecc}(r_H)$ additional time steps. Since fire spreads at unit distance per time step, the maximum eccentricity ensures that fires from the backbone reach all vertices in every attached copy of $H$.

This sequential strategy captures the essential constraint: the fire spreading through the backbone cannot reach all branches simultaneously; it must traverse through the hierarchical structure, with propagation delays determined by the maximum distance from each branch's root.

## Applications in Engineering

### 1. **Distributed Control Systems**
- **Wireless sensor networks**: Deploying monitoring stations (ignition points) in clustered networks to ensure full coverage. The comb graph models regions with linear corridors and transverse sensor arrays.
- **Industrial process monitoring**: Chemical plants or factories with a main production line (spine) and parallel quality-control stations (teeth).

### 2. **Epidemic/Information Spreading**
- **Pandemic containment**: Modeling healthcare infrastructure with regional centers (backbone) and local clinics (branches); determining optimal vaccination or quarantine site placement.
- **Misinformation diffusion**: Understanding how rumors spread through organizational hierarchies where central offices gate information flow to regional offices.

### 3. **Infrastructure Networks**
- **Power grid resilience**: Main transmission lines (spine) with distributed transformers and load centers (teeth). Burning number optimization informs where to place protective isolation devices.
- **Transportation networks**: Highway systems (backbone) with service/rest areas (branches); determining critical points for evacuation or emergency response.

### 4. **Network Resilience & Firefighting**
- **Percolation theory**: The burning number relates to graph robustness—higher burning numbers indicate more resilient networks.
- **Critical infrastructure protection**: Identifying minimum number of control nodes needed to contain cascading failures in hierarchical networks.

## Common Mistakes / Pitfalls

### 1. **Confusing Rooted Products with Cartesian Products**
**Mistake:** Assuming $b(G \circ H) = b(G \square H)$.

**Reality:** Rooted products have strict bottlenecks; thus $b(G \circ H) \leq b(G \square H)$ is a proper inequality when the bottleneck structure is non-trivial. The rooted product is **always** harder to burn (requires more fires) than the Cartesian product.

### 2. **Ignoring Eccentricity vs. Diameter**
**Mistake:** Using diameter $\text{diam}(H)$ instead of eccentricity $\text{ecc}(r_H)$ in the bound.

**Reality:** The propagation delay depends on the maximum distance from the **specific root** to any vertex. If the root is poorly chosen (e.g., an end-vertex of a path), $\text{ecc}(r_H)$ equals the diameter, but a central root (center of graph) minimizes eccentricity to the