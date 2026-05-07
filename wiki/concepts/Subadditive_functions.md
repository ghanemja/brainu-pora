# Subadditive Functions

## Definition

A function $f: \mathbb{R}_{\geq 0} \to \mathbb{R}$ is **subadditive** if for all $x, y \geq 0$:

$$f(x + y) \leq f(x) + f(y)$$

Equivalently, in optimization contexts, a function is subadditive when the cost of combining two quantities is at most the sum of their individual costs. This contrasts with **superadditive** functions, which satisfy the reverse inequality.

A related concept is **strict subadditivity**: $f(x + y) < f(x) + f(y)$ for all $x, y > 0$, which implies diminishing returns or synergistic effects.

## Key Equations

**Subadditivity property (basic):**
$$f(x + y) \leq f(x) + f(y) \quad \forall x, y \geq 0$$

**Extended form (finite composition):**
$$f\left(\sum_{i=1}^{n} x_i\right) \leq \sum_{i=1}^{n} f(x_i)$$

**Normalized subadditivity** (often more useful in algorithms):
For $f-f(0)$ to be subadditive:
$$f(x+y) - f(0) \leq f(x) - f(0) + f(y) - f(0)$$

which simplifies to:
$$f(x+y) \leq f(x) + f(y) - f(0)$$

**Asymptotic form** (for algorithmic analysis):
$$\lim_{n \to \infty} \frac{f(n)}{n} = \inf_{n} \frac{f(n)}{n}$$

This limit exists for subadditive functions (Fekete's lemma).

## Physical Intuition / Derivation

### Why Subadditivity Matters

Subadditivity captures the intuition that "combining efforts has diminishing returns" or "there are no economies of scale that compound." Consider:

- **Cost allocation**: If the cost of processing 5 units plus 3 units exceeds the cost of processing them separately, you pay a premium for batching—anti-subadditive (superadditive).
- **Coverage problems**: When intervals are ordered sequentially and we pay for *exposed* (uncovered) portions, combining intervals may cause overlap, so $f(x+y) < f(x) + f(y)$ naturally arises.

### From the Source Material Context

In the interval ordering problem, $f$ assigns a cost to the exposed part of an interval. If we have:
- Interval of length $x$: exposed cost $f(x)$
- Interval of length $y$: exposed cost $f(y)$
- Combined: exposed cost $f(x+y)$

If there is *overlap potential* or *coverage reuse*, then $f(x+y) \leq f(x) + f(y)$. For example, with $f(x) = 2^x$ (exponential cost growth), subadditivity fails because $2^{x+y} = 2^x \cdot 2^y > 2^x + 2^y$. Yet the paper shows polynomial-time solutions *when* $f(x) - f(0)$ is subadditive—a structural property that enables dynamic programming.

## Applications in Engineering

### 1. **Algorithm Design & Complexity**
- **Interval Scheduling Optimization**: The source problem uses subadditivity to derive polynomial-time algorithms via DP. When $f(x) - f(0)$ is subadditive, the problem admits efficient solutions despite potentially exponential state spaces.
- **Parameterized Complexity**: Subadditive cost functions allow pruning in branch-and-bound algorithms because marginal costs decrease predictably.

### 2. **Network & Resource Allocation**
- **Load Balancing**: Distributing tasks across servers exhibits subadditivity when latency is shared (one server handling multiple tasks is cheaper per-task than separate servers).
- **Network Flow**: Link costs are often subadditive: sending 10+10 units across a link is cheaper than 20 units due to congestion pricing models.

### 3. **Manufacturing & Logistics**
- **Batch Processing**: Subadditive cost functions model economies of scale—batching 100 items into one shipment costs less than two 50-item shipments (plus overhead per shipment).
- **Inventory Management**: Holding cost $f(x) = cx$ is additive (linear); $f(x) = c\sqrt{x}$ is subadditive (square-root law in storage).

### 4. **Information Theory & Coding**
- **Compression**: Kolmogorov complexity of concatenated strings: $K(xy) \leq K(x) + K(y) + O(\log n)$ is subadditive (with logarithmic slack).
- **Error Correction**: Combining error correction codes exhibits subadditive redundancy requirements.

### 5. **Data Structures & Amortized Analysis**
- **Amortized Cost**: Many data structures (heaps, disjoint sets) have amortized costs that are subadditive by definition: total cost over $n$ operations is less than $n$ times the worst-case single operation.

## Common Mistakes / Pitfalls

### Mistake 1: Confusing with Concavity
**Wrong:** "Subadditive functions are concave."
**Right:** Subadditivity does *not* imply concavity. Example: $f(x) = \lfloor x \rfloor$ is subadditive but not concave everywhere. Concavity is a continuity/smoothness property; subadditivity is a discrete property.

### Mistake 2: Assuming $f(0) = 0$
**Wrong:** Applying $f(x+y) \leq f(x) + f(y)$ directly when $f(0) \neq 0$.
**Right:** The proper formulation is $f(x+y) - f(0) \leq f(x) - f(0) + f(y) - f(0)$ when $f(0) \neq 0$. This is