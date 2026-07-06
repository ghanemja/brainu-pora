# Self-hosted vendor bundles (docs/HARDENING.md Phase 5)

Pinned UMD builds, committed so the deployed frontend loads **no CDN at
runtime**. Versions match the CDN pins in `design/Brain University.html`
(which remain as the zero-build dev fallback when `design/.compiled/` is
absent).

| File | Package | Source | sha384 |
|---|---|---|---|
| `react.production.min.js` | react@18.3.1 | unpkg.com/react@18.3.1/umd/react.production.min.js | `DGyLxAyjq0f9SPpVevD6IgztCFlnMF6oW/XQGmfe+IsZ8TqEiDrcHkMLKI6fiB/Z` |
| `react-dom.production.min.js` | react-dom@18.3.1 | unpkg.com/react-dom@18.3.1/umd/react-dom.production.min.js | `gTGxhz21lVGYNMcdJOyq01Edg0jhn/c22nsx0kyqP0TxaV5WVdsSH1fSDUf5YJj1` |
| `babel.min.js` | @babel/standalone@7.29.0 | unpkg.com/@babel/standalone@7.29.0/babel.min.js | `m08KidiNqLdpJqLq95G/LEi8Qvjl/xUYll3QILypMoQ65QorJ9Lvtp2RXYGBFj1y` |
| `three.min.js` | three@0.150.0 | unpkg.com/three@0.150.0/build/three.min.js | `T0aPHVj59bnuhOH27TkOKoOaIHLx4bJRRV5UJ6/O48mVZw8wzfoxtFfsyOSg1T74` |
| `3d-force-graph.min.js` | 3d-force-graph@1.73.4 | unpkg.com/3d-force-graph@1.73.4/dist/3d-force-graph.min.js | `GNPicn8pBA2/PGSyPTpxIlPurgLUYcNYJ2zskIq782dE9+gp5E32WSyuxZqA7J+u` |

Notes:

- `babel.min.js` byte-matches the SRI hash pinned in the HTML's dev-mode CDN
  tag (`sha384-m08Ki...`). It is vendored as an offline/dev fallback only —
  the production path loads precompiled `.compiled/*.js` and never loads
  Babel at all.
- React/react-dom here are the **production** builds; dev mode deliberately
  keeps the CDN *development* builds for readable errors.
- To re-verify any file:
  `openssl dgst -sha384 -binary FILE | openssl base64 -A`
