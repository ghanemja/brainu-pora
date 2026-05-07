# Hamming Distance

## Definition

The **Hamming distance** between two strings or sequences of equal length is the count of positions at which the corresponding symbols differ. Formally, for two strings $w$ and $w'$ of length $n$ over a common alphabet:

$$d_H(w, w') = |\{i : 1 \leq i \leq n, w[i] \neq w'[i]\}|$$

In other words, it measures the minimum number of **single-symbol substitutions** (edits) required to transform one string into the other.

The **Hamming ball** of radius $k$ centered at word $w$, denoted $B(w, k)$, is the set of all words within Hamming distance $k$ from $w$:

$$B(w, k) = \{w' : d_H(w, w') \leq k\}$$

## Key Equations

For strings of length $n$ over an alphabet of size $\sigma$:

**Maximum Hamming distance:**
$$d_H^{\max}(n) = n$$
(occurs when all positions differ)

**Size of Hamming ball** (for binary alphabet):
$$|B(w, k)| = \sum_{i=0}^{k} \binom{n}{i}$$

**Relationship to edit distance:** 
Hamming distance is a special case of edit distance where only substitutions are allowed (no insertions or deletions).

## Physical Intuition / Derivation

### Why Hamming Distance Matters

Consider transmitting data through a noisy channel. If you send a codeword $w$ and receive $w'$, the Hamming distance tells you how many bit flips occurred. This is intuitive: each differing position represents an error event.

### Why Only Substitutions?

Hamming distance restricts to substitutions (not insertions/deletions) because:
1. **Position-to-position correspondence:** Both strings must have equal length, so positions line up naturally
2. **Simplicity:** Counting mismatches at each position is computationally trivial (linear time)
3. **Information theory:** In fixed-length code systems, substitutions are the natural error model

### Hamming Ball Growth

For a binary string of length $n$, the Hamming ball $B(w, k)$ grows combinatorially. At radius $k$, there are $\binom{n}{k}$ strings differing in exactly $k$ positions. This exponential growth ($2^{kH(k/n)}$ where $H$ is binary entropy) is fundamental to coding theory—it limits how many codewords you can pack while maintaining error-correcting capability.

### Connection to Compression

In the source material, Hamming distance appears in the context of **LZ77 compression** and how edits (k-Modifications) within Hamming distance $k$ affect compression ratio. A word $w'$ at distance $k$ from $w$ is obtained by changing exactly $k$ symbols, and the question is: how much does this perturb the parse structure?

## Applications in Engineering

### 1. **Error-Correcting Codes**
Hamming codes use Hamming distance to measure code strength. A code with **minimum Hamming distance** $d_{min}$ can:
- Detect up to $d_{min} - 1$ errors
- Correct up to $\lfloor(d_{min}-1)/2\rfloor$ errors

This is the foundation of reliable data transmission in communication systems.

### 2. **Digital Communication & Data Storage**
- **QR codes, barcodes:** Use checksums based on Hamming distance to verify integrity
- **DRAM/Flash storage:** Error-correcting codes protect against bit flips
- **Network protocols:** Detect packet corruption

### 3. **Pattern Matching & Spell Checking**
Finding all words within Hamming distance $k$ from a query enables:
- Fuzzy string search (typo tolerance)
- DNA sequence alignment (approximate matching)
- Image similarity comparison

### 4. **Data Compression (as in source material)**
Understanding how small edits (within Hamming distance $k$) affect compression helps optimize pre-processing strategies. If you can identify words $w'$ near $w$ that compress better, you can apply targeted transformations.

### 5. **Machine Learning & Information Retrieval**
- **Nearest neighbor search:** Hamming distance provides efficient indexing in high-dimensional binary spaces
- **Locality-sensitive hashing:** Hash functions preserving Hamming distance enable approximate nearest-neighbor queries
- **Recommender systems:** Measuring user/item similarity

### 6. **Cryptography & Steganography**
- Cryptanalysis: Hamming distance between ciphertext and plaintext helps detect patterns
- Steganography: Embedding data in images by minimizing Hamming distance to original

## Common Mistakes / Pitfalls

### 1. **Confusing with Edit Distance (Levenshtein Distance)**
**Mistake:** Treating Hamming distance as equivalent to edit distance.  
**Reality:** Hamming distance *only* counts substitutions; edit distance also allows insertions and deletions. For strings of different lengths, Hamming distance is undefined.

### 2. **Assuming Symmetry in Cost**
**Mistake:** Thinking all positions contribute equally without considering alphabet size.  
**Reality:** For non-binary alphabets, the "distance" can be weighted differently (e.g., in DNA, mismatches between different nucleotides might have different costs biologically).

### 3. **Misinterpreting Hamming Ball Size**
**Mistake:** Forgetting that $|B(w, k)|$ grows combinatorially, leading to underestimated complexity.  
**Reality:** For large $k$ relative to $n$, the ball size approaches $2^n$, making exhaustive search infeasible.

### 4. **Ignoring String Length Constraint**
**Mistake:** Applying Hamming distance to variable-length sequences.  
**Reality:** Hamming distance requires equal-length strings; use edit distance for variable-length comparisons.

### 5. **Over-Relying on Triangle Inequality Misuse**
**Mistake:** Assuming triangle inequality bounds in algorithms without verifying that the intermediate string is in your search space.  
**Reality:** While Hamming distance satisfies