# Thread Group Synchronization

## Definition

Thread group synchronization is a coordination mechanism in GPU computing where multiple threads within a defined group collectively execute a shared computational task, ensuring their operations are coordinated through explicit communication primitives. In NVIDIA GPU terminology (CUDA), this typically involves thread groups (warps or thread blocks) using **warp shuffle operations** or **shared memory barriers** to exchange data and maintain execution coherence.

In the context of batch query processing (e.g., Range Minimum Queries), thread group synchronization enables:
1. **Query distribution** — assigning work items to thread groups
2. **Intra-group data exchange** — broadcasting query parameters across threads
3. **Result aggregation** — collecting and routing computed results back to source threads

## Key Equations

### Memory Coalescing Efficiency

For a batch of $m$ queries processed by thread groups of size $g$:

**Strategy 1 (Multi-load):**
$$\text{Memory accesses} = g \cdot m \quad \Rightarrow \quad \text{Coalesced transfers} = m$$

**Strategy 2 (Warp-local Queuing - WLQ):**
$$\text{Memory accesses} = m \quad \Rightarrow \quad \text{Coalesced transfers} = \frac{m}{g}$$

**Coalescing efficiency gain (Strategy 2 vs Strategy 1):**
$$\eta = \frac{m}{g \cdot m} \cdot \frac{m}{g} = \frac{1}{g^2} \quad \text{(relative reduction in transfers)}$$

For practical GPU hardware with $g \leq 16$, Strategy 2 reduces memory bandwidth demand by a factor of $g$.

### Query Assignment and Thread Indexing

**Multi-load assignment:**
$$j = \left\lfloor \frac{\text{tid}}{g} \right\rfloor, \quad \text{where } \text{tid} \in [0, g \cdot m)$$

Each thread independently loads query bounds $(l_j, r_j)$ from global memory.

**WLQ assignment:**
$$\text{tid} \in [0, m), \quad \text{rank} = \text{tid mod } g$$

Thread $\text{tid}$ loads $(l_{\text{tid}}, r_{\text{tid}})$ into registers, then broadcasts via shuffle in round $\text{rank}$.

## Physical Intuition / Derivation

### Why Synchronization is Necessary

GPUs execute massive thread populations (thousands to millions) that can diverge in execution. Without explicit synchronization, threads operating on different data would produce incorrect or conflicting results. Thread group synchronization creates **deterministic execution boundaries** within groups.

### Two Architectural Strategies

**Multi-load (Embarrassingly Parallel):**
- Spawn $g \cdot m$ threads total
- Each thread pair $(i, j)$ where $i \in [0, g)$ and $j \in [0, m)$ handles one RMQ
- **Advantage:** No communication overhead; hardware naturally load-balances
- **Disadvantage:** Redundant memory fetches (same query parameters loaded $g$ times)
- Memory bandwidth: $g \cdot m$ reads → hardware coalesces into $m$ transfers (still $g\times$ more pressure on memory subsystem per thread)

**Warp-local Queuing (Register-based Queueing):**
- Spawn $m$ threads (rounded to multiple of $g$)
- Organize into groups of $g$; threads within group rotate RMQ ownership
- Thread with rank $r$ in round $k$ broadcasts $(l_{g \cdot k + r}, r_{g \cdot k + r})$ via **warp shuffle** primitive
- **Advantage:** Each query loaded once; $g\times$ reduction in memory transactions
- **Disadvantage:** Requires cross-thread communication (shuffle latency ~4-5 cycles); higher register pressure
- **Shuffle operation cost:** $O(1)$ per broadcast within a warp (no memory access)

### Round-by-Round Execution in WLQ

For a group of size $g$ processing $m$ RMQs sequentially:

$$\text{Round } k \in [0, g) : \quad \text{active thread} = k, \quad \text{broadcast } (l_{k}, r_{k}) \rightarrow \text{all threads}$$

All $g$ threads then compute RMQ in parallel, with the active thread collecting the result:

$$\text{result}[k] = \text{rmq\_compute}(l_k, r_k, \text{shared\_data}) \quad \text{(executed collaboratively)}$$

Finally, result flows back to source thread via reverse shuffle. This pattern repeats until all $m$ RMQs are processed.

## Applications in Engineering

### 1. **Database & Search Engines**
- Batch processing of range queries (min/max lookups over sorted arrays)
- GPU acceleration of indexing and range-aggregate operations
- Reduces per-query latency when processing millions of concurrent queries

### 2. **Numerical Computing**
- Parallel reduction operations (sum, product, min, max across large arrays)
- Finite element methods (FEM): element-wise computations requiring local synchronization
- Linear algebra kernels (matrix multiplications, factorizations)

### 3. **Machine Learning**
- Batch normalization: threads compute statistics over mini-batches
- Attention mechanisms: cross-thread aggregation of similarity scores
- Inference on GPUs: coordinating computation across thread groups for tensor operations

### 4. **Graphics & Simulation**
- Particle systems: synchronizing force computations across neighbors
- Rendering: tile-based deferred rendering uses thread groups for lighting passes
- Physics simulation: coordinating collision detection and resolution

### 5. **Real-time Data Processing**
- Stream processing: batching incoming records for synchronized operations
- Log aggregation: parallel histogram computation over event streams

## Common Mistakes / Pitfalls

### 1. **Ignoring Memory Coalescing**
Many engineers default to Multi-load strategy without analyzing memory bandwidth. At scale, the $g$-fold increase in memory transactions can become the critical bottleneck, negating parallelism gains.
- **Fix:** Profile memory utilization; use WLQ when