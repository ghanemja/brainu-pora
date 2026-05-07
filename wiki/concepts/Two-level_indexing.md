# Two-level Indexing

## Definition

**Two-level indexing** (also called **hierarchical indexing** or **DEEP-INDEXED**) is a data retrieval strategy that organizes an index itself as an indexed structure, creating a recursive hierarchy to maintain constant-time lookup performance as the indexed dataset grows. Instead of storing all page references in a single flat index, a second-level index catalogs ranges or sections of the primary index, allowing a search agent to first locate the relevant portion of the index, then perform the final lookup within that section.

**Formal structure:**
- **Level 0 (Data):** Content distributed across $M$ pages
- **Level 1 (Primary Index):** Flat index of $N = M/k$ entries (one per $k$ pages)
- **Level 2 (Secondary Index):** Index over the primary index, with $\lceil N/k \rceil$ entries

This recursive design prevents performance degradation when the index itself becomes too large for a single-pass search.

## Key Equations

### Lookup Cost Model

**Flat indexing cost** (single-level):
$$C_{\text{FLAT}} \approx O(M^2)$$

The cost scales quadratically because as the dataset grows, the index grows linearly with $M$, and searching an index of size $M/k$ requires $O(M)$ scans, yielding $O(M) \times O(M) = O(M^2)$ cumulative token expenditure.

**Single-level indexed cost:**
$$C_{\text{INDEXED}} = O(1)$$

Retrieval requires exactly one index lookup plus one data page read when the index remains navigable.

**Two-level indexed cost** (hierarchical):
$$C_{\text{DEEP-INDEXED}} = O(1) + O(1) = O(1)$$

The secondary index is small enough ($\lceil \sqrt{M} \rceil$ entries) to remain navigable, so two lookups in constant time preserve $O(1)$ retrieval.

### Recursion Condition (Library Theorem)

The indexing strategy applies recursively to any sequential store, including the index itself:

$$\text{If index size } N = M/k \text{ exceeds navigability threshold } T, \text{ then index the index.}$$

This creates a logarithmic stack depth: $\log_k M$ levels are needed in the worst case, though in practice 2 levels suffice for practical values of $M$.

## Physical Intuition / Derivation

### Why Flat Indexing Fails

Consider a knowledge base with $M = 1,000$ items distributed across 100 pages. A flat `get_index()` call returns a 100-entry table of contents. For a language model scanning sequentially:

- **First lookup:** Find the target range in the 100-entry index → requires reading/scanning most of the index
- **Token cost:** The model must attend to ~100 entries in the index, then read the target page
- **Scaling problem:** At $M = 5,000$ (500 pages), the flat index grows to 500 entries, requiring proportionally more tokens to search

The token cost becomes $O(M)$ per query, and since each query traverses the full index, total cost is $O(M^2)$.

### How Two-Level Indexing Restores Efficiency

By organizing the index hierarchically:

1. **Secondary index:** 5 sections, each covering 100 pages → $\lceil 500 / 100 \rceil = 5$ entries
   - Cost to search the secondary index: constant (5 entries is trivially navigable)
2. **Primary index:** 100 entries within the target section
   - Once the correct section is identified, the primary index is small enough for direct lookup
3. **Result:** 1 page read, regardless of $M$

**Empirical confirmation from data:** At $M = 1,000$, single-level INDEXED degrades (94% accuracy), but DEEP-INDEXED maintains steady performance (90% accuracy, 1–2 page reads). At $M = 5,000$, DEEP-INDEXED holds at 1–2 reads while flat approaches fail.

### Recursive Application

The Library Theorem is **self-similar**: if the primary index becomes too large to search efficiently, the same recursion principle applies to the index itself. This is not a limitation but a feature—it extends the method to arbitrary scales:

$$\text{Index the index the index...}$$

In practice, 2–3 levels suffice for $M$ up to $10^6$ or more.

## Applications in Engineering

### 1. **Database Systems**
- **B-trees and B+ trees** use recursive indexing: internal nodes index regions of child nodes, which index data pages
- Maintains $O(\log_B N)$ lookup time where $B$ is block size
- Standard in production databases (MySQL, PostgreSQL)

### 2. **File System Organization**
- **Multi-level file allocation tables** (FAT32, NTFS): clusters organized into regions, with a master index
- Inodes in Unix-like systems use direct, indirect, and double-indirect blocks—a form of hierarchical indexing

### 3. **Virtual Memory & Page Tables**
- **Multilevel page tables** (x86-64 uses 4 levels): virtual addresses are hierarchically decomposed to avoid storing a single flat page table of $2^{64}$ entries
- Each level indexes the next, reducing memory overhead and enabling sparse address spaces

### 4. **Search Engines & Information Retrieval**
- **Inverted index hierarchies:** term → section → documents
- **Sharded indices:** partitions of a search index are themselves indexed by a partition index
- Enables efficient scaling to billions of documents

### 5. **Time-Series Databases**
- **Block indices:** data organized into time blocks, with an index of block ranges and their timestamps
- Allows fast range queries without scanning all blocks

### 6. **Large Language Models & Context Windows**
- As described in the source: managing retrieval-augmented generation (RAG) over large corpora
- Two-level indexing allows the model to locate relevant documents with constant token overhead, regardless of corpus size

## Common Mistakes / Pitfalls

### 1. **Assuming One Level Suffices**
- **Mistake:** Implementing a single index and expecting it to scale linearly