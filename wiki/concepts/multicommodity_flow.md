# multicommodity flow

## Definition

**Multicommodity flow** (MCF) is a fundamental problem in combinatorial optimization and network theory that generalizes the single-commodity flow problem to scenarios with multiple distinct flow types (commodities) sharing a common network infrastructure.

Formally, given:
- A directed graph $G = (V, E)$ with edge capacities $u_e$ for each edge $e \in E$
- $k$ commodities, where commodity $i$ has:
  - Source node $s_i$ and sink node $t_i$
  - Demand $d_i$ (the required flow quantity)
  
**The goal** is to route flow $f_i(e)$ for each commodity $i$ on each edge $e$ such that:
1. **Capacity constraints**: $\sum_{i=1}^{k} f_i(e) \leq u_e$ for all $e \in E$
2. **Flow conservation**: For each commodity $i$, flow is conserved at all nodes except $s_i$ and $t_i$
3. **Demand satisfaction**: The net flow from $s_i$ to $t_i$ equals $d_i$

The problem can be formulated as a **fractional MCF** (where flows need not be integer) or an **integral MCF** (where flows are restricted to integers).

## Key Equations

### Linear Program Formulation (Fractional MCF)

$$\text{minimize} \quad \sum_{i=1}^{k} \sum_{e \in E} c_e \cdot f_i(e)$$

subject to:

$$\sum_{i=1}^{k} f_i(e) \leq u_e \quad \forall e \in E \quad \text{(capacity)}$$

$$\sum_{e \in \delta^+(v)} f_i(e) - \sum_{e \in \delta^-(v)} f_i(e) = \begin{cases} d_i & \text{if } v = s_i \\ -d_i & \text{if } v = t_i \\ 0 & \text{otherwise} \end{cases} \quad \forall i, v$$

$$f_i(e) \geq 0 \quad \forall i, e$$

where $\delta^+(v)$ and $\delta^-(v)$ denote outgoing and incoming edges at node $v$, and $c_e$ is the per-unit cost on edge $e$.

### Feasibility Condition (Necessary and Sufficient)

The MCF problem is **feasible** if and only if for every cut $(S, T)$ in the graph:

$$\sum_{i: s_i \in S, t_i \in T} d_i \leq \text{capacity of cut}$$

This is the **max-flow min-cut theorem** generalized to multiple commodities.

## Physical Intuition / Derivation

### Why Multiple Commodities Matter

In the classical single-commodity flow problem, all units of flow are interchangeable—a unit of flow is just a unit of flow. However, real-world networks often simultaneously route distinct types of traffic that cannot be mixed:

- **Transportation networks**: packages destined for different cities (each city-pair is a commodity)
- **Telecommunication networks**: different data streams (video, email, VoIP) with different QoS requirements
- **Power grids**: electrical power from different generation sources to different load centers
- **Supply chain networks**: different product types flowing through shared distribution channels

### Why It's Hard

The addition of the capacity constraint $\sum_i f_i(e) \leq u_e$ creates a **coupling** between commodities. The key insight:

- **Single commodity**: can be solved in polynomial time (max-flow algorithms)
- **Multiple commodities**: the fractional version is a polynomial-time solvable LP, but **integral MCF is NP-hard** in general graphs
- **Approximation algorithms**: leverage multiplicative weights (as cited in [GK07]) to achieve $(1 + \epsilon)$-approximation in polynomial time

### Derivation via Linear Programming Duality

The dual of the fractional MCF LP assigns **prices (potentials)** $\pi_v$ to nodes and **prices** $\lambda_e$ to edges:

$$\text{maximize} \quad \sum_{i=1}^{k} d_i (\pi_{t_i} - \pi_{s_i}) - \sum_{e \in E} u_e \lambda_e$$

subject to:

$$\pi_v - \pi_u + \lambda_{(u,v)} \geq c_{(u,v)} \quad \forall (u,v) \in E$$

$$\lambda_e \geq 0 \quad \forall e$$

At optimality, complementary slackness conditions connect primal flows to dual prices, providing algorithmic insights (e.g., cost-scaling algorithms).

## Applications in Engineering

### 1. **Network Routing and Traffic Engineering**
- **Data center networks**: routing multiple tenant traffic flows while respecting link capacities
- **SDN (Software-Defined Networks)**: computing optimal routing schemes for heterogeneous traffic types
- **MPLS (Multiprotocol Label Switching)**: label-switched paths for different service classes

### 2. **Transportation and Logistics**
- **Vehicle routing**: distributing goods from multiple origins to multiple destinations with shared vehicle capacity
- **Airline scheduling**: routing passengers of different itineraries through connecting flights
- **Public transit**: balancing multiple passenger flows on shared infrastructure

### 3. **Power Systems**
- **Optimal power flow (OPF)**: directing power from multiple generators to multiple loads subject to transmission line limits
- **Microgrids**: coordinating distributed energy resources serving multiple districts
- **Renewable integration**: routing variable renewable generation efficiently across demand centers

### 4. **Supply Chain and Manufacturing**
- **Multi-product distribution networks**: optimizing flow of different SKUs through shared warehouses and transport routes
- **Inventory routing**: coordinating deliveries of multiple products to minimize cost while respecting vehicle capacity and demand

### 5. **Telecommunications**
- **Optical network design**: routing different wavelengths or traffic streams on shared fiber links
- **ISP backbone networks**: managing flows for different services (video, web, P2P)