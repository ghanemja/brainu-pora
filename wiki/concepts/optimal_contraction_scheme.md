# Optimal Contraction Scheme

## Definition

An **optimal contraction scheme** is a systematic approach to evaluating tensor networks by ordering the sequence of pairwise tensor contractions to minimize computational complexity. For a tensor network problem, an optimal scheme determines the order in which tensors are combined (contracted) such that the overall number of arithmetic operations is minimized, rather than contracting arbitrarily or in a fixed left-to-right order.

In the context of structured tensor networks (e.g., chain or tree-like architectures), an optimal contraction scheme reduces the computational complexity from potentially exponential scaling to polynomial scaling in the network size and bond dimensions.

---

## Key Equations

For a tensor network with $n$ nodes, bond dimension $d$, and degree of connectivity $k$ (maximum number of neighbors per variable):

### Matrix-Vector Method (Dense Representation)
$$\text{Complexity}_{\text{dense}} = O(nd^{2k})$$

where $n$ contractions of a $d^k \times d^k$ matrix with vectors are required.

### Sparse Tensor Method (Exploiting Sparsity)
$$\text{Complexity}_{\text{sparse, single}} = O(nd^{k+1}) \quad \text{per variable}$$

$$\text{Complexity}_{\text{sparse, total}} = \begin{cases}
O(n^2d^{k+1}) & \text{without reuse} \\
O(nd^{k+1}) & \text{with intermediate reuse}
\end{cases}$$

### Stair-Structured Networks
$$\text{Complexity}_{\text{stair}} = O(nkd^k) \quad \text{for } k \geq 3$$

**Spatial Complexity:**
$$\text{Space}_{\text{sparse}} = O(nd^{k+1})$$

---

## Physical Intuition / Derivation

### Why Contraction Order Matters

Consider contracting three tensors $A$, $B$, $C$ with dimensions roughly $d \times d \times d$:
- **Left-to-right:** $(A \circ B) \circ C$ performs one contraction of cost $\sim d^4$, then another of cost $\sim d^4$ → total $O(d^4)$
- **Different order:** contracting $B$ and $C$ first might yield a much smaller intermediate object, reducing subsequent cost

For large tensor networks, suboptimal ordering compounds: choosing bad contraction sequences can increase complexity from $O(nd^{k+1})$ to $O(n^2d^{k+1})$ or worse.

### Sparsity Exploitation

The key insight in the sparse tensor method is recognizing that many tensors have **redundant index structure**: if a tensor has $k$ neighbor interactions, it typically contains $k-1$ pairs of repeated input-output indices. This means:

$$\text{Non-zero elements} \approx d^{k+1} \quad \ll d^{2k}$$

For sparse tensors with $O(d^{k+1})$ non-zero entries, matrix-vector multiplication requires only $O(d^{k+1})$ operations rather than $O(d^{2k})$.

### Intermediate Reuse

When solving for multiple variables (as in quantum optimization or probabilistic inference), an optimal contraction scheme reuses intermediate contractions from previous computations. Rather than fully re-contracting for each new variable, only a single additional matrix-vector multiplication ($O(d^2)$) is needed after the initial full contraction, reducing total complexity from $O(n^2d^{k+1})$ to $O(nd^{k+1})$.

---

## Applications in Engineering

### 1. Quantum Circuit Simulation
- Contracting tensor networks representing many-body quantum states
- Critical for simulating NISQ (Noisy Intermediate-Scale Quantum) devices where state vectors become intractable
- Optimal schemes enable simulation of systems with 20-30 qubits via tensor networks where naive approaches fail at 15+

### 2. Probabilistic Graphical Models & Inference
- Computing marginal probabilities in Bayesian networks and factor graphs
- Optimal contraction reduces inference time from exponential to polynomial in many structured domains
- Applications: medical diagnosis, robotics belief propagation, constraint satisfaction

### 3. Variational Quantum Algorithms (VQA)
- When solving QUDO (Quantum Unconstrained Optimization) problems
- Determining each variable requires contracting tensor chains; optimal reuse means only one full contraction needed regardless of number of variables
- Reduces per-variable cost from $O(nd^{k+1})$ to $O(d^2)$ after initial setup

### 4. Machine Learning & Tensor Decomposition
- Training tensor networks for numerical computing and ML
- Efficient backpropagation through tensor network layers
- Low-rank approximations of high-dimensional data

### 5. Classical Simulation of Quantum Systems
- Computing partition functions in statistical mechanics
- Evaluating expectation values in quantum many-body systems
- Study of strongly correlated electrons and condensed matter phases

---

## Common Mistakes / Pitfalls

### 1. **Ignoring Sparsity Structure**
- **Mistake:** Treating sparse tensors as dense $d^{2k}$ objects
- **Consequence:** Inflates complexity estimates by factors of $d^k$; algorithms appear intractable when they're actually feasible
- **Fix:** Explicitly track which indices are constrained/repeated before estimating flops

### 2. **Failing to Recognize Reuse Opportunities**
- **Mistake:** Recomputing full tensor contractions for each variable independently
- **Consequence:** $O(n^2d^{k+1})$ complexity instead of $O(nd^{k+1})$
- **Fix:** Structure algorithm to save intermediate contraction results from first variable evaluation

### 3. **Confusing Bond Dimension Scaling**
- **Mistake:** Assuming bond dimension is $d$ throughout; forgetting it grows as $d^k$ for a node with $k$ neighbors
- **Consequence:** Underestimates memory and compute requirements; crashes in production
- **Fix:** Carefully track bond dimension at each node based on connectivity

### 4. **Neglecting Tensor Network Topology**
- **Mistake:** Using