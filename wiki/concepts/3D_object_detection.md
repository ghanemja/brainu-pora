---
source: pora
chapter: 10
layer: S
kind: learned
tags: [pora, robot-autonomy, learned]
---
# 3D object detection

Predict oriented 3D boxes from point clouds or voxels, which is what a planner needs to reason about other agents.

<!-- pora:begin -->
## In Principles of Robot Autonomy

- Read: [Chapter 10: Object Detection and Recognition](https://porabook.com/book/object-detection/)
- Stack layer: Perception · learned

### Key ideas

1. 3D detectors predict oriented boxes (x, y, z, length, width, height, yaw) plus class, which gives a planner the position, size and heading of agents in metric space.
2. Lidar-based methods operate on voxels or pillars (VoxelNet, SECOND, PointPillars) or directly on points; many use a bird's-eye-view (BEV) representation where objects rarely overlap and scale does not shrink with distance.
3. Camera-only 3D detection must infer depth from monocular cues or multi-view geometry and is less accurate in range; fusion with lidar or radar combines dense semantics with metric depth.

Try it: Project a synthetic lidar point cloud of two boxes onto a 0.2 m BEV occupancy grid in NumPy and plot max height per cell.

Needs first: [[Object_detection_and_recognition]], [[Point_cloud_and_voxel_networks]]

Part of [[Principles_of_Robot_Autonomy]]. Summary and study notes from the unofficial PoRA Atlas; the book is the authoritative reference.
<!-- pora:end -->
