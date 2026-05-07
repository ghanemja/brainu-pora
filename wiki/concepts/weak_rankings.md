# Weak Rankings

## Definition

A **weak ranking** is a preference ordering over a set of alternatives where indifference is permitted—that is, not all pairs of alternatives need to be strictly ordered relative to one another. Formally, a weak ranking is a **complete preorder** on a set $X$: a binary relation $\succsim$ that is:

- **Complete**: For all $x, y \in X$, either $x \succsim y$ or $y \succsim x$ (or both)
- **Transitive**: For all $x, y, z \in X$, if $x \succsim y$ and $y \succsim z$, then $x \succsim z$

From a weak ranking $\succsim$, we derive:
- **Strict preference**: $x \succ y$ iff $x \succsim y$ and $y \not\succsim x$
- **Indifference**: $x \sim y$ iff $x \succsim y$ and $y \succsim x$

This contrasts with **strict rankings**, where indifference is prohibited and $\succ$ is a total order (antisymmetric).

## Key Equations

**Equivalence decomposition of weak rankings:**

$$\succsim \, = \, (\succ \cup \sim)$$

where the strict and indifference relations partition preferences:
- $x \succ y$ XOR $y \succ x$ XOR $x \sim y$ for any distinct $x, y$

**Induced weak rankings in matching contexts:**

Given a set of matchings $M$ and an agent's strict ranking over objects $O$, the induced weak ranking over $M$ satisfies:

$$m \succsim m' \iff \text{object assigned in } m \succsim_O \text{ object assigned in } m'$$

This creates indifference classes: all matchings where an agent receives the same object are mutually indifferent.

## Physical Intuition / Derivation

### Why Weak Rankings Arise Naturally

In many real-world settings, strict orderings are artificially restrictive:

1. **Matching and assignment problems**: An agent may have strict preferences over which *object* they receive, but multiple matchings deliver the same object to that agent. The agent genuinely cannot distinguish between these matchings—there is nothing forcing them to break ties arbitrarily.

2. **Indifference vs. incompleteness**: A weak ranking permits *indifference* (knowing alternatives are equally preferred) while maintaining *completeness* (being able to compare any two alternatives). This is more realistic than either strict rankings or incomplete preferences.

3. **Condorcet dimension complications**: When voters' preferences are weak rather than strict, the Condorcet dimension problem becomes harder. A weak ranking may admit fewer pairwise defeat relationships, changing which candidates qualify as "undefeated." This is why prior work on Condorcet dimension assumed strict rankings—the weak case was substantially more complex and remained open until recent work (Connor et al. 2025, Song et al. 2026).

### Information-Theoretic View

Weak rankings encode less information than strict rankings on the same set. If agents have strict preferences over a smaller set of objects, the induced weak ranking over a larger set of alternatives (e.g., matchings) "forgets" distinctions not relevant to the agent's core preference.

## Applications in Engineering

### 1. **Matching and Assignment Algorithms**
   - **Capacitated house allocation and stable matching**: Weak rankings capture agent preferences when institutional constraints collapse strict preference distinctions. Algorithms must find stable or popular matchings respecting weak preference structures (Manlove & Sng 2006, Abraham et al. 2007).
   - **Matroid-constrained matching**: When feasibility is restricted by matroid constraints and agents have weak preferences over outcomes, algorithms determine whether popular structures exist (Kavitha et al. 2025).

### 2. **Social Choice and Voting**
   - **Condorcet dimension under preference aggregation**: Understanding how many dimensions are needed to embed weak rankings as geometric projections. Determines computational difficulty of voting protocols (Charikar et al. 2025, Song et al. 2026).
   - **Set-valued voting rules**: Relaxations like dominating sets and approximately dominating sets must account for weak preference information (Charikar et al. 2026).

### 3. **Graph Structure Selection**
   - **Popular branchings and arborescences**: In directed graphs where agents have weak preferences over edge structures, algorithms identify structures preferred by majorities under weak preference orderings (Kavitha et al. 2025).

### 4. **Weighted and Constrained Settings**
   - **Weighted preference aggregation**: Extensions to weighted edges and costs require handling indifference in preference aggregation (Csáji et al. 2025).

## Common Mistakes / Pitfalls

1. **Confusing weak ranking with incomplete preference**: A weak ranking is *complete* (all pairs are comparable) but allows indifference. An incomplete preference relation leaves some pairs incomparable. These are distinct concepts.

2. **Assuming strict-preference algorithms work on weak rankings**: Results on Condorcet dimension, dominating sets, and popularity were historically proven for strict rankings. These results **do not automatically transfer** to weak rankings; as the source material notes, the weak case remained open and is substantially harder.

3. **Ignoring indifference when implementing voting/matching algorithms**: If an algorithm assumes strict rankings and is applied to weak rankings, it may incorrectly break indifferences or miss that certain alternatives are equivalent under the preference order.

4. **Treating weak rankings as arbitrary ties**: Indifference in a weak ranking is *determined by the context* (e.g., matching to the same object), not arbitrary. You cannot optimize away indifference without changing the fundamental problem.

5. **Forgetting that indifference is transitive**: A common error in algorithm design is treating indifference as a binary relation only between direct comparisons. Transitivity means if $x \sim y$ and $y \sim z$, then $x \sim z$ must hold, creating indifference classes.

## See Also

- [[Strict Ranking|Strict Rankings]]
- [[Condorcet Dimension]]
- [[Popular Matching]]
- [[Stable Matching]]
- [[Matroid Constraint]]
- [[Complete Preorder]]

## Sources

- Charikar et al. (