# no-wait scheduling

## Definition

**No-wait scheduling** is a real-time packet scheduling discipline where data streams are forbidden from queuing at intermediate network nodes. Upon arrival at a switch, a stream must be forwarded to the next node **immediately**—there is no buffering or waiting allowed.

In the context of Time-Sensitive Networking (TSN), no-wait scheduling enforces a strict forwarding constraint: if a frame arrives at switch $i$ at time $t$, it must depart toward switch $i+1$ at time $t + d_{\text{fwd}}$, where $d_{\text{fwd}}$ is the fixed forwarding delay (typically negligible).

### Key Property
No-wait scheduling is optimal for minimizing both **network latency** and **jitter** simultaneously, since queuing delays—the dominant source of jitter in real-time systems—are eliminated by design.

## Key Equations

Let:
- $S$ = set of streams to be scheduled
- $|S|$ = number of streams
- $n$ = number of nodes (switches) in the network
- $p_i$ = period of stream $i$
- $p_S = \text{lcm}(p_1, p_2, \ldots, p_{|S|})$ = hyperperiod (least common multiple of all periods)

### Complexity of Optimal Algorithm

For a daisy-chain (line) topology, the optimal no-wait schedule can be computed in:

$$T_{\text{opt}} = O\left((n + |S|) \cdot |S|^{1.5} \log_2 p_S + |S| \cdot p_S \log_2 p_S\right)$$

For **feasibility checking alone** (determining if a no-wait schedule exists):

$$T_{\text{feas}} = O(|S| \cdot n)$$

### Scheduling Constraint (Daisy-Chain)

For a stream traversing nodes $1 \to 2 \to \cdots \to n$, let $a_i(t)$ be the arrival time at node $i$. The no-wait constraint enforces:

$$a_{i+1}(t) = a_i(t) + d_i$$

where $d_i$ is the deterministic traversal time through node $i$.

## Physical Intuition / Derivation

### Why No-Wait?

Traditional packet scheduling allows frames to wait in queues at switches. While flexible, this introduces **queuing delay variance** (jitter), unacceptable for hard real-time systems (e.g., industrial automation, aviation, automotive).

No-wait scheduling trades flexibility for predictability:
- ✓ **Guaranteed latency**: frame arrives at destination at deterministic time $t_0 + L$ where $L = \sum d_i$
- ✓ **Zero jitter**: all frames of same stream experience identical latency
- ✗ **Less flexibility**: schedule must be computed offline; not all demand matrices are schedulable

### Graph Coloring Reformulation

The core insight is to recast no-wait scheduling as a **restricted graph coloring problem**:

1. Each stream instance (frame) is a vertex
2. Two frames conflict if they cannot use the same output port at any switch at overlapping times
3. Colors represent time slots at output ports
4. Constraints: certain time slots are forbidden for certain frames (resource unavailability)

**Why this matters**: While graph coloring is NP-hard generally, the underlying conflict graph for a daisy-chain topology forms an **interval graph** (each vertex corresponds to an interval on the line). Interval graphs have polynomial-time coloring algorithms.

## Applications in Engineering

### 1. **Time-Sensitive Networking (TSN) / Deterministic Ethernet**
- Industrial IoT: coordinating motion control across distributed devices (e.g., collaborative robots)
- Automotive: in-vehicle communication (e.g., AUTOSAR systems) where millisecond-level latency is critical
- Railway systems: real-life deployment mentioned in source; synchronizing sensor/actuator networks across train cars

### 2. **Avionics & Aerospace**
- Flight control systems requiring provable worst-case latency bounds
- Federated avionics architectures where multiple computers share a time-triggered network

### 3. **Power Grid & Critical Infrastructure**
- Protective relay communications in electrical substations (must respond in < 100 ms)
- Synchrophasor networks for real-time grid state monitoring

### 4. **Robotics & Manufacturing**
- Multi-robot coordination in assembly lines where frame loss or jitter causes mechanical failure
- Real-time vision processing with guaranteed pipeline latency

## Common Mistakes / Pitfalls

### 1. **Confusing No-Wait with Zero-Latency**
No-wait does **not** mean zero latency; it means zero *queuing* latency. Propagation and processing delays still exist:
$$L_{\text{total}} = L_{\text{prop}} + L_{\text{proc}} + L_{\text{queue}} = L_{\text{prop}} + L_{\text{proc}} + 0$$

### 2. **Assuming All Problems Are Schedulable**
A no-wait schedule may **not exist** for a given demand set, even if standard scheduling methods succeed. Schedulability is a stricter constraint than for queue-based systems.

### 3. **Forgetting the Hyperperiod Explosion**
For streams with periods like $p_1 = 7, p_2 = 11, p_3 = 13$, we have $p_S = 1001$. This exponential growth means algorithms scaling with $p_S$ become intractable for many real inputs.

### 4. **Topology Limitations**
The polynomial-time algorithm works specifically for **daisy-chain (line) topologies**. Generalizing to arbitrary network topologies (trees, meshes) returns to NP-hardness. Students often assume the result transfers universally.

### 5. **Misunderstanding Gate Control Lists (GCLs)**
GCLs are the *implementation mechanism* for enforcing time-triggered forwarding decisions, not the scheduling algorithm itself. A GCL specifies which output port is open at which time slot, but computing the optimal GCL is the hard problem.

## See Also

- [[Time-Sensitive Networking (TS