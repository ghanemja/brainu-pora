# Facility Location

## Definition

**Facility location** is a combinatorial optimization problem concerned with determining the optimal placement of facilities (service centers, warehouses, manufacturing plants, etc.) to minimize total cost while satisfying demand from distributed customers or users.

In its most general form, the problem asks: *Given a set of potential facility sites and a set of demand points, which facilities should be opened and how should demand be routed to minimize the sum of facility opening costs and demand service costs?*

The problem typically involves:
- **Decision variables**: which facilities to open and how much demand each facility serves
- **Objective**: minimize total cost (opening costs + service/transportation costs)
- **Constraints**: all demand must be satisfied; service capacity limitations; facility opening constraints

In recent contexts (as noted in the source material), **consistent facility location** extends the classical formulation to dynamic/online settings where facilities and demand evolve over time, requiring that facility configurations remain stable to avoid downstream disruption to dependent systems.

## Key Equations

### Classical Facility Location (Static)

Let:
- $F$ = set of potential facility locations, $|F| = m$
- $D$ = set of demand points, $|D| = n$
- $f_i$ = fixed cost to open facility $i \in F$
- $c_{ij}$ = cost to serve demand point $j$ from facility $i$
- $d_j$ = demand at point $j$
- $y_i \in \{0,1\}$ = binary indicator (facility $i$ open)
- $x_{ij} \geq 0$ = amount of demand $j$ served by facility $i$

**Objective:**
$$\min \sum_{i \in F} f_i y_i + \sum_{i \in F} \sum_{j \in D} c_{ij} x_{ij}$$

**Constraints:**
$$\sum_{i \in F} x_{ij} = d_j \quad \forall j \in D$$
$$x_{ij} \leq d_j y_i \quad \forall i \in F, j \in D$$
$$y_i \in \{0,1\}, \quad x_{ij} \geq 0$$

### Consistent/Low-Recourse Extension

For online/dynamic facility location, introduce:
- $\mathbf{S}_t$ = solution (facility configuration) at time $t$
- **Recourse cost** = penalty for changes between consecutive solutions

$$\text{Cost}_t = \text{(service cost at time } t) + \lambda \cdot \text{Recourse}(\mathbf{S}_t, \mathbf{S}_{t-1})$$

where $\lambda$ weights stability relative to service quality. Recourse is typically measured as the Hamming distance or number of facility state changes between consecutive time steps.

## Physical Intuition / Derivation

### Why Facility Location Matters

Imagine a retail company deciding where to place warehouses to serve stores across a country. Opening each warehouse costs money (rent, equipment, staffing), but it reduces transportation costs by serving nearby stores. The tension is fundamental:
- **Open many facilities** → low transportation cost, but high facility costs
- **Open few facilities** → low facility costs, but long transportation routes and high delivery costs

The facility location problem finds the Pareto-optimal trade-off.

### Why Consistency/Low Recourse Matters

In static settings, we solve once and ship it. But real systems change:
- **Customer demand** shifts seasonally or over time
- **Competitor facilities** open or close
- **New data arrives** that improves demand forecasts

A naive approach: re-optimize from scratch every time conditions change. But consider downstream impacts:

1. **Feature Engineering / ML Systems** (from source): If features derived from facility locations (e.g., which warehouse serves which region) change abruptly, all downstream machine learning models trained on those features must be retrained—a massive cost at scale.

2. **Operational Continuity**: Supply chains, inventory flows, and employee assignments all depend on facility configurations. Frequent wholesale changes introduce operational chaos.

3. **System Reliability**: In biometrics or image processing (per source), consistent low-dimensional representations ensure stable identification and recognition. High recourse = flickering outputs = unreliable systems.

**Key insight**: The value of a solution has two components:
$$\text{Value} = \text{(Optimality)} - \text{(Stability Cost)}$$

A solution that is slightly suboptimal but stable may be far more valuable than a "perfect" solution that changes constantly.

### Derivation of Consistency Metrics

**Recourse** (number of facility changes):
$$R(\mathbf{S}_t, \mathbf{S}_{t-1}) = \sum_{i \in F} |y_i^{(t)} - y_i^{(t-1)}|$$

**Consistency ratio** (in competitive analysis):
$$\text{CR} = \frac{\text{Cost}_{\text{consistent}}(t) + \lambda \cdot R(t)}{\text{Cost}_{\text{optimal}}(t)}$$

A low CR indicates that constraining the algorithm to remain consistent does not significantly degrade solution quality.

## Applications in Engineering

### 1. **Supply Chain & Logistics**
- Warehouse location optimization: minimize sum of facility opening costs and shipping distances
- Distribution network design: determine hub locations in transportation networks
- Last-mile delivery: routing from regional fulfillment centers to customers

### 2. **Feature Engineering & Machine Learning**
- **Low-rank approximation** (per source): selecting principal components or feature subsets that remain stable as data evolves, reducing retraining costs
- Data deduplication for foundation models: clustering-based facility location identifies representative samples without churn
- Dimensionality reduction: consistent feature bases reduce downstream model instability

### 3. **Biometric & Image Processing Systems** (per source)
- Fingerprint/iris recognition: maintain stable low-dimensional representations of biometric templates to ensure reliable identification
- Object detection & facial recognition: consistent feature spaces prevent flickering detections as new data arrives

### 4. **Data Compression & Signal Processing**
- Maintain stable reduced representations (e.g., codebook design in VQ) that preserve essential structure while controlling noise propagation

### 5. **Information Retrieval & Text Mining**
- Stable TF-IDF or embedding-based