---
source: pora
chapter: 13
layer: E
kind: classical
tags: [pora, robot-autonomy, classical]
---
# Monte Carlo localization

Particle-filter localization that can recover from being lost or placed at an unknown starting pose.

<!-- pora:begin -->
## In Principles of Robot Autonomy

- Read: [Chapter 13: Robot Localization](https://porabook.com/book/robot-localization/)
- Stack layer: Estimation & mapping · classical
- Run: [Particle Filter Localization](https://colab.research.google.com/github/StanfordASL/pora-exercises/blob/main/ch13/exercises/particle_filter_localization.ipynb) ([source](https://github.com/StanfordASL/pora-exercises/blob/main/ch13/exercises/particle_filter_localization.ipynb))

### Key ideas

1. Monte Carlo localization is a particle filter over robot pose in a known map: sample motion, weight by p(z | x, map) such as a likelihood-field or beam model, then resample.
2. Initializing particles uniformly over free space solves global localization, since the filter can represent many hypotheses until measurements disambiguate them.
3. To recover from kidnapping or particle collapse, inject a small fraction of random particles, as in augmented MCL, when average measurement likelihood drops suddenly.

Try it: On a 1-D corridor of length 10 with doors at 2, 5, and 8, run MCL with particles initialized uniformly; plot the particle histogram after each door sighting as the robot moves right.

Needs first: [[Particle_filter]], [[Probabilistic_motion_and_sensor_models]]

Part of [[Principles_of_Robot_Autonomy]]. Summary and study notes from the unofficial PoRA Atlas; the book is the authoritative reference.
<!-- pora:end -->
