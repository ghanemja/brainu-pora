# Lexicographical Ordering

## Definition

**Lexicographical ordering** (also called **dictionary ordering** or **lexicographic order**) is a method of arranging sequences or multi-component objects by comparing them element-by-element from left to right (most significant to least significant). The first differing element determines the relative order; if all compared elements match, the shorter sequence precedes the longer one.

Formally, for sequences $\mathbf{a} = (a_1, a_2, \ldots, a_n)$ and $\mathbf{b} = (b_1, b_2, \ldots, b_m)$:
- $\mathbf{a} <_{\text{lex}} \mathbf{b}$ if there exists an index $k$ such that $a_i = b_i$ for all $i < k$ and $a_k < b_k$, or if $\mathbf{a}$ is a prefix of $\mathbf{b}$.

## Key Equations

For bit-string comparisons (common in computer architecture):

$$\text{order}(\mathbf{x}, \mathbf{y}) = \begin{cases}
\mathbf{x} <_{\text{lex}} \mathbf{y} & \text{if } \exists k : x_i = y_i \, \forall i < k \text{ and } x_k < y_k \\
\mathbf{x} = \mathbf{y} & \text{if } x_i = y_i \, \forall i \\
\mathbf{x} >_{\text{lex}} \mathbf{y} & \text{otherwise}
\end{cases}$$

For floating-point numbers with independent fields (sign, exponent, mantissa):

$$\text{size}_{\text{total}} = \text{sizeof}(\text{sign}) + \text{sizeof}(\text{exponent}) + \text{sizeof}(\text{mantissa})$$

where the **most significant bit** (MSB) represents the sign, allowing lexicographical comparison to directly yield numerical ordering when fields are positioned by significance.

## Physical Intuition / Derivation

### Why Lexicographical Order Works for Multi-Field Comparisons

Consider sorting floating-point numbers. A number consists of three independent fields:
1. **Sign** (1 bit: negative vs. positive)
2. **Exponent** ($w_e$ bits: order of magnitude)
3. **Mantissa** ($w_m$ bits: fractional precision)

The numerical relationship between two numbers is determined hierarchically:
- If signs differ, the negative is smaller
- If signs match but exponents differ, the larger exponent indicates a larger magnitude
- If signs and exponents match, the larger mantissa indicates a larger value

Lexicographical ordering exploits this hierarchy by processing bits from **most significant to least significant**. By placing the sign at the MSB position and exponent above the mantissa, bit-level lexicographical comparison automatically respects numerical order.

### Inductive Construction

The source material demonstrates correctness via induction over bit position $k$:

**Base case** ($k=1$): Partitioning by the MSB (sign bit) correctly divides the array into two groups where all negatives precede positives (ascending order).

**Inductive step**: If the array is correctly sorted by the first $k$ bits, processing the $(k+1)$-th bit within each $k$-bit sub-partition further refines the sort. Elements are placed into 0-groups (bit=0) before 1-groups (bit=1). This extends the sorted property because:
- Elements within the same $k$-bit prefix are now distinguished by the $(k+1)$-th bit
- The placement rule (0 before 1) ensures lexicographical correctness
- All previous groupings are preserved (monotonicity)

This construction directly maps to the **radix sort** algorithm and justifies its correctness.

## Applications in Engineering

### 1. **Sorting Floating-Point Numbers in Hardware**
The primary application in the source material: designing efficient hardware sorters. By treating IEEE 754 floats as bit-strings and applying lexicographical ordering:
- Sign bit → primary partition
- Exponent bits → secondary partitions  
- Mantissa bits → tertiary refinement
- Negative numbers require special handling (bitwise inversion)

### 2. **Database Indexing and Query Processing**
B-trees and other index structures rely on lexicographical ordering:
- Composite keys (e.g., `(last_name, first_name, birth_date)`) are naturally ordered lexicographically
- Range queries across multiple fields become efficient
- Prefix searches align with lexicographical structure

### 3. **File System Path Comparison**
Operating systems compare directory paths lexicographically:
```
/home/alice
/home/bob
/home/bob/documents
/home/bob/downloads
```

### 4. **Protocol Header Processing**
Network packets are classified by examining headers field-by-field (destination, source, protocol, port) in lexicographical order.

### 5. **Version Numbering**
Software versions like `3.2.1` vs. `3.10.0` are compared lexicographically by component:
- Major version (3 = 3) → equal
- Minor version (2 < 10) → first version is smaller

### 6. **Cryptographic Ordering**
In distributed systems and blockchain, lexicographical ordering determines consensus and ordering of transactions.

## Common Mistakes / Pitfalls

### 1. **Confusing Lexicographical with Numerical Order (String Context)**
```
❌ WRONG: "9" > "10" (lexicographically)
✓ CORRECT: "10" < "2" (lexicographically); but 10 > 2 (numerically)
```
Lexicographical order is **not** numerical order for numeric strings. Use numeric conversion when appropriate.

### 2. **Ignoring Bit Position Significance in Hardware**
Students may apply lexicographical sort to floating-point bit-strings without ensuring the MSB encodes the most significant logical field (sign). If fields are misaligned:
```
❌ WRONG: Exponent at MSB, sign at middle → incorrect numerical order
✓