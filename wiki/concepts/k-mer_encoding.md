# k-mer encoding

## Definition

**k-mer encoding** is a feature representation technique for genomic sequences where a sequence of length $k$ nucleotides (or characters from an alphabet) is converted into a numerical feature vector suitable for machine learning and data structure applications.

In genomics, a **k-mer** is a contiguous subsequence of length $k$ from a DNA/RNA sequence. The nucleotide alphabet is $\{\text{A}, \text{C}, \text{G}, \text{T}\}$ (or $\{\text{A}, \text{C}, \text{G}, \text{U}\}$ for RNA). **Ordinal k-mer encoding** maps each nucleotide position to a normalized ordinal value in the range $[0, 1]$:

$$\text{encoded position}_i = \frac{\text{nucleotide index}}{3}$$

where nucleotide indices are $\{0, 1, 2, 3\}$ for the four DNA bases.

The full encoded k-mer is a vector of $k$ normalized ordinal values, forming input features for neural networks and other machine learning models.

## Key Equations

**Ordinal encoding per position:**
$$x_i = \frac{n_i}{3} \in [0, 1], \quad n_i \in \{0, 1, 2, 3\}$$

**Encoded k-mer feature vector:**
$$\mathbf{x}_{k\text{-mer}} = [x_1, x_2, \ldots, x_k]^T$$

**Alternative: one-hot encoding** (for reference):
$$\text{one-hot}_i = [I(n=0), I(n=1), I(n=2), I(n=3)] \in \{0,1\}^4$$

where $I(\cdot)$ is the indicator function. This produces $4k$-dimensional sparse vectors.

## Physical Intuition / Derivation

### Why ordinal encoding for k-mers?

k-mer encoding bridges the discrete symbolic world of genomic sequences and the continuous feature spaces of machine learning. Unlike hash-based approaches (which destroy sequential structure), ordinal encoding preserves positional and sequence structure information:

1. **Positional awareness**: Each position in the k-mer maintains its identity; a mutation at position 1 differs from the same mutation at position $k$.

2. **Learnable representation**: MLPs can learn that adjacent nucleotides have relationships (e.g., codon structure, secondary structure propensities) because ordinal values preserve order: A < C < G < T or vice versa depending on biochemical context.

3. **Dimensionality efficiency**: Ordinal encoding produces $k$ features per k-mer; one-hot would require $4k$ features. For $k=15$, this is 15 vs. 60 dimensions.

4. **Normalization to [0,1]**: Normalizing by dividing by 3 ensures stable gradient flow in neural networks and fair comparison across positions.

### Why NOT hash-based features?

Hash functions (e.g., rolling hashes) destroy the sequential structure of k-mers. They are useful for fast counting and indexing but discard information about which positions matter—a trained model cannot learn position-specific patterns.

## Applications in Engineering

### 1. **Genomic Data Compression and Indexing**

**Context**: Genomics workloads process massive k-mer counts from whole-genome sequencing. Real datasets exhibit:
- **E. coli**: 5.3M keys, extreme skew ($\alpha = 0.97$), 42 distinct values
- **C. elegans**: 69.7M keys, intermediate skew ($\alpha = 0.82$), 760 distinct values

**Application**: Using ordinal k-mer encoding as input to learned compressed static functions (CSF), researchers can compress k-mer count tables to 5–26 bits per key—dramatically reducing memory compared to hash tables (which offer no compression) or MPH tables (7–70× more memory).

### 2. **Machine Learning for Genomics**

k-mer encoding enables:
- **Classification**: Predicting organism species, antibiotic resistance, or disease association from genomic k-mer profiles
- **Variant calling**: Distinguishing true genetic variants from sequencing errors
- **Metagenomic binning**: Assigning short reads to source organisms using k-mer composition

### 3. **Sequence Similarity Search**

k-mers enable fast approximate matching:
- BLAST and similar tools use k-mer seeds to quickly identify candidate alignments before expensive alignment scoring
- Ordinal encoding could improve learned index structures for similarity queries

### 4. **De Novo Assembly**

Genome assembly algorithms (e.g., de Bruijn graphs) fundamentally rely on k-mer counting to build overlap graphs. Compression and efficient indexing of these counts directly impacts assembly speed and memory footprint.

## Common Mistakes / Pitfalls

### 1. **Conflating k-mer encoding with k-mer representation**

- **Mistake**: Assuming all k-mer "encodings" preserve sequence structure equally.
- **Reality**: Hash-based, ordinal, one-hot, and embedding-based encodings have fundamentally different information content. Choose based on whether sequential structure or fast hashing matters more.

### 2. **Over-normalizing ordinal values**

- **Mistake**: Using raw indices $\{0, 1, 2, 3\}$ directly without dividing by 3, leading to inconsistent feature scaling and poor neural network training.
- **Fix**: Always normalize ordinal features to $[0, 1]$ or use standardization.

### 3. **Ignoring reverse complement**

- **Mistake**: In double-stranded DNA, k-mer "ACGT" and its reverse complement "ACGT" (opposite strand, reversed) are identical sequences biologically. Treating them as separate doubles the data.
- **Context**: This may or may not matter depending on the application (abundance counting vs. classification), but should be considered explicitly.

### 4. **Wrong k value**

- **Mistake**: Choosing $k$ arbitrarily without considering:
  - Organism genome size: $k$ should be large enough that random k-mers are unlikely ($k \geq \log_4 G$ for genome size $G$)
  - Model capacity: Too small $k