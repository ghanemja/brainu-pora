# Sequential Calibration

## Definition

**Sequential calibration** is the problem of adjusting a sequence of probabilistic predictions over time to match the empirical frequencies of outcomes, ensuring that predictions are well-calibrated with respect to ground truth labels.

More formally, given:
- A domain $X$ of instances
- A distribution $D$ over $X$ 
- A prediction function $f: X \to [0,1]$ mapping instances to predicted probabilities
- Labels $\mu_D(x) \in [0,1]$ representing the true conditional probability for instance $x$

The goal is to find a calibrated prediction function $g$ that minimizes the **calibration distance**, defined as the cost of transporting mass from predicted values to true values in probability space.

The sequential aspect refers to the horizon length—the number of time steps or samples required to achieve a target calibration error (e.g., Expected Calibration Error, ECE).

## Key Equations

**Calibration Distance (Transportation Cost):**
$$\text{CalDist}_D(f) = \min_{\pi} \mathbb{E}_{x \sim D}[\|f(x) - g(x)\|]$$

where the minimum is over all recalibration functions $g$, viewed as an optimal transport problem.

**Expected Calibration Error (ECE):**
$$\text{ECE}_\epsilon = \text{minimum horizon length } T \text{ such that } \mathbb{E}[\text{CalDist}] \leq \epsilon$$

From Hart's result (cited in the source):
$$\text{Horizon length} = O(1/\epsilon^3) \text{ for achieving } \epsilon\text{-calibration}$$

**Cost Lower Bound (from partition analysis):**
$$\text{Cost per partition} \geq \Omega(1/k^2) \times \text{size of partition}$$
$$\text{Total cost over all partitions} \geq \Omega(1/k)$$

where $k$ is the number of distinct prediction values.

## Physical Intuition / Derivation

### The Transportation Perspective

Calibration can be understood geometrically. Imagine points on the probability line $[0,1]$:
- **Predicted values** $f(x)$ are positioned at specific locations
- **True values** $\mu_D(x)$ are at different locations
- **Mass** at each location is proportional to $D(x)$

Calibration requires moving (transporting) predicted masses to align with true values. The cost is the weighted distance moved.

### Sequential Bottleneck

The sequential aspect introduces a key challenge: **sample complexity**. To distinguish between different calibration scenarios, one must observe enough samples to:

1. **Detect rare events**: If predictions at two values are separated by $\Omega(1/k)$, and you have $l$ instances in a partition, you must move at least $l/2$ predictions by this distance.

2. **Overcome collision thresholds**: From the source material's example with domain $X = \{x_-, x_+\} \cup \{x_1, \ldots, x_k\}$:
   - Two calibration scenarios differ fundamentally, but are indistinguishable until a collision occurs in the sample
   - This requires $\Omega(\sqrt{|X|})$ sample size to reliably distinguish

### The Pure vs. Mixed Case Example

The source illustrates this with two distributions:

**Pure case** (all predictions 1/2): 
$$\text{CalDist}_D(f) = \frac{1}{4}|1/3 - 1/2| + \frac{1}{4}|2/3 - 1/2| = \frac{1}{12}$$

**Mixed case** (predictions randomly 0 or 1):
$$\text{CalDist}_D(f) \approx \frac{1}{24} + O(1/\sqrt{k})$$

The $\Omega(1)$ gap persists despite being indistinguishable with fewer than $\sqrt{k}$ samples, establishing a fundamental lower bound.

## Applications in Engineering

### 1. **Machine Learning Model Validation**
- Ensuring that neural networks outputting confidence scores reflect true success rates
- Calibrating medical risk prediction models where predicted probabilities must match actual outcome frequencies
- Adjusting temperature scaling or other post-hoc calibration methods over time

### 2. **Autonomous Systems & Robotics**
- Sequential prediction of task success rates; robots must learn when confidence levels truly match execution reliability
- Safety-critical systems where miscalibration can lead to inappropriate fallback actions

### 3. **Weather Forecasting & Climate Science**
- Long-horizon sequential forecasts must maintain calibration across multiple prediction horizons
- Assessing whether predicted probabilities of precipitation match observed frequencies

### 4. **Finance & Risk Management**
- Calibrating credit risk models for loan default prediction
- Sequential adjustment of volatility forecasts to match realized returns
- Ensuring that Value-at-Risk (VaR) predictions match actual tail event frequencies

### 5. **Information Retrieval & Ranking**
- Search engines must calibrate ranking scores so that "relevance" scores match click-through rates
- Ad bidding systems where predicted click probabilities drive revenue allocation

## Common Mistakes / Pitfalls

### 1. **Confusing Calibration with Accuracy**
A model can be well-calibrated but inaccurate (e.g., always predicting 0.7 and observing 0.7 outcomes is calibrated but useless). Conversely, an accurate model is not necessarily calibrated.

### 2. **Ignoring Sample Complexity**
Practitioners often assume calibration can be verified with small samples. The lower bound $\Omega(\sqrt{|X|})$ or $\Omega(1/\epsilon^3)$ shows this is false—adequate sample sizes scale with domain size and desired precision.

### 3. **Assuming Recalibration is "Free"**
Post-hoc recalibration (e.g., Platt scaling, isotonic regression) introduces its own error if applied naively. Sequential recalibration must account for computational cost of moving predictions in probability space.

### 4. **Neglecting Temporal Dependencies**
Sequential calibration assumes labels can be exchangeable in some sense. In truly non-stationary