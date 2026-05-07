# LZ77 Compression

## Definition

**LZ77** (Lempel-Ziv 1977) is a lossless data compression algorithm that encodes data by replacing repeated sequences with references to earlier occurrences. Rather than storing literal characters, the compressor represents a substring as a tuple $(d, \ell)$ where:
- $d$ = **distance**: how many positions back the match begins
- $\ell$ = **length**: how many characters to copy

The compressed output is a sequence of tokens, each being either a literal character or a $(d, \ell)$ reference pair.

**LZ77 output structure**: For a string $w$, the compression $\text{LZ77}(w)$ produces a sequence of *blocks* $B = \{b_1, b_2, \ldots, b_n\}$, where each block encodes either a literal or a match reference.

## Key Equations

**Compression ratio and cost function:**
$$C(w) = \text{number of blocks in } \text{LZ77}(w)$$

For a given threshold parameter $p \in (0,1)$, a string $w$ is a **positive instance** if reducing the compression cost by a proportion $p$ would yield significant savings:
$$\text{improvement} \geq p \cdot C(w)$$

**Block pair inclusion ordering:**
If blocks $b_{i,1}, b_{i,2}$ and $b_{j,1}, b_{j,2}$ are consecutive block pairs from $\text{LZ77}(w)$, the fundamental structural property is:
$$b_{i,1}b_{i,2} \subset b_{j,1}b_{j,2} \quad \text{(proper substring inclusion)}$$

This forms a **strictly nested chain** for positive instances:
$$b_{1,1}b_{1,2} \subset b_{2,1}b_{2,2} \subset \cdots \subset b_{m,1}b_{m,2} \quad \text{with} \quad m \geq pC(w)$$

**Hitting set bound:**
For a thin hitting set $R$ of block pairs with cardinality:
$$|R| \leq \left\lceil \frac{C(w)}{t} \right\rceil = \left\lceil \frac{1}{p} \right\rceil \quad \text{where} \quad t = \lceil pC(w) \rceil$$

## Physical Intuition / Derivation

### Why LZ77 Works

LZ77 exploits the **redundancy** inherent in natural data: repeated sequences are common, and storing a backward reference (two integers) is often cheaper than storing the literal sequence.

### The Compression Analysis Problem

The source material addresses a *refinement* problem: given that a compressed string admits further optimization, how do we efficiently locate where to make edits?

**Core insight**: If we can reduce compression cost by $\geq p \cdot C(w)$, then there must exist a "long chain" of nested block pairs. This chain captures the structural relationship of edits.

**Why chains matter**: 
- Each block pair $b_i b_i'$ is a substring of the original word $w$
- If one block pair is contained in another, the larger one "encompasses" the edits made
- A long chain means edits are localized within a growing sequence of regions

### Hitting Set Strategy

Rather than enumerate all possible chains (exponential), we exploit the **partially ordered set (poset)** structure of block pairs under inclusion:

1. **Level assignment**: Assign each block pair $x$ a depth $d(x)$ = distance from the empty string $\varepsilon$ in the Hasse diagram
2. **Sparse residue selection**: Pick block pairs whose depths form a residue class modulo $t = \lceil pC(w) \rceil$
3. **Guarantee**: Any chain of length $\geq t$ must pass through all residue classes, thus intersecting our hitting set

This yields a small representative set $R$ with size $O(1/p)$ that necessarily "hits" every long compression chain.

### From Representatives to Edit Positions

For each representative $x \in R$:
1. Extract the substring **content** of $x$ from $w$
2. Search for all occurrences of this content within **Hamming distance 2** (allowing up to 2 character mismatches)
3. At least one such match will correspond to an optimal edit location

This converts the chain-hitting problem into a near-substring matching problem, which is solvable in polynomial time.

## Applications in Engineering

### 1. **Data Compression & Storage**
- **Gzip, PNG, DEFLATE**: Modern compression formats build on LZ77 principles
- **Backup systems**: Efficient incremental backups by finding repeated data blocks
- **Disk deduplication**: Identify duplicate content in storage arrays

### 2. **Network Protocol Optimization**
- **HTTP compression**: Browsers and servers use LZ77-based algorithms (gzip, brotli)
- **Video/audio streaming**: Reduce bandwidth by compressing frame data before transmission
- **DNS response compression**: Pointer-based references reduce packet sizes

### 3. **Bioinformatics & Sequence Analysis**
- **Genome compression**: Reference-based compression exploits repetitive DNA sequences
- **Sequence alignment**: LZ77 principles guide approximate matching algorithms
- **Protein database indexing**: Fast lookup via compressed representations

### 4. **Algorithm Design for Constraint Problems**
- **Edit distance computation**: Identify edit locations by analyzing compressed chains (as shown in the source material)
- **Approximate string matching**: Find similar sequences using compressed structure analysis
- **Outlier detection**: Regions that compress poorly often indicate novel or corrupted data

### 5. **Machine Learning Preprocessing**
- **Feature extraction**: Compressed representation encodes data regularity
- **Anomaly detection**: Unusual sequences have high compression cost
- **Dimensionality reduction**: Compression cost as a proxy for intrinsic data complexity

## Common Mistakes / Pitfalls

### 1. **Confusing Distance and Index**
❌ **Wrong**: Using absolute position in the string as distance  
✅ **Right**: Distance is relative offset backward from current position

### 2. **Forgetting the Greedy Nature**