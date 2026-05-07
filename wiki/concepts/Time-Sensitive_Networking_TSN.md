# Time-Sensitive Networking (TSN)

## Definition

**Time-Sensitive Networking (TSN)** is a set of IEEE 802.1 standards that enable **deterministic and predictable communication** over Ethernet networks by providing:

- **Bounded latency**: Guaranteed maximum network delay
- **Low jitter**: Deterministic packet delivery with minimal timing variation
- **Reliability**: Lossless packet transmission for critical data
- **Scheduling guarantees**: Prioritized real-time traffic over best-effort communication

Unlike traditional Ethernet (best-effort delivery), TSN transforms Ethernet into a real-time communication infrastructure suitable for cyber-physical systems, industrial automation, and safety-critical applications.

### Core Problem

The fundamental TSN scheduling problem: Given a set of data streams with timing constraints (deadlines, periods, sizes), compute a **schedule** that determines when each stream transmits on network switches to guarantee all deadlines are met.

**Key challenge**: TSN standards specify the communication capabilities but **not how to compute schedules**—this remains an open optimization problem.

---

## Key Equations

### No-Wait Scheduling Constraint

For a stream $i$ with:
- Release time: $r_i$
- Deadline: $d_i$
- Packet size: $L_i$
- Transmission time: $t_i = L_i / B$ (where $B$ = link bandwidth)

A valid no-wait schedule must satisfy:

$$r_i \leq s_i \leq c_i \leq d_i$$

where:
- $s_i$ = start transmission time
- $c_i = s_i + t_i$ = completion time
- **No-wait constraint**: Each packet transmits immediately after becoming available (no idle time buffering)

### Daisy-Chain Topology Constraint

For a daisy-chain (serial chain of $n$ switches), stream $i$ passing through switches in sequence:

$$c_{i,j} + \text{prop\_delay} \leq s_{i,j+1}$$

where $c_{i,j}$ is completion time at switch $j$ and $s_{i,j+1}$ is start time at next switch.

### Graph Coloring Formulation

The scheduling problem is recast as a **constrained interval graph coloring**:

- **Vertices**: Each $V_{i,j}$ represents stream $i$'s transmission window at switch $j$
- **Edges**: Connect conflicting transmissions (overlapping time windows)
- **Colors**: Time slots available for each transmission
- **Constraint**: Restricted color set per vertex (not all colors available everywhere)

The goal is finding a **proper coloring** (no two adjacent vertices share a color) in polynomial time.

---

## Physical Intuition / Derivation

### Why TSN Matters

Traditional Ethernet uses **statistical multiplexing**: packets from different sources share network links via random access (CSMA/CD). Under high load, queueing delays become unpredictable.

**Cyber-physical systems require determinism**: A robot arm's motion control, vehicle brake actuation, or power grid protection must complete with *guaranteed* timing. Random delays are unacceptable.

### The No-Wait Scheduling Insight

**No-wait scheduling** is attractive because:

1. **Memory efficiency**: Don't buffer packets at intermediate switches
2. **Latency reduction**: Packets transmit immediately upon arrival
3. **Predictability**: Strict time windows → deterministic behavior

However, computing feasible no-wait schedules is computationally hard for arbitrary topologies.

### Why Daisy-Chain Simplifies the Problem

A daisy-chain topology (switches arranged linearly: $S_1 \to S_2 \to \cdots \to S_n$) has special structure:

- **Sequential transmission**: Each stream visits switches in order
- **Interval graph property**: Each stream's transmission windows form an interval in the schedule
- **Polynomial-time solvability**: Graph coloring on *interval graphs* is NP-hard in general, but becomes polynomial with additional constraints

The key technical result: **Constrained coloring of interval graphs can be solved in polynomial time**, even though unconstrained graph coloring is NP-hard.

### Algorithm Approach

1. **Model** each stream-switch pair $(i,j)$ as a vertex with time interval $[r_i, d_i]$
2. **Identify conflicts**: Streams that cannot transmit simultaneously
3. **Build interval graph**: Edges connect conflicting transmissions
4. **Solve constrained coloring**: Assign time slots (colors) respecting:
   - No two streams use same slot at same switch
   - Deadlines respected
   - Dependency ordering (stream completes at $j$ before starting at $j+1$)

Result: **Polynomial-time complexity** scaling as $O(\text{streams} \times \text{switches})$

---

## Applications in Engineering

### Industrial Automation (Industry 4.0)

- **Deterministic control loops**: Manufacturing robots coordinating over networked Ethernet instead of proprietary real-time fieldbus
- **Predictable latency**: Guaranteed sub-millisecond communication for coordinated motion control
- **Example**: Multi-axis CNC machine where spindle, tool changer, and robot must synchronize precisely

### Automotive / In-Vehicle Networks

- **Vehicle electrification**: Distributed battery management systems, motor controllers, brake-by-wire requiring deterministic communication
- **Safety-critical protocols**: Replace CAN/FlexRay with TSN Ethernet for higher bandwidth + determinism
- **Example**: Autonomous vehicle sensor fusion (LiDAR, camera, radar) with synchronized timing guarantees

### Avionics & Aerospace

- **Cockpit networks**: Deterministic communication between flight control systems, displays, and sensor interfaces
- **Real-time redundancy**: Multiple redundant channels with guaranteed switchover timing
- **Certification advantage**: TSN standardization aids safety certification (DO-178C compliance)

### Power Systems & Smart Grids

- **Synchrophasor networks**: Time-synchronized measurement and protection with sub-millisecond latency
- **Microgrid coordination**: Distributed energy resources (solar inverters, batteries) requiring deterministic voltage/frequency regulation
- **Substation automation**: Merging units, intelligent electronic devices communicating with bounded delay

### Medical Devices

- **Operating room networks**: Surgical robots, imaging systems, monitoring equipment needing synchronized real-