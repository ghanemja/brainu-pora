# Burrows-Wheeler Transform (BWT)

## Definition

The **Burrows-Wheeler Transform** is a lossless data transformation algorithm that rearranges a string of characters to improve compressibility while remaining fully reversible. It reorders input symbols based on lexicographic sorting of all cyclic rotations of the input block, producing an output that exhibits high locality in symbol distribution—consecutive identical symbols cluster together, enabling highly efficient downstream compression.

Given an input string $S$ of length $n$, the BWT:
1. Generates all $n$ cyclic rotations of $S$
2. Sorts these rotations lexicographically
3. Outputs the last column of the sorted rotation matrix
4. Records the row index of the original string (the "primary index") to enable reverse transformation

## Key Equations

**Transform Output:**
Given sorted rotation matrix $M$ where row $i$ is the $i$-th lexicographically smallest rotation:

$$\text{BWT}(S) = M[0, n-1] \parallel M[1, n-1] \parallel \cdots \parallel M[n-1, n-1]$$

where the last column concatenation creates the transformed output.

**Inverse Reconstruction:**
The BWT is reversible through the Last-First mapping, exploiting the property that:

$$\text{LF}(i) = \text{rank of } M[i, n-1] \text{ among identical symbols in first column}$$

**Run-Length and Symbol Clustering:**
The BWT output exhibits dramatic probability shifts at run boundaries, motivating ensemble estimation:

$$P(s | h_t) = \frac{f_{m,h_t,s}}{\sum_{a=0}^{3} f_{m,h_t,a}}, \quad f_{m,h_t,s} = 1 + 2^{\alpha_m} c_{m,h_t,s}$$

where $c_{m,h_t,s}$ is the observed count of symbol $s$ in context $h_t$ for expert $m$, and $\alpha_m$ scales count influence in deep (sparse) context models.

## Physical Intuition / Derivation

**Why BWT Improves Compression:**

The transform exploits a fundamental observation: *symbols with similar left contexts tend to cluster together*. Consider the string "mississippi":

- All rotations beginning with 's' have already seen specific character sequences
- By sorting lexicographically, these rotations group together
- The *last* character of these grouped rotations becomes predictable from context

This is not a coincidence—sorting rotations is equivalent to grouping symbols by their *right context* (what came before in the original string). When symbols with similar right contexts are adjacent, standard entropy coders (arithmetic coding, range coding) see symbol frequencies that are locally stable rather than globally averaged.

**The Invertibility Guarantee:**

Despite destroying sequential information, BWT remains perfectly reversible because:
- The first column of the sorted matrix is deterministically recoverable (sort the output)
- The Last-First property creates a bijection: position $i$ in the transformed output maps to a specific position in the first column
- Following this mapping repeatedly recovers the original string

**Probability Dynamics at Run Boundaries:**

The BWT output naturally produces long runs of identical symbols. Between run boundaries, probability distributions can swing dramatically:

$$P(\text{symbol at position } i | \text{previous symbols}) \approx \begin{cases} \text{high} & \text{within a run} \\ \text{uncertain} & \text{at run boundary} \end{cases}$$

This motivates the use of **ensembles of exponential moving averages (EMA) with different time constants $\tau$**—a lightweight multiscale estimator that avoids expensive Krichevsky-Trofimov updates while adapting to both fast and slow distributional changes.

## Applications in Engineering

### 1. **Genomic Data Compression**
The source material describes application to nucleotide sequences, where:
- BWT preprocessing enables expert selection across context orders $k \in \{3, 7, 11, 13, 15\}$
- Per-block (80-symbol) expert selection chooses the best-performing Markov model
- Reverse-complement coupling ($\rho_{\text{rc}}$) exploits biological symmetry (DNA strands)

**Example:** The markov-mix codec maintains model state of ~2.45 GB (dominated by 2 GB order-15 model), achieving compression through block-wise expert selection rather than global model switching.

### 2. **Parallel Chunk-Based Coding**
The BWT output is partitioned into independent chunks of size $C = 2^{24}$ bytes:

$$\text{Chunks} = \lceil n/C \rceil$$

Once BWT is computed (sequential bottleneck), arithmetic/range coding across chunks is **embarrassingly parallel**:
- Each chunk stores its compressed size in a header
- Direct random-access decoding is possible without sequential dependency
- Scheduling overhead remains subdominant for practical blocks where $\lceil n/C \rceil$ is small

### 3. **Statistical Data Compression Backends**
BWT serves as a preprocessing stage for:
- **Arithmetic coding** with rescaling (CACM variant)
- **Range coding** with branchless, in-register context updates
- **PPM (Prediction by Partial Matching)** as alternative to per-symbol backoff

### 4. **Real-Time Adaptive Modeling**
The spike in probability at run boundaries is handled by ensemble methods:
- Fixed-step EMAs with different $\tau$ (sometimes called *Vitter counters* in compression literature)
- Avoids overhead of full Bayesian updates (Krichevsky-Trofimov)
- Provides low-latency adaptation to distributional shifts

## Common Mistakes / Pitfalls

1. **Assuming BWT is a Compression Algorithm**
   - BWT is a *preprocessing transform*, not a compressor itself
   - Compression gain comes from downstream entropy coding (arithmetic, range coding, etc.)
   - Without a back-end coder, BWT output may actually be *larger* than input

2. **Underestimating the Primary Index**
   - The primary index (position of original string in sorted matrix) must be stored
   - This is typically 4 bytes per block, creating