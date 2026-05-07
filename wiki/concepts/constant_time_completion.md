# constant time completion

## Definition

**Constant time completion** is a technique for efficiently finishing a partial traversal of a data structure (such as an occurrence list) in $O(1)$ time, exploiting the fact that only a bounded number of elements remain unprocessed.

More formally: Given a traversal that has processed elements at positions $\geq r$ in a sorted occurrence list, if at most $p$ unprocessed elements remain below position $r$, then the traversal can be completed in $O(1)$ amortized time by explicitly handling only those $O(p)$ remaining elements.

This technique is particularly useful in **streaming algorithms** where a parameter $r$ (the "right endpoint") sweeps left-to-right through a sequence, and you incrementally process elements as they are encountered. When a character becomes **rare** (i.e., fewer than $p$ occurrences remain in the unprocessed portion), the traversal switches to an exhaustive completion phase rather than continuing incremental processing.

## Key Equations

Let $\Lambda_a$ denote the sorted occurrence list for character $a$ in word $w$, and let $\text{nocc}'[a]$ denote the count of unprocessed occurrences of $a$.

**Condition for constant time completion:**
$$\text{nocc}'[a] < p \implies \text{completion cost} = O(\text{nocc}'[a]) = O(1)$$

where $p$ is a fixed parameter (typically $p = |\Sigma|$ or a constant threshold).

**Processing guarantee:**
If position $r$ has swept through all but at most $p$ occurrences in $\Lambda_a$, then:
$$\text{iterations already executed} \geq |\Lambda_a| - p$$

Therefore, the remaining elements to enumerate is $\leq p$, yielding $O(1)$ completion cost.

## Physical Intuition / Derivation

### The Core Insight

Imagine sweeping a "right endpoint" $r$ from right to left across a word $w$. As $r$ moves, you maintain occurrence counts for each character. When a character $a$ becomes **rare** (say, only 2 occurrences remain unprocessed), you face a choice:

1. **Continue incremental processing:** Keep sweeping until all occurrences are encountered. Cost: proportional to the number of positions between $r$ and the next unprocessed occurrence.
2. **Complete exhaustively:** Stop the sweep and directly enumerate the remaining $p-1$ unprocessed occurrences from the occurrence list. Cost: $O(p)$.

For a constant $p$, option 2 is $O(1)$ and becomes preferable once the character is rare.

### Why It Works: The Amortization Argument

Each position $r$ visits contributes one step to the **min background traversal** (a simultaneous traversal of all occurrence lists). By the time a character $a$ becomes rare:

- The traversal has already visited $\geq |\Lambda_a| - p$ positions where $a$ occurs.
- Hence, it has already processed $\geq |\Lambda_a| - p$ entries in $\Lambda_a$.
- At most $p-1$ entries remain; these can be handled by directly indexing into $\Lambda_a$ in $O(p) = O(1)$ time.

This avoids the cost of sweeping past all remaining positions to naturally encounter the last few occurrences of $a$.

### Example Walkthrough (from source)

In the example with word $w = e^* a \, e^* b \, e^* a \, e^* b \, e^* a \, e^* b \, e^* a \, e^* b \, e^*$:

- Both $a$ and $b$ initially have occurrence counts $> p = 3$, so are **frequent**.
- As $r$ is decremented from right to left, the min background traversal processes occurrences incrementally.
- When $r = i_6$, character $b$ has only 2 unprocessed occurrences (below $i_6$). It becomes **rare**.
- Instead of continuing the sweep, `GetRareOccurrencesSingle(b, 1, i_6-1)` finishes the traversal in constant time by directly accessing the remaining entries from $\Lambda_b$.
- Result: $\Delta[b] = \{i_2, i_4\}$ is stored in $O(1)$ time.

## Applications in Engineering

### 1. **String Matching & Pattern Recognition**
In languages defined by regular expressions or logical conditions (e.g., counting specific subsequences), constant time completion enables efficient enumeration of matching segments in streaming fashion without materializing all intermediate results.

### 2. **Database Query Processing**
When filtering tuples by multiple attributes, characters map to attribute values; rare attributes (few matching rows) can be completed quickly once detected, reducing I/O cost.

### 3. **Finite Automata & Language Recognition**
When building recognizers for languages with bounded alphabet, the technique amortizes the cost of state transitions by completing rare transitions (few remaining symbols) in $O(1)$ rather than sweeping the entire remaining input.

### 4. **Compressed Data Structures**
In suffix arrays, FM-index variants, or other compressed text indices, constant time completion allows random-access queries to unfinished ranges without decompressing full blocks.

### 5. **Real-Time Systems**
For applications with strict latency bounds (e.g., network packet processing), once a packet stream becomes rare (few remaining flows of interest), completion in $O(1)$ avoids worst-case delays.

## Common Mistakes / Pitfalls

### 1. **Confusing "Rare" with "Empty"**
A character is rare when $\text{nocc}'[a] < p$, not when it has zero occurrences. If you wait until it is completely gone, you've missed the early-completion opportunity. Always switch to exhaustive completion *as soon as* the threshold is crossed.

### 2. **Incorrect Threshold Selection**
If $p$ is too large, most characters never become rare, and you never benefit from constant time completion. If $p$ is too small (e.g., $p=1$), you enter the exhaustive phase too early, processing most characters exhaustively rather than incrementally. The optimal choice is algorithm-dependent; often