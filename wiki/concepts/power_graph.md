# power graph

## Definition

A **power graph** is a visualization and compression technique for dense graphs that abstracts multiple vertices into **modules** (also called supernodes) and represents all edges between two modules as a single **compression edge**. 

Formally, a power graph consists of:
- A set of modules $M$ that partition or hierarchically organize the original vertex set $V$
- A condensed edge set where each edge represents all connections between two modules
- A **tree compression** structure where modules form a containment hierarchy: if two modules overlap, one must be completely contained within the other (no partial overlaps allowed)

This constraint—that modules follow a tree structure rather than an arbitrary DAG—distinguishes power graphs from more general **DAG compressions**.

## Key Characteristics

| Property | Description |
|----------|-------------|
| **Module Structure** | Modules group vertices; nesting is allowed |
| **Overlap Constraint** | If modules $M_i$ and $M_j$ overlap: either $M_i \subseteq M_j$ or $M_j \subseteq M_i$ |
| **Compression Type** | Corresponds to **tree compressions** (hierarchical, no crossing containment) |
| **Complexity** | Finding a minimal power graph (single-level) is **NP-hard** (Dwyer et al.) |

## Physical Intuition / Derivation

### Problem It Solves
Dense graphs with many vertices and edges become visually incomprehensible. A power graph "zooms out" by grouping related vertices into modules, replacing clutter with abstract structure.

### Why Tree Compression?
The containment constraint (tree structure) ensures:
1. **Clear hierarchy**: Modules have a parent-child relationship, like a file system
2. **No ambiguity**: No overlapping modules with unclear boundaries
3. **Efficient representation**: The tree structure itself aids both visualization and compression

### Comparison to DAG Compression
A **DAG compression** relaxes the tree constraint, allowing more flexible module relationships (directed acyclic graph of containment). This can yield smaller compressions but at computational cost:
- Example: The **rook graph** has linear-size DAG compressions but no known linear-size tree compression
- This suggests DAG compression is strictly more powerful than tree compression

## Applications in Engineering

### 1. **Network Visualization**
   - Representing large social networks, communication graphs, or organizational hierarchies
   - Collapsing departments/teams into single nodes in org charts

### 2. **Circuit Design & Hardware Abstraction**
   - Hierarchical compression of VLSI circuits (gates → modules → blocks)
   - Simplifying layouts of complex chip designs

### 3. **Software Architecture**
   - Visualizing large codebases: functions → classes → packages → modules
   - Identifying and abstracting tightly coupled subsystems

### 4. **Biological Networks**
   - Protein interaction networks: individual proteins → functional complexes → pathways
   - Gene regulatory networks with hierarchical modules

### 5. **Infrastructure & Logistics**
   - Supply chain networks: nodes → distribution centers → regions
   - Road networks: intersections → neighborhoods → cities

## Computational Complexity

Finding minimal power graphs is **NP-hard**, even in restricted cases:

$$\text{DECISION PROBLEM: Given } G=(V,E) \text{ and } k, \text{ does } G \text{ admit a compression with } |E_{\text{compressed}}| \leq k?$$

This is NP-hard (Dwyer et al., Bannach et al.).

**Important caveat**: Minimizing only compression edges $|E|$ is a theoretical interest. The true objective is minimizing total encoding size:
$$\text{Minimize: } |M| + |E_{\text{compressed}}|$$
where $|M|$ is the encoding cost of the module structure. Whether this combined problem is hard remains an active research question.

## Common Mistakes / Pitfalls

1. **Confusing Tree vs. DAG Compression**
   - ❌ Assuming all graph compressions use tree structure
   - ✓ Power graphs specifically enforce tree containment; DAG compressions are more general

2. **Ignoring Encoding Cost**
   - ❌ Minimizing only compression edges while ignoring the cost to store module definitions
   - ✓ The full cost is $|M| + |E_{\text{compressed}}|$; small edge sets may require expensive module hierarchies

3. **NP-hardness Misconception**
   - ❌ Concluding that power graphs are impractical
   - ✓ NP-hardness applies to optimal solutions; good heuristics and approximations are effective for engineering applications

4. **Overlapping Modules**
   - ❌ Allowing modules to cross without containment
   - ✓ Strict tree structure (one contains the other) is essential to power graph definition

5. **Scalability Assumptions**
   - ❌ Assuming compression always yields linear-size results
   - ✓ Compression quality depends on graph structure; worst-case sizes can be large

## See Also

- [[DAG compression]] — generalization allowing directed acyclic module hierarchies
- [[tree compression]] — the formal class to which power graphs belong
- [[twin-width]] — graph parameter bounding compression; graphs with bounded twin-width have linear-size tree compressions
- [[graph visualization]] — broader context for compression as a visual abstraction technique
- [[module detection]] — closely related problem of identifying natural modules/communities in graphs

## Sources

- Dwyer et al. [10] — Original hardness results for minimal power graphs
- Bannach et al. [1] — Complexity analysis of DAG vs. tree compressions; rook graph lower bounds
- Bonnet et al. [4] — Twin-width parameter and relationship to compressions
- Chudigiewitsch, Tantau, Winkler — Comprehensive treatment of compression complexity and update dynamics