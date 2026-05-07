# Memory Fragmentation

## Definition

**Memory fragmentation** is the phenomenon where free memory space becomes scattered into non-contiguous regions, making it impossible to allocate large contiguous blocks even though the total available free space exceeds the required size.

More formally, consider a memory array of $M$ slots and a dynamic collection of live objects $X$. An **allocation map** $\phi: X \to \{0, 1, \ldots, M-1\}$ assigns each object $x$ to a contiguous interval $[\phi(x), \phi(x) + \mu(x))$, where $\mu(x)$ is the object's size. Memory fragmentation occurs when:

$$\sum_{x \in X} \mu(x) + F_{\text{free}} \leq M \text{ but } \max_{\text{free regions}} |\text{contiguous gap}| < \mu(x_{\text{new}})$$

where $x_{\text{new}}$ is an object to be inserted and $F_{\text{free}}$ is the total free space.

### Formal Problem Statement

The **Memory Reallocation Problem** dynamically maintains object assignments subject to:
- All objects in memory occupy non-overlapping contiguous regions
- Live objects satisfy: $\sum_{x \in X} \mu(x) \leq (1-\epsilon)M$ for some slack $\epsilon > 0$
- Online updates (insertions/deletions) may trigger **rearrangements** (moving objects) to defragment
- **Overhead** of an operation = (total size of moved objects) / (size of inserted/deleted object)

## Key Equations

### Fragmentation Ratio

The **fragmentation ratio** quantifies wasted space:

$$\text{Frag} = \frac{M - \sum_{x \in X} \mu(x)}{\text{largest contiguous gap}}$$

When $\text{Frag} \gg 1$, severe fragmentation occurs.

### Allocation Efficiency

The **memory utilization** is:

$$U = \frac{\sum_{x \in X} \mu(x)}{M}$$

With slack parameter $\epsilon$, we have $U \leq 1 - \epsilon$ at all times, guaranteeing room for defragmentation.

### Worst-Case Expected Overhead

For online allocators, the cost per operation relates to movement:

$$\mathbb{E}[\text{Overhead}] = \mathbb{E}\left[\frac{\sum \text{size of moved objects}}{\text{size of inserted/deleted object}}\right]$$

Recent results by Jin (2026) achieve:

$$\mathbb{E}[\text{Overhead}] = \text{polylog}(\epsilon^{-1})$$

improving previous bounds of $\widetilde{O}(\epsilon^{-1/2})$ (Farach-Colton et al., 2024), approaching the information-theoretic lower bound of $\Omega(\log \epsilon^{-1})$.

## Physical Intuition / Derivation

### Why Fragmentation Occurs

Imagine a parking lot where cars (objects) of varying sizes arrive and leave. Initially, the lot is organized with all cars packed tightly. As cars leave randomly over time, gaps emerge throughout the lot. Even though the total empty space might fit several new cars, they're scattered in small disconnected chunks. A large truck arriving might find no contiguous space despite abundant total vacancy.

This is **external fragmentation** — the inverse of internal fragmentation (wasted space within allocated blocks).

### Defragmentation Trade-off

The allocator faces a fundamental trade-off:
- **No movement**: Simple but allows severe fragmentation
- **Frequent movement**: Maintains defragmented state but incurs overhead (memory traffic, CPU, energy)

The optimal strategy balances these costs dynamically. The recent polylogarithmic result uses the **sunflower lemma** from combinatorics: roughly, if many gap-size patterns exist, a "sunflower" (structured repeating pattern) must appear, allowing efficient prediction and grouping of future gaps.

### Why Slack $\epsilon$ Matters

The parameter $\epsilon$ (guaranteeing $\sum \mu(x) \leq (1-\epsilon)M$) provides buffer space for rearrangements:
- Smaller $\epsilon$ = tighter packing → more severe potential fragmentation → more expensive defragmentation
- Overhead scaling with $\text{polylog}(\epsilon^{-1})$ means doubling available slack increases overhead cost only logarithmically

## Applications in Engineering

### 1. **Operating Systems & Virtual Memory**
- Heap allocators (malloc/free) must manage fragmentation to avoid thrashing
- Page replacement policies in virtual memory systems
- Garbage collection in languages like Java, Python

### 2. **Storage Systems & Databases**
- Disk I/O optimization: fragmented file systems reduce access speed
- Database buffer pool management
- SSD wear leveling and block allocation

### 3. **Real-Time Embedded Systems**
- Hard real-time constraints require bounded worst-case allocation time
- Predictable memory layouts critical for safety-critical applications (avionics, automotive)

### 4. **GPU Memory Management**
- VRAM fragmentation limits neural network batch sizes
- CUDA memory allocation for dynamic workloads
- Tensor reorganization overhead in deep learning frameworks

### 5. **Network Packet Buffers**
- Router memory fragmentation affects throughput
- Variable-size packet allocation with high-speed line rates
- Quality-of-Service guarantees require efficient defragmentation

### 6. **Cache-Oblivious Algorithms**
- Optimal data layout minimizes cache fragmentation
- Recursive restructuring of data for locality

## Common Mistakes / Pitfalls

### 1. **Confusing External and Internal Fragmentation**
- **External**: fragmented free space (addressed here)
- **Internal**: wasted space within allocated blocks (orthogonal issue)

Both exist; solving one doesn't solve the other.

### 2. **Ignoring the Slack Parameter $\epsilon$**
- Claiming $\epsilon \to 0$ (full memory utilization) is unrealistic
- Fragmentation overhead grows as $\epsilon$ shrinks
- Must reserve buffer space; the question is *how much*

### 3. **Assuming Movement Cost is Negligible**