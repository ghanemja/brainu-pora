---
video: pwoUySMYUlM | Deep Learning with Point Clouds | Deep Learning for 3D Object Detection, Part 3 | MATLAB | 11:49
---
## What a planner needs from perception

A 2-D box in an image says where something appears, not where it is. A planner needs objects in metric space, so a **3-D detector** outputs an oriented box for each object:

$$(x,\ y,\ z,\ l,\ w,\ h,\ \theta)$$

That's the center, the size (length, width, height), and the **yaw** $\theta$, the heading around the vertical axis, plus a class and a score. Many detectors also predict velocity. With this, a planner knows how far away a car is, how much room it takes up, and which way it's pointing.

## Detecting in the lidar point cloud

Most accurate 3-D detectors use lidar. Typical pipelines turn the points into a grid with voxel or pillar networks (VoxelNet, SECOND, PointPillars), compress it to a 2-D feature map seen from above, and run a detection head on it. Anchor-based heads regress boxes from preset car or pedestrian shapes. Center-based heads such as CenterPoint predict a heatmap of object centers, then regress size and yaw at each peak.

## Why the bird's-eye view works

Seen from above, objects on a road almost never overlap, and an object's size on the grid doesn't depend on its distance: a car is about $4.5 \times 1.8$ m whether it's 5 m or 50 m away. That's the opposite of a camera image, where far objects shrink and near ones hide others. The planner also reasons in this top-down view, so detections arrive in the form it needs.

## Worked example: corners of a box

A car is detected at center $(10, 5)$ m with $l = 4.5$ m, $w = 1.8$ m and yaw $\theta = 30°$. Each corner is the center plus the rotated half-size offset $(\pm l/2,\ \pm w/2) = (\pm 2.25,\ \pm 0.9)$. For the front-left corner:

$$x = 10 + 2.25\cos 30° - 0.9 \sin 30° \approx 11.50, \qquad y = 5 + 2.25 \sin 30° + 0.9 \cos 30° \approx 6.90$$

The other corners are $(12.40, 5.35)$, $(8.50, 3.10)$ and $(7.60, 4.65)$. Collision checks use these four points.

## Cameras, and fusing sensors

Camera-only 3-D detection must infer depth, from object size, from where an object meets the ground, or from several overlapping cameras. It's cheap and sees color and texture, but depth error grows quickly with range. Lidar gives precise depth but is sparse at long range and sees no color. Radar measures speed directly and works in rain and fog. **Fusion** combines them, either by merging each sensor's detections or by merging features inside the network.

> **Common mistake:** ignoring the 180° heading ambiguity. A box with yaw $\theta$ and one with $\theta + 180°$ cover exactly the same space, so the box IoU looks perfect, but a tracker reading the heading predicts the car driving backwards. Check heading separately.
