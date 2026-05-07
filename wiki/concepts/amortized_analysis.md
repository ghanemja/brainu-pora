# Amortized Analysis

## Definition

**Amortized analysis** is a method for analyzing the average cost of a sequence of operations on a data structure, where the cost is averaged over all operations in the sequence rather than bounding the worst-case cost of any individual operation. The key insight is that while some operations may be expensive, they occur infrequently enough that the average cost per operation remains low.

Formally, for a sequence of $n$ operations, the amortized cost per operation is:
$$\text{Amortized Cost} = \frac{\text{Total Cost of } n \text{ operations}}{n}$$

This differs fundamentally from worst-case analysis (which bounds the maximum cost of any single operation) and average-case analysis (which assumes probabilistic input distributions). Amortized analysis applies to deterministic sequences of operations.

## Key Equations

**Amortized Cost Definition:**
$$A_i = \frac{1}{n}\sum_{j=1}^{n} C_j$$

where $C_j$ is the actual cost of operation $j$ and $A_i$ is the amortized cost per operation.

**Potential Function Method:**
$$A_i = C_i + \Phi_i - \Phi_{i-1}$$

where:
- $C_i$ = actual cost of operation $i$
- $\Phi_i$ = potential (stored energy) of the data structure after operation $i$
- $A_i$ = amortized cost of operation $i$

**Total Cost via Potential:**
$$\sum_{i=1}^{n} C_i = \sum_{i=1}^{n} A_i + \Phi_0 - \Phi_n$$

## Physical Intuition / Derivation

### The Intuition

Imagine a bank account. When you withdraw money (perform an expensive operation), you're drawing on savings accumulated during cheap operations. Amortized analysis formalizes this idea: we "charge" each cheap operation slightly more than it actually costs, storing the excess as potential. When an expensive operation occurs, we spend down this potential to pay for it.

### Three Classical Techniques

#### 1. **Aggregate Analysis**

Sum the total cost of all operations, then divide by the number of operations.

*Example:* Dynamic array doubling
- Insertions: most cost $O(1)$, but doubling costs $O(n)$
- With $n$ insertions, doubling occurs $O(\log n)$ times
- Total cost: $O(n)$ (geometric series of copying)
- Amortized per insertion: $O(1)$

#### 2. **Accounting Method (Banker's Method)**

Assign a "charge" to each operation that may differ from its actual cost. Cheap operations are charged more; expensive operations are charged less. The accumulated credit pays for expensive operations.

*Steps:*
1. Define the amortized cost $A_i$ for operation $i$
2. Ensure total credit never goes negative: $\sum_{j=1}^{i} (A_j - C_j) \geq 0$ for all $i$
3. If this holds, then $\sum A_j$ upper bounds $\sum C_j$

#### 3. **Potential Function Method (Physicist's Method)**

Define a potential function $\Phi$ that maps the data structure state to a non-negative real number.

**Key Properties:**
- Start with empty structure: $\Phi_0 = 0$ (or define initial potential)
- End state potential can be non-zero
- Amortized cost of operation $i$: $A_i = C_i + \Delta\Phi_i$

**Why this works:** 
$$\sum_{i=1}^{n} C_i = \sum_{i=1}^{n} A_i - (\Phi_n - \Phi_0)$$

If we choose $\Phi$ so that $\Phi_n \geq \Phi_0$, then actual total cost is at most the sum of amortized costs.

### Derivation Through Memory Reallocation Example

From the source material, consider the memory reallocation problem:

- **Actual cost** of an operation: overhead = (total bytes moved) / (bytes inserted)
- **Naive bound:** In worst case, an insertion might force copying the entire heap, giving $O(M)$ overhead where $M$ is memory size
- **Amortized bound:** Allocate the data structure so that:
  - When used, live objects occupy at most $(1-\varepsilon)M$
  - Each insertion/deletion uses only "high-probability" space that rarely requires moves
  - Most operations have low cost; rarely an operation triggers rebuilding
  - Amortized overhead: $\text{polylog}(\varepsilon^{-1})$ (from the paper)

The **potential function** here represents "how fragmented is memory" or "how much work is owed for future rearrangements."

## Applications in Engineering

### Computer Science & Data Structures

| Data Structure | Operation | Amortized Cost | Use |
|---|---|---|---|
| **Dynamic Array** | Insertion | $O(1)$ | Automatic resizing; capacity doubles when full |
| **Splay Trees** | Search/Insert/Delete | $O(\log n)$ | Self-optimizing BST; rarely accessed nodes become expensive |
| **Disjoint Set Union** | Union/Find | $O(\alpha(n))$ | Nearly constant with inverse Ackermann; used in Kruskal's algorithm |
| **Binary Counter** | Increment | $O(1)$ | Counting $n$ increments costs $O(n)$ total despite individual bits changing |

### Memory Management

- **Garbage collection:** GC pauses amortized over time; occasional full collections justified by many cheap incremental collections
- **Memory reallocation:** As in the source paper—rearranging memory is expensive but necessary; amortized analysis proves efficiency
- **Virtual memory:** Page faults are expensive but occur infrequently; page replacement policies rely on amortized analysis

### Algorithms

- **Fibonacci heaps:** $O(1)$ amortized insert/decrease-key; $O(\log n)$ delete enables Dijkstra's with $O(E + V\log V)$ complexity