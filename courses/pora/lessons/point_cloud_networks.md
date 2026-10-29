---
video: Cge-hot0Oc0 | PointNet: Deep Learning on Point Sets for 3D Classification and Segmentation | ComputerVisionFoundation Videos | 11:24
---
## Why point clouds are awkward for networks

A lidar scan is a list of $N$ points, each with $(x, y, z)$ and often intensity. Three things make it unlike an image:

- **No order.** The same scan can be listed in any order; the network's answer must not change.
- **Irregular.** Points aren't on a grid, so there's no "neighbor to the right" for a convolution kernel.
- **Uneven density.** Near objects get thousands of points, far ones a handful, and most of space is empty.

So image-style convolution doesn't apply directly. The main answers are point-based networks, and grids (voxels or pillars).

## PointNet: shared MLP, then max-pool

**PointNet** handles order with a symmetric function. A small network $h$, the same for every point, maps each point to a feature vector. Then an element-wise **max** across all points pools them into one global feature, and a final network $\gamma$ produces the output:

$$f(\{x_1, \dots, x_N\}) = \gamma\Big( \max_{i} \, h(x_i) \Big)$$

Max doesn't care about order, so neither does $f$. For segmentation, the global feature is attached back to each point's own feature to label every point.

## Worked example: order doesn't matter

Three points give per-point features $h(x_1) = (0.2, 0.9)$, $h(x_2) = (0.7, 0.1)$ and $h(x_3) = (0.4, 0.5)$. Max-pooling each dimension gives

$$\max = (0.7,\ 0.9)$$

List the points as $x_3, x_1, x_2$ and the result is identical. Only $x_2$ (first entry) and $x_1$ (second entry) affect the output; $x_3$ could move a little and nothing would change. PointNet's answer depends on a small set of **critical points**, which makes it robust to missing points.

## Local structure: PointNet++

Plain PointNet looks at each point alone and then at everything at once, so it misses local shape such as the corner of a car. **PointNet++** works hierarchically: pick well-spread centers (farthest point sampling), group the neighbors within a radius of each, run a mini-PointNet on each group, and repeat on the centers. That gives growing receptive fields, much like a CNN.

## Voxels and pillars

The other route puts points on a grid. **Voxel** methods divide space into small 3-D cells and use 3-D convolutions; since most voxels are empty, **sparse** convolutions compute only where there are points. **PointPillars** uses vertical columns instead: a small PointNet summarizes the points in each pillar, which yields a 2-D bird's-eye-view image that fast 2-D CNNs can process. That's a common choice for real-time lidar detection.

> **Common mistake:** feeding points to an ordinary MLP in whatever order the sensor returned them. The same scene in a different order gives a different answer, and the network ends up learning the sensor's scan pattern instead of the scene.
