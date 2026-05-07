# Machine Unlearning

## Definition

**Machine unlearning** is a computational technique that removes the influence of specific data points from a trained machine learning model without retraining from scratch. Formally, given:

- An initial dataset $D_0 = (x_1, x_2, \ldots, x_n)$
- An algorithm $\mathcal{A}$ that produces an outcome $h_0$ (model, statistic, or hypothesis)
- A sequence of deletion requests for data points $x_{j_1}, x_{j_2}, \ldots, x_{j_k}$

A machine unlearning mechanism must efficiently produce updated outcomes $h_1, h_2, \ldots, h_k$ that reflect the state of the dataset after successive deletions, ideally matching what would result from retraining $\mathcal{A}$ from scratch on the remaining data.

**Perfect unlearning** is defined as producing outputs that are **computationally indistinguishable** from those obtained by complete retraining. This is the gold standard but carries significant hidden costs (see [[#Common Mistakes / Pitfalls]]).

---

## Key Equations

### Perfect Retraining (Ideal Standard)

For a dataset $D$ with deletion requests, the perfect unlearning outcome should satisfy:

$$h_{\text{unlearning}}(D \setminus \{x_j\}) \stackrel{d}{=} h_{\text{retraining}}(D \setminus \{x_j\})$$

where $\stackrel{d}{=}$ denotes computational indistinguishability.

### Approximate Unlearning (Relaxed Notion)

When perfect unlearning is infeasible, approximate definitions use differential privacy-style bounds:

$$\Pr[\mathcal{A}_{\text{unlearn}}(D, \text{delete } x_j) \in S] \leq e^{\epsilon} \cdot \Pr[\mathcal{A}_{\text{rerain}}(D \setminus \{x_j\}) \in S] + \delta$$

where $\epsilon$ and $\delta$ control privacy loss and $S$ is any measurable set of outcomes.

---

## Physical Intuition / Derivation

### Why Unlearning Matters

Traditional model deletion (retraining from scratch) is computationally prohibitive when data deletion requests arrive frequently. Unlearning seeks to answer: *Can we efficiently update a model to "forget" a deleted point without repeating all computation?*

### The Perfect Unlearning Paradox

The source material reveals a critical flaw in pursuing perfect unlearning: **the very mechanism that makes deletion look indistinguishable from never having included the data can be weaponized to reconstruct the entire dataset.**

**Reconstruction Attack Mechanism:**
An adversary controlling only $\omega(1)$ data points (essentially a constant number) can:
1. Issue deletion requests sequentially
2. Observe how the model's behavior changes with each deletion
3. Invert these changes to reconstruct the deleted data points
4. Repeat for nearly the entire dataset

**Intuition:** Perfect unlearning requires the model to respond differently when data is absent versus present. An adversary can observe these differential responses and reverse-engineer what was deleted—particularly for tasks (like summation) that are "securely computable" without deletion constraints.

### The Leakage-Utility Tension

This creates a fundamental trade-off:
- **Perfect unlearning** $\Rightarrow$ Strong guarantees for deleted data, but **leaks undeleted data**
- **Weak unlearning** $\Rightarrow$ Protects undeleted data, but leaves deleted data partially recoverable

---

## Applications in Engineering

### 1. **GDPR/CCPA Compliance**
- Legal requirement in EU (GDPR) and California (CCPA) for Right to be Forgotten
- Critical for companies training models on customer data
- Unlearning avoids the $\mathcal{O}(n)$ cost of retraining after each deletion request

### 2. **Data Valuation & Machine Teaching**
- Remove poisoned or adversarial training examples
- Assess influence of individual data points on model predictions
- Incrementally improve training datasets

### 3. **Federated Learning**
- Participants in federated networks want to revoke their contributions
- Central server must efficiently update global model without participant data
- Privacy-critical in healthcare, finance, IoT networks

### 4. **Real-time ML Systems**
- Spam detection (remove flagged examples)
- Recommendation systems (forget user history on request)
- Content moderation (retract training data from flagged content)

### 5. **Statistical Databases**
- Bulletin boards where records must be deletable
- Exact summation/aggregation with deletion support
- Query results must not leak information about deleted rows

---

## Common Mistakes / Pitfalls

### 1. **Conflating Perfect Unlearning with Privacy**
**Mistake:** Assuming that making deletion indistinguishable from never training on data protects *all* users.

**Reality:** Perfect unlearning actually compromises the privacy of **undeleted** data. A deletion request leaks information about what was deleted, which can be inverted to reconstruct the dataset.

**Correct approach:** Develop definitions that explicitly protect undeleted data against leakage caused by deletion operations.

### 2. **Ignoring the Reconstruction Attack**
**Mistake:** Designing unlearning mechanisms that satisfy perfect retraining without considering adversarial deletion queries.

**Reality:** Even with $\omega(1)$ controlled data points, an adversary can reconstruct nearly the entire dataset by exploiting differential responses to deletion requests.

### 3. **Oversimplifying the Definition**
**Mistake:** Using naive definitions like "the model should not change" or "delete all parameters related to that data."

**Reality:** No single definition works for all functionalities. Exact summation and statistical learning have different requirements than neural network retraining.

### 4. **Assuming Unlearning is Always Feasible**
**Mistake:** Believing that all tasks can be unlearned efficiently while preserving utility.

**Reality:** Some functionalities (like exact summation) are fundamentally incompatible with perfect unlearning. Trade-offs must be made explicit.

### 5. **Ignoring