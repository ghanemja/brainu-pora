# Fairness Constraints

## Definition

Fairness constraints are formal restrictions applied to algorithmic decision-making systems to ensure equitable treatment across protected groups (demographic categories such as gender, race, or ethnicity). In the context of scoring functions, fairness constraints require that the algorithm's output satisfies specific statistical or distributional properties that prevent systematic bias or discrimination against any protected group.

More formally, a fairness constraint is a logical or mathematical condition of the form:

$$C(f, G_i) \leq \epsilon$$

where $f$ is a scoring or decision function, $G_i$ is a protected group, and $\epsilon$ is a tolerance threshold. The constraint ensures that some disparity metric between groups remains below an acceptable level.

## Key Equations

### Linear Scoring Function with Fairness

For a linear scoring function:
$$f(c) = \sum_{j=1}^{d} w_j \cdot x_j$$

where $w_j$ are weights and $x_j$ are feature scores, fairness constraints typically restrict the weight vector $\mathbf{w} = [w_1, \ldots, w_d]$ to lie within a feasible subspace $\mathcal{W}_{\text{fair}}$ such that:

$$\mathcal{W}_{\text{fair}} = \{\mathbf{w} : C(f, G_i) \leq \epsilon \text{ for all protected groups } G_i\}$$

### Multi-Group Fairness Constraint

For multiple protected groups $G_1, G_2, \ldots, G_k$, the joint fairness requirement becomes:

$$\bigcap_{i=1}^{k} \{\mathbf{w} : C(f_{\mathbf{w}}, G_i) \leq \epsilon_i\}$$

This represents the intersection of all individual group constraints, which may be empty (no feasible solution exists) or computationally expensive to characterize.

### Optimization Objective

The practical problem becomes:

$$\min_{\mathbf{w} \in \mathcal{W}_{\text{fair}}} \left\| \mathbf{w} - \mathbf{w}^{\text{ref}} \right\|_2$$

where $\mathbf{w}^{\text{ref}}$ is a reference (potentially unfair) weighting, minimizing deviation while maintaining fairness.

## Physical Intuition / Derivation

### Why Fairness Constraints Matter

In real-world selection processes (hiring, admissions, lending, criminal sentencing), algorithms often inherit biases present in historical data. A naive scoring function that optimizes accuracy or efficiency alone may systematically disadvantage protected groups, even without explicit discriminatory intent.

**Example scenario:** An officer designs a hiring scoring function with equal weights: $f(c) = 0.5 \times g + 0.5 \times s$ where $g$ is GPA and $s$ is standardized test score. If these features correlate with protected characteristics, this "neutral" weighting may select disproportionately from one demographic group. Fairness constraints force the algorithm to adjust weights (e.g., $f(c) = 0.6 \times g + 0.4 \times s$) to maintain approximately equal representation or equal selection rates across groups.

### The Tie-Breaking Challenge

A critical subtlety emerges when multiple candidates have identical or very similar scores. If candidates are tied, the tie-breaking rule (which candidates to select) can significantly alter demographic representation in the final selection. This means fairness constraints must account not just for score distributions, but for how tied candidates are resolved—adding a combinatorial layer of complexity.

### Computational Hardness

When multiple protected groups are present *and* tie-breaking is properly considered, the problem of finding any fair scoring function becomes **NP-hard** even in low dimensions (2D). This reflects a fundamental tension:
- With one protected group, efficient algorithms exploit a "Small $k$ Opportunity" (where $k$ is dataset size)
- With multiple groups, the feasible region $\mathcal{W}_{\text{fair}}$ becomes highly constrained and non-convex
- A lower bound of $\Omega(n^k)$ applies for constant numbers of protected groups, meaning brute-force enumeration may be necessary in worst cases

## Applications in Engineering

### 1. **Hiring and Recruitment Algorithms**
Scoring functions select candidates based on weighted combinations of qualifications. Fairness constraints ensure recruitment doesn't inadvertently exclude protected groups, satisfying legal requirements (e.g., disparate impact doctrine under Title VII).

**Example:** Weight adjustments to balance GPA, test scores, and experience while maintaining equal hiring rates across gender and racial groups.

### 2. **Lending and Credit Scoring**
Financial institutions use scoring functions to assess creditworthiness. Fairness constraints prevent algorithmic redlining (systematic denial of credit to protected neighborhoods/demographics) while maintaining credit quality.

### 3. **Criminal Justice and Risk Assessment**
Recidivism prediction algorithms guide sentencing and parole decisions. Fairness constraints mitigate racial disparities in criminal justice outcomes, ensuring equal false positive/negative rates across racial groups.

### 4. **University Admissions**
Holistic scoring combines test scores, GPA, essays, and extracurriculars. Fairness constraints can enforce equal admission rates or equal qualification thresholds across demographic groups.

### 5. **Content Recommendation Systems**
Recommendation algorithms weight user features and item attributes. Fairness constraints ensure recommendations don't create filter bubbles that disproportionately affect minorities or create disparate visibility for content creators from protected groups.

## Common Mistakes / Pitfalls

### 1. **Ignoring Feasibility**
Engineers often assume a fair scoring function always exists. In reality, tight fairness constraints may create an empty feasible region $\mathcal{W}_{\text{fair}} = \emptyset$, requiring relaxation of constraints or acceptance that perfect fairness is impossible.

### 2. **Neglecting Tie-Breaking**
A common oversight is treating scores as continuous and ignoring that in practice, ties are common. The tie-breaking rule can dramatically shift group representation, undermining fairness. A scoring function may satisfy statistical fairness metrics while unfair tie-breaking reverses this benefit.

### 3. **Conflating Different Fairness Definitions**
"Fairness" is not monolithic. Equal selection rates, equal false positive rates,