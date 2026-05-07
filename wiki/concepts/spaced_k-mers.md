# spaced k-mers

## Definition

A **spaced k-mer** is a subsequence extracted from a biological sequence (typically DNA) by applying a fixed binary mask pattern to select a subset of positions within a contiguous window of length $k$. 

Formally, given:
- A sequence $S = s_1 s_2 \ldots s_n$ over alphabet $\mathcal{N} = \{A, C, G, T\}$
- A mask pattern $M = m_1 m_2 \ldots m_k$ where $m_i \in \{0, 1\}$
- A position $i$ in the sequence

The spaced k-mer at position $i$ is the subsequence formed by selecting only positions where $m_j = 1$. The *weight* $w$ of the mask is the number of 1-bits: $w = \sum_{j=1}^{k} m_j$.

**Distinction from contiguous k-mers:** Contiguous k-mers use the all-ones mask $(111...1)$, selecting every position. Spaced k-mers use sparser patterns $(1011...01)$, skipping certain positions to improve mutation tolerance.

**Compact representation:** Each nucleotide encodes as 2 bits (A=00, C=01, G=10, T=11), allowing up to 32-mers to fit in a single 64-bit machine word.

## Key Equations

**Nucleotide bit encoding:**
$$\text{encode}(X) \in \{00_2, 01_2, 10_2, 11_2\} \quad \text{for } X \in \{A, C, G, T\}$$

**Storage requirement for $k$-mer:**
$$\text{bits required} = 2k \quad \text{(fits in 64-bit word when } k \leq 32\text{)}$$

**Spaced k-mer extraction with mask:**
If $M$ is a binary mask and $w = \text{popcount}(M)$ (number of set bits), the spaced k-mer is $w$ bits long:
$$\text{bits(spaced k-mer)} = 2w$$

**Throughput metric:**
$$\text{Throughput} = \frac{\text{sequence data (MB)}}{\text{time (sec)} \times \text{number of cores}}$$

Current state-of-the-art: ~750 MB/s per core.

## Physical Intuition / Derivation

### Why Spaced k-mers?

**Problem with contiguous k-mers:** A single point mutation (substitution) destroys *all* k-mers spanning that position, reducing search sensitivity. For example, in a 21-mer, one SNP eliminates 21 overlapping matches.

**Solution intuition:** By skipping certain positions with a mask, we allow the algorithm to match regions despite mutations at unmonitored positions. The mask is designed such that:
1. The $w$ selected positions are evolutionarily conserved (under selection pressure)
2. The skipped positions tolerate higher mutation rates
3. The total span remains $k$ for statistical significance

### Pattern Design Logic

A well-designed mask balances:
- **Sensitivity:** Fewer selected positions (lower $w$) → more mismatches tolerated → higher recall
- **Specificity:** More selected positions (higher $w$) → fewer spurious matches → higher precision
- **Span:** Window length $k$ determines the evolutionary distance captured

For example:
- Mask `101010101` (alternating) over span 9: weight=5, good for moderate divergence
- Mask `111000111` (clustered) over span 9: weight=6, emphasizes anchor regions

### Efficient Extraction via Bit Manipulation

The speed comes from CPU-level operations:

1. **Extract k-mer window:** Load 2k bits from position $i$
2. **Apply mask:** Bitwise AND with the mask pattern to zero out unwanted bits
3. **Compact bits:** Use BMI2 instructions (e.g., `PEXT`) to compress remaining bits contiguously
4. **Hash/Index:** Use the resulting value directly for lookups

This avoids iteration over individual positions and exploits instruction-level parallelism.

## Applications in Engineering

### 1. **Genome Assembly**
- De Bruijn graphs use k-mers as nodes; spaced k-mers reduce edge count while maintaining overlap information
- Better noise tolerance from sequencing errors

### 2. **Read Mapping & Alignment**
- Seed finding for long-read alignment (e.g., minimap, BLASR)
- Spaced seeds improve sensitivity over contiguous seeds by tolerating SNPs
- Faster indexing: fewer false positives to expand with dynamic programming

### 3. **Metagenomic Classification**
- Rapid taxonomic binning using k-mer profiles
- Spaced k-mers improve discrimination between species with high sequence similarity
- Lower memory footprint per classifier (fewer unique k-mers to track)

### 4. **Alignment-Free Sequence Comparison**
- Compute sequence distance/similarity without computing actual alignment
- Spaced k-mer distance metrics robust to insertion/deletion and substitution
- Used in phylogenetic estimation and contamination detection

### 5. **Quality Control & Error Detection**
- Identify problematic regions: unusual k-mer frequencies signal sequencing errors or contamination
- Spaced k-mers flag errors at positions prone to miscalls (homopolymer runs, low complexity)

### 6. **Database Search & Indexing**
- Build searchable indices for genomic databases
- Logarithmic query time with spaced k-mer prefiltering
- Critical for clinical genomics (variant databases, resistance gene detection)

## Common Mistakes / Pitfalls

### 1. **Ignoring Mask Orientation**
**Mistake:** Applying the mask in the wrong frame, or inconsistently between forward/reverse strands.  
**Impact:** Systematic bias, missing true matches, spurious matches.  
**Fix:** Ensure mask application is deterministic and consistent with database construction.

### 2. **Suboptimal Mask Design**
**Mistake:** Using a generic mask without validating for the target problem (e.g., using same mask for