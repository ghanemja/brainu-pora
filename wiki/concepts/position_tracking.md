# Position Tracking

## Definition

Position tracking is a computational technique for maintaining and efficiently accessing occurrence locations of symbols or patterns within a string or sequence. In the context of infix enumeration and dynamic string analysis, position tracking involves:

1. **Maintaining occurrence lists**: Ordered collections of all positions where each symbol $a \in \Sigma$ appears in a string $w$
2. **Interval tracking**: Identifying the last $\leq p$ occurrences of a symbol within a specific range $w[l, r]$
3. **Boundary management**: Efficiently determining when a symbol transitions from "rare" (appearing infrequently) to "frequent" (appearing regularly) within a substring

Formally, for a symbol $a$ and substring $w[l, r]$, we track the minimal position $r$ where $a$ becomes frequent, defined as:

$$r = \min\{r' : |w[l, r'] \cap \{a\}| > p\}$$

where $p$ is a threshold parameter, and $r = |w| + 1$ if $a$ remains rare throughout $w[l, |w|]$.

## Key Equations

**Occurrence List Concatenation:**
Given left interval information (LI) and right interval information (RI) at boundary position $r_{l-1}$:
- LI at $r_{l-1}$: yields the $\leq p$ last occurrences of $a$ left of $r_{l-1}$ and right of $r_{l}$
- RI at $r_{l-1}$: yields the $\leq p$ first occurrences of $a$ right of $r_{l-1}$

Concatenating and truncating these lists gives:
$$\text{Occurrences}(a, w[l, r_{l-1}]) = \text{LI}(a, r_{l-1}) \oplus \text{RI}(a, r_{l-1})$$

where $\oplus$ denotes concatenation with subsequent truncation to length $p$.

**Interval Sweep Coverage:**
The number of untracked occurrences after a background traversal is bounded:
$$|\text{Untracked}(a)| \leq p$$

## Physical Intuition / Derivation

Position tracking addresses the practical challenge of *incremental pattern access* in dynamic strings. Consider enumerating all infixes matching pattern $aΣ^*a$ (substrings beginning and ending with $a$):

1. **Naive approach**: Examine all $O(n^2)$ possible substrings—prohibitively expensive.

2. **Smart approach**: 
   - Maintain a sorted list of all positions where $a$ occurs
   - For each pair of positions $(i, j)$ with $i < j$ where $a$ appears, the substring $w[i, j]$ is a valid infix
   - Only $O(|{a}|^2)$ pairs exist, where $|{a}|$ is the frequency of $a$

3. **Tracking mechanism**: Rather than recomputing occurrence lists from scratch, we:
   - Perform a single **max-left background traversal** (scan from left), extracting the final $\leq p$ occurrences in constant time
   - Use **LI/RI (left/right interval) information** at boundary positions to avoid re-scanning previously processed regions
   - Truncate concatenated lists to bounded size, guaranteeing that at most $p$ occurrences are ever "loose" or untracked

This creates a **lazy evaluation** framework where expensive global computations are amortized across infix enumerations.

## Applications in Engineering

### 1. **String Matching & Pattern Recognition**
- **DNA sequence analysis**: Track positions of motifs in genomic sequences to identify coding regions
- **Network protocol parsing**: Maintain occurrence lists of delimiters in packet payloads for efficient message boundary detection

### 2. **Compiler Design**
- **Lexical analysis**: Track position of keyword occurrences to generate symbol tables with $O(\log n)$ amortized overhead per token
- **Error recovery**: Position tracking enables pinpoint reporting of syntax errors in source code

### 3. **Database Indexing**
- **Inverted indexes**: Maintain position lists for terms to support phrase queries and proximity searches
- **Dynamic updates**: Incrementally update occurrence lists when documents are inserted/deleted

### 4. **Stream Processing**
- **Event log analysis**: Track positions of critical events in high-volume log streams
- **Sliding window statistics**: Efficiently compute pattern frequencies over time-bounded windows

### 5. **Natural Language Processing**
- **Concordance generation**: Rapidly locate and enumerate all contexts where a word appears
- **N-gram extraction**: Track positions to generate occurrence-based n-gram statistics for language models

## Common Mistakes / Pitfalls

### 1. **Forgetting Boundary Conditions**
**Mistake**: Assuming $r = |w| + 1$ only when $a$ never appears.
**Correction**: Set $r = |w| + 1$ when $a$ is *initially rare* in $w[l, |w|]$—it may still have occasional occurrences.

### 2. **Confusing "Last $p$ Occurrences" with "All Occurrences"**
**Mistake**: Assuming truncated occurrence lists are complete.
**Correction**: The bound $|\text{Untracked}| \leq p$ is intentional—beyond $p$ occurrences, older positions are intentionally discarded to maintain constant-time operations.

### 3. **Not Accounting for Concatenation Overhead**
**Mistake**: Assuming LI $\oplus$ RI concatenation is free.
**Correction**: While the lists are bounded to size $p$, the merge operation is $O(p)$; amortized analysis distributes this cost across infix enumerations.

### 4. **Position Indices vs. Symbol Values**
**Mistake**: Treating position lists as sets of symbols rather than positions.
**Correction**: A position tracking list stores indices $\{i : w[i] = a\}$, not copies of $a$ itself. Order and index relationships are paramount.

### 5. **Premature Termination of Background Traversal**
**Mistake**: Stopping a max-left traversal as soon as $