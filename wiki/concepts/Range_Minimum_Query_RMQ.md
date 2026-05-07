# Range Minimum Query (RMQ)

## Definition

A **Range Minimum Query (RMQ)** is a preprocessing and query operation on an array that answers the question: *given an array $A$ and a query interval $[l, r]$, what is the minimum value in $A[l..r]$?*

Formally, for an array $A[1..n]$, an RMQ $(l, r)$ returns:
$$\text{RMQ}(l, r) = \min_{i=l}^{r} A[i]$$

The goal of RMQ data structures is to answer such queries **efficiently** after a preprocessing phase, trading construction time and memory overhead for fast query answering.

### Problem Variants

- **Static RMQ**: Array is fixed after preprocessing; only queries are performed
- **Dynamic RMQ**: Array elements can be updated between queries
- **Batched RMQ**: Multiple queries processed simultaneously (e.g., on GPU)

---

## Key Equations

### Query Complexity Trade-off

For an array of size $n$, fundamental trade-offs exist between:

| Approach | Preprocessing | Query Time | Space |
|----------|---|---|---|
| Naive (no preprocessing) | $O(1)$ | $O(n)$ | $O(1)$ |
| Sparse Table | $O(n \log n)$ | $O(1)$ | $O(n \log n)$ |
| Segment Tree | $O(n)$ | $O(\log n)$ | $O(n)$ |
| Cartesian Tree | $O(n)$ | $O(1)$ after $O(n)$ space | $O(n)$ |

### Sparse Table Construction

For a sparse table $M[i, j]$ where $M[i, j] = \min(A[i..i+2^j-1])$:

$$M[i, j] = \begin{cases} 
A[i] & \text{if } j = 0 \\
\min(M[i, j-1], M[i+2^{j-1}, j-1]) & \text{if } j > 0
\end{cases}$$

Query answering using two overlapping intervals:
$$\text{RMQ}(l, r) = \min(M[l, k], M[r - 2^k + 1, k]) \quad \text{where } k = \lfloor \log_2(r - l + 1) \rfloor$$

### Batched Query Throughput

For GPU-accelerated RMQ with $q$ queries on array of size $n$:
$$\text{Throughput} \approx \frac{q \cdot n}{T_{\text{total}}} \quad [\text{queries/second}]$$

where construction time $T_{\text{const}}$ amortizes over a batch of queries.

---

## Physical Intuition / Derivation

### Why RMQ Matters

Consider a temperature monitoring system collecting $n$ sensor readings over time. A naive approach to answer "what was the minimum temperature between day $l$ and day $r$?" requires scanning all $r - l + 1$ values each time. For millions of historical queries, this becomes prohibitively slow.

RMQ data structures **precompute** strategic summaries of the array so that queries can be answered by combining these pre-computed results rather than rescanning the raw data.

### Hierarchical Decomposition Intuition

Modern GPU-accelerated RMQ (as in the source material) builds a **multi-level hierarchy** of range summaries:

1. **Level 0 (finest)**: Original array elements
2. **Level 1**: Minimum of consecutive blocks (e.g., min of 256 elements)
3. **Level 2**: Minimum of blocks at Level 1 (e.g., min of 256 Level-1 blocks)
4. **...Level k (coarsest)**: Single minimum of entire array

**Query answering**: To find $\min(A[l..r])$, identify which blocks fully lie within $[l, r]$, query the hierarchy, and post-filter partial blocks at the edges.

### Why GPU Acceleration Works

- **Data parallelism**: Thousands of queries can be answered simultaneously on different GPU threads
- **Memory coalescing**: Structured access patterns allow GPU memory bandwidth to be fully utilized
- **Hardware specialization**: Ray-tracing (RT) cores can be repurposed for hierarchy traversal via triangle-ray intersection tests

---

## Applications in Engineering

### 1. Computational Geometry & Spatial Queries
- **Lowest Common Ancestor (LCA)** in trees: RMQ on Euler tour of tree determines LCA in $O(1)$ time
- **Range aggregation**: Segment covering, interval scheduling
- **Collision detection**: Hierarchical bounding volumes use RMQ-like queries

### 2. Bioinformatics
- **DNA sequence analysis**: Find minimum GC-content regions
- **Protein fold prediction**: Query minimum energy states across sequence windows

### 3. Time-Series Data Processing
- **Sensor networks**: Efficiently query minimum readings from distributed sensors
- **Financial analytics**: Find minimum stock price in any historical window
- **Environmental monitoring**: Temperature, humidity, pressure range queries

### 4. Database Systems
- **Index structures**: RMQ accelerates min/max aggregates in OLAP queries
- **Time-series databases**: InfluxDB, TimescaleDB use similar hierarchical structures
- **Window functions**: SQL OVER clauses benefit from efficient RMQ

### 5. Signal Processing
- **Envelope detection**: Find minimum signal amplitude over time windows
- **Noise floor estimation**: Track minimum power levels

### 6. Computer Graphics
- **Texture filtering**: Minimum values in mipmap hierarchies
- **Ray tracing optimization**: Bounding volume hierarchies (BVH) use min queries for intersection culling

---

## Common Mistakes / Pitfalls

### 1. **Confusing RMQ with Sorting**
❌ *Error*: "I'll just sort the range and take the first element"  
✅ *Correct*: RMQ must preserve order—only minimum **value** is needed, not positions. Sorting destroys array structure needed for efficient hierarchy.