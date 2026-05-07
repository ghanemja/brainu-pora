# Binary Search on Batches

## Definition

**Binary search on batches** is an algorithmic technique for GPU-resident data structures where, instead of assigning operations to threads and having each thread traverse an index layer, compute resources (warps/thread blocks) are assigned to data layer buckets, and each bucket **locates the operations it is responsible for within a batch of incoming requests using binary search**.

This inverts the traditional operation-to-thread mapping: rather than $O(B)$ threads each performing $O(\log I)$ index traversals (where $B$ is batch size and $I$ is index size), we perform $O(D)$ bucket searches, each executing a single $O(\log B)$ binary search on the batch (where $D$ is the number of data buckets).

### Key Insight

The flipped indexing paradigm eliminates redundant index traversals by having the data layer "pull" relevant operations from the batch, rather than having operations "push" themselves through the index. This is particularly effective on GPUs because:
- It **reduces warp divergence** (threads within a warp follow the same code path during binary search)
- It **eliminates index layer contention** under concurrent updates
- It **simplifies memory layout** (no complex index maintenance required)

## Key Equations

**Traditional approach (operation-centric):**
$$\text{Total work} = B \times \log I$$
where each of $B$ operations traverses an index of size $I$.

**Batch binary search approach (bucket-centric):**
$$\text{Total work} = D \times \log B$$
where each of $D$ buckets searches the batch of size $B$.

**Relative efficiency improvement:**
$$\text{Speedup} \approx \frac{B \times \log I}{D \times \log B}$$

For typical parameters (e.g., $B = 1024$, $I = 10^6$, $D = 128$):
$$\text{Speedup} \approx \frac{1024 \times 20}{128 \times 10} \approx 16\times$$

**Warp divergence reduction:**
In binary search on a sorted batch, all threads in a warp follow $O(\log B)$ comparison steps *in lockstep*, maximizing SIMD utilization.

## Physical Intuition / Derivation

### Why This Works on GPUs

1. **Index Traversal Bottleneck (Traditional Approach)**
   - Each thread independently traverses an index (B-tree, LSM-tree, etc.)
   - Index structure is irregular; different threads access different cache lines
   - Threads diverge at comparison nodes, causing warp serialization
   - Under concurrent updates, index nodes become hot spots

2. **Batch Search Advantage (FliX Approach)**
   - Batch is typically kept in fast memory (registers, shared memory, L1)
   - Binary search exhibits **predictable memory access patterns**: each comparison halves the search space
   - All threads in a warp perform the same comparisons on the same (or nearby) batch elements
   - No index layer to contend with; updates simply append to buckets

### Derivation of the Flipped Paradigm

**Step 1:** Recognize that ordered CDSs solve two problems:
- *Locating* which bucket holds a key (index layer)
- *Searching* within the bucket (data layer)

**Step 2:** Observe that in a batch, all operations are already co-located in fast memory.

**Step 3:** Invert responsibility: instead of indexing operations to buckets, ask each bucket to locate its operations in the batch via binary search.

**Step 4:** Benefit: we trade $B$ index traversals (expensive, divergent) for $D$ batch searches (cheap, aligned), where typically $D \ll B$.

## Applications in Engineering

### 1. **GPU Database Systems**
- Query engines must process millions of filter/join operations concurrently
- FliX reduces latency for range queries and successor lookups while avoiding hash table limitations
- **Use case:** Real-time analytics on GPU-resident fact tables

### 2. **In-Situ Data Processing**
- Scientific computing applications (molecular dynamics, climate simulation) benefit from maintaining ordered, searchable datasets on GPU without frequent host transfers
- **Use case:** Checkpoint-to-GPU data structure validation and indexing

### 3. **High-Frequency Trading Platforms**
- Order books must support rapid insertions/deletions/searches while maintaining total order
- FliX's 8x insertion throughput improvement enables order book state updates at microsecond scale
- **Use case:** GPU-accelerated order matching engines

### 4. **Graph Processing on GPU**
- Batch processing of graph updates (edge insertions/deletions) requires locating source/destination nodes
- FliX's ordered search without index maintenance simplifies dynamic graph construction
- **Use case:** Evolving social network graph indexing

### 5. **Streaming Data Aggregation**
- Batches of records must be routed to appropriate aggregate buckets
- Binary search on batch reduces memory bandwidth and warp divergence compared to hash-based routing
- **Use case:** GPU-accelerated approximate aggregations over sliding windows

## Common Mistakes / Pitfalls

### 1. **Assuming Batch Size is Always Large**
- **Mistake:** Believing binary search on batch is always faster than index traversal
- **Reality:** If $B < D$, the cost becomes $O(D \log B) > O(B \log I)$. Binary search on batches is optimal for $B \gg D$, typical in GPU workloads but not universal.

### 2. **Neglecting Batch Preparation Overhead**
- **Mistake:** Counting only search cost, ignoring sort/prepare cost for the batch
- **Reality:** Batches must be sorted or organized for binary search to work. If data arrives unsorted, amortized cost includes sorting: $O(B \log B + D \log B)$.

### 3. **Forgetting About Memory Coalescing**
- **Mistake:** Assuming all threads reading the batch achieve good cache locality
- **Reality:** Only if the batch is laid out contiguously in memory. Poor memory alignment can serialize shared memory access.

### 4. **Conflating Batch Binary Search with Batch Normalization**
- **Mistake:** Thinking this applies to neural network batching
- **Reality