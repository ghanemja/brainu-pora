# Index Contraction Optimization

## Definition

**Index contraction optimization** is a computational strategy for evaluating tensor networks by exploiting sparsity patterns and ordering contractions to minimize arithmetic operations. The core principle is to contract tensors in an order that reduces the dimensionality of intermediate tensors, thereby avoiding expensive operations on high-dimensional objects.

In the context of constraint satisfaction problems represented as tensor networks (e.g., QUDO problems), the optimization leverages two key structural properties:

1. **Sparse tensor structure**: Constraint tensors with $m > 2$ indices contain only $O(d^2)$ non-zero elements (not $d^m$), due to value transmission constraints
2. **Contraction ordering**: Systematically contracting from edges inward reduces the growth of intermediate tensor dimensions

The result is an exponential reduction in computational complexity compared to dense tensor contraction.

---

## Key Equations

### Sparse Format Complexity

**Single row contraction** (n−3 tensors of dimension d):
$$\text{Cost} = O\left(\sum_{m=1}^{n-3} d^2 d^m\right) = O(d^{n-1})$$

**Dense format equivalent**:
$$\text{Cost}_{\text{dense}} = O\left(\sum_{m=1}^{n-3} d^3 d^m\right) = O(d^n)$$

**Full tensor network** (n layers):
$$\boxed{\text{Sparse complexity} = O(nd^{n-1})}$$
$$\text{Dense complexity} = O(nd^{n+1})$$

### Multi-row contraction
When contracting an $m$-index tensor (from previous rows) with a row of $m$ standard tensors:
$$\text{Cost}_{\text{sparse}} = O(md^m) \quad \text{vs.} \quad \text{Cost}_{\text{dense}} = O(d^{m+2})$$

### Subsequent variables
Determining the $m$-th variable without intermediate reuse:
$$\text{Cost} = O((n-m)d^{n-1-m})$$

### Memory footprint
Initial tensor network spatial complexity:
$$\text{Space} = O(n^2 d^2)$$
(lattice of $O(n^2)$ tensors, each with $O(d^2)$ non-zero elements)

---

## Physical Intuition / Derivation

### Why Sparse Structure Helps

In constraint satisfaction problems, a tensor $S$ encodes allowed value assignments. The constraint that *incoming values match outgoing values in each direction* creates diagonal or near-diagonal structure:

$$S_{\alpha_1, \alpha_2, \ldots, \alpha_m} \neq 0 \text{ only when constraints satisfied}$$

This reduces occupancy from $d^m$ to $O(d^2)$ elements—a massive reduction for large $m$.

### Contraction Order as a Computational Path

Consider a tensor network as a graph. Each contraction eliminates edges (indices). The key insight:

- **Contracting leaf tensors first** (right-to-left in a row) eliminates indices without creating large intermediates
- **Result**: Each new contraction operates on a tensor of roughly $d$ indices with $O(d^m)$ operations ($m$ indices from the row)
- **Cumulative cost**: $\sum_{m=1}^{n-3} O(d^m) = O(d^{n-1})$ rather than $O(d^n)$

### The Bottleneck: Last Two Layers

The bottleneck appears when contracting the final row (with $n$ tensors) against a large $(n-1)$-index tensor:
- Each element of this large tensor requires $O(d^m)$ operations to contract with a row
- This scales as $O(d^{n-1})$ unavoidably

This defines the lower bound for the entire algorithm.

---

## Applications in Engineering

### 1. **Constraint Satisfaction & Optimization**
- Solving QUDO (Quadratic Unconstrained Discrete Optimization) problems
- Supply chain optimization, scheduling, combinatorial design
- **Benefit**: Exact solutions for problems with special structure

### 2. **Probabilistic Graphical Models**
- Computing marginals in Bayesian networks or factor graphs
- Message-passing algorithms (belief propagation)
- **Application**: Decoding error-correcting codes, inference in probabilistic systems

### 3. **Quantum Computing Simulation**
- Simulating tensor networks (MPS, PEPS) for quantum states
- **Benefit**: Exponential speedup in simulating specific quantum circuit structures

### 4. **Machine Learning on Structured Data**
- Tensor decomposition and contraction in neural network compression
- Efficient computation of multi-way interactions in feature spaces

### 5. **Numerical Simulation**
- Evaluating partition functions in lattice models
- **Example**: Statistical mechanics computations in materials science

---

## Common Mistakes / Pitfalls

### 1. **Ignoring Sparsity Structure**
**Mistake**: Implementing tensor contraction with dense libraries (e.g., treating all tensors as full $d$-dimensional arrays)
- **Result**: $O(nd^{n+1})$ complexity; code becomes intractable for $n > 5$
- **Fix**: Use sparse tensor formats; exploit constraint structure explicitly

### 2. **Arbitrary Contraction Ordering**
**Mistake**: Contracting tensors in problem-given order rather than optimizing for intermediate size
- **Example**: Contracting large tensors from the center outward
- **Result**: Intermediate tensors grow to full $d^n$ dimensionality
- **Fix**: Always contract edges/leaves first, minimize free indices at each step

### 3. **Recomputation vs. Storage Trade-off**
**Mistake**: Assuming reuse of intermediate results always helps
- **Reality**: Exponential reduction is the same whether caching intermediates or recomputing ($O(nd^{n-1})$ either way)
- **Implication**: For single-variable solutions, reuse adds memory ($O(nd^{n-1})$ space) with negligible time gain

### 4. **Misidentifying the Bottleneck**
**