# MPC Model

## Definition

The **Massive Parallel Computation (MPC) model** is a theoretical framework for analyzing distributed algorithms in environments with severe memory constraints. In this model:

- The system consists of $m$ machines (processors/vertices)
- Each machine has **polylogarithmic local memory**: $O(\text{poly}\log n)$ per processor
- Computation proceeds in synchronous rounds
- In each round, machines can perform local computation and exchange messages with other machines
- The total input size is $n$ across all machines

The MPC model is more restrictive than the standard **distributed memory model** (which typically allows $\text{poly}(n)$ memory per processor) but less restrictive than the **streaming model** (which uses only constant space). It represents a middle ground capturing the constraints of modern distributed systems.

### Key Constraint
A machine can store only:
$$\text{Memory per machine} = O(\text{poly}\log n)$$

This polylogarithmic bound is the defining feature that distinguishes MPC from other distributed computing models.

## Key Equations

**Communication Complexity in MPC:**
$$\text{Total bits communicated} = m \cdot \text{poly}\log n \text{ bits per round}$$

**Time Complexity:**
$$T_{\text{MPC}} = \text{number of rounds to reach consensus/solution}$$

**Memory-Time Tradeoff:**
For problems like Minimum Spanning Tree (MST) in the MPC model:
$$\text{Memory} = O(\text{poly}\log n) \implies T_{\text{rounds}} = \Theta(\log D + \text{poly}\log n)$$

where $D$ is network diameter.

## Physical Intuition / Derivation

### Motivation

The MPC model arose from practical constraints in:

1. **Wireless and Ad-hoc Networks**: Nodes (devices) have extremely limited RAM and storage
2. **Biological Networks**: Cells operate with chemical signaling and minimal information storage
3. **Cloud Computing**: Distributed systems must process massive data ($n \to \infty$) with limited per-node memory

### Why Polylogarithmic?

Consider a system processing $n$ data items:
- Each item cannot be stored entirely on one machine (violates $O(\text{poly}\log n)$ memory)
- But the machine can store metadata: $O(\log n)$ bits per item class, or $O(\log^k n)$ total
- This allows elegant algorithms that don't require storing full item data locally

### Computation Flow

```
Round 1: Local computation + neighbor exchange
         ↓
Round 2: Process received messages + send new messages
         ↓
Round 3: Aggregate partial results
         ↓
...until convergence
```

Each round is restricted by:
- Local computation on $O(\text{poly}\log n)$ bits
- Message complexity limited by network bandwidth
- No vertex can "remember" more than $O(\text{poly}\log n)$ bits between rounds

## Applications in Engineering

### 1. Distributed Minimum Spanning Tree (MST)

**Problem**: Find MST in network with memory-constrained nodes

**Challenge**: Classical algorithms (GHS, Garay-Peleg) require each node to store $\Omega(\sqrt{n})$ fragment information

**MPC Solution**: 
- Compute MST using base fragments
- Aggregate fragment information without storing it globally
- Achieves $O(\log n)$ rounds with $O(\text{poly}\log n)$ memory per node

**Time Complexity**: $\tilde{O}(\sqrt{n} + D)$ rounds (optimal for some graph classes)

### 2. Symmetry Breaking (MIS, Coloring)

- **Maximal Independent Set (MIS)**: $O(\log^2 n)$ rounds in MPC
- **Graph Coloring**: $\Delta$-coloring in $O(\text{poly}\log n)$ rounds with bounded memory
- **Application**: Distributed clustering, channel allocation in wireless networks

### 3. Aggregate Functions

**Partwise Aggregation**: Compute global sum, max, or count across distributed data

$$\text{Result} = \sum_{i=1}^{m} f(\text{data}_i)$$

where each machine processes its local data in $O(\text{poly}\log n)$ space and communicates partial results.

### 4. Graph Algorithms

- Edge/vertex enumeration with memory constraints
- Clique listing in sparse graphs
- Connected components identification

### 5. Data Processing Pipelines

Modern systems like MapReduce/Spark work under MPC-like constraints where:
- Each mapper/reducer has limited memory
- Data is larger than any single node can store
- Communication between nodes is bottleneck

## Common Mistakes / Pitfalls

### 1. **Confusing MPC with PRAM**
- ❌ **Mistake**: Assuming each processor has $O(n)$ memory (PRAM model)
- ✓ **Correct**: MPC allows only $O(\text{poly}\log n)$ memory per processor

### 2. **Ignoring Communication Cost**
- ❌ **Mistake**: Counting only local computation rounds
- ✓ **Correct**: Must account for message complexity and synchronization overhead

### 3. **Assuming Constant Space is Achievable**
- ❌ **Mistake**: Trying to solve complex problems with $O(1)$ space
- ✓ **Correct**: Polylogarithmic space allows algorithms like Emek-Wattenhofer but constant space requires specialized techniques (randomization, restricted input)

### 4. **Overestimating Base Fragment Size**
- ❌ **Mistake**: Assuming all fragments must be stored at one node
- ✓ **Correct**: Information can be distributed; need only $O(\text{poly}\log n)$ bits **per machine**

### 5. **Mixing KT1 and KT2 Models**
- ❌ **Mistake**: Assuming nodes know neighbor IDs initially (KT1 property)
- ✓ **Correct**: Standard MPC (KT2) requires nodes to discover neighbor IDs through communication

## See Also

- [[Distributed Algorithms]] — General framework for algorithms on distributed systems
- [[Minimum Spanning