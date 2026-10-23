---
source: pora
chapter: 9
layer: S
kind: learned
tags: [pora, robot-autonomy, learned]
---
# Attention & vision transformers

Models that relate every part of the input to every other part through attention, now common for images, point clouds, and multimodal input.

<!-- pora:begin -->
## In Principles of Robot Autonomy

- Read: [Chapter 9: Deep Learning Architectures for Perception](https://porabook.com/book/deep-learning-perception/)
- Stack layer: Perception · learned

### Key ideas

1. Self-attention computes Attention(Q, K, V) = softmax(Q K^T / √d_k) V, so each token's output is a weighted mix of all tokens' values, with weights from query-key similarity.
2. Vision transformers split an image into patches (e.g. 16×16), linearly embed each as a token, add positional embeddings, and process them with stacked attention and MLP blocks.
3. Attention gives a global receptive field in one layer but costs O(N^2) in the number of tokens and has weaker built-in spatial bias than CNNs, so ViTs typically need more data or pretraining.

Try it: Implement single-head attention in NumPy for 6 tokens of dimension 64 and compare softmax entropy with and without the 1/√d_k scaling.

Needs first: [[Neural_network]]

Unlocks: [[Learned_fusion_BEV_and_features]]

Part of [[Principles_of_Robot_Autonomy]]. Summary and study notes from the unofficial PoRA Atlas; the book is the authoritative reference.
<!-- pora:end -->
