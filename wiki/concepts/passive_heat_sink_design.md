

<!-- merged 20260430_233934 by aerospace: Provides worked example linking thermal resistance budget to practical fin geometry and material selection. -->
## Example: 50W LED Array, 85°C Junction, 25°C Ambient

  **Required R_total = (85 − 25) / 50 = 1.2 K/W**

  Typical allocation (aluminum 6061-T6):
  - R_j-to-c (LED package): 0.15 K/W
  - R_interface (thermal paste, 0.5 mm): 0.08 K/W
  - R_sink (finned Al, natural convection): **0.97 K/W** (limiting term)

  For R_sink ≤ 1.0 K/W with h ≈ 75 W/m²K (natural convection) and η_f ≈ 0.75:
  - Required A_eff = 1 / (75 × 0.75) ≈ **0.18 m²** (bare metal equivalent)
  - With pin fins (ϕ 4 mm, L 25 mm, 20 mm pitch): physical area ≈ **0.8–1.0 m²** (accounting for base plate + 60–80 pins)

  Material choices: Al 6061-T6 (k = 167 W/m·K, cost-effective) vs. Cu (k = 400 W/m·K, heavier).
