# Snake Configuration

## Definition

A **snake configuration** is a connected, linearly-arranged structure of modular robotic units (cubes) that can adaptively own and hold cells in a grid space. Formally, a snake configuration $S(P)$ is defined by:

- A **spine path** $P$: a valid sequence of grid cells forming the backbone of the snake
- A **head vertex** and **tail vertex**: interchangeable endpoints of the spine
- **Module ownership**: modules contained within the snake's cell space that the snake permanently possesses
- **Module holding**: modules in non-free cells that the snake temporarily occupies during operations
- **Cell space**: the set of all cells occupied by the snake, which expands/contracts dynamically

The distinction between owned and held modules is critical: owned modules remain with the snake indefinitely, while held modules are released when the snake retracts from their cells.

## Key Equations

**Push Operation Complexity:**
$$\text{Push makespan} = O(1)$$

**Pull Operation Complexity:**
$$\text{Pull makespan} = O(1)$$

**Teleportation Capacity:**
$$N_{\text{teleport}} \leq 12 \text{ modules per push}$$

**Cell Expansion per Push:**
$$\Delta \text{cells}_{\text{push}} = 21$$

**Invariant - Held Modules:**
$$|M_{\text{held}}| = |C_{\text{held}}|$$

where $M_{\text{held}}$ and $C_{\text{held}}$ are the sets of held modules and held cells, respectively.

**Invariant - Owned Modules:**
$$\frac{d|M_{\text{owned}}|}{dt}\bigg|_{\text{pull}} \geq 0$$

Owned modules never decrease during pull operations.

## Physical Intuition / Derivation

### Motivation
Snake configurations model modular robotic systems that must navigate and manipulate environments where they encounter fixed obstacles. The robot must track which modules it "owns" (has claimed) versus temporarily "holds" (is currently occupying but may release).

### Core Insight
The key innovation is **decoupling ownership from occupancy**. A snake can:

1. **Push forward** (expand): extend its spine into new territory, gaining up to 12 interior modules via teleportation and claiming up to 21 new cells. If a cell was previously non-free, the snake *holds* (but does not own) its module.

2. **Pull backward** (contract): retract the tail, releasing held modules back into vacated cells. Since the snake only leaves modules in cells it *held*, it never loses ownership of its original modules.

3. **Fork** (reproduce): split into two independent snakes by teleporting interior modules along a prefix/suffix of the spine. The new snake forms a valid configuration with $O(1)$ transformations.

4. **Join** (merge): combine two snakes at a common endpoint if their union forms a valid spine path.

### Why O(1) Complexity?
Push and pull operations achieve constant-time makespan (schedule length) because:
- Teleportation within the spine is distance-independent
- All physical movements happen in parallel across modules
- The spine topology remains valid after each operation by construction

### Head-Tail Interchangeability (Lemma 11)
The roles of head and tail are interchangeable because the snake's operations (push, pull, teleportation) are defined symmetrically. Reversing the orientation of the spine path and relabeling endpoints requires only $O(1)$ module rearrangements within the spine.

## Applications in Engineering

### Modular Robotics
- **Reconfigurable robots**: snakes enable robot swarms to dynamically split into smaller units (forking) and reassemble (joining) for task-specific morphologies
- **Space exploration**: a single snake rover could adapt its structure to navigate narrow canyons (pull to contract) or reach distant areas (push to extend)

### Self-Assembling Systems
- **Manufacturing**: modular manufacturing lines where workstations (modules) can be dynamically allocated by "owning" them when in use and "holding" them during transient occupation
- **Warehouse automation**: mobile shelf systems that rearrange themselves while maintaining item integrity

### Parallel Computing / Graph Algorithms
- **Network reconfiguration**: snakes model dynamic network topologies where nodes (modules) can be claimed or temporarily borrowed, with complexity guarantees for reorganization tasks

### Multi-Agent Path Planning
- **Collision avoidance**: snakes' held/owned distinction provides a framework for agents to negotiate shared spaces without permanent conflicts

## Common Mistakes / Pitfalls

1. **Confusing Ownership with Occupancy**
   - ❌ "The snake owns every cell it occupies."
   - ✓ The snake *holds* non-free cells but only *owns* modules it explicitly claimed.

2. **Assuming Push Always Costs Memory**
   - ❌ "Each push increases owned modules by 21."
   - ✓ Only up to 12 interior modules are teleported; the remaining 9 cells may be owned or held depending on prior occupancy.

3. **Forgetting Head-Tail Symmetry**
   - ❌ "Head and tail have different operational capabilities."
   - ✓ They are functionally symmetric via $O(1)$ swapping operations (Lemma 11).

4. **Misunderstanding Fork Complexity**
   - ❌ "Creating a new snake requires linear time in its length."
   - ✓ Forking is $O(1)$ because only a constant number of interior modules need teleportation; the spine path itself is just reinterpreted.

5. **Ignoring Spine Validity Constraints**
   - ❌ "Any path can be a valid spine."
   - ✓ The union of two spines can only form a valid joined snake if their combined path is itself a valid spine (no cycles, proper connectivity).

## See Also

- [[Modular Robotics]]
- [[Parallel Scheduling Algorithms]]
- [[Graph Path Planning]]
- [[Reconfigurable Systems]]
- [[Self-Assembly]]

## Sources

- Lecture/paper excerpt on "snake configuration" in the context of parallel sliding-cubes robots
  - Lemma 9, 10, 11; Corollary 12 (push/pull/teleportation