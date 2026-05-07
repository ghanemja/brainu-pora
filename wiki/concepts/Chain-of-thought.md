# Chain-of-thought

## Definition

**Chain-of-thought (CoT)** is a reasoning technique that externalizes intermediate computational steps as text or structured artifacts, making reasoning processes explicit, verifiable, and composable. Rather than computing a final answer directly, a system generates a sequence of intermediate reasoning steps, each building on previous results.

In the context of transformer-based agents, chain-of-thought extends beyond simple prompting to include:
- **Externalized reasoning traces**: intermediate results written to persistent storage
- **Multi-step inference**: multiple forward passes through a language model, conditioned on accumulated context
- **Tool integration**: interleaving symbolic operations (retrieval, arithmetic, code execution) with language model inference

The key insight is that externalization decouples **reasoning capacity** (what can be thought) from **inference capacity** (what fits in a single forward pass), enabling agents to reason over problems vastly larger than their context window.

## Key Equations

The Library Theorem formalizes the cost of reasoning under different retrieval strategies:

### Sequential Retrieval (no indexing)
For an agent with context window size $W$ querying a memory store of size $N$:

$$\text{Cost per query} = \Omega(N) \text{ page reads}$$

$$\text{Cumulative cost over } T \text{ steps} = \Theta(T^2)$$

This arises because sequential scanning requires reading through all stored items until the target is found, with expected cost $N/2$ in the worst case.

### Indexed Retrieval (external indexing)
With a structured index of branching factor $b$ (e.g., $b=10$ for decimal search):

$$\text{Cost per query} = O(\log_b N) \text{ page reads}$$

$$\text{Cumulative cost over } T \text{ steps} = O(T \log_b T)$$

This dramatic reduction—from quadratic to nearly-linear cumulative cost—arises because each index lookup eliminates $b-1$ of $b$ branches, achieving exponential pruning of the search space.

### Context Window as I/O Page
The transformer context window functions as a read/write page of fixed size $W$:
$$\text{Page capacity} = W \text{ tokens (typically 100K–1M)}$$
$$\text{Effective items per page} = W / \text{(tokens per item)}$$

Each tool call or external memory access incurs a "page read" cost proportional to the tokens required to transmit the retrieved data into the next inference call.

## Physical Intuition / Derivation

### Why Externalization Helps

A language model's forward pass has fixed computational capacity: it can attend to at most $W$ tokens simultaneously. For problems requiring reasoning over $N > W$ total facts, a single pass is insufficient.

**Externalization breaks the problem recursively**:
1. Maintain a persistent **external reasoning state** (file system, vector store, structured memory)
2. Each inference step: read relevant subset of state ($O(W)$ tokens), compute updates, write results back
3. Next step: condition on accumulated trace, read new relevant subset
4. Continue until goal is reached

This is analogous to a human working through a complex proof on paper: the paper is the external memory, individual glances capture one "page," and writing down intermediate results allows composition of many small cognitive steps into large reasoning processes.

### The Index Advantage

Without indexing, finding a relevant fact requires **linear scan**: read item 1, read item 2, ... until found. Expected cost is $N/2$ items, or $\Theta(N)$ page reads.

With indexing (e.g., binary search tree, hash table), the agent:
- Compares target against an index node (O(W) tokens for index description)
- Eliminates a large fraction of possibilities ($b-1$ out of $b$ branches)
- Repeats recursively: $\log_b N$ iterations

**Concrete example**: Searching an encyclopedia of 10,000 entries
- Linear scan: average 5,000 reads; worst case 10,000 reads
- Indexed search ($b=10$): $\log_{10} 10,000 = 4$ reads

### The Parametric Memory Interference Problem

A critical finding: when content is semantically familiar (e.g., real encyclopedia entries), the language model's parametric memory (weights learned during pretraining) interferes with protocol adherence. The model "recognizes" the domain and generates answers directly, bypassing the index entirely.

This creates a **dissociation**:
- **Index construction**: LLMs excel (semantic understanding needed to map content to index structure)
- **Index traversal**: LLMs fail at scale (understanding tempts shortcutting the protocol)

**Solution**: Separate concerns—use LLMs for semantic tasks, deterministic algorithms for navigational logic.

## Applications in Engineering

### 1. Large-Scale Autonomous Agents
Deploy AI agents on problems exceeding context window size (e.g., code repositories with 1M+ LOC):
- Agent uses indexed search to locate relevant modules
- Reads one module at a time into context
- Generates edits, caches results, proceeds to next module
- **Benefit**: Enables complex refactoring without rewriting entire codebase in each step

### 2. Retrieval-Augmented Generation (RAG) Systems
Search over distributed knowledge before generation:
- Index documents by semantic embeddings or explicit metadata
- Query returns $k$ most relevant passages (logarithmic retrieval)
- Condition LLM generation on retrieved context
- **Benefit**: Reduces hallucination; grounds outputs in external facts

### 3. Automated Theorem Proving & Mathematical Reasoning
Structured chains over lemmas and proof steps:
- Maintain proof state (goals, hypotheses, proved lemmas) externally
- Index lemma library by tactic applicability
- Each step: retrieve relevant lemmas, attempt proof step, update state
- **Benefit**: Scales verification to large formal mathematics (e.g., Lean proofs)

### 4. Debugging & Root Cause Analysis
Hierarchical tracing through distributed system logs:
- Index logs by timestamp, service, error code, and causal dependencies
- Agent traces chain of causality: event A caused event B caused event C
- Indexed retrieval avoids re-scanning all $N$ log entries at each step
- **Benefit**: Mean time to resolution (MTTR) decreases from $