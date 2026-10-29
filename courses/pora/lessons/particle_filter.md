---
video: YBeVDxTHiYM | Particle Filter - 5 Minutes with Cyrill | Cyrill Stachniss | 5:12
video: BfKEf2s7Y80 | The Particle Filter: A Full Tutorial | James Han | 6:19
---
## A belief made of samples

A **particle filter** represents the belief with $M$ samples, called **particles**, $x^{[1]}, \dots, x^{[M]}$, each a concrete guess of the state. Where the belief is high, particles are dense; where it's low, they're sparse or absent.

Unlike a Kalman filter, nothing forces the belief to be Gaussian. Particles can form two clusters for two hypotheses, a banana shape after a turn, or anything else, and nonlinear models are no problem: you just push each particle through them. More particles give a better approximation, at more compute.

## The loop: move, weight, resample

At each step, for every particle:

- **Sample** a new state from the motion model, $x_t^{[m]} \sim p(x_t \mid u_t, x_{t-1}^{[m]})$, so noise is added randomly per particle.
- **Weight** it by how well it explains the measurement, $w^{[m]} \propto p(z_t \mid x_t^{[m]})$.

Then **resample**: draw $M$ new particles from the current set, each picked with probability proportional to its weight. Likely particles get copied, unlikely ones die out, and all weights reset to equal.

## Worked example: four particles

Particles sit at $x = 1, 2, 3, 4$ m. A range sensor reads $z = 2.9$ m with Gaussian noise $\sigma = 0.5$ m, so each particle's likelihood is $e^{-(x - 2.9)^2 / (2 \cdot 0.25)}$:

- Likelihoods: $0.0007$, $0.198$, $0.980$, $0.089$. Their sum is about $1.27$.
- Normalized weights: about $0.001$, $0.16$, $0.77$, $0.07$.
- Weighted mean: $\sum w^{[m]} x^{[m]} \approx 2.91$ m.

After resampling, most of the four new particles are copies of the one at 3 m, and the one at 1 m almost surely disappears.

## Resampling has a cost

Resampling focuses particles in likely regions, but it also throws away diversity. Repeat it too often and all particles become copies of a few ancestors: **particle deprivation**, with no particles left near the truth if the filter was wrong. Two standard fixes:

- **Low-variance resampling** draws all $M$ samples with one random number and evenly spaced pointers, so it doesn't lose particles by chance.
- Resample only when the **effective sample size** $N_{\text{eff}} = 1 / \sum_m (w^{[m]})^2$ drops below, say, $M/2$. In the example, $N_{\text{eff}} \approx 1.6$ out of 4, so it's time to resample.

## How many particles?

Enough to have some near the truth after every motion step. That grows quickly with the dimension of the state and the spread of the belief: a few hundred particles may track a robot's pose well once it's localized, while thousands may be needed to find it in a large building from scratch. Particle filters suit low-dimensional, multimodal problems, not large states such as whole maps.

> **Common mistake:** a sensor model that's too confident. If the likelihood is very sharp, one particle takes nearly all the weight every step and the cloud collapses. Inflating the measurement noise above the sensor's datasheet value often makes the filter work better.
