---
source: pora
chapter: 8
layer: S
kind: classical
tags: [pora, robot-autonomy, classical]
---
# Feature detection & matching

Find distinctive image points and describe them so the same point can be matched across views, as SIFT does.

<!-- pora:begin -->
## In Principles of Robot Autonomy

- Read: [Chapter 8: Classical Methods for Perception](https://porabook.com/book/classical-perception/)
- Stack layer: Perception · classical
- Run: [SIFT Feature Matching](https://colab.research.google.com/github/StanfordASL/pora-exercises/blob/main/ch06/sift_feature_matching.ipynb) ([source](https://github.com/StanfordASL/pora-exercises/blob/main/ch06/sift_feature_matching.ipynb))

### Key ideas

1. Good features are distinctive and repeatable: corners (Harris, FAST) have strong gradients in two directions, unlike flat regions or edges where a patch can slide without changing.
2. A descriptor summarizes the local patch; SIFT detects scale-space extrema of difference-of-Gaussians, assigns a dominant orientation, and builds a 128-D histogram of gradient orientations, giving scale and rotation invariance.
3. Matching uses nearest neighbors in descriptor space; Lowe's ratio test keeps a match only if the best distance is clearly smaller than the second-best, and RANSAC then rejects geometric outliers.

Try it: Compute the Harris response det(M) - k·trace(M)^2 on a synthetic image containing a square in NumPy, and verify it is high at corners, negative on edges, near zero in flat areas.

Needs first: [[Image_filtering_and_convolution]]

Unlocks: [[Structure_from_motion]], [[Classical_visual_recognition]], [[SLAM_front_end]]

Part of [[Principles_of_Robot_Autonomy]]. Summary and study notes from the unofficial PoRA Atlas; the book is the authoritative reference.
<!-- pora:end -->
