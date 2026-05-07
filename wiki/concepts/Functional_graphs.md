# Functional graphs

## Definition

A **functional graph** is a directed graph in which every node has exactly one outgoing edge. Formally, a functional graph $G = (V, E)$ satisfies:

$$\forall v \in V: |\{u \in V : (v, u) \in E\}| = 1$$

This unique outgoing edge structure creates a highly constrained topology where the graph structure is determined by a function $f: V \to V$, with edge $(v, f(v))$ for each node $v$.

**Key structural property:** Every connected component of a functional graph consists of:
- A single directed cycle (the "core")
- Trees hanging off the cycle, with edges directed toward the cycle

This is sometimes called a **1-in-tree** or **successor graph** in the literature.

## Key Equations

### Cycle Detection via Closed Walks

For a node $v$ on a cycle of length $c$, a closed walk of length $l$ exists if and only if:
$$c \mid l$$

where "$\mid$" denotes divisibility. The indicator function is:

$$\text{Cycl}_l(v) = \begin{cases} 1 & \text{if node } v \text{ lies on a cycle whose length divides } l \\ 0 & \text{otherwise} \end{cases}$$

### Unique Walk Property

Because each node has outdegree exactly 1, there is a unique walk (sequence of edges) of any length $l$ starting from node $v$:

$$\text{Walk}_l(v) \text{ is unique for all } l \geq 0$$

The endpoint of this walk is deterministic: $w = f^{(l)}(v)$, where $f^{(l)}$ denotes $l$-fold functional composition.

## Physical Intuition / Derivation

### Why Functional Graphs Matter

The constraint that each node has exactly one outgoing edge dramatically simplifies graph structure compared to general directed graphs. This makes them ideal for:

1. **Deterministic state machines**: Each state has exactly one successor state
2. **Iterative processes**: Apply a function repeatedly; the sequence is deterministic
3. **Cycle detection in sequences**: If you iterate a function long enough, you must enter a cycle

### Understanding the Cycle-Walk Relationship

Consider iterating a function $f$ starting from node $v$: the sequence is
$$v, f(v), f^{(2)}(v), f^{(3)}(v), \ldots$$

Since the graph is finite and each node has one outgoing edge:
- Eventually you must revisit a node
- Once you revisit a node, you enter a cycle and stay in it forever
- The cycle length $c$ divides all subsequent walk lengths from that node

**Example:** If a node lies on a 2-cycle (like nodes in $C_{2l}$):
- A walk of length 4 returns you to where you started (closes the walk)
- A walk of length 5 does not ($2 \nmid 5$)
- A walk of length $2k$ always closes

This is *why* functional graphs reduce cycle detection to a walk-closure problem: closed walks are entirely determined by divisibility.

### Message Passing Insight

The source material shows that **forward-only** message passing suffices for functional graphs, unlike general directed graphs. Why?

In a functional graph, starting from node $v$ and following the unique outgoing edge, you traverse along the graph structure until reaching a cycle. The closure of the walk—returning to $v$ after $l$ steps—forms a loop in the graph itself. This loop provides a "natural" forward path back to $v$, eliminating the need for explicit reverse edges in the message-passing architecture.

## Applications in Engineering

### 1. **Pseudorandom Number Generators**
Functional iteration is fundamental to PRNG design. The generator is a function $f$, and the seed determines the starting node. Cycle length (detected via functional graph analysis) determines period.

### 2. **Hash Table Collision Analysis**
In hash functions with chaining, if collisions form a functional graph structure, the expected cycle length determines performance degradation. Understanding functional graph properties helps predict collision clustering.

### 3. **State Machine Verification**
Embedded systems and control logic often use state machines where each state has one default successor. Analyzing the functional graph structure identifies:
- Reachable states from an initial state
- Unreachable deadlock states
- Whether termination states are reachable

### 4. **Distributed Consensus and Gossip Algorithms**
Functional graphs model synchronous update rules where each node's next state depends deterministically on current states. Cycle detection predicts oscillation vs. convergence behavior.

### 5. **Rho-Algorithm for Discrete Logarithm**
Pollard's rho algorithm exploits functional graph structure to find cycles in pseudorandom sequences, enabling efficient solving of the discrete log problem in cryptography.

### 6. **Graph Neural Network Expressivity**
The source material's application to MPNNs (Message-Passing Neural Networks) shows functional graphs as a test case for GNN expressiveness—the simplified structure reveals exactly what architectural components are *necessary* to detect patterns (cycle participation).

## Common Mistakes / Pitfalls

### Mistake 1: Confusing Closed Walks with Simple Cycles

**Wrong:** "If a closed walk of length $l$ exists from node $v$, then $v$ lies on a simple $l$-cycle."

**Right:** In general directed graphs, a closed walk can traverse the same cycle multiple times. For example, on a 3-cycle, a closed walk of length 6 traverses the cycle twice.

**Key insight:** On functional graphs specifically, these notions coincide (as noted in Remark 15) because unique outdegrees prevent "shortcuts" and multiple-edge sequences. On general graphs, you need additional constraints to rule out repeated cycles.

### Mistake 2: Assuming All Nodes Can Reach All Other Nodes

**Wrong:** "In a functional graph with $n$ nodes, any node can reach any other."

**Right:** Nodes not on cycles can only reach nodes downstream in their tail. The graph decomposes into components, each with one cycle and trees feeding into it.

### Mistake 3: Forgetting the "Exactly One" Outdegree Requirement

**Wrong:** Treating a graph as functional when some nodes have outdegree 