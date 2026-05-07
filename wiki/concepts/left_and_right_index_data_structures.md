# Left and Right Index Data Structures

## Definition

**Left Index (LI)** and **Right Index (RI)** are dual index data structures used to efficiently track and enumerate occurrences of alphabet symbols in text substrings during dynamic text processing and infix enumeration tasks.

Formally, for a word $w$ over alphabet $\Sigma$ and a position $p$ in $w$:

- **Left Index at position $p$**: Stores the $\leq p$ most recent occurrences of each symbol $a \in \Sigma$ appearing to the left of and including position $p$. Denoted $\text{LI}(p)$.

- **Right Index at position $p$**: Stores the $\leq p$ earliest/first occurrences of each symbol $a \in \Sigma$ appearing to the right of position $p$. Denoted $\text{RI}(p)$.

These structures maintain **occurrence lists**—ordered lists of positions where each symbol appears—enabling efficient infix matching and symbol frequency analysis.

## Key Equations

For a substring $w[l, r]$ where $l$ is a left boundary and $r$ is a right boundary:

$$\text{cover}(a) = \text{LI}(r) \cup \text{RI}(l-1)$$

This equation states that all occurrences of symbol $a$ in the interval $[l, r)$ are covered by:
- Symbols tracked in $\text{LI}(r)$ (up to $p$ most recent $a$'s to the left of $r$)
- Symbols tracked in $\text{RI}(l-1)$ (up to $p$ earliest $a$'s to the right of $l-1$)

When $a$ becomes **frequent** (appears more than $p$ times in $w[l, r]$), let $r_{\min}$ be the minimal position where this occurs:

$$|w[l, r_{\min}-1] \cap \{a\}| \leq p < |w[l, r_{\min}] \cap \{a\}|$$

## Physical Intuition / Derivation

### The Problem They Solve

When processing strings dynamically (streaming, infix enumeration), we need to quickly answer: *"What symbols appear in substring $w[l, r]$, and at which positions?"* 

Naively scanning the entire substring is prohibitively expensive. Instead, we maintain **sliding window indices** that track only the most relevant occurrences.

### Why Separate Left and Right Indices?

Consider a string sweep from left to right:

```
w = a b c a d a b a
    1 2 3 4 5 6 7 8
         [l    r]
```

As we move the right boundary $r$ rightward, we encounter new occurrences. But we can't afford to store all of them. The **Left Index** keeps the most recent (rightmost) occurrences of each symbol **before** $r$, which are the most useful for matching infixes ending at $r$.

Similarly, when the left boundary $l$ moves right, the **Right Index** tracks upcoming symbols (at position $l-1$ and beyond), capturing what's "coming next" after leaving the current window.

### Constant-Time Operations via Background Traversal

A **max-left background traversal** pre-computes over symbol $a$:
- The positions of the $\leq p$ last occurrences of $a$ in the full word
- These are obtained incrementally, allowing the traversal to finish in constant time even if interrupted

Given $\text{LI}(r_{l-1})$ and $\text{RI}(r_{l-1})$ at a critical position, we can concatenate and truncate occurrence lists to obtain coverage of all relevant $a$'s in $O(1)$ amortized time.

## Applications in Engineering

### 1. **Infix Enumeration and Pattern Matching**
In databases and search systems, enumerate all substrings matching a pattern (e.g., "$aΣ^*a$"—strings starting and ending with $a$) efficiently without listing all possible substrings.

### 2. **Streaming String Algorithms**
Maintain dynamic statistics over sliding windows (e.g., symbol frequency in text segments) while processing unbounded input streams with minimal memory overhead.

### 3. **Information Retrieval**
Index-based approximate substring matching in natural language processing, enabling fast range queries: "Find all positions where symbol $x$ appears between positions $l$ and $r$."

### 4. **Finite Automata State Minimization**
LI/RI structures support the tractability classification of regular languages (e.g., distinguishing $L = aΣ^*a$ vs. $L' = bΣ^*a$) by enabling efficient prefix-to-membership reduction.

### 5. **Text Compression and Edit Distance**
Accelerate longest common substring and repetitive structure detection by maintaining indexed occurrence lists across dynamic updates.

## Common Mistakes / Pitfalls

### 1. **Confusing "Last $p$" with "All Occurrences"**
LI/RI deliberately **truncate** to the $p$ most relevant occurrences. Forgetting this leads to incorrect complexity analysis. You cannot recover all symbol positions from LI/RI alone if the symbol is "frequent" (appears >$p$ times).

### 2. **Boundary Condition Errors**
- Positions are off-by-one-prone: Is $\text{LI}(p)$ the index *at* position $p$ or *before* position $p$?
- Setting $r = |w| + 1$ when no frequent occurrence exists requires careful sentinel handling.

### 3. **Misapplying Concatenation/Truncation**
When merging $\text{LI}(r_{l-1})$ (last $a$'s left of $r_{l-1}$) with $\text{RI}(r_{l-1})$ (first $a$'s right of $r_{l-1}$), you must:
- Avoid double-counting positions at the boundary
- Truncate the result to $\leq p$ entries, keeping the *most recent* from the left side

Failing to do so breaks