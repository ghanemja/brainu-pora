---
source: pora
chapter: 14
layer: E
kind: classical
tags: [pora, robot-autonomy, classical]
---
# SLAM front end

The perception side of SLAM: extract features, associate them with landmarks, reject outliers, and detect loop closures before any estimation runs.

<!-- pora:begin -->
## In Principles of Robot Autonomy

- Read: [Chapter 14: Simultaneous Localization and Mapping (SLAM)](https://porabook.com/book/slam/)
- Stack layer: Estimation & mapping · classical

### Key ideas

1. The front end turns raw sensor data into abstract constraints: detect and describe features (e.g. ORB keypoints), match them or register scans (ICP), and output relative pose measurements.
2. Data association decides which observation corresponds to which landmark; gating by Mahalanobis distance and RANSAC on geometric models reject outliers before they reach the estimator.
3. Loop closure detection recognizes a previously visited place (e.g. via bag-of-words appearance matching); a single false loop closure can badly warp the map, so verification is critical.

Try it: Generate 20 2-D point correspondences under a known rotation and translation, corrupt 6 with random outliers, and fit the transform with a simple RANSAC loop using 2-point samples and SVD.

Needs first: [[Feature_detection_and_matching]], [[Point_cloud_registration_ICP]]

Unlocks: [[Graph_and_factor-graph_SLAM]]

Part of [[Principles_of_Robot_Autonomy]]. Summary and study notes from the unofficial PoRA Atlas; the book is the authoritative reference.
<!-- pora:end -->
