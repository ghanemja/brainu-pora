# Doubly-linked list data structure

## Definition

A **doubly-linked list** is a linear data structure where each element (node) contains:
- A **data value** or reference
- A **forward pointer** (next) pointing to the subsequent node
- A **backward pointer** (previous) pointing to the preceding node
- Optionally, sentinel nodes at the head and tail to simplify boundary conditions

Formally, a doubly-linked list $\Lambda$ can be represented as a sequence of nodes where each node $n_i$ maintains:
$$n_i = \langle \text{data}_i, \text{prev}_i, \text{next}_i \rangle$$

with $\text{next}_i \to n_{i+1}$ and $\text{prev}_i \to n_{i-1}$ for $i \in \{1, \ldots, k\}$, where $k$ is the list length.

## Key Equations

**Time Complexity Analysis:**
- Insert at known position: $O(1)$ time
- Delete at known position: $O(1)$ time  
- Search (linear scan): $O(n)$ time
- Space complexity: $O(n)$ where $n$ is the number of elements

**Memory Layout:**
$$\text{Memory per node} = s_{\text{data}} + 2s_{\text{pointer}} \text{ bytes}$$

where $s_{\text{pointer}}$ typically equals 8 bytes on 64-bit systems.

## Physical Intuition / Derivation

### Why Doubly-Linked Lists Exist

Consider insertion/deletion operations:
- **Singly-linked lists** require $O(n)$ time to delete an element because you must traverse from the head to find the predecessor node
- **Doubly-linked lists** eliminate this bottleneck: given a node to delete, you can immediately access its predecessor via the backward pointer and update pointers in $O(1)$ time

### The Bidirectional Navigation Principle

The key insight is **redundancy for speed**: storing backward pointers is memory-efficient (one extra pointer per node) compared to the algorithmic cost of traversing to find predecessors.

```
Traditional singly-linked:  A → B → C → D → (null)
                           ↑           ↑
                       Must traverse from A to get to C's predecessor

Doubly-linked:  (null) ← A ↔ B ↔ C ↔ D → (null)
                           ↑   ↓   ↑
                       Direct O(1) access in both directions
```

### Practical Use Case: Occurrence Lists

In the source material, doubly-linked lists enable **occurrence lists**—collections tracking where specific elements appear in a sequence. The critical operation is:

$$\text{Delete}(\Lambda, i) \text{ requires: Find node at } T[i], \text{ then remove from } \Lambda' \text{ in } O(1)$$

This works because:
1. Array $T[i]$ stores a direct pointer to the node in the list
2. Doubly-linked structure allows the node to update its neighbors: 
   $$\text{prev}(i).\text{next} \leftarrow \text{next}(i)$$
   $$\text{next}(i).\text{prev} \leftarrow \text{prev}(i)$$
3. No traversal needed; O(1) guaranteed

## Applications in Engineering

### 1. **Algorithm Implementation**
- **Cache/buffer management**: LRU (Least Recently Used) caches use doubly-linked lists to track access order while maintaining O(1) eviction
- **Undo/Redo functionality**: Text editors maintain doubly-linked lists of edits for bidirectional navigation
- **Scheduling queues**: Operating systems use them for process scheduling with efficient insertion/removal

### 2. **Language Parsing & Enumeration**
From the source material: occurrence lists implemented as doubly-linked lists enable efficient enumeration of language infixes with **constant delay** between successive results. This is critical for:
- Finite automaton simulation with occurrence tracking
- Pattern matching in formal language processing

### 3. **Database Index Structures**
- **B-link trees** and similar structures use doubly-linked leaves for range queries
- Skip lists optionally include backward pointers for bidirectional scans

### 4. **Memory Management**
- Kernel memory allocators (Linux buddy allocator, glibc malloc) use doubly-linked lists to track free blocks

## Common Mistakes / Pitfalls

### 1. **Assuming Constant-Time Search**
❌ **Wrong**: "Doubly-linked lists have O(1) search"  
✓ **Correct**: O(1) applies only to insert/delete *at a known location*. Finding an element still requires $O(n)$ traversal.

### 2. **Pointer Dereferencing in Loop Bounds**
A subtle bug: storing `node.next` before a loop that might delete nodes:
```
next_node = current.next    // Correct: cache before potential deletion
for node in list:
    delete(node)
    current = next_node     // Safe even if list structure changes
```

### 3. **Cache Locality Misses**
❌ **Misconception**: "Doubly-linked lists are always faster for dynamic data"  
✓ **Reality**: Poor cache locality compared to arrays. Forward and backward pointers point to arbitrary memory addresses, causing frequent cache misses in tight loops. Use arrays when random access dominates.

### 4. **Memory Overhead Underestimation**
For small data (e.g., integers), the pointer overhead is significant:
- List of 100 integers: $100 \times 8 \text{ bytes (data)} + 200 \times 8 \text{ bytes (pointers)} = 1.6 \text{ KB}$
- Array of 100 integers: $100 \times 8 \text{ bytes} = 0.8 \text{ KB}$

### 5. **Forgetting Sentinel Nodes**
Boundary conditions (inserting at head, deleting tail) become complex without sentinel nodes. Always use them to eliminate special cases.

## See Also

- [[Hash Table with Chaining]] — doubly-linked