# Plancherel Theorem

## Definition

The **Plancherel theorem** states that the $L^2$ norm of a function equals the $L^2$ norm of its Fourier transform (up to a scaling constant). For a function $f: \mathbb{R} \to \mathbb{C}$, this establishes an isometry between the time domain and frequency domain under the $L^2$ metric.

More formally: if $\hat{f}(\omega)$ denotes the Fourier transform of $f(t)$, then

$$\int_{-\infty}^{\infty} |f(t)|^2 \, dt = \frac{1}{2\pi} \int_{-\infty}^{\infty} |\hat{f}(\omega)|^2 \, d\omega$$

(The scaling factor $1/2\pi$ depends on the Fourier transform convention used.)

## Key Equations

**Standard formulation (with angular frequency $\omega$):**
$$\|f\|_{L^2(\mathbb{R})}^2 = \frac{1}{2\pi} \|\hat{f}\|_{L^2(\mathbb{R})}^2$$

**Characteristic function version** (used in probability):
For random variable $X$ with characteristic function $\phi(\omega) = \mathbb{E}[e^{i\omega X}]$,
$$\|f_X\|_{L^2}^2 = \frac{1}{2\pi} \|\phi_X\|_{L^2}^2$$

**Parseval's identity** (equivalent form for inner products):
$$\langle f, g \rangle_{L^2} = \frac{1}{2\pi} \langle \hat{f}, \hat{g} \rangle_{L^2}$$

**Discrete version** (finite-length signals):
$$\sum_{n=0}^{N-1} |f[n]|^2 = \frac{1}{N} \sum_{k=0}^{N-1} |F[k]|^2$$

where $F[k]$ is the DFT of $f[n]$.

## Physical Intuition / Derivation

### Energy Conservation Principle

The Plancherel theorem embodies **energy conservation**: the total energy of a signal is the same whether measured in the time domain or the frequency domain. If you sum up all the squared amplitudes in time, you get the same result as summing squared amplitudes across all frequencies.

### Geometric Interpretation

The Fourier transform is a **linear operator** that maps functions in $L^2(\mathbb{R})$ to other functions in $L^2(\mathbb{R})$. Plancherel's theorem asserts this operator is an **isometry**—it preserves distances and lengths. This means:

- Orthogonal functions in time remain orthogonal in frequency
- The "magnitude" of a signal is intrinsic and independent of representation
- No information is lost in the transformation (it's invertible)

### Derivation Sketch

Starting from the orthogonality of complex exponentials:
$$\int_{-\infty}^{\infty} e^{i\omega t} e^{-i\omega' t} \, dt = 2\pi \delta(\omega - \omega')$$

And the Fourier inversion formula:
$$f(t) = \frac{1}{2\pi} \int_{-\infty}^{\infty} \hat{f}(\omega) e^{i\omega t} \, d\omega$$

One can compute:
$$\|f\|_{L^2}^2 = \langle f, f \rangle = \left\langle f, \frac{1}{2\pi}\int \hat{f}(\omega) e^{i\omega t} d\omega \right\rangle$$

By Fubini and orthogonality, this yields the Plancherel identity.

## Applications in Engineering

### Signal Processing & Communications
- **Energy computation**: Computing signal power directly from frequency-domain measurements (spectrum analyzers, power spectral density)
- **Filter design**: Ensuring energy constraints in frequency response
- **Data compression**: Identifying which frequency components carry most energy for lossy compression

### Robust Statistics & Contamination Analysis
- **Hypothesis testing under contamination**: Controlling total variation distance between probability distributions via their characteristic functions (as in the source material)
- **Robustness certification**: Bounding statistical complexity using $L^2$ distance of Fourier transforms
- **Mean estimation under model mismatch**: Using frequency-domain analysis to establish sample complexity lower bounds

### Quantum Mechanics & Quantum Computing
- **Uncertainty principle**: Plancherel underpins Heisenberg's uncertainty—concentrated signals in time must be spread in frequency
- **State analysis**: Energy conservation in quantum state transformations

### Image & Audio Processing
- **JPEG/MP3 compression**: Discarding small-magnitude frequency components preserves most energy
- **Noise reduction**: Spectral methods leverage energy localization
- **Feature extraction**: Identifying dominant frequencies (e.g., pitch detection in audio)

### Control Theory
- **Frequency response analysis**: Relating time-domain stability margins to frequency-domain gain
- **Energy-optimal control**: Computing minimal control effort using frequency-domain norms

### Harmonic Analysis & Approximation Theory
- **Orthogonal decomposition**: Constructing bases with controlled energy in specified frequency bands
- **Sampling theory**: Whittaker-Shannon interpolation relies on Plancherel for perfect reconstruction guarantees

## Common Mistakes / Pitfalls

### 1. Forgetting the Scaling Factor
Many students write $\|f\|_{L^2} = \|\hat{f}\|_{L^2}$ without the $1/2\pi$ factor. This works only in some conventions (e.g., physics with angular frequency vs. signal processing with normalized frequency).
- **Fix**: Always verify the convention used in your textbook/field.

### 2. Confusing with Fourier Inversion
Plancherel is *not* the Fourier inversion formula. It guarantees that the transform is an isometry, but doesn't directly give you $f$ from $\hat{f}$.

###