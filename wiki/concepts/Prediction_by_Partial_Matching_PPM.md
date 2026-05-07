# Prediction by Partial Matching (PPM)

## Definition

**Prediction by Partial Matching (PPM)** is a hierarchical inference strategy that routes computation across multiple tiers of increasing cost and fidelity, indexed by the **code length** $L(i)$ under a domain-specific **Probability-Lookup Table (PLT)**. Rather than executing a single full model on every query, PPM first attempts to satisfy requests using cached high-probability outputs, applying lightweight corrections, quantized approximations, and only invoking full-fidelity inference when necessary.

PPM is a **cost-aware execution framework** that treats a trained model's probability distribution as a recipe for pre-computation. It organizes inference infrastructure around:
1. **Online PLT maintenance** — updating as new data arrives
2. **Multi-tier execution engine** — indexed by code length (equivalently, probability rank)
3. **Principled routing** — governed by value-of-caching signal $V(a)$

## Key Equations

### Code Length and Routing

The fundamental routing decision is based on the **expected code length** $L(i)$ (in bits) required to encode output $a$ under the domain-specific model:

$$L(a) = -\log_2 p(a)$$

where $p(a)$ is the model's probability estimate for action/output $a$.

### Value of Caching

The **net value** of pre-computing and caching a result (vs. computing it on-demand) is:

$$V(a) = \hat{p}(a) \cdot C_c - C_s$$

where:
- $\hat{p}(a)$ = observed frequency of queries matching $a$ (empirical probability)
- $C_c$ = cost of computation at Tier 4 (full model inference)
- $C_s$ = cost of cache storage and lookup

A result is cached (or promoted to a higher tier) when $V(a) > 0$.

### Tier-Based Cost Model

Under PPM, expected inference cost per query decreases over deployment time:

$$\mathbb{E}[\text{Cost}(t)] = p^*(t) \cdot C_{\text{Tier 4}} + (1-p^*(t)) \cdot \bar{C}_{\text{Tiers 1-3}}$$

where $p^*(t)$ is the fraction of queries requiring Tier 4 (full inference) at time $t$, and $p^*(t)$ decreases monotonically as the cache/artifact store accumulates.

## Physical Intuition / Derivation

### Why PPM Works: The Probability-Cost Duality

Modern ML models output **probability distributions** over their domain (next token, action, search ranking, etc.). However, standard deployment ignores this: every query triggers the same full computation regardless of output probability.

PPM inverts this logic:
- **High-probability outputs** (short code length, $-\log p(a)$ small) should be pre-computed and cached
- **Low-probability outputs** (long code length) cost more to represent; compute them on-demand

This is **information-theoretic**: the code length $L(a) = -\log_2 p(a)$ measures how "surprising" an output is. Unsurprising (common) outputs deserve investment in caching.

### The Four-Tier Spectrum

PPM instantiates the same computational structure across all domains:

| Tier | Mechanism | Code Length | Cost | Example (LLM) |
|------|-----------|-------------|------|---|
| **1** | Exact pre-computation | $L \approx 0$ | $C_1$ (lookup) | Exact output cache |
| **2** | Cached base + lightweight correction | $L$ small | $C_2 \approx 0.1 C_4$ | KV-cache prefix + small model tail |
| **3** | Approximate/quantized model | $L$ medium | $C_3 \approx 0.5 C_4$ | Quantized model inference |
| **4** | Full-fidelity inference | $L$ large | $C_4$ | Full-precision forward pass |

Routing between tiers is **not** manual thresholding—it emerges from optimizing $V(a)$ as empirical probabilities $\hat{p}(a)$ are observed.

### The Learning Curve

Under stationary traffic, as deployment continues:
- Cache accumulates outputs for frequently-queried inputs
- $p^*(t)$ (fraction needing Tier 4) decreases exponentially (or power-law)
- Serving cost per query **drops over time** (unlike traditional systems with constant per-query cost)

This creates a virtuous cycle: system becomes self-optimizing without retraining.

## Applications in Engineering

### 1. **Large Language Model (LLM) Inference**
- **Tier 1**: Exact output cache (repeated queries → instant response)
- **Tier 2**: KV-cache for matched prefix + small model for suffix generation
- **Tier 3**: Quantized model (INT8, 4-bit weights)
- **Tier 4**: Full-precision forward pass
- **Benefit**: Deployment cost falls from $\mathcal{O}(1)$ per query to $\mathcal{O}(\log N)$ as cache grows (where $N$ = total queries served)

### 2. **Search & Information Retrieval**
- **Tier 1**: Session replay (user's past queries cached)
- **Tier 2**: Cached workflow + personalization correction
- **Tier 3**: Lightweight ranking model (fast feature-based ranker)
- **Tier 4**: Full neural retrieval model
- **Benefit**: Reduces expensive neural ranking calls by 80–95% for repetitive user patterns

### 3. **Game Playing (Chess / MCTS)**
- **Tier 1**: Exact tablebase lookup (endgame positions, precomputed)
- **Tier 2**: Cached opening line + shallow search adjustment
- **Tier 3**: Standard MCTS with reduced node budget
- **Tier 4**: Full MCTS from scratch (high branching factor)
- **Benefit**: Exploits opening theory and endgame tables to prune search early

### 4.