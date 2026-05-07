

<!-- merged 20260501_014646 by aerospace: Bridges aerospace control principles (latency budgeting, bandwidth hierarchy) and mobile manipulation; provides quantitative reference for conveyor-picking systems. -->
## Control Bandwidth and Latency Coupling in Mobile/Moving-Target Tasks

When a controller must track a moving target (e.g., conveyor belt at velocity $v_{\text{belt}}$), the **positional slip per control cycle** is:

$$\Delta x_{\text{slip}} = v_{\text{belt}} \cdot \tau_{\text{latency}}$$

For $v_{\text{belt}} = 1$ m/s and $\tau_{\text{latency}} = 50$ ms:
$$\Delta x_{\text{slip}} = 1 \text{ m/s} \times 0.05 \text{ s} = 0.05 \text{ m} = 5 \text{ cm}$$

To keep positional error within acceptable bounds (e.g., <5 cm for a 0–2 kg pick task), the total loop latency must be **tightly budgeted**. A typical allocation:
- Sensor acquisition: 10 ms
- Controller decision: 20 ms  
- Actuator response: 10 ms
- Safety margin: 10 ms
- **Total: ≤50 ms**

The **inner servo loop** (joint-level feedback) should run at ≥200 Hz (τ_inner ≤ 5 ms) to support outer-loop task commands at ≥50 Hz (τ_outer ≈ 20 ms).

This mirrors aerospace practice in high-bandwidth flight control: latency directly erodes stability margin.
|
