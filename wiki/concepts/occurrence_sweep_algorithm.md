# Occurrence Sweep Algorithm

## Definition

The **occurrence sweep algorithm** is a computational technique for efficiently enumerating and tracking occurrences of symbols within a string or sequence during dynamic query processing. It systematically traverses a word $w$ while maintaining bounded lists of recent symbol occurrences, enabling constant-time or near-constant-time access to contextual position information.

More formally, for a word $w$ over alphabet $\Sigma$ and a parameter $p$ (bounded threshold), the algorithm maintains:
- **Left Information (LI)**: The last $p$ occurrences of each symbol $a \in \Sigma$ to the left of the current position
- **Right Information (RI)**: The first $p$ occurrences of each symbol $a \in \Sigma$ to the right of the current position

These lists are maintained and updated as the sweep progresses, allowing queries about symbol distributions to be answered in constant or polylogarithmic time.

## Key Equations

The core sweep operates on intervals $w[l, r]$ where occurrences are tracked:

$$\text{LI}_{r_{l-1}}(a) := \{\text{last } p \text{ positions of } a \text{ left of } r_{l-1}\}$$

$$\text{RI}_{r_{l-1}}(a) := \{\text{first } p \text{ positions of } a \text{ right of } r_{l-1}\}$$

For a position $r$ where symbol $a$ transitions from rare to frequent:

$$r = \min\{j > l : |w[l, j] \cap a| > p\}$$

The concatenation and truncation operation used to merge occurrence lists:

$$\text{Concat-Trunc}(\text{LI}, \text{RI}) = \text{last } p(\text{LI} \cup \text{RI})$$

## Physical Intuition / Derivation

### Problem Motivation

When processing dynamic strings or streaming data, we often need to answer queries about *infixes* (substrings) with specific properties—for instance, "find all substrings starting and ending with symbol $a$." Naive enumeration would require examining all $O(n^2)$ possible substrings, which becomes prohibitively expensive.

### Core Insight

The key observation is that we can focus our attention on **critical positions** where the frequency of a symbol transitions between "rare" (appears ≤ $p$ times) and "frequent" (appears > $p$ times). Between these critical positions, the structure of occurrences changes in predictable ways.

### Sweep Mechanics

1. **Background Traversal**: The algorithm performs a "max-left background traversal"—a preprocessing pass that scans the word leftward, accumulating occurrence positions until we've seen sufficiently many instances of each symbol.

2. **Bounded Storage**: Rather than storing all occurrences (which could be $O(n)$ per symbol), we maintain only the last $p$ occurrences and first $p$ occurrences. This keeps memory usage to $O(|\Sigma| \cdot p)$.

3. **List Concatenation**: When transitioning between intervals, occurrence lists are merged by taking the union of left-occurrences and right-occurrences, then truncating to the last $p$ items. This preserves all relevant positional information while discarding older occurrences that won't affect future queries in the bounded region.

4. **Amortized Constant Time**: Although each individual operation might take $O(p)$ or $O(\log n)$ time, the amortized cost per position swept is constant because:
   - We process each occurrence at most twice (once in background traversal, once in main sweep)
   - List updates are bounded by $p$
   - Total work is $O(n + p \cdot |\Sigma|)$ spread over $n$ positions

## Applications in Engineering

### 1. **String Pattern Matching & Text Processing**
- Efficient infix enumeration for regular language membership testing
- Solving dynamic regex matching and substring queries without materializing all matches
- Streaming text analysis where memory is constrained

### 2. **Database Query Optimization**
- Pattern enumeration in document collections with bounded result sets
- Tractability classification of languages for query planning (ZG vs. non-ZG languages)
- Determining whether a pattern can be answered tractably vs. requiring exponential resources

### 3. **Bioinformatics**
- Finding all genomic regions where certain motifs appear (bounded occurrences)
- Efficient substring enumeration in DNA/protein sequences with bounded frequency constraints
- Tracking conservation patterns across genomic intervals

### 4. **Compiler Design & Formal Languages**
- Recognition and enumeration of language infixes for context-free parsing with bounded lookahead
- Determining if a formal language admits tractable dynamic membership testing
- Optimizing automata-based matching in lexical analysis

### 5. **Stream Processing & Online Algorithms**
- Processing unbounded data streams with fixed memory footprint
- Maintaining summary statistics of symbol occurrences in sliding windows
- Real-time monitoring of pattern frequencies in log streams or sensor data

## Common Mistakes / Pitfalls

### 1. **Confusing Rare vs. Frequent Thresholds**
Students often misunderstand the relationship between the parameter $p$ and the algorithm's behavior. The threshold $p$ is not arbitrary—it determines both the memory requirement ($O(p \cdot |\Sigma|)$) and which pattern languages become tractable. Setting $p$ too small loses information; too large wastes memory.

### 2. **Assuming All Occurrences Are Tracked**
A critical insight that's easy to miss: the algorithm does *not* track all symbol occurrences globally. It only maintains the last/first $p$ occurrences *relative to the current position*. Beyond those $p$ boundary occurrences, all earlier/later occurrences are discarded. This is intentional and enables the constant-time bounds.

### 3. **Forgetting the Amortized Analysis**
The algorithm achieves $O(1)$ amortized time per position, not worst-case $O(1)$ per operation. Individual occurrence list updates can take $O(p)$ time. Understanding amortized analysis is essential to see why this is still efficient across the full sweep.

### 4. **Misapplying to Unbounded Contexts**
The algorithm works well for tract