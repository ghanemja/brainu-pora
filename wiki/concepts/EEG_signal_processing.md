# EEG Signal Processing

## Definition

EEG (electroencephalography) signal processing is the acquisition, conditioning, and analysis of electrical brain activity recorded non-invasively from scalp electrodes. It encompasses the full pipeline from raw voltage measurements through artifact removal, feature extraction, and interpretation for clinical or research applications.

**Core components:**
- **Acquisition**: Multi-channel recordings (typically 8–256 channels) placed according to standardized montages (e.g., 10-20 system)
- **Preprocessing**: Noise reduction, artifact removal, and signal conditioning
- **Analysis**: Feature extraction and computational modeling (spectral analysis, connectivity measures, nonlinear dynamics)
- **Interpretation**: Clinical or functional inference (diagnosis, cognitive state, neural dynamics)

EEG provides millisecond-level temporal resolution of neural population activity, making it valuable for studying dynamic brain processes like attention, cognition, and neurological disorders.

---

## Key Equations

### Sampling and Nyquist Theorem

For a signal sampled at rate $f_s$, the maximum recoverable frequency without aliasing is:

$$f_{\text{Nyquist}} = \frac{f_s}{2}$$

For typical EEG ($f_s = 128 \text{ Hz}$), maximum frequency = 64 Hz.

### Bandpass Filtering

Preprocessed EEG is filtered into frequency bands. A digital filter with transfer function $H(z)$ attenuates unwanted frequencies:

$$Y(z) = H(z) \cdot X(z)$$

Common bands:
- **Delta** ($\delta$): 0.5–4 Hz (sleep, deep brain states)
- **Theta** ($\theta$): 4–8 Hz (drowsiness, meditation)
- **Alpha** ($\alpha$): 8–12 Hz (relaxation, posterior dominant rhythm)
- **Beta** ($\beta$): 12–30 Hz (active cognition, motor activity)
- **Gamma** ($\gamma$): 30–100+ Hz (attention, sensory processing)

### Power Spectral Density

The power in frequency band $[f_1, f_2]$ via Fourier analysis:

$$P(f) = |X(f)|^2$$

where $X(f) = \mathcal{F}\{x(t)\}$ is the Fourier transform. Band power:

$$P_{\text{band}} = \int_{f_1}^{f_2} P(f) \, df$$

### Electrode Reference Montages

**Common reference** (all channels referenced to earlobe or nose):
$$V_{\text{channel}} = V_{\text{electrode}} - V_{\text{reference}}$$

**Laplacian reference** (emphasizes local activity, reduces volume conduction):
$$V_{\text{Laplacian}}(i) = V(i) - \frac{1}{n}\sum_{\text{neighbors}} V(j)$$

---

## Physical Intuition / Derivation

### Why EEG is Noisy

The scalp EEG signal is the *spatially and temporally blurred* superposition of millions of neural dipoles. Key degradation sources:

1. **Volume conduction**: Current spreads through brain tissue, cerebrospinal fluid, and skull, attenuating and spatially smearing signals. A dipole at the cortex appears at multiple electrodes with reduced amplitude.
2. **Skull resistance**: The skull has ~100× higher resistance than brain tissue, further attenuating and low-pass filtering neural signals.
3. **Environmental noise**: Electrical line noise (50/60 Hz), muscle artifacts (EMG), eye movements (EOG), cardiac activity (ECG), and equipment noise.

### Preprocessing Justification

**Artifact removal** is critical because brain signals are $\sim 10\,\mu\text{V}$ while muscle artifacts can be $> 100\,\mu\text{V}$.

**ICA (Independent Component Analysis)** decomposes:
$$X(t) = A \cdot S(t)$$

where $X$ is observed multichannel EEG, $A$ is a mixing matrix, and $S$ contains independent components. Non-brain components (eye blinks, muscle activity) cluster in fast, impulsive ICs and can be removed.

**Filtering philosophy**: Remove frequency content known to be non-neural (line noise at 50/60 Hz, high-frequency muscle activity $> 100$ Hz) while preserving neural signatures in classical bands.

### Signal Model

EEG can be modeled as:

$$x_i(t) = \sum_k a_{ik} s_k(t) + n_i(t)$$

where:
- $x_i(t)$ = signal at electrode $i$
- $s_k(t)$ = activity from neural source $k$ (across brain)
- $a_{ik}$ = volume conduction mixing coefficient (geometry-dependent)
- $n_i(t)$ = noise (artifacts, equipment noise)

The ill-posed *source localization* problem seeks to invert this and estimate $s_k(t)$ from $x_i(t)$.

---

## Applications in Engineering

### Clinical Diagnostics

- **ADHD detection**: Altered alpha/theta power ratios and abnormal connectivity patterns differentiate ADHD from control groups (as in the referenced dataset).
- **Epilepsy monitoring**: Detect seizure onset via sharp wave detection and abnormal spectral patterns.
- **Sleep staging**: Classify sleep stages (N1, N2, N3, REM) using standardized EEG criteria (spindles, K-complexes, slow waves).

### Brain-Computer Interfaces (BCIs)

Extract features from EEG to decode user intent:
- **Motor imagery BCIs**: Modulation of beta/mu rhythms ($8\text{–}12$ Hz) over motor cortex to control prosthetics.
- **P300 spellers**: Exploit event-related potentials (ERP) for character selection.
- **Workload assessment**: Real-time mental workload monitoring via theta/alpha power ratios.

### Cognitive Neuroscience Research

- Study attention mechanisms via event-related potentials (ERPs) and spectral dynamics.
- Investigate nonlinear dynamics of neural circuits (e.g., cross-frequency coupling,