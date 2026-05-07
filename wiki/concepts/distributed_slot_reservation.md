# Distributed Slot Reservation

## Definition

**Distributed Slot Reservation** is a hierarchical protocol for allocating contiguous time slots (or bandwidth intervals) in a distributed system without central coordination. It operates through a multi-phase, bottom-up aggregation of resource requests followed by top-down distribution of allocated intervals, using a virtual tree structure to organize the network into fragments.

The protocol ensures that:
- Each node's resource needs are aggregated upward through fragment leaders
- A root node allocates intervals based on total demand
- Intervals are decomposed and distributed downward to requesting endpoints
- All slots are reserved deterministically with no conflicts

This is particularly relevant in **wireless MAC protocols**, **time-division multiplexing (TDM)** networks, and **distributed scheduling systems** where nodes must coordinate access to a shared resource (e.g., communication slots, processor time) without a global scheduler.

---

## Key Equations

Let $F$ denote a fragment and $|F|$ its cardinality (number of base fragments it contains).

**Interval Size Calculation (Bottom-Up):**
$$I_{\text{req}}(F) = |F| + \sum_{C \in \text{children}(F)} I_{\text{req}}(C)$$

where $I_{\text{req}}(F)$ is the total interval size requested by fragment $F$ and its descendants.

**Allocation Per Fragment:**
$$I_{\text{alloc}}(F) = I_{\text{req}}(F)$$

The root assigns contiguous slots $[s, s + I_{\text{alloc}}(\text{root}) - 1]$.

**Sub-interval Reservation:**
For fragment $F$ within parent $P$:
$$I_F \subseteq I_P, \quad |I_F| = |F|$$

The leader of $F$ reserves the first $|F|$ slots from its allocated interval.

---

## Physical Intuition / Derivation

### Why Hierarchical Aggregation?

In a flat network, every node requesting slots must communicate with every other node—O(n²) messages. A hierarchical approach reduces this by organizing nodes into a **virtual tree of fragments** where:
- **Fragments** are clusters of nodes under a common leader
- **Leaders** represent their fragment's collective demand upward
- Only leaders communicate across levels

### The Two-Phase Cycle

**Phase 1: Upward Aggregation (Steps 1–2)**
1. Each base fragment $B$ polls its MWOE-adjacent (Maximum Weight Outgoing Edge) neighbors to learn their demand
2. This demand is summed: $D_B = \sum_{v \in \text{neighbors}(B)} d_v$
3. Fragment leaders aggregate: $D_F = |F| + \sum_{C \in \text{children}(F)} D_C$
4. The root learns the system-wide demand $D_{\text{root}}$

**Intuition:** Think of this like a census. Local information bubbles up through intermediate aggregators without redundant broadcasts.

**Phase 2: Downward Distribution (Steps 3–4)**
1. Root allocates: $I_{\text{root}} = [0, D_{\text{root}} - 1]$
2. Each fragment leader receives an interval and reserves the first $|F|$ slots for its direct members
3. Remaining slots are split and passed to child fragments
4. This mirrors the aggregation structure, so each requesting endpoint receives its exact allocation

**Intuition:** The interval is **traced backward** along the same virtual tree edges where requests traveled upward. This guarantees no fragmentation and no conflicts.

### Why Depth d = 3?

The protocol iterates the broadcast and interval allocation cycles $d = 3$ times. This is because:
- The virtual fragment tree has depth at most 3 (by design or constraint)
- Each iteration handles one level of the hierarchy
- After 3 rounds, the entire tree is processed

$$\text{Total communication rounds} = O(d \log n) = O(\log n)$$

---

## Applications in Engineering

### 1. **Wireless MAC Protocols**
In multi-hop wireless networks (e.g., sensor networks, ad hoc networks), nodes compete for transmission slots. Distributed slot reservation avoids the overhead of a centralized scheduler:
- **Example:** TDMA scheduling in WSNs where slot pools are hierarchically allocated to clusters
- **Benefit:** O(log n) latency instead of O(n) under centralized allocation

### 2. **Time-Division Multiplexing (TDM)**
In telecom switching fabrics and optical networks, time slots must be reserved on shared media:
- **Example:** Frame-based scheduling in asynchronous transfer mode (ATM) switches
- **Benefit:** Deterministic, contention-free access; dead time = 0

### 3. **Distributed Database Systems**
Coordinating access to a shared resource (e.g., a log, a disk buffer) across multiple servers:
- **Example:** Write-ahead logging (WAL) in replicated databases where each replica reserves log slots
- **Benefit:** No bottleneck at a single log allocator; horizontal scalability

### 4. **Real-Time Task Scheduling**
In embedded systems with multiple processors, time-sliced execution of real-time tasks:
- **Example:** Scheduling periodic tasks on a multi-core embedded platform
- **Benefit:** Predictable deadline guarantees via contiguous slot allocation

### 5. **Software-Defined Networking (SDN)**
Controllers allocate bandwidth intervals to flows in a network:
- **Example:** QoS-aware flow scheduling across multiple network segments
- **Benefit:** Hierarchical aggregation of flow demands reduces control-plane overhead

---

## Common Mistakes / Pitfalls

### 1. **Confusing Fragment Structure with Physical Topology**
**Mistake:** Assuming fragments must correspond to physical clusters or neighbor sets.

**Reality:** Fragments are *virtual*, defined by the algorithm. A fragment can span multiple physical locations, and neighborhood is defined by MWOE edges in a virtual forest, not proximity.

### 2. **Thinking Intervals Are Fragmented**
**Mistake:** Expecting allocated intervals to be scattered or fragmented across the system.

**Reality:** Intervals are *contiguous* by design. The downward distribution mirrors the upward aggregation, ensuring each endpoint receives a contiguous sub-interval.

### 3.