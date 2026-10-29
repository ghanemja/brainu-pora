---

---
## A Bayes filter on a grid

The Bayes filter is exact but abstract: it needs a probability for every possible state. The **histogram filter** makes that concrete by chopping the state space into a finite number of cells $k = 1, \dots, K$ and keeping one probability per cell:

$$\mathrm{bel}(x_t) \approx (p_{1,t},\ p_{2,t},\ \dots,\ p_{K,t}), \qquad \sum_k p_{k,t} = 1$$

The belief is just a vector. It can have any shape, including several peaks, so it handles ambiguous situations such as a hallway with identical doors that a single Gaussian can't represent.

## Predict: shift and blur

The integral in the Bayes filter's prediction step becomes a sum over cells:

$$\bar p_{k,t} = \sum_i p(x_t = k \mid u_t,\ x_{t-1} = i)\; p_{i,t-1}$$

That's a matrix times a vector. When motion works the same everywhere ("move one cell right, give or take"), it's a **convolution**: shift the histogram by the commanded motion, then blur it by the motion noise. Uncertainty grows.

> **Common mistake:** cells larger than one step of motion. At 3 cm per update on a 10 cm grid, a rounded shift moves the belief zero cells every time, so the filter thinks the robot never moves.

## Correct: multiply and normalize

The measurement update is element-wise. Multiply each cell by how likely the measurement would be from there, then rescale so the cells sum to 1:

$$p_{k,t} = \eta\; p(z_t \mid x_t = k)\; \bar p_{k,t}$$

Cells consistent with what the robot sees grow; the rest shrink. No Jacobians, no Gaussians, no approximations beyond the grid itself.

## Worked example: two doors in five cells

A circular hallway has 5 cells, with doors at cells 0 and 1. The sensor reports "door" with probability $0.6$ at a door and $0.2$ elsewhere. Start uniform at $0.2$.

- Sense "door": multiply to $(0.12, 0.12, 0.04, 0.04, 0.04)$, normalize to $(0.33, 0.33, 0.11, 0.11, 0.11)$.
- Move one cell right (exactly): $(0.11, 0.33, 0.33, 0.11, 0.11)$.
- Sense "door" again: multiply to $(0.067, 0.2, 0.067, 0.022, 0.022)$, sum $0.378$, normalize to $(0.18, 0.53, 0.18, 0.06, 0.06)$.

Cell 1 now leads, since it's the only cell with a door both before and after the move.

## Exact, but only in low dimensions

The number of cells multiplies with every dimension. Localizing $(x, y, \theta)$ in a $50 \times 50$ m building with 10 cm cells and 5° heading bins takes $500 \times 500 \times 72 = 18$ million cells, updated every step. That's workable, but add velocity or a second robot and it's hopeless. Histogram filters suit 1-D to 3-D problems; beyond that, particle filters spend their effort only where probability is high.
