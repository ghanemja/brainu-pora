# state tree compression

## Definition

**State tree compression** is an algorithmic technique for efficiently representing and enumerating all solutions to a combinatorial problem by constructing a compact tree representation where redundant (non-branching) states are merged together.

In the specific context of Eulerian trail enumeration, a state tree initially encodes all possible ways to complete a partial Eulerian trail (prefix) into a full trail. Compression removes intermediate states that have exactly one child, since such states do not represent meaningful decision points—they can only be extended in one unique way.

The compressed state tree maintains the property that:
- Every non-compressed node has **at least 2 child states** (branching nodes), OR
- There are **at most O(1) consecutive non-branching states** between branching nodes

This ensures the overall tree size remains linear in the problem structure rather than exponential.

## Key Equations

**Uncompressed state tree complexity:**
$$\text{Size} = O(m \cdot z_T)$$

where $m$ is the number of edges and $z_T$ is the total number of Eulerian trails.

**Compressed state tree complexity:**
$$\text{Size} = O(m + z_T)$$

The compression achieves linear dependence on both the problem size ($m$) and the number of solutions ($z_T$), preventing exponential blowup from non-branching intermediate states.

**Branching condition:** A state $s$ is branching if and only if the prefix it represents can be completed to **at least 2 distinct** Eulerian trails:
$$|E(s)| \geq 2$$

where $E(s)$ denotes the set of all possible Eulerian trails extending prefix $s$.

## Physical Intuition / Derivation

### Why Compression is Necessary

Imagine enumerating all valid paths through a graph by building a decision tree:
- At each internal state (partial path), we decide which edge to follow next
- If a state has only **one valid next edge**, it forces no choice—this state is "information-poor"
- Uncompressed, such states waste space and time

**Example:** Consider a linear sequence of forced edges: $A \to B \to C \to D$. In the uncompressed tree, this creates nodes $A, B, C, D$ as a path. In the compressed tree, we collapse this into a **single edge** labeled with the sequence $A \to B \to C \to D$.

### Two Compression Rules

**Rule 1: Single Out-Degree Contraction**

If node $v$ has exactly one outgoing edge to neighbor $w$:
- Every Eulerian trail must traverse this edge immediately upon reaching $v$
- Therefore, $v$ and $w$ can be **merged into a single compressed node** without loss of information about trail count
- This applies globally and is simple to implement

**Rule 2: SCC-Aware Contraction** (weaker, more technical variant)

For directed graphs with strongly connected components (SCCs):
- If node $v$ has exactly one edge leaving its SCC and exactly one edge staying within its SCC
- The edge within the SCC must be traversed first on all trails
- This edge can be contracted with its target

The weaker variant is necessary because exhaustively applying the stronger rule after every transition has fine-grained complexity barriers.

### Resulting Tree Structure

After compression:
1. **Branching nodes**: Multiple children (correspond to genuine choice points)
2. **Compressed edges**: May represent sequences of forced transitions
3. **Size bound**: With $O(1)$ non-branching consecutive states allowed, the tree height remains logarithmic-ish and overall size becomes $O(m + z_T)$

This is optimal: you cannot enumerate $z_T$ solutions faster than $O(z_T)$, and you need $O(m)$ just to represent the input graph.

## Applications in Engineering

### 1. **Circuit Design & Verification**
- **Eulerian path problems** arise in VLSI routing (finding single-pass connections through all nets)
- State tree compression accelerates enumeration of all valid routing solutions
- Reduces memory footprint when exploring layout alternatives

### 2. **Network Protocol Analysis**
- Enumerating all possible execution traces through concurrent protocols
- State compression prevents combinatorial explosion when analyzing message orderings
- Critical for formal verification of distributed systems

### 3. **Compiler Optimization & Code Generation**
- **Instruction scheduling**: enumerate all valid orderings of instructions respecting dependencies
- State compression avoids redundant exploration of forced instruction sequences
- Enables efficient generation of all Pareto-optimal schedules

### 4. **Supply Chain & Logistics**
- **Hamiltonian/Eulerian path problems** in vehicle routing and scheduling
- Compress state trees when enumerating delivery routes with constraints
- Reduces search space for multi-objective optimization (cost, time, distance)

### 5. **Bioinformatics**
- **DNA sequence assembly**: reconstruct genomes from overlapping fragments (de Bruijn graphs)
- Eulerian paths solve the overlap problem; compression speeds enumeration of alternative assemblies
- Important for ambiguous regions with multiple valid reconstructions

## Common Mistakes / Pitfalls

### 1. **Confusing Compression with Elimination**
❌ **Mistake:** Removing non-branching states entirely from the tree.  
✓ **Correct:** Compress them by merging them into edges; the information is still encoded, just more compactly.

### 2. **Forgetting to Track Edge Labels During Compression**
❌ **Mistake:** When contracting nodes, losing the actual edges/transitions represented.  
✓ **Correct:** Compressed edges must store the sequence of operations they represent so decompression yields full solutions.

### 3. **Over-applying Compression Rules**
❌ **Mistake:** Trying to apply Rule 2 (SCC-aware) exhaustively after every transition without concern for computational cost.  
✓ **Correct:** Use the weaker technical variant that maintains $O(1)$ amortized cost; fine-grained complexity barriers exist for stronger rules.

### 4. **Not Validating the O(1) Consecutive Non-Branching Bound**
❌ **Mistake:** Assuming all non-branching states are removed; they may still appear in clusters.  
✓ **Correct:** The guarantee is that consecutive non-branching states are