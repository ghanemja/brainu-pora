---
video: py5byOOHZM8 | CNN: Convolutional Neural Networks Explained - Computerphile | Computerphile | 14:17
---
## Filters the network learns for itself

A **convolutional layer** slides small kernels over the image, exactly like classical filtering, except the kernel weights are learned by gradient descent instead of designed by hand. Each kernel produces one output channel, a map of where its pattern appears.

Two properties make this the right layer for images:

- **Weight sharing**: the same kernel is used at every position, so the layer has very few parameters.
- **Translation equivariance**: shift the input and the output shifts the same way, so a pattern is detected wherever it appears.

## Worked example: sizes and parameter counts

The output width of a convolution with input width $W$, kernel $K$, padding $P$ and stride $S$ is

$$W_{\text{out}} = \left\lfloor \frac{W - K + 2P}{S} \right\rfloor + 1$$

Take a $224 \times 224 \times 3$ image and 64 kernels of size $3 \times 3$, with padding 1. With stride 1, the output is $224 \times 224 \times 64$; with stride 2 it's $\lfloor 223/2 \rfloor + 1 = 112$ wide. The weights number $3 \cdot 3 \cdot 3 \cdot 64 + 64 = 1792$, whatever the image size. A dense layer mapping the same image to just 64 outputs would need $224 \cdot 224 \cdot 3 \cdot 64 \approx 9.6$ million.

## Depth builds up the receptive field

One $3 \times 3$ layer sees a $3 \times 3$ patch. Stack two and each output sees $5 \times 5$; three, $7 \times 7$. Pooling or stride-2 layers halve the resolution and grow the view much faster.

So networks learn a hierarchy. Early layers learn edge and color detectors much like Sobel filters; middle layers combine them into textures and parts; deep layers respond to whole objects such as wheels, faces and cars.

## A typical architecture

A classification CNN repeats convolution, normalization and ReLU blocks, halving the size and adding channels, then ends with a small classifier. **ResNets** add skip connections, $y = x + F(x)$, so very deep networks still train. For detection or segmentation, the same convolutional part (the **backbone**) feeds a task-specific **head**.

Robots usually fine-tune a backbone **pretrained** on millions of images.

> **Common mistake:** assuming a CNN handles rotation and scale the way it handles shifts. Convolution is equivariant only to translation. A network that has only seen upright objects at one size will struggle with rotated or much smaller ones, unless training data covers them (data augmentation).
