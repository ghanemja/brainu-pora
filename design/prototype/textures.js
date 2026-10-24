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

  // ── Slate chalkboard: green-black stone, grain, eraser swipes, ghost writing, dust ──
  function slate() {
    const W = 1600, H = 820, [c, x] = canvas(W, H), r = rng(7);
    const img = x.createImageData(W, H), d = img.data, n = fbm(W, H, 6, 5, 11), m = fbm(W, H, 2, 3, 23);
    for (let y = 0; y < H; y++) for (let i = 0; i < W; i++) {
      const k = (y * W + i) * 4, v = (n(i, y) - 0.5) * 22 + (m(i, y) - 0.5) * 16 + (r() - 0.5) * 9;
      d[k] = 34 + v; d[k + 1] = 47 + v; d[k + 2] = 41 + v * 0.9; d[k + 3] = 255;
    }
    x.putImageData(img, 0, 0);
    // eraser swipes: broad, soft, mostly horizontal strokes of old chalk
    x.filter = "blur(14px)"; x.lineCap = "round";
    for (let s = 0; s < 46; s++) {
      x.strokeStyle = `rgba(222,230,224,${0.018 + r() * 0.035})`; x.lineWidth = 50 + r() * 110;
      const y0 = r() * H, x0 = r() * W * 0.8, len = 200 + r() * 700;
      x.beginPath(); x.moveTo(x0, y0);
      x.bezierCurveTo(x0 + len * 0.3, y0 + (r() - 0.5) * 90, x0 + len * 0.7, y0 + (r() - 0.5) * 90, x0 + len, y0 + (r() - 0.5) * 60); x.stroke();
    }
    for (let s = 0; s < 10; s++) { // a few circular wipes
      x.strokeStyle = `rgba(222,230,224,${0.02 + r() * 0.03})`; x.lineWidth = 60 + r() * 60;
      x.beginPath(); x.arc(r() * W, r() * H, 60 + r() * 120, r() * 6, r() * 6 + 3 + r() * 3); x.stroke();
    }
    // ghost writing: faint scribbles left after erasing
    x.filter = "blur(1.6px)";
    for (let s = 0; s < 90; s++) {
      x.strokeStyle = `rgba(235,240,235,${0.035 + r() * 0.05})`; x.lineWidth = 2 + r() * 2.5;
      let px = r() * W, py = r() * H; x.beginPath(); x.moveTo(px, py);
      const steps = 6 + (r() * 14) | 0;
      for (let k = 0; k < steps; k++) { const nx = px + 8 + r() * 22, ny = py + (r() - 0.5) * 26; x.quadraticCurveTo(px + (nx - px) / 2, py - 14 + r() * 28, nx, ny); px = nx; py = ny; }
      x.stroke();
    }
    x.filter = "none";
    // chalk dust settles toward the tray
    const g = x.createLinearGradient(0, H * 0.72, 0, H); g.addColorStop(0, "rgba(230,232,226,0)"); g.addColorStop(1, "rgba(230,232,226,0.10)");
    x.fillStyle = g; x.fillRect(0, 0, W, H);
    for (let s = 0; s < 5000; s++) { const yy = H - Math.pow(r(), 2.2) * H * 0.35; x.fillStyle = `rgba(240,240,232,${0.05 + r() * 0.16})`; x.fillRect(r() * W, yy, 1 + r() * 1.6, 1 + r() * 1.6); }
    // fine dust everywhere
    for (let s = 0; s < 9000; s++) { x.fillStyle = `rgba(240,240,232,${r() * 0.06})`; x.fillRect(r() * W, r() * H, 1, 1); }
    // darker toward the frame
    const v = x.createRadialGradient(W / 2, H / 2, H * 0.35, W / 2, H / 2, W * 0.62); v.addColorStop(0, "rgba(0,0,0,0)"); v.addColorStop(1, "rgba(0,0,0,0.38)");
    x.fillStyle = v; x.fillRect(0, 0, W, H);
    return c.toDataURL("image/jpeg", 0.88);
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

  const root = document.documentElement.style;
  const put = (name, url) => root.setProperty(name, `url("${url}")`);
  try {
    put("--tex-paper", paper([251, 249, 241], 31));
    put("--tex-cream", paper([248, 243, 228], 37));
    put("--tex-frame", wood(700, 140, 41, [[146, 94, 54], [104, 62, 30], [70, 38, 16]], 3));
    put("--tex-desk", wood(1200, 600, 53, [[176, 124, 80], [134, 88, 52], [96, 60, 32]], 5));
    put("--tex-wall", wall());
    put("--tex-slate", slate());
    document.documentElement.classList.add("tex-ready");
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
