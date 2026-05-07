# Fourier Transform

## Definition

The **Fourier transform** is a mathematical operation that decomposes a function (or signal) into its constituent frequencies. It transforms a function from the **time domain** (or spatial domain) into the **frequency domain**, representing how much of each frequency is present in the original signal.

For a function $f(t)$ of a continuous real variable, the **Fourier transform** is defined as:

$$\hat{f}(\omega) = \int_{-\infty}^{\infty} f(t) e^{-i\omega t} dt$$

The **inverse Fourier transform** recovers the original function:

$$f(t) = \frac{1}{2\pi} \int_{-\infty}^{\infty} \hat{f}(\omega) e^{i\omega t} d\omega$$

**For discrete signals** (crucial in digital signal processing), the **Discrete Fourier Transform (DFT)** is:

$$\hat{f}[k] = \sum_{n=0}^{N-1} f[n] e^{-i 2\pi kn / N}$$

where $k = 0, 1, \ldots, N-1$.

In **Boolean function analysis** (relevant to learning theory), the Fourier transform over the hypercube $\{-1,+1\}^n$ expresses a Boolean function as a sum of Fourier basis functions:

$$f(x) = \sum_{S \subseteq [n]} \hat{f}(S) \chi_S(x)$$

where $\chi_S(x) = \prod_{i \in S} x_i$ are the Fourier basis elements.

---

## Key Equations

### Parseval's Theorem
Energy is conserved between domains:
$$\int_{-\infty}^{\infty} |f(t)|^2 dt = \frac{1}{2\pi} \int_{-\infty}^{\infty} |\hat{f}(\omega)|^2 d\omega$$

### Convolution Theorem
Convolution in time becomes multiplication in frequency:
$$f(t) * g(t) \leftrightarrow \hat{f}(\omega) \cdot \hat{g}(\omega)$$

### Modulation (Frequency Shift)
$$e^{i\omega_0 t} f(t) \leftrightarrow \hat{f}(\omega - \omega_0)$$

### Differentiation Property
$$\frac{df}{dt} \leftrightarrow i\omega \hat{f}(\omega)$$

### Boolean Fourier Analysis
**Spectral Norm** (concentration of mass):
$$\|\hat{f}\|_1 = \sum_{S \subseteq [n]} |\hat{f}(S)|$$

**Influence of variable $i$**:
$$\text{Inf}_i(f) = \sum_{S: i \in S} \hat{f}(S)^2$$

---

## Physical Intuition / Derivation

### Why Fourier Transform Works

The Fourier transform leverages **orthogonality** of complex exponentials. The key insight is that exponential functions $e^{i\omega t}$ form a complete orthogonal basis:

$$\int_{-\infty}^{\infty} e^{i\omega_1 t} \cdot e^{-i\omega_2 t} dt \propto \delta(\omega_1 - \omega_2)$$

Any signal can be expressed as a superposition (weighted sum) of these basis functions at different frequencies.

### Intuitive Picture

Imagine a **complex musical chord**: it contains multiple pure tones (frequencies) at different amplitudes. The Fourier transform is like a **prism for sound**—it separates the chord into its pure tones. The magnitude $|\hat{f}(\omega)|$ tells you the amplitude of frequency $\omega$; the phase tells you temporal alignment.

### Why Complex Exponentials?

The factor $e^{-i\omega t} = \cos(\omega t) - i\sin(\omega t)$ captures **both amplitude and phase** simultaneously. Using complex notation is mathematically elegant and computationally efficient.

### Boolean Function Perspective

For Boolean functions on the hypercube, the Fourier basis $\chi_S$ consists of **parity functions** (XOR of a subset of variables). This decomposition is powerful because:
- **Low-degree Fourier coefficients** capture the essential "structure" of the function
- **Concentration** of mass at low degrees characterizes learnability
- Rare high-degree terms correspond to complex, noise-like behavior

---

## Applications in Engineering

### Signal Processing & Communications
- **Spectrum analysis**: Identify frequency content of audio, radio, vibration signals
- **Filtering**: Design low-pass, high-pass, and band-pass filters by zeroing unwanted frequencies
- **Data compression**: JPEG, MP3 use Fourier or cosine transforms; most energy concentrates in few low-frequency components
- **Modulation**: Transmit signals by encoding data onto carrier frequencies

### Control Systems
- **Frequency response analysis**: Understand system stability and performance via Bode plots
- **Controller design**: Shape system response across frequency spectrum
- **Feedback stability**: Nyquist criterion uses frequency-domain analysis

### Power Systems & Electrical Engineering
- **Harmonic analysis**: Decompose distorted voltages/currents into fundamental + harmonics
- **Power quality**: Identify and mitigate harmonic pollution
- **Transient response**: Analyze fault conditions using frequency decomposition

### Imaging & Computer Vision
- **Image processing**: Blur, sharpen, denoise via frequency filtering
- **Feature extraction**: Low-frequency components encode shape; high-frequency encode edges
- **Compression**: JPEG uses discrete cosine transform (DCT), a Fourier variant

### Machine Learning & Learning Theory
- **Boolean function learning**: Fourier analysis characterizes function complexity
  - Functions with small $\ell_1$ Fourier norm are efficiently learnable
  - DNF formulas and decision trees have concentrated low-degree Fourier mass
- **Agnostic learning**: Fourier tools bound learning complexity
- **Spectral methods**: Kernel machines and spectral clustering