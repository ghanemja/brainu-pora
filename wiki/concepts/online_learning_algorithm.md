# Online Learning Algorithm

## Definition

An **online learning algorithm** is a computational procedure that makes sequential decisions under uncertainty, updating its strategy dynamically as new information arrives, without requiring complete knowledge of the future environment beforehand.

In the context of decision-making under distributional shift (as illustrated in the source material), an online learning algorithm must navigate the tension between two competing objectives:

1. **Consistency**: achieving low loss when predictions are accurate (small prediction error)
2. **Robustness**: maintaining bounded loss even under large distributional shifts, without advance knowledge of the error magnitude

The algorithm observes a predicted distribution $\hat{p}$ of future events and must commit to actions while the true distribution $p$ remains unknown. The quality of the prediction is measured by the Earth Mover Distance (EMD): $\text{EMD}(\hat{p}, p)$.

## Key Equations

**Loss bound with robustness guarantee:**
$$L(\text{algorithm}) = O\left(\min_{\sqrt{b} \cdot \max(\text{EMD}(\hat{p}, p), 1)} \right)$$

where $b$ is a problem-dependent parameter (e.g., rental cost in ski rental problems).

**Robust loss bound:**
$$L_{\text{robust}} = O(b \log b)$$

achieved when the algorithm employs a truncation-based modification independent of the unknown true EMD.

**Consistency regime:**
When $\text{EMD}(\hat{p}, p) \leq \sqrt{b} \log b$, the algorithm maintains near-optimal performance:
$$L = \text{OPT} + O(\sqrt{b} \cdot \text{EMD}(\hat{p}, p))$$

**Truncation threshold:**
$$U = \min\{d : P_{\hat{p}}(D > d) \leq 1/\sqrt{b}\}$$

where $U$ defines the truncation point based on tail probability mass in the predicted distribution.

## Physical Intuition / Derivation

### The Core Dilemma

Online learning algorithms face a fundamental trade-off. Consider a simple approach: **compute the optimal policy for the predicted distribution $\hat{p}$, then execute it.** This performs excellently when $\hat{p} \approx p$, but catastrophically fails when predictions are wildly wrong—incurring arbitrarily large additive losses.

The naive question is: *why not just add a safety margin?* For instance, in the ski rental problem, delay purchasing by $\sqrt{b}$ days. This gives the loss bound:
$$O\left(\sqrt{b} \cdot \max(\text{EMD}(\hat{p}, p), 1)\right)$$

This base algorithm is **non-robust** because its loss scales linearly with prediction error. If EMD is large, this could be terrible.

### The Truncation Trick

The key insight is to add a **truncation condition** that protects against rare but devastating tail events in the prediction:

1. Compute the optimal buying threshold $\hat{K}$ under predicted distribution $\hat{p}$
2. Separately compute $U$: the point where the predicted distribution concentrates $1 - 1/\sqrt{b}$ of its probability mass
3. **If $U < \hat{K}$** (the optimal policy occurs in the tail of the prediction), override: buy on day $U + \sqrt{b}$ instead

**Why does this work?**

- **When predictions are good** ($\text{EMD} \leq \sqrt{b}\log b$): The truncation only triggers if the optimal buying time occurs when $\hat{p}$ has negligible probability mass—a rare event. When it occurs, translating between $\hat{p}$ and $p$ adds only $O(1)$ multiplicative loss.

- **When predictions are bad**: The truncation forces an action before the tail probability dominates, limiting worst-case loss to $O(b \log b)$ regardless of how wrong $\hat{p}$ is.

This elegantly decouples robustness from consistency: the modification is "invisible" in the low-error regime but provides absolute protection in high-error regimes.

## Applications in Engineering

### 1. Supply Chain & Inventory Management
Online learning algorithms decide procurement quantities using demand forecasts. Real demand distributions differ from predictions (e.g., unexpected supply disruptions). The robust algorithm prevents catastrophic overstock/understock while exploiting accurate forecasts.

### 2. Online Pricing & Revenue Management
An airline predicts passenger demand distribution and must set prices dynamically. The algorithm must commit prices without knowing true demand but should quickly adapt if early bookings deviate significantly from predictions.

### 3. Job Scheduling & Resource Allocation
Computing clusters receive jobs with predicted execution time distributions. Schedulers must allocate resources upfront. Online learning prevents pathological cases where all predictions are wrong while maintaining efficiency under accurate forecasts.

### 4. Adaptive Control Systems
Robotics and autonomous systems make control decisions based on learned environment models. Robustness guarantees ensure safe operation even when the learned model degrades significantly.

### 5. Machine Learning Model Deployment
When deploying ML models, actual data distributions drift from training data (distribution shift). Online learning algorithms monitor performance and trigger fallback strategies without requiring explicit knowledge of the shift magnitude.

### 6. Network Routing
Routers must decide packet forwarding using predicted link latency/capacity distributions. The algorithm achieves both consistency (exploits accurate predictions) and robustness (handles congestion/failures).

## Common Mistakes / Pitfalls

### 1. **Confusing "Online" with "Real-Time"**
Online learning does not require instant response or low computational complexity. It means decisions are made sequentially with incomplete future information. Algorithms can be computationally expensive.

### 2. **Ignoring the Role of Prediction Error Metrics**
Students often treat EMD abstractly. Remember: the algorithm's guarantees *depend critically* on whether EMD is measured correctly. Using wrong distance metrics (e.g., total variation instead of EMD for heavy-tailed distributions) breaks robustness.

### 3. **Over-Trusting the Consistency Regime**
Just because $\text{EMD}(\hat{p}, p) \leq \sqrt{b}\log b$ is achievable in practice doesn't mean you can ignore robustness. The regime is not verifiable without knowing $p$—the whole point of robustness is handling *unknown*