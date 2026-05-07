# CKKS Scheme

## Definition

The **CKKS scheme** (Cheon-Kim-Kim-Song, 2017) is a *leveled* fully homomorphic encryption (FHE) scheme designed to encrypt and perform approximate arithmetic on **real and complex numbers**. Unlike integer-only schemes (BFV, BGV), CKKS uses floating-point-style approximate arithmetic with controlled noise management, making it particularly suited for machine learning, signal processing, and numerical computing applications.

**Key Characteristic:** CKKS trades *exact correctness* for *efficiency and practical usability*—acceptable for applications where inexact floating-point operations are standard.

---

## Key Equations

### Encoding and Scaling

CKKS encodes a real/complex vector $\mathbf{m} = (m_0, m_1, \ldots, m_{n-1}) \in \mathbb{C}^n$ via:

$$\text{Encode}(\mathbf{m}, \Delta) \mapsto \text{poly}(\lfloor \Delta \cdot \mathbf{m} \rfloor)$$

where $\Delta$ is a **scaling factor** controlling precision. Larger $\Delta$ preserves more precision but uses more noise budget.

### Rescaling (Noise Management)

After each multiplication, noise grows exponentially. CKKS applies **rescaling**:

$$ct' = \text{Rescale}(ct, q_i \to q_{i-1}) = \lfloor ct / p_i \rfloor_{q_{i-1}}$$

where $q_i$ is the modulus at level $i$ and $p_i$ is a prime factor. This reduces both the modulus and noise simultaneously, enabling deeper circuits than schemes without rescaling.

### Decryption Error

Decryption introduces approximate error:

$$\text{Decrypt}(ct) \approx \mathbf{m} + \epsilon$$

where $\epsilon$ depends on cumulative noise and rescaling operations. Application developers must manage **circuit depth** to remain within acceptable error bounds.

---

## Physical Intuition / Derivation

### Why Approximation?

Real-valued computations in practice—neural networks, physics simulations, signal processing—already use floating-point arithmetic with rounding errors. CKKS exploits this tolerance:

- **Exact schemes** (BFV/BGV) encode integers into polynomial rings, limiting precision for real numbers and causing rapid noise growth
- **Approximate schemes** (CKKS) directly encode real numbers with a scaling factor, mirroring how CPUs handle floats

### The Scaling Factor Trade-off

The scaling factor $\Delta$ is the "decimal point" analog:
- $\Delta$ **large** → high precision, but higher noise levels, fewer multiplication levels possible
- $\Delta$ **small** → more levels available, but lower precision

This is fundamentally different from exact schemes where precision is orthogonal to noise.

### Rescaling as Noise Control

Without rescaling:
$$\text{noise}_{after\_mult} \approx \text{noise}_1 \cdot \text{noise}_2 + \text{other terms} \quad (\text{explosive growth})$$

With rescaling:
$$\text{noise}_{after\_rescale} \approx \frac{\text{noise}_{after\_mult}}{p_i} \quad (\text{linear growth in depth})$$

This enables **multiplicative depth** $\log(Q/\Delta)$ proportional to the bit-length of total modulus $Q$.

---

## Applications in Engineering

### Machine Learning
- **Inference on encrypted data:** Neural networks over CKKS-encrypted inputs without decrypting (privacy-preserving prediction)
- **Ciphertext packing:** CKKS encodes vectors (not scalars), dramatically reducing number of ciphertexts and homomorphic operations for matrix multiplication (2.5–3× speedup with GPU acceleration)

### Signal Processing & Numerical Computing
- **Encrypted filtering:** IIR/FIR filter design on encrypted signals
- **Scientific computing:** Approximate solutions to PDEs with encrypted coefficients (acceptable for iterative solvers)

### Privacy-Preserving Analytics
- **Secure aggregation:** Multiple parties compute statistics without revealing individual records
- **Encrypted data mining:** Clustering, regression on encrypted datasets

### Hardware Acceleration
- **GPU deployment:** FIDESlib and similar libraries exploit CKKS's floating-point nature for efficient GPU tensor operations
- **Sparsity exploitation:** CKKS works naturally with sparse matrices (store only non-zero values), reducing memory and computation

---

## Common Mistakes / Pitfalls

### 1. **Confusing CKKS with Exact FHE**
**Error:** Assuming ciphertexts decrypt bit-perfectly.  
**Reality:** CKKS introduces unavoidable error; verify error bounds before deployment. For some ML tasks, errors $< 10^{-3}$ are invisible.

### 2. **Ignoring Depth vs. Precision Trade-off**
**Error:** Choosing $\Delta$ arbitrarily or too large.  
**Reality:** $\Delta$ directly trades off circuit depth. Compute required depth first: $\text{depth} = \lceil \log_2(Q/\Delta) \rceil - 1$. Set $\Delta$ accordingly.

### 3. **Assuming Ciphertext Packing is Automatic**
**Error:** Expecting a library to pack automatically.  
**Reality:** CKKS can pack $n$ complex numbers into one ciphertext (polynomial ring degree $= 2n$), but you must manually leverage this for matrix operations.

### 4. **Not Accounting for Rescaling Complexity**
**Error:** Treating rescaling as "free."  
**Reality:** Each rescaling reduces the modulus permanently; depth is bounded by the number of rescalings. Dense unrelated multiplications may fail after a few operations.

### 5. **Comparing Directly to BFV/BGV Without Context**
**Error:** Using CKKS for high-precision exact integer arithmetic.  
**Reality:** CKKS excels at approximate real-valued ML/signal processing. For exact cryptographic protocols or symbolic computation, BFV/BGV are better.

---

## See Also

- [[Fully Homomorphic Encryption (FH