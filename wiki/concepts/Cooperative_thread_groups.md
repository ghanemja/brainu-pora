# Cooperative Thread Groups

## Definition

**Cooperative thread groups** are synchronized collections of GPU threads that work together to solve a computational problem by sharing work, synchronizing execution, and coordinating memory access patterns. In the context of GPU acceleration (particularly NVIDIA CUDA), a cooperative thread group is a logical grouping of threads that:

1. Execute the same kernel code in lockstep or near-lockstep
2. Can synchronize at defined checkpoints via barriers
3. Share data through fast shared memory
4. Coordinate global memory access to achieve coalesced loading patterns
5. Collectively operate on partitions of input data with defined granularity

Unlike thread blocks (which are fixed architectural units), cooperative thread groups are a programming abstraction that allows developers to express fine-grained parallelism and synchronization at a level above individual threads.

## Key Equations

While cooperative thread groups are primarily an architectural/algorithmic concept rather than a mathematical one, their efficiency can be characterized by:

**Memory Access Efficiency:**
$$\text{Coalesced Bandwidth} = \frac{N_{\text{threads}} \times W_{\text{data}}}{N_{\text{transactions}}}$$

where $N_{\text{threads}}$ is the group size, $W_{\text{data}}$ is bits per element, and $N_{\text{transactions}}$ is the number of separate memory transactions required.

**Synchronization Overhead:**
$$T_{\text{total}} = T_{\text{computation}} + T_{\text{sync}} \times (\text{barrier count})$$

where $T_{\text{sync}}$ represents the latency introduced by synchronization points.

**Occupancy with Thread Groups:**
$$\text{Occupancy} = \frac{\text{Active Warps}}{\text{Maximum Warps per SM}} = f(\text{group size}, \text{shared memory}, \text{registers})$$

## Physical Intuition / Derivation

### Why Cooperative Thread Groups Matter

Modern GPUs are fundamentally **data-parallel** machines: they achieve high throughput by executing many threads in parallel. However, uncoordinated parallel execution leads to inefficiencies:

- **Memory traffic amplification**: If $N$ independent threads load the same cache line, they trigger $N$ separate transactions instead of one.
- **Redundant computation**: Threads may redundantly solve overlapping subproblems without sharing intermediate results.
- **Synchronization bottlenecks**: Many algorithms require threads to exchange partial results, but lacking efficient coordination mechanisms forces expensive global synchronizations.

### How They Work

Cooperative thread groups solve these problems through **structured parallelism**:

1. **Work Partitioning**: The input problem is divided into chunks, each assigned to a thread group. For example, in GPU-RMQ (Range Minimum Query acceleration), a hierarchy is scanned by thread groups, with each group responsible for a granularity level.

2. **Coalesced Memory Access**: When a thread group collectively accesses contiguous memory (e.g., via vector loading), the GPU hardware detects this pattern and merges transactions. If threads 0–31 each load 4 bytes from addresses $a, a+4, a+8, \ldots, a+124$, the GPU issues a single 128-byte transaction instead of 32 separate ones.

3. **Intra-group Communication**: Threads share results via:
   - **Shared memory**: Fast on-chip storage (typically 48–96 KB per block), allowing $O(1)$ latency reads/writes.
   - **Warp shuffles**: Direct register-to-register communication within a warp (32 threads on NVIDIA GPUs) with minimal latency.
   - **Implicit synchronization**: Barriers ensure all threads reach a checkpoint before proceeding.

4. **Granularity Tuning**: The group size is tuned to match the hardware and algorithm:
   - **Too small**: Insufficient parallelism to hide latency; poor resource utilization.
   - **Too large**: Excessive shared memory usage; reduced occupancy; synchronization overhead dominates.

### Example: Scanning with Thread Groups

In GPU-RMQ, thread groups scan hierarchical range-minimum summaries. A group of $G$ threads collectively processes a chunk of data:
- Thread $i$ loads element $i$ from the current hierarchy level
- All threads synchronize (barrier)
- Threads cooperatively compute a local scan/reduction result
- Result is written to the next hierarchy level

This coordination ensures:
- **Memory coalescence**: All $G$ threads load from contiguous addresses in a single transaction.
- **Cache locality**: Intermediate results stay in fast shared memory.
- **Reduced bandwidth**: A single summarized result is written per group instead of $G$ scattered writes.

## Applications in Engineering

### 1. **GPU-Accelerated Data Processing**
   - **Range Minimum Queries (GPU-RMQ)**: Cooperative thread groups scan hierarchical data structures to answer RMQs in parallel. Each group processes one granularity level, achieving up to 8× speedup over baselines.
   - **Sorting & Scanning**: Parallel prefix scans (used in radix sort, stream compaction) rely on thread groups to perform local scans in shared memory, then coordinate global reductions.

### 2. **Scientific Computing**
   - **Finite element assembly**: Thread groups collectively load mesh data and assemble stiffness matrices, ensuring coalesced memory access for sparse tensors.
   - **Molecular dynamics**: Neighbor-list computations group threads to process particle batches cooperatively.

### 3. **Machine Learning**
   - **Warp-level matrix operations**: Tensor Cores (specialized hardware) require thread groups to load input tiles cooperatively into shared memory.
   - **Gradient computation**: Backpropagation uses thread groups to compute local reductions (sums of partial gradients) before synchronizing.

### 4. **Ray Tracing & Graphics**
   - **Hybrid acceleration (GPU-RMQ)**: The top hierarchy level of GPU-RMQ is expressed as a triangle scene, allowing RT cores (ray-triangle hardware) to handle one granularity level while CUDA cores handle lower levels. Thread groups coordinate between these heterogeneous processing paths.
   - **BVH traversal**: Thread groups cooperatively traverse bounding volume hierarchies for ray-scene intersection.

### 5. **Database Query Processing**
   - **Index scans**: Multi-threaded scans of B-tree or hash index structures use cooperative groups to