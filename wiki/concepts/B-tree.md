# B-tree

## Definition

A **B-tree** is a self-balancing, ordered search tree data structure optimized for systems with block-oriented I/O access (such as disk drives or transformer context windows). It generalizes binary search trees to accommodate multi-way branching.

**Formal Definition:** A B-tree of order $b$ (branching factor) is a tree where:
- Each internal node contains up to $b-1$ keys that partition a key space into $b$ ranges
- Each internal node has exactly $b$ children (except possibly the root)
- All leaves are at the same depth
- Each leaf contains data pages or references to data
- The tree remains balanced after insertion and deletion

**Key Property:** For a B-tree with branching factor $b$ and $N$ data pages, the height is bounded by:
$$h = \lceil \log_b N \rceil$$

This logarithmic height is the fundamental advantage over sequential search.

## Key Equations

**Retrieval Cost (Indexed Access):**
$$\text{Page reads} \leq \lceil \log_b N \rceil + 1$$

where the $+1$ accounts for the final data page read after traversing $\lceil \log_b N \rceil$ index pages.

**Sequential Access Cost (Lower Bound):**
$$\text{Page reads} \geq \Omega(N)$$

in the worst case; $\mathbb{E}[\text{reads}] = \frac{N+1}{2}$ under uniform random placement.

**Branching Factor (in token-constrained systems):**
$$b = \left\lfloor \frac{C}{\eta + \kappa + \delta} \right\rfloor$$

where:
- $C$ = page/context window capacity (tokens)
- $\eta$ = tokens per key
- $\kappa$ = tokens per separator key
- $\delta$ = tokens per entry formatting overhead

## Physical Intuition / Derivation

### Why Multi-Way Trees?

Binary search trees require $O(\log_2 N)$ comparisons but $O(\log_2 N)$ I/O operations. When each I/O is expensive (disk seek: ~10 ms; network round-trip: ~100 ms), the constant matters enormously.

A B-tree increases branching at the cost of slightly more comparison work *within* a single page. Since one page read is ~1000× more expensive than a single comparison, fitting $b$ children per node instead of 2 dramatically reduces I/O rounds.

### The Tree's Depth

With $b$ branches per internal node, the root can partition into $b$ ranges, each containing $\approx N/b$ remaining items. After one level, we've reduced search space by factor $b$. After two levels: $b^2$. After $h$ levels: $b^h$.

To accommodate $N$ pages at depth $h$:
$$b^h \geq N \implies h \geq \log_b N$$

Since the tree must be balanced, $h = \lceil \log_b N \rceil$ exactly.

### Branching Factor Selection

In page-constrained systems (like LLM context windows), each internal node is itself a page of capacity $C$ tokens. We must fit $b$ index entries, each requiring:
- A key (separates two child ranges): $\kappa$ tokens
- Metadata (child page identifier, formatting): $\eta + \delta$ tokens

This gives $b = \lfloor C / (\eta + \kappa + \delta) \rfloor$. **Counterintuitive result:** Larger page capacity increases branching, reducing tree depth automatically. A 4k-token context vs. 100-token context gives vastly different $b$, but the exponential separation $\log_b N$ remains dramatic.

## Applications in Engineering

### 1. **Database Indexing**
Relational databases (PostgreSQL, MySQL, SQLite) use B-trees as the primary index structure. A query on a 1-billion-row table requires $\approx \log_b (\text{1 billion}) \approx 3$–5 disk reads instead of 500 million sequential scans.

### 2. **File Systems**
Modern filesystems (NTFS, ext4, HFS+) organize directory entries and file metadata in B-tree-like structures. Finding a file in a million-file directory takes $O(\log N)$ operations.

### 3. **Key-Value Stores & NoSQL**
Systems like RocksDB, LevelDB, and Cassandra use B-tree variants (LSM trees) for efficient range queries and point lookups.

### 4. **Language Model Context Management** (from source)
When an LLM has a fixed context window $C$ tokens and must retrieve information from an external knowledge store of $N$ pages:
- **Sequential access** (flatten all pages as conversation history): $\Omega(N)$ page reads to find target
- **B-tree indexed access**: $\lceil \log_b N \rceil + 1$ page reads

With $b = \lfloor C / (\eta + \kappa + \delta) \rfloor$ determined by token budgets, a 4k-token context might give $b \approx 50$, allowing $N = 10^9$ pages retrievable in just 5 reads.

### 5. **Storage Hardware Optimization**
SSDs have 4 KB pages; databases choose $b$ such that one internal node fits one page. This minimizes cache misses and leverages hardware prefetching.

## Common Mistakes / Pitfalls

1. **Confusing height with $\log_2 N$**: B-tree depth is $\log_b N$, not $\log_2 N$. The base matters! With $b=100$, you get $\approx 5$ levels for a billion items; with $b=2$, you get $\approx 30$ levels. The exponential advantage is *huge*.

2. **Forgetting the data read**: The cost formula is $\lceil \log_b N \rceil + 1$ reads. The final $+1$ is the data page itself. Pure index traversal is one thing; actually retrieving the data is another.

3. **Assuming $b$ is free**: The branching factor