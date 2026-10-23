---
source: pora
chapter: 15
layer: E
kind: classical
tags: [pora, robot-autonomy, classical]
---
# Object tracking & data association

Follow detected objects over time, deciding which new detection belongs to which existing track.

<!-- pora:begin -->
## In Principles of Robot Autonomy

- Read: [Chapter 15: Sensor Fusion and Object Tracking](https://porabook.com/book/sensor-fusion/)
- Stack layer: Estimation & mapping · classical

### Key ideas

1. Each track has its own filter (often a Kalman filter with a constant-velocity model) that predicts where the object will be when the next detections arrive.
2. Data association matches detections to tracks, e.g. by gating with Mahalanobis distance and solving the assignment with the Hungarian algorithm on a cost matrix; JPDA and MHT handle ambiguity probabilistically.
3. Track management births tracks from unmatched detections and deletes tracks that go unmatched for several frames, trading false tracks against missed objects.

Try it: Given 3 track predictions and 3 detections in 2-D, build the 3x3 Euclidean cost matrix and solve it with scipy.optimize.linear_sum_assignment; then perturb one detection to see when the assignment flips.

Needs first: [[Kalman_filter]], [[Object_detection_and_recognition]]

Related: [[Sensor_fusion]]

Part of [[Principles_of_Robot_Autonomy]]. Summary and study notes from the unofficial PoRA Atlas; the book is the authoritative reference.
<!-- pora:end -->
