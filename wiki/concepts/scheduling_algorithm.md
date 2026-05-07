# Scheduling Algorithm

## Definition

A **scheduling algorithm** is a computational procedure that determines the optimal assignment of tasks, flows, or resources to time slots and/or physical paths in a system, subject to constraints such as deadth deadlines, resource availability, and network topology.

In the context of **Time-Sensitive Networking (TSN)**, a scheduling algorithm computes a deterministic timetable specifying when and how data flows traverse network switches to meet stringent timing requirements. A **no-wait schedule** is a particular class where packets are transmitted immediately upon arrival at each network node without buffering delays.

### Formal Characterization

For a given network with $n$ flows, $m$ switches/nodes, and a topology constraint, the scheduling problem seeks an assignment:

$$\sigma: F \times N \to \mathbb{T}$$

where $F$ is the set of flows, $N$ is the set of network nodes, and $\mathbb{T}$ is a set of time intervals, such that:
- All timing constraints are satisfied
- Resource conflicts are eliminated (no two flows use the same link simultaneously)
- Optimality criterion is achieved (e.g., minimized latency, maximized throughput)

## Key Equations

### Conflict Resolution Constraint

For flows $f_i$ and $f_j$ sharing a link $e$:

$$\text{end\_time}(f_i, e) \leq \text{start\_time}(f_j, e) \quad \text{or} \quad \text{end\_time}(f_j, e) \leq \text{start\_time}(f_i, e)$$

This ensures mutual exclusion on shared resources.

### No-Wait Propagation

In a no-wait schedule, if a flow $f$ arrives at node $n$ at time $t_{\text{arr}}$, it must depart by:

$$t_{\text{dep}} = t_{\text{arr}} + L_{\text{proc}}$$

where $L_{\text{proc}}$ is the fixed processing/transmission latency at that node.

### Time Complexity

For the daisy-chain topology algorithm presented in the source material:

$$T_{\text{complexity}} = O(|F| \cdot |N|^2)$$

where $|F|$ is the number of flows and $|N|$ is the network size, allowing polynomial scaling to tens of thousands of flows.

## Physical Intuition / Derivation

### Problem Formulation as Graph Coloring

The key insight is to reformulate the no-wait scheduling problem as a **chromatic coloring problem on interval graphs**:

1. **Vertices**: Each flow-link pair $(f, e)$ represents a vertex—the time interval during which flow $f$ occupies link $e$.

2. **Edges**: Two vertices are connected if their time intervals **conflict** (overlap), indicating that two flows cannot simultaneously use the same link.

3. **Coloring**: Each "color" represents a unique time slot or scheduling decision. The goal is to find the **chromatic number** $\chi(G)$—the minimum number of colors needed so no adjacent vertices share a color.

### Why Interval Graphs?

On a **daisy-chain topology** (a linear cascade of switches), flows follow predetermined paths. The temporal overlap of flows on each link forms an interval graph—a special graph class where:
- Vertices correspond to intervals on the real line
- Two vertices are adjacent iff their intervals overlap
- Interval graphs have polynomial-time optimal coloring algorithms

This structure is key to achieving polynomial complexity where brute-force approaches (SMT solvers) become exponential.

### Algorithm Strategy

Algorithm 1 exploits this structure by:
1. Constructing the interval conflict graph for the given topology and flows
2. Applying an efficient interval graph coloring algorithm (e.g., greedy left-to-right scheduling)
3. Verifying no-wait feasibility: once a schedule exists, it satisfies all timing constraints

## Applications in Engineering

### 1. **Time-Sensitive Networking (TSN)**
- **IEEE 802.1Qbv/Qch standards** for deterministic Ethernet in automotive, industrial, and aerospace systems
- Guarantees bounded latency for safety-critical control loops (e.g., autonomous vehicle sensor fusion)
- Example: Controller in Carriage 1 (source material) orchestrates real-time communication across train cars

### 2. **Industrial Automation**
- Programmable Logic Controller (PLC) networks requiring synchronized sensor-actuator cycles
- Avoidance of packet drops and jitter in manufacturing lines
- Enables deterministic response times in subsecond ranges

### 3. **Aerospace & Avionics**
- Avionic Full-Duplex Switched Ethernet (AFDX) scheduling for flight-critical systems
- Certifiable real-time performance for redundancy management and system health monitoring

### 4. **Robotics & Real-Time Control**
- Multi-robot coordination with strict temporal synchronization
- Guaranteed message delivery for control loops with $< 10$ ms deadlines

### 5. **Data Center & Cloud Computing**
- Low-latency scheduling for microsecond-level SLAs (Service Level Agreements)
- Load balancing across switch fabrics with bounded congestion

## Common Mistakes / Pitfalls

### 1. **Confusing Optimality with Feasibility**
- A schedule may **exist** (feasible) but not be **optimal** (minimal latency/resources)
- SMT solvers guarantee optimality but don't scale; heuristic algorithms scale but may be suboptimal
- **Fix**: Understand the problem class—polynomial-time optimal algorithms exist only for special topologies (e.g., daisy-chain), not arbitrary networks

### 2. **Ignoring Practical Constraints**
- Theoretical algorithms assume perfect knowledge of all flows and timing
- Real systems have **dynamic arrivals, failures, and rerouting**
- **Fix**: Distinguish between *offline scheduling* (pre-computed, static) and *online scheduling* (reactive, adaptive)

### 3. **Scalability Underestimation**
- SMT solvers timeout on $\sim$300 flows; Algorithm 1 handles 45,000 in 30 minutes
- Students often prototype with SMT solvers and assume algorithms won't scale further
- **Fix**: Exploit problem structure (topology, flow patterns) for polynomial solutions

### 4. **