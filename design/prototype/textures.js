/* Procedural material textures for the prototype: slate chalkboard, wood (frame
 * and desk) and paper. Painted once on canvases at load, then exposed as CSS
 * custom properties (--tex-slate, --tex-frame, --tex-desk, --tex-paper,
 * --tex-cream) so the stylesheet can use them like any background image.
 * Also injects the SVG filter that gives text a chalky, broken stroke. */
(function () {
  "use strict";
  // Small seeded RNG so the materials look the same on every load.
  const rng = (seed) => () => { seed |= 0; seed = (seed + 0x6d2b79f5) | 0; let t = Math.imul(seed ^ (seed >>> 15), 1 | seed); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };

  // Tileable value noise with smooth interpolation; fbm sums a few octaves.
  function noise2(cells, seed) {
    const r = rng(seed), g = new Float32Array(cells * cells);
    for (let i = 0; i < g.length; i++) g[i] = r();
    const at = (x, y) => g[(((y % cells) + cells) % cells) * cells + (((x % cells) + cells) % cells)];
    const s = (t) => t * t * (3 - 2 * t);
    return (x, y) => { const xi = Math.floor(x), yi = Math.floor(y), xf = s(x - xi), yf = s(y - yi);
      const a = at(xi, yi), b = at(xi + 1, yi), c = at(xi, yi + 1), d = at(xi + 1, yi + 1);
      return a + (b - a) * xf + (c - a) * yf + (a - b - c + d) * xf * yf; };
  }
  function fbm(w, h, base, octaves, seed) {
    const layers = []; for (let o = 0; o < octaves; o++) layers.push(noise2(base << o, seed + o * 101));
    return (x, y) => { let v = 0, amp = 0.5, tot = 0; for (let o = 0; o < octaves; o++) { const f = (base << o); v += layers[o](x / w * f, y / h * f) * amp; tot += amp; amp *= 0.5; } return v / tot; };
  }
  const canvas = (w, h) => { const c = document.createElement("canvas"); c.width = w; c.height = h; return [c, c.getContext("2d")]; };

  // ── Slate chalkboard ──
  // Real boards read as: fine stone tooth, soft cloudiness, streaky felt-eraser
  // smears (parallel streaks, ragged ends), half-erased old writing, and dust.
  // Low-frequency layers are painted small and scaled up; grain is per pixel.
  function slate() {
    const W = 2048, H = 1024, [c, x] = canvas(W, H), r = rng(7);
    x.fillStyle = "#25312c"; x.fillRect(0, 0, W, H);
    // soft cloudiness
    { const w = 256, h = 128, [m, mx] = canvas(w, h), n = fbm(w, h, 3, 4, 11), img = mx.createImageData(w, h), d = img.data;
      for (let y = 0; y < h; y++) for (let i = 0; i < w; i++) { const k = (y * w + i) * 4, v = n(i, y);
        d[k] = d[k + 1] = d[k + 2] = v > 0.5 ? 235 : 0; d[k + 3] = Math.abs(v - 0.5) * 70; }
      mx.putImageData(img, 0, 0); x.imageSmoothingQuality = "high"; x.drawImage(m, 0, 0, W, H); }
    const chalk = (a) => `rgba(226,232,226,${a})`;
    // old writing, then mostly wiped away
    const ghost = (() => {
      const [g, gx] = canvas(W, H), lines = ["x_dot = A x + B u", "P(x | z) ∝ P(z | x) P(x)", "K = P Hᵀ (H P Hᵀ + R)⁻¹", "q = (x, y, θ)", "min Σ xᵀQx + uᵀRu", "v = r ω", "J(θ) = E[Σ γᵗ r]", "∇f = 0", "SE(2)", "x_{k+1} = f(x_k, u_k)", "ẋ = v cos θ"];
      gx.fillStyle = chalk(1); gx.strokeStyle = chalk(1); gx.lineCap = "round";
      for (let s = 0; s < 26; s++) {
        gx.globalAlpha = 0.05 + r() * 0.09; gx.save(); gx.translate(r() * W * 0.9, 60 + r() * (H - 120)); gx.rotate((r() - 0.5) * 0.06);
        if (s % 5 === 4) { // a little diagram: axes with a curve, or a robot circle and heading
          gx.lineWidth = 3; gx.beginPath();
          if (r() < 0.5) { gx.moveTo(0, 0); gx.lineTo(0, -120); gx.moveTo(0, 0); gx.lineTo(180, 0); gx.moveTo(6, -10); gx.bezierCurveTo(60, -140, 110, -20, 170, -70); }
          else { gx.arc(60, -50, 44, 0, Math.PI * 2); gx.moveTo(60, -50); gx.lineTo(130, -80); }
          gx.stroke();
        } else { gx.font = `${38 + r() * 34}px Kalam, Caveat, cursive`; gx.fillText(lines[s % lines.length], 0, 0); }
        gx.restore();
      }
      gx.globalAlpha = 1; gx.globalCompositeOperation = "destination-out"; // the eraser took most of it
      for (let y = 0; y < H; y += 2) { gx.fillStyle = `rgba(0,0,0,${0.35 + r() * 0.6})`; gx.fillRect(0, y, W, 2 + r() * 3); }
      return g;
    })();
    x.filter = "blur(1.2px)"; x.drawImage(ghost, 0, 0); x.filter = "none";
    // felt-eraser smears: bands of thin parallel streaks with ragged ends
    for (let s = 0; s < 34; s++) {
      const bw = 260 + r() * 700, bh = 50 + r() * 120, strength = 0.014 + r() * 0.026;
      x.save(); x.translate(r() * W, r() * H); x.rotate((r() - 0.5) * 0.22 + (r() < 0.15 ? (r() - 0.5) * 1.2 : 0));
      for (let y = -bh / 2; y < bh / 2; y += 1.3) {
        const env = Math.sin(Math.PI * (y / bh + 0.5)), a = strength * env * (0.4 + r() * 1.2);
        const x0 = -bw / 2 + (r() - 0.5) * 80, x1 = bw / 2 + (r() - 0.5) * 80;
        x.fillStyle = chalk(a); x.fillRect(x0, y, x1 - x0, 1.1 + r());
      }
      x.restore();
    }
    // chalk dust settles toward the tray
    const g = x.createLinearGradient(0, H * 0.78, 0, H); g.addColorStop(0, chalk(0)); g.addColorStop(1, chalk(0.08));
    x.fillStyle = g; x.fillRect(0, 0, W, H);
    // stone tooth and dust specks, per pixel (also breaks up any banding)
    const img = x.getImageData(0, 0, W, H), d = img.data;
    for (let k = 0; k < d.length; k += 4) {
      const p = k / 4, yy = (p / W) | 0, q = r();
      let v = (q - 0.5) * 11;
      if (q > 0.9985 - (yy > H * 0.85 ? 0.004 : 0)) v += 40 + r() * 60; // a speck of chalk
      else if (q < 0.0015) v -= 18; // a pit in the slate
      d[k] += v; d[k + 1] += v; d[k + 2] += v * 0.95;
    }
    x.putImageData(img, 0, 0);
    // a touch darker toward the frame
    const v = x.createRadialGradient(W / 2, H * 0.45, H * 0.4, W / 2, H / 2, W * 0.6); v.addColorStop(0, "rgba(0,0,0,0)"); v.addColorStop(1, "rgba(0,0,0,0.3)");
    x.fillStyle = v; x.fillRect(0, 0, W, H);
    return c;
  }

  // ── Wood: warped grain bands with pores and growth rings ──
  function wood(W, H, seed, palette, scaleY) {
    const [c, x] = canvas(W, H), r = rng(seed), img = x.createImageData(W, H), d = img.data;
    const warp = fbm(W, H, 4, 4, seed + 3), fine = fbm(W, H, 32, 2, seed + 9);
    const [a, b, k] = palette; // light, dark, line
    for (let y = 0; y < H; y++) for (let i = 0; i < W; i++) {
      const w = warp(i, y), t = Math.sin((y / H * scaleY + w * 3.2) * Math.PI * 2) * 0.5 + 0.5;
      const ring = Math.pow(Math.abs(Math.sin((y / H * scaleY * 2.3 + w * 5.1) * Math.PI)), 18);
      const f = (fine(i, y) - 0.5) * 0.25, mix = Math.min(1, Math.max(0, t * 0.7 + f + 0.15));
      const p = (y * W + i) * 4, pore = r() < 0.004 ? 0.35 : 0;
      for (let ch = 0; ch < 3; ch++) d[p + ch] = (a[ch] * (1 - mix) + b[ch] * mix) * (1 - ring * 0.32 - pore) + k[ch] * ring * 0.32;
      d[p + 3] = 255;
    }
    x.putImageData(img, 0, 0);
    return c.toDataURL("image/jpeg", 0.9);
  }

  // ── Paper: warm stock with fibres and a little tooth ──
  function paper(base, seed) {
    const S = 384, [c, x] = canvas(S, S), r = rng(seed), img = x.createImageData(S, S), d = img.data, n = fbm(S, S, 8, 4, seed + 1);
    for (let y = 0; y < S; y++) for (let i = 0; i < S; i++) {
      const p = (y * S + i) * 4, v = (n(i, y) - 0.5) * 10 + (r() - 0.5) * 7;
      d[p] = base[0] + v; d[p + 1] = base[1] + v; d[p + 2] = base[2] + v * 0.8; d[p + 3] = 255;
    }
    x.putImageData(img, 0, 0);
    for (let s = 0; s < 420; s++) { // fibres
      const len = 4 + r() * 14, ang = r() * Math.PI, px = r() * S, py = r() * S;
      x.strokeStyle = r() < 0.5 ? `rgba(120,100,70,${0.05 + r() * 0.07})` : `rgba(255,255,255,${0.15 + r() * 0.2})`; x.lineWidth = 0.6;
      x.beginPath(); x.moveTo(px, py); x.quadraticCurveTo(px + Math.cos(ang) * len / 2 + (r() - 0.5) * 3, py + Math.sin(ang) * len / 2 + (r() - 0.5) * 3, px + Math.cos(ang) * len, py + Math.sin(ang) * len); x.stroke();
    }
    return c.toDataURL("image/png");
  }

  // ── Painted plaster wall: soft roller mottling, a little grit ──
  function wall() {
    const S = 512, [c, x] = canvas(S, S), r = rng(61), img = x.createImageData(S, S), d = img.data;
    const big = fbm(S, S, 3, 4, 63), grit = fbm(S, S, 48, 2, 67);
    for (let y = 0; y < S; y++) for (let i = 0; i < S; i++) {
      const p = (y * S + i) * 4, v = (big(i, y) - 0.5) * 14 + (grit(i, y) - 0.5) * 9 + (r() - 0.5) * 4;
      d[p] = 206 + v; d[p + 1] = 208 + v; d[p + 2] = 192 + v * 0.9; d[p + 3] = 255;
    }
    x.putImageData(img, 0, 0);
    return c.toDataURL("image/jpeg", 0.9);
  }

  // ── Cork: warm granules, dark flecks, pin holes ──
  function cork() {
    const S = 420, [c, x] = canvas(S, S), r = rng(71), n = fbm(S, S, 6, 3, 73), img = x.createImageData(S, S), d = img.data;
    for (let y = 0; y < S; y++) for (let i = 0; i < S; i++) {
      const p = (y * S + i) * 4, v = (n(i, y) - 0.5) * 30 + (r() - 0.5) * 26;
      d[p] = 184 + v; d[p + 1] = 136 + v * 0.85; d[p + 2] = 86 + v * 0.6; d[p + 3] = 255;
    }
    x.putImageData(img, 0, 0);
    for (let k = 0; k < 2600; k++) { const rad = 0.6 + r() * 2.2; x.fillStyle = r() < 0.55 ? `rgba(90,52,22,${0.25 + r() * 0.4})` : `rgba(235,200,150,${0.2 + r() * 0.35})`;
      x.beginPath(); x.ellipse(r() * S, r() * S, rad, rad * (0.5 + r() * 0.6), r() * 3, 0, Math.PI * 2); x.fill(); }
    for (let k = 0; k < 40; k++) { x.fillStyle = "rgba(40,22,8,.55)"; x.beginPath(); x.arc(r() * S, r() * S, 0.9, 0, Math.PI * 2); x.fill(); }
    return c.toDataURL("image/jpeg", 0.9);
  }

  const root = document.documentElement.style;
  const put = (name, url) => root.setProperty(name, `url("${url}")`);
  try {
    put("--tex-paper", paper([251, 249, 241], 31));
    put("--tex-cream", paper([248, 243, 228], 37));
    put("--tex-frame", wood(700, 140, 41, [[146, 94, 54], [104, 62, 30], [70, 38, 16]], 3));
    put("--tex-desk", wood(1200, 600, 53, [[176, 124, 80], [134, 88, 52], [96, 60, 32]], 5));
    put("--tex-wall", wall());
    put("--tex-cork", cork());
    document.documentElement.classList.add("tex-ready");
    // The slate writes old chalk in Kalam, so wait (briefly) for the font.
    const paintSlate = () => slate().toBlob((b) => b && put("--tex-slate", URL.createObjectURL(b)), "image/jpeg", 0.9);
    const fonts = document.fonts ? document.fonts.load("48px Kalam") : Promise.resolve();
    Promise.race([fonts, new Promise((ok) => setTimeout(ok, 1500))]).then(paintSlate, paintSlate);
  } catch (e) { /* canvas unavailable: the stylesheet's flat colors still apply */ }

  // Chalk: grainy, broken strokes with a slightly uneven edge.
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false"><defs>
    <filter id="chalk" x="-4%" y="-8%" width="108%" height="116%" color-interpolation-filters="sRGB">
      <feTurbulence type="fractalNoise" baseFrequency="1.35" numOctaves="2" seed="4" result="grain"/>
      <feColorMatrix in="grain" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  2.4 0 0 0 -0.62" result="holes"/>
      <feComposite in="SourceGraphic" in2="holes" operator="in" result="grainy"/>
      <feTurbulence type="fractalNoise" baseFrequency="0.06" numOctaves="2" seed="9" result="wob"/>
      <feDisplacementMap in="grainy" in2="wob" scale="1.6" xChannelSelector="R" yChannelSelector="G" result="rough"/>
      <feGaussianBlur in="rough" stdDeviation="0.35" result="soft"/>
      <feMerge><feMergeNode in="soft"/><feMergeNode in="rough"/></feMerge>
    </filter></defs></svg>`;
  const add = () => document.body.insertAdjacentHTML("afterbegin", svg);
  if (document.body) add(); else document.addEventListener("DOMContentLoaded", add, { once: true });
})();
