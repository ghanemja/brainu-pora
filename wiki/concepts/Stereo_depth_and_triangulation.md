---
source: pora
chapter: 7
layer: S
kind: classical
tags: [pora, robot-autonomy, classical]
---
# Stereo depth & triangulation

Recover depth from disparity between two calibrated cameras.

<!-- pora:begin -->
## In Principles of Robot Autonomy

- Read: [Chapter 7: Stereo Vision and Structure From Motion](https://porabook.com/book/stereo-vision/)
- Stack layer: Perception · classical
- Watch: [AA174A lecture 9: Stereo Vision](https://youtu.be/idD08N4rgJU)

### Key ideas

1. After rectification, corresponding points lie on the same image row, so matching becomes a 1D search along that row for the disparity d = u_left - u_right.
2. For rectified cameras with focal length f (pixels) and baseline b, depth is Z = f b / d: large disparity means near, small disparity means far.
3. Since dZ/dd = -Z^2/(f b), a fixed one-pixel disparity error causes depth error that grows quadratically with distance; longer baselines improve far accuracy but make matching harder.

Try it: Plot Z = f b / d for d = 1..100 px with f = 700, b = 0.12 and overlay the depth uncertainty for ±0.5 px of disparity error.

Needs first: [[Epipolar_geometry]]

Unlocks: [[Structure_from_motion]]

Part of [[Principles_of_Robot_Autonomy]]. Summary and study notes from the unofficial PoRA Atlas; the book is the authoritative reference.
<!-- pora:end -->
