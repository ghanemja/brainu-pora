# direct access queries

## Definition

**Direct access queries** are a class of database queries that maintain a dynamic data structure over an evolving word (string) such that, given an index $i$, one can directly retrieve the $i$-th occurrence of an infix matching a regular language $L$ without enumerating all preceding occurrences.

Formally, suppose we have:
- A word $w$ that changes under update operations (e.g., letter substitutions)
- A regular language $L$ over alphabet $\Sigma$
- An $L$-infix: a contiguous substring $w[j..k]$ such that $w[j..k] \in L$

A **direct access query** answers: *"What is the $i$-th $L$-infix in the current word $w$?"* and returns the indices $[j_i, k_i]$ identifying that infix, or determines that fewer than $i$ infixes exist.

This contrasts with:
- **Membership queries**: determining whether a given infix $[j,k]$ belongs to $L$
- **Enumeration queries**: listing all $L$-infixes (incurs cost per occurrence)

## Key Equations

Let $n = |w|$ be the word length and $m$ be the number of $L$-infixes in $w$.

The primary complexity measure is:

$$T_{\text{query}}(i) = \text{time to retrieve the } i\text{-th } L\text{-infix}$$

$$T_{\text{update}} = \text{time to process one letter update}$$

The data structure must satisfy:
- Correctness: for all $1 \leq i \leq m$, query returns the $i$-th infix in sorted order
- Efficiency: $T_{\text{query}}(i)$ and $T_{\text{update}}$ are sublinear in $n$

## Physical Intuition / Derivation

**Why is direct access non-trivial?**

Consider a naive approach: on each query for the $i$-th infix, scan the entire word and extract all $L$-infixes, then return the $i$-th. This requires $O(n^2)$ time per query in the worst case (checking all $O(n^2)$ substrings). When the word updates, all infixes must be recomputed.

**The challenge:** Regular languages can have complex structure. For example:
- $L = aa$ (consecutive pairs of $a$'s) may have $\Theta(n)$ infixes
- $L = aΣ^*b + bΣ^*a$ (words with $a$ then $b$, or $b$ then $a$) exhibits different structural patterns

**The key insight** is that by maintaining a carefully designed auxiliary data structure (e.g., based on finite automaton states and position indices), one can:
1. Track which positions *can* start an $L$-infix (via automaton state analysis)
2. Use index structures (e.g., balanced trees) to map from "occurrence number $i$" to actual text positions
3. Support updates incrementally without recomputing all infixes

This is possible *when the language has low description complexity* relative to the word length. For tractable languages, one achieves query time significantly better than the word length $n$.

## Applications in Engineering

### 1. **Dynamic Information Extraction**
Document spanners and information extraction systems must track patterns (e.g., entities matching a regex) as documents are edited in real-time. Direct access queries enable jumping to the $i$-th entity occurrence instantly, useful in:
- Text editors with "go to $n$-th match" functionality
- Database views over evolving documents

### 2. **Pattern Matching in Streaming Data**
In network monitoring or log analysis, one indexes network flows or log entries matching a signature pattern. Direct access allows:
- Query: "retrieve the 1000-th suspicious packet stream"
- Without scanning the first 999 infixes

### 3. **Biological Sequence Analysis**
DNA/protein sequence databases maintain indices of motif occurrences. Direct access enables:
- Fast lookup of the $i$-th occurrence of a conserved domain
- Efficient comparative genomics queries

### 4. **Full-Text Search Engines**
Augment inverted indices with direct access to the $i$-th occurrence of a phrase pattern in a dynamically updated document collection.

## Common Mistakes / Pitfalls

1. **Confusing with enumeration:** Direct access queries do *not* enumerate all infixes; they jump directly to index $i$. Enumeration-based solutions that list all $O(m)$ matches first are inefficient for large $m$ and sparse queries.

2. **Assuming $O(1)$ per query:** Even with direct access, query time typically depends on $\log m$ or $\log n$ (logarithmic in the index), not constant. Students sometimes expect direct array indexing.

3. **Underestimating update cost:** Maintaining the index under dynamic updates requires rebalancing data structures. The update operation is not "free"—there is inherent trade-off between query and update time.

4. **Overgeneralizing to arbitrary languages:** Direct access is tractable only for *specific* regular languages with manageable structure. For arbitrary languages $L$, the number of $L$-infixes can be exponential in $n$, rendering the problem intractable.

5. **Ignoring the role of neutral letters:** For some languages (e.g., $L = aa$ with a neutral letter), even deciding tractability is subtle. A neutral letter $\epsilon$ can "split" infixes in non-obvious ways, complicating index structure design.

## See Also

- [[Dynamic membership queries]] — testing whether a given infix belongs to $L$ under updates
- [[L-infix queries]] — the general framework of querying language-based patterns in dynamic words
- [[Regular language pattern matching]] — the foundational pattern-matching problem
- [[Document spanners]] — information extraction model that motivates infix-based queries
- [[Monadic second-order logic (MSO)]] — theoretical framework generalizing infix queries to broader logical predicates

## Sources

- Bourhis, Florent, Florent Capelli, Stefan Mengel, and Cristian Riveros. "Dynamic direct access of MSO query evaluation over strings." *