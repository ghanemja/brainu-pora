# Matching Problem

## Definition

A **matching problem** is a combinatorial assignment problem where agents must be matched to objects (or resources) subject to feasibility constraints and preference considerations. Formally:

Given:
- A set of agents $A = \{a_1, a_2, \ldots, a_n\}$
- A set of objects $O = \{o_1, o_2, \ldots, o_m\}$ with capacities $c(o_j)$ for each object
- Preference relations $\succeq_i$ over objects for each agent $i$

A **matching** $M$ assigns each agent to a subset of objects such that:
$$\sum_{i: o_j \in M(a_i)} 1 \leq c(o_j) \quad \forall o_j \in O$$

where $M(a_i)$ denotes the set of objects matched to agent $a_i$.

**Constrained variants** further restrict feasible matchings via:
- **Matroid constraints**: The set of matched objects must form an independent set in a matroid structure
- **Arborescence constraints**: Matched objects form a directed tree structure (generalization of branchings)

**Preference models** can range from restrictive to general:
- **Strict rankings**: Total order $\succ_i$ with no indifference
- **Weak rankings**: Allows tied (indifferent) objects
- **Partial orders**: Arbitrary transitive relations (e.g., semiorders where indifference need not be transitive)

## Key Equations

### Pareto Optimality

A matching $M^*$ is **Pareto-optimal** if no other matching $M$ exists such that:
$$M \succeq_i M^* \text{ for all } i \in A \quad \text{and} \quad M \succ_j M^* \text{ for at least one } j \in A$$

### Condorcet Winning

A matching $M$ is a **Condorcet winner** if for every alternative matching $M'$:
$$|\{i : M \succeq_i M'\}| > |\{i : M' \succ_i M\}|$$

A set $\mathcal{S}$ of matchings is **weakly Condorcet-winning** if for every matching outside $\mathcal{S}$:
$$|\{i : M \in \mathcal{S}, M \succeq_i M'\}| \geq |\{i : M' \succ_i M \text{ for all } M \in \mathcal{S}\}|$$

### Condorcet Dimension

The **Condorcet dimension** is the minimum cardinality of a set $\mathcal{S}$ that is guaranteed to be (weakly) Condorcet-winning in all preference instances:

$$d_C(\mathcal{P}) = \min \{|\mathcal{S}| : \mathcal{S} \text{ is Condorcet-winning for all preference profiles in class } \mathcal{P}\}$$

## Physical Intuition / Derivation

### Why Matching Problems Matter

Matching problems arise whenever we need fair allocation under capacity constraints. The tension between **individual preference satisfaction** and **collective agreement** creates a fundamental trade-off:

- **Pareto optimality**: No resource is wasted (no objectively better allocation exists)
- **Condorcet winningness**: A majority prefers the allocation to alternatives

### Core Insight: Pareto ⟹ Condorcet

The main theoretical result connects these concepts:

> **Every Pareto-optimal set of matchings of size $\geq 2$ is weakly Condorcet-winning.**

*Why this holds:* If $M$ is Pareto-optimal and some agent $i$ strictly prefers $M'$ to all matchings in the Pareto-optimal set $\mathcal{S}$, then $M'$ must make another agent worse off. This creates a coalition voting *against* $M'$, ensuring the Pareto set maintains majority support.

### Complexity by Preference Structure

The **Condorcet dimension** grows with preference generality:

| Preference Model | Matchings | Matroid-Constrained | Arborescences |
|---|---|---|---|
| Strict Rankings | 2 | 2 | 2 |
| Weak Rankings | 2 | 2 | $n$ |
| Partial Orders | 2 | $\Theta(\sqrt{n})$ | $n$ |

Interpretation: When agents can have *arbitrary* partial order preferences (e.g., incomparable options), we need exponentially more representative matchings to guarantee majority approval. This reflects real-world complexity in preference elicitation.

### Capacity Doubling Result

A practical technique: **Doubling the capacity of every object guarantees existence of a weak Condorcet winner** in any instance. This gives a constructive bound for achieving consensus in constrained allocation.

## Applications in Engineering

### Course Allocation
Instructors assign courses to time slots with capacity constraints and temporal restrictions. Matroid constraints model which time slots can run simultaneously. A matching outcome should satisfy both:
- No time slot exceeds enrollment capacity
- The assignment is Pareto-efficient (no reshuffling helps all students)

### Resource Scheduling
Allocating computing resources (GPUs, memory) to jobs with:
- Job priorities (strict/weak orderings over resource configurations)
- Hardware constraints (arborescence structure: GPU cluster with hierarchical allocation)
- Goal: Find allocation sets that resist majority override

### Mechanism Design (Liquid Democracy)
In democratic systems, citizens can:
- Vote directly on issues (strict preference)
- Delegate to representatives (partial order: unaware which representatives best represent them)

Branchings model delegation chains; arborescences generalize to hierarchical governance. Condorcet dimension quantifies how many governance structures suffice for consensus.

### Supply Chain & Logistics
Matching suppliers to retailers with:
- Supplier capacities
- Retail demand and preferences
- Matroids represent feasible supplier subsets (e.g., geographic diversity, risk balancing)

Goal: Negotiate an allocation that survives coalition blocking attempts.

### Kidney Exchange Programs
Patients matched to donors with:
- Compatibility constraints (who can receive