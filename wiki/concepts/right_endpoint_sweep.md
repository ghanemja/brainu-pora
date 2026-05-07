# Right Endpoint Sweep

## Definition

The **right endpoint sweep** is an algorithmic technique for processing an input string or word by iteratively decrementing a right pointer $r$ from the end of the string toward position 1, maintaining invariants about which string positions and alphabet letters have been "visited" or "processed" by the sweep.

In the context of pattern matching and language decision problems, the right endpoint sweep works in conjunction with:
- **Occurrence lists** $\Lambda_a$ for each alphabet letter $a$, recording positions where $a$ appears
- **Letter frequency tracking** via counters $\text{nocc}'[a]$ that decrement as $r$ passes occurrences of letter $a$
- **Rare letter identification**, where a letter becomes "rare" in the prefix $w[1,r]$ once fewer than a threshold $p$ occurrences remain unprocessed

## Key Equations

Let $w$ be an input word of length $n$, and let $\text{occ}_a$ denote the set of positions where letter $a$ occurs.

**Rare letter condition:**
$$\text{letter } a \text{ is rare in } [1,r] \iff |\{i \in \text{occ}_a : i > r\}| < p$$

where $p$ is a fixed threshold (typically a small constant depending on the pattern being matched).

**Counter invariant:**
$$\text{nocc}'[a] = |\{i \in \text{occ}_a : i \geq r\}|$$

The counter decrements by 1 each time $r$ is decremented past an occurrence of $a$:
$$\text{nocc}'[a] \leftarrow \text{nocc}'[a] - 1 \text{ when } r \text{ moves from position } j \text{ to } j-1 \text{ and } j \in \text{occ}_a$$

## Physical Intuition / Derivation

### Why Sweep from Right?

The right endpoint sweep processes the word *backward*, which allows efficient **lazy evaluation** of pattern conditions. Rather than precomputing all information about the entire word, the algorithm defers work until necessary:

1. **Late binding of decisions**: As $r$ moves left, new positions enter the "active window" $w[1,r]$. Properties of this window are tested on-demand.

2. **Constant-time finalization of rare letters**: When a letter becomes rare (fewer than $p$ unprocessed occurrences remain), the min background traversal can finish in constant time by **Claim 6.4**:
   - Every position $i \geq r$ has already been visited during the sweep
   - At most $p-1$ positions with this letter remain
   - The remaining positions can be enumerated without further traversal

### Min Background Traversal Integration

The sweep is paired with a **min background traversal** for each letter—a separate pointer that advances through the occurrence list $\Lambda_a$ as $r$ moves. This ensures:

- **Synchronization**: Each rightward decrement of $r$ corresponds to one step of the traversal
- **Work distribution**: Heavy traversal work is spread across multiple decrements rather than concentrated when a letter becomes rare
- **Constant-time completion**: By the time a letter becomes rare, the traversal has already consumed most of the occurrence list, leaving only $O(p)$ work remaining

### Example Scenario

In Example D.2 with word $w = e^* a \, e^* b \, e^* a \, e^* b \, e^* a \, e^* b \, e^* a \, e^* b \, e^*$:

- Initially, both $a$ and $b$ are frequent (many occurrences remain)
- As $r$ decrements past position $i_6$ (an occurrence of $b$), the counter $\text{nocc}'[b]$ drops to 2, which is less than $p=3$
- Letter $b$ becomes rare; the min background traversal is finished in $O(1)$ time
- The unprocessed occurrences of $b$ are retrieved directly: $\Delta[b] = \{i_2, i_4\}$
- Similarly for $a$ at position $i_5$

## Applications in Engineering

### Pattern Matching & Text Search
Right endpoint sweeps enable **efficient pattern matching algorithms** where patterns are described by symbolic constraints (e.g., formal language specifications) rather than literal strings. The sweep avoids redundant scanning of the text.

### Finite Automata & Language Recognition
In decision procedures for languages defined by finite automata, the right endpoint sweep processes input words in reverse, allowing states to be computed incrementally rather than from scratch for each prefix.

### Compiler Optimization
Backward data-flow analysis in compiler back-ends (e.g., liveness analysis, reaching definitions) uses sweep-like traversals to propagate information from the end of a program toward its beginning.

### XML/Structured Data Processing
Stream-based processors that must recognize patterns in nested or sequenced data can apply right-sweep techniques to defer structural validation until necessary, reducing memory overhead.

## Common Mistakes / Pitfalls

1. **Neglecting the occurrence list ordering**: Many implementations assume $\Lambda_a$ is sorted. The source material explicitly notes that in the actual implementation, indices may be in *arbitrary order*. The min background traversal must not assume sorted input.

2. **Incorrect rare-letter threshold**: Setting $p$ too small causes premature "rarification," losing the benefit of deferred work distribution. Setting it too large wastes preprocessing. The choice of $p$ must be calibrated to the specific pattern/language being recognized.

3. **Off-by-one errors in finalization**: When a letter becomes rare at position $r$, at most $p-1$ occurrences remain in the unprocessed list. Confusing "exactly $p$" with "at most $p$" leads to incomplete result sets.

4. **Assuming the sweep is purely sequential**: The sweep pointer $r$ and the background traversal pointers are *independent* entities. Conflating them or assuming synchronized progression leads to skipped occurrences.

5. **Ignoring synchronization between multiple letters**: When multiple letters are tracked, their min background traversals must all advance in lock-step with $r$. Asynchronous advancement causes corrupted occurrence lists.

## See Also

- [[Occurrence List]]
- [[