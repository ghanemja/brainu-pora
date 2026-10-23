---
source: pora
chapter: 10
layer: S
kind: learned
tags: [pora, robot-autonomy, learned]
---
# Semantic & instance segmentation

Label every pixel or point by class, and separate individual objects of the same class.

<!-- pora:begin -->
## In Principles of Robot Autonomy

- Read: [Chapter 10: Object Detection and Recognition](https://porabook.com/book/object-detection/)
- Stack layer: Perception · learned

### Key ideas

1. Semantic segmentation assigns a class to every pixel; instance segmentation also separates individual objects of the same class; panoptic segmentation combines both for 'stuff' and 'things'.
2. Fully convolutional networks with encoder-decoder structure (FCN, U-Net with skip connections, DeepLab with dilated convolutions) recover per-pixel predictions at full resolution while using deep context.
3. Mask R-CNN extends Faster R-CNN with a small mask head per detected box, giving instance masks; accuracy is measured with per-class IoU, averaged as mIoU.

Try it: Given a NumPy array of predicted and ground-truth label maps, write a function computing per-class IoU and mIoU, and test it on a small hand-made 6×6 example.

Needs first: [[Convolutional_neural_networks]]

Part of [[Principles_of_Robot_Autonomy]]. Summary and study notes from the unofficial PoRA Atlas; the book is the authoritative reference.
<!-- pora:end -->
