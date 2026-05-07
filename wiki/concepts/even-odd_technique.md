# even-odd technique

## Definition

The **even-odd technique** is an algorithmic strategy for maintaining constant-delay enumeration in problems involving backtracking and state restoration. It works by partitioning enumeration steps into two phases based on parity:

- **Even phase**: Process outputs corresponding to even-indexed positions/parameters while in a "decreasing" or "destructive" state modification mode
- **Odd phase**: Process outputs corresponding to odd-indexed positions/parameters while in an "increasing" or "reconstructive" state restoration mode

The technique ensures that after completing one full cycle (both phases), the underlying data structure returns to its initial state, allowing subsequent cycles to proceed without additional restoration overhead.

## Key Equations

For enumeration with a parameter $r$ ranging over interval $[1, |w|]$ with an updatable state $\Psi$:

**Enumeration schedule:**
$$\text{Outputs for even } r \text{ during } |w| \to 1 \text{ (decreasing phase)}$$
$$\text{Outputs for odd } r \text{ during } 1 \to |w| \text{ (increasing phase)}$$

**State complexity:**
- Standard enumeration: $O(k)$ state restoration cost for $k$ outputs
- Even-odd technique: $O(1)$ amortized cost per output (constant delay)

**Precondition for correctness:**
The sequence of update operations must form a reversible pair: each destructive operation (removal) during the decreasing phase has a corresponding constructive inverse (reinsertion) during the increasing phase.

## Physical Intuition / Derivation

### Motivation: The Backtracking Problem

Consider enumerating all valid configurations by iteratively modifying a parameter (e.g., right endpoint $r$ in a string). A naive approach:

1. Decrease $r$ and generate outputs
2. When done, restore state by undoing all changes
3. Cost: $O(k)$ restoration work for $k$ modifications

### The Even-Odd Insight

Instead of restoring all at once, **interleave restoration with generation**:

**First pass (decreasing):** 
- Modify state destructively: $w \to w[1:|w|-1] \to \cdots \to w[1:1]$
- Emit outputs only when condition holds AND index is even
- State becomes progressively "simplified"

**Second pass (increasing):**
- Restore state constructively: $w[1:1] \to \cdots \to w[1:|w|]$
- Emit outputs only when index is odd
- State returns to original configuration while generating

**Key observation:** The cost of restoring state is "paid for" by the computational work already done during generation. Each restoration step can be merged with the next generation step, achieving **amortized constant time per output**.

### Example: Enumeration of Infixes in Regular Language

For a word $w$ and language $L$, enumerate all $L$-infixes (substrings in $L$):

```
For left endpoint l = 1, 2, ..., |w|:
  Starting with full word w:
    -- DECREASING PHASE (r: |w| → 1) --
    For r = |w|, |w|-1, ..., 1:
      If r is even AND w[l:r] ∈ L:
        OUTPUT w[l:r]
      Remove w[r] from state
    
    -- INCREASING PHASE (r: 1 → |w|) --
    For r = 1, 2, ..., |w|:
      Add w[r] back to state
      If r is odd AND w[l:r] ∈ L:
        OUTPUT w[l:r]
```

After both phases, the state is restored for the next value of $l$.

## Applications in Engineering

### 1. **Database Query Enumeration**
Enumerating results from complex queries with backtracking constraints. The even-odd technique allows constant-delay enumeration without materializing intermediate results.

### 2. **Compiler Optimization**
Pattern matching and code generation phases in compilers that must enumerate valid transformations while maintaining intermediate states.

### 3. **Regular Language Processing**
As shown in the source material: enumerating infixes, substrings, or other linguistic features of words while verifying membership in a finite automaton with dynamic updates.

### 4. **Graph Enumeration Algorithms**
Enumerating paths, cycles, or subgraphs where each enumeration step requires edge/node removal and restoration, particularly in constant-memory or constant-delay contexts.

### 5. **Combinatorial Search**
Backtracking algorithms in constraint satisfaction problems (CSP) where enumeration solutions must maintain an updatable constraint store.

## Common Mistakes / Pitfalls

1. **Forgetting the symmetry requirement**: The even-odd split only works if the "destruction" phase (decreasing $r$) can be perfectly reversed by the "construction" phase (increasing $r$). Asymmetric operations break the technique.

2. **Confusing parity with phases**: Students often assume *all* even-indexed outputs go in phase 1 and *all* odd-indexed in phase 2, rather than understanding that parity determines *when* (in which phase) an output can be produced.

3. **Misapplying to non-reversible updates**: The technique requires that updates are reversible (e.g., deletion followed by reinsertion). Irreversible modifications (lossy compression, destructive sorting) cannot use this technique.

4. **Overhead from state complexity**: While constant-delay is achieved, the hidden constant depends on state restoration time. If updates are $O(n)$ each, amortized cost per output is still $O(n)$, not truly constant.

5. **Initialization/finalization errors**: Failing to ensure the state is properly initialized before the decreasing phase or that it reaches the correct final state after the increasing phase invalidates the entire enumeration.

## See Also

- [[Constant-delay enumeration]] — The broader algorithmic paradigm that even-odd technique enables
- [[Backtracking algorithms]] — The broader class of problems where even-odd is applicable
- [[Dynamic data structures]] — The supporting infrastructure needed to perform efficient reversible updates
- [[Regular language recognition]] — The specific application domain in the source material
- [[Amortized analysis]] — The theoretical framework for analyzing constant-delay amortization

##