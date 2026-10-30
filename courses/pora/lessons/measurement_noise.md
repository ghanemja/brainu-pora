---
video: hRAFPdDppzs | What's the difference between accuracy and precision? | TED-Ed | 4:53
video: VIvYxnhkvvc | What is Gaussian Noise? | Iain Explains Signals, Systems, and Digital Comms | 5:55
---
## Two kinds of error

The book splits sensor error in two:

- **Systematic error (bias)** is repeatable: a miscalibrated range sensor that always reads 3 cm long. If you can model it, you can subtract it; averaging never removes it.
- **Random error (noise)** changes every reading and can't be predicted, only described with a probability distribution.

A standard model puts both in one line:

$$z = h(x) + b + v, \qquad v \sim \mathcal{N}(0, R)$$

Here $h(x)$ is what a perfect sensor would read, $b$ is the bias, and $v$ is zero-mean Gaussian noise with variance $R$ (written $\sigma^2$ for a single reading). In everyday terms, bias hurts **accuracy** and noise hurts **precision**.

## Averaging and integrating

Average $N$ independent readings and the noise's standard deviation shrinks by $\sqrt N$: 100 readings are 10 times less noisy than one. The opposite happens when you *integrate* a noisy rate: the error does a random walk and its standard deviation grows like $\sqrt t$. That's why odometry gets worse the longer you drive.

## Trust each sensor by its variance

Two independent sensors measure the same quantity, with variances $\sigma_A^2$ and $\sigma_B^2$. The best combination (the one with the smallest variance) weights each reading by the *inverse* of its variance:

$$\hat z = \frac{z_A/\sigma_A^2 + z_B/\sigma_B^2}{1/\sigma_A^2 + 1/\sigma_B^2}, \qquad \sigma^2_{\text{fused}} = \frac{1}{1/\sigma_A^2 + 1/\sigma_B^2}$$

The fused estimate always has a smaller variance than either sensor alone. This one formula is the heart of the Kalman filter, coming up in the estimation lessons.

## Worked example

Sensor A reads 2.00 m with $\sigma_A = 1$ cm; sensor B reads 2.03 m with $\sigma_B = 2$ cm. The inverse variances are $1$ and $1/4$, so the weights are $\tfrac{1}{1.25} = 0.8$ and $\tfrac{0.25}{1.25} = 0.2$:

$$\hat z = 0.8 \times 2.00 + 0.2 \times 2.03 = 2.006\ \text{m}, \qquad \sigma^2_{\text{fused}} = \frac{1}{1.25} = 0.8\ \text{cm}^2$$

so the fused standard deviation is about $0.89$ cm, better than A's 1 cm.

> **Common mistake:** weighting by $1/\sigma$ instead of $1/\sigma^2$. That would give 2/3 and 1/3 here, and trusts the noisy sensor too much.
