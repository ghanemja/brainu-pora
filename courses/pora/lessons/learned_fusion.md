---
video: OFE3tUiobPA | Simple-BEV: What Really Matters for Multi-Sensor BEV Perception? (ICRA 2023) | Adam Harley | 4:27
---
## Where to fuse: early, mid or late

Classical fusion combines estimates: each sensor detects objects separately, and a filter merges the results. That's **late fusion**. It's modular, but each sensor's detector throws away information before the merge: a camera can't see that a dim lidar return is a pedestrian's leg.

**Learned fusion** combines sensors inside a network. **Mid-level** fusion merges intermediate features from each sensor, so the network can use camera texture and lidar depth together. It usually beats late fusion on accuracy, at the cost of tighter coupling between sensors.

## A shared bird's-eye-view grid

To merge features, they have to live in the same place. The common choice is a **bird's-eye-view** (BEV) grid on the ground, centered on the vehicle: for example, $0.5$ m cells covering $100 \times 100$ m, a $200 \times 200$ grid. Every sensor's features are mapped into this grid in metric coordinates, then a CNN or transformer processes the combined grid. Lidar maps in directly, for example with pillars, since its points already have 3-D coordinates. Cameras are the hard part.

## Lifting camera features into BEV

An image pixel gives a direction but no depth, so the network has to supply it:

- **Lift-splat** methods predict, for each pixel, a probability over depth bins. The pixel's feature is spread along its ray in proportion, then summed ("splatted") into the BEV cells it passes through.
- **Attention** methods such as BEVFormer go the other way: each BEV cell projects its 3-D location into the cameras and gathers the image features found there, using attention.

Both rely on the cameras' intrinsics and extrinsics, built into the geometry.

## Worked example: where a BEV cell lands in the image

A BEV cell on the ground lies 20 m ahead and 2 m to the left of a camera mounted 1.5 m up. In the camera frame ($X$ right, $Y$ down, $Z$ forward) it is $(-2, 1.5, 20)$. With $f = 1000$ px and principal point $(800, 450)$:

$$u = 1000 \cdot \frac{-2}{20} + 800 = 700, \qquad v = 1000 \cdot \frac{1.5}{20} + 450 = 525$$

So that cell's query gathers features from around pixel $(700, 525)$. Every one of the 40,000 cells does the same for every camera that sees it.

## Handing off to the classical stack

The network's output is usually detections (3-D boxes) or an occupancy grid, ideally with confidence. Classical modules take over from there: a tracker associates detections over time with Kalman filters, and the planner reasons on the result. That boundary is where learned and classical components meet. The learned side is more accurate, but needs lots of labeled data and is harder to verify.

> **Common mistake:** letting calibration drift after training. The network learned with one set of extrinsics. If a camera gets bumped by just 1°, features land $50 \tan 1° \approx 0.87$ m off at 50 m, and objects appear doubled or in the wrong lane. Monitor calibration, and train with small perturbations.
