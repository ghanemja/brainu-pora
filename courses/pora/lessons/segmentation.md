---
video: 5QUmlXBb0MY | Image Segmentation, Semantic Segmentation, Instance Segmentation, and Panoptic Segmentation | LearnOpenCV | 5:04
video: g7z4mkfRjI4 | Mask R-CNN | ComputerVisionFoundation Videos | 12:22
---
## Three kinds of segmentation

Detection draws boxes; segmentation labels pixels (or lidar points).

- **Semantic segmentation** gives every pixel a class: road, sidewalk, car, person, sky. Two people touching get one merged "person" region.
- **Instance segmentation** separates individual objects: person 1, person 2, each with its own mask.
- **Panoptic segmentation** does both. Countable **things** (cars, people) get instance masks, and amorphous **stuff** (road, grass, sky) gets class labels.

For robots, segmentation gives drivable area, free floor space, and the exact outline of obstacles, which a box can't.

## Encoder–decoder networks

A classification CNN shrinks the image as it goes, trading resolution for context. Segmentation needs both: enough context to know a pixel is part of a car, and full resolution to place the car's edge.

- **Encoder–decoder** networks shrink, then upsample back to full size.
- **U-Net** adds **skip connections** that copy fine detail from each encoder level to the matching decoder level.
- **DeepLab** uses **dilated convolutions**, kernels with gaps, to see a wide area without shrinking the feature map.

## Instance masks with Mask R-CNN

**Mask R-CNN** builds instance segmentation on top of detection. It is Faster R-CNN plus a small extra head: for each detected box, a tiny fully convolutional network predicts a mask, typically $28 \times 28$, over just that box, which is then resized to the box's size in the image. Detection separates the instances; the mask head outlines each one.

## Worked example: measuring with IoU

For each class, compare predicted pixels with the true ones. Say the true road covers 10,000 pixels, the prediction covers 9,000, and 8,500 of them overlap:

$$\text{IoU}_{\text{road}} = \frac{8500}{9000 + 10000 - 8500} = \frac{8500}{10500} \approx 0.81$$

The **mIoU** is the mean of this over all classes. Every class counts equally, so a model that is great on road but misses pedestrians gets a poor score.

## Why not just count correct pixels?

**Pixel accuracy**, the fraction of pixels labeled correctly, is dominated by the big classes. If road and sky fill 90% of every image, a model that never finds a single pedestrian can still score above 90%. For a robot, the small classes, such as people, cyclists and curbs, are often the ones that matter most.

> **Common mistake:** reporting pixel accuracy, or a single averaged number, and calling the model good. Always check per-class IoU for the classes that matter to safety. A large average can hide a class the model barely detects.
