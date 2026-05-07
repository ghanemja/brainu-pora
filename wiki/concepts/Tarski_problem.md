# Tarski Problem

## Definition

The **Tarski problem** is a fundamental computational search problem in the theory of fixed points and monotone functions. It asks: given query access to a monotone function, find a fixed point efficiently.

**Formal Definition (Tarski(n, k)):** Given a monotone function $f : [n]^k \to [n]^k$, find a point $x \in [n]^k$ such that:
$$f(x) = x$$

where $[n] = \{1, 2, \ldots, n\}$ and the domain/codomain is the lattice $[n]^k$ with the coordinate-wise partial order $\preceq$.

**Monotonicity Requirement:** A function $f: [n]^k \to [n]^k$ is monotone if:
$$a \preceq b \implies f(a) \preceq f(b)$$

for all $a, b \in [n]^k$, where $\preceq$ denotes coordinate-wise comparison.

### Tarski's Theorem (Brouwer-Tarski Fixed Point Theorem)

**Guarantee:** Every monotone function $f: [n]^k \to [n]^k$ admits at least one fixed point. This is a direct consequence of Brouwer's fixed-point theorem applied to the lattice setting.

### Relaxation: The Tarski* Problem

The **Tarski* problem** (Tarski-star) is a computational relaxation that provides algorithmic intermediate structure:

**Definition (Tarski*(n, k)):** Given query access to a monotone function $f : [n]^k \to [n]^k \times \{\pm 1\}$ satisfying:
1. $f(a)_{[k]} \preceq f(b)_{[k]}$ for all $a \preceq b$ (first $k$ coordinates are monotone)
2. $f(a)_{k+1} \leq f(b)_{k+1}$ for all $a \preceq b$ ($(k+1)$-th coordinate is monotone)

Find a point $x \in [n]^k$ satisfying **either**:
$$f(x)_{[k]} \succeq x \text{ and } f(x)_{k+1} = +1$$
**or**
$$f(x)_{[k]} \preceq x \text{ and } f(x)_{k+1} = -1$$

**Key Insight:** Unlike Tarski(n, k), a solution to Tarski*(n, k) is not required to be a fixed point—the additional binary coordinate provides "guidance" to relax the exact fixed-point requirement.

## Key Equations

### Query Complexity Bounds

**Theorem 1 (Tarski(n, k) complexity):**
$$\text{Query complexity of } \text{Tarski}(n, k) = O(\log^{\lceil(k-1)/3\rceil + 1} n)$$

**Theorem 2 (Tarski*(n, 3) complexity):**
$$\text{Query complexity of } \text{Tarski}^*(n, 3) = O(\log n)$$

**General Bound (Tarski*(n, k)):**
$$\text{Query complexity of } \text{Tarski}^*(n, k) \leq O(\log^{\lceil k/3 \rceil} n)$$

### Reduction Relationship

The reduction from Tarski(n, k+1) to Tarski*(n, k) satisfies:
$$Q(\text{Tarski}(n, k+1)) \leq O(\log n) \cdot Q(\text{Tarski}^*(n, k))$$

where $Q(\cdot)$ denotes query complexity.

### Decomposition (Safe Partial-Information Functions)

For safe partial-information functions used in algorithm design:
$$Q(\text{Tarski}^*(n, a+b)) \lesssim Q(\text{Tarski}^*(n, a)) \cdot Q(\text{Tarski}^*(n, b))$$

(from decomposition theorem of [CL22])

## Physical Intuition / Derivation

### Why This Problem Matters

The Tarski problem models equilibrium-finding scenarios in multi-agent systems and optimization:

- **Game Theory:** Finding a Nash equilibrium in a finite game where payoff functions are monotone
- **Economic Markets:** Equilibrium prices in supply-demand models with monotone clearing functions
- **Distributed Consensus:** Finding consensus points in systems with monotone preference/compatibility functions

### Intuition Behind Tarski*

The relaxation to Tarski* captures a practical algorithmic insight:

1. **Pure Fixed Point (Tarski):** Must find exactly $f(x) = x$—stringent requirement
2. **Signed Guidance (Tarski*):** The function "votes" via $f(x)_{k+1}$ whether to move up ($+1$) or down ($-1$) relative to $x$

This breaks the problem into a **binary search with feedback structure** rather than requiring exact equilibrium. The sign bit acts as an oracle guidance to navigate the lattice more efficiently.

### Why Query Complexity Matters

In computational complexity, **query complexity** measures the number of function evaluations needed in the worst case. For Tarski:
- Each query reveals $f(x)$ for one point $x$
- Lower bounds show $\Omega(\log n)$ queries are necessary (information-theoretic argument)
- Upper bounds use **binary search + divide-and-conquer** strategies on the lattice

The progression from $O(\log^{(k-1)/2+1} n)$ to $O(\log^{(k-1)/3+1} n)$ reflects algorithmic improvements in exploiting lattice structure via safe partial-information functions.

## Applications in Engineering

### 1. **Market Clearing and Economic Equilibrium**
- **Application:** Finding equilibrium prices in supply-demand networks
- **Why monotone:** Supplier quantity monotonically increases with price; consumer demand decreases monotonically
- **Use:** Auction mechanisms, dynamic pricing algorithms

### 2. **Distributed Consensus Algorithms**
- **Application