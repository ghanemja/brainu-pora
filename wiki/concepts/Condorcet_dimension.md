# Condorcet Dimension

## Definition

The **Condorcet dimension** is the minimum cardinality of a set of matchings (or more generally, feasible allocations) such that this set constitutes a **Condorcet-winning set**—meaning that for every alternative matching outside the set, a strict majority of agents prefers their favorite matching within the set over that competitor.

Formally, given a set of agents with preferences over objects, a set $\mathcal{M}$ of matchings is **Condorcet-winning** if:

$$\forall \text{ matching } M \notin \mathcal{M}, \quad |\{i : M_i^* \succ_i M\}| > \frac{n}{2}$$

where $M_i^*$ is agent $i$'s favorite matching in $\mathcal{M}$, and $\succ_i$ denotes agent $i$'s preference relation.

The **Condorcet dimension** $\text{CD}(\mathcal{I})$ is defined as:

$$\text{CD}(\mathcal{I}) = \min \{|\mathcal{M}| : \mathcal{M} \text{ is a Condorcet-winning set}\}$$

### Special Case: Condorcet Winners

A single matching $M$ is a **Condorcet winner** (or **popular matching**) if it is preferred by a strict majority to every alternative matching. This corresponds to Condorcet dimension 1, but such winners need not exist.

## Key Equations

### Majority Preference Condition
For a set $\mathcal{M}$ to be Condorcet-winning:

$$\forall M \notin \mathcal{M}: \quad \left|\left\{i \in N : \exists M' \in \mathcal{M}, M' \succ_i M\right\}\right| > \frac{|N|}{2}$$

### Connection to Pareto Optimality
A key theoretical result: **any Pareto-optimal set of two matchings is a Condorcet-winning set** (under weak orders).

A matching $M$ is **Pareto-optimal** if there does not exist another matching $M'$ such that $M' \succeq_i M$ for all agents $i$, with strict preference for at least one agent.

## Physical Intuition / Derivation

### The Problem Setting

Imagine assigning housing, jobs, or resources to a group of agents. The challenge: no single assignment may satisfy a majority—preferences may be fragmented or cyclic.

**Example of nonexistence:**
- 3 agents, 3 items
- Agent 1: prefers $M_A \succ M_B \succ M_C$
- Agent 2: prefers $M_B \succ M_C \succ M_A$
- Agent 3: prefers $M_C \succ M_A \succ M_B$

Any single matching loses a majority vote to some other matching (cyclic majorities—Condorcet's paradox).

### Why Condorcet Dimension?

Rather than insist on a single popular outcome (which may not exist), we relax the requirement: **provide a small set of options** such that the majority can always find something they prefer in this set over any outsider.

The Condorcet dimension quantifies the minimal set size needed to achieve this guarantee.

### Key Structural Insight

For **weak orders** (transitive, complete preferences):
- Condorcet dimension is **always 2** for matchings, even with matroid constraints
- Any Pareto-optimal pair of matchings suffices

For **partial orders** (incomplete or intransitive preferences):
- Condorcet dimension jumps to $\Theta(\sqrt{n})$ for matchings
- Rises further to $\Theta(n)$ with matroid constraints
- This dramatic transition reveals sensitivity to preference structure

## Applications in Engineering

### 1. **Resource Allocation Systems**
- **Housing markets:** Assign housing to multiple families where no single allocation satisfies a majority
- **Job assignment:** Match workers to projects such that the algorithm outputs a small set of options, each defensible against alternatives
- **Curriculum scheduling:** Provide a small set of course schedules that collectively dominate other proposals

### 2. **Social Choice and Voting**
- **Ranked-choice ballots:** Instead of selecting one winner (which may not exist), output a small set of "co-winners" that collectively beat any challenger
- **Committee selection:** Minimize the set of candidate committees that maintain majority support

### 3. **Procurement and Supply Chain**
- **Supplier selection:** Under fragmented stakeholder preferences, maintain a small set of qualifying supplier matchings rather than forcing consensus on a single choice
- **Multi-objective procurement:** When budget, quality, and delivery preferences conflict across departments, design a compact Pareto set

### 4. **Bipartite Matching with Constraints**
- **Matching with matroid constraints:** Applied when matched items must form an independent set in a matroid (e.g., selecting diverse candidates, satisfying skill diversity)
- **Arborescence problems:** Selecting spanning trees in directed graphs where multiple agents have conflicting preferences over edge configurations

## Common Mistakes / Pitfalls

### 1. **Confusing Condorcet Winners with Condorcet Dimension 1**
A Condorcet winner may not exist even when trying to minimize dimension. Condorcet dimension 1 is achievable only when a majority-stable single outcome exists.

### 2. **Assuming Pareto Optimality Is Sufficient for All Preference Types**
- **True** under weak orders: every Pareto-optimal pair is Condorcet-winning
- **False** under partial orders: Pareto-optimal matchings may not form a Condorcet-winning set; worse, no Pareto-optimal pair may exist

### 3. **Ignoring the Cost of Constraints**
Adding matroid constraints doesn't increase Condorcet dimension for weak orders, but **increases it from $\Theta(\sqrt{n})$ to $\Theta(n)$ under partial orders**. This is not intuitive and often overlooked.

### 4. **Treating as Purely Theoretical**
The notion is deeply practical: it directly models "resource augmentation"—how much slack in item capacities is needed to