# Cache Utilization

## Definition

**Cache utilization** refers to the effectiveness with which a computational system exploits its available cache hierarchy—both in terms of *capacity* (how much of the cache can be filled with useful data) and *longevity* (how long data remains resident before eviction)—to minimize memory latency and bandwidth bottlenecks during algorithm execution.

In the context of GPU acceleration, cache utilization measures how efficiently an algorithm leverages the multi-tiered memory structure (registers → L1/L2 cache → global/VRAM) to reduce costly off-chip memory accesses. A well-optimized algorithm maximizes cache hits (data found in fast cache) and minimizes cache misses (forced to fetch from slower memory).

### Quantitative Measure

Cache utilization can be formalized as:

$$\text{Cache Utilization Ratio} = \frac{\text{Cache Hits}}{\text{Total Memory Accesses}} = \frac{C_h}{C_h + C_m}$$

where $C_h$ is the number of cache hits and $C_m$ is the number of cache misses.

The **effective memory bandwidth** consumed depends on the hit ratio and access patterns:

$$B_{\text{eff}} = B_{\text{peak}} \cdot \alpha + B_{\text{mem}} \cdot (1-\alpha)$$

where $\alpha$ is the cache hit ratio, $B_{\text{peak}}$ is cache bandwidth, and $B_{\text{mem}}$ is main memory bandwidth.

---

## Key Equations

### Memory Access Cost Model

The average latency per memory access is:

$$L_{\text{avg}} = \alpha \cdot L_{\text{cache}} + (1-\alpha) \cdot L_{\text{mem}}$$

where:
- $\alpha$ = cache hit ratio (0 to 1)
- $L_{\text{cache}}$ = cache access latency (typically 1–4 cycles for L1)
- $L_{\text{mem}}$ = main memory access latency (100–400 cycles for GPU global memory)

### Working Set vs. Cache Size

For an algorithm to maintain high utilization, its **active working set** $W$ must satisfy:

$$W \leq C \cdot \eta$$

where:
- $W$ = size of data actively accessed within a computational window
- $C$ = total cache capacity
- $\eta$ = efficiency factor accounting for non-uniform access patterns (typically 0.5–0.8)

### Cache Footprint Scaling

In hierarchical acceleration structures (like GPU-RMQ), memory footprint grows with dataset size. The utilization horizon—the maximum dataset size before cache performance degrades—occurs when:

$$N_{\text{crit}} = \log_2\left(\frac{C}{s}\right)$$

where $N_{\text{crit}}$ is the log-scale dataset size and $s$ is the per-element metadata size.

---

## Physical Intuition / Derivation

### Why Cache Matters

Modern GPUs can perform teraflops of computation, but global memory bandwidth is the true bottleneck. A single L1 cache miss can cost 100+ cycles of stalled computation. By keeping frequently-accessed data in fast caches, we amortize this latency across many operations.

### The Utilization Cliff

Cache utilization does not degrade *gradually*. Instead, performance exhibits a sharp **utilization cliff**: as long as the active dataset fits in cache, throughput remains near-peak; once it exceeds cache capacity, throughput plummets to memory-bound levels.

From the source material, GPU-RMQ demonstrates this clearly:
- **RTX 3090 / RTX 4090** (24GB global memory): Performance remains high until $2^{22}$ elements (16 MB data fits in cache)
- **RTX 6000 Pro** (96GB global memory): GPU-RMQ sustains performance up to $2^{33}$ elements by maintaining a compact hierarchical structure that fits in L2 cache longer than competing methods (RTXRMQ, LCA)

### Hierarchical Structure Effect

GPU-RMQ achieves 4× better cache utilization (handling 4× larger datasets) than competing methods because:

1. **Compact representation**: Hierarchical acceleration structures encode range query information more densely
2. **Spatial locality**: Parent-child relationships in the hierarchy exhibit temporal reuse
3. **Reduced metadata**: 4–10× smaller memory footprint per query capability compared to flat LCA tables

When $C_{\text{GPU-RMQ}} = 0.25 \cdot C_{\text{competitors}}$, the effective dataset scaling is:

$$N_{\text{GPU-RMQ}} = 4 \times N_{\text{competitors}}$$

---

## Applications in Engineering

### 1. **Database Query Acceleration**
Range minimum/maximum queries (RMQs) power indexing in SQL and document retrieval. Efficient cache utilization directly reduces query latency in billion-row datasets.

### 2. **Bioinformatics & Sequence Analysis**
Substring pattern matching and sequence alignment require rapid RMQ evaluation. GPU caches sustain high throughput for whole-genome scans when hierarchical structures fit in memory.

### 3. **Real-Time Graphics & Game Engines**
Collision detection, spatial partitioning trees, and occlusion culling depend on cache-efficient data structures to maintain frame rates at high resolutions.

### 4. **High-Frequency Trading & Financial Modeling**
Tick data analysis and sliding-window statistics require sub-microsecond query latency—only achievable with optimal cache utilization.

### 5. **GPU-Accelerated Machine Learning**
Matrix operations and tensor reductions benefit from careful cache management to avoid bandwidth saturation, especially in sparse or irregular access patterns.

---

## Common Mistakes / Pitfalls

### 1. **Assuming Uniform Cache Behavior Across GPUs**
Different GPU generations (RTX 3090 vs. RTX 6000 Pro) have different cache sizes, L2 policies, and memory configurations. A cache-optimal algorithm for one card may perform poorly on another.

**Fix**: Profile on target hardware; design structures to scale gracefully across memory hierarchies.

### 2. **Ignoring Working Set Size**
Developers often assume "if my array fits in