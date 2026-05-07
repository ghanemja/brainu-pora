# Occurrence List

## Definition

An **occurrence list** $\Lambda_a$ is a data structure that maintains an ordered record of all positions (indices) in a text string $w$ where a particular symbol or character $a$ appears. Formally, for a character $a \in \Sigma$ (alphabet) and a word $w = w[1..n]$:

$$\Lambda_a = \{i \in [1,n] : w[i] = a\}$$

The occurrence list is typically stored as a sequence of indices in the order they appear in the text, allowing efficient traversal and enumeration of all positions where $a$ occurs.

### Rare vs. Frequent Letters

In algorithmic contexts (particularly pattern matching and text analysis), a letter $a$ is classified as:
- **Rare** in $[1,r]$: the number of occurrences $|\Lambda_a \cap [1,r]| \leq p$ (below a threshold $p$)
- **Frequent** in $[1,r]$: the number of occurrences $|\Lambda_a \cap [1,r]| > p$

This classification enables adaptive algorithms that handle high and low-frequency symbols differently.

## Key Equations

**Occurrence count in interval $[L,R]$:**
$$\text{count}_a(L,R) = |\{i \in \Lambda_a : L \leq i \leq R\}|$$

**Unprocessed occurrences when $a$ becomes rare:**
$$|\text{remaining occurrences}| \leq p$$

This bound ensures that once a letter transitions to "rare," the remaining occurrences can be processed in constant time (proportional to $p$, a fixed parameter).

## Physical Intuition / Derivation

### Why Occurrence Lists?

When processing a text from right to left (as in the example with endpoint $r$ sweeping), a naive algorithm would recompute positions of characters repeatedly. An occurrence list pre-computes this information:

1. **Preprocessing phase**: Scan the input word $w$ once, collecting all indices for each character into $\Lambda_a$.
2. **Query phase**: Instead of searching for character occurrences, directly iterate through pre-stored indices.

### Min Background Traversal

The **min background traversal** is a lazy evaluation technique paired with occurrence lists:

- As the right endpoint $r$ moves leftward through the text, a parallel traversal pointer advances through $\Lambda_a$ at each step.
- This ensures that by the time letter $a$ becomes rare (fewer than $p$ remaining occurrences), the traversal has already visited most of $\Lambda_a$.
- The remaining $\leq p$ unvisited occurrences can be processed in $O(p)$ time (constant in algorithms where $p$ is a fixed parameter).

**Key insight from Claim 6.4**: When $a$ becomes rare at position $r$, the traversal has swept over all but at most $p$ occurrences of $a$, enabling constant-time completion of the traversal.

## Applications in Engineering

### 1. **String Pattern Matching & Text Search**
Occurrence lists accelerate queries like "find all positions of substring $ab$ in text $w$" by precomputing character locations, avoiding repeated linear scans.

### 2. **Formal Language Recognition**
In parsing and automata-based language recognition (e.g., the $L_{ab}$ language in Example D.2), occurrence lists enable efficient enumeration of valid infix positions without redundant text rescans.

### 3. **Sequence Analysis in Bioinformatics**
DNA/protein sequence analysis uses occurrence lists to quickly identify all positions of motifs (e.g., restriction enzyme sites) without rescanifying the entire genome.

### 4. **Database Indexing & Information Retrieval**
Inverted indices (a variant of occurrence lists) map terms to document positions, forming the backbone of full-text search engines and database indexes.

### 5. **Compiler Lexical Analysis**
Symbol tables and occurrence tracking in compiler front-ends use similar structures to map identifiers to all their definition and use sites.

## Common Mistakes / Pitfalls

### 1. **Confusing Occurrence List with Index**
Students sometimes treat $\Lambda_a$ as a single position rather than a *set/list* of all positions. The occurrence list is a collection, not a scalar.

### 2. **Ignoring the Lazy Evaluation Cost**
Assuming the min background traversal is free. In reality:
- Building $\Lambda_a$ requires $O(|w|)$ time initially.
- Completing a partially-traversed list still requires $O(p)$ time for unprocessed occurrences.

The cost is *amortized* constant, not worst-case constant.

### 3. **Misapplying the "Rare Letter" Threshold**
The parameter $p$ must be chosen carefully. Setting $p$ too small increases false rare classifications; setting it too large defeats the algorithmic advantage (frequent letters should be handled by different logic).

### 4. **Not Accounting for Space**
Storing $\Lambda_a$ for all $a \in \Sigma$ requires $O(|w| \cdot |\Sigma|)$ space. In large alphabets, this can dominate memory usage.

### 5. **Off-by-One Errors in Interval Queries**
When computing occurrences in $[L,R]$, ensure boundary conditions are correct:
- Is the interval inclusive or exclusive at endpoints?
- Are indices 0-based or 1-based?

## See Also

- [[Min Background Traversal]] – Lazy evaluation strategy paired with occurrence lists
- [[Inverted Index]] – Database/IR variant; maps terms to document positions
- [[Text Pattern Matching]] – Core application of occurrence lists
- [[Formal Language Recognition]] – Use in automata-based string processing
- [[Symbol Table]] – Compiler application storing identifier occurrences

## Sources

- Amarilli, A., Dziadek, S., & Segoufin, L. – Lecture/paper excerpt on min background traversal and occurrence lists (Sections D.2–D.4)
- Example D.2: Illustration of min background traversal on language $L_{ab}$ with occurrence lists $\Lambda_a$ and $\Lambda_b$
- Claim 6.4: Proof that occurrence list processing can be