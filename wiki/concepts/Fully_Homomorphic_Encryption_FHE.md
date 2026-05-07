# Fully Homomorphic Encryption (FHE)

## Definition

**Fully Homomorphic Encryption (FHE)** is a cryptographic scheme that enables arbitrary computations on encrypted data without decryption. Formally, an FHE scheme allows an untrusted server to evaluate any computable function $f$ on ciphertexts $\mathrm{Enc}(m_1), \mathrm{Enc}(m_2), \ldots, \mathrm{Enc}(m_n)$ such that:

$$\mathrm{Dec}(\mathrm{Eval}(f, \mathrm{Enc}(m_1), \ldots, \mathrm{Enc}(m_n))) = f(m_1, \ldots, m_n)$$

Unlike **partially homomorphic** schemes (supporting only addition or multiplication), FHE supports *both* addition and multiplication circuits of arbitrary depth, enabling Turing-complete computation on encrypted data.

**Key property**: The plaintext messages remain secret throughout the entire computation—neither intermediate results nor the function itself need exposure to the computing party.

---

## Key Equations

### Homomorphic Properties

For ciphertexts $c_1 = \mathrm{Enc}(m_1)$ and $c_2 = \mathrm{Enc}(m_2)$:

**Additive homomorphism:**
$$\mathrm{Dec}(c_1 \oplus c_2) = m_1 + m_2 \pmod{p}$$

**Multiplicative homomorphism:**
$$\mathrm{Dec}(c_1 \otimes c_2) = m_1 \cdot m_2 \pmod{p}$$

### Sparse Matrix Multiplication (SpMSpM) in FHE

Given two $N \times N$ sparse matrices $A$ (stored CSR) and $B$ (stored CSC), the encrypted result element is:

$$C[i,j]_{\mathrm{encrypted}} = \bigoplus_{k: A[i,k] \neq 0 \land B[k,j] \neq 0} A[i,k] \otimes B[k,j]$$

where $\oplus$ and $\otimes$ denote homomorphic addition and multiplication. The hybrid CSR/CSC representation minimizes **rotation operations**:

$$\mathrm{EvalRotate}(c, r) = \text{rotation by } r \text{ positions in the plaintext slot vector}$$

---

## Physical Intuition / Derivation

### Why FHE is Necessary

Consider a cloud computing scenario: a client sends sensitive data to a server for computation. Traditional encryption forces decryption before processing—exposing plaintext to the server. FHE inverts this paradigm: *the server computes without ever accessing plaintext*.

### The Core Challenge: Noise Growth

Most FHE schemes (e.g., CKKS, BGV) rely on **lattice-based cryptography**. During computation:

1. Each ciphertext carries "noise" $e$ to hide the message: $c = m + e \pmod{q}$
2. Each homomorphic operation (multiplication especially) *amplifies* this noise
3. If noise exceeds the modulus $q$, decryption fails—this is called the **noise budget**

**Bootstrapping** (Gentry's breakthrough) refreshes the noise budget by homomorphically decrypting a ciphertext using its own private key. This permits arbitrary-depth circuits.

### Sparse Linear Algebra Optimization

The proposed GPU-optimized method addresses FHE's fundamental inefficiency for sparse operations:

- **Naive approach**: Treat all zero entries as real numbers → massive wasted computation
- **Smart sparsity exploitation**: Store only non-zero values (NZVs) with coordinate indices
- **Hybrid CSR/CSC layout**: 
  - CSR (Compressed Sparse Row) for matrix $A$ aligns with row-iteration in matmul
  - CSC (Compressed Sparse Column) for matrix $B$ aligns with column-iteration
  - This "row-column pairing" ensures accessed elements are pre-aligned, minimizing expensive homomorphic rotation operations

**Key insight**: Homomorphic rotations are bandwidth-intensive on GPUs; the hybrid layout reduces them by structurally matching the algorithm's access pattern.

---

## Applications in Engineering

### 1. **Secure Cloud Computing & Privacy-Preserving Analytics**
- Clients upload encrypted datasets; cloud performs ML inference without ever seeing raw data
- Banks can analyze customer transaction patterns without decrypting records
- Healthcare providers compute statistics on patient data while maintaining HIPAA compliance

### 2. **Federated & Collaborative Learning**
- Multiple parties perform joint machine learning without sharing plaintext models or gradients
- Critical for privacy-preserving model training across institutions
- Enables **secure multi-party computation (MPC)** protocols

### 3. **Graph Neural Networks (GNNs) on Encrypted Graphs**
- Analyze network topology (social networks, citation graphs, molecular structures) without exposing graph structure
- Crucial for competitive intelligence and biological data privacy

### 4. **Signal Processing & Bioinformatics**
- Process encrypted genomic data for disease association studies
- Analyze encrypted sensor streams without intermediate data exposure
- DNA sequence matching on encrypted sequences

### 5. **Compliance & Regulatory Requirements**
- GDPR, CCPA, and HIPAA increasingly mandate computation without decryption
- Automated processing of encrypted personal data in real-time systems

### 6. **Encrypted Database Queries**
- Query encrypted databases without revealing search terms or database structure
- Secure information retrieval without keyword exposure

---

## Common Mistakes / Pitfalls

### 1. **Confusing FHE with Searchable Encryption**
**Error**: Thinking FHE is just encrypted search.  
**Fact**: FHE supports *arbitrary computation*; searchable encryption typically supports only equality/range queries. FHE is strictly more powerful but far less efficient.

### 2. **Assuming "Encrypted Operands" Are Automatic**
**Error**: Believing that if encryption exists, both operands can be encrypted simultaneously.  
**Fact**: Most prior FHE sparse matmul systems assume one operand