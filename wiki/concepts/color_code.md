# color code

## Definition

The **color code** is a family of 2-dimensional topological quantum error correction (QEC) codes defined on trivalent lattices (typically triangular or hexagonal lattices) where each qubit is assigned a "color" (red, green, blue) corresponding to its position relative to the lattice geometry. The code encodes logical qubits in a way that exploits the geometric structure to detect and correct errors through stabilizer measurements.

Formally, a color code is a stabilizer code where:
- Stabilizer generators are assigned to vertices and plaquettes of a 2D colored lattice
- The code distance grows with the system size, enabling fault-tolerant quantum computation
- Syndrome measurement reveals the location and type of errors through the pattern of violated stabilizers

The color code is **unitarily equivalent** to multiple copies of the toric code (TC) via constant-depth circuits composed of geometrically-local Clifford gates, meaning their error correction properties are fundamentally related despite different geometric presentations.

## Key Equations

For a color code with code distance $d$, the fundamental performance metrics are:

**Logical Error Rate Threshold:**
$$P_L \approx c \left(\frac{p}{p_{th}}\right)^{\alpha}$$

where $p$ is the physical error rate, $p_{th}$ is the threshold error rate, $c$ is a constant, and $\alpha$ is the exponent characterizing sub-threshold performance.

**Error Correction Capability:**
A color code can correct errors of weight up to $\lfloor (d-1)/2 \rfloor$, where $d$ is the code distance.

**Polynomial Representation:**
2D topologically-translationally-invariant (TTI) codes, including color codes, admit a polynomial representation over $\mathbb{F}_2[x, y]$ where the syndrome structure encodes algebraic properties of the code.

## Physical Intuition / Derivation

### Geometric Structure
The color code is constructed on a 2D lattice where each face is colored with one of three colors such that no two adjacent faces share the same color. Qubits live on edges, and stabilizer generators are assigned to vertices and colored plaquettes. This tripartite structure is essential: the three colors correspond to three independent "copy-like" structures that together form the full code.

### Relationship to the Toric Code
The unitary equivalence between color codes and the toric code is the key to understanding their decoding. A color code on a trivalent lattice can be decomposed into three copies of the toric code through a local change of basis (a constant-depth circuit of local Clifford gates). This means:

1. **Syndrome measurement** in the color code reveals the same topological information as three coupled toric codes
2. **Error correction** problems reduce to identifying excitations in the toric code picture
3. **Graph-matching decoders** designed for the toric code can be adapted by "coarse-graining" the color code back to the toric code picture

### Coarse-Graining Strategy
The decoding process works as follows:

1. Measure syndromes in the color code (pattern of violated stabilizers)
2. Map this syndrome to the effective toric code picture via the unitary equivalence
3. Apply a graph-matching decoder to identify the lowest-weight correction in the toric code space
4. Map the correction back to the original color code qubits using the inverse unitary transformation

This procedure is efficient because the graph-matching problem on the toric code (minimum-weight perfect matching) runs in polynomial time, typically scaling as $O(n^3)$ or better for practical implementations.

## Applications in Engineering

### Quantum Error Correction Protocols
- **Practical QEC implementation:** Color codes offer advantages over surface codes in some architectural constraints because errors can be corrected at higher rates for certain noise models
- **Hardware-efficient decoding:** The unitary equivalence to toric codes allows reuse of well-optimized graph-matching decoders
- **Fault-tolerant quantum computing:** Provides the foundation for logical qubit operations with provable error thresholds

### Decoder Development
- **Graph-matching decoders:** Applied to color codes (particularly the Bacon-Bacon family) on codes like distance-12 on 12×6 lattices and distance-24 on 24×24 lattices
- **Comparison with neural decoders:** Benchmarked against belief propagation (BP) and BP-ordered statistics decoders (BP-OSD)
- **Noise-specific optimization:** Variants tailored for phase-flip or bit-flip dominated noise environments

### Code-Capacity Studies
- Numerical investigations of threshold behavior under independent and identically distributed (i.i.d.) error models
- Systematic evaluation of logical error rates as a function of physical error probability

## Common Mistakes / Pitfalls

1. **Confusing color with qubit location:** The color labels refer to *faces* or *regions* of the lattice, not individual qubits. Qubits sit on edges/vertices, and colors determine which stabilizers are measured.

2. **Assuming independent decoding:** Color code errors cannot be decoded independently per color; the three copies are coupled, and corrections must account for this global structure.

3. **Misinterpreting unitary equivalence:** The equivalence to toric codes does not mean color codes *are* toric codes—only that their syndrome structure can be mapped to toric code excitations via a fixed change of basis. The physical implementation differs.

4. **Overlooking coarse-graining overhead:** Converting between color code and toric code pictures for decoding introduces latency; real-time syndrome extraction must account for this.

5. **Confusing code distance definitions:** The distance of a color code depends on the specific lattice geometry; codes with the same polynomial representation may have different distances on different lattices (e.g., distance-12 vs. distance-24).

6. **Assuming BP-OSD performance:** While graph-matching decoders are efficient, belief propagation with ordered statistics decoders (BP-OSD) often outperform them at high logical error rates, though with higher computational cost. Trade-offs must be problem-specific.

## See Also

- [[toric code]] — the canonical 2D topological code to which color codes are unitarily equivalent
- [[stabilizer codes]] — the broader framework of which color codes are a specific instance
- [[minimum-weight perfect matching]] — the graph algorithm underlying efficient color code decoders
- [[quantum error