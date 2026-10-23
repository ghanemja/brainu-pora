---
source: pora
chapter: 15
layer: E
kind: learned
tags: [pora, robot-autonomy, learned]
---
# Learned fusion (BEV & features)

Fuse sensors inside a network, for example in a bird's-eye-view feature space, then hand the result to classical filters. Where the classical and learned halves of the stack meet.

<!-- pora:begin -->
## In Principles of Robot Autonomy

- Read: [Chapter 15: Sensor Fusion and Object Tracking](https://porabook.com/book/sensor-fusion/)
- Stack layer: Estimation & mapping · learned

### Key ideas

1. Learned fusion maps camera images and lidar points into a shared bird's-eye-view grid where features from all sensors are aligned in metric ground coordinates.
2. Camera-to-BEV lifting predicts depth or uses attention (e.g. transformer queries over image features) to place image features in 3-D, since a single image lacks direct depth.
3. The network outputs detections or occupancy with uncertainty, which classical trackers and filters then consume; mid-level feature fusion often beats fusing final detections, but it needs calibrated sensors and lots of data.

Try it: Take a pinhole camera with focal length 500 px at height 1.5 m looking level; compute where a ground point 10 m ahead projects in the image, then how far it moves in BEV if the pitch is off by 1 degree.

Needs first: [[Sensor_fusion]], [[Attention_and_vision_transformers]]

Part of [[Principles_of_Robot_Autonomy]]. Summary and study notes from the unofficial PoRA Atlas; the book is the authoritative reference.
<!-- pora:end -->
