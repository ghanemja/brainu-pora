---
video: hUVyDabn1Mg | Simple Stereo | Camera Calibration | First Principles of Computer Vision | 16:34
---
## Rectify, then search one row

A stereo rig is two calibrated cameras a fixed distance apart, the **baseline** $b$. First, **rectification** warps both images so their epipolar lines become the same horizontal rows. Then a point at row $v$ in the left image appears at row $v$ in the right image, shifted left by the **disparity**

$$d = u_{\text{left}} - u_{\text{right}}$$

Finding matches is now a 1-D search along each row, which makes it possible to compute a disparity for every pixel at video rate.

## Depth from disparity

Similar triangles turn disparity into depth. With focal length $f$ in pixels and baseline $b$ in meters:

$$Z = \frac{f\, b}{d}$$

Large disparity means near, small disparity means far, and zero disparity means infinitely far. Once you have $Z$, the pinhole model gives $X = (u - c_x) Z / f$ and $Y = (v - c_y) Z / f$, so every matched pixel becomes a 3-D point.

## Worked example: how accuracy falls with range

A rig has $f = 700$ px and $b = 0.12$ m, so $f b = 84$ px·m.

- A disparity of 42 px gives $Z = 84 / 42 = 2$ m. A disparity of 4.2 px gives $Z = 20$ m.
- The sensitivity is $|dZ/dd| = Z^2 / (f b)$. At 2 m, a one-pixel matching error moves the depth by $4 / 84 \approx 0.05$ m. At 20 m, the same one-pixel error moves it by $400 / 84 \approx 4.8$ m.

Ten times farther gives a hundred times worse depth. Depth error grows with the **square** of distance.

## Finding the match

**Block matching** compares a small window around each left pixel with windows along the same row in the right image, scoring with the sum of absolute or squared differences, and keeps the best disparity. It fails where the window has no texture (blank walls), on repeated patterns, and at **occlusions**, where a point is visible in one camera only. **Semi-global matching** adds a smoothness preference across neighboring pixels, and learned stereo networks do better still on hard surfaces.

## Choosing the baseline

A longer baseline makes disparity larger for the same depth, so far-away depth is more accurate. But it also makes the two views more different, so matching gets harder, more points are occluded, and close objects may fall out of one camera's view. Small rigs suit indoor robots; cars use wider ones.

> **Common mistake:** quoting a stereo camera's depth accuracy as one number. It holds at one distance only. Always ask "at what range?", and don't use stereo depth far beyond the range it was designed for.
